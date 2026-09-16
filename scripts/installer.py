#!/usr/bin/env python3
"""Install verified locale artifacts from an immutable release namespace.

This file is published as a release asset. It must stay self-contained:
it may only use the Python standard library and never import sibling
modules, because users download it alone before a release is trusted.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Optional, Sequence

SCHEMA_VERSION = 1
INSTALLER_ASSET = "installer.py"
MANIFEST_ASSET = "release-manifest.json"
SUMS_ASSET = "SHA256SUMS"
MANIFEST_MAX_BYTES = 10 * 1024 * 1024
SUMS_MAX_BYTES = 1024 * 1024
ARCHIVE_MAX_BYTES = 64 * 1024 * 1024
FILE_MODE = 0o644
FILE_MODE_INT = 0o644
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ARCHIVE_TIMESTAMP_TEXT = "1980-01-01T00:00:00Z"
FETCH_TIMEOUT = 60.0
LATEST_VERSION = "latest"
USER_AGENT = "coding-agent-docs-template-installer"
SEMVER_RE = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
REPOSITORY_RE = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?"
)
LOCALE_KEY_RE = re.compile(
    r"[a-z]{2,3}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|[0-9]{3}))?"
)
SHA256_RE = re.compile(r"[0-9a-f]{64}")
LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


class InstallerError(ValueError):
    """Raised when a release asset or target tree violates the contract."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validated_version_selection(value: str) -> str:
    if value == LATEST_VERSION:
        return value
    if SEMVER_RE.fullmatch(value) is None:
        raise InstallerError("version must be 'latest' or full SemVer without a leading v prefix")
    return value


def _validated_release_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise InstallerError("release URL must be an absolute http(s) URL")
    if "@" in parsed.netloc or parsed.username or parsed.password:
        raise InstallerError("release URL must not contain credentials")
    if parsed.query or parsed.fragment:
        raise InstallerError("release URL must not contain a query or fragment")
    if parsed.scheme != "https" and parsed.hostname not in LOCAL_HOSTS:
        raise InstallerError("release URL must use https except on localhost")
    segments = [segment for segment in parsed.path.split("/") if segment]
    if any(segment in (".", "..") for segment in segments):
        raise InstallerError("release URL path must not contain . or .. segments")
    return value.rstrip("/")


def _asset_url(release_url: str, version: str, name: str) -> str:
    return "%s/%s/%s" % (release_url, version, name)


def _fetch(url: str, max_bytes: int) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT}, method="GET"
    )
    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
            if response.status != 200:
                raise InstallerError(
                    "release asset request failed: HTTP %s for %s" % (response.status, url)
                )
            length = response.headers.get("Content-Length")
            if length is not None:
                if not length.isdigit():
                    raise InstallerError(
                        "release server sent a non-integer Content-Length for %s" % url
                    )
                if int(length) > max_bytes:
                    raise InstallerError(
                        "release asset exceeds the %d byte download limit: %s"
                        % (max_bytes, url)
                    )
            chunks = []
            total = 0
            while True:
                chunk = response.read(min(65536, max_bytes + 1))
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise InstallerError(
                        "release asset exceeds the %d byte download limit: %s"
                        % (max_bytes, url)
                    )
                chunks.append(chunk)
    except urllib.error.HTTPError as exc:
        raise InstallerError("release asset request failed: HTTP %s for %s" % (exc.code, url)) from exc
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        raise InstallerError("cannot fetch release asset %s: %s" % (url, exc)) from exc
    return b"".join(chunks)


def _parsed_json(data: bytes, description: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise InstallerError("%s is not valid UTF-8 JSON: %s" % (description, exc)) from exc


def _validated_manifest(manifest: Any) -> Mapping[str, Any]:
    if not isinstance(manifest, dict):
        raise InstallerError("release manifest must be an object")
    if set(manifest) != {
        "schema_version",
        "version",
        "source_commit",
        "repository",
        "locales",
        "installer",
    }:
        raise InstallerError("release manifest has unexpected top-level keys")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise InstallerError("unsupported release manifest schema_version")
    if SEMVER_RE.fullmatch(manifest["version"]) is None:
        raise InstallerError("release manifest version must be full SemVer")
    if COMMIT_RE.fullmatch(manifest["source_commit"]) is None:
        raise InstallerError("release manifest source_commit must be 40 lowercase hex characters")
    if REPOSITORY_RE.fullmatch(manifest["repository"]) is None:
        raise InstallerError("release manifest repository must be an OWNER/NAME slug")
    _validated_installer_record(manifest["installer"])
    if not isinstance(manifest["locales"], dict) or not manifest["locales"]:
        raise InstallerError("release manifest locales must be a non-empty object")
    for tag, record in manifest["locales"].items():
        if LOCALE_KEY_RE.fullmatch(tag) is None:
            raise InstallerError("unsupported locale tag in release manifest: %s" % tag)
        _validated_locale_record(tag, record, manifest["version"])
    return manifest


def _validated_installer_record(record: Any) -> None:
    if not isinstance(record, dict) or set(record) != {"asset", "sha256", "bytes"}:
        raise InstallerError("release manifest installer record is invalid")
    if record["asset"] != INSTALLER_ASSET:
        raise InstallerError("release manifest installer asset must be %s" % INSTALLER_ASSET)
    if not isinstance(record["sha256"], str) or SHA256_RE.fullmatch(record["sha256"]) is None:
        raise InstallerError("release manifest installer sha256 is invalid")
    if isinstance(record["bytes"], bool) or not isinstance(record["bytes"], int) or record["bytes"] < 1:
        raise InstallerError("release manifest installer bytes is invalid")
    if record["bytes"] > MANIFEST_MAX_BYTES:
        raise InstallerError("release installer exceeds the download size limit")


def _validated_locale_record(tag: str, record: Any, version: str) -> None:
    if not isinstance(record, dict):
        raise InstallerError("locale record must be an object: %s" % tag)
    if set(record) != {"status", "asset", "sha256", "bytes", "compression", "members"}:
        raise InstallerError("locale record has unexpected keys: %s" % tag)
    if record["status"] != "complete":
        raise InstallerError("locale %s is not complete" % tag)
    expected_asset = "coding-agent-docs-template-%s-v%s.zip" % (tag, version)
    if record["asset"] != expected_asset:
        raise InstallerError(
            "locale %s asset name does not bind the locale and version: %s"
            % (tag, record["asset"])
        )
    if not isinstance(record["sha256"], str) or SHA256_RE.fullmatch(record["sha256"]) is None:
        raise InstallerError("locale %s archive sha256 is invalid" % tag)
    if (
        isinstance(record["bytes"], bool)
        or not isinstance(record["bytes"], int)
        or not 1 <= record["bytes"] <= ARCHIVE_MAX_BYTES
    ):
        raise InstallerError("locale %s archive size is outside the download limit" % tag)
    if record["compression"] != "stored":
        raise InstallerError("locale %s archive must use stored compression" % tag)
    members = record["members"]
    if not isinstance(members, list) or not members:
        raise InstallerError("locale %s must declare at least one member" % tag)
    for member in members:
        _validated_member_record(tag, member)
    paths = [member["path"] for member in members]
    if len(set(paths)) != len(paths):
        raise InstallerError("locale %s declares duplicate member paths" % tag)
    if len({path.lower() for path in paths}) != len(paths):
        raise InstallerError("locale %s declares case-fold colliding member paths" % tag)
    for path in paths:
        _validated_member_path(path)


def _validated_member_record(tag: str, member: Any) -> None:
    if not isinstance(member, dict) or set(member) != {"path", "sha256", "bytes", "mode", "timestamp"}:
        raise InstallerError("locale %s has an invalid member record" % tag)
    if not isinstance(member["path"], str) or SHA256_RE.fullmatch(member["sha256"]) is None:
        raise InstallerError("locale %s has an invalid member hash" % tag)
    if (
        isinstance(member["bytes"], bool)
        or not isinstance(member["bytes"], int)
        or member["bytes"] < 0
    ):
        raise InstallerError("locale %s has an invalid member size" % tag)
    if member["mode"] != FILE_MODE_INT:
        raise InstallerError("locale %s member mode must be 0644" % tag)
    if member["timestamp"] != ARCHIVE_TIMESTAMP_TEXT:
        raise InstallerError("locale %s member timestamp must be %s" % (tag, ARCHIVE_TIMESTAMP_TEXT))


def _validated_member_path(path: str) -> PurePosixPath:
    if "\\" in path or "\x00" in path:
        raise InstallerError("member path must not contain backslashes or NUL: %s" % path)
    segments = path.split("/")
    if not all(segments):
        raise InstallerError("member path must be a non-empty relative path: %s" % path)
    if any(segment in (".", "..") for segment in segments):
        raise InstallerError("member path must not contain . or .. segments: %s" % path)
    return PurePosixPath(path)


def _validated_sums(data: bytes) -> Mapping[str, str]:
    try:
        text = data.decode("ascii")
    except UnicodeError as exc:
        raise InstallerError("SHA256SUMS must be ASCII") from exc
    sums: dict[str, str] = {}
    for line in text.splitlines():
        if not line:
            continue
        match = SHA256_RE.fullmatch(line[:64]) if len(line) > 66 else None
        separator = line[64:66]
        name = line[66:]
        if match is None or separator != "  " or not name or "/" in name or "\\" in name:
            raise InstallerError("SHA256SUMS contains a malformed line")
        if name in sums:
            raise InstallerError("SHA256SUMS declares %s twice" % name)
        sums[name] = line[:64]
    if not sums:
        raise InstallerError("SHA256SUMS is empty")
    return sums


def _verified_manifest(
    release_url: str, version: str, installer_bytes: bytes
) -> Mapping[str, Any]:
    if version == LATEST_VERSION:
        pointer = _validated_manifest(
            _parsed_json(
                _fetch(_asset_url(release_url, LATEST_VERSION, MANIFEST_ASSET), MANIFEST_MAX_BYTES),
                "latest release pointer",
            )
        )
        version = pointer["version"]
        if SEMVER_RE.fullmatch(version) is None:
            raise InstallerError("latest release pointer declares an invalid version")
    url_base = _asset_url(release_url, version, "")
    sums = _validated_sums(_fetch(_asset_url(release_url, version, SUMS_ASSET), SUMS_MAX_BYTES))
    manifest_data = _fetch(_asset_url(release_url, version, MANIFEST_ASSET), MANIFEST_MAX_BYTES)
    expected = sums.get(MANIFEST_ASSET)
    if expected is None:
        raise InstallerError("SHA256SUMS does not cover release-manifest.json")
    if _sha256(manifest_data) != expected:
        raise InstallerError("release manifest does not match SHA256SUMS")
    manifest = _validated_manifest(
        _parsed_json(manifest_data, "release-manifest.json")
    )
    if manifest["version"] != version:
        raise InstallerError(
            "release manifest version %s does not match the requested version %s"
            % (manifest["version"], version)
        )
    if manifest["installer"]["sha256"] != _sha256(installer_bytes):
        raise InstallerError(
            "the running installer does not match the release manifest installer hash"
        )
    if sums.get(INSTALLER_ASSET) != manifest["installer"]["sha256"]:
        raise InstallerError("SHA256SUMS and the release manifest disagree about installer.py")
    return manifest


def _read_verified_archive(data: bytes, tag: str, record: Mapping[str, Any]) -> dict[str, bytes]:
    if _sha256(data) != record["sha256"]:
        raise InstallerError("locale %s archive does not match its manifest hash" % tag)
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except (zipfile.BadZipFile, OSError) as exc:
        raise InstallerError("locale %s archive is not a valid ZIP" % tag) from exc
    with archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(set(names)) != len(names):
            raise InstallerError("locale %s archive contains duplicate members" % tag)
        declared = {member["path"]: member for member in record["members"]}
        if set(names) != set(declared):
            missing = sorted(set(declared) - set(names))
            extra = sorted(set(names) - set(declared))
            raise InstallerError(
                "locale %s archive members differ from the manifest (missing: %s; unexpected: %s)"
                % (tag, missing or "none", extra or "none")
            )
        members: dict[str, bytes] = {}
        for info in sorted(infos, key=lambda item: item.filename):
            _validated_member_path(info.filename)
            mode = info.external_attr >> 16
            if stat.S_IFMT(mode) != stat.S_IFREG or info.is_dir():
                raise InstallerError("locale %s archive member must be a regular file: %s" % (tag, info.filename))
            if mode & 0o7777 != FILE_MODE:
                raise InstallerError("locale %s archive member mode must be 0644: %s" % (tag, info.filename))
            if info.create_system != 3:
                raise InstallerError("locale %s archive member must use Unix metadata: %s" % (tag, info.filename))
            if info.compress_type != zipfile.ZIP_STORED:
                raise InstallerError("locale %s archive member must use stored compression: %s" % (tag, info.filename))
            if info.date_time != ARCHIVE_TIMESTAMP:
                raise InstallerError("locale %s archive member timestamp must be %s" % (tag, ARCHIVE_TIMESTAMP_TEXT))
            payload = archive.read(info)
            entry = declared[info.filename]
            if len(payload) != entry["bytes"] or _sha256(payload) != entry["sha256"]:
                raise InstallerError("locale %s archive member does not match its manifest hash: %s" % (tag, info.filename))
            members[info.filename] = payload
    return members


def _resolve_target_root(path: Path) -> Path:
    target = Path(path).absolute()
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise InstallerError("repo root must be a real directory, not a symlink or file")
    if not target.exists():
        if not target.parent.is_dir() or target.parent.is_symlink():
            raise InstallerError("repo root parent must be an existing non-symlink directory")
    return target


def _checked_member_target(root: Path, path: PurePosixPath) -> tuple[Path, bool]:
    """Return (absolute target, exists) and reject symlinked ancestor directories."""

    probe = root
    for segment in path.parts[:-1]:
        probe = probe / segment
        if probe.is_symlink():
            raise InstallerError(
                "target directory chain contains a symlink: %s" % probe
            )
        if probe.exists() and not probe.is_dir():
            raise InstallerError("target path parent is not a directory: %s" % probe)
    target = root.joinpath(*path.parts)
    if target.is_symlink() or target.exists():
        return target, True
    return target, False


def plan_conflicts(root: Path, members: Mapping[str, bytes]) -> list[str]:
    """Return every member whose target already exists; also reject symlinked ancestors."""

    conflicts = []
    for name in sorted(members):
        path = _validated_member_path(name)
        target, exists = _checked_member_target(root, path)
        if exists:
            conflicts.append(name)
    return conflicts


def _write_members(root: Path, members: Mapping[str, bytes]) -> tuple[str, ...]:
    """Write staged members after conflict checks; roll back created files on failure."""

    ordered = sorted(members)
    conflicts = plan_conflicts(root, ordered)
    if conflicts:
        raise InstallerError(
            "target tree already contains %d conflicting path(s); refusing to overwrite: %s. "
            "Install into an empty directory or run 'export' to materialize the artifact "
            "for a manual diff and merge instead."
            % (len(conflicts), ", ".join(conflicts))
        )
    created_dirs: list[Path] = []
    created_files: list[Path] = []
    if not root.exists():
        root.mkdir()
        os.chmod(root, 0o755)
        created_dirs.append(root)
    try:
        for name in ordered:
            path = _validated_member_path(name)
            _ensure_parent_dirs(root, path, created_dirs)
            target = root.joinpath(*path.parts)
            with open(target, "xb") as handle:
                handle.write(members[name])
            created_files.append(target)
            os.chmod(target, FILE_MODE)
    except OSError as exc:
        for target in reversed(created_files):
            try:
                target.unlink()
            except OSError:
                pass
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise InstallerError(
            "install failed before completion; the target tree was left unchanged: %s" % exc
        ) from exc
    return tuple(ordered)


def _ensure_parent_dirs(root: Path, path: PurePosixPath, created: list[Path]) -> None:
    current = root
    for segment in path.parts[:-1]:
        current = current / segment
        if current.is_symlink():
            raise InstallerError("target directory chain contains a symlink: %s" % current)
        if not current.exists():
            current.mkdir()
            os.chmod(current, 0o755)
            created.append(current)
        elif not current.is_dir():
            raise InstallerError("target parent exists but is not a directory: %s" % current)


def _selected_locale_record(manifest: Mapping[str, Any], locale: str) -> Mapping[str, Any]:
    record = manifest["locales"].get(locale)
    if record is None:
        supported = ", ".join(sorted(manifest["locales"]))
        raise InstallerError(
            "unsupported locale: %s (this release supports: %s). For other languages, "
            "install the English bundle and configure the response and project "
            "document language in AGENTS.md." % (locale, supported)
        )
    if record["status"] != "complete":
        raise InstallerError("locale %s is not complete and cannot be installed" % locale)
    return record


def _verified_members(
    release_url: str, manifest: Mapping[str, Any], locale: str
) -> dict[str, bytes]:
    record = _selected_locale_record(manifest, locale)
    asset_url = _asset_url(release_url, manifest["version"], record["asset"])
    archive = _fetch(asset_url, ARCHIVE_MAX_BYTES)
    if len(archive) != record["bytes"]:
        raise InstallerError(
            "locale %s archive size %d does not match the manifest declaration %d"
            % (locale, len(archive), record["bytes"])
        )
    return _read_verified_archive(archive, locale, record)


def install(
    release_url: str,
    version: str,
    locale: str,
    repo_root: Path,
    *,
    installer_bytes: Optional[bytes] = None,
) -> Sequence[str]:
    """Verify a release and install one complete locale into a target tree."""

    release_url = _validated_release_url(release_url)
    version = _validated_version_selection(version)
    manifest = _verified_manifest(release_url, version, _running_installer_bytes(installer_bytes))
    record = _selected_locale_record(manifest, locale)
    members = _verified_members(release_url, manifest, locale)
    target = _resolve_target_root(repo_root)
    written = _write_members(target, members)
    return written


def export_artifact(
    release_url: str,
    version: str,
    locale: str,
    output: Path,
    *,
    installer_bytes: Optional[bytes] = None,
) -> tuple[str, ...]:
    """Verify a release and atomically write its locale artifact to an empty directory."""

    release_url = _validated_release_url(release_url)
    version = _validated_version_selection(version)
    manifest = _verified_manifest(release_url, version, _running_installer_bytes(installer_bytes))
    record = _selected_locale_record(manifest, locale)
    members = _verified_members(release_url, manifest, locale)
    output = _validated_export_output(Path(output))
    stage = Path(tempfile.mkdtemp(prefix=".template-install-", dir=output.parent))
    published = False
    try:
        for name in sorted(members):
            path = _validated_member_path(name)
            target = stage.joinpath(*path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(members[name])
            os.chmod(target, FILE_MODE)
        if output.exists():
            output.rmdir()
        os.replace(stage, output)
        published = True
    except OSError as exc:
        raise InstallerError("cannot publish the exported artifact: %s" % exc) from exc
    finally:
        if not published:
            shutil.rmtree(stage, ignore_errors=True)
    return tuple(sorted(members))


def list_locales(
    release_url: str,
    version: str,
    *,
    installer_bytes: Optional[bytes] = None,
) -> Mapping[str, Any]:
    """Verify a release and return its manifest for locale listing."""

    release_url = _validated_release_url(release_url)
    version = _validated_version_selection(version)
    return _verified_manifest(release_url, version, _running_installer_bytes(installer_bytes))


def _running_installer_bytes(installer_bytes: Optional[bytes]) -> bytes:
    if installer_bytes is not None:
        return installer_bytes
    try:
        return Path(__file__).resolve().read_bytes()
    except OSError as exc:
        raise InstallerError("cannot read the running installer for self-verification: %s" % exc) from exc


def _validated_export_output(output: Path) -> Path:
    output = output.absolute()
    parent = output.parent
    if not parent.is_dir() or parent.is_symlink():
        raise InstallerError("output parent must be an existing non-symlink directory")
    if output.is_symlink():
        raise InstallerError("output must not be a symlink")
    if output.exists():
        if not output.is_dir():
            raise InstallerError("output must be an empty directory")
        try:
            next(output.iterdir())
        except StopIteration:
            pass
        else:
            raise InstallerError("output must be an empty directory")
    return output


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="verify and install one locale into a project root")
    _add_remote_arguments(install_parser)
    install_parser.add_argument("--repo-root", required=True, type=Path, help="target project root")
    install_parser.add_argument("--locale", required=True, help="complete locale tag from the release manifest")
    install_parser.add_argument("--version", default=LATEST_VERSION, help="release version, or 'latest'")

    export_parser = subparsers.add_parser("export", help="materialize one verified locale artifact into an empty directory")
    _add_remote_arguments(export_parser)
    export_parser.add_argument("--output", required=True, type=Path, help="empty output directory")
    export_parser.add_argument("--locale", required=True, help="complete locale tag from the release manifest")
    export_parser.add_argument("--version", default=LATEST_VERSION, help="release version, or 'latest'")

    list_parser = subparsers.add_parser("list-locales", help="list verified locales of a release")
    _add_remote_arguments(list_parser)
    list_parser.add_argument("--version", default=LATEST_VERSION, help="release version, or 'latest'")

    args = parser.parse_args(argv)
    try:
        if args.command == "install":
            written = install(args.release_url, args.version, args.locale, args.repo_root)
            print("Installed %s locale with %d files into %s" % (args.locale, len(written), args.repo_root))
        elif args.command == "export":
            written = export_artifact(args.release_url, args.version, args.locale, args.output)
            print("Exported %s locale with %d files to %s" % (args.locale, len(written), args.output))
        else:
            manifest = list_locales(args.release_url, args.version)
            print("Release %s (source commit %s, repository %s)" % (
                manifest["version"], manifest["source_commit"], manifest["repository"]
            ))
            for tag in sorted(manifest["locales"]):
                print("%s: %s" % (tag, manifest["locales"][tag]["status"]))
    except InstallerError as exc:
        print("Install failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


def _add_remote_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--release-url",
        required=True,
        help="base URL of the immutable per-version release namespace (<base>/<version>/<asset>)",
    )


if __name__ == "__main__":
    raise SystemExit(main())
