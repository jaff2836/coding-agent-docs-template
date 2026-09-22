#!/usr/bin/env python3
"""Verify release candidates and published releases without mutating remote state."""

from __future__ import annotations

import argparse
import hashlib
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
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
FILE_MODE = 0o644
ADOPTION_POLICIES = frozenset(("copy", "decide", "merge"))
ADOPTION_SUMMARY_STATUSES = (
    "missing",
    "identical",
    "merge",
    "decision",
    "blocked",
)
UPGRADE_SUMMARY_STATUSES = (
    "unchanged",
    "template-only",
    "project-only",
    "converged",
    "diverged",
    "blocked",
)
ADOPTION_TARGET_STATES = frozenset(
    (
        "absent",
        "file",
        "unreadable",
        "case-variant",
        "symlink",
        "parent-symlink",
        "parent-not-directory",
        "special",
    )
)


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
            ["git", "cat-file", "-e", "%s^{commit}" % github_main],
            cwd=repository_root,
        )
    except VerificationError as exc:
        raise VerificationError(
            "synchronized main commit %s is not available locally; "
            "fetch it before release verification" % github_main
        ) from exc
    try:
        _command(
            ["git", "merge-base", "--is-ancestor", source_commit, github_main],
            cwd=repository_root,
        )
    except VerificationError as exc:
        shallow = _command(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=repository_root,
        ).decode("ascii").strip()
        if shallow == "true":
            raise VerificationError(
                "release source ancestry cannot be verified because the local "
                "repository is shallow; fetch complete history before release "
                "verification"
            ) from exc
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


def _draft_release_metadata(
    repository_root: Path, repository: str, tag: str
) -> Mapping[str, Any]:
    output = _command(
        [
            "gh",
            "release",
            "view",
            tag,
            "--repo",
            repository,
            "--json",
            "databaseId,tagName,isDraft,isImmutable,isPrerelease",
        ],
        cwd=repository_root,
    )
    try:
        value = json.loads(output.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError("GitHub draft release metadata is not valid JSON") from exc
    if not isinstance(value, dict):
        raise VerificationError("GitHub draft release metadata must be an object")
    return {
        "id": value.get("databaseId"),
        "tag_name": value.get("tagName"),
        "draft": value.get("isDraft"),
        "immutable": value.get("isImmutable"),
        "prerelease": value.get("isPrerelease"),
    }


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


def _verify_tree_file_mode(mode: int, relative: str, platform_name: str) -> None:
    if platform_name == "nt":
        if mode & stat.S_IWRITE:
            return
        raise VerificationError(
            "verification file is read-only on Windows: %s" % relative
        )
    if mode != FILE_MODE:
        raise VerificationError("verification file mode is not 0644: %s" % relative)


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
        _verify_tree_file_mode(
            stat.S_IMODE(path.lstat().st_mode), relative, os.name
        )
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


def _validated_adoption_summary(plan: Any) -> Mapping[str, int]:
    """Return a complete adoption summary or fail with a stable diagnostic."""

    if not isinstance(plan, dict):
        raise VerificationError("adoption plan must be an object")
    summary = plan.get("summary")
    if not isinstance(summary, dict):
        raise VerificationError("adoption plan summary must be an object")
    # This validates the published adoption-plan contract. Do not derive it from
    # the verifier checkout's installer, which may differ from the release source.
    expected_statuses = set(ADOPTION_SUMMARY_STATUSES)
    if set(summary) != expected_statuses:
        raise VerificationError("adoption plan summary has invalid statuses")
    for status in ADOPTION_SUMMARY_STATUSES:
        value = summary[status]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise VerificationError(
                "adoption plan summary value must be a non-negative integer: %s"
                % status
            )
    return summary


def _validated_upgrade_plan(
    plan: Any,
    *,
    expected_current: Mapping[str, bytes],
    expected_target: Mapping[str, bytes],
    repository: str,
    current_version: str,
    base_version: str,
    locale: str,
) -> None:
    """Validate format 2 against current bytes and the controlled E2E target.

    Base hashes are checked for shape, nullability, and classification
    consistency. The verifier does not duplicate the installer's historical
    release parser; independent base-byte comparison remains a consumer step.
    """

    if not isinstance(plan, dict) or set(plan) != {
        "format",
        "format_version",
        "stability",
        "base_release",
        "release",
        "guide",
        "summary",
        "upgrade_summary",
        "paths",
    }:
        raise VerificationError("upgrade adoption plan has invalid top-level keys")
    if (
        plan["format"] != "coding-agent-docs-template/adoption-plan"
        or isinstance(plan["format_version"], bool)
        or not isinstance(plan["format_version"], int)
        or plan["format_version"] != 2
        or plan["stability"] != "experimental"
        or plan["guide"] != "artifact/docs/TEMPLATE_GUIDE.md §2"
    ):
        raise VerificationError("upgrade adoption plan identity is invalid")
    for key, version in (("base_release", base_version), ("release", current_version)):
        release = plan[key]
        if not isinstance(release, dict) or set(release) != {
            "repository",
            "version",
            "source_commit",
            "locale",
        }:
            raise VerificationError("upgrade adoption plan %s is invalid" % key)
        if (
            not isinstance(release["repository"], str)
            or release["repository"].casefold() != repository.casefold()
            or not isinstance(release["version"], str)
            or release["version"] != version
            or not isinstance(release["locale"], str)
            or release["locale"] != locale
            or not isinstance(release["source_commit"], str)
            or COMMIT_RE.fullmatch(release["source_commit"]) is None
        ):
            raise VerificationError("upgrade adoption plan %s provenance is invalid" % key)

    summary = _validated_adoption_summary(plan)
    upgrade_summary = plan["upgrade_summary"]
    if not isinstance(upgrade_summary, dict) or set(upgrade_summary) != set(
        UPGRADE_SUMMARY_STATUSES
    ):
        raise VerificationError("upgrade adoption plan summary has invalid statuses")
    for status in UPGRADE_SUMMARY_STATUSES:
        value = upgrade_summary[status]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise VerificationError(
                "upgrade adoption plan summary value must be a non-negative integer: %s"
                % status
            )

    paths = plan["paths"]
    if not isinstance(paths, list):
        raise VerificationError("upgrade adoption plan paths must be an array")
    expected_entry_keys = {
        "path",
        "policy",
        "status",
        "upgrade_status",
        "base_sha256",
        "artifact_sha256",
        "target_sha256",
        "target",
        "reason",
    }
    seen: set[str] = set()
    summary_counts = {status: 0 for status in ADOPTION_SUMMARY_STATUSES}
    upgrade_counts = {status: 0 for status in UPGRADE_SUMMARY_STATUSES}
    current_paths: set[str] = set()
    for entry in paths:
        if not isinstance(entry, dict) or set(entry) != expected_entry_keys:
            raise VerificationError("upgrade adoption plan path entry is invalid")
        path = entry["path"]
        if (
            not isinstance(path, str)
            or not path
            or "\\" in path
            or "\x00" in path
            or not all(part and part not in (".", "..") for part in path.split("/"))
            or path in seen
        ):
            raise VerificationError("upgrade adoption plan path is invalid or duplicated")
        seen.add(path)
        if not isinstance(entry["reason"], str) or not entry["reason"]:
            raise VerificationError("upgrade adoption plan path reason is invalid")
        target = entry["target"]
        if not isinstance(target, str) or target not in ADOPTION_TARGET_STATES:
            raise VerificationError("upgrade adoption plan target state is invalid")
        for hash_key in ("base_sha256", "artifact_sha256", "target_sha256"):
            digest = entry[hash_key]
            if digest is not None and (
                not isinstance(digest, str)
                or SHA256_RE.fullmatch(digest) is None
            ):
                raise VerificationError("upgrade adoption plan %s is invalid" % hash_key)
        if (target == "file") != (entry["target_sha256"] is not None):
            raise VerificationError("upgrade adoption plan target hash is inconsistent")
        upgrade_status = entry["upgrade_status"]
        if upgrade_status not in UPGRADE_SUMMARY_STATUSES:
            raise VerificationError("upgrade adoption plan path status is invalid")
        base_sha256 = entry["base_sha256"]
        artifact_sha256 = entry["artifact_sha256"]
        target_sha256 = entry["target_sha256"]
        expected_target_sha256 = (
            hashlib.sha256(expected_target[path]).hexdigest()
            if path in expected_target
            else None
        )
        expected_target_state = "file" if path in expected_target else "absent"
        if target != expected_target_state or target_sha256 != expected_target_sha256:
            raise VerificationError(
                "upgrade adoption plan target does not match the verification fixture"
            )
        if target not in ("absent", "file"):
            expected_upgrade_status = "blocked"
        elif base_sha256 == artifact_sha256 == target_sha256:
            expected_upgrade_status = "unchanged"
        elif base_sha256 == target_sha256 and artifact_sha256 != base_sha256:
            expected_upgrade_status = "template-only"
        elif base_sha256 == artifact_sha256 and target_sha256 != base_sha256:
            expected_upgrade_status = "project-only"
        elif artifact_sha256 == target_sha256 and base_sha256 != artifact_sha256:
            expected_upgrade_status = "converged"
        else:
            expected_upgrade_status = "diverged"
        if upgrade_status != expected_upgrade_status:
            raise VerificationError(
                "upgrade adoption plan path classification is inconsistent"
            )
        upgrade_counts[upgrade_status] += 1
        if path in expected_current:
            current_paths.add(path)
            policy = entry["policy"]
            if not isinstance(policy, str) or policy not in ADOPTION_POLICIES:
                raise VerificationError("upgrade adoption plan current path policy is invalid")
            if target not in ("absent", "file"):
                expected_status = "blocked"
            elif policy == "decide":
                expected_status = "decision"
            elif target == "absent":
                expected_status = "missing"
            elif target_sha256 == artifact_sha256:
                expected_status = "identical"
            else:
                expected_status = "merge"
            if (
                not isinstance(entry["status"], str)
                or entry["status"] not in ADOPTION_SUMMARY_STATUSES
                or entry["status"] != expected_status
                or artifact_sha256
                != hashlib.sha256(expected_current[path]).hexdigest()
            ):
                raise VerificationError("upgrade adoption plan current path is invalid")
            summary_counts[entry["status"]] += 1
        elif (
            entry["policy"] is not None
            or entry["status"] is not None
            or artifact_sha256 is not None
            or base_sha256 is None
        ):
            raise VerificationError("upgrade adoption plan base-only path is invalid")
        elif target in ("absent", "file") and entry["reason"] != (
            "This path is absent from the current release; review whether to keep or "
            "remove it by hand."
        ):
            raise VerificationError("upgrade adoption plan base-only reason is invalid")
    ordered = [entry["path"] for entry in paths]
    if ordered != sorted(ordered):
        raise VerificationError("upgrade adoption plan paths are not sorted")
    if current_paths != set(expected_current):
        raise VerificationError("upgrade adoption plan does not cover current paths")
    if summary_counts != summary or sum(summary.values()) != len(expected_current):
        raise VerificationError("upgrade adoption plan current summary is inconsistent")
    if upgrade_counts != upgrade_summary or sum(upgrade_summary.values()) != len(paths):
        raise VerificationError("upgrade adoption plan upgrade summary is inconsistent")


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
    base_version: Optional[str] = None,
) -> None:
    if base_version is not None:
        base_version = installer._validated_base_version(base_version)
        installer._require_older_base_version(base_version, version)
    installer_bytes = artifacts.files["installer.py"]
    expected_by_locale = {
        locale: _archive_members(artifacts, locale)
        for locale in sorted(artifacts.manifest["locales"])
    }
    with tempfile.TemporaryDirectory(prefix="published-release-e2e-") as temporary:
        base = Path(temporary)
        installer_path = base / "installer.py"
        installer_path.write_bytes(installer_bytes)
        for locale, expected in expected_by_locale.items():
            source_export = base / ("source-%s" % locale)
            export_template.export_locale(
                repository_root, locale, source_export, require_complete=True
            )
            _compare_assets(expected, _tree_files(source_export), "%s source export" % locale)

        for selector in ("latest", version):
            listing = _command(
                [
                    sys.executable,
                    "-B",
                    str(installer_path),
                    "list-locales",
                    "--release-url",
                    release_url,
                    "--version",
                    selector,
                ],
                cwd=base,
            )
            if not listing.decode("utf-8", errors="replace").startswith(
                "Release %s " % version
            ):
                raise VerificationError(
                    "%s selector did not resolve to release %s" % (selector, version)
                )
            for locale, expected in expected_by_locale.items():
                prefix = "%s-%s" % (selector, locale)
                install_root = base / (prefix + "-install")
                exported = base / (prefix + "-export")
                adoption_root = base / (prefix + "-existing")
                adoption_output = base / (prefix + "-adopt")
                adoption_root.mkdir()
                expected_target = {"README.md": b"# Existing project\n"}
                (adoption_root / "README.md").write_bytes(
                    expected_target["README.md"]
                )
                before = _tree_snapshot(adoption_root)

                remote_arguments = [
                    "--release-url",
                    release_url,
                    "--version",
                    selector,
                    "--locale",
                    locale,
                ]
                _command(
                    [
                        sys.executable,
                        "-B",
                        str(installer_path),
                        "install",
                        *remote_arguments,
                        "--repo-root",
                        str(install_root),
                    ],
                    cwd=base,
                )
                _command(
                    [
                        sys.executable,
                        "-B",
                        str(installer_path),
                        "export",
                        *remote_arguments,
                        "--output",
                        str(exported),
                    ],
                    cwd=base,
                )
                _command(
                    [
                        sys.executable,
                        "-B",
                        str(installer_path),
                        "adopt",
                        *remote_arguments,
                        "--repo-root",
                        str(adoption_root),
                        "--output",
                        str(adoption_output),
                    ],
                    cwd=base,
                )
                if _tree_snapshot(adoption_root) != before:
                    raise VerificationError("adopt modified the target repository")
                try:
                    plan = json.loads(
                        (adoption_output / "adoption-plan.json").read_text(
                            encoding="utf-8"
                        )
                    )
                except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                    raise VerificationError("adopt did not write a valid plan") from exc
                summary = _validated_adoption_summary(plan)
                if sum(summary.values()) != len(expected):
                    raise VerificationError("adoption plan does not cover every artifact path")
                _compare_assets(expected, _tree_files(install_root), prefix + " install")
                _compare_assets(expected, _tree_files(exported), prefix + " export")
                _compare_assets(
                    expected,
                    _tree_files(adoption_output / "artifact"),
                    prefix + " adopt artifact",
                )
                if base_version is not None:
                    upgrade_output = base / (prefix + "-upgrade-adopt")
                    _command(
                        [
                            sys.executable,
                            "-B",
                            str(installer_path),
                            "adopt",
                            *remote_arguments,
                            "--base-version",
                            base_version,
                            "--repo-root",
                            str(adoption_root),
                            "--output",
                            str(upgrade_output),
                        ],
                        cwd=base,
                    )
                    if _tree_snapshot(adoption_root) != before:
                        raise VerificationError(
                            "base-aware adopt modified the target repository"
                        )
                    try:
                        upgrade_plan = json.loads(
                            (upgrade_output / "adoption-plan.json").read_text(
                                encoding="utf-8"
                            )
                        )
                    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                        raise VerificationError(
                            "base-aware adopt did not write a valid plan"
                        ) from exc
                    _validated_upgrade_plan(
                        upgrade_plan,
                        expected_current=expected,
                        expected_target=expected_target,
                        repository=artifacts.manifest["repository"],
                        current_version=version,
                        base_version=base_version,
                        locale=locale,
                    )
                    _compare_assets(
                        expected,
                        _tree_files(upgrade_output / "artifact"),
                        prefix + " base-aware adopt artifact",
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
                    _command(
                        [
                            sys.executable,
                            "-B",
                            str(installer_path),
                            "install",
                            *remote_arguments,
                            "--repo-root",
                            str(conflict_root),
                        ],
                        cwd=base,
                    )
                except VerificationError as exc:
                    if "conflicting path(s)" not in str(exc):
                        raise
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
    metadata = _draft_release_metadata(repository_root, repository, tag)
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
    base_version: Optional[str] = None,
) -> None:
    """Verify an immutable latest release and exercise its public installer paths."""

    repository_root = Path(repository_root).resolve()
    version, source_commit, repository = _validated_identity(
        version, source_commit, repository
    )
    if base_version is not None:
        base_version = installer._validated_base_version(base_version)
        installer._require_older_base_version(base_version, version)
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
        base_version=base_version,
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
    published.add_argument(
        "--base-version",
        help="older exact SemVer for optional base-aware adopt verification",
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
            verify_published(
                release_url=args.release_url,
                base_version=args.base_version,
                **common,
            )
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
