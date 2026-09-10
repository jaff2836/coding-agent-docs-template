from __future__ import annotations

import contextlib
import importlib.util
import io
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


def write(root: Path, relative_path: str, content: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def combined_form_source() -> Path:
    materialized = REPOSITORY_ROOT / "docs/changes/_template/01-CHANGE.md"
    if materialized.is_file():
        return materialized
    return (
        REPOSITORY_ROOT.parents[1]
        / "locales/en/docs/changes/_template/01-CHANGE.md"
    )


def write_minimal_artifact(root: Path) -> None:
    write(root, "AGENTS.md", "# Project\n")
    write(root, "CLAUDE.md", "@AGENTS.md\n")
    write(
        root,
        "docs/DOCS_GUIDE.md",
        "# Documentation Guide\n\n- **Template version:** 1.0.0\n",
    )
    write(root, ".agents/skills/design/SKILL.md", "# Design\n")
    write(root, ".agents/skills/review-round/SKILL.md", "# Review\n")
    write(
        root,
        ".agents/skills/review-round/agents/openai.yaml",
        "policy:\n  allow_implicit_invocation: false\n",
    )


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

    def test_links_imports_and_section_targets_cannot_escape_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "artifact"
            outside = parent / "OUTSIDE.md"
            outside.write_text("# Outside\n## 1. Existing\n", encoding="utf-8")
            write(root, "docs/SOURCE.md", "[outside](../../OUTSIDE.md) §1\n")
            write(root, ".omp/WATCHDOG.md", "@../../OUTSIDE.md\n")

            link_errors = []
            import_errors = []
            section_errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(link_errors, [])
                CHECK_DOCS.check_imports(import_errors, [])
                CHECK_DOCS.check_section_refs(section_errors, [])

            self.assertIn("escapes artifact root", "\n".join(link_errors))
            self.assertIn("escapes artifact root", "\n".join(import_errors))
            self.assertIn("document target does not exist", "\n".join(section_errors))

    def test_named_section_target_cannot_be_an_external_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "artifact"
            outside = parent / "OUTSIDE.md"
            outside.write_text("# Outside\n## 1. Existing\n", encoding="utf-8")
            write(root, "docs/SOURCE.md", "PROJECT §1\n")
            project = root / "docs/00-PROJECT.md"
            try:
                project.symlink_to(outside)
            except OSError as error:
                self.skipTest("symlinks unavailable: %s" % error)

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])

            self.assertIn("escapes artifact root", "\n".join(errors))

    def test_invariant_continuation_lines_are_compared_across_locales(self) -> None:
        source = """# Review
## 6. Any translated heading
<!-- template-section:project-invariants -->

<!-- template-example:project-invariant -->
- **Example:** ignored
- **Rule:** shared first line
  source-only continuation
"""
        copy = """# Bugbot
## 완전히 다른 제목
<!-- template-section:project-invariants -->

- **Rule:** shared first line
  different continuation
"""
        self.assertNotEqual(
            CHECK_DOCS.section_bullets(
                source,
                CHECK_DOCS.PROJECT_INVARIANTS_MARKER,
                CHECK_DOCS.PROJECT_INVARIANT_EXAMPLE_MARKER,
            ),
            CHECK_DOCS.section_bullets(
                copy, CHECK_DOCS.PROJECT_INVARIANTS_MARKER
            ),
        )

    def test_example_is_omitted_only_while_marker_labels_an_example(self) -> None:
        without_example_marker = """# Review
## Invariants
<!-- template-section:project-invariants -->

- **First real invariant**
- **Second real invariant**
"""
        copy = """# Bugbot
## Invariants
<!-- template-section:project-invariants -->

- **Second real invariant**
"""
        source_bullets = CHECK_DOCS.section_bullets(
            without_example_marker,
            CHECK_DOCS.PROJECT_INVARIANTS_MARKER,
            CHECK_DOCS.PROJECT_INVARIANT_EXAMPLE_MARKER,
        )
        copy_bullets = CHECK_DOCS.section_bullets(
            copy, CHECK_DOCS.PROJECT_INVARIANTS_MARKER
        )
        self.assertNotEqual(source_bullets, copy_bullets)
        self.assertEqual(source_bullets[0], "- **First real invariant**")

        with_example_marker = without_example_marker.replace(
            "- **First real invariant**",
            "<!-- template-example:project-invariant -->\n"
            "- **Example:** template-only rule",
        )
        self.assertEqual(
            CHECK_DOCS.section_bullets(
                with_example_marker,
                CHECK_DOCS.PROJECT_INVARIANTS_MARKER,
                CHECK_DOCS.PROJECT_INVARIANT_EXAMPLE_MARKER,
            ),
            copy_bullets,
        )

        marker_before_real_rule = without_example_marker.replace(
            "- **First real invariant**",
            "<!-- template-example:project-invariant -->\n"
            "- **First real invariant**",
        )
        with self.assertRaises(ValueError):
            CHECK_DOCS.section_bullets(
                marker_before_real_rule,
                CHECK_DOCS.PROJECT_INVARIANTS_MARKER,
                CHECK_DOCS.PROJECT_INVARIANT_EXAMPLE_MARKER,
            )

    def test_section_markers_must_exist_once_and_follow_the_heading(self) -> None:
        missing = """# Review
## Invariants
- **Rule**
"""
        misplaced = """# Review
## Invariants
Translated guidance
<!-- template-section:project-invariants -->
- **Rule**
"""
        duplicate = """# Review
## Invariants
<!-- template-section:project-invariants -->
<!-- template-section:project-invariants -->
- **Rule**
"""
        for text in (missing, misplaced, duplicate):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    CHECK_DOCS.section_bullets(
                        text, CHECK_DOCS.PROJECT_INVARIANTS_MARKER
                    )

    def test_example_marker_must_precede_a_top_level_bullet(self) -> None:
        misplaced = """# Review
## Invariants
<!-- template-section:project-invariants -->

<!-- template-example:project-invariant -->
Translated guidance
- **Rule**
"""
        with self.assertRaises(ValueError):
            CHECK_DOCS.section_bullets(
                misplaced,
                CHECK_DOCS.PROJECT_INVARIANTS_MARKER,
                CHECK_DOCS.PROJECT_INVARIANT_EXAMPLE_MARKER,
            )

    def test_numbered_headings_ignore_fenced_and_commented_decoys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TARGET.md"
            path.write_text(
                "# Target\n"
                "## 1. Visible\n"
                "```text\n## 2. Fenced decoy\n```\n"
                "<!--\n## 3. Commented decoy\n-->\n",
                encoding="utf-8",
            )

            self.assertEqual(CHECK_DOCS.numbered_headings(path), {"1"})

    def test_release_history_marker_controls_section_reference_cutoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            guide = """# Guide
## 1. Current guidance

## 2. Localized history heading
<!-- template-section:release-history -->

`docs/REMOVED.md` §99
"""
            write(root, "docs/TEMPLATE_GUIDE.md", guide)

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])
            self.assertEqual(errors, [])

            for invalid in (
                guide.replace("<!-- template-section:release-history -->\n", ""),
                guide.replace(
                    "<!-- template-section:release-history -->",
                    "translated guidance\n<!-- template-section:release-history -->",
                ),
            ):
                write(root, "docs/TEMPLATE_GUIDE.md", invalid)
                errors = []
                with patch.object(CHECK_DOCS, "ROOT", root):
                    CHECK_DOCS.check_section_refs(errors, [])
                self.assertTrue(errors)
                self.assertIn("template-section:release-history", "\n".join(errors))

    def test_current_version_heading_must_be_inside_marked_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/DOCS_GUIDE.md",
                "# Docs\n\n- **Template version:** 1.2.3\n",
            )
            write(
                root,
                "docs/TEMPLATE_GUIDE.md",
                "# Guide\n\n"
                "- **Template version:** 1.2.3\n\n"
                "### v1.2.3 — unrelated heading\n\n"
                "## History\n"
                "<!-- template-section:release-history -->\n\n"
                "### v1.2.30 — prefix collision\n"
                "### v1.2.2 — previous release\n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_versions(errors, [])

            self.assertIn(
                "Current version is absent from TEMPLATE_GUIDE.md history: 1.2.3",
                errors,
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
            self.assertIn("document target does not exist", "\n".join(errors))

    def test_combined_form_can_be_copied_without_optional_siblings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            change = docs / "changes/example"
            change.mkdir(parents=True)
            for name in ("00-PROJECT.md", "01-DESIGN.md", "02-TODO.md"):
                (docs / name).write_text("# Placeholder\n", encoding="utf-8")
            (change / "01-CHANGE.md").write_text(
                combined_form_source().read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            self.assertEqual(errors, [])

    def test_main_accepts_an_arbitrary_materialized_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "build" / "artifact"
            write_minimal_artifact(root)

            previous_root = CHECK_DOCS.ROOT
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = CHECK_DOCS.main(["--root", str(root)])

            self.assertEqual(result, 0, stderr.getvalue())
            self.assertIn("All checks passed", stdout.getvalue())
            self.assertEqual(CHECK_DOCS.ROOT, previous_root)

    def test_internal_source_exclusions_are_top_level_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_minimal_artifact(root)
            write(root, "locales/en/BROKEN.md", "[missing](./missing.txt)\n")
            write(root, "template/common/BROKEN.md", "[missing](./missing.txt)\n")
            write(root, "docs/locales/BROKEN.md", "[missing](./missing.txt)\n")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = CHECK_DOCS.run_checks(
                    root, excluded_top_level=("locales", "template")
                )
            self.assertEqual(result, 1)
            self.assertIn("docs/locales/BROKEN.md", stderr.getvalue())
            self.assertNotIn("locales/en/BROKEN.md", stderr.getvalue())
            self.assertNotIn("template/common/BROKEN.md", stderr.getvalue())

            (root / "docs/locales/BROKEN.md").unlink()
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = CHECK_DOCS.run_checks(
                    root, excluded_top_level=("locales", "template")
                )
            self.assertEqual(result, 0, stderr.getvalue())

            stderr = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
                stderr
            ):
                result = CHECK_DOCS.main(["--root", str(root)])
            self.assertEqual(result, 1)
            self.assertIn("locales/en/BROKEN.md", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
