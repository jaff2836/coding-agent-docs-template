from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COMMON_TESTS = load_module(
    "common_test_check_docs",
    REPOSITORY_ROOT / "template/common/tests/test_check_docs.py",
)
MAINTAINER_CHECKER = load_module(
    "maintainer_check_docs",
    REPOSITORY_ROOT / "scripts/check-docs.py",
)

# Re-export the canonical artifact suite so the documented maintainer test
# command exercises the exact checker and tests shipped in every artifact.
CheckDocsTests = COMMON_TESTS.CheckDocsTests


class MaintainerCheckDocsTests(unittest.TestCase):
    def test_no_arguments_check_source_tree_with_payload_exclusions(self) -> None:
        with patch.object(
            MAINTAINER_CHECKER.CHECK_DOCS, "run_checks", return_value=0
        ) as run_checks:
            self.assertEqual(MAINTAINER_CHECKER.main([]), 0)
        run_checks.assert_called_once_with(
            REPOSITORY_ROOT,
            excluded_top_level=("locales", "template"),
        )

    def test_explicit_arguments_use_artifact_cli_without_exclusions(self) -> None:
        arguments = ["--root", "/tmp/example-artifact"]
        with patch.object(
            MAINTAINER_CHECKER.CHECK_DOCS, "main", return_value=0
        ) as artifact_main:
            self.assertEqual(MAINTAINER_CHECKER.main(arguments), 0)
        artifact_main.assert_called_once_with(arguments)


if __name__ == "__main__":
    unittest.main()
