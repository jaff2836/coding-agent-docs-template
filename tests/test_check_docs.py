from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import subprocess
import tempfile
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


# Root copies of Korean payload files whose project-owned parts may differ.
ROOT_COPY_FIXTURES = {
    "docs/REVIEW.md": (
        "# Review\n\n## 6. Project-specific Invariants\n\n"
        "<!-- template-section:project-invariants -->\n\n"
        "- **Keep:** The fixture keeps this rule.\n\n"
        "## 9. Accepted Deferrals\n\n| ID | Scope |\n| --- | --- |\n\n"
        "## 10. Review Conclusion\n\nShared conclusion.\n"
    ),
    "docs/REVIEW_ROUND.md": (
        "# Round\n\n## 2. Parameters\n\n### 2.1 리뷰어 등록\n\n"
        "| 리뷰어 | 슬롯 |\n|---|---|\n\nShared text after the table.\n\n"
        "## 3. Steps\n\nShared steps.\n"
    ),
    ".cursor/BUGBOT.md": (
        "# Bugbot\n\n## 이 저장소의 불변조건\n\n"
        "<!-- template-section:project-invariants -->\n\n"
        "- **Keep:** The fixture keeps this rule.\n\n"
        "## 확정된 설계 결정과 승인된 deferral\n\n- 확정된 결정: none\n\n"
        "## Do Not Report\n\nShared list.\n"
    ),
}
README_FIXTURES = {
    "README.md": "| Locale | Language | Status |\n| --- | --- | --- |\n",
    "README.ko.md": "| Locale | 언어 | 상태 |\n| --- | --- | --- |\n",
}


class MaintainerCheckDocsTests(unittest.TestCase):
    def write_source(self, root: Path) -> None:
        COMMON_TESTS.write_minimal_artifact(root)
        for path in (
            ".claude/skills/project-analysis/SKILL.md",
            "locales/ko/.agents/skills/project-analysis/SKILL.md",
            "locales/ko/.claude/skills/project-analysis/SKILL.md",
        ):
            COMMON_TESTS.write(root, path, "# Analysis\n")
        COMMON_TESTS.write(
            root, "docs/TEMPLATE_GUIDE.md",
            "# Source Guide\n\n- **Template version:** 1.0.0\n",
        )
        COMMON_TESTS.write(
            root, "CHANGELOG.md",
            "# Releases\n\n<!-- template-section:release-history -->\n\n"
            "## v1.0.0 — unpublished candidate\n",
        )
        for path, content in ROOT_COPY_FIXTURES.items():
            COMMON_TESTS.write(root, path, content)
            COMMON_TESTS.write(root, "locales/ko/" + path, content)
        for path, header in README_FIXTURES.items():
            COMMON_TESTS.write(
                root, path,
                "# Template\n\n" + header
                + "| `en` | English | complete |\n| `ko` | Korean | complete |\n",
            )
        root.joinpath("locales/manifest.json").write_bytes(
            REPOSITORY_ROOT.joinpath("locales/manifest.json").read_bytes()
        )

    def edit(self, root: Path, path: str, old: str, new: str) -> None:
        target = root / path
        text = target.read_text(encoding="utf-8")
        self.assertEqual(text.count(old), 1, old)
        target.write_text(text.replace(old, new), encoding="utf-8")

    def run_wrapper(self, root: Path, arguments: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch.object(MAINTAINER_CHECKER, "REPOSITORY_ROOT", root),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = MAINTAINER_CHECKER.main(arguments)
        return result, stdout.getvalue(), stderr.getvalue()

    def test_no_arguments_check_source_tree_with_payload_exclusions(self) -> None:
        MAINTAINER_CHECKER.CHECK_DOCS.HISTORY_PATH = "unexpected.md"
        with patch.object(
            MAINTAINER_CHECKER.CHECK_DOCS, "run_checks", return_value=0
        ) as run_checks:
            self.assertEqual(MAINTAINER_CHECKER.main([]), 0)
        self.assertEqual(MAINTAINER_CHECKER.CHECK_DOCS.HISTORY_PATH, "CHANGELOG.md")
        run_checks.assert_called_once_with(
            REPOSITORY_ROOT,
            excluded_top_level=("locales", "template"),
        )

    def test_explicit_arguments_use_artifact_cli_without_exclusions(self) -> None:
        arguments = ["--root", "/tmp/example-artifact"]
        MAINTAINER_CHECKER.CHECK_DOCS.HISTORY_PATH = "CHANGELOG.md"
        with patch.object(
            MAINTAINER_CHECKER.CHECK_DOCS, "main", return_value=0
        ) as artifact_main:
            self.assertEqual(MAINTAINER_CHECKER.main(arguments), 0)
        self.assertEqual(
            MAINTAINER_CHECKER.CHECK_DOCS.HISTORY_PATH,
            "docs/TEMPLATE_GUIDE.md",
        )
        artifact_main.assert_called_once_with(arguments)

    def test_matching_analysis_copies_allow_other_source_skill_differences(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_source(root)
            for name in ("design", "review-round"):
                COMMON_TESTS.write(
                    root, "locales/ko/.agents/skills/%s/SKILL.md" % name,
                    "# Different locale contract\n",
                )
            result, stdout, stderr = self.run_wrapper(root, [])
            self.assertEqual(result, 0, stderr)
            self.assertIn("All checks passed", stdout)

    def test_analysis_pair_drift_is_rejected_even_when_each_pair_matches(self) -> None:
        for prefix in ("", "locales/ko/"):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_source(root)
                for adapter in (".agents", ".claude"):
                    COMMON_TESTS.write(
                        root, prefix + adapter + "/skills/project-analysis/SKILL.md",
                        "# Analysis\n\n## Metadata\n\n- **Owner:** Regression\n",
                    )
                result, stdout, stderr = self.run_wrapper(root, [])
                self.assertEqual(result, 1)
                self.assertIn("Source analysis skill copies differ", stderr)
                self.assertIn(".agents/skills/project-analysis/SKILL.md", stderr)
                self.assertIn("locales/ko/", stderr)
                self.assertNotIn("All checks passed", stdout)

    def test_missing_or_non_file_locale_analysis_copy_is_rejected(self) -> None:
        for state in ("missing", "directory"):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_source(root)
                path = root / "locales/ko/.agents/skills/project-analysis/SKILL.md"
                path.unlink()
                if state == "directory":
                    path.mkdir()
                result, stdout, stderr = self.run_wrapper(root, [])
                self.assertEqual(result, 1)
                self.assertIn("Cannot read source analysis skill locales/ko/", stderr)
                self.assertNotIn("All checks passed", stdout)

    def test_unreadable_locale_analysis_copy_reports_path_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_source(root)
            target = (
                root / "locales/ko/.agents/skills/project-analysis/SKILL.md"
            ).resolve()
            read_bytes = Path.read_bytes

            def read_with_denial(path: Path) -> bytes:
                if path == target:
                    raise PermissionError("fixture access denied")
                return read_bytes(path)

            with patch.object(Path, "read_bytes", read_with_denial):
                result, stdout, stderr = self.run_wrapper(root, [])
            self.assertEqual(result, 1)
            self.assertIn("locales/ko/.agents/skills/project-analysis/SKILL.md", stderr)
            self.assertIn("fixture access denied", stderr)
            self.assertNotIn("All checks passed", stdout)

    def test_external_locale_analysis_copy_is_rejected_even_with_matching_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory, \
                tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            self.write_source(root)
            external = Path(outside) / "SKILL.md"
            path = root / "locales/ko/.agents/skills/project-analysis/SKILL.md"
            external.write_bytes(path.read_bytes())
            path.unlink()
            COMMON_TESTS.CheckDocsTests.symlink_or_skip(self, path, external)
            result, stdout, stderr = self.run_wrapper(root, [])
            self.assertEqual(result, 1)
            self.assertIn("Cannot read source analysis skill locales/ko/", stderr)
            self.assertNotIn("All checks passed", stdout)

    @unittest.skipUnless(os.name == "nt", "native Windows junction required")
    def test_external_locale_analysis_directory_junction_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory, \
                tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            self.write_source(root)
            external = Path(outside)
            link = root / "locales/ko/.agents/skills/project-analysis"
            external.joinpath("SKILL.md").write_bytes(link.joinpath("SKILL.md").read_bytes())
            link.joinpath("SKILL.md").unlink()
            link.rmdir()
            subprocess.run(
                ["cmd.exe", "/c", "mklink", "/J", str(link), str(external)],
                check=True, capture_output=True, timeout=15,
            )
            try:
                self.assertTrue(link.is_junction())
                result, stdout, stderr = self.run_wrapper(root, [])
                self.assertEqual(result, 1)
                self.assertIn("Cannot read source analysis skill locales/ko/", stderr)
                self.assertNotIn("All checks passed", stdout)
            finally:
                os.rmdir(link)

    def test_root_copies_may_differ_only_in_project_owned_parts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_source(root)
            for path in ("docs/REVIEW.md", ".cursor/BUGBOT.md"):
                self.edit(
                    root, path, "- **Keep:** The fixture keeps this rule.\n",
                    "- **Keep:** The fixture keeps this rule.\n"
                    "- **Own:** The project adds this rule.\n",
                )
            self.edit(
                root, "docs/REVIEW.md", "| --- | --- |\n",
                "| --- | --- |\n| DFR-001 | Project deferral |\n",
            )
            self.edit(
                root, "docs/REVIEW_ROUND.md", "|---|---|\n",
                "|---|---|\n| Reviewer | `A` |\n",
            )
            self.edit(
                root, ".cursor/BUGBOT.md", "- 확정된 결정: none\n",
                "- 확정된 결정: D-001 — project decision\n",
            )
            result, stdout, stderr = self.run_wrapper(root, [])
            self.assertEqual(result, 0, stderr)
            self.assertIn("All checks passed", stdout)

    def test_root_copy_drift_outside_project_owned_parts_is_rejected(self) -> None:
        for path, old, new, line in (
            ("docs/REVIEW.md", "Shared conclusion.", "Drifted conclusion.", 16),
            ("docs/REVIEW_ROUND.md", "Shared text after the table.",
             "Drifted text after the table.", 10),
            ("docs/REVIEW_ROUND.md", "| 리뷰어 | 슬롯 |", "| 리뷰어 | 역할 |", 7),
            (".cursor/BUGBOT.md", "Shared list.\n", "Shared list.\n\nExtra.\n",
             16),
        ):
            with self.subTest(path=path, new=new), \
                    tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_source(root)
                self.edit(root, path, old, new)
                result, stdout, stderr = self.run_wrapper(root, [])
                self.assertEqual(result, 1)
                self.assertIn(
                    "Root copy %s differs from locales/ko/%s outside "
                    "project-owned sections at line %d" % (path, path, line),
                    stderr,
                )
                self.assertNotIn("All checks passed", stdout)

    def test_missing_project_owned_heading_is_rejected(self) -> None:
        for prefix in ("", "locales/ko/"):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_source(root)
                self.edit(
                    root, prefix + "docs/REVIEW_ROUND.md",
                    "### 2.1 리뷰어 등록", "### 2.1 Reviewers",
                )
                result, _, stderr = self.run_wrapper(root, [])
                self.assertEqual(result, 1)
                self.assertIn(
                    "%sdocs/REVIEW_ROUND.md: heading '### 2.1 리뷰어 등록' "
                    "must appear exactly once (found 0)" % prefix,
                    stderr,
                )

    def test_readme_locale_table_must_list_complete_manifest_locales(self) -> None:
        for path in README_FIXTURES:
            for old, new, message in (
                ("| `ko` |", "| `fr` |",
                 "%s:6: locale fr is not complete in locales/manifest.json"),
                ("| Korean | complete |", "| Korean | experimental |",
                 "%s:6: locale ko status must be complete, not experimental"),
            ):
                with self.subTest(path=path, new=new), \
                        tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    self.write_source(root)
                    self.edit(root, path, old, new)
                    result, stdout, stderr = self.run_wrapper(root, [])
                    self.assertEqual(result, 1)
                    self.assertIn(message % path, stderr)
                    self.assertNotIn("All checks passed", stdout)

    def test_readme_locale_table_may_omit_an_unpublished_complete_locale(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_source(root)
            for path in README_FIXTURES:
                self.edit(root, path, "| `ko` | Korean | complete |\n", "")
            result, stdout, stderr = self.run_wrapper(root, [])
            self.assertEqual(result, 0, stderr)
            self.assertIn("All checks passed", stdout)

    def test_readme_without_locale_table_or_manifest_is_rejected(self) -> None:
        for state in ("no table", "invalid manifest"):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_source(root)
                if state == "no table":
                    self.edit(root, "README.ko.md", "| Locale |", "| Tag |")
                    expected = (
                        "README.ko.md: expected one table whose first column "
                        "is Locale (found 0)"
                    )
                else:
                    root.joinpath("locales/manifest.json").write_bytes(b"{}\n")
                    expected = "Cannot read locale manifest: "
                result, stdout, stderr = self.run_wrapper(root, [])
                self.assertEqual(result, 1)
                self.assertIn(expected, stderr)
                self.assertNotIn("All checks passed", stdout)

    def test_real_wrapper_alternates_source_and_artifact_without_state_leaks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            artifact = Path(directory) / "artifact"
            self.write_source(source)
            COMMON_TESTS.write_minimal_artifact(artifact)
            COMMON_TESTS.write(
                artifact, "docs/TEMPLATE_GUIDE.md",
                "# Artifact Guide\n\n- **Template version:** 1.0.0\n\n"
                "## History\n<!-- template-section:release-history -->\n\n"
                "### v1.0.0\n",
            )
            for tree in ("locales", "template"):
                COMMON_TESTS.write(source, tree + "/BROKEN.md", "[bad](MISSING.md)\n")
            checker = MAINTAINER_CHECKER.CHECK_DOCS
            initial_root = checker.ROOT
            initial_exclusions = checker.EXCLUDED_TOP_LEVEL_NAMES
            for arguments, expected in (
                ([], 0),
                (["--root", str(artifact)], 0),
                (["--root", str(source)], 1),
                ([], 0),
            ):
                with self.subTest(arguments=arguments):
                    result, _, stderr = self.run_wrapper(source, arguments)
                    self.assertEqual(result, expected, stderr)
                    if expected:
                        self.assertIn("docs/TEMPLATE_GUIDE.md", stderr)
                        self.assertIn("template-section:release-history", stderr)
                    self.assertEqual(checker.ROOT, initial_root)
                    self.assertEqual(checker.EXCLUDED_TOP_LEVEL_NAMES, initial_exclusions)
            for tree in ("locales", "template"):
                broken = tree + "/BROKEN.md"
                COMMON_TESTS.write(artifact, broken, "[bad](MISSING.md)\n")
                result, stdout, stderr = self.run_wrapper(
                    source, ["--root", str(artifact)]
                )
                self.assertEqual(result, 1)
                self.assertIn(broken, stderr)
                self.assertNotIn("All checks passed", stdout)
                self.assertEqual(self.run_wrapper(source, [])[0], 0)
                artifact.joinpath(broken).unlink()
            self.assertEqual(self.run_wrapper(source, ["--root", str(artifact)])[0], 0)

    def test_real_checker_failure_codes_are_preserved(self) -> None:
        for state, expected in (("broken link", 1), ("missing AGENTS.md", 2)):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_source(root)
                if state == "broken link":
                    COMMON_TESTS.write(root, "docs/BROKEN.md", "[bad](MISSING.md)\n")
                else:
                    root.joinpath("AGENTS.md").unlink()
                result, stdout, stderr = self.run_wrapper(root, [])
                self.assertEqual(result, expected, stderr)
                self.assertNotIn("All checks passed", stdout)

    def test_source_candidate_heading_does_not_allow_a_different_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_source(root)
            self.assertEqual(self.run_wrapper(root, [])[0], 0)
            history = root / "CHANGELOG.md"
            history.write_text(
                history.read_text(encoding="utf-8").replace("v1.0.0", "v0.9.0"),
                encoding="utf-8",
            )
            result, _, stderr = self.run_wrapper(root, [])
            self.assertEqual(result, 1)
            self.assertIn("Current version is absent from CHANGELOG.md history: 1.0.0", stderr)

    def test_source_git_attributes_keep_maintainer_and_payload_paths_lf(self) -> None:
        paths = (
            "AGENTS.md", "scripts/check-docs.py",
            "template/common/scripts/check-docs.py", "locales/ko/docs/TEMPLATE_GUIDE.md",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath(".gitattributes").write_bytes(
                REPOSITORY_ROOT.joinpath(".gitattributes").read_bytes()
            )
            subprocess.run(
                ["git", "init", "--quiet", str(root)], check=True, capture_output=True,
            )
            result = subprocess.run(
                ["git", "-c", "core.attributesFile=", "check-attr", "-z",
                 "text", "eol", "--", *paths],
                cwd=root, env=dict(os.environ, GIT_ATTR_NOSYSTEM="1"),
                check=True, capture_output=True,
            )
            fields = result.stdout.decode("utf-8").split("\0")[:-1]
            attributes = {
                (fields[i], fields[i + 1]): fields[i + 2]
                for i in range(0, len(fields), 3)
            }
            for path in paths:
                self.assertEqual(attributes[path, "text"], "auto")
                self.assertEqual(attributes[path, "eol"], "lf")


if __name__ == "__main__":
    unittest.main()
