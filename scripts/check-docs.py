#!/usr/bin/env python3
"""Run the canonical artifact checker against the maintainer source tree.

The distributable checker lives under ``template/common``. A source checkout
also contains locale and common source directories that are not materialized
project documentation, so the no-argument maintainer command excludes those
two top-level trees from recursive Markdown discovery. Passing any CLI option
delegates unchanged to the artifact checker; in particular, ``--root`` checks
an arbitrary materialized artifact without maintainer exclusions.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Optional, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
COMMON_CHECKER = REPOSITORY_ROOT / "template/common/scripts/check-docs.py"

SPEC = importlib.util.spec_from_file_location("common_check_docs", COMMON_CHECKER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load canonical checker: %s" % COMMON_CHECKER)
CHECK_DOCS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_DOCS)


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments:
        CHECK_DOCS.HISTORY_PATH = "docs/TEMPLATE_GUIDE.md"
        return CHECK_DOCS.main(arguments)
    CHECK_DOCS.HISTORY_PATH = "CHANGELOG.md"
    return CHECK_DOCS.run_checks(
        REPOSITORY_ROOT,
        excluded_top_level=("locales", "template"),
    )


if __name__ == "__main__":
    sys.exit(main())
