#!/usr/bin/env python3
"""Build deterministic locale archives and their release metadata."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

import check_locales
import export_template


ROOT = Path(__file__).resolve().parent.parent
INSTALLER_PATH = Path("scripts/installer.py")
SCHEMA_VERSION = 1
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ARCHIVE_TIMESTAMP_TEXT = "1980-01-01T00:00:00Z"
FILE_MODE = 0o644
COMPRESSION = "stored"
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
REPOSITORY_RE = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?"
)
TEMPLATE_VERSION_RE = re.compile(
    r"^\s*-\s*\*\*Template version:\*\*\s*(\S+)", re.MULTILINE
)


class ReleaseError(ValueError):
    """Raised when release inputs or generated assets violate the contract."""


@dataclass(frozen=True)
class ReleaseArtifacts:
    """Complete deterministic output of one packaging run."""

    files: Mapping[str, bytes]
    manifest: Mapping[str, Any]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validated_version(value: str) -> str:
    if not check_locales._is_semver(value):
        raise ReleaseError("version must be full SemVer without a leading v prefix")
    return value


def _validated_commit(value: str) -> str:
    if COMMIT_RE.fullmatch(value) is None:
        raise ReleaseError("source commit must be 40 lowercase hexadecimal characters")
    return value


def _validated_repository(value: str) -> str:
    if REPOSITORY_RE.fullmatch(value) is None:
        raise ReleaseError("repository must be a normalized OWNER/NAME slug")
    return value


def verify_source_revision(repository_root: Path, source_commit: str) -> None:
    """Require an exact clean Git checkout for the declared source commit."""

    repository_root = Path(repository_root).resolve()
    source_commit = _validated_commit(source_commit)
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=repository_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout.strip()
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repository_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=repository_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ReleaseError("cannot verify source Git revision: %s" % exc) from exc
    if Path(top).resolve() != repository_root:
        raise ReleaseError("source root must be the Git repository root")
    if head != source_commit:
        raise ReleaseError(
            "source commit %s does not match checkout HEAD %s"
            % (source_commit, head)
        )
    if status:
        raise ReleaseError("source checkout must be clean before packaging")


def _installer_bytes(repository_root: Path) -> bytes:
    path = repository_root / INSTALLER_PATH
    candidate = repository_root
    has_symlink = False
    for part in INSTALLER_PATH.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            has_symlink = True
            break
    if has_symlink or not path.is_file():
        raise ReleaseError("installer must be a regular non-symlink file")
    try:
        data = path.read_bytes()
        data.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise ReleaseError("installer must be readable UTF-8: %s" % exc) from exc
    if not data or b"\r" in data or not data.endswith(b"\n"):
        raise ReleaseError("installer must be non-empty UTF-8 with LF and a final newline")
    return data


def _artifact_members(root: Path) -> tuple[tuple[str, bytes], ...]:
    members = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.is_symlink():
            raise ReleaseError("artifact must not contain symlinks")
        members.append((path.relative_to(root).as_posix(), path.read_bytes()))
    return tuple(members)


def _verify_artifact_version(root: Path, locale: str, version: str) -> None:
    for relative in ("docs/TEMPLATE_GUIDE.md", "docs/DOCS_GUIDE.md"):
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise ReleaseError(
                "%s artifact cannot read %s: %s" % (locale, relative, exc)
            ) from exc
        match = TEMPLATE_VERSION_RE.search(text)
        if match is None:
            raise ReleaseError(
                "%s artifact has no Template version in %s" % (locale, relative)
            )
        if match.group(1) != version:
            raise ReleaseError(
                "%s artifact Template version %s does not match release version %s"
                % (locale, match.group(1), version)
            )


def _zip_bytes(members: tuple[tuple[str, bytes], ...]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_STORED) as archive:
        for path, data in members:
            info = zipfile.ZipInfo(path, date_time=ARCHIVE_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (stat.S_IFREG | FILE_MODE) << 16
            archive.writestr(info, data)
    return output.getvalue()


def _member_records(
    members: tuple[tuple[str, bytes], ...]
) -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "sha256": _sha256(data),
            "bytes": len(data),
            "mode": FILE_MODE,
            "timestamp": ARCHIVE_TIMESTAMP_TEXT,
        }
        for path, data in members
    ]


def build_release_artifacts(
    repository_root: Path,
    *,
    version: str,
    source_commit: str,
    repository: str,
) -> ReleaseArtifacts:
    """Build all release assets in memory from validated source files."""

    repository_root = Path(repository_root).resolve()
    version = _validated_version(version)
    source_commit = _validated_commit(source_commit)
    repository = _validated_repository(repository)
    manifest_source = export_template.load_validated_manifest(
        repository_root, require_stable=True
    )
    complete = check_locales.complete_locales(manifest_source)
    installer_data = _installer_bytes(repository_root)

    files: dict[str, bytes] = {}
    locale_records: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="template-package-") as temporary:
        temporary_root = Path(temporary)
        for locale in complete:
            exported = temporary_root / locale
            export_template.export_locale(
                repository_root,
                locale,
                exported,
                require_complete=True,
            )
            _verify_artifact_version(exported, locale, version)
            members = _artifact_members(exported)
            expected = tuple(
                path
                for path, _ in export_template.artifact_sources(
                    repository_root,
                    manifest_source,
                    locale,
                    require_complete=True,
                )
            )
            if tuple(path for path, _ in members) != expected:
                raise ReleaseError("exported member inventory differs for %s" % locale)
            archive = _zip_bytes(members)
            asset = "coding-agent-docs-template-%s-v%s.zip" % (locale, version)
            files[asset] = archive
            locale_records[locale] = {
                "status": "complete",
                "asset": asset,
                "sha256": _sha256(archive),
                "bytes": len(archive),
                "compression": COMPRESSION,
                "members": _member_records(members),
            }

    files["installer.py"] = installer_data
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "version": version,
        "source_commit": source_commit,
        "repository": repository,
        "locales": locale_records,
        "installer": {
            "asset": "installer.py",
            "sha256": _sha256(installer_data),
            "bytes": len(installer_data),
        },
    }
    manifest_data = (
        json.dumps(
            manifest,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    files["release-manifest.json"] = manifest_data
    checksum_names = sorted(files)
    files["SHA256SUMS"] = "".join(
        "%s  %s\n" % (_sha256(files[name]), name) for name in checksum_names
    ).encode("ascii")
    return ReleaseArtifacts(files=dict(sorted(files.items())), manifest=manifest)


def _validate_output(repository_root: Path, output: Path) -> tuple[Path, bool]:
    output = output.absolute()
    if not output.parent.is_dir() or output.parent.is_symlink():
        raise ReleaseError("output parent must be an existing non-symlink directory")
    try:
        output.resolve(strict=False).relative_to(repository_root.resolve())
    except ValueError:
        pass
    else:
        raise ReleaseError("output must be outside the source repository")
    existed = output.exists() or output.is_symlink()
    if output.is_symlink():
        raise ReleaseError("output must not be a symlink")
    if existed:
        if not output.is_dir():
            raise ReleaseError("output must be an empty directory")
        try:
            next(output.iterdir())
        except StopIteration:
            pass
        else:
            raise ReleaseError("output must be an empty directory")
    return output, existed


def write_release_artifacts(
    repository_root: Path, output: Path, artifacts: ReleaseArtifacts
) -> tuple[str, ...]:
    """Atomically publish an in-memory release to an empty directory."""

    output, existed = _validate_output(Path(repository_root), Path(output))
    stage = Path(tempfile.mkdtemp(prefix=".template-release-", dir=output.parent))
    published = False
    try:
        for name, data in artifacts.files.items():
            if (
                not name
                or name in (".", "..")
                or Path(name).name != name
                or "/" in name
                or "\\" in name
            ):
                raise ReleaseError("release asset name must be a safe basename")
            if not isinstance(data, bytes):
                raise ReleaseError("release asset data must be bytes")
            target = stage / name
            target.write_bytes(data)
            target.chmod(FILE_MODE)
        if existed:
            output.rmdir()
        os.replace(stage, output)
        published = True
    except OSError as exc:
        raise ReleaseError("cannot publish release artifacts: %s" % exc) from exc
    finally:
        if not published:
            shutil.rmtree(stage, ignore_errors=True)
    return tuple(sorted(artifacts.files))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="release SemVer without v")
    parser.add_argument("--source-commit", required=True, help="exact lowercase Git SHA")
    parser.add_argument("--repository", required=True, help="OWNER/NAME repository slug")
    parser.add_argument("--output", required=True, type=Path, help="empty output directory")
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="clean source repository root",
    )
    args = parser.parse_args(argv)
    try:
        verify_source_revision(args.root, args.source_commit)
        artifacts = build_release_artifacts(
            args.root,
            version=args.version,
            source_commit=args.source_commit,
            repository=args.repository,
        )
        names = write_release_artifacts(args.root, args.output, artifacts)
    except (ReleaseError, export_template.ExportError) as exc:
        print("Packaging failed: %s" % exc, file=sys.stderr)
        return 1
    print("Packaged %d release assets in %s" % (len(names), args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
