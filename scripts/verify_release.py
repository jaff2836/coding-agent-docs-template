#!/usr/bin/env python3
"""Verify release candidates and published releases without mutating remote state."""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

import export_template
import installer
import package_release


ROOT = Path(__file__).resolve().parent.parent
REMOTE_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
FILE_MODE = 0o644


class VerificationError(ValueError):
    """Raised when a release verification condition is not satisfied."""


def _command(arguments: Sequence[str], *, cwd: Path) -> bytes:
    """Run one read-only verification command and return its stdout bytes."""

    command = [str(argument) for argument in arguments]
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise VerificationError(
            "cannot run verification command %s: %s" % (command[0], exc)
        ) from exc
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).decode(
            "utf-8", errors="replace"
        ).strip()
        raise VerificationError(
            "verification command failed (%s): %s"
            % (" ".join(command), detail or "exit %d" % completed.returncode)
        )
    return completed.stdout


def _validated_remote_name(value: str) -> str:
    if REMOTE_NAME_RE.fullmatch(value) is None:
        raise VerificationError("remote must be a configured Git remote name")
    return value


def _validated_identity(
    version: str, source_commit: str, repository: str
) -> tuple[str, str, str]:
    try:
        return (
            package_release._validated_version(version),
            package_release._validated_commit(source_commit),
            package_release._validated_repository(repository),
        )
    except package_release.ReleaseError as exc:
        raise VerificationError(str(exc)) from exc


def _run_local_gates(repository_root: Path, source_commit: str) -> None:
    """Run the documented source gates without changing the checkout."""

    package_release.verify_source_revision(repository_root, source_commit)
    commands = (
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
        [sys.executable, "-B", "scripts/check-docs.py"],
        [sys.executable, "-B", "scripts/check-locales.py", "--require-stable"],
        ["git", "diff", "--check"],
    )
    for command in commands:
        _command(command, cwd=repository_root)
    package_release.verify_source_revision(repository_root, source_commit)


def _compare_assets(
    expected: Mapping[str, bytes], actual: Mapping[str, bytes], label: str
) -> None:
    expected_names = set(expected)
    actual_names = set(actual)
    if expected_names != actual_names:
        missing = sorted(expected_names - actual_names)
        unexpected = sorted(actual_names - expected_names)
        raise VerificationError(
            "%s asset inventory differs (missing: %s; unexpected: %s)"
            % (label, missing or "none", unexpected or "none")
        )
    changed = sorted(name for name in expected_names if expected[name] != actual[name])
    if changed:
        raise VerificationError(
            "%s asset bytes differ: %s" % (label, ", ".join(changed))
        )


def _build_reproducible_assets(
    repository_root: Path, *, version: str, source_commit: str, repository: str
) -> package_release.ReleaseArtifacts:
    first = package_release.build_release_artifacts(
        repository_root,
        version=version,
        source_commit=source_commit,
        repository=repository,
    )
    second = package_release.build_release_artifacts(
        repository_root,
        version=version,
        source_commit=source_commit,
        repository=repository,
    )
    _compare_assets(first.files, second.files, "repeated package")
    if first.manifest != second.manifest:
        raise VerificationError("repeated package manifests differ")
    return first


def _ls_remote(repository_root: Path, remote: str, refs: Sequence[str]) -> dict[str, str]:
    output = _command(["git", "ls-remote", remote, *refs], cwd=repository_root)
    parsed: dict[str, str] = {}
    for raw_line in output.decode("utf-8", errors="strict").splitlines():
        try:
            commit, name = raw_line.split("\t", 1)
        except ValueError as exc:
            raise VerificationError("git ls-remote returned a malformed line") from exc
        parsed[name] = commit
    return parsed


def _verify_remote_refs(
    repository_root: Path,
    *,
    version: str,
    source_commit: str,
    origin_remote: str,
    github_remote: str,
) -> str:
    origin_remote = _validated_remote_name(origin_remote)
    github_remote = _validated_remote_name(github_remote)
    main_ref = "refs/heads/main"
    tag_ref = "refs/tags/v%s" % version
    peeled_ref = "%s^{}" % tag_ref
    origin = _ls_remote(repository_root, origin_remote, (main_ref,))
    github = _ls_remote(
        repository_root, github_remote, (main_ref, tag_ref, peeled_ref)
    )
    origin_main = origin.get(main_ref)
    github_main = github.get(main_ref)
    if origin_main is None or github_main is None:
        raise VerificationError("Origin and GitHub must both publish refs/heads/main")
    if origin_main != github_main:
        raise VerificationError(
            "Origin and GitHub main differ: %s != %s" % (origin_main, github_main)
        )
    if tag_ref not in github or peeled_ref not in github:
        raise VerificationError("GitHub release tag must be an annotated tag: v%s" % version)
    if github[peeled_ref] != source_commit:
        raise VerificationError(
            "GitHub tag v%s resolves to %s, expected %s"
            % (version, github[peeled_ref], source_commit)
        )
    local_type = _command(
        ["git", "cat-file", "-t", tag_ref], cwd=repository_root
    ).decode("ascii").strip()
    local_commit = _command(
        ["git", "rev-parse", peeled_ref], cwd=repository_root
    ).decode("ascii").strip()
    if local_type != "tag" or local_commit != source_commit:
        raise VerificationError("local annotated tag does not match the declared source commit")
    try:
        _command(
            ["git", "merge-base", "--is-ancestor", source_commit, github_main],
            cwd=repository_root,
        )
    except VerificationError as exc:
        raise VerificationError(
            "release source commit is not an ancestor of the synchronized main"
        ) from exc
    return github_main


def _release_metadata(repository_root: Path, repository: str, tag: str) -> Mapping[str, Any]:
    output = _command(
        ["gh", "api", "repos/%s/releases/tags/%s" % (repository, tag)],
        cwd=repository_root,
    )
    try:
        value = json.loads(output.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError("GitHub release metadata is not valid JSON") from exc
    if not isinstance(value, dict):
        raise VerificationError("GitHub release metadata must be an object")
    return value


def _latest_release_metadata(
    repository_root: Path, repository: str
) -> Mapping[str, Any]:
    output = _command(
        ["gh", "api", "repos/%s/releases/latest" % repository],
        cwd=repository_root,
    )
    try:
        value = json.loads(output.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError("GitHub latest release metadata is not valid JSON") from exc
    if not isinstance(value, dict):
        raise VerificationError("GitHub latest release metadata must be an object")
    return value


def _require_release_shape(
    metadata: Mapping[str, Any], *, tag: str, draft: bool, immutable: bool
) -> None:
    if metadata.get("tag_name") != tag:
        raise VerificationError("GitHub release tag_name does not match %s" % tag)
    if metadata.get("draft") is not draft:
        raise VerificationError(
            "GitHub release %s draft state must be %s" % (tag, draft)
        )
    if bool(metadata.get("immutable", False)) is not immutable:
        raise VerificationError(
            "GitHub release %s immutable state must be %s" % (tag, immutable)
        )
    if not draft and metadata.get("prerelease") is not False:
        raise VerificationError("published release must not be a prerelease")


def _download_release_assets(
    repository_root: Path, repository: str, tag: str
) -> dict[str, bytes]:
    with tempfile.TemporaryDirectory(prefix="release-assets-") as temporary:
        destination = Path(temporary)
        _command(
            [
                "gh",
                "release",
                "download",
                tag,
                "--repo",
                repository,
                "--dir",
                str(destination),
            ],
            cwd=repository_root,
        )
        assets: dict[str, bytes] = {}
        for path in sorted(destination.iterdir()):
            if path.is_symlink() or not path.is_file():
                raise VerificationError("downloaded release asset is not a regular file")
            assets[path.name] = path.read_bytes()
        if not assets:
            raise VerificationError("GitHub release has no downloadable assets")
        return assets


def _tree_files(root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise VerificationError("verification tree contains a symlink: %s" % relative)
        if path.is_dir():
            continue
        if not path.is_file():
            raise VerificationError("verification tree contains a special file: %s" % relative)
        if stat.S_IMODE(path.lstat().st_mode) != FILE_MODE:
            raise VerificationError("verification file mode is not 0644: %s" % relative)
        files[relative] = path.read_bytes()
    return files


def _tree_snapshot(root: Path) -> tuple[tuple[str, str, int, bytes], ...]:
    snapshot = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            snapshot.append((relative, "symlink", mode, os.readlink(path).encode()))
        elif path.is_dir():
            snapshot.append((relative, "dir", mode, b""))
        elif path.is_file():
            snapshot.append((relative, "file", mode, path.read_bytes()))
        else:
            snapshot.append((relative, "special", mode, b""))
    return tuple(snapshot)


def _archive_members(
    artifacts: package_release.ReleaseArtifacts, locale: str
) -> dict[str, bytes]:
    record = artifacts.manifest["locales"][locale]
    archive_data = artifacts.files[record["asset"]]
    try:
        with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
            return {name: archive.read(name) for name in archive.namelist()}
    except (zipfile.BadZipFile, OSError) as exc:
        raise VerificationError("locally packaged archive is invalid: %s" % locale) from exc


def _check_artifact(repository_root: Path, artifact_root: Path) -> None:
    _command(
        [
            sys.executable,
            "-B",
            str(artifact_root / "scripts/check-docs.py"),
            "--root",
            str(artifact_root),
        ],
        cwd=artifact_root,
    )
    _command(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(artifact_root / "tests"),
            "-p",
            "test_check_docs.py",
            "-v",
        ],
        cwd=repository_root,
    )


def _verify_published_e2e(
    repository_root: Path,
    *,
    release_url: str,
    version: str,
    artifacts: package_release.ReleaseArtifacts,
) -> None:
    installer_bytes = artifacts.files["installer.py"]
    expected_by_locale = {
        locale: _archive_members(artifacts, locale)
        for locale in sorted(artifacts.manifest["locales"])
    }
    with tempfile.TemporaryDirectory(prefix="published-release-e2e-") as temporary:
        base = Path(temporary)
        for locale, expected in expected_by_locale.items():
            source_export = base / ("source-%s" % locale)
            export_template.export_locale(
                repository_root, locale, source_export, require_complete=True
            )
            _compare_assets(expected, _tree_files(source_export), "%s source export" % locale)

        for selector in ("latest", version):
            manifest = installer.list_locales(
                release_url,
                selector,
                installer_bytes=installer_bytes,
            )
            if manifest["version"] != version:
                raise VerificationError(
                    "%s selector resolved to %s instead of %s"
                    % (selector, manifest["version"], version)
                )
            for locale, expected in expected_by_locale.items():
                prefix = "%s-%s" % (selector, locale)
                install_root = base / (prefix + "-install")
                exported = base / (prefix + "-export")
                adoption_root = base / (prefix + "-existing")
                adoption_output = base / (prefix + "-adopt")
                adoption_root.mkdir()
                (adoption_root / "README.md").write_text(
                    "# Existing project\n", encoding="utf-8"
                )
                before = _tree_snapshot(adoption_root)

                installer.install(
                    release_url,
                    selector,
                    locale,
                    install_root,
                    installer_bytes=installer_bytes,
                )
                installer.export_artifact(
                    release_url,
                    selector,
                    locale,
                    exported,
                    installer_bytes=installer_bytes,
                )
                plan = installer.adopt(
                    release_url,
                    selector,
                    locale,
                    adoption_root,
                    adoption_output,
                    installer_bytes=installer_bytes,
                )
                if _tree_snapshot(adoption_root) != before:
                    raise VerificationError("adopt modified the target repository")
                if sum(plan["summary"].values()) != len(expected):
                    raise VerificationError("adoption plan does not cover every artifact path")
                _compare_assets(expected, _tree_files(install_root), prefix + " install")
                _compare_assets(expected, _tree_files(exported), prefix + " export")
                _compare_assets(
                    expected,
                    _tree_files(adoption_output / installer.ADOPTION_ARTIFACT_DIR),
                    prefix + " adopt artifact",
                )
                if selector == version:
                    _check_artifact(repository_root, exported)

                conflict_root = base / (prefix + "-conflict")
                conflict_root.mkdir()
                (conflict_root / "AGENTS.md").write_text(
                    "keep\n", encoding="utf-8"
                )
                conflict_before = _tree_snapshot(conflict_root)
                try:
                    installer.install(
                        release_url,
                        selector,
                        locale,
                        conflict_root,
                        installer_bytes=installer_bytes,
                    )
                except installer.InstallerError:
                    pass
                else:
                    raise VerificationError("install accepted an existing conflicting path")
                if _tree_snapshot(conflict_root) != conflict_before:
                    raise VerificationError("failed install changed the conflict target")


def verify_candidate(
    repository_root: Path,
    *,
    version: str,
    source_commit: str,
    repository: str,
    origin_remote: str,
    github_remote: str,
) -> None:
    """Verify a clean candidate and byte-compare it with an existing draft."""

    repository_root = Path(repository_root).resolve()
    version, source_commit, repository = _validated_identity(
        version, source_commit, repository
    )
    _run_local_gates(repository_root, source_commit)
    artifacts = _build_reproducible_assets(
        repository_root,
        version=version,
        source_commit=source_commit,
        repository=repository,
    )
    main_commit = _verify_remote_refs(
        repository_root,
        version=version,
        source_commit=source_commit,
        origin_remote=origin_remote,
        github_remote=github_remote,
    )
    tag = "v%s" % version
    metadata = _release_metadata(repository_root, repository, tag)
    _require_release_shape(metadata, tag=tag, draft=True, immutable=False)
    draft_assets = _download_release_assets(repository_root, repository, tag)
    _compare_assets(artifacts.files, draft_assets, "GitHub draft")
    print(
        "Candidate release verification passed: %s at %s; synchronized main %s; %d assets"
        % (tag, source_commit, main_commit, len(artifacts.files))
    )


def verify_published(
    repository_root: Path,
    *,
    version: str,
    source_commit: str,
    repository: str,
    release_url: str,
    origin_remote: str,
    github_remote: str,
) -> None:
    """Verify an immutable latest release and exercise its public installer paths."""

    repository_root = Path(repository_root).resolve()
    version, source_commit, repository = _validated_identity(
        version, source_commit, repository
    )
    release_url = installer._validated_release_url(release_url)
    expected_repository = installer._github_repository(release_url)
    if expected_repository is None or expected_repository.casefold() != repository.casefold():
        raise VerificationError("release URL repository does not match --repository")
    package_release.verify_source_revision(repository_root, source_commit)
    artifacts = package_release.build_release_artifacts(
        repository_root,
        version=version,
        source_commit=source_commit,
        repository=repository,
    )
    main_commit = _verify_remote_refs(
        repository_root,
        version=version,
        source_commit=source_commit,
        origin_remote=origin_remote,
        github_remote=github_remote,
    )
    tag = "v%s" % version
    metadata = _release_metadata(repository_root, repository, tag)
    _require_release_shape(metadata, tag=tag, draft=False, immutable=True)
    latest = _latest_release_metadata(repository_root, repository)
    if latest.get("id") != metadata.get("id") or latest.get("tag_name") != tag:
        raise VerificationError("published release is not the current GitHub latest release")
    published_assets = _download_release_assets(repository_root, repository, tag)
    _compare_assets(artifacts.files, published_assets, "published GitHub release")
    _verify_published_e2e(
        repository_root,
        release_url=release_url,
        version=version,
        artifacts=artifacts,
    )
    package_release.verify_source_revision(repository_root, source_commit)
    print(
        "Published release verification passed: %s at %s; synchronized main %s; %d assets"
        % (tag, source_commit, main_commit, len(artifacts.files))
    )


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--version", required=True, help="full SemVer without v")
    parser.add_argument("--source-commit", required=True, help="exact lowercase Git SHA")
    parser.add_argument("--repository", required=True, help="GitHub OWNER/NAME slug")
    parser.add_argument("--origin-remote", default="origin", help="Cursor Origin Git remote name")
    parser.add_argument("--github-remote", default="github", help="GitHub Git remote name")
    parser.add_argument(
        "--root", type=Path, default=ROOT, help="clean exact source checkout"
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    candidate = subparsers.add_parser(
        "candidate", help="verify local gates, remote refs, and an existing draft"
    )
    _add_common_arguments(candidate)
    published = subparsers.add_parser(
        "published", help="verify an immutable latest release through public HTTPS"
    )
    _add_common_arguments(published)
    published.add_argument(
        "--release-url", required=True, help="GitHub Releases root URL"
    )
    args = parser.parse_args(argv)
    try:
        common = {
            "repository_root": args.root,
            "version": args.version,
            "source_commit": args.source_commit,
            "repository": args.repository,
            "origin_remote": args.origin_remote,
            "github_remote": args.github_remote,
        }
        if args.command == "candidate":
            verify_candidate(**common)
        else:
            verify_published(release_url=args.release_url, **common)
    except (
        VerificationError,
        export_template.ExportError,
        installer.InstallerError,
        package_release.ReleaseError,
    ) as exc:
        print("Release verification failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
