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
    write(root, ".agents/skills/project-analysis/SKILL.md", "# Analysis\n")
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

            for duplicate in (
                "policy:\n"
                "  allow_implicit_invocation: false\n"
                "  allow_implicit_invocation: invalid\n",
                "policy:\n"
                "  allow_implicit_invocation: false\n"
                "  allow_implicit_invocation: false\n",
            ):
                config.write_text(duplicate, encoding="utf-8")
                errors = []
                with patch.object(CHECK_DOCS, "ROOT", root):
                    CHECK_DOCS.check_skill_configs(errors, [])
                self.assertTrue(errors, duplicate)

    def test_watchdog_must_import_exactly_the_canonical_review_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "AGENTS.md", "# Project\n")
            write(root, "CLAUDE.md", "@AGENTS.md\n")
            write(root, "README.md", "# Readme\n")
            write(root, "docs/REVIEW.md", "# Review\n")

            for body in (
                "@../README.md\n",
                "@../docs/REVIEW.md\n@../README.md\n",
                "@../docs/REVIEW.md\n@../docs/REVIEW.md\n",
            ):
                write(root, ".omp/WATCHDOG.md", body)
                errors = []
                with patch.object(CHECK_DOCS, "ROOT", root):
                    CHECK_DOCS.check_imports(errors, [])
                self.assertIn("must import exactly", "\n".join(errors), body)

            write(root, ".omp/WATCHDOG.md", "@../docs/REVIEW.md\n")
            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_imports(errors, [])
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

    def test_artifact_root_agents_file_cannot_be_an_external_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "artifact"
            root.mkdir()
            outside = parent / "AGENTS.md"
            outside.write_text("# External instructions\n", encoding="utf-8")
            try:
                (root / "AGENTS.md").symlink_to(outside)
            except OSError as error:
                self.skipTest("symlinks unavailable: %s" % error)

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = CHECK_DOCS.run_checks(root)
            self.assertEqual(result, 2)
            self.assertIn("AGENTS.md was not found", stderr.getvalue())

    def test_optional_skill_copy_cannot_be_an_external_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "artifact"
            outside = parent / "SKILL.md"
            write(root, ".agents/skills/design/SKILL.md", "# Design\n")
            outside.write_text("# Design\n", encoding="utf-8")
            copy = root / ".claude/skills/design/SKILL.md"
            copy.parent.mkdir(parents=True)
            try:
                copy.symlink_to(outside)
            except OSError as error:
                self.skipTest("symlinks unavailable: %s" % error)

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root), patch.object(
                CHECK_DOCS,
                "SKILL_PAIRS",
                [
                    (
                        ".agents/skills/design/SKILL.md",
                        ".claude/skills/design/SKILL.md",
                    )
                ],
            ):
                CHECK_DOCS.check_skill_copies(errors, [])
            self.assertIn("escapes artifact root", "\n".join(errors))

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

    def test_markdown_directory_cannot_be_an_external_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "artifact"
            outside = parent / "handbook"
            outside.mkdir()
            write(outside, "BROKEN.md", "[missing](./MISSING.md)\n")
            root.mkdir()
            try:
                (root / "handbook").symlink_to(outside, target_is_directory=True)
            except OSError as error:
                self.skipTest("symlinks unavailable: %s" % error)

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            self.assertIn("Markdown directory escapes artifact root", "\n".join(errors))

    def test_markdown_file_cannot_be_an_external_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "artifact"
            outside = parent / "OUTSIDE.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            link = root / ".omp/WATCHDOG.md"
            link.parent.mkdir(parents=True)
            try:
                link.symlink_to(outside)
            except OSError as error:
                self.skipTest("symlinks unavailable: %s" % error)

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])

            self.assertIn("Markdown source escapes artifact root", "\n".join(errors))

    def test_markdown_path_must_be_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "not-a-file.md").mkdir()

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])

            self.assertIn("Markdown source is not a file: not-a-file.md", errors)

    def test_skipped_directories_are_pruned_before_descent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/README.md", "# Docs\n")

            def fake_walk(path: Path, *, topdown: bool, followlinks: bool):
                self.assertEqual(path, root)
                self.assertTrue(topdown)
                self.assertFalse(followlinks)
                child_directories = ["node_modules", "docs"]
                yield root, child_directories, []
                self.assertEqual(child_directories, ["docs"])
                yield root / "docs", [], ["README.md"]

            with patch.object(CHECK_DOCS, "ROOT", root), patch.object(
                CHECK_DOCS.os, "walk", side_effect=fake_walk
            ):
                files = CHECK_DOCS.md_files([])

            self.assertEqual(files, [root / "docs/README.md"])

    def test_malformed_external_uri_does_not_crash_link_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "README.md", "[external](http://[invalid)\n")

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])

            self.assertEqual(errors, [])

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

    def test_indented_code_bullet_is_not_a_top_level_invariant(self) -> None:
        text = """# Review
## Invariants
<!-- template-section:project-invariants -->

    - **Code example:** not an invariant
 - **Rule A:** first invariant
 - **Rule B:** second invariant
- **Rule C:** shallower invariant
"""
        self.assertEqual(
            CHECK_DOCS.section_bullets(
                text, CHECK_DOCS.PROJECT_INVARIANTS_MARKER
            ),
            [
                "- **Rule A:** first invariant",
                "- **Rule B:** second invariant",
                "- **Rule C:** shallower invariant",
            ],
        )

    def test_markdown_line_context_recognizes_blockquote_fences(self) -> None:
        text = (
            "> ```markdown\n"
            "> [decoy](./TARGET.md)\n"
            "> ```\n"
            "Visible prose\n"
        )
        self.assertEqual(
            CHECK_DOCS.markdown_line_context(text),
            ((False, False), (False, False), (False, False), (True, True)),
        )

        root_fence = (
            "```markdown\n"
            "> ```\n"
            "[decoy](./TARGET.md)\n"
            "```\n"
            "Visible prose\n"
        )
        self.assertEqual(
            CHECK_DOCS.markdown_line_context(root_fence),
            (
                (False, False),
                (False, False),
                (False, False),
                (False, False),
                (True, True),
            ),
        )

        unclosed_quote_fence = "> ```markdown\n> decoy\nVisible prose\n"
        self.assertEqual(
            CHECK_DOCS.markdown_line_context(unclosed_quote_fence),
            ((False, False), (False, False), (True, True)),
        )

        fence_inside_comment = (
            "<!--\n"
            "```markdown\n"
            "## 99. Commented decoy\n"
            "-->\n"
            "## 1. Visible heading\n"
        )
        self.assertEqual(
            CHECK_DOCS.markdown_line_context(fence_inside_comment),
            (
                (True, True),
                (True, False),
                (True, False),
                (True, False),
                (True, True),
            ),
        )

    def test_inline_code_comment_delimiter_does_not_mask_following_prose(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/SOURCE.md",
                "`<!--` is an inline-code example.\n"
                "[missing](./MISSING.md)\n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            self.assertIn("MISSING.md", "\n".join(errors))

    def test_list_relative_fence_masks_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/SOURCE.md",
                "- outer\n"
                "  - inner\n"
                "    ~~~markdown\n"
                "    [example](./MISSING.md)\n"
                "    ~~~\n",
            )

            errors = []
            notes = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, notes)
            self.assertEqual(errors, [])
            self.assertIn("checked 0 links", "\n".join(notes))

    def test_relative_links_ignore_non_prose_and_all_uri_schemes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/TARGET.md", "# Target\n")
            write(root, "docs/user guide.md", "# Guide\n")
            write(root, "docs/paren(guide).md", "# Parenthesized guide\n")
            write(
                root,
                "docs/SOURCE.md",
                "[target](./TARGET.md#manual-anchor)\n"
                "[angle](<./user guide.md>)\n"
                "[escaped-space](./user\\ guide.md)\n"
                "[parentheses](./paren(guide).md)\n"
                "[escaped-parentheses](./paren\\(guide\\).md)\n"
                "```markdown\n[fenced](./FENCED.md)\n```\n"
                "<!-- [commented](./COMMENTED.md) -->\n"
                "<!--\n[multiline](./MULTILINE.md)\n-->\n"
                "`[inline-code](./INLINE.md)`\n"
                "[upper](HTTPS://example.com/file.md)\n"
                "[ftp](ftp://example.com/file.md)\n"
                "[tel](tel:+12025550123)\n"
                "[protocol-relative](//example.com/file.md)\n"
                "\n"
                "    [indented-code](./INDENTED.md)\n"
                "\n"
                "- list item\n"
                "\n"
                "      [list-code](./LIST-CODE.md)\n",
            )

            errors = []
            notes = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, notes)
            self.assertEqual(errors, [])
            self.assertIn("checked 5 links", "\n".join(notes))

    def test_relative_link_with_optional_title_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/SOURCE.md", '[guide](./MISSING.md "Guide")\n')

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            self.assertIn("MISSING.md", "\n".join(errors))

    def test_plain_text_link_fragments_are_not_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "README.md",
                "suffix](./MISSING.md)\n\\](./ALSO-MISSING.md)\n",
            )

            errors = []
            notes = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, notes)

            self.assertEqual(errors, [])
            self.assertIn("checked 0 links", "\n".join(notes))

    def test_reference_style_relative_link_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/SOURCE.md",
                "[guide][api]\n\n[api]: ./MISSING.md \"Guide\"\n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            self.assertIn("MISSING.md", "\n".join(errors))

    def test_reference_style_section_link_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/TARGET.md", "# Target\n## 1. Existing\n")

            for link in ("[policy][target]", "[target][]", "[target]"):
                write(
                    root,
                    "docs/SOURCE.md",
                    "%s §9\n\n[target]: ./TARGET.md\n" % link,
                )
                errors = []
                with patch.object(CHECK_DOCS, "ROOT", root):
                    CHECK_DOCS.check_section_refs(errors, [])
                self.assertIn("section does not exist", "\n".join(errors), link)

    def test_section_suffix_does_not_cross_paragraphs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/TARGET.md", "# Target\n## 1. Existing\n")
            write(
                root,
                "docs/SOURCE.md",
                "[policy](./TARGET.md)\n\n§9\n"
                "`./TARGET.md`\n\n§9\n"
                "TARGET.md\n\n§9\n"
                "TARGET\n\n§9\n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])

            self.assertEqual(errors, [])

    def test_section_references_ignore_fenced_and_commented_decoys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/TARGET.md", "# Target\n## 1. Existing\n")
            write(
                root,
                "docs/SOURCE.md",
                "TARGET §1\n"
                "```markdown\nTARGET §99\n```\n"
                "<!-- TARGET §98 -->\n"
                "<!--\nTARGET §97\n-->\n"
                "`TARGET §96`\n"
                "\n"
                "    MISSING.md §95\n"
                "\n"
                "- list item\n"
                "\n"
                "      MISSING.md §94\n",
            )

            errors = []
            notes = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, notes)
            self.assertEqual(errors, [])
            self.assertIn("checked 1", "\n".join(notes))

    def test_section_link_with_optional_title_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/TARGET.md", "# Target\n## 1. Existing\n")
            write(
                root,
                "docs/SOURCE.md",
                '[policy](./TARGET.md "Guide") §9\n',
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])
            self.assertIn("section does not exist", "\n".join(errors))

    def test_numbered_headings_ignore_fenced_and_commented_decoys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TARGET.md"
            path.write_text(
                "# Target\n"
                "## 1. Visible\n"
                "  ## 4. Indented visible\n"
                "```text\n## 2. Fenced decoy\n```\n"
                "<!--\n## 3. Commented decoy\n-->\n",
                encoding="utf-8",
            )

            self.assertEqual(CHECK_DOCS.numbered_headings(path), {"1", "4"})

    def test_all_unordered_list_markers_are_invariant_bullets(self) -> None:
        source = """# Review
## 6. Invariants
<!-- template-section:project-invariants -->

* **Rule A:** source
"""
        copy = """# Bugbot
## Invariants
<!-- template-section:project-invariants -->

+ **Rule B:** copy
"""
        source_bullets = CHECK_DOCS.section_bullets(
            source, CHECK_DOCS.PROJECT_INVARIANTS_MARKER
        )
        copy_bullets = CHECK_DOCS.section_bullets(
            copy, CHECK_DOCS.PROJECT_INVARIANTS_MARKER
        )
        self.assertEqual(source_bullets, ["* **Rule A:** source"])
        self.assertEqual(copy_bullets, ["+ **Rule B:** copy"])
        self.assertNotEqual(source_bullets, copy_bullets)

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
                "```markdown\n### v1.2.3 — fenced decoy\n```\n"
                "<!-- ### v1.2.3 — commented decoy -->\n"
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

    def test_template_version_ignores_fenced_and_commented_decoys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "DOC.md"
            path.write_text(
                "# Guide\n"
                "```markdown\n- **Template version:** 9.9.9\n```\n"
                "<!-- - **Template version:** 9.9.9 -->\n",
                encoding="utf-8",
            )
            with patch.object(CHECK_DOCS, "ROOT", root):
                self.assertIsNone(CHECK_DOCS.read_template_version(path))

    def test_duplicate_template_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/DOCS_GUIDE.md",
                "# Guide\n"
                "- **Template version:** 1.0.0\n"
                "- **Template version:** 0.9.0\n",
            )
            write(
                root,
                "docs/TEMPLATE_GUIDE.md",
                "# Template\n"
                "- **Template version:** 1.0.0\n\n"
                "## History\n"
                "<!-- template-section:release-history -->\n\n"
                "### v1.0.0\n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_versions(errors, [])
            self.assertIn("exactly once", "\n".join(errors))

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
            self.assertEqual(
                "\n".join(errors).count("document target does not exist"), 1
            )

    def test_missing_explicit_section_name_with_md_suffix_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/SOURCE.md", "MISSING.md §9\n")

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])
            self.assertIn("document target does not exist", "\n".join(errors))

    def test_explicit_section_filename_accepts_case_and_hyphens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for filename in ("security-policy.md", "SECURITY-POLICY.md"):
                write(root, "docs/SOURCE.md", "%s §9\n" % filename)
                errors = []
                with patch.object(CHECK_DOCS, "ROOT", root):
                    CHECK_DOCS.check_section_refs(errors, [])
                self.assertIn(
                    "document target does not exist", "\n".join(errors), filename
                )

    def test_inline_link_parts_may_follow_one_line_break(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/SOURCE.md",
                "[destination](\n./MISSING-DESTINATION.md)\n\n"
                "[title](./MISSING-TITLE.md\n\"Title\")\n\n"
                "[split title](./MISSING-SPLIT.md \"First\nsecond\")\n\n"
                "[paragraph](\n\n./NOT-A-LINK.md)\n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            report = "\n".join(errors)
            self.assertIn("MISSING-DESTINATION.md", report)
            self.assertIn("MISSING-TITLE.md", report)
            self.assertIn("MISSING-SPLIT.md", report)
            self.assertNotIn("NOT-A-LINK.md", report)

    def test_root_relative_urls_are_not_file_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/SOURCE.md",
                "[site](/docs/start)\n[absolute](/MISSING.md)\n",
            )

            errors = []
            notes = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, notes)
            self.assertEqual(errors, [])
            self.assertIn("checked 0 links", "\n".join(notes))

    def test_raw_html_blocks_are_not_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/SOURCE.md",
                "<pre>\n[pre](./MISSING-PRE.md)\n\n[still pre](./MISSING-PRE-2.md)\n</pre>\n"
                "<SCRIPT type=\"text/plain\">[script](./MISSING-SCRIPT.md)</script>\n"
                "[after raw](./MISSING-AFTER-RAW.md)\n\n"
                "<div>\n[div](./MISSING-DIV.md)\n\n"
                "[after block](./MISSING-AFTER-BLOCK.md)\n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            report = "\n".join(errors)
            for hidden in ("PRE.md", "PRE-2.md", "SCRIPT.md", "DIV.md"):
                self.assertNotIn("MISSING-" + hidden, report)
            self.assertIn("MISSING-AFTER-RAW.md", report)
            self.assertIn("MISSING-AFTER-BLOCK.md", report)

    def test_reference_definition_allows_only_an_optional_title(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "docs/SOURCE.md",
                "[prose]: ./NOT-A-DEFINITION.md trailing prose\n"
                "[glued]: <./NOT-A-DEFINITION-2.md>trailing\n"
                "[title]: ./MISSING-TITLE.md \"Title\"\n"
                "[angle]: <./MISSING-ANGLE.md> 'Title'\n"
                "[paren]: ./MISSING-PAREN.md (Title)  \n",
            )

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_relative_links(errors, [])
            report = "\n".join(errors)
            self.assertNotIn("NOT-A-DEFINITION", report)
            for missing in ("MISSING-TITLE.md", "MISSING-ANGLE.md", "MISSING-PAREN.md"):
                self.assertIn(missing, report)

    def test_template_version_compares_complete_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            history = (
                "## History\n"
                "<!-- template-section:release-history -->\n\n"
                "### %s — pending changes\n"
            )
            write(
                root,
                "docs/DOCS_GUIDE.md",
                "# Docs\n\n- **Template version:** 미릴리스 (tag 없음)\n",
            )
            write(
                root,
                "docs/TEMPLATE_GUIDE.md",
                "# Guide\n\n- **Template version:** 미릴리스 (최근 tag: v1.2)\n\n"
                + history % "미릴리스 (최근 tag: v1.2)",
            )
            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_versions(errors, [])
            self.assertIn("Template versions differ", "\n".join(errors))

            for value, heading in (
                ("미릴리스 (최근 tag: v1.2)", "미릴리스 (최근 tag: v1.2)"),
                ("Unreleased (latest tag: v1.2)", "Unreleased (Latest Tag: v1.2)"),
            ):
                write(
                    root,
                    "docs/DOCS_GUIDE.md",
                    "# Docs\n\n- **Template version:** %s\n" % value,
                )
                write(
                    root,
                    "docs/TEMPLATE_GUIDE.md",
                    "# Guide\n\n- **Template version:** %s\n\n" % value
                    + history % heading,
                )
                errors = []
                notes = []
                with patch.object(CHECK_DOCS, "ROOT", root):
                    CHECK_DOCS.check_versions(errors, notes)
                self.assertEqual(errors, [], value)
                self.assertIn("Template versions match: %s" % value, notes)

    def test_ambiguous_document_short_name_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "docs/00-POLICY.md", "# Policy\n## 9. Numbered\n")
            write(root, "docs/POLICY.md", "# Policy\n## 1. Plain\n")
            write(root, "docs/SOURCE.md", "POLICY §9\n")

            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])
            self.assertIn("ambiguous document name", "\n".join(errors))

            write(root, "docs/SOURCE.md", "`docs/00-POLICY.md` §9\n00-POLICY.md §9\n")
            errors = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_section_refs(errors, [])
            self.assertEqual(errors, [])

    def test_optional_contract_files_cannot_escape_or_be_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            write(root, "AGENTS.md", "# Project\n")
            write(root, "CLAUDE.md", "@AGENTS.md\n")
            write(root, "docs/REVIEW.md", "# Review\n")
            external = Path(outside) / "external.md"
            external.write_text("@../docs/REVIEW.md\n", encoding="utf-8")

            (root / ".omp").mkdir()
            (root / ".omp/WATCHDOG.md").symlink_to(external)
            (root / ".cursor").mkdir()
            (root / ".cursor/BUGBOT.md").symlink_to(external)
            errors = []
            notes = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_imports(errors, notes)
                CHECK_DOCS.check_invariants(errors, notes)
            report = "\n".join(errors)
            self.assertIn(".omp/WATCHDOG.md escapes artifact root", report)
            self.assertIn(".cursor/BUGBOT.md escapes artifact root", report)
            self.assertNotIn("omitted", "\n".join(notes))

            (root / ".omp/WATCHDOG.md").unlink()
            (root / ".omp/WATCHDOG.md").mkdir()
            (root / ".cursor/BUGBOT.md").unlink()
            errors = []
            notes = []
            with patch.object(CHECK_DOCS, "ROOT", root):
                CHECK_DOCS.check_imports(errors, notes)
                CHECK_DOCS.check_invariants(errors, notes)
            self.assertEqual(errors, [".omp/WATCHDOG.md is not a file"])
            self.assertIn("BUGBOT.md omitted (allowed)", notes)

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
