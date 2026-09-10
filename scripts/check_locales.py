#!/usr/bin/env python3
"""Validate locale source inventories and cross-locale contracts.

The manifest is the source of truth for locale tags, source roots, output
paths, stable markers, commands, and skill contracts.  This checker never
discovers a new supported locale or output member implicitly.
"""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, DefaultDict, Dict, List, Mapping, Optional, Sequence, Set, Tuple


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = Path("locales/manifest.json")

BCP47_RE = re.compile(
    r"[a-z]{2,3}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|[0-9]{3}))?"
)
SEMVER_RE = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
ID_RE = re.compile(r"[a-z][a-z0-9-]*")
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
PLACEHOLDER_TOKEN_RE = re.compile(r"\{\{[^{}\r\n]+\}\}")
SECTION_MARKER_RE = re.compile(
    r"^<!-- template-(?:section|example):[a-z][a-z0-9-]* -->$", re.MULTILINE
)
SKILL_MARKER_RE = re.compile(
    r"^<!-- template-skill-contract:[a-z][a-z0-9-]*:v[1-9][0-9]* -->$",
    re.MULTILINE,
)
SKILL_FIXTURE_MARKER_RE = re.compile(
    r"^<!-- template-skill-fixture:[a-z][a-z0-9-]* -->$", re.MULTILINE
)
SKILL_TEMPLATE_MARKER_RE = re.compile(
    r"^<!-- template-skill-(?:contract:[a-z][a-z0-9-]*:v[1-9][0-9]*|"
    r"fixture:[a-z][a-z0-9-]*) -->$",
    re.MULTILINE,
)
TEMPLATE_MARKER_RE = re.compile(r"^<!-- template-[^>\r\n]+ -->$", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
LINK_TARGET_RE = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
NUMBERED_HEADING_RE = re.compile(
    r"^(#{1,6})[ \t]+(\d+(?:\.\d+)*)(?=[. \t])", re.MULTILINE
)
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
TEMPLATE_CONTRACT_ASSERTION_RE = re.compile(
    r"^> \[template-contract:[^]\r\n]+\] [^\r\n]+$", re.MULTILINE
)
TOP_LEVEL_FRONTMATTER_FIELD_RE = re.compile(
    r"^([A-Za-z][A-Za-z0-9-]*)[ \t]*:(.*)$"
)
FENCE_LINE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")
BLOCKQUOTE_MARKER_RE = re.compile(r"[ ]{0,3}>[ \t]?")
PROJECT_INVARIANT_EXAMPLE_PREFIXES = ("- **Example:**", "- **예시:**")

ALLOWED_STATUSES = frozenset(("complete", "experimental", "stale"))
IGNORED_SOURCE_PARTS = frozenset(("__pycache__",))
IGNORED_SOURCE_SUFFIXES = frozenset((".pyc", ".pyo"))
WINDOWS_RESERVED_COMPONENTS = frozenset(
    ("con", "prn", "aux", "nul")
    + tuple("com%d" % number for number in range(1, 10))
    + tuple("lpt%d" % number for number in range(1, 10))
)

# These checks deliberately use only protocol identifiers, stable paths,
# front-matter keys, and manifest-backed markers.  Translated prose is never a
# fixture oracle.
SKILL_FIXTURE_REGISTRY: Mapping[str, Mapping[str, Any]] = {
    "design-minimal-artifact": {
        "skill_id": "design",
        "assertion": (
            "> [template-contract:v1] "
            "MUST_USE_MINIMUM_REQUIRED_DESIGN_ARTIFACTS"
        ),
        "skill_links": ("../../../docs/01-DESIGN.md",),
        "skill_tokens": ("§1", "§2", "§3"),
    },
    "design-requires-approval": {
        "skill_id": "design",
        "assertion": (
            "> [template-contract:v1] "
            "MUST_NOT_IMPLEMENT_BEFORE_USER_AGREEMENT"
        ),
        "document": "docs/01-DESIGN.md",
        "document_tokens": ("Draft", "Accepted", "Superseded", "Rejected"),
    },
    "design-reuses-accepted-spec": {
        "skill_id": "design",
        "assertion": (
            "> [template-contract:v1] "
            "MUST_REUSE_ACCEPTED_SCOPE_WITHOUT_REAPPROVAL"
        ),
        "skill_tokens": ("INTENT", "SPEC", "PLAN"),
        "skill_links": ("../../../docs/02-TODO.md",),
    },
    "review-round-explicit-only": {
        "skill_id": "review-round",
        "assertion": (
            "> [template-contract:v1] "
            "MUST_REQUIRE_EXPLICIT_USER_INVOCATION"
        ),
        "skill_tokens": ("disable-model-invocation: true",),
        "common_document": ".agents/skills/review-round/agents/openai.yaml",
        "common_tokens": ("policy:", "allow_implicit_invocation: false"),
        "common_implicit_invocation": False,
    },
    "review-round-exact-head-gate": {
        "skill_id": "review-round",
        "assertion": (
            "> [template-contract:v1] MUST_GATE_ON_EXACT_HEAD_AND_BASE"
        ),
        "skill_links": (
            "../../../docs/REVIEW.md",
            "../../../docs/REVIEW_ROUND.md",
        ),
        "document": "docs/REVIEW_ROUND.md",
        "document_tokens": ("head SHA", "base"),
    },
    "review-round-user-confirmed-merge": {
        "skill_id": "review-round",
        "assertion": (
            "> [template-contract:v1] "
            "MUST_REQUIRE_USER_CONFIRMATION_BEFORE_MERGE"
        ),
        "skill_tokens": ("on_pass",),
        "document": "docs/REVIEW_ROUND.md",
        "document_tokens": ("on_pass", "head", "base", "merge"),
    },
}


class ManifestError(ValueError):
    """Raised for JSON input that cannot represent a manifest."""


def _duplicate_rejecting_object(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ManifestError("duplicate JSON key %r" % key)
        result[key] = value
    return result


def _has_symlink_component(repository_root: Path, path: Path) -> bool:
    cursor = repository_root
    for part in path.relative_to(repository_root).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return True
    return False


def _read_manifest(
    path: Path, errors: List[str], repository_root: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    if repository_root is not None and _has_symlink_component(repository_root, path):
        errors.append("manifest path must not contain a symlink: %s" % path)
        return None
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        errors.append("cannot stat manifest %s: %s" % (path, exc))
        return None
    if not stat.S_ISREG(mode):
        errors.append("manifest must be a regular file: %s" % path)
        return None
    try:
        raw = path.read_bytes()
    except OSError as exc:
        errors.append("cannot read manifest %s: %s" % (path, exc))
        return None
    if b"\r" in raw:
        errors.append("manifest must use LF line endings: %s" % path)
    if not raw.endswith(b"\n"):
        errors.append("manifest is missing a final newline: %s" % path)
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_duplicate_rejecting_object
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ManifestError) as exc:
        errors.append("invalid manifest %s: %s" % (path, exc))
        return None
    if not isinstance(value, dict):
        errors.append("manifest root must be an object")
        return None
    return value


def _require_keys(
    value: Mapping[str, Any], keys: Sequence[str], label: str, errors: List[str]
) -> bool:
    expected = set(keys)
    missing = [key for key in keys if key not in value]
    unexpected = sorted(set(value) - expected)
    if missing:
        errors.append("%s is missing required field(s): %s" % (label, ", ".join(missing)))
    if unexpected:
        errors.append(
            "%s has unexpected field(s): %s" % (label, ", ".join(unexpected))
        )
    return not missing and not unexpected


def _is_safe_relative_path(value: Any) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or value == "."
        or "\\" in value
        or ":" in value
        or any(ord(character) < 32 for character in value)
    ):
        return False
    path = PurePosixPath(value)
    components = path.parts
    return (
        not path.is_absolute()
        and path.as_posix() == value
        and all(part not in ("", ".", "..") for part in components)
        and all(not part.endswith((".", " ")) for part in components)
        and all(
            part.split(".", 1)[0].rstrip(" ").casefold()
            not in WINDOWS_RESERVED_COMPONENTS
            for part in components
        )
    )


def _validate_path_list(value: Any, label: str, errors: List[str]) -> bool:
    if not isinstance(value, list):
        errors.append("%s must be an array" % label)
        return False
    valid = True
    seen: Set[str] = set()
    seen_casefolded: Dict[str, str] = {}
    for index, item in enumerate(value):
        item_label = "%s[%d]" % (label, index)
        if not _is_safe_relative_path(item):
            errors.append("%s must be a normalized relative POSIX path" % item_label)
            valid = False
            continue
        if item in seen:
            errors.append("%s contains duplicate path %r" % (label, item))
            valid = False
        seen.add(item)
        folded = item.casefold()
        if folded in seen_casefolded and seen_casefolded[folded] != item:
            errors.append(
                "%s contains case-fold-colliding paths %r and %r"
                % (label, seen_casefolded[folded], item)
            )
            valid = False
        seen_casefolded[folded] = item
    return valid


def _validate_manifest_schema(manifest: Mapping[str, Any], errors: List[str]) -> bool:
    start = len(errors)
    if not _require_keys(
        manifest,
        ("schema_version", "baseline", "required_stable_locales", "artifact", "contracts", "locales"),
        "manifest",
        errors,
    ):
        return False
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        errors.append("schema_version must be integer 1")

    baseline = manifest["baseline"]
    if not isinstance(baseline, dict):
        errors.append("baseline must be an object")
    elif _require_keys(baseline, ("template_version", "source_commit"), "baseline", errors):
        version = baseline["template_version"]
        commit = baseline["source_commit"]
        if not _is_semver(version):
            errors.append("baseline.template_version must be SemVer")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append("baseline.source_commit must be a lowercase full SHA")

    required = manifest["required_stable_locales"]
    if not isinstance(required, list) or not required:
        errors.append("required_stable_locales must be a non-empty array")
    elif not all(isinstance(tag, str) for tag in required):
        errors.append("required_stable_locales entries must be strings")
    elif len(required) != len(set(required)):
        errors.append("required_stable_locales contains a duplicate tag")

    artifact = manifest["artifact"]
    if not isinstance(artifact, dict):
        errors.append("artifact must be an object")
    elif _require_keys(
        artifact,
        ("excluded_baseline_paths", "renamed_baseline_paths", "common_root", "common_paths", "localized_paths"),
        "artifact",
        errors,
    ):
        if not _is_safe_relative_path(artifact["common_root"]):
            errors.append("artifact.common_root must be a normalized relative POSIX path")
        _validate_path_list(
            artifact["excluded_baseline_paths"],
            "artifact.excluded_baseline_paths",
            errors,
        )
        _validate_path_list(artifact["common_paths"], "artifact.common_paths", errors)
        _validate_path_list(
            artifact["localized_paths"], "artifact.localized_paths", errors
        )
        renamed = artifact["renamed_baseline_paths"]
        if not isinstance(renamed, dict):
            errors.append("artifact.renamed_baseline_paths must be an object")
        else:
            for source, destination in renamed.items():
                if not _is_safe_relative_path(source) or not _is_safe_relative_path(destination):
                    errors.append(
                        "artifact.renamed_baseline_paths must map normalized relative POSIX paths"
                    )

    contracts = manifest["contracts"]
    if not isinstance(contracts, dict):
        errors.append("contracts must be an object")
    elif _require_keys(
        contracts, ("section_markers", "required_commands", "skills"), "contracts", errors
    ):
        _validate_section_contracts(contracts["section_markers"], errors)
        _validate_command_contracts(contracts["required_commands"], errors)
        _validate_skill_contracts(contracts["skills"], errors)

    locales = manifest["locales"]
    if not isinstance(locales, dict) or not locales:
        errors.append("locales must be a non-empty object")
    else:
        for tag, entry in locales.items():
            label = "locales.%s" % tag
            if not isinstance(entry, dict):
                errors.append("%s must be an object" % label)
                continue
            if not _require_keys(entry, ("status", "source_root", "baseline_version"), label, errors):
                continue
            if not isinstance(entry["status"], str) or entry["status"] not in ALLOWED_STATUSES:
                errors.append(
                    "%s.status must be one of %s"
                    % (label, ", ".join(sorted(ALLOWED_STATUSES)))
                )
            if not _is_safe_relative_path(entry["source_root"]):
                errors.append("%s.source_root must be a normalized relative POSIX path" % label)
            version = entry["baseline_version"]
            if not _is_semver(version):
                errors.append("%s.baseline_version must be SemVer" % label)

    return len(errors) == start


def _validate_contract_array(value: Any, label: str, errors: List[str]) -> bool:
    if not isinstance(value, list) or not value:
        errors.append("%s must be a non-empty array" % label)
        return False
    return True


def _validate_section_contracts(value: Any, errors: List[str]) -> None:
    label = "contracts.section_markers"
    if not _validate_contract_array(value, label, errors):
        return
    ids: Set[str] = set()
    markers: Set[str] = set()
    for index, item in enumerate(value):
        item_label = "%s[%d]" % (label, index)
        if not isinstance(item, dict) or not _require_keys(item, ("id", "marker", "paths"), item_label, errors):
            if not isinstance(item, dict):
                errors.append("%s must be an object" % item_label)
            continue
        contract_id = item["id"]
        marker = item["marker"]
        if not isinstance(contract_id, str) or not ID_RE.fullmatch(contract_id):
            errors.append("%s.id must be a stable lowercase ID" % item_label)
        elif contract_id in ids:
            errors.append("%s contains duplicate id %r" % (label, contract_id))
        else:
            ids.add(contract_id)
        if not isinstance(marker, str) or not SECTION_MARKER_RE.fullmatch(marker):
            errors.append("%s.marker is not a stable section/example marker" % item_label)
        elif marker in markers:
            errors.append("%s contains duplicate marker %r" % (label, marker))
        else:
            markers.add(marker)
        _validate_path_list(item["paths"], "%s.paths" % item_label, errors)
        if isinstance(item["paths"], list) and not item["paths"]:
            errors.append("%s.paths must not be empty" % item_label)


def _validate_command_contracts(value: Any, errors: List[str]) -> None:
    label = "contracts.required_commands"
    if not _validate_contract_array(value, label, errors):
        return
    ids: Set[str] = set()
    values: Set[str] = set()
    for index, item in enumerate(value):
        item_label = "%s[%d]" % (label, index)
        if not isinstance(item, dict) or not _require_keys(item, ("id", "value", "paths"), item_label, errors):
            if not isinstance(item, dict):
                errors.append("%s must be an object" % item_label)
            continue
        contract_id = item["id"]
        command = item["value"]
        if not isinstance(contract_id, str) or not ID_RE.fullmatch(contract_id):
            errors.append("%s.id must be a stable lowercase ID" % item_label)
        elif contract_id in ids:
            errors.append("%s contains duplicate id %r" % (label, contract_id))
        else:
            ids.add(contract_id)
        if (
            not isinstance(command, str)
            or not command.strip()
            or command != command.strip()
            or "\n" in command
            or "`" in command
        ):
            errors.append("%s.value must be one unquoted command line" % item_label)
        elif command in values:
            errors.append("%s contains duplicate command %r" % (label, command))
        else:
            values.add(command)
        _validate_path_list(item["paths"], "%s.paths" % item_label, errors)
        if isinstance(item["paths"], list) and not item["paths"]:
            errors.append("%s.paths must not be empty" % item_label)


def _validate_skill_contracts(value: Any, errors: List[str]) -> None:
    label = "contracts.skills"
    if not _validate_contract_array(value, label, errors):
        return
    ids: Set[str] = set()
    markers: Set[str] = set()
    fixture_ids: Set[str] = set()
    fixture_owners: Dict[str, str] = {}
    for index, item in enumerate(value):
        item_label = "%s[%d]" % (label, index)
        if not isinstance(item, dict) or not _require_keys(
            item, ("id", "marker", "paths", "fixture_ids"), item_label, errors
        ):
            if not isinstance(item, dict):
                errors.append("%s must be an object" % item_label)
            continue
        contract_id = item["id"]
        marker = item["marker"]
        if not isinstance(contract_id, str) or not ID_RE.fullmatch(contract_id):
            errors.append("%s.id must be a stable lowercase ID" % item_label)
        elif contract_id in ids:
            errors.append("%s contains duplicate id %r" % (label, contract_id))
        else:
            ids.add(contract_id)
        if not isinstance(marker, str) or not SKILL_MARKER_RE.fullmatch(marker):
            errors.append("%s.marker is not a stable skill marker" % item_label)
        elif isinstance(contract_id, str) and ID_RE.fullmatch(contract_id) and (
            re.fullmatch(
                r"<!-- template-skill-contract:%s:v[1-9][0-9]* -->"
                % re.escape(contract_id),
                marker,
            )
            is None
        ):
            errors.append("%s.marker does not match its skill id" % item_label)
        else:
            if marker in markers:
                errors.append("%s contains duplicate marker %r" % (label, marker))
            markers.add(marker)
        paths = item["paths"]
        _validate_path_list(paths, "%s.paths" % item_label, errors)
        if isinstance(paths, list) and len(paths) != 2:
            errors.append("%s.paths must contain the .agents/.claude skill pair" % item_label)
        fixtures = item["fixture_ids"]
        if not isinstance(fixtures, list) or not fixtures:
            errors.append("%s.fixture_ids must be a non-empty array" % item_label)
        else:
            local_seen: Set[str] = set()
            for fixture in fixtures:
                if not isinstance(fixture, str) or not ID_RE.fullmatch(fixture):
                    errors.append("%s contains an invalid fixture ID" % item_label)
                elif isinstance(contract_id, str) and not fixture.startswith(
                    contract_id + "-"
                ):
                    errors.append(
                        "%s fixture ID %r does not belong to skill %s"
                        % (item_label, fixture, contract_id)
                    )
                elif fixture in local_seen or fixture in fixture_ids:
                    errors.append("duplicate skill fixture ID %r" % fixture)
                else:
                    local_seen.add(fixture)
                    fixture_ids.add(fixture)
                    fixture_owners[fixture] = contract_id

    registered = set(SKILL_FIXTURE_REGISTRY)
    for fixture in sorted(fixture_ids - registered):
        errors.append("skill fixture %r has no fixture implementation" % fixture)
    for fixture in sorted(registered - fixture_ids):
        errors.append("fixture registry entry %r is not declared in the manifest" % fixture)
    for fixture in sorted(fixture_ids & registered):
        expected_owner = SKILL_FIXTURE_REGISTRY[fixture]["skill_id"]
        if fixture_owners.get(fixture) != expected_owner:
            errors.append(
                "skill fixture %r belongs to %s, not %s"
                % (fixture, expected_owner, fixture_owners.get(fixture))
            )


def _check_locale_metadata(manifest: Mapping[str, Any], errors: List[str]) -> None:
    locales = manifest["locales"]
    required = manifest["required_stable_locales"]
    baseline_version = manifest["baseline"]["template_version"]

    for tag in list(locales) + list(required):
        if "_" in tag:
            errors.append("locale tag %r must use BCP 47 hyphens, not underscores" % tag)
        elif not BCP47_RE.fullmatch(tag):
            errors.append(
                "locale tag %r is outside the supported canonical BCP 47 form "
                "language[-Script][-REGION]" % tag
            )
    unknown_required = sorted(set(required) - set(locales))
    for tag in unknown_required:
        errors.append("required stable locale %r is not in the manifest allowlist" % tag)

    roots: Dict[str, str] = {}
    folded_tags: Dict[str, str] = {}
    folded_roots: Dict[str, str] = {}
    for tag, entry in locales.items():
        source_root = entry["source_root"]
        expected_suffix = PurePosixPath("locales") / tag
        if PurePosixPath(source_root) != expected_suffix:
            errors.append(
                "%s source_root must be %s" % (tag, expected_suffix.as_posix())
            )
        if source_root in roots:
            errors.append(
                "locale source_root %r is shared by %s and %s"
                % (source_root, roots[source_root], tag)
            )
        roots[source_root] = tag
        folded_tag = tag.casefold()
        if folded_tag in folded_tags and folded_tags[folded_tag] != tag:
            errors.append(
                "locale tags collide after case-folding: %s and %s"
                % (folded_tags[folded_tag], tag)
            )
        folded_tags[folded_tag] = tag
        folded_root = source_root.casefold()
        if folded_root in folded_roots and folded_roots[folded_root] != source_root:
            errors.append(
                "locale source roots collide after case-folding: %s and %s"
                % (folded_roots[folded_root], source_root)
            )
        folded_roots[folded_root] = source_root
        status = entry["status"]
        version = entry["baseline_version"]
        if status == "complete" and version != baseline_version:
            errors.append(
                "%s is complete but baseline_version %s does not match %s"
                % (tag, version, baseline_version)
            )
        if status == "stale" and _compare_semver(version, baseline_version) >= 0:
            errors.append(
                "%s is stale but baseline_version %s is not older than %s"
                % (tag, version, baseline_version)
            )


def _parse_semver(version: Any) -> Optional[Tuple[Tuple[int, int, int], Optional[Tuple[str, ...]]]]:
    if not isinstance(version, str):
        return None
    match = SEMVER_RE.fullmatch(version)
    if match is None:
        return None
    prerelease_text = match.group(4)
    prerelease = tuple(prerelease_text.split(".")) if prerelease_text else None
    if prerelease is not None and any(
        identifier.isdigit()
        and len(identifier) > 1
        and identifier.startswith("0")
        for identifier in prerelease
    ):
        return None
    return (
        (int(match.group(1)), int(match.group(2)), int(match.group(3))),
        prerelease,
    )


def _is_semver(version: Any) -> bool:
    return _parse_semver(version) is not None


def _compare_semver(left: str, right: str) -> int:
    left_parsed = _parse_semver(left)
    right_parsed = _parse_semver(right)
    if left_parsed is None or right_parsed is None:
        raise ValueError("SemVer comparison requires validated versions")
    left_core, left_pre = left_parsed
    right_core, right_pre = right_parsed
    if left_core != right_core:
        return -1 if left_core < right_core else 1
    if left_pre is None or right_pre is None:
        if left_pre is right_pre:
            return 0
        return 1 if left_pre is None else -1
    for left_id, right_id in zip(left_pre, right_pre):
        if left_id == right_id:
            continue
        left_numeric = left_id.isdigit()
        right_numeric = right_id.isdigit()
        if left_numeric and right_numeric:
            return -1 if int(left_id) < int(right_id) else 1
        if left_numeric != right_numeric:
            return -1 if left_numeric else 1
        return -1 if left_id < right_id else 1
    if len(left_pre) == len(right_pre):
        return 0
    return -1 if len(left_pre) < len(right_pre) else 1


def complete_locales(manifest: Mapping[str, Any]) -> Tuple[str, ...]:
    """Return locales eligible for inclusion as complete payloads.

    W-004 can use this result without treating an intentional experimental
    locale as a source-validation error.
    """

    baseline = manifest["baseline"]["template_version"]
    return tuple(
        sorted(
            tag
            for tag, entry in manifest["locales"].items()
            if entry["status"] == "complete"
            and entry["baseline_version"] == baseline
        )
    )


def stable_release_errors(manifest: Mapping[str, Any]) -> List[str]:
    """Return required-locale failures for a stable release gate."""

    complete = set(complete_locales(manifest))
    return [
        "required stable locale %r is not complete" % tag
        for tag in manifest["required_stable_locales"]
        if tag not in complete
    ]


def _collect_source_files(
    repository_root: Path, source_root: Path, label: str, errors: List[str]
) -> Set[str]:
    if _has_symlink_component(repository_root, source_root):
        errors.append("%s source path must not contain a symlink: %s" % (label, source_root))
        return set()
    if not source_root.is_dir():
        errors.append("%s source root is missing: %s" % (label, source_root))
        return set()
    files: Set[str] = set()
    try:
        entries = sorted(source_root.rglob("*"))
    except OSError as exc:
        errors.append("cannot walk %s source root: %s" % (label, exc))
        return set()
    for entry in entries:
        relative = entry.relative_to(source_root)
        try:
            mode = entry.lstat().st_mode
        except OSError as exc:
            errors.append("cannot stat %s: %s" % (entry, exc))
            continue
        if stat.S_ISLNK(mode):
            errors.append("%s source contains symlink: %s" % (label, relative.as_posix()))
        elif any(part in IGNORED_SOURCE_PARTS for part in relative.parts):
            continue
        elif entry.suffix in IGNORED_SOURCE_SUFFIXES:
            continue
        elif stat.S_ISDIR(mode):
            continue
        elif not stat.S_ISREG(mode):
            errors.append(
                "%s source contains non-regular file: %s"
                % (label, relative.as_posix())
            )
        else:
            files.add(relative.as_posix())
    return files


def _check_inventory(
    root: Path, manifest: Mapping[str, Any], errors: List[str]
) -> Dict[str, str]:
    artifact = manifest["artifact"]
    common_paths = list(artifact["common_paths"])
    localized_paths = list(artifact["localized_paths"])
    common_set = set(common_paths)
    localized_set = set(localized_paths)
    overlap = sorted(common_set & localized_set)
    for path in overlap:
        errors.append("duplicate output path is owned by common and locale: %s" % path)

    folded: Dict[str, str] = {}
    for path in common_paths + localized_paths:
        key = path.casefold()
        if key in folded and folded[key] != path:
            errors.append(
                "output paths collide after case-folding: %s and %s"
                % (folded[key], path)
            )
        folded[key] = path
    for path in common_paths + localized_paths:
        for parent in PurePosixPath(path).parents:
            if parent == PurePosixPath("."):
                continue
            owner = folded.get(parent.as_posix().casefold())
            if owner is not None:
                errors.append(
                    "output file path is also used as a parent directory: %s and %s"
                    % (owner, path)
                )

    common_root = artifact["common_root"]
    for tag, entry in manifest["locales"].items():
        if common_root.casefold() == entry["source_root"].casefold():
            errors.append("common and locale %s share source root %s" % (tag, common_root))

    actual_common = _collect_source_files(
        root, root / common_root, "common", errors
    )
    _compare_inventory("common", common_set, actual_common, errors)
    common_texts: Dict[str, str] = {}
    for relative in sorted(actual_common & common_set):
        text = _check_utf8_lf_file(root / common_root / relative, "common", errors)
        if text is not None:
            common_texts[relative] = text

    declared_locale_directories = {
        PurePosixPath(entry["source_root"]).name
        for entry in manifest["locales"].values()
    }
    locales_root = root / "locales"
    if locales_root.is_dir():
        for entry in sorted(locales_root.iterdir()):
            if entry.name in IGNORED_SOURCE_PARTS or not entry.is_dir():
                continue
            if entry.name not in declared_locale_directories:
                errors.append("undeclared locale source directory: locales/%s" % entry.name)
    for tag, entry in manifest["locales"].items():
        actual = _collect_source_files(root, root / entry["source_root"], tag, errors)
        _compare_inventory("locale %s" % tag, localized_set, actual, errors)
    return common_texts


def _compare_inventory(
    label: str, expected: Set[str], actual: Set[str], errors: List[str]
) -> None:
    for path in sorted(expected - actual):
        errors.append("%s is missing source file: %s" % (label, path))
    for path in sorted(actual - expected):
        errors.append("%s has unexpected source file: %s" % (label, path))


def _check_utf8_lf_file(path: Path, label: str, errors: List[str]) -> Optional[str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        errors.append("cannot read %s source %s: %s" % (label, path, exc))
        return None
    if b"\r" in raw:
        errors.append("%s source must use LF line endings: %s" % (label, path))
    if not raw.endswith(b"\n"):
        errors.append("%s source is missing a final newline: %s" % (label, path))
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append("%s source is not UTF-8: %s (%s)" % (label, path, exc))
        return None


def _read_locale_texts(
    root: Path, manifest: Mapping[str, Any], errors: List[str]
) -> Dict[Tuple[str, str], str]:
    texts: Dict[Tuple[str, str], str] = {}
    for tag, entry in manifest["locales"].items():
        source_root = root / entry["source_root"]
        for relative in manifest["artifact"]["localized_paths"]:
            path = source_root / relative
            if _has_symlink_component(root, path) or not path.is_file():
                continue
            text = _check_utf8_lf_file(path, tag, errors)
            if text is not None:
                texts[(tag, relative)] = text
    return texts


def _check_contract_paths(manifest: Mapping[str, Any], errors: List[str]) -> None:
    localized = set(manifest["artifact"]["localized_paths"])
    contracts = manifest["contracts"]
    for group_name in ("section_markers", "required_commands", "skills"):
        for contract in contracts[group_name]:
            for path in contract["paths"]:
                if path not in localized:
                    errors.append(
                        "contracts.%s %s references non-localized path: %s"
                        % (group_name, contract["id"], path)
                    )


def _check_placeholders(
    manifest: Mapping[str, Any], texts: Mapping[Tuple[str, str], str], errors: List[str]
) -> None:
    tags = list(manifest["locales"])
    for relative in manifest["artifact"]["localized_paths"]:
        for tag in tags:
            text = texts.get((tag, relative))
            if text is not None:
                _check_placeholder_syntax(tag, relative, text, errors)
        if len(tags) < 2:
            continue
        reference = tags[0]
        reference_text = texts.get((reference, relative))
        if reference_text is None:
            continue
        expected = Counter(PLACEHOLDER_RE.findall(reference_text))
        for tag in tags[1:]:
            text = texts.get((tag, relative))
            if text is None:
                continue
            actual = Counter(PLACEHOLDER_RE.findall(text))
            if actual != expected:
                errors.append(
                    "placeholder multiset differs for %s: %s != %s"
                    % (relative, reference, tag)
                )


def _check_placeholder_syntax(
    tag: str, relative: str, text: str, errors: List[str]
) -> None:
    tokens = PLACEHOLDER_TOKEN_RE.findall(text)
    invalid = [
        token
        for token in tokens
        if token != "{{...}}" and PLACEHOLDER_RE.fullmatch(token) is None
    ]
    remainder = PLACEHOLDER_TOKEN_RE.sub("", text)
    if invalid or "{{" in remainder or "}}" in remainder:
        errors.append("%s:%s contains malformed placeholder syntax" % (tag, relative))


def _strip_blockquote_markers(
    line: str, limit: Optional[int] = None
) -> Tuple[int, str]:
    """Strip leading blockquote containers, optionally to a stored fence depth."""

    depth = 0
    cursor = 0
    while limit is None or depth < limit:
        marker = BLOCKQUOTE_MARKER_RE.match(line, cursor)
        if marker is None:
            break
        cursor = marker.end()
        depth += 1
    return depth, line[cursor:]


def _markdown_line_context(text: str) -> Tuple[Tuple[bool, bool], ...]:
    """Return ``(outside_fence, outside_html_comment)`` for each line."""

    context = []
    fence_character: Optional[str] = None
    fence_length = 0
    fence_blockquote_depth = 0
    in_html_comment = False
    for line in text.splitlines():
        blockquote_depth, fence_candidate = _strip_blockquote_markers(line)
        if fence_character is not None:
            if blockquote_depth < fence_blockquote_depth:
                fence_character = None
                fence_length = 0
                fence_blockquote_depth = 0
            else:
                _, closing_candidate = _strip_blockquote_markers(
                    line, fence_blockquote_depth
                )
                context.append((False, False))
                stripped = closing_candidate.lstrip(" ")
                if (
                    len(closing_candidate) - len(stripped) <= 3
                    and re.fullmatch(
                        re.escape(fence_character) + "{%d,}[ \t]*" % fence_length,
                        stripped,
                    )
                ):
                    fence_character = None
                    fence_length = 0
                    fence_blockquote_depth = 0
                continue

        fence = FENCE_LINE_RE.fullmatch(fence_candidate)
        if fence is not None:
            sequence = fence.group(1)
            fence_character = sequence[0]
            fence_length = len(sequence)
            fence_blockquote_depth = blockquote_depth
            context.append((False, False))
            continue

        context.append((True, not in_html_comment))
        cursor = 0
        while cursor < len(line):
            token = "-->" if in_html_comment else "<!--"
            position = line.find(token, cursor)
            if position < 0:
                break
            in_html_comment = not in_html_comment
            cursor = position + len(token)
    return tuple(context)


def _visible_contract_assertions(text: str) -> List[str]:
    lines = text.splitlines()
    context = _markdown_line_context(text)
    return [
        line
        for line, (outside_fence, outside_comment) in zip(lines, context)
        if outside_fence
        and outside_comment
        and TEMPLATE_CONTRACT_ASSERTION_RE.fullmatch(line) is not None
    ]


def _visible_full_line_matches(text: str, pattern: Any) -> List[str]:
    lines = text.splitlines()
    context = _markdown_line_context(text)
    return [
        line
        for line, line_context in zip(lines, context)
        if all(line_context) and pattern.fullmatch(line) is not None
    ]


def _mask_html_comments(text: str) -> str:
    """Replace HTML comments with whitespace while preserving line structure."""

    parts: List[str] = []
    cursor = 0
    while cursor < len(text):
        start = text.find("<!--", cursor)
        if start < 0:
            parts.append(text[cursor:])
            break
        parts.append(text[cursor:start])
        end = text.find("-->", start + 4)
        comment_end = len(text) if end < 0 else end + 3
        parts.append(
            "".join(
                "\n" if character == "\n" else " "
                for character in text[start:comment_end]
            )
        )
        cursor = comment_end
    return "".join(parts)


def _mask_fenced_code_blocks(text: str) -> str:
    masked_lines: List[str] = []
    for line, (outside_fence, _) in zip(
        text.splitlines(keepends=True), _markdown_line_context(text)
    ):
        if outside_fence:
            masked_lines.append(line)
        else:
            masked_lines.append(
                "".join("\n" if character == "\n" else " " for character in line)
            )
    return "".join(masked_lines)


def _observable_markdown_text(text: str) -> str:
    """Return prose/source text outside HTML comments and fenced examples."""

    return _mask_fenced_code_blocks(_mask_html_comments(text))


def _mask_inline_code_spans(text: str) -> str:
    """Mask same-line Markdown code spans outside fenced code blocks."""

    masked_lines: List[str] = []
    for line, (outside_fence, _) in zip(
        text.splitlines(keepends=True), _markdown_line_context(text)
    ):
        if not outside_fence:
            masked_lines.append(line)
            continue
        masked = list(line)
        cursor = 0
        while cursor < len(line):
            start = line.find("`", cursor)
            if start < 0:
                break
            escaped = 0
            before = start - 1
            while before >= 0 and line[before] == "\\":
                escaped += 1
                before -= 1
            if escaped % 2:
                cursor = start + 1
                continue
            delimiter_length = 1
            while (
                start + delimiter_length < len(line)
                and line[start + delimiter_length] == "`"
            ):
                delimiter_length += 1
            search = start + delimiter_length
            closing_end: Optional[int] = None
            while search < len(line):
                closing = line.find("`", search)
                if closing < 0:
                    break
                closing_length = 1
                while (
                    closing + closing_length < len(line)
                    and line[closing + closing_length] == "`"
                ):
                    closing_length += 1
                if closing_length == delimiter_length:
                    closing_end = closing + closing_length
                    break
                search = closing + closing_length
            if closing_end is None:
                cursor = start + delimiter_length
                continue
            for index in range(start, closing_end):
                if masked[index] != "\n":
                    masked[index] = " "
            cursor = closing_end
        masked_lines.append("".join(masked))
    return "".join(masked_lines)


def _structural_markdown_text(text: str) -> str:
    return _mask_inline_code_spans(_observable_markdown_text(text))


def _contains_observable_token(text: str, token: str) -> bool:
    visible = _observable_markdown_text(text)
    if re.fullmatch(r"§\d+(?:\.\d+)*", token):
        return re.search(
            r"(?<![0-9.])%s(?![0-9A-Za-z_-]|\.[0-9A-Za-z_-])"
            % re.escape(token),
            visible,
        ) is not None
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", token):
        return re.search(
            r"(?<![A-Za-z0-9_-])%s(?![A-Za-z0-9_-])" % re.escape(token),
            visible,
        ) is not None
    return token in visible


def _marked_section_line_bounds(
    text: str, marker: str
) -> Tuple[int, int, int, List[str]]:
    lines = text.splitlines()
    context = _markdown_line_context(text)
    indexes = [
        index
        for index, line in enumerate(lines)
        if line == marker and all(context[index])
    ]
    if len(indexes) != 1:
        raise ValueError(
            "marker %s must appear exactly once outside fenced code and "
            "enclosing HTML comments (found %d)" % (marker, len(indexes))
        )

    marker_index = indexes[0]
    heading_index = marker_index - 1
    while heading_index >= 0 and not lines[heading_index].strip():
        heading_index -= 1
    if (
        heading_index < 0
        or not all(context[heading_index])
        or HEADING_RE.match(lines[heading_index]) is None
    ):
        raise ValueError("marker %s must directly follow a Markdown heading" % marker)

    level = len(lines[heading_index]) - len(lines[heading_index].lstrip("#"))
    end_index = len(lines)
    for index in range(marker_index + 1, len(lines)):
        heading = HEADING_RE.match(lines[index])
        if heading is not None and all(context[index]):
            heading_level = len(lines[index]) - len(lines[index].lstrip("#"))
            if heading_level <= level:
                end_index = index
                break
    return heading_index, marker_index, end_index, lines


def _numbered_heading_sequence(text: str) -> Tuple[Tuple[int, str], ...]:
    headings = []
    visible_text = _structural_markdown_text(text)
    for line, (outside_fence, _) in zip(
        visible_text.splitlines(), _markdown_line_context(visible_text)
    ):
        if not outside_fence:
            continue
        match = NUMBERED_HEADING_RE.match(line)
        if match is not None:
            headings.append((len(match.group(1)), match.group(2)))
    return tuple(headings)


def _relative_link_target_sequence(text: str) -> Tuple[str, ...]:
    targets = []
    visible_text = _structural_markdown_text(text)
    for line, (outside_fence, _) in zip(
        visible_text.splitlines(), _markdown_line_context(visible_text)
    ):
        if not outside_fence:
            continue
        for target in LINK_TARGET_RE.findall(line):
            if target.startswith("/") or URI_SCHEME_RE.match(target):
                continue
            targets.append(PurePosixPath(target).as_posix())
    return tuple(targets)


def _check_structural_parity(
    manifest: Mapping[str, Any],
    texts: Mapping[Tuple[str, str], str],
    errors: List[str],
) -> None:
    tags = list(manifest["locales"])
    if len(tags) < 2:
        return
    reference = tags[0]
    for relative in manifest["artifact"]["localized_paths"]:
        reference_text = texts.get((reference, relative))
        if reference_text is None:
            continue
        expected_headings = _numbered_heading_sequence(reference_text)
        expected_links = _relative_link_target_sequence(reference_text)
        for tag in tags[1:]:
            text = texts.get((tag, relative))
            if text is None:
                continue
            headings = _numbered_heading_sequence(text)
            if headings != expected_headings:
                errors.append(
                    "numbered heading sequence differs for %s: %s != %s"
                    % (relative, reference, tag)
                )
            links = _relative_link_target_sequence(text)
            if links != expected_links:
                errors.append(
                    "relative-link target sequence differs for %s: %s != %s"
                    % (relative, reference, tag)
                )


def _check_markers(
    manifest: Mapping[str, Any], texts: Mapping[Tuple[str, str], str], errors: List[str]
) -> None:
    section_expected: DefaultDict[str, List[str]] = defaultdict(list)
    for contract in manifest["contracts"]["section_markers"]:
        for relative in contract["paths"]:
            section_expected[relative].append(contract["marker"])

    skill_expected: DefaultDict[str, List[str]] = defaultdict(list)
    for contract in manifest["contracts"]["skills"]:
        for relative in contract["paths"]:
            skill_expected[relative].append(contract["marker"])
            skill_expected[relative].extend(
                "<!-- template-skill-fixture:%s -->" % fixture
                for fixture in contract["fixture_ids"]
            )

    registered_markers = {
        contract["marker"]
        for group in ("section_markers", "skills")
        for contract in manifest["contracts"][group]
    }
    registered_markers.update(
        "<!-- template-skill-fixture:%s -->" % fixture
        for contract in manifest["contracts"]["skills"]
        for fixture in contract["fixture_ids"]
    )
    registered_assertions = {
        rule["assertion"] for rule in SKILL_FIXTURE_REGISTRY.values()
    }

    for tag in manifest["locales"]:
        for relative in manifest["artifact"]["localized_paths"]:
            text = texts.get((tag, relative))
            if text is None:
                continue
            actual_sections = _visible_full_line_matches(text, SECTION_MARKER_RE)
            expected_sections = section_expected.get(relative, [])
            if actual_sections != expected_sections:
                errors.append(
                    "%s:%s section marker sequence differs: expected %r, got %r"
                    % (tag, relative, expected_sections, actual_sections)
                )
            actual_skills = _visible_full_line_matches(
                text, SKILL_TEMPLATE_MARKER_RE
            )
            expected_skills = skill_expected.get(relative, [])
            if actual_skills != expected_skills:
                errors.append(
                    "%s:%s skill marker sequence differs: expected %r, got %r"
                    % (tag, relative, expected_skills, actual_skills)
                )
            for marker in _visible_full_line_matches(text, TEMPLATE_MARKER_RE):
                if marker not in registered_markers:
                    errors.append("%s:%s has unknown template marker %s" % (tag, relative, marker))
            for assertion in _visible_contract_assertions(text):
                if assertion not in registered_assertions:
                    errors.append(
                        "%s:%s has unregistered template contract assertion %s"
                        % (tag, relative, assertion)
                    )
            for marker in expected_sections:
                if not marker.startswith("<!-- template-section:"):
                    continue
                try:
                    _marked_section_line_bounds(text, marker)
                except ValueError as error:
                    errors.append("%s:%s %s" % (tag, relative, error))


def _command_occurrences(text: str, command: str) -> int:
    inline = sum(1 for value in INLINE_CODE_RE.findall(text) if value == command)
    standalone = sum(1 for line in text.splitlines() if line.strip() == command)
    return inline + standalone


def _python_commands(text: str) -> Counter[str]:
    values = list(INLINE_CODE_RE.findall(text))
    values.extend(line.strip() for line in text.splitlines())
    return Counter(
        value for value in values if value.startswith(("python ", "python3 "))
    )


def _check_commands(
    manifest: Mapping[str, Any], texts: Mapping[Tuple[str, str], str], errors: List[str]
) -> None:
    declared: DefaultDict[str, Counter[str]] = defaultdict(Counter)
    for contract in manifest["contracts"]["required_commands"]:
        for relative in contract["paths"]:
            if contract["value"].startswith(("python ", "python3 ")):
                declared[relative][contract["value"]] += 1
        for tag in manifest["locales"]:
            for relative in contract["paths"]:
                text = texts.get((tag, relative))
                if text is None:
                    continue
                count = _command_occurrences(
                    _mask_html_comments(text), contract["value"]
                )
                if count != 1:
                    errors.append(
                        "%s:%s must contain command %s exactly once (found %d)"
                        % (tag, relative, contract["id"], count)
                    )
    for tag in manifest["locales"]:
        for relative in manifest["artifact"]["localized_paths"]:
            text = texts.get((tag, relative))
            if text is None:
                continue
            actual = _python_commands(_mask_html_comments(text))
            expected = declared.get(relative, Counter())
            if actual != expected:
                errors.append(
                    "%s:%s Python command inventory differs from manifest: "
                    "expected %r, got %r" % (tag, relative, expected, actual)
                )


def _frontmatter_fields(text: str) -> Optional[Dict[str, List[str]]]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    fields: DefaultDict[str, List[str]] = defaultdict(list)
    for line in lines[1:end]:
        match = TOP_LEVEL_FRONTMATTER_FIELD_RE.fullmatch(line)
        if match is not None:
            fields[match.group(1)].append(match.group(2))
    return dict(fields)


def _plain_frontmatter_name(value: str) -> Optional[str]:
    match = re.fullmatch(
        r"[ \t]*([a-z][a-z0-9-]*)(?:[ \t]+#.*)?[ \t]*", value
    )
    return match.group(1) if match is not None else None


def _unquoted_frontmatter_boolean(value: str) -> Optional[bool]:
    match = re.fullmatch(r"[ \t]*(true|false)(?:[ \t]+#.*)?[ \t]*", value)
    if match is None:
        return None
    return match.group(1) == "true"


def _read_implicit_invocation_policy(text: str) -> Optional[bool]:
    lines = text.splitlines()
    policy_indexes = [
        index
        for index, line in enumerate(lines)
        if re.fullmatch(r"policy:\s*(?:#.*)?", line)
    ]
    if len(policy_indexes) != 1:
        return None

    entries = []
    for line in lines[policy_indexes[0] + 1 :]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0 or line.startswith("\t"):
            break
        entries.append((indent, line.strip()))
    if not entries:
        return None

    child_indent = min(indent for indent, _ in entries)
    values = []
    for indent, entry in entries:
        if indent != child_indent:
            continue
        match = re.fullmatch(
            r"allow_implicit_invocation:\s*(true|false)\s*(?:#.*)?", entry
        )
        if match is not None:
            values.append(match.group(1) == "true")
    return values[0] if len(values) == 1 else None


def _check_skills(
    manifest: Mapping[str, Any],
    texts: Mapping[Tuple[str, str], str],
    errors: List[str],
) -> None:
    for contract in manifest["contracts"]["skills"]:
        paths = contract["paths"]
        if len(paths) != 2:
            continue
        suffixes = []
        for prefix, path in ((".agents/", paths[0]), (".claude/", paths[1])):
            if not path.startswith(prefix):
                errors.append(
                    "skill %s paths must be ordered as .agents then .claude" % contract["id"]
                )
                break
            suffixes.append(path[len(prefix) :])
        else:
            if suffixes[0] != suffixes[1]:
                errors.append("skill %s pair paths do not match" % contract["id"])
        for tag in manifest["locales"]:
            left_text = texts.get((tag, paths[0]))
            right_text = texts.get((tag, paths[1]))
            if left_text is not None and right_text is not None and left_text != right_text:
                errors.append(
                    "%s skill pair differs for %s: %s != %s"
                    % (tag, contract["id"], paths[0], paths[1])
                )
            for relative in paths:
                text = texts.get((tag, relative))
                if text is None:
                    continue
                visible_marker_count = sum(
                    1
                    for line, line_context in zip(
                        text.splitlines(), _markdown_line_context(text)
                    )
                    if line == contract["marker"] and all(line_context)
                )
                if visible_marker_count != 1:
                    errors.append(
                        "%s:%s must contain skill marker %s exactly once"
                        % (tag, relative, contract["id"])
                    )
                fields = _frontmatter_fields(text)
                if fields is None:
                    errors.append("%s:%s has invalid YAML front matter" % (tag, relative))
                    continue
                names = fields.get("name", [])
                if (
                    len(names) != 1
                    or _plain_frontmatter_name(names[0]) != contract["id"]
                ):
                    errors.append(
                        "%s:%s front matter name must equal skill id %s exactly once"
                        % (tag, relative, contract["id"])
                    )
                if contract["id"] == "review-round":
                    invocation_values = fields.get("disable-model-invocation", [])
                    if (
                        len(invocation_values) != 1
                        or _unquoted_frontmatter_boolean(invocation_values[0]) is not True
                    ):
                        errors.append(
                            "%s:%s must define one unquoted "
                            "disable-model-invocation: true boolean"
                            % (tag, relative)
                        )


def _check_skill_fixture_observables(
    manifest: Mapping[str, Any],
    texts: Mapping[Tuple[str, str], str],
    common_texts: Mapping[str, str],
    errors: List[str],
) -> None:
    contracts = {
        contract["id"]: contract for contract in manifest["contracts"]["skills"]
    }
    for fixture_id, rule in SKILL_FIXTURE_REGISTRY.items():
        contract = contracts.get(rule["skill_id"])
        if contract is None or fixture_id not in contract["fixture_ids"]:
            continue
        skill_path = contract["paths"][0]
        for tag in manifest["locales"]:
            skill_text = texts.get((tag, skill_path))
            if skill_text is None:
                continue
            missing_skill_tokens = [
                token
                for token in rule.get("skill_tokens", ())
                if not _contains_observable_token(skill_text, token)
            ]
            if missing_skill_tokens:
                errors.append(
                    "%s fixture %s is missing skill token(s): %s"
                    % (tag, fixture_id, ", ".join(missing_skill_tokens))
                )
            links = set(_relative_link_target_sequence(skill_text))
            missing_links = [
                target
                for target in rule.get("skill_links", ())
                if target not in links
            ]
            if missing_links:
                errors.append(
                    "%s fixture %s is missing canonical skill link(s): %s"
                    % (tag, fixture_id, ", ".join(missing_links))
                )

            document_path = rule.get("document")
            if document_path is not None:
                document = texts.get((tag, document_path))
                if document is None:
                    errors.append(
                        "%s fixture %s cannot read canonical document %s"
                        % (tag, fixture_id, document_path)
                    )
                else:
                    missing_document_tokens = [
                        token
                        for token in rule.get("document_tokens", ())
                        if not _contains_observable_token(document, token)
                    ]
                    if missing_document_tokens:
                        errors.append(
                            "%s fixture %s canonical document is missing token(s): %s"
                            % (
                                tag,
                                fixture_id,
                                ", ".join(missing_document_tokens),
                            )
                        )

            common_path = rule.get("common_document")
            if common_path is not None:
                common = common_texts.get(common_path)
                if common is None:
                    errors.append(
                        "%s fixture %s cannot read common document %s"
                        % (tag, fixture_id, common_path)
                    )
                else:
                    missing_common_tokens = [
                        token
                        for token in rule.get("common_tokens", ())
                        if token not in common
                    ]
                    if missing_common_tokens:
                        errors.append(
                            "%s fixture %s common document is missing token(s): %s"
                            % (tag, fixture_id, ", ".join(missing_common_tokens))
                        )
                    expected_policy = rule.get("common_implicit_invocation")
                    if (
                        expected_policy is not None
                        and _read_implicit_invocation_policy(common)
                        is not expected_policy
                    ):
                        errors.append(
                            "%s fixture %s common config must define "
                            "policy.allow_implicit_invocation as one unquoted "
                            "false boolean"
                            % (tag, fixture_id)
                        )

    for contract in manifest["contracts"]["skills"]:
        expected = [
            (
                "<!-- template-skill-fixture:%s -->" % fixture_id,
                SKILL_FIXTURE_REGISTRY[fixture_id]["assertion"],
            )
            for fixture_id in contract["fixture_ids"]
        ]
        skill_path = contract["paths"][0]
        for tag in manifest["locales"]:
            skill_text = texts.get((tag, skill_path))
            if skill_text is None:
                continue
            lines = skill_text.splitlines()
            context = _markdown_line_context(skill_text)
            actual_assertions = _visible_contract_assertions(skill_text)
            expected_assertions = [assertion for _, assertion in expected]
            if actual_assertions != expected_assertions:
                errors.append(
                    "%s fixture stable assertion sequence differs for %s"
                    % (tag, contract["id"])
                )
            for marker, assertion in expected:
                indexes = [
                    index
                    for index, line in enumerate(lines)
                    if line == marker and all(context[index])
                ]
                if len(indexes) != 1:
                    errors.append(
                        "%s fixture marker %s must appear exactly once outside "
                        "fenced code and enclosing HTML comments"
                        % (tag, marker)
                    )
                    continue
                following = indexes[0] + 1
                while following < len(lines) and not lines[following].strip():
                    following += 1
                if (
                    following >= len(lines)
                    or lines[following] != assertion
                    or not all(context[following])
                ):
                    errors.append(
                        "%s fixture marker %s must be followed by its exact assertion"
                        % (tag, marker)
                    )


def _section_bounds(text: str, marker: str) -> Optional[Tuple[int, int]]:
    try:
        _, marker_index, end_index, _ = _marked_section_line_bounds(text, marker)
    except ValueError:
        return None
    return marker_index, end_index


def _top_level_bullets(
    text: str, marker_index: int, end_index: int
) -> List[Tuple[int, str]]:
    lines = text.splitlines()
    context = _markdown_line_context(text)
    bullets: List[Tuple[int, str]] = []
    current: Optional[List[str]] = None
    current_index: Optional[int] = None
    bullet_indent: Optional[int] = None
    for index in range(marker_index + 1, end_index):
        if not all(context[index]):
            continue
        line = lines[index]
        stripped = line.strip()
        bullet_match = re.match(r"^( {0,3})-\s+", line)
        if bullet_match is not None and bullet_indent is None:
            bullet_indent = len(bullet_match.group(1))
        if (
            bullet_match is not None
            and len(bullet_match.group(1)) <= bullet_indent
        ):
            if current is not None and current_index is not None:
                bullets.append((current_index, "\n".join(current)))
            current = [stripped]
            current_index = index
            bullet_indent = len(bullet_match.group(1))
            continue
        indent = len(line) - len(line.lstrip(" "))
        if current is not None and stripped and indent > (bullet_indent or 0):
            current.append(stripped)
    if current is not None and current_index is not None:
        bullets.append((current_index, "\n".join(current)))
    return bullets


def _check_invariant_contract(
    manifest: Mapping[str, Any], texts: Mapping[Tuple[str, str], str], errors: List[str]
) -> None:
    section_contract = next(
        (
            item
            for item in manifest["contracts"]["section_markers"]
            if item["id"] == "project-invariants"
        ),
        None,
    )
    example_contract = next(
        (
            item
            for item in manifest["contracts"]["section_markers"]
            if item["id"] == "project-invariant-example"
        ),
        None,
    )
    if section_contract is None:
        errors.append("project-invariants section contract is missing")
        return
    if example_contract is None:
        errors.append("project-invariant-example marker contract is missing")
        return
    review_path = next(
        (path for path in section_contract["paths"] if path == "docs/REVIEW.md"), None
    )
    bugbot_path = next(
        (path for path in section_contract["paths"] if path == ".cursor/BUGBOT.md"), None
    )
    if review_path is None or bugbot_path is None:
        errors.append("project-invariants must cover docs/REVIEW.md and .cursor/BUGBOT.md")
        return
    if review_path not in example_contract["paths"]:
        errors.append("project-invariant-example must target docs/REVIEW.md")
        return

    section_marker = section_contract["marker"]
    example_marker = example_contract["marker"]
    for tag in manifest["locales"]:
        review = texts.get((tag, review_path))
        bugbot = texts.get((tag, bugbot_path))
        if review is None or bugbot is None:
            continue
        review_bounds = _section_bounds(review, section_marker)
        bugbot_bounds = _section_bounds(bugbot, section_marker)
        if review_bounds is None or bugbot_bounds is None:
            continue
        review_lines = review.splitlines()
        review_context = _markdown_line_context(review)
        example_indexes = [
            index
            for index in range(review_bounds[0] + 1, review_bounds[1])
            if review_lines[index] == example_marker and all(review_context[index])
        ]
        if len(example_indexes) != 1:
            errors.append("%s review invariant example marker is outside its section" % tag)
            continue
        example_position = example_indexes[0]
        review_bullets = _top_level_bullets(review, *review_bounds)
        bugbot_bullets = _top_level_bullets(bugbot, *bugbot_bounds)
        examples = [item for item in review_bullets if item[0] > example_position]
        if not examples:
            errors.append("%s review invariant example marker has no following bullet" % tag)
            continue
        example = examples[0]
        next_content = example_position + 1
        while next_content < review_bounds[1] and not review_lines[next_content].strip():
            next_content += 1
        if example[0] != next_content:
            errors.append(
                "%s review invariant example marker must immediately precede its bullet"
                % tag
            )
            continue
        if not example[1].startswith(PROJECT_INVARIANT_EXAMPLE_PREFIXES):
            errors.append(
                "%s review invariant example marker must immediately precede "
                "an English or Korean template example bullet" % tag
            )
            continue
        if not review_bullets or review_bullets[0][0] != example[0]:
            errors.append("%s review invariant example must be the first bullet" % tag)
        invariants = [body for position, body in review_bullets if position != example[0]]
        copies = [body for _, body in bugbot_bullets]
        if not 2 <= len(invariants) <= 10:
            errors.append("%s must define 2 to 10 project invariants" % tag)
        if invariants != copies:
            errors.append("%s REVIEW/BUGBOT project invariants differ" % tag)


def check_locales(root: Path = ROOT, require_stable: bool = False) -> List[str]:
    """Return every locale contract error for *root*."""

    root = Path(root)
    errors: List[str] = []
    manifest = _read_manifest(root / MANIFEST_PATH, errors, root)
    if manifest is None:
        return errors
    if not _validate_manifest_schema(manifest, errors):
        return errors

    _check_locale_metadata(manifest, errors)
    _check_contract_paths(manifest, errors)
    common_texts = _check_inventory(root, manifest, errors)
    texts = _read_locale_texts(root, manifest, errors)
    _check_placeholders(manifest, texts, errors)
    _check_structural_parity(manifest, texts, errors)
    _check_markers(manifest, texts, errors)
    _check_commands(manifest, texts, errors)
    _check_skills(manifest, texts, errors)
    _check_skill_fixture_observables(manifest, texts, common_texts, errors)
    _check_invariant_contract(manifest, texts, errors)
    if require_stable:
        errors.extend(stable_release_errors(manifest))
    return errors


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root (default: checker parent directory)",
    )
    parser.add_argument(
        "--require-stable",
        action="store_true",
        help="also require every required_stable_locales entry to be complete",
    )
    args = parser.parse_args(argv)
    errors = check_locales(args.root.resolve(), require_stable=args.require_stable)
    if errors:
        print("Locale source check failed:", file=sys.stderr)
        for error in errors:
            print("- %s" % error, file=sys.stderr)
        return 1
    print("Locale source check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
