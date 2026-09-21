#!/usr/bin/env python3
"""Install, export, or stage verified locale artifacts from an immutable release.

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

SCHEMA_VERSION = 2
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
ADOPTION_POLICIES = frozenset(("copy", "decide", "merge"))
ADOPTION_STATUSES = ("missing", "identical", "merge", "decision", "blocked")
ADOPTION_PLAN_NAME = "adoption-plan.json"
ADOPTION_ARTIFACT_DIR = "artifact"
ADOPTION_FORMAT = "coding-agent-docs-template/adoption-plan"
ADOPTION_FORMAT_VERSION = 1
ADOPTION_UPGRADE_FORMAT_VERSION = 2
ADOPTION_GUIDE = "artifact/docs/TEMPLATE_GUIDE.md §2"
UPGRADE_STATUSES = (
    "unchanged",
    "template-only",
    "project-only",
    "converged",
    "diverged",
    "blocked",
)
UPGRADE_REMOVAL_REASON = (
    "This path is absent from the current release; review whether to keep or "
    "remove it by hand."
)
ADOPTION_REASONS = {
    ("missing", "copy"): "The target has no file here; add the artifact file.",
    ("missing", "merge"): "The target has no file here; add the artifact file and fill in the project values.",
    ("identical", "copy"): "The target file already matches the artifact.",
    ("identical", "merge"): "The target file already matches the artifact.",
    ("merge", "copy"): "Template-owned file differs; start from the artifact version and reapply intentional project edits.",
    ("merge", "merge"): "Project-owned file differs; keep the existing content and merge in the template sections.",
    ("decision", "absent"): "Adopt this file only if the project explicitly decides to use it.",
    ("decision", "file"): "The project must decide whether to keep its file, adopt the artifact version, or remove it.",
}
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
GITHUB_HOST = "github.com"
GITHUB_RELEASE_PATH_RE = re.compile(
    r"/(?P<repository>"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?"
    r")/releases"
)
GITHUB_RELEASE_ASSET_PATH_RE = re.compile(
    r"/[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/releases/"
    r"(?:latest/download|download/v" + SEMVER_RE.pattern + r")/[^/]+"
)


class InstallerError(ValueError):
    """Raised when a release asset or target tree violates the contract."""


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Reject redirects for localhost fixtures and unsupported transports."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class _GitHubReleaseRedirects(urllib.request.HTTPRedirectHandler):
    """Follow only an HTTPS chain initiated by one trusted GitHub asset URL."""

    max_repeats = 2
    max_redirections = 5

    def __init__(self, initial_url: str) -> None:
        super().__init__()
        self._trusted_sources = {initial_url}

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if req.full_url not in self._trusted_sources:
            return None
        target = urllib.parse.urljoin(req.full_url, newurl)
        parsed = urllib.parse.urlsplit(target)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or "@" in parsed.netloc
            or parsed.username
            or parsed.password
            or parsed.fragment
        ):
            return None
        redirected = super().redirect_request(
            req, fp, code, msg, headers, target
        )
        if redirected is not None:
            self._trusted_sources.add(redirected.full_url)
        return redirected


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validated_version_selection(value: str) -> str:
    if value == LATEST_VERSION:
        return value
    if SEMVER_RE.fullmatch(value) is None:
        raise InstallerError("version must be 'latest' or full SemVer without a leading v prefix")
    return value


def _validated_base_version(value: str) -> str:
    if value == LATEST_VERSION or SEMVER_RE.fullmatch(value) is None:
        raise InstallerError(
            "base version must be full SemVer without a leading v prefix; "
            "'latest' is not allowed"
        )
    return value


def _semver_parts(value: str) -> tuple[tuple[int, int, int], Optional[tuple[str, ...]]]:
    """Return SemVer precedence components after full validation."""

    if SEMVER_RE.fullmatch(value) is None:
        raise InstallerError("version must be full SemVer")
    without_build = value.split("+", 1)[0]
    core, separator, prerelease = without_build.partition("-")
    major, minor, patch = (int(part) for part in core.split("."))
    return (major, minor, patch), (tuple(prerelease.split(".")) if separator else None)


def _compare_semver_precedence(left: str, right: str) -> int:
    """Compare two validated SemVer values, ignoring build metadata."""

    left_core, left_pre = _semver_parts(left)
    right_core, right_pre = _semver_parts(right)
    if left_core != right_core:
        return -1 if left_core < right_core else 1
    if left_pre is None or right_pre is None:
        if left_pre is right_pre:
            return 0
        return 1 if left_pre is None else -1
    for left_part, right_part in zip(left_pre, right_pre):
        if left_part == right_part:
            continue
        left_numeric = left_part.isdigit()
        right_numeric = right_part.isdigit()
        if left_numeric and right_numeric:
            return -1 if int(left_part) < int(right_part) else 1
        if left_numeric != right_numeric:
            return -1 if left_numeric else 1
        return -1 if left_part < right_part else 1
    if len(left_pre) == len(right_pre):
        return 0
    return -1 if len(left_pre) < len(right_pre) else 1


def _require_older_base_version(base_version: str, current_version: str) -> None:
    if _compare_semver_precedence(base_version, current_version) >= 0:
        raise InstallerError(
            "base version %s must have lower SemVer precedence than current version %s"
            % (base_version, current_version)
        )


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
    normalized = value.rstrip("/")
    if parsed.hostname in LOCAL_HOSTS:
        return normalized
    if (
        parsed.scheme != "https"
        or parsed.netloc.lower() != GITHUB_HOST
        or GITHUB_RELEASE_PATH_RE.fullmatch(parsed.path.rstrip("/")) is None
    ):
        raise InstallerError(
            "release URL must be https://github.com/OWNER/NAME/releases"
        )
    return normalized


def _github_repository(release_url: str) -> Optional[str]:
    parsed = urllib.parse.urlsplit(release_url)
    if parsed.hostname != GITHUB_HOST:
        return None
    match = GITHUB_RELEASE_PATH_RE.fullmatch(parsed.path.rstrip("/"))
    if match is None:
        return None
    return match.group("repository")


def _is_github_release_asset_url(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.netloc.lower() != GITHUB_HOST
        or parsed.query
        or parsed.fragment
    ):
        return False
    return GITHUB_RELEASE_ASSET_PATH_RE.fullmatch(parsed.path) is not None


def _asset_url(release_url: str, version: str, name: str) -> str:
    if not name or "/" in name or "\\" in name:
        raise InstallerError("release asset name must be a basename")
    if _github_repository(release_url) is not None:
        if version == LATEST_VERSION:
            return "%s/latest/download/%s" % (release_url, name)
        return "%s/download/v%s/%s" % (release_url, version, name)
    return "%s/%s/%s" % (release_url, version, name)


def _fetch(url: str, max_bytes: int) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT}, method="GET"
    )
    try:
        redirect_handler = (
            _GitHubReleaseRedirects(url)
            if _is_github_release_asset_url(url)
            else _RejectRedirects()
        )
        opener = urllib.request.build_opener(redirect_handler)
        with opener.open(request, timeout=FETCH_TIMEOUT) as response:
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
        exc.close()
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
        raise InstallerError(
            "unsupported release manifest schema_version; download and run "
            "installer.py from the same release version"
        )
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
    folded_paths = {path.lower(): path for path in paths}
    for path in paths:
        parts = PurePosixPath(path).parts
        for length in range(1, len(parts)):
            parent = "/".join(parts[:length])
            conflicting = folded_paths.get(parent.lower())
            if conflicting is not None:
                raise InstallerError(
                    "locale %s declares member path prefix conflict: %s and %s"
                    % (tag, conflicting, path)
                )


def _validated_member_record(tag: str, member: Any) -> None:
    if not isinstance(member, dict) or set(member) != {
        "path",
        "sha256",
        "bytes",
        "mode",
        "timestamp",
        "policy",
    }:
        raise InstallerError("locale %s has an invalid member record" % tag)
    if not isinstance(member["policy"], str) or member["policy"] not in ADOPTION_POLICIES:
        raise InstallerError("locale %s has an invalid member adoption policy" % tag)
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


def _validated_base_manifest(manifest: Any) -> Mapping[str, Any]:
    """Validate only the two historical schemas accepted for base comparison.

    This parser must not be used by current release verification. Its exact-key
    handling is intentionally isolated so historical compatibility cannot loosen
    the running installer's self-binding contract.
    """

    if not isinstance(manifest, dict) or set(manifest) != {
        "schema_version",
        "version",
        "source_commit",
        "repository",
        "locales",
        "installer",
    }:
        raise InstallerError("base release manifest has unexpected top-level keys")
    schema_version = manifest["schema_version"]
    if (
        isinstance(schema_version, bool)
        or not isinstance(schema_version, int)
        or schema_version not in (1, 2)
    ):
        raise InstallerError("unsupported base release manifest schema_version")
    version = manifest["version"]
    if not isinstance(version, str) or SEMVER_RE.fullmatch(version) is None:
        raise InstallerError("base release manifest version must be full SemVer")
    source_commit = manifest["source_commit"]
    if not isinstance(source_commit, str) or COMMIT_RE.fullmatch(source_commit) is None:
        raise InstallerError(
            "base release manifest source_commit must be 40 lowercase hex characters"
        )
    repository = manifest["repository"]
    if not isinstance(repository, str) or REPOSITORY_RE.fullmatch(repository) is None:
        raise InstallerError("base release manifest repository must be an OWNER/NAME slug")
    _validated_base_installer_record(manifest["installer"])
    locales = manifest["locales"]
    if not isinstance(locales, dict) or not locales:
        raise InstallerError("base release manifest locales must be a non-empty object")
    for tag, record in locales.items():
        if not isinstance(tag, str) or LOCALE_KEY_RE.fullmatch(tag) is None:
            raise InstallerError("unsupported locale tag in base release manifest: %s" % tag)
        _validated_base_locale_record(tag, record, version, schema_version)
    return manifest


def _validated_base_installer_record(record: Any) -> None:
    if not isinstance(record, dict) or set(record) != {"asset", "sha256", "bytes"}:
        raise InstallerError("base release manifest installer record is invalid")
    if record["asset"] != INSTALLER_ASSET:
        raise InstallerError("base release manifest installer asset must be %s" % INSTALLER_ASSET)
    if not isinstance(record["sha256"], str) or SHA256_RE.fullmatch(record["sha256"]) is None:
        raise InstallerError("base release manifest installer sha256 is invalid")
    if (
        isinstance(record["bytes"], bool)
        or not isinstance(record["bytes"], int)
        or not 1 <= record["bytes"] <= MANIFEST_MAX_BYTES
    ):
        raise InstallerError("base release manifest installer bytes is invalid")


def _validated_base_locale_record(
    tag: str, record: Any, version: str, schema_version: int
) -> None:
    if not isinstance(record, dict) or set(record) != {
        "status",
        "asset",
        "sha256",
        "bytes",
        "compression",
        "members",
    }:
        raise InstallerError("base locale record has unexpected keys: %s" % tag)
    if record["status"] != "complete":
        raise InstallerError("base locale %s is not complete" % tag)
    expected_asset = "coding-agent-docs-template-%s-v%s.zip" % (tag, version)
    if record["asset"] != expected_asset:
        raise InstallerError(
            "base locale %s asset name does not bind the locale and version: %s"
            % (tag, record["asset"])
        )
    if not isinstance(record["sha256"], str) or SHA256_RE.fullmatch(record["sha256"]) is None:
        raise InstallerError("base locale %s archive sha256 is invalid" % tag)
    if (
        isinstance(record["bytes"], bool)
        or not isinstance(record["bytes"], int)
        or not 1 <= record["bytes"] <= ARCHIVE_MAX_BYTES
    ):
        raise InstallerError("base locale %s archive size is outside the download limit" % tag)
    if record["compression"] != "stored":
        raise InstallerError("base locale %s archive must use stored compression" % tag)
    members = record["members"]
    if not isinstance(members, list) or not members:
        raise InstallerError("base locale %s must declare at least one member" % tag)
    for member in members:
        _validated_base_member_record(tag, member, schema_version)
    paths = [member["path"] for member in members]
    if len(set(paths)) != len(paths):
        raise InstallerError("base locale %s declares duplicate member paths" % tag)
    if len({path.casefold() for path in paths}) != len(paths):
        raise InstallerError("base locale %s declares case-fold colliding member paths" % tag)
    for path in paths:
        _validated_member_path(path)
    folded_paths = {path.casefold(): path for path in paths}
    for path in paths:
        parts = PurePosixPath(path).parts
        for length in range(1, len(parts)):
            parent = "/".join(parts[:length])
            conflicting = folded_paths.get(parent.casefold())
            if conflicting is not None:
                raise InstallerError(
                    "base locale %s declares member path prefix conflict: %s and %s"
                    % (tag, conflicting, path)
                )


def _validated_base_member_record(tag: str, member: Any, schema_version: int) -> None:
    expected_keys = {"path", "sha256", "bytes", "mode", "timestamp"}
    if schema_version == 2:
        expected_keys.add("policy")
    if not isinstance(member, dict) or set(member) != expected_keys:
        raise InstallerError("base locale %s has an invalid member record" % tag)
    if schema_version == 2 and (
        not isinstance(member["policy"], str)
        or member["policy"] not in ADOPTION_POLICIES
    ):
        raise InstallerError("base locale %s has an invalid member adoption policy" % tag)
    if (
        not isinstance(member["path"], str)
        or not isinstance(member["sha256"], str)
        or SHA256_RE.fullmatch(member["sha256"]) is None
    ):
        raise InstallerError("base locale %s has an invalid member hash" % tag)
    if (
        isinstance(member["bytes"], bool)
        or not isinstance(member["bytes"], int)
        or member["bytes"] < 0
    ):
        raise InstallerError("base locale %s has an invalid member size" % tag)
    if member["mode"] != FILE_MODE_INT:
        raise InstallerError("base locale %s member mode must be 0644" % tag)
    if member["timestamp"] != ARCHIVE_TIMESTAMP_TEXT:
        raise InstallerError(
            "base locale %s member timestamp must be %s"
            % (tag, ARCHIVE_TIMESTAMP_TEXT)
        )


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
        _require_matching_repository(release_url, pointer)
        version = pointer["version"]
        if SEMVER_RE.fullmatch(version) is None:
            raise InstallerError("latest release pointer declares an invalid version")
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
    _require_matching_repository(release_url, manifest)
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


def _verified_base_release(
    release_url: str,
    version: str,
    locale: str,
    current_manifest: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any], dict[str, bytes]]:
    """Read one exact historical release without loading its installer code."""

    sums = _validated_sums(
        _fetch(_asset_url(release_url, version, SUMS_ASSET), SUMS_MAX_BYTES)
    )
    manifest_data = _fetch(
        _asset_url(release_url, version, MANIFEST_ASSET), MANIFEST_MAX_BYTES
    )
    if sums.get(MANIFEST_ASSET) != _sha256(manifest_data):
        raise InstallerError("base release manifest does not match SHA256SUMS")
    manifest = _validated_base_manifest(
        _parsed_json(manifest_data, "base release-manifest.json")
    )
    _require_matching_repository(release_url, manifest)
    if manifest["version"] != version:
        raise InstallerError(
            "base release manifest version %s does not match the requested version %s"
            % (manifest["version"], version)
        )
    if manifest["repository"].casefold() != current_manifest["repository"].casefold():
        raise InstallerError("base and current release repositories do not match")

    # This is deliberately a closed release inventory. A future release that
    # adds a signed sidecar or another asset must update this contract and its
    # fixtures in the same change before that release can be used as a base.
    expected_assets = {MANIFEST_ASSET, INSTALLER_ASSET}
    expected_assets.update(
        record["asset"] for record in manifest["locales"].values()
    )
    if set(sums) != expected_assets:
        missing = sorted(expected_assets - set(sums))
        unexpected = sorted(set(sums) - expected_assets)
        raise InstallerError(
            "base SHA256SUMS asset inventory differs (missing: %s; unexpected: %s)"
            % (missing or "none", unexpected or "none")
        )
    installer_record = manifest["installer"]
    if sums[INSTALLER_ASSET] != installer_record["sha256"]:
        raise InstallerError(
            "base SHA256SUMS and release manifest disagree about installer.py"
        )
    for tag, record in manifest["locales"].items():
        if sums[record["asset"]] != record["sha256"]:
            raise InstallerError(
                "base SHA256SUMS and release manifest disagree about locale %s" % tag
            )

    installer_data = _fetch(
        _asset_url(release_url, version, INSTALLER_ASSET), MANIFEST_MAX_BYTES
    )
    if (
        len(installer_data) != installer_record["bytes"]
        or _sha256(installer_data) != installer_record["sha256"]
    ):
        raise InstallerError("base installer.py does not match its manifest record")

    record = _selected_locale_record(manifest, locale)
    archive = _fetch(
        _asset_url(release_url, version, record["asset"]), ARCHIVE_MAX_BYTES
    )
    if len(archive) != record["bytes"]:
        raise InstallerError(
            "base locale %s archive size %d does not match the manifest declaration %d"
            % (locale, len(archive), record["bytes"])
        )
    members = _read_verified_archive(archive, locale, record)
    return manifest, record, members


def _require_matching_repository(
    release_url: str, manifest: Mapping[str, Any]
) -> None:
    expected = _github_repository(release_url)
    if (
        expected is not None
        and manifest["repository"].casefold() != expected.casefold()
    ):
        raise InstallerError(
            "release manifest repository %s does not match release URL repository %s"
            % (manifest["repository"], expected)
        )


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
            "For an existing repository, run 'adopt' to stage the verified artifact with a "
            "per-path adoption plan, or install into an empty directory."
            % (len(conflicts), ", ".join(conflicts))
        )
    created_dirs: list[Path] = []
    created_files: list[Path] = []
    try:
        if not root.exists():
            root.mkdir()
            created_dirs.append(root)
            os.chmod(root, 0o755)
        for name in ordered:
            path = _validated_member_path(name)
            _ensure_parent_dirs(root, path, created_dirs)
            target = root.joinpath(*path.parts)
            with open(target, "xb") as handle:
                created_files.append(target)
                handle.write(members[name])
            os.chmod(target, FILE_MODE)
    except (InstallerError, OSError) as exc:
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
            created.append(current)
            os.chmod(current, 0o755)
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
    _publish_directory(Path(output), members)
    return tuple(sorted(members))


def _publish_directory(output: Path, files: Mapping[str, bytes]) -> None:
    """Stage *files* next to an empty output directory and publish them atomically."""

    output = _validated_export_output(output)
    stage = Path(tempfile.mkdtemp(prefix=".template-install-", dir=output.parent))
    published = False
    try:
        for name in sorted(files):
            path = _validated_member_path(name)
            target = stage.joinpath(*path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[name])
            os.chmod(target, FILE_MODE)
        if output.exists():
            output.rmdir()
        os.replace(stage, output)
        published = True
    except OSError as exc:
        raise InstallerError("cannot publish the output directory: %s" % exc) from exc
    finally:
        if not published:
            shutil.rmtree(stage, ignore_errors=True)


def adopt(
    release_url: str,
    version: str,
    locale: str,
    repo_root: Path,
    output: Path,
    *,
    installer_bytes: Optional[bytes] = None,
    base_version: Optional[str] = None,
) -> Mapping[str, Any]:
    """Verify a release and stage it with a read-only plan for an existing repository.

    The target repository is only listed, stat-ed and read. The verified artifact
    and the plan are published together into an empty output directory that must
    be outside the repository.
    """

    release_url = _validated_release_url(release_url)
    version = _validated_version_selection(version)
    if base_version is not None:
        base_version = _validated_base_version(base_version)
    root = _validated_adoption_root(Path(repo_root))
    output = _validated_export_output(Path(output))
    _require_separate_trees(root, output)
    manifest = _verified_manifest(release_url, version, _running_installer_bytes(installer_bytes))
    record = _selected_locale_record(manifest, locale)
    members = _verified_members(release_url, manifest, locale)
    if base_version is None:
        plan = adoption_plan(root, manifest, locale, record, members)
    else:
        _require_older_base_version(base_version, manifest["version"])
        base_manifest, base_record, base_members = _verified_base_release(
            release_url, base_version, locale, manifest
        )
        plan = upgrade_adoption_plan(
            root,
            manifest,
            locale,
            record,
            members,
            base_manifest,
            base_record,
            base_members,
        )
    files = {
        "%s/%s" % (ADOPTION_ARTIFACT_DIR, name): data for name, data in members.items()
    }
    files[ADOPTION_PLAN_NAME] = _plan_bytes(plan)
    _publish_directory(output, files)
    return plan


def _validated_adoption_root(path: Path) -> Path:
    root = path.absolute()
    if root.is_symlink() or not root.is_dir():
        raise InstallerError(
            "repo root must be an existing directory, not a symlink; "
            "use 'install' for a new project"
        )
    return root


def _require_separate_trees(root: Path, output: Path) -> None:
    real_root = root.resolve()
    real_output = output.resolve(strict=False)
    if (
        real_output == real_root
        or real_root in real_output.parents
        or real_output in real_root.parents
    ):
        raise InstallerError(
            "adoption output must be outside the repository root and must not contain it"
        )


def adoption_plan(
    root: Path,
    manifest: Mapping[str, Any],
    locale: str,
    record: Mapping[str, Any],
    members: Mapping[str, bytes],
) -> dict[str, Any]:
    """Classify every artifact path against the target without modifying it."""

    listings: dict[Path, Optional[tuple[str, ...]]] = {}
    entries = []
    for member in sorted(record["members"], key=lambda item: item["path"]):
        name = member["path"]
        policy = member["policy"]
        state, target_sha256 = _adoption_target(
            root, _validated_member_path(name), listings
        )
        artifact_sha256 = _sha256(members[name])
        status = _adoption_status(policy, state, target_sha256, artifact_sha256)
        entries.append(
            {
                "path": name,
                "policy": policy,
                "status": status,
                "target": state,
                "artifact_sha256": artifact_sha256,
                "target_sha256": target_sha256,
                "reason": _adoption_reason(status, policy, state),
            }
        )
    summary = {status: 0 for status in ADOPTION_STATUSES}
    for entry in entries:
        summary[entry["status"]] += 1
    return {
        "format": ADOPTION_FORMAT,
        "format_version": ADOPTION_FORMAT_VERSION,
        "stability": "experimental",
        "release": {
            "repository": manifest["repository"],
            "version": manifest["version"],
            "source_commit": manifest["source_commit"],
            "locale": locale,
        },
        "guide": ADOPTION_GUIDE,
        "summary": summary,
        "paths": entries,
    }


def upgrade_adoption_plan(
    root: Path,
    manifest: Mapping[str, Any],
    locale: str,
    record: Mapping[str, Any],
    members: Mapping[str, bytes],
    base_manifest: Mapping[str, Any],
    base_record: Mapping[str, Any],
    base_members: Mapping[str, bytes],
) -> dict[str, Any]:
    """Classify the base/current inventory union without modifying the target."""

    current_records = {member["path"]: member for member in record["members"]}
    base_records = {member["path"]: member for member in base_record["members"]}
    listings: dict[Path, Optional[tuple[str, ...]]] = {}
    entries = []
    for name in sorted(set(base_records) | set(current_records)):
        state, target_sha256 = _adoption_target(
            root, _validated_member_path(name), listings
        )
        base_sha256 = _sha256(base_members[name]) if name in base_members else None
        artifact_sha256 = _sha256(members[name]) if name in members else None
        upgrade_status = _upgrade_status(
            state, base_sha256, artifact_sha256, target_sha256
        )
        current_member = current_records.get(name)
        if current_member is None:
            policy = None
            status = None
            reason = (
                _adoption_reason("blocked", "", state)
                if upgrade_status == "blocked"
                else UPGRADE_REMOVAL_REASON
            )
        else:
            policy = current_member["policy"]
            status = _adoption_status(
                policy, state, target_sha256, artifact_sha256
            )
            reason = _adoption_reason(status, policy, state)
        entries.append(
            {
                "path": name,
                "policy": policy,
                "status": status,
                "upgrade_status": upgrade_status,
                "target": state,
                "base_sha256": base_sha256,
                "artifact_sha256": artifact_sha256,
                "target_sha256": target_sha256,
                "reason": reason,
            }
        )

    summary = {status: 0 for status in ADOPTION_STATUSES}
    upgrade_summary = {status: 0 for status in UPGRADE_STATUSES}
    for entry in entries:
        if entry["status"] is not None:
            summary[entry["status"]] += 1
        upgrade_summary[entry["upgrade_status"]] += 1
    return {
        "format": ADOPTION_FORMAT,
        "format_version": ADOPTION_UPGRADE_FORMAT_VERSION,
        "stability": "experimental",
        "base_release": {
            "repository": base_manifest["repository"],
            "version": base_manifest["version"],
            "source_commit": base_manifest["source_commit"],
            "locale": locale,
        },
        "release": {
            "repository": manifest["repository"],
            "version": manifest["version"],
            "source_commit": manifest["source_commit"],
            "locale": locale,
        },
        "guide": ADOPTION_GUIDE,
        "summary": summary,
        "upgrade_summary": upgrade_summary,
        "paths": entries,
    }


def _adoption_target(
    root: Path,
    path: PurePosixPath,
    listings: dict[Path, Optional[tuple[str, ...]]],
) -> tuple[str, Optional[str]]:
    """Return the target state and file hash using only list, lstat and read calls."""

    current = root
    parts = path.parts
    for index, segment in enumerate(parts):
        last = index == len(parts) - 1
        if current not in listings:
            try:
                listings[current] = tuple(os.listdir(current))
            except OSError:
                listings[current] = None
        names = listings[current]
        if names is None:
            return "unreadable", None
        if segment not in names:
            folded = segment.casefold()
            if any(name.casefold() == folded for name in names):
                return "case-variant", None
            return "absent", None
        current = current / segment
        try:
            mode = current.lstat().st_mode
        except OSError:
            return "unreadable", None
        if stat.S_ISLNK(mode):
            return ("symlink" if last else "parent-symlink"), None
        if not last:
            if not stat.S_ISDIR(mode):
                return "parent-not-directory", None
            continue
        if not stat.S_ISREG(mode):
            return "special", None
        digest = hashlib.sha256()
        try:
            with open(current, "rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    digest.update(chunk)
        except OSError:
            return "unreadable", None
        return "file", digest.hexdigest()
    raise InstallerError("artifact member path is empty")


def _adoption_status(
    policy: str, state: str, target_sha256: Optional[str], artifact_sha256: str
) -> str:
    if state not in ("absent", "file"):
        return "blocked"
    if policy == "decide":
        return "decision"
    if state == "absent":
        return "missing"
    return "identical" if target_sha256 == artifact_sha256 else "merge"


def _upgrade_status(
    state: str,
    base_sha256: Optional[str],
    artifact_sha256: Optional[str],
    target_sha256: Optional[str],
) -> str:
    """Classify the base/current/target equality partition; None means absent."""

    if state not in ("absent", "file"):
        return "blocked"
    if base_sha256 == artifact_sha256 == target_sha256:
        return "unchanged"
    if base_sha256 == target_sha256 and artifact_sha256 != base_sha256:
        return "template-only"
    if base_sha256 == artifact_sha256 and target_sha256 != base_sha256:
        return "project-only"
    if artifact_sha256 == target_sha256 and base_sha256 != artifact_sha256:
        return "converged"
    return "diverged"


def _adoption_reason(status: str, policy: str, state: str) -> str:
    if status == "blocked":
        return "Resolve the %s target path by hand before adopting this file." % state
    if status == "decision":
        return ADOPTION_REASONS[(status, state)]
    return ADOPTION_REASONS[(status, policy)]


def _plan_bytes(plan: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(plan, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _print_adoption_summary(plan: Mapping[str, Any], output: Path) -> None:
    release = plan["release"]
    summary = plan["summary"]
    if plan["format_version"] == ADOPTION_UPGRADE_FORMAT_VERSION:
        print(
            "Upgrade classification assumes the target was derived from base %s; "
            "absence alone cannot prove a project deletion."
            % plan["base_release"]["version"]
        )
    print(
        "Adoption plan for %s %s: %d paths (%s)"
        % (
            release["locale"],
            release["version"],
            sum(summary.values()),
            ", ".join("%s %d" % (status, summary[status]) for status in ADOPTION_STATUSES),
        )
    )
    for status in ADOPTION_STATUSES:
        if status == "identical":
            continue
        paths = [entry["path"] for entry in plan["paths"] if entry["status"] == status]
        if paths:
            print("%s:" % status)
            for path in paths:
                print("  %s" % path)
    if plan["format_version"] == ADOPTION_UPGRADE_FORMAT_VERSION:
        upgrade_summary = plan["upgrade_summary"]
        print(
            "Upgrade classification: %d paths (%s)"
            % (
                len(plan["paths"]),
                ", ".join(
                    "%s %d" % (status, upgrade_summary[status])
                    for status in UPGRADE_STATUSES
                ),
            )
        )
        for status in UPGRADE_STATUSES:
            if status == "unchanged":
                continue
            paths = [
                entry["path"]
                for entry in plan["paths"]
                if entry["upgrade_status"] == status
            ]
            if paths:
                print("upgrade %s:" % status)
                for path in paths:
                    print("  %s" % path)
    print(
        "Wrote %s and %s/ in %s. The target repository was not modified; "
        "follow %s to merge."
        % (ADOPTION_PLAN_NAME, ADOPTION_ARTIFACT_DIR, output, plan["guide"])
    )


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

    adopt_parser = subparsers.add_parser(
        "adopt",
        help="stage one verified locale with a read-only adoption plan for an existing repository",
    )
    _add_remote_arguments(adopt_parser)
    adopt_parser.add_argument("--repo-root", required=True, type=Path, help="existing project root; never modified")
    adopt_parser.add_argument("--output", required=True, type=Path, help="empty output directory outside the project")
    adopt_parser.add_argument("--locale", required=True, help="complete locale tag from the release manifest")
    adopt_parser.add_argument("--version", default=LATEST_VERSION, help="release version, or 'latest'")
    adopt_parser.add_argument(
        "--base-version",
        help="older exact SemVer previously applied to the target; adopt only",
    )

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
        elif args.command == "adopt":
            plan = adopt(
                args.release_url,
                args.version,
                args.locale,
                args.repo_root,
                args.output,
                base_version=args.base_version,
            )
            _print_adoption_summary(plan, args.output)
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
        help="GitHub Releases root (https://github.com/OWNER/NAME/releases)",
    )


if __name__ == "__main__":
    raise SystemExit(main())
