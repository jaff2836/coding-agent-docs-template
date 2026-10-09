#!/usr/bin/env python3
"""Run the canonical artifact checker against the maintainer source tree.

The distributable checker lives under ``template/common``. A source checkout
also contains locale and common source directories that are not materialized
project documentation, so the no-argument maintainer command excludes those
two top-level trees from recursive Markdown discovery. It also checks the
source project-analysis copies and the root review copies against the Korean
payload, and the root README locale tables against the locale manifest.
Passing any CLI option delegates unchanged to the artifact checker; in
particular, ``--root`` checks an arbitrary materialized artifact without
maintainer exclusions.
"""

from __future__ import annotations

import importlib.util
import itertools
import re
import sys
from pathlib import Path
from typing import Optional, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
COMMON_CHECKER = REPOSITORY_ROOT / "template/common/scripts/check-docs.py"
LOCALE_CHECKER = REPOSITORY_ROOT / "scripts/check_locales.py"

# Root copies of Korean payload files. Each listed heading opens a section the
# project fills in: either the whole section or only its table body rows may
# differ from the payload (D-019).
ROOT_COPY_OWNED_SECTIONS = {
    "docs/REVIEW.md": (
        ("## 6. Project-specific Invariants", "section"),
        ("## 9. Accepted Deferrals", "rows"),
    ),
    "docs/REVIEW_ROUND.md": (
        ("### 2.1 리뷰어 등록", "rows"),
    ),
    ".cursor/BUGBOT.md": (
        ("## 이 저장소의 불변조건", "section"),
        ("## 확정된 설계 결정과 승인된 deferral", "section"),
    ),
}
README_LOCALE_TABLES = ("README.md", "README.ko.md")
TABLE_SEPARATOR_RE = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load checker: %s" % path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECK_DOCS = load_module("common_check_docs", COMMON_CHECKER)
CHECK_LOCALES = load_module("maintainer_check_locales", LOCALE_CHECKER)


def read_source_file(relative_path: str) -> bytes:
    root = REPOSITORY_ROOT.resolve()
    resolved = (root / relative_path).resolve(strict=True)
    resolved.relative_to(root)
    if not resolved.is_file():
        raise ValueError("expected a regular file")
    return resolved.read_bytes()


def check_source_analysis_copies() -> list[str]:
    reference = None
    reference_path = None
    errors = []
    for relative_path in (
        ".agents/skills/project-analysis/SKILL.md",
        ".claude/skills/project-analysis/SKILL.md",
        "locales/ko/.agents/skills/project-analysis/SKILL.md",
        "locales/ko/.claude/skills/project-analysis/SKILL.md",
    ):
        try:
            content = read_source_file(relative_path)
        except (OSError, RuntimeError, ValueError) as error:
            errors.append(
                "Cannot read source analysis skill %s: %s" % (relative_path, error)
            )
            continue
        if reference is None:
            reference = content
            reference_path = relative_path
        elif content != reference:
            errors.append(
                "Source analysis skill copies differ: %s != %s"
                % (reference_path, relative_path)
            )
    return errors


def table_body_rows(
    lines: list[str], context: Sequence[tuple[bool, bool]], start: int, end: int
) -> set[int]:
    """Return body row indexes of the tables between *start* and *end*.

    A table is a header and separator outside fences and HTML comments; its
    body is the run of ``|`` lines that follows them outside comments.
    """

    rows: set[int] = set()
    index = start
    while index < end - 1:
        if (
            lines[index].startswith("|")
            and TABLE_SEPARATOR_RE.match(lines[index + 1])
            and all(context[index])
            and all(context[index + 1])
        ):
            index += 2
            while index < end and lines[index].startswith("|") and all(context[index]):
                rows.add(index)
                index += 1
        else:
            index += 1
    return rows


def shared_lines(
    text: str, owned: Sequence[tuple[str, str]], label: str, errors: list[str]
) -> Optional[list[tuple[int, str]]]:
    """Return numbered lines outside the project-owned parts of *text*."""

    lines = text.splitlines()
    context = CHECK_DOCS.markdown_line_context(text)
    keep = [True] * len(lines)
    for heading, scope in owned:
        starts = [
            index
            for index, line in enumerate(lines)
            if line.rstrip() == heading and all(context[index])
        ]
        if len(starts) != 1:
            errors.append(
                "%s: heading %r must appear exactly once (found %d)"
                % (label, heading, len(starts))
            )
            return None
        level = len(heading) - len(heading.lstrip("#"))
        end = len(lines)
        for index in range(starts[0] + 1, len(lines)):
            match = CHECK_DOCS.HEADING_RE.match(lines[index])
            if match and all(context[index]) and len(match.group(1)) <= level:
                end = index
                break
        if scope == "section":
            owned_lines = range(starts[0] + 1, end)
        else:
            owned_lines = table_body_rows(lines, context, starts[0] + 1, end)
        for index in owned_lines:
            keep[index] = False
    return [(index + 1, line) for index, line in enumerate(lines) if keep[index]]


def check_root_copies() -> list[str]:
    errors: list[str] = []
    for relative_path, owned in ROOT_COPY_OWNED_SECTIONS.items():
        source_path = "locales/ko/" + relative_path
        compared = []
        for path in (relative_path, source_path):
            try:
                text = read_source_file(path).decode("utf-8")
            except (OSError, RuntimeError, ValueError) as error:
                errors.append("Cannot read root copy %s: %s" % (path, error))
                continue
            compared.append(shared_lines(text, owned, path, errors))
        if len(compared) != 2 or None in compared:
            continue
        for copy, source in itertools.zip_longest(*compared, fillvalue=(None, None)):
            if copy[1] != source[1]:
                errors.append(
                    "Root copy %s differs from %s outside project-owned "
                    "sections at line %s"
                    % (relative_path, source_path, copy[0] or "end of file")
                )
                break
    return errors


def table_cells(line: str) -> list[str]:
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def check_readme_locale_table() -> list[str]:
    manifest, manifest_errors = CHECK_LOCALES.read_validated_manifest(
        REPOSITORY_ROOT.resolve()
    )
    if manifest is None:
        return ["Cannot read locale manifest: %s" % error for error in manifest_errors]
    complete = CHECK_LOCALES.complete_locales(manifest)
    errors = []
    for relative_path in README_LOCALE_TABLES:
        try:
            text = read_source_file(relative_path).decode("utf-8")
        except (OSError, RuntimeError, ValueError) as error:
            errors.append("Cannot read %s: %s" % (relative_path, error))
            continue
        lines = text.splitlines()
        context = CHECK_DOCS.markdown_line_context(text)
        headers = [
            index
            for index, line in enumerate(lines[:-1])
            if line.startswith("|")
            and table_cells(line)[0] == "Locale"
            and TABLE_SEPARATOR_RE.match(lines[index + 1])
            and all(context[index])
        ]
        if len(headers) != 1:
            errors.append(
                "%s: expected one table whose first column is Locale (found %d)"
                % (relative_path, len(headers))
            )
            continue
        # Rows hold the locale tag, the language name, and the status.
        for index in range(headers[0] + 2, len(lines)):
            if not lines[index].startswith("|"):
                break
            cells = table_cells(lines[index])
            if len(cells) < 3:
                errors.append(
                    "%s:%d: locale row needs tag, language, and status"
                    % (relative_path, index + 1)
                )
                continue
            if cells[0] not in complete:
                errors.append(
                    "%s:%d: locale %s is not complete in locales/manifest.json"
                    % (relative_path, index + 1, cells[0])
                )
            if cells[2] != "complete":
                errors.append(
                    "%s:%d: locale %s status must be complete, not %s"
                    % (relative_path, index + 1, cells[0], cells[2])
                )
    return errors


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments:
        CHECK_DOCS.HISTORY_PATH = "docs/TEMPLATE_GUIDE.md"
        return CHECK_DOCS.main(arguments)
    CHECK_DOCS.HISTORY_PATH = "CHANGELOG.md"
    errors = (
        check_source_analysis_copies()
        + check_root_copies()
        + check_readme_locale_table()
    )
    if errors:
        for error in errors:
            print("ERROR: %s" % error, file=sys.stderr)
        return 1
    return CHECK_DOCS.run_checks(
        REPOSITORY_ROOT,
        excluded_top_level=("locales", "template"),
    )


if __name__ == "__main__":
    sys.exit(main())
