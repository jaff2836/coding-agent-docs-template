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
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple
from urllib.parse import unquote, urlsplit


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

VERSION_RE = re.compile(
    r"^[ \t]*-[ \t]*\*\*Template version:\*\*[ \t]*(\S(?:[^\r\n]*\S)?)[ \t]*$",
    re.MULTILINE,
)
IMPORT_LINE_RE = re.compile(r"^@([^\s]+)\s*$")
HEADING_RE = re.compile(r"^[ ]{0,3}(#{1,6})\s+(.*)$")
HEADING_NUM_RE = re.compile(r"^[ ]{0,3}#{1,6}\s+(\d+(?:\.\d+)*)[.\s]")
FENCE_LINE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")
BLOCKQUOTE_MARKER_RE = re.compile(r"[ ]{0,3}>[ \t]?")
# CommonMark HTML blocks: type 1 ends at its closing tag, type 6 at a blank line.
HTML_BLOCK_RAW_RE = re.compile(
    r"^[ ]{0,3}<(pre|script|style|textarea)(?:[ \t>]|$)", re.IGNORECASE
)
HTML_BLOCK_TAG_RE = re.compile(
    r"^[ ]{0,3}</?(address|article|aside|base|basefont|blockquote|body|caption|"
    r"center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|"
    r"figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|"
    r"legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|"
    r"param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|"
    r"track|ul)(?:[ \t>]|/>|$)",
    re.IGNORECASE,
)
LIST_ITEM_RE = re.compile(r"^( *)(?:[-+*]|\d{1,9}[.)])([ \t]+)")
REFERENCE_DEFINITION_RE = re.compile(
    r"^[ ]{0,3}\[((?:\\.|[^\]\r\n])+)\]:[ \t]*"
)
REFERENCE_DEFINITION_TAIL_RE = re.compile(
    r"(?:[ \t]+(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|\((?:\\.|[^()\\])*\)))?[ \t]*"
)
SECTION_GROUP = r"§\d+(?:\.\d+)*(?:·§\d+(?:\.\d+))*"
SECTION_AFTER_LINK_RE = re.compile(r"[ \t]*(" + SECTION_GROUP + ")")
SECTION_PATH_RE = re.compile(r"`([^`\s]+\.md)`[ \t]*(" + SECTION_GROUP + ")")
SECTION_FILENAME_RE = re.compile(
    r"(?<![\w./-])([A-Za-z0-9][A-Za-z0-9_.-]*\.md)[ \t]+("
    + SECTION_GROUP
    + ")",
    re.IGNORECASE,
)
SECTION_NAME_RE = re.compile(
    r"(?<![\w./-])([A-Z][A-Z_]*)[ \t]+(" + SECTION_GROUP + ")"
)
SECTION_SPLIT_RE = re.compile(r"[§·]+")

PROJECT_INVARIANTS_MARKER = "<!-- template-section:project-invariants -->"
RELEASE_HISTORY_MARKER = "<!-- template-section:release-history -->"
PROJECT_INVARIANT_EXAMPLE_MARKER = (
    "<!-- template-example:project-invariant -->"
)
PROJECT_INVARIANT_EXAMPLE_PREFIXES = tuple(
    "%s **%s:**" % (marker, label)
    for marker in ("-", "+", "*")
    for label in ("Example", "예시")
)

HISTORY_PATH = "docs/TEMPLATE_GUIDE.md"

SKILL_PAIRS: List[Tuple[str, str]] = [
    (
        ".agents/skills/design/SKILL.md",
        ".claude/skills/design/SKILL.md",
    ),
    (
        ".agents/skills/project-analysis/SKILL.md",
        ".claude/skills/project-analysis/SKILL.md",
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


def md_files(errors: Optional[List[str]] = None) -> List[Path]:
    files = []
    for directory, child_directories, child_files in os.walk(
        ROOT, topdown=True, followlinks=False
    ):
        parent = Path(directory)
        at_root = parent == ROOT
        retained_directories = []
        for name in child_directories:
            if name in SKIP_DIR_NAMES or (
                at_root and name in EXCLUDED_TOP_LEVEL_NAMES
            ):
                continue
            path = parent / name
            if path.is_symlink():
                message = (
                    "Markdown directory symlinks are not supported: %s" % rel(path)
                    if is_inside_root(path)
                    else "Markdown directory escapes artifact root: %s" % rel(path)
                )
                if errors is not None and message not in errors:
                    errors.append(message)
                continue
            if name.endswith(".md"):
                message = "Markdown source is not a file: %s" % rel(path)
                if errors is not None and message not in errors:
                    errors.append(message)
            retained_directories.append(name)
        child_directories[:] = retained_directories

        for name in child_files:
            if not name.endswith(".md") or (
                at_root and name in EXCLUDED_TOP_LEVEL_NAMES
            ):
                continue
            path = parent / name
            if not is_inside_root(path):
                message = "Markdown source escapes artifact root: %s" % rel(path)
                if errors is not None and message not in errors:
                    errors.append(message)
                continue
            if not path.is_file():
                message = "Markdown source is not a file: %s" % rel(path)
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


def path_entry_exists(path: Path) -> bool:
    """Return whether a path entry exists without following its final symlink."""

    return path.exists() or path.is_symlink()


def optional_file_present(path: Path, label: str, errors: List[str]) -> bool:
    """Return whether an optional contract file exists as a regular in-root file.

    A missing entry is an allowed omission. An entry that escapes the artifact
    root or is not a regular file is reported instead of being treated as absent.
    """

    if not path_entry_exists(path):
        return False
    if not is_inside_root(path):
        errors.append("%s escapes artifact root" % label)
        return False
    if not path.is_file():
        errors.append("%s is not a file" % label)
        return False
    return True


def check_relative_links(errors: List[str], notes: List[str]) -> None:
    broken = []
    scanned = 0
    links = 0
    for md in md_files(errors):
        scanned += 1
        text = md.read_text(encoding="utf-8")
        searchable = markdown_searchable_text(text, mask_inline_code=True)
        destinations = markdown_link_destinations(searchable)
        destinations.extend(markdown_reference_destinations(searchable))
        for destination in destinations:
            target = local_link_path(destination)
            if target is None:
                continue
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
        a_is_file = is_file_inside_root(a)
        b_is_file = is_file_inside_root(b)
        if path_entry_exists(a) and not is_inside_root(a):
            errors.append("Skill source escapes artifact root: %s" % left)
            continue
        if path_entry_exists(b) and not is_inside_root(b):
            errors.append("Skill copy escapes artifact root: %s" % right)
            continue
        if not a_is_file and not b_is_file:
            errors.append("Skill files are missing: %s, %s" % (left, right))
            continue
        if not a_is_file:
            errors.append("Skill source is missing: %s" % left)
            continue
        if not b_is_file:
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
    values: List[Optional[bool]] = []
    for indent, entry in entries:
        if indent != child_indent:
            continue
        key = re.match(r"allow_implicit_invocation:\s*(.*)$", entry)
        if key is None:
            continue
        value = re.fullmatch(
            r"(true|false)\s*(?:#.*)?", key.group(1), re.IGNORECASE
        )
        values.append(
            value.group(1).lower() == "true" if value is not None else None
        )
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
    if not optional_file_present(watchdog, ".omp/WATCHDOG.md", errors):
        if not path_entry_exists(watchdog):
            notes.append("WATCHDOG.md omitted (allowed)")
        return

    imports = []
    for line in watchdog.read_text(encoding="utf-8").splitlines():
        match = IMPORT_LINE_RE.match(line)
        if match:
            imports.append(match.group(1))
    expected_import = "../docs/REVIEW.md"
    if imports != [expected_import]:
        for spec in imports:
            if not is_inside_root(watchdog.parent / spec):
                errors.append(
                    ".omp/WATCHDOG.md import escapes artifact root: %s" % spec
                )
        found = ", ".join("@" + spec for spec in imports) or "none"
        errors.append(
            ".omp/WATCHDOG.md must import exactly @%s (found: %s)"
            % (expected_import, found)
        )
        return
    dest = watchdog.parent / expected_import
    if not is_inside_root(dest):
        errors.append(
            ".omp/WATCHDOG.md import escapes artifact root: %s" % expected_import
        )
    elif not dest.is_file():
        errors.append(
            ".omp/WATCHDOG.md import target is missing: %s" % expected_import
        )
    else:
        notes.append("WATCHDOG.md import: @%s" % expected_import)


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


def indented_code_line_indexes(text: str) -> set:
    """Return line indexes belonging to ordinary or list-relative code blocks."""

    code_lines = set()
    list_items: List[Tuple[int, int]] = []
    in_code = False
    code_indent = 4
    previous_blank = True

    for index, raw_line in enumerate(text.splitlines()):
        _, line = strip_blockquote_markers(raw_line)
        line = line.expandtabs(4)
        if not line.strip():
            if in_code:
                code_lines.add(index)
            previous_blank = True
            continue

        leading = len(line) - len(line.lstrip(" "))
        list_item = LIST_ITEM_RE.match(line)
        if list_item is not None:
            marker_indent = len(list_item.group(1))
            while list_items and marker_indent <= list_items[-1][0]:
                list_items.pop()
            while list_items and marker_indent < list_items[-1][1]:
                list_items.pop()
            list_items.append((marker_indent, list_item.end()))
            in_code = False
            previous_blank = False
            continue

        while list_items and leading < list_items[-1][1]:
            list_items.pop()
        required_indent = (list_items[-1][1] if list_items else 0) + 4
        if in_code:
            if leading >= code_indent:
                code_lines.add(index)
                previous_blank = False
                continue
            in_code = False
        if previous_blank and leading >= required_indent:
            code_indent = required_indent
            in_code = True
            code_lines.add(index)
        previous_blank = False
    return code_lines


def markdown_line_context(text: str) -> Tuple[Tuple[bool, bool], ...]:
    """Return ``(outside_fence, outside_enclosing_comment)`` per line."""

    context = []
    fence_character: Optional[str] = None
    fence_length = 0
    fence_blockquote_depth = 0
    in_html_comment = False
    html_block_end: Optional[str] = None
    indented_code_lines = indented_code_line_indexes(text)
    inline_masked_lines = mask_inline_code_spans(text).splitlines()
    list_items: List[Tuple[int, int]] = []
    for index, line in enumerate(text.splitlines()):
        blockquote_depth, container_line = strip_blockquote_markers(line)
        container_line = container_line.expandtabs(4)
        if html_block_end is not None:
            context.append((False, False))
            if html_block_end == "" and not container_line.strip():
                html_block_end = None
            elif html_block_end and html_block_end in line.lower():
                html_block_end = None
            continue
        if fence_character is not None:
            if blockquote_depth < fence_blockquote_depth:
                fence_character = None
                fence_length = 0
                fence_blockquote_depth = 0
            else:
                _, closing_container = strip_blockquote_markers(
                    line, fence_blockquote_depth
                )
                closing_candidate = list_relative_line(
                    closing_container.expandtabs(4), list_items, update=False
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

        if not in_html_comment and index in indented_code_lines:
            context.append((False, False))
            continue

        fence_candidate = list_relative_line(
            container_line, list_items, update=not in_html_comment
        )
        fence = (
            None
            if in_html_comment
            else FENCE_LINE_RE.fullmatch(fence_candidate)
        )
        if fence is not None:
            sequence = fence.group(1)
            fence_character = sequence[0]
            fence_length = len(sequence)
            fence_blockquote_depth = blockquote_depth
            context.append((False, False))
            continue

        raw_block = (
            None if in_html_comment else HTML_BLOCK_RAW_RE.match(fence_candidate)
        )
        if raw_block is not None:
            closing = "</%s>" % raw_block.group(1).lower()
            context.append((False, False))
            if closing not in fence_candidate.lower()[raw_block.end() :]:
                html_block_end = closing
            continue
        if not in_html_comment and HTML_BLOCK_TAG_RE.match(fence_candidate):
            context.append((False, False))
            html_block_end = ""
            continue

        context.append((True, not in_html_comment))
        cursor = 0
        while cursor < len(line):
            token = "-->" if in_html_comment else "<!--"
            search_line = line if in_html_comment else inline_masked_lines[index]
            position = search_line.find(token, cursor)
            if position < 0:
                break
            in_html_comment = not in_html_comment
            cursor = position + len(token)
    return tuple(context)


def list_relative_line(
    line: str, list_items: List[Tuple[int, int]], *, update: bool
) -> str:
    """Remove the active list container indentation from one Markdown line."""

    if not line.strip():
        return line
    leading = len(line) - len(line.lstrip(" "))
    if update:
        list_item = LIST_ITEM_RE.match(line)
        if list_item is not None:
            marker_indent = len(list_item.group(1))
            while list_items and marker_indent <= list_items[-1][0]:
                list_items.pop()
            while list_items and marker_indent < list_items[-1][1]:
                list_items.pop()
            list_items.append((marker_indent, list_item.end()))
            return line[list_item.end() :]
        while list_items and leading < list_items[-1][1]:
            list_items.pop()
    if list_items and leading >= list_items[-1][1]:
        return line[list_items[-1][1] :]
    return line


def mask_text_range(characters: List[str], start: int, end: int) -> None:
    """Replace non-newline characters in one range while preserving offsets."""

    for index in range(start, end):
        if characters[index] not in "\r\n":
            characters[index] = " "


def mask_inline_code_spans(text: str) -> str:
    """Mask paired Markdown backtick spans while preserving string offsets."""

    characters = list(text)
    cursor = 0
    while cursor < len(text):
        start = text.find("`", cursor)
        if start < 0:
            break
        opening_end = start + 1
        while opening_end < len(text) and text[opening_end] == "`":
            opening_end += 1
        run_length = opening_end - start

        candidate = opening_end
        closing_end: Optional[int] = None
        while candidate < len(text):
            closing_start = text.find("`", candidate)
            if closing_start < 0:
                break
            run_end = closing_start + 1
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1
            if run_end - closing_start == run_length:
                closing_end = run_end
                break
            candidate = run_end

        if closing_end is None:
            cursor = opening_end
            continue
        mask_text_range(characters, start, closing_end)
        cursor = closing_end
    return "".join(characters)


def markdown_searchable_text(text: str, *, mask_inline_code: bool = False) -> str:
    """Mask non-prose Markdown constructs while preserving string offsets."""

    masked_lines = []
    in_html_comment = False
    contexts = markdown_line_context(text)
    inline_masked_lines = mask_inline_code_spans(text).splitlines(keepends=True)
    for line, inline_masked_line, (outside_fence, _) in zip(
        text.splitlines(keepends=True), inline_masked_lines, contexts
    ):
        characters = list(line)
        content_end = len(line.rstrip("\r\n"))
        if not outside_fence:
            mask_text_range(characters, 0, content_end)
            masked_lines.append("".join(characters))
            continue

        cursor = 0
        while cursor < content_end:
            if in_html_comment:
                end = line.find("-->", cursor, content_end)
                stop = content_end if end < 0 else end + 3
                mask_text_range(characters, cursor, stop)
                cursor = stop
                if end >= 0:
                    in_html_comment = False
                continue

            start = inline_masked_line.find("<!--", cursor, content_end)
            if start < 0:
                break
            end = line.find("-->", start + 4, content_end)
            stop = content_end if end < 0 else end + 3
            mask_text_range(characters, start, stop)
            cursor = stop
            if end < 0:
                in_html_comment = True
        masked_lines.append("".join(characters))
    searchable = "".join(masked_lines)
    return mask_inline_code_spans(searchable) if mask_inline_code else searchable


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def markdown_link_label_start(text: str, closing_bracket: int) -> Optional[int]:
    """Return the matching unescaped ``[`` on the same line, if present."""

    if is_escaped(text, closing_bracket):
        return None
    nested = 0
    cursor = closing_bracket - 1
    while cursor >= 0 and text[cursor] not in "\r\n":
        if is_escaped(text, cursor):
            cursor -= 1
            continue
        if text[cursor] == "]":
            nested += 1
        elif text[cursor] == "[":
            if nested:
                nested -= 1
            else:
                return cursor
        cursor -= 1
    return None


def markdown_inline_links(text: str) -> List[Tuple[int, str, int]]:
    """Return ``(start, destination, end)`` for valid inline Markdown links."""

    links = []
    search_from = 0
    while True:
        marker = text.find("](", search_from)
        if marker < 0:
            break
        label_start = markdown_link_label_start(text, marker)
        if label_start is None:
            search_from = marker + 2
            continue
        cursor = skip_link_whitespace(text, marker + 2)
        if cursor is None:
            search_from = marker + 2
            continue
        if cursor >= len(text):
            break

        destination: List[str] = []
        link_end: Optional[int] = None
        if text[cursor] == "<":
            cursor += 1
            valid = False
            while cursor < len(text) and text[cursor] not in "\r\n":
                character = text[cursor]
                if character == "\\" and cursor + 1 < len(text):
                    destination.append(text[cursor + 1])
                    cursor += 2
                    continue
                if character == ">":
                    valid = True
                    cursor += 1
                    break
                destination.append(character)
                cursor += 1
            if valid:
                link_end = markdown_inline_link_end(text, cursor)
        else:
            depth = 0
            valid = False
            while cursor < len(text):
                character = text[cursor]
                if character == "\\" and cursor + 1 < len(text):
                    destination.append(text[cursor + 1])
                    cursor += 2
                    continue
                if character == "(":
                    depth += 1
                    destination.append(character)
                    cursor += 1
                    continue
                if character == ")":
                    if depth == 0:
                        valid = True
                        cursor += 1
                        link_end = cursor
                        break
                    depth -= 1
                    destination.append(character)
                    cursor += 1
                    continue
                if character.isspace() and depth == 0:
                    valid = True
                    break
                destination.append(character)
                cursor += 1
            if valid and link_end is None:
                link_end = markdown_inline_link_end(text, cursor)
        if link_end is not None and destination:
            links.append((label_start, "".join(destination), link_end))
        search_from = max(link_end or cursor, marker + 2)
    return links


def skip_link_whitespace(text: str, cursor: int) -> Optional[int]:
    """Skip spaces, tabs and at most one line ending that does not end a paragraph."""

    while cursor < len(text) and text[cursor] in " \t":
        cursor += 1
    if cursor < len(text) and text[cursor] in "\r\n":
        cursor += 2 if text.startswith("\r\n", cursor) else 1
        while cursor < len(text) and text[cursor] in " \t":
            cursor += 1
        if cursor >= len(text) or text[cursor] in "\r\n":
            return None
    return cursor


def markdown_inline_link_end(text: str, cursor: int) -> Optional[int]:
    """Return the offset after an inline link's closing parenthesis."""

    skipped = skip_link_whitespace(text, cursor)
    if skipped is None or skipped >= len(text):
        return None
    cursor = skipped
    if text[cursor] == ")":
        return cursor + 1
    opener = text[cursor]
    closing = {'"': '"', "'": "'", "(": ")"}.get(opener)
    if closing is None:
        return None
    cursor += 1
    while cursor < len(text):
        if text[cursor] == "\\" and cursor + 1 < len(text):
            cursor += 2
            continue
        if text[cursor] in "\r\n":
            following = skip_link_whitespace(text, cursor)
            if following is None:
                return None
            cursor = following
            continue
        if text[cursor] == closing:
            cursor += 1
            break
        cursor += 1
    else:
        return None
    skipped = skip_link_whitespace(text, cursor)
    if skipped is None:
        return None
    return skipped + 1 if skipped < len(text) and text[skipped] == ")" else None


def markdown_link_destinations(text: str) -> List[str]:
    """Extract inline-link destinations, including bracketed and escaped forms."""

    return [destination for _, destination, _ in markdown_inline_links(text)]


def normalize_reference_label(label: str) -> str:
    unescaped = re.sub(r"\\(.)", r"\1", label)
    return " ".join(unescaped.split()).casefold()


def markdown_reference_definitions(text: str) -> List[Tuple[str, str]]:
    """Extract normalized labels and destinations from link definitions."""

    definitions = []
    for line in text.splitlines():
        definition = REFERENCE_DEFINITION_RE.match(line)
        if definition is None:
            continue
        label = normalize_reference_label(definition.group(1))
        cursor = definition.end()
        destination = []
        if cursor < len(line) and line[cursor] == "<":
            cursor += 1
            while cursor < len(line):
                character = line[cursor]
                if character == "\\" and cursor + 1 < len(line):
                    destination.append(line[cursor + 1])
                    cursor += 2
                    continue
                if character == ">":
                    cursor += 1
                    break
                destination.append(character)
                cursor += 1
            else:
                continue
        else:
            depth = 0
            while cursor < len(line):
                character = line[cursor]
                if character == "\\" and cursor + 1 < len(line):
                    destination.append(line[cursor + 1])
                    cursor += 2
                    continue
                if character == "(":
                    depth += 1
                elif character == ")":
                    if depth == 0:
                        destination = []
                        break
                    depth -= 1
                elif character.isspace() and depth == 0:
                    break
                destination.append(character)
                cursor += 1
            if depth != 0:
                continue
        if destination and REFERENCE_DEFINITION_TAIL_RE.fullmatch(line[cursor:]):
            definitions.append((label, "".join(destination)))
    return definitions


def markdown_reference_destinations(text: str) -> List[str]:
    """Extract destinations from visible Markdown link reference definitions."""

    return [destination for _, destination in markdown_reference_definitions(text)]


def markdown_reference_links(
    text: str, definitions: dict
) -> List[Tuple[int, str, int]]:
    """Resolve full, collapsed, and shortcut reference-style links."""

    links = []
    search_from = 0
    while True:
        closing = text.find("]", search_from)
        if closing < 0:
            break
        label_start = markdown_link_label_start(text, closing)
        if label_start is None:
            search_from = closing + 1
            continue

        label = text[label_start + 1 : closing]
        link_end = closing + 1
        if link_end < len(text) and text[link_end] == "[":
            cursor = link_end + 1
            reference = []
            while cursor < len(text) and text[cursor] not in "\r\n":
                if text[cursor] == "\\" and cursor + 1 < len(text):
                    reference.extend(text[cursor : cursor + 2])
                    cursor += 2
                    continue
                if text[cursor] == "]":
                    link_end = cursor + 1
                    break
                reference.append(text[cursor])
                cursor += 1
            else:
                search_from = closing + 1
                continue
            label = "".join(reference) or label

        destination = definitions.get(normalize_reference_label(label))
        if destination is not None:
            links.append((label_start, destination, link_end))
        search_from = max(link_end, closing + 1)
    return links


def local_link_path(destination: str) -> Optional[str]:
    """Return the file path for a local Markdown destination, if it has one."""

    try:
        parsed = urlsplit(destination)
    except ValueError:
        return None
    if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
        return None
    return unquote(parsed.path) or None


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
        bullet_match = re.match(r"^( {0,3})[-+*]\s+", line)
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
    """Collect short docs/ names for references such as `PROJECT §8`.

    A short name shared by several files maps to the tuple of those files so a
    symbolic reference cannot silently resolve to an arbitrary one of them.
    """
    candidates: dict = {}
    for path in sorted((ROOT / "docs").glob("*.md")):
        if not is_inside_root(path):
            message = "Markdown source escapes artifact root: %s" % rel(path)
            if errors is not None and message not in errors:
                errors.append(message)
            continue
        if not path.is_file():
            continue
        candidates.setdefault(re.sub(r"^\d+-", "", path.stem), []).append(path)
    return {
        name: paths[0] if len(paths) == 1 else tuple(paths)
        for name, paths in candidates.items()
    }


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
        searchable = markdown_searchable_text(text)
        searchable_without_inline_code = markdown_searchable_text(
            text, mask_inline_code=True
        )
        limit = len(text)
        if cut_at and md == cut_at[0]:
            limit = cut_at[1]
        references: List[Tuple[str, str, str]] = []
        definitions = {}
        for label, destination in markdown_reference_definitions(
            searchable_without_inline_code
        ):
            definitions.setdefault(label, destination)
        links = markdown_inline_links(searchable_without_inline_code)
        links.extend(
            markdown_reference_links(searchable_without_inline_code, definitions)
        )
        for start, destination, end in links:
            if start >= limit:
                continue
            local_ref = local_link_path(destination)
            if local_ref is None or not local_ref.endswith(".md"):
                continue
            section = SECTION_AFTER_LINK_RE.match(
                searchable_without_inline_code, end
            )
            if section is not None:
                references.append((destination, section.group(1), "path"))

        for regex, kind, search_text in (
            (SECTION_PATH_RE, "path", searchable),
            (SECTION_FILENAME_RE, "filename", searchable_without_inline_code),
            (SECTION_NAME_RE, "name", searchable_without_inline_code),
        ):
            for match in regex.finditer(search_text):
                if match.start() >= limit:
                    continue
                ref, group = match.group(1), match.group(2)
                references.append((ref, group, kind))

        for ref, group, kind in references:
            if kind == "name":
                short_name = ref[:-3] if ref.endswith(".md") else ref
                target = names.get(short_name)
            else:
                local_ref = local_link_path(ref)
                if local_ref is None:
                    continue
                target = next(
                    (
                        candidate
                        for candidate in (md.parent / local_ref, ROOT / local_ref)
                        if is_inside_root(candidate) and candidate.is_file()
                    ),
                    None,
                )
                if target is None and kind == "filename":
                    short_name = re.sub(r"^\d+-", "", Path(local_ref).stem)
                    target = names.get(short_name)
            if isinstance(target, tuple):
                broken.append(
                    "%s: %s %s (ambiguous document name: %s; use a file name or path)"
                    % (rel(md), ref, group, ", ".join(rel(path) for path in target))
                )
                continue
            if target is None:
                if kind in {"path", "filename"}:
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
    if not optional_file_present(copy_file, INVARIANT_COPY, errors):
        if not path_entry_exists(copy_file):
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


def read_template_versions(path: Path) -> List[str]:
    if not is_file_inside_root(path):
        return []
    text = path.read_text(encoding="utf-8")
    return VERSION_RE.findall(markdown_searchable_text(text, mask_inline_code=True))


def read_template_version(path: Path) -> Optional[str]:
    versions = read_template_versions(path)
    return versions[0] if len(versions) == 1 else None


def require_template_version(path: Path, label: str, errors: List[str]) -> Optional[str]:
    versions = read_template_versions(path)
    if len(versions) != 1:
        errors.append(
            "Template version must appear exactly once in %s (found %d)"
            % (label, len(versions))
        )
        return None
    return versions[0]


def check_versions(errors: List[str], notes: List[str]) -> None:
    guide = ROOT / "docs" / "TEMPLATE_GUIDE.md"
    docs_guide = ROOT / "docs" / "DOCS_GUIDE.md"
    v2 = require_template_version(
        docs_guide, "docs/DOCS_GUIDE.md", errors
    )

    # TEMPLATE_GUIDE.md may be deleted after adoption. An existing invalid
    # entry is an error, not an allowed omission.
    if not path_entry_exists(guide):
        notes.append(
            "TEMPLATE_GUIDE.md omitted (allowed): checking version only in "
            "DOCS_GUIDE.md"
        )
        if v2:
            notes.append("Template version: %s" % v2)
        return
    if not optional_file_present(guide, "docs/TEMPLATE_GUIDE.md", errors):
        return

    v1 = require_template_version(
        guide, "docs/TEMPLATE_GUIDE.md", errors
    )
    if v1 and v2 and v1 != v2:
        errors.append(
            "Template versions differ: TEMPLATE_GUIDE=%s, DOCS_GUIDE=%s"
            % (v1, v2)
        )
    elif v1 and v2:
        notes.append("Template versions match: %s" % v1)
        history_path = ROOT / HISTORY_PATH
        if not is_file_inside_root(history_path):
            errors.append(
                "Release history source is missing or unsafe: %s" % HISTORY_PATH
            )
            return
        history = history_path.read_text(encoding="utf-8")
        try:
            _, marker_index, end_index, _ = marked_section_bounds(
                history, RELEASE_HISTORY_MARKER
            )
        except ValueError as error:
            errors.append("%s: %s" % (HISTORY_PATH, error))
            return
        searchable_lines = markdown_searchable_text(history).splitlines()
        release_history = "\n".join(
            searchable_lines[marker_index + 1 : end_index]
        )
        version_heading = re.compile(
            r"^[ ]{0,3}#{2,3}\s+(?:v?%s|\[v?%s\]\([^\r\n)]+\))(?:\s|$)"
            % (re.escape(v1), re.escape(v1)),
            re.MULTILINE | re.IGNORECASE,
        )
        if version_heading.search(release_history) is None:
            errors.append(
                "Current version is absent from %s history: %s" % (HISTORY_PATH, v1)
            )
        else:
            notes.append("Current version is present in revision history: %s" % v1)


def _run_checks() -> int:
    if not is_file_inside_root(ROOT / "AGENTS.md"):
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
