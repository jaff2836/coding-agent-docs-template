#!/usr/bin/env python3
"""문서 템플릿의 의존성 없는 검사.

상대 Markdown 링크, 스킬 사본, 알려진 @import, 안내 문서의 Template version을
확인합니다. 하나라도 실패하면 종료 코드 1입니다. 저장소 루트 기준이며 cwd는
달라도 됩니다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIR_NAMES = {".git", "node_modules", ".venv", "venv", "__pycache__"}

LINK_RE = re.compile(r"\]\(((?!https?://)[^)\s#]+?\.md)(?:#[^)]*)?\)")
VERSION_RE = re.compile(
    r"^\s*-\s*\*\*Template version:\*\*\s*(\S+)", re.MULTILINE
)
IMPORT_LINE_RE = re.compile(r"^@([^\s]+)\s*$")

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
    for md in md_files():
        scanned += 1
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            dest = (md.parent / target)
            if not dest.is_file():
                broken.append("%s: %s" % (rel(md), target))
    if broken:
        errors.append("깨진 상대 링크:")
        errors.extend("  %s" % item for item in broken)
    else:
        notes.append("상대 링크: %d개 파일, 깨진 링크 없음" % scanned)


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


def check_imports(errors: List[str], notes: List[str]) -> None:
    claude = ROOT / "CLAUDE.md"
    if not claude.is_file():
        errors.append("CLAUDE.md가 없습니다")
    else:
        body = claude.read_text(encoding="utf-8").strip()
        if body != "@AGENTS.md":
            errors.append("CLAUDE.md import가 @AGENTS.md가 아닙니다: %r" % body)
        elif not (ROOT / "AGENTS.md").is_file():
            errors.append("CLAUDE.md가 가리키는 AGENTS.md가 없습니다")
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


def read_template_version(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    match = VERSION_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def check_versions(errors: List[str], notes: List[str]) -> None:
    guide = ROOT / "docs" / "TEMPLATE_GUIDE.md"
    docs_guide = ROOT / "docs" / "DOCS_GUIDE.md"
    v1 = read_template_version(guide)
    v2 = read_template_version(docs_guide)
    if v1 is None:
        errors.append("docs/TEMPLATE_GUIDE.md에서 Template version을 찾지 못했습니다")
    if v2 is None:
        errors.append("docs/DOCS_GUIDE.md에서 Template version을 찾지 못했습니다")
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
    if not (ROOT / "docs" / "TEMPLATE_GUIDE.md").is_file():
        sys.stderr.write("저장소 루트를 찾지 못했습니다\n")
        return 2
    errors: List[str] = []
    notes: List[str] = []
    check_relative_links(errors, notes)
    check_skill_copies(errors, notes)
    check_imports(errors, notes)
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
