#!/usr/bin/env python3
"""Dependency-free checks for a materialized documentation template.

Checks relative links, skill copies and the Codex explicit-invocation policy,
known @imports, invariant lists in REVIEW and BUGBOT, section-number references
that identify a document, and the Template version in the guide documents. Any
failure produces exit code 1. Pass ``--root`` to check an arbitrary materialized
artifact; otherwise the artifact root is inferred from this script's location.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple


DEFAULT_ROOT = Path(__file__).resolve().parent.parent
ROOT = DEFAULT_ROOT
EXCLUDED_TOP_LEVEL_NAMES = frozenset()

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    # Generated and vendored directories. Avoid false positives in adopted repos.
    "dist",
    "build",
    "target",
    "vendor",
    ".next",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "site-packages",
}

LINK_RE = re.compile(r"\]\(((?!https?://)(?!mailto:)[^)\s#]+?)(?:#[^)]*)?\)")
VERSION_RE = re.compile(
    r"^\s*-\s*\*\*Template version:\*\*\s*(\S+)", re.MULTILINE
)
IMPORT_LINE_RE = re.compile(r"^@([^\s]+)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
HEADING_NUM_RE = re.compile(r"^#{1,6}\s+(\d+(?:\.\d+)*)[.\s]")
FENCE_LINE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")
BLOCKQUOTE_MARKER_RE = re.compile(r"[ ]{0,3}>[ \t]?")
SECTION_GROUP = r"§\d+(?:\.\d+)*(?:·§\d+(?:\.\d+))*"
SECTION_LINK_RE = re.compile(
    r"\]\(((?!https?://)[^)\s#]+?\.md)\)\s*(" + SECTION_GROUP + ")"
)
SECTION_PATH_RE = re.compile(r"`([^`\s]+\.md)`\s*(" + SECTION_GROUP + ")")
SECTION_NAME_RE = re.compile(r"\b([A-Z][A-Z_]*)(?:\.md)?\s+(" + SECTION_GROUP + ")")
SECTION_SPLIT_RE = re.compile(r"[§·]+")

PROJECT_INVARIANTS_MARKER = "<!-- template-section:project-invariants -->"
RELEASE_HISTORY_MARKER = "<!-- template-section:release-history -->"
PROJECT_INVARIANT_EXAMPLE_MARKER = (
    "<!-- template-example:project-invariant -->"
)
PROJECT_INVARIANT_EXAMPLE_PREFIXES = ("- **Example:**", "- **예시:**")

HISTORY_PATH = "docs/TEMPLATE_GUIDE.md"

SKILL_PAIRS: List[Tuple[str, str]] = [
    (
        ".agents/skills/design/SKILL.md",
        ".claude/skills/design/SKILL.md",
    ),
    (
        ".agents/skills/review-round/SKILL.md",
        ".claude/skills/review-round/SKILL.md",
    ),
]

# Codex configuration that blocks implicit invocation and its paired skill source.
SKILL_CONFIGS: List[Tuple[str, str]] = [
    (
        ".agents/skills/review-round/SKILL.md",
        ".agents/skills/review-round/agents/openai.yaml",
    ),
]

INVARIANT_SOURCE = "docs/REVIEW.md"
INVARIANT_COPY = ".cursor/BUGBOT.md"


def is_skipped(path: Path) -> bool:
    try:
        parts = path.relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
        return any(part in SKIP_DIR_NAMES for part in parts)
    return (
        bool(parts) and parts[0] in EXCLUDED_TOP_LEVEL_NAMES
    ) or any(part in SKIP_DIR_NAMES for part in parts)


def md_files(errors: Optional[List[str]] = None) -> List[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        if is_skipped(path):
            continue
        if not is_inside_root(path):
            message = "Markdown source escapes artifact root: %s" % rel(path)
            if errors is not None and message not in errors:
                errors.append(message)
            continue
        files.append(path)
    return sorted(files)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def is_inside_root(path: Path) -> bool:
    """Return whether *path* resolves inside the checked artifact root."""

    try:
        path.resolve().relative_to(ROOT.resolve())
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def is_file_inside_root(path: Path) -> bool:
    return is_inside_root(path) and path.is_file()


def check_relative_links(errors: List[str], notes: List[str]) -> None:
    broken = []
    scanned = 0
    links = 0
    for md in md_files(errors):
        scanned += 1
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            links += 1
            dest = md.parent / target
            if not is_inside_root(dest):
                broken.append("%s: %s (target escapes artifact root)" % (rel(md), target))
            elif not dest.exists():
                broken.append("%s: %s" % (rel(md), target))
    if broken:
        errors.append("Broken relative links:")
        errors.extend("  %s" % item for item in broken)
    else:
        notes.append(
            "Relative links: checked %d links in %d files; none broken"
            % (links, scanned)
        )


def check_skill_copies(errors: List[str], notes: List[str]) -> None:
    for left, right in SKILL_PAIRS:
        a = ROOT / left
        b = ROOT / right
        if not is_file_inside_root(a) and not is_file_inside_root(b):
            errors.append("Skill files are missing: %s, %s" % (left, right))
            continue
        if not is_file_inside_root(a):
            errors.append("Skill source is missing: %s" % left)
            continue
        if not is_file_inside_root(b):
            notes.append("Skill copy omitted (allowed): %s" % right)
            continue
        if a.read_bytes() != b.read_bytes():
            errors.append("Skill copies differ: %s ↔ %s" % (left, right))
        else:
            notes.append("Skill copies match: %s" % left)


def read_implicit_invocation_policy(path: Path) -> Optional[bool]:
    """Read the policy.allow_implicit_invocation boolean from Codex config.

    This narrowly validates the mapping form generated by the template rather
    than parsing all YAML. Quoted strings and duplicate keys are not accepted
    as the policy boolean.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
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
            r"allow_implicit_invocation:\s*(true|false)\s*(?:#.*)?",
            entry,
            re.IGNORECASE,
        )
        if match:
            values.append(match.group(1).lower() == "true")
    return values[0] if len(values) == 1 else None


def check_skill_configs(errors: List[str], notes: List[str]) -> None:
    for skill, config in SKILL_CONFIGS:
        if not is_file_inside_root(ROOT / skill):
            continue
        config_path = ROOT / config
        if not is_file_inside_root(config_path):
            errors.append(
                "Codex explicit-invocation config is missing: %s "
                "(implicit invocation is enabled for %s)"
                % (config, skill)
            )
            continue
        policy = read_implicit_invocation_policy(config_path)
        if policy is None:
            errors.append(
                "Codex explicit-invocation policy is not a valid boolean: %s "
                "(policy.allow_implicit_invocation: false is required)" % config
            )
        elif policy:
            errors.append(
                "Codex implicit invocation is enabled: %s "
                "(policy.allow_implicit_invocation: false is required)" % config
            )
        else:
            notes.append("Codex explicit-invocation policy verified: %s" % config)


def check_imports(errors: List[str], notes: List[str]) -> None:
    claude = ROOT / "CLAUDE.md"
    if not is_file_inside_root(claude):
        errors.append("CLAUDE.md is missing")
    else:
        body = claude.read_text(encoding="utf-8").strip()
        if body != "@AGENTS.md":
            errors.append("CLAUDE.md import is not @AGENTS.md: %r" % body)
        else:
            notes.append("CLAUDE.md import: @AGENTS.md")

    watchdog = ROOT / ".omp" / "WATCHDOG.md"
    if not is_file_inside_root(watchdog):
        notes.append("WATCHDOG.md omitted (allowed)")
        return

    imports = []
    for line in watchdog.read_text(encoding="utf-8").splitlines():
        match = IMPORT_LINE_RE.match(line)
        if match:
            imports.append(match.group(1))
    if not imports:
        errors.append(".omp/WATCHDOG.md has no @path import")
        return
    for spec in imports:
        dest = watchdog.parent / spec
        if not is_inside_root(dest):
            errors.append(".omp/WATCHDOG.md import escapes artifact root: %s" % spec)
        elif not dest.is_file():
            errors.append(".omp/WATCHDOG.md import target is missing: %s" % spec)
        else:
            notes.append("WATCHDOG.md import: @%s" % spec)


def strip_blockquote_markers(
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


def markdown_line_context(text: str) -> Tuple[Tuple[bool, bool], ...]:
    """Return ``(outside_fence, outside_enclosing_comment)`` per line."""

    context = []
    fence_character: Optional[str] = None
    fence_length = 0
    fence_blockquote_depth = 0
    in_html_comment = False
    for line in text.splitlines():
        blockquote_depth, fence_candidate = strip_blockquote_markers(line)
        if fence_character is not None:
            if blockquote_depth < fence_blockquote_depth:
                fence_character = None
                fence_length = 0
                fence_blockquote_depth = 0
            else:
                _, closing_candidate = strip_blockquote_markers(
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


def marked_section_bounds(
    text: str, marker: str
) -> Tuple[int, int, int, List[str]]:
    """Return heading, marker, and end line indexes for one marked section.

    A stable marker must occur exactly once and directly follow its Markdown
    heading, with only blank lines between them. This keeps translated heading
    text out of the checker contract while making misplaced markers fail closed.
    """
    lines = text.splitlines()
    context = markdown_line_context(text)
    indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip() == marker and all(context[index])
    ]
    if len(indexes) != 1:
        raise ValueError(
            "marker %s must appear exactly once (found %d)" % (marker, len(indexes))
        )

    marker_index = indexes[0]
    heading_index = marker_index - 1
    while heading_index >= 0 and not lines[heading_index].strip():
        heading_index -= 1
    if heading_index < 0:
        raise ValueError("marker %s must follow a Markdown heading" % marker)
    heading = HEADING_RE.match(lines[heading_index])
    if heading is None or not all(context[heading_index]):
        raise ValueError(
            "marker %s must directly follow a Markdown heading" % marker
        )

    level = len(heading.group(1))
    end_index = len(lines)
    for index in range(marker_index + 1, len(lines)):
        following_heading = HEADING_RE.match(lines[index])
        if (
            following_heading
            and all(context[index])
            and len(following_heading.group(1)) <= level
        ):
            end_index = index
            break
    return heading_index, marker_index, end_index, lines


def section_bullets(
    text: str,
    marker: str,
    example_marker: Optional[str] = None,
) -> List[str]:
    """Return complete top-level bullets from a section selected by a marker.

    When ``example_marker`` occurs once inside the section, only a recognized
    English or Korean template-example bullet immediately following it is
    omitted. If an adopter deletes or rewrites the example, the marker must be
    deleted too so a real invariant can never be silently excluded.
    """
    _, marker_index, end_index, lines = marked_section_bounds(text, marker)

    example_index: Optional[int] = None
    if example_marker is not None:
        context = markdown_line_context(text)
        indexes = [
            index
            for index, line in enumerate(lines)
            if line.strip() == example_marker and all(context[index])
        ]
        if len(indexes) > 1:
            raise ValueError(
                "marker %s must appear at most once (found %d)"
                % (example_marker, len(indexes))
            )
        if indexes:
            example_index = indexes[0]
            if not marker_index < example_index < end_index:
                raise ValueError(
                    "marker %s must follow %s inside the same section"
                    % (example_marker, marker)
                )

    context = markdown_line_context(text)
    entries: List[Tuple[int, str]] = []
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
                entries.append((current_index, "\n".join(current)))
            current = [stripped]
            current_index = index
            bullet_indent = len(bullet_match.group(1))
            continue
        indent = len(line) - len(line.lstrip(" "))
        if current is not None and stripped and indent > (bullet_indent or 0):
            current.append(stripped)
    if current is not None and current_index is not None:
        entries.append((current_index, "\n".join(current)))

    if example_index is not None:
        next_content = example_index + 1
        while next_content < end_index and not lines[next_content].strip():
            next_content += 1
        entries_by_index = {index: body for index, body in entries}
        example_body = entries_by_index.get(next_content)
        if example_body is None:
            raise ValueError(
                "marker %s must immediately precede a top-level bullet"
                % example_marker
            )
        if not example_body.startswith(PROJECT_INVARIANT_EXAMPLE_PREFIXES):
            raise ValueError(
                "marker %s must immediately precede an English or Korean "
                "template example bullet" % example_marker
            )
        entries = [entry for entry in entries if entry[0] != next_content]

    return [body for _, body in entries]


def numbered_headings(path: Path) -> set:
    numbers = set()
    text = path.read_text(encoding="utf-8")
    for line, context in zip(text.splitlines(), markdown_line_context(text)):
        if not all(context):
            continue
        match = HEADING_NUM_RE.match(line)
        if match:
            numbers.add(match.group(1))
    return numbers


def doc_short_names(errors: Optional[List[str]] = None) -> dict:
    """Collect short docs/ names for references such as `PROJECT §8`."""
    names = {}
    for path in sorted((ROOT / "docs").glob("*.md")):
        if not is_inside_root(path):
            message = "Markdown source escapes artifact root: %s" % rel(path)
            if errors is not None and message not in errors:
                errors.append(message)
            continue
        if not path.is_file():
            continue
        names[re.sub(r"^\d+-", "", path.stem)] = path
    return names


def history_cut(errors: List[str]) -> Optional[Tuple[Path, int]]:
    """Return where marked release history starts; refs after it are skipped."""
    path = ROOT / HISTORY_PATH
    if not is_file_inside_root(path):
        return None
    text = path.read_text(encoding="utf-8")
    try:
        heading_index, _, _, _ = marked_section_bounds(text, RELEASE_HISTORY_MARKER)
    except ValueError as error:
        errors.append("%s: %s" % (HISTORY_PATH, error))
        return None
    lines = text.splitlines(keepends=True)
    return path, sum(len(line) for line in lines[:heading_index])


def check_section_refs(errors: List[str], notes: List[str]) -> None:
    """Validate section refs that name a document, such as `REVIEW.md §6`.

    Same-file references such as `§4` do not identify their target document and
    are therefore not checked.
    """
    names = doc_short_names(errors)
    cut_at = history_cut(errors)
    headings: dict = {}
    broken: List[str] = []
    checked = 0

    for md in md_files(errors):
        text = md.read_text(encoding="utf-8")
        limit = len(text)
        if cut_at and md == cut_at[0]:
            limit = cut_at[1]
        for regex, kind in (
            (SECTION_LINK_RE, "path"),
            (SECTION_PATH_RE, "path"),
            (SECTION_NAME_RE, "name"),
        ):
            for match in regex.finditer(text):
                if match.start() >= limit:
                    continue
                ref, group = match.group(1), match.group(2)
                if kind == "name":
                    target = names.get(ref)
                else:
                    target = next(
                        (
                            candidate
                            for candidate in (md.parent / ref, ROOT / ref)
                            if is_inside_root(candidate) and candidate.is_file()
                        ),
                        None,
                    )
                if target is None:
                    if kind == "path":
                        broken.append(
                            "%s: %s %s (document target does not exist)"
                            % (rel(md), ref, group)
                        )
                    continue
                target = target.resolve()
                if target not in headings:
                    headings[target] = numbered_headings(target)
                for number in filter(None, SECTION_SPLIT_RE.split(group)):
                    checked += 1
                    if number not in headings[target]:
                        broken.append(
                            "%s: %s §%s (section does not exist in %s)"
                            % (rel(md), ref, number, rel(target))
                        )

    if broken:
        errors.append("Section-number references do not match actual headings:")
        errors.extend("  %s" % item for item in sorted(set(broken)))
    else:
        notes.append("Section-number references: checked %d; no mismatches" % checked)


def check_invariants(errors: List[str], notes: List[str]) -> None:
    copy_file = ROOT / INVARIANT_COPY
    if not is_file_inside_root(copy_file):
        notes.append("BUGBOT.md omitted (allowed)")
        return

    source_file = ROOT / INVARIANT_SOURCE
    if not is_file_inside_root(source_file):
        errors.append(
            "Cannot compare invariants because %s is missing" % INVARIANT_SOURCE
        )
        return

    try:
        source = section_bullets(
            source_file.read_text(encoding="utf-8"),
            PROJECT_INVARIANTS_MARKER,
            PROJECT_INVARIANT_EXAMPLE_MARKER,
        )
    except ValueError as error:
        errors.append("%s: %s" % (INVARIANT_SOURCE, error))
        source = None
    try:
        copy = section_bullets(
            copy_file.read_text(encoding="utf-8"), PROJECT_INVARIANTS_MARKER
        )
    except ValueError as error:
        errors.append("%s: %s" % (INVARIANT_COPY, error))
        copy = None
    if source is None or copy is None:
        return

    if source == copy:
        notes.append("Invariant lists match: %d items" % len(source))
        return

    errors.append("Invariant lists differ: %s ↔ %s" % (INVARIANT_SOURCE, INVARIANT_COPY))
    for item in source:
        if item not in copy:
            errors.append("  Only in %s: %s" % (INVARIANT_SOURCE, item))
    for item in copy:
        if item not in source:
            errors.append("  Only in %s: %s" % (INVARIANT_COPY, item))


def read_template_version(path: Path) -> Optional[str]:
    if not is_file_inside_root(path):
        return None
    match = VERSION_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def check_versions(errors: List[str], notes: List[str]) -> None:
    guide = ROOT / "docs" / "TEMPLATE_GUIDE.md"
    docs_guide = ROOT / "docs" / "DOCS_GUIDE.md"
    v2 = read_template_version(docs_guide)
    if v2 is None:
        errors.append("Template version not found in docs/DOCS_GUIDE.md")

    # TEMPLATE_GUIDE.md may be deleted after adoption.
    if not is_file_inside_root(guide):
        notes.append(
            "TEMPLATE_GUIDE.md omitted (allowed): checking version only in "
            "DOCS_GUIDE.md"
        )
        if v2:
            notes.append("Template version: %s" % v2)
        return

    v1 = read_template_version(guide)
    if v1 is None:
        errors.append("Template version not found in docs/TEMPLATE_GUIDE.md")
    if v1 and v2 and v1 != v2:
        errors.append(
            "Template versions differ: TEMPLATE_GUIDE=%s, DOCS_GUIDE=%s"
            % (v1, v2)
        )
    elif v1 and v2:
        notes.append("Template versions match: %s" % v1)
        history = guide.read_text(encoding="utf-8")
        try:
            _, marker_index, end_index, lines = marked_section_bounds(
                history, RELEASE_HISTORY_MARKER
            )
        except ValueError as error:
            errors.append("%s: %s" % (HISTORY_PATH, error))
            return
        release_history = "\n".join(lines[marker_index + 1 : end_index])
        version_heading = re.compile(
            r"^###\s+v?%s(?:\s|$)" % re.escape(v1), re.MULTILINE
        )
        if version_heading.search(release_history) is None:
            errors.append(
                "Current version is absent from TEMPLATE_GUIDE.md history: %s" % v1
            )
        else:
            notes.append("Current version is present in revision history: %s" % v1)


def _run_checks() -> int:
    if not (ROOT / "AGENTS.md").is_file():
        sys.stderr.write("AGENTS.md was not found at the artifact root: %s\n" % ROOT)
        return 2
    errors: List[str] = []
    notes: List[str] = []
    check_relative_links(errors, notes)
    check_skill_copies(errors, notes)
    check_skill_configs(errors, notes)
    check_imports(errors, notes)
    check_invariants(errors, notes)
    check_section_refs(errors, notes)
    check_versions(errors, notes)
    for line in notes:
        sys.stdout.write(line + "\n")
    if errors:
        sys.stderr.write("FAILED:\n")
        for line in errors:
            sys.stderr.write(line + "\n")
        return 1
    sys.stdout.write("All checks passed\n")
    return 0


def run_checks(
    root: Path = DEFAULT_ROOT,
    *,
    excluded_top_level: Sequence[str] = (),
) -> int:
    """Run checks at ``root`` with optional source-repository exclusions.

    ``excluded_top_level`` is an internal integration hook for a maintainer
    wrapper. It excludes only matching first path components from recursive
    Markdown discovery; fixed contract paths such as ``docs/REVIEW.md`` remain
    checked. The public CLI intentionally does not expose this option.
    """
    exclusions = frozenset(excluded_top_level)
    for name in exclusions:
        if not name or Path(name).parts != (name,) or name in {".", ".."}:
            raise ValueError(
                "excluded_top_level entries must be single relative path names: %r"
                % name
            )

    global ROOT, EXCLUDED_TOP_LEVEL_NAMES
    previous_root = ROOT
    previous_exclusions = EXCLUDED_TOP_LEVEL_NAMES
    ROOT = root.expanduser().resolve()
    EXCLUDED_TOP_LEVEL_NAMES = exclusions
    try:
        return _run_checks()
    finally:
        ROOT = previous_root
        EXCLUDED_TOP_LEVEL_NAMES = previous_exclusions


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check one materialized coding-agent documentation template."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="materialized artifact root (default: inferred from this script)",
    )
    args = parser.parse_args(argv)
    return run_checks(args.root)


if __name__ == "__main__":
    sys.exit(main())
