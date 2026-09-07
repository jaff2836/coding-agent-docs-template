#!/usr/bin/env python3
"""문서 템플릿의 의존성 없는 검사.

상대 링크, 스킬 사본과 Codex 명시 호출 설정, 알려진 @import, REVIEW와 BUGBOT의
불변조건 목록, 문서를 지목한 절 번호 참조, 안내 문서의 Template version을
확인합니다. 하나라도 실패하면 종료 코드 1입니다. 저장소 루트 기준이며 cwd는
달라도 됩니다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    # 생성물·vendored 디렉터리. 적용 저장소에서 링크 검사 오탐을 막습니다.
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

# 템플릿의 안내용 예시 줄. 복제본에는 없으므로 대조에서 제외합니다.
EXAMPLE_BULLET_PREFIX = "- **예시:"

HEADING_NUM_RE = re.compile(r"^#{1,6}\s+(\d+(?:\.\d+)*)[.\s]")
SECTION_GROUP = r"§\d+(?:\.\d+)?(?:·§\d+(?:\.\d+)?)*"
SECTION_LINK_RE = re.compile(
    r"\]\(((?!https?://)[^)\s#]+?\.md)\)\s*(" + SECTION_GROUP + ")"
)
SECTION_PATH_RE = re.compile(r"`([^`\s]+\.md)`\s*(" + SECTION_GROUP + ")")
SECTION_NAME_RE = re.compile(r"\b([A-Z][A-Z_]*)(?:\.md)?\s+(" + SECTION_GROUP + ")")
SECTION_SPLIT_RE = re.compile(r"[§·]+")

# 릴리스 이력은 그 판의 구조를 설명하려고 옛 파일명·절 번호를 의도적으로 인용합니다
# (TEMPLATE_GUIDE.md "아래 릴리스 이력의 옛 파일명·절 번호는 당시 구조를 설명합니다").
HISTORY_SECTION: Tuple[str, str] = ("docs/TEMPLATE_GUIDE.md", "템플릿 변경 이력")

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

# Codex에서 암묵 호출을 막는 설정과 그 짝이 되는 스킬 원본.
SKILL_CONFIGS: List[Tuple[str, str]] = [
    (
        ".agents/skills/review-round/SKILL.md",
        ".agents/skills/review-round/agents/openai.yaml",
    ),
]

# 불변조건 목록의 정본과 복제본. 절 번호는 저장소마다 다를 수 있어 헤딩 문구로 찾습니다.
INVARIANT_SOURCE: Tuple[str, str] = ("docs/REVIEW.md", "Project-specific Invariants")
INVARIANT_COPY: Tuple[str, str] = (".cursor/BUGBOT.md", "불변조건")


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def md_files() -> List[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        if is_skipped(path):
            continue
        files.append(path)
    return sorted(files)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def check_relative_links(errors: List[str], notes: List[str]) -> None:
    broken = []
    scanned = 0
    links = 0
    for md in md_files():
        scanned += 1
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            links += 1
            dest = (md.parent / target)
            if not dest.exists():
                broken.append("%s: %s" % (rel(md), target))
    if broken:
        errors.append("깨진 상대 링크:")
        errors.extend("  %s" % item for item in broken)
    else:
        notes.append(
            "상대 링크: %d개 파일에서 %d개 확인, 깨진 링크 없음" % (scanned, links)
        )


def check_skill_copies(errors: List[str], notes: List[str]) -> None:
    for left, right in SKILL_PAIRS:
        a = ROOT / left
        b = ROOT / right
        if not a.is_file() and not b.is_file():
            errors.append("스킬 파일이 없습니다: %s, %s" % (left, right))
            continue
        if not a.is_file():
            errors.append("스킬 원본이 없습니다: %s" % left)
            continue
        if not b.is_file():
            notes.append("스킬 사본 생략(허용): %s" % right)
            continue
        if a.read_bytes() != b.read_bytes():
            errors.append("스킬 사본이 다릅니다: %s ↔ %s" % (left, right))
        else:
            notes.append("스킬 사본 일치: %s" % left)


def check_skill_configs(errors: List[str], notes: List[str]) -> None:
    for skill, config in SKILL_CONFIGS:
        if not (ROOT / skill).is_file():
            continue
        if (ROOT / config).is_file():
            notes.append("Codex 명시 호출 설정 있음: %s" % config)
        else:
            errors.append(
                "Codex 명시 호출 설정이 없습니다: %s (%s의 암묵 호출이 열립니다)"
                % (config, skill)
            )


def check_imports(errors: List[str], notes: List[str]) -> None:
    claude = ROOT / "CLAUDE.md"
    if not claude.is_file():
        errors.append("CLAUDE.md가 없습니다")
    else:
        body = claude.read_text(encoding="utf-8").strip()
        if body != "@AGENTS.md":
            errors.append("CLAUDE.md import가 @AGENTS.md가 아닙니다: %r" % body)
        else:
            notes.append("CLAUDE.md import: @AGENTS.md")

    watchdog = ROOT / ".omp" / "WATCHDOG.md"
    if not watchdog.is_file():
        notes.append("WATCHDOG.md 생략(허용)")
        return

    imports = []
    for line in watchdog.read_text(encoding="utf-8").splitlines():
        match = IMPORT_LINE_RE.match(line)
        if match:
            imports.append(match.group(1))
    if not imports:
        errors.append(".omp/WATCHDOG.md에 @경로 import가 없습니다")
        return
    for spec in imports:
        dest = watchdog.parent / spec
        if not dest.is_file():
            errors.append(".omp/WATCHDOG.md import 대상이 없습니다: %s" % spec)
        else:
            notes.append("WATCHDOG.md import: @%s" % spec)


def section_bullets(text: str, heading_needle: str) -> Optional[List[str]]:
    """헤딩 문구로 절을 찾아 그 절의 목록 항목만 돌려줍니다."""
    lines = text.splitlines()
    start = None
    level = 0
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match and heading_needle in match.group(2):
            start = index + 1
            level = len(match.group(1))
            break
    if start is None:
        return None

    bullets = []
    for line in lines[start:]:
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) <= level:
            break
        stripped = line.strip()
        if stripped.startswith(EXAMPLE_BULLET_PREFIX):
            continue
        if stripped.startswith("- "):
            bullets.append(stripped)
    return bullets


def numbered_headings(path: Path) -> set:
    numbers = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_NUM_RE.match(line)
        if match:
            numbers.add(match.group(1))
    return numbers


def doc_short_names() -> dict:
    """`PROJECT §8`처럼 이름만 쓰는 참조를 위해 docs/의 짧은 이름을 모읍니다."""
    names = {}
    for path in sorted((ROOT / "docs").glob("*.md")):
        names[re.sub(r"^\d+-", "", path.stem)] = path
    return names


def history_cut() -> Optional[Tuple[Path, int]]:
    """릴리스 이력 절이 시작하는 위치. 그 뒤의 절 참조는 검사하지 않습니다."""
    path_name, needle = HISTORY_SECTION
    path = ROOT / path_name
    if not path.is_file():
        return None
    offset = 0
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        match = HEADING_RE.match(line.rstrip("\n"))
        if match and needle in match.group(2):
            return (path, offset)
        offset += len(line)
    return None


def check_section_refs(errors: List[str], notes: List[str]) -> None:
    """`REVIEW.md §6`처럼 문서를 지목한 절 참조가 실제 헤딩과 맞는지 봅니다.

    문서를 지목하지 않은 같은 파일 안의 `§4` 같은 참조는 대상이 모호하므로
    검사하지 않습니다.
    """
    names = doc_short_names()
    cut_at = history_cut()
    headings: dict = {}
    broken: List[str] = []
    checked = 0

    for md in md_files():
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
                        (c for c in (md.parent / ref, ROOT / ref) if c.is_file()),
                        None,
                    )
                if target is None:
                    continue
                target = target.resolve()
                if target not in headings:
                    headings[target] = numbered_headings(target)
                for number in filter(None, SECTION_SPLIT_RE.split(group)):
                    checked += 1
                    if number not in headings[target]:
                        broken.append(
                            "%s: %s §%s (%s에 그 절이 없습니다)"
                            % (rel(md), ref, number, rel(target))
                        )

    if broken:
        errors.append("절 번호 참조가 실제 헤딩과 다릅니다:")
        errors.extend("  %s" % item for item in sorted(set(broken)))
    else:
        notes.append("절 번호 참조: %d건 확인, 불일치 없음" % checked)


def check_invariants(errors: List[str], notes: List[str]) -> None:
    copy_path, copy_needle = INVARIANT_COPY
    copy_file = ROOT / copy_path
    if not copy_file.is_file():
        notes.append("BUGBOT.md 생략(허용)")
        return

    source_path, source_needle = INVARIANT_SOURCE
    source_file = ROOT / source_path
    if not source_file.is_file():
        errors.append("%s가 없어 불변조건을 대조할 수 없습니다" % source_path)
        return

    source = section_bullets(source_file.read_text(encoding="utf-8"), source_needle)
    copy = section_bullets(copy_file.read_text(encoding="utf-8"), copy_needle)
    if source is None:
        errors.append(
            "%s에서 `%s` 헤딩을 찾지 못했습니다" % (source_path, source_needle)
        )
    if copy is None:
        errors.append("%s에서 `%s` 헤딩을 찾지 못했습니다" % (copy_path, copy_needle))
    if source is None or copy is None:
        return

    if source == copy:
        notes.append("불변조건 목록 일치: %d개" % len(source))
        return

    errors.append("불변조건 목록이 다릅니다: %s ↔ %s" % (source_path, copy_path))
    for item in source:
        if item not in copy:
            errors.append("  %s에만 있음: %s" % (source_path, item))
    for item in copy:
        if item not in source:
            errors.append("  %s에만 있음: %s" % (copy_path, item))


def read_template_version(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    match = VERSION_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def check_versions(errors: List[str], notes: List[str]) -> None:
    guide = ROOT / "docs" / "TEMPLATE_GUIDE.md"
    docs_guide = ROOT / "docs" / "DOCS_GUIDE.md"
    v2 = read_template_version(docs_guide)
    if v2 is None:
        errors.append("docs/DOCS_GUIDE.md에서 Template version을 찾지 못했습니다")

    # TEMPLATE_GUIDE.md는 적용 후 삭제할 수 있습니다 (TEMPLATE_GUIDE.md §5).
    if not guide.is_file():
        notes.append("TEMPLATE_GUIDE.md 생략(허용): 판 기록은 DOCS_GUIDE.md만 확인")
        if v2:
            notes.append("Template version: %s" % v2)
        return

    v1 = read_template_version(guide)
    if v1 is None:
        errors.append("docs/TEMPLATE_GUIDE.md에서 Template version을 찾지 못했습니다")
    if v1 and v2 and v1 != v2:
        errors.append(
            "Template version이 다릅니다: TEMPLATE_GUIDE=%s, DOCS_GUIDE=%s"
            % (v1, v2)
        )
    elif v1 and v2:
        notes.append("Template version 일치: %s" % v1)
        history = guide.read_text(encoding="utf-8")
        if ("### v%s" % v1) not in history and ("### %s" % v1) not in history:
            errors.append("TEMPLATE_GUIDE.md 변경 이력에 현재 판이 없습니다: %s" % v1)
        else:
            notes.append("변경 이력에 현재 판 있음: %s" % v1)


def main() -> int:
    if not (ROOT / "AGENTS.md").is_file():
        sys.stderr.write(
            "저장소 루트에서 AGENTS.md를 찾지 못했습니다: %s\n"
            "check-docs.py는 저장소의 scripts/ 아래에 두고 실행하세요.\n" % ROOT
        )
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
        sys.stderr.write("실패:\n")
        for line in errors:
            sys.stderr.write(line + "\n")
        return 1
    sys.stdout.write("모든 검사 통과\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
