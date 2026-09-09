from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_docs", REPOSITORY_ROOT / "scripts" / "check-docs.py"
)
assert SPEC is not None and SPEC.loader is not None
CHECK_DOCS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_DOCS)


class CheckDocsTests(unittest.TestCase):
    def test_codex_policy_must_be_boolean_false(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / ".agents/skills/review-round/SKILL.md"
            config = root / ".agents/skills/review-round/agents/openai.yaml"
            config.parent.mkdir(parents=True)
            skill.write_text("skill", encoding="utf-8")

            for value in ("true", '"false"', "missing"):
                if value == "missing":
                    config.write_text("policy: {}\n", encoding="utf-8")
                else:
                    config.write_text(
                        "policy:\n  allow_implicit_invocation: %s\n" % value,
                        encoding="utf-8",
                    )
                errors = []
                with patch.object(CHECK_DOCS, "ROOT", root):
                    CHECK_DOCS.check_skill_configs(errors, [])
                self.assertTrue(errors, value)

            config.write_text(
                "policy:\n  allow_implicit_invocation: false\n", encoding="utf-8"
            )
            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_skill_configs(errors, [])
            self.assertEqual(errors, [])

    def test_checkout_parent_named_build_does_not_skip_docs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "build" / "repository"
            document = root / "docs/BROKEN.md"
            document.parent.mkdir(parents=True)
            document.write_text("[missing](./missing.txt)\n", encoding="utf-8")

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            self.assertTrue(errors)

    def test_invariant_continuation_lines_are_compared(self) -> None:
        source = """# Review
## 6. Project-specific Invariants
- **Rule:** shared first line
  source-only continuation
"""
        copy = """# Bugbot
## 불변조건
- **Rule:** shared first line
  different continuation
"""
        self.assertNotEqual(
            CHECK_DOCS.section_bullets(source, "Project-specific Invariants"),
            CHECK_DOCS.section_bullets(copy, "불변조건"),
        )

    def test_deep_section_reference_is_not_truncated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "TARGET.md").write_text(
                "# Target\n## 1.2 Existing\n", encoding="utf-8"
            )
            (docs / "SOURCE.md").write_text(
                "[target](./TARGET.md) §1.2.99\n", encoding="utf-8"
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])
            self.assertTrue(errors)
            self.assertIn("§1.2.99", "\n".join(errors))

    def test_missing_explicit_section_path_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "SOURCE.md").write_text(
                "`docs/MISSING.md` §9\n", encoding="utf-8"
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])
            self.assertTrue(errors)
            self.assertIn("문서 대상이 없습니다", "\n".join(errors))

    def test_combined_form_can_be_copied_without_optional_siblings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            change = docs / "changes/example"
            change.mkdir(parents=True)
            for name in ("00-PROJECT.md", "01-DESIGN.md", "02-TODO.md"):
                (docs / name).write_text("# Placeholder\n", encoding="utf-8")
            (change / "01-CHANGE.md").write_text(
                (REPOSITORY_ROOT / "docs/changes/_template/01-CHANGE.md").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
