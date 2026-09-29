from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
import check_locales as CHECK_LOCALES  # noqa: E402


def _ignore_generated(_directory: str, names: list[str]) -> list[str]:
    return [name for name in names if name == "__pycache__" or name.endswith(".pyc")]


class LocaleFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="locale-source-check-")
        self.root = Path(self.temporary.name) / "repository"
        self.root.mkdir()
        shutil.copytree(
            REPOSITORY_ROOT / "locales",
            self.root / "locales",
            ignore=_ignore_generated,
        )
        shutil.copytree(
            REPOSITORY_ROOT / "template",
            self.root / "template",
            ignore=_ignore_generated,
        )
        self.root.joinpath("docs").mkdir()
        shutil.copy2(
            REPOSITORY_ROOT / "docs/TEMPLATE_GUIDE.md",
            self.root / "docs/TEMPLATE_GUIDE.md",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def symlink_or_skip(
        self, link: Path, target: str | Path, *, target_is_directory: bool = False
    ) -> None:
        try:
            link.symlink_to(target, target_is_directory=target_is_directory)
        except NotImplementedError as exc:
            self.skipTest("symlink creation is unavailable: %s" % exc)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("symlink creation requires Windows privileges: %s" % exc)
            raise

    @property
    def manifest_path(self) -> Path:
        return self.root / "locales/manifest.json"

    def load_manifest(self) -> Dict[str, Any]:
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, manifest: Dict[str, Any]) -> None:
        self.manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def path(self, relative: str) -> Path:
        return self.root / relative

    def errors(self, require_stable: bool = False) -> list[str]:
        return CHECK_LOCALES.check_locales(self.root, require_stable=require_stable)

    def assert_error(self, needle: str, errors: list[str] | None = None) -> None:
        actual = self.errors() if errors is None else errors
        self.assertTrue(any(needle in error for error in actual), actual)

    def test_repository_locale_sources_are_consistent(self) -> None:
        self.assertEqual(self.errors(), [])

    def search_pattern(self, tag: str) -> str:
        text = self.path("locales/%s/docs/TEMPLATE_GUIDE.md" % tag).read_text(encoding="utf-8")
        declaration = next(
            line for line in text.splitlines()
            if line.startswith("template_placeholder_pattern=")
        )
        literal = declaration.split("=", 1)[1]
        self.assertTrue(literal.startswith("'") and literal.endswith("'"))
        return literal[1:-1]

    def test_placeholder_search_rejects_loss_of_independent_vocabulary(self) -> None:
        tokens = {
            "en": ("Adapt to the project", "Describe as appropriate for the project",
                   "Customize for the project", "Briefly describe", r"\| Example",
                   "Example decision", "Example completion", r"\*\*Example:\*\*"),
            "ko": ("프로젝트에 맞게 작성", "간단히 작성", r"\| 예시",
                   "예시 결정", "예시 완료", r"\*\*예시:\*\*"),
        }
        for tag, vocabulary in tokens.items():
            path = self.path("locales/%s/docs/TEMPLATE_GUIDE.md" % tag)
            original = path.read_text(encoding="utf-8")
            pattern = self.search_pattern(tag)
            for token in (r"\{\{", "YYYY-MM-DD", "template-example:project-invariant", *vocabulary):
                with self.subTest(tag=tag, token=token):
                    # Remove one alternative while keeping all other declarations/references valid.
                    alternatives = re.split(r"(?<!\\)\|", pattern)
                    self.assertIn(token, alternatives)
                    altered = "|".join(part for part in alternatives if part != token)
                    path.write_text(original.replace(pattern, altered, 1), encoding="utf-8", newline="\n")
                    self.assert_error("%s:docs/TEMPLATE_GUIDE.md placeholder search misses sentinel" % tag)
                    path.write_text(original, encoding="utf-8", newline="\n")

    def test_placeholder_search_requires_one_literal_declaration(self) -> None:
        for tag in ("en", "ko"):
            path = self.path("locales/%s/docs/TEMPLATE_GUIDE.md" % tag)
            original = path.read_text(encoding="utf-8")
            declaration = "template_placeholder_pattern='%s'" % self.search_pattern(tag)
            for replacement in ("", declaration + "\n" + declaration,
                                declaration.replace("|", "|\\\n", 1),
                                "template_placeholder_pattern=$OTHER_PATTERN"):
                with self.subTest(tag=tag, replacement=replacement):
                    path.write_text(original.replace(declaration, replacement, 1), encoding="utf-8", newline="\n")
                    self.assert_error("must declare template_placeholder_pattern exactly once")
                    path.write_text(original, encoding="utf-8", newline="\n")

    def test_placeholder_search_rejects_empty_or_invalid_regex(self) -> None:
        path = self.path("locales/en/docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        pattern = self.search_pattern("en")
        for replacement, expected in (("", "must not match empty text"),
                                      ("[", "invalid placeholder search pattern")):
            with self.subTest(pattern=replacement):
                path.write_text(original.replace(pattern, replacement, 1), encoding="utf-8", newline="\n")
                self.assert_error(expected)

    def test_both_search_commands_require_the_quoted_shared_regex_operand(self) -> None:
        reference = '"$template_placeholder_pattern"'
        for tag in ("en", "ko"):
            path = self.path("locales/%s/docs/TEMPLATE_GUIDE.md" % tag)
            original = path.read_text(encoding="utf-8")
            for command, occurrence in (("rg", 0), ("grep", 1)):
                for replacement in ('"YYYY-MM-DD"', "$template_placeholder_pattern"):
                    with self.subTest(tag=tag, command=command, replacement=replacement):
                        parts = original.split(reference)
                        self.assertEqual(len(parts), 3)
                        altered = (reference.join(parts[:occurrence + 1]) + replacement
                                   + reference.join(parts[occurrence + 1:]))
                        path.write_text(altered, encoding="utf-8", newline="\n")
                        self.assert_error("%s must use the quoted shared pattern" % command)
                        path.write_text(original, encoding="utf-8", newline="\n")

    def test_search_declaration_must_precede_commands(self) -> None:
        path = self.path("locales/en/docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        declaration = "template_placeholder_pattern='%s'" % self.search_pattern("en")
        altered = original.replace(declaration, "", 1).replace(
            'grep -rnE', declaration + '\ngrep -rnE', 1
        )
        path.write_text(altered, encoding="utf-8", newline="\n")
        self.assert_error("rg must use the quoted shared pattern")

    def test_search_contract_cannot_be_satisfied_by_comments_or_other_fences(self) -> None:
        path = self.path("locales/en/docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        declaration = "```bash\ntemplate_placeholder_pattern='%s'\n```" % self.search_pattern("en")
        for replacement in ("<!--\n" + declaration + "\n-->",
                            declaration.replace("```bash", "```text"),
                            "````text\n" + declaration + "\n````"):
            with self.subTest(replacement=replacement):
                path.write_text(original.replace(declaration, replacement, 1), encoding="utf-8", newline="\n")
                self.assert_error("must declare template_placeholder_pattern exactly once")

        for command in ("rg", "grep"):
            altered = original.replace(command + " ", "# " + command + " ", 1)
            path.write_text(altered, encoding="utf-8", newline="\n")
            self.assert_error(command + " must use the quoted shared pattern")

    def test_root_search_delegation_rejects_missing_or_decoy_links(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        for label, tag in (("영문 가이드", "en"), ("한국어 가이드", "ko")):
            link = "[%s](../locales/%s/docs/TEMPLATE_GUIDE.md)" % (label, tag)
            for replacement in ("", "<!-- " + link + " -->", "\n```md\n" + link + "\n```\n"):
                with self.subTest(tag=tag, replacement=replacement):
                    self.assertEqual(original.count(link), 1)
                    path.write_text(original.replace(link, replacement, 1), encoding="utf-8", newline="\n")
                    self.assert_error("search section must delegate to ../locales/%s/" % tag)

    def test_root_guide_cannot_own_an_independent_search_pattern(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        for snippet in (
            "```sh\nrg 'YYYY-MM-DD|Customize for the project' .\n```\n",
            "```sh\nrg 'YYYY-MM-DD' .\n",
            "```bash\ngrep -rnE 'YYYY-MM-DD' .\n```\n",
            "```sh\ntemplate_placeholder_pattern='YYYY-MM-DD'\n```\n",
            "```regex\nYYYY-MM-DD|Customize for the project\n```\n",
        ):
            with self.subTest(snippet=snippet):
                altered = original.replace("## 4. ", snippet + "\n## 4. ", 1)
                path.write_text(altered, encoding="utf-8", newline="\n")
                self.assert_error("maintainer guide must not define an independent placeholder search")
        path.write_text(original + "\nrg 또는 grep의 정본은 locale 가이드입니다.\n", encoding="utf-8", newline="\n")
        self.assertEqual(self.errors(), [])

    def test_root_search_gate_does_not_skip_a_missing_or_non_file_guide(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        path.unlink()
        self.assert_error("cannot read maintainer docs/TEMPLATE_GUIDE.md")
        path.mkdir()
        self.assert_error("cannot read maintainer docs/TEMPLATE_GUIDE.md")

    def test_root_search_gate_rejects_git_grep_and_command_wrappers(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        for command in (
            "git grep -nE 'YYYY-MM-DD|Customize for the project' -- '*.md'",
            "git -C . --no-pager grep -nE 'YYYY-MM-DD' -- '*.md'",
            "git \\" + "\n  grep -nE 'YYYY-MM-DD' -- '*.md'",
            "command rg 'YYYY-MM-DD' .",
            "env LC_ALL=C grep -rnE 'YYYY-MM-DD' .",
            "cd .;grep -rnE 'YYYY-MM-DD' .",
        ):
            snippets = ["```sh\n" + command + "\n```\n"]
            if "\n" not in command:
                snippets.append("`" + command + "`\n")
            for snippet in snippets:
                with self.subTest(snippet=snippet):
                    altered = original.replace("## 4. ", snippet + "\n## 4. ", 1)
                    path.write_text(altered, encoding="utf-8", newline="\n")
                    self.assert_error("maintainer guide must not define an independent placeholder search")
        malformed = "```sh\ngit grep -nE 'YYYY-MM-DD .\n```\n"
        path.write_text(original.replace("## 4. ", malformed + "\n## 4. ", 1),
                        encoding="utf-8", newline="\n")
        self.assert_error("not a maintainer check command: git grep -nE 'YYYY-MM-DD .")

    def test_root_search_gate_allows_unrelated_sections_and_search_mentions(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        mention = (
            "`rg` 또는 `grep`의 정본은 locale 가이드입니다.\n"
            "<!--\n```sh\ngit grep -nE 'YYYY-MM-DD'\n```\n-->\n"
            "```sh\n# git grep -nE 'YYYY-MM-DD'\n```\n"
        )
        unrelated = (
            "```sh\ngit grep -n 'release' -- '*.md'\ngrep -n 'release' CHANGELOG.md\n```\n"
            "```regex\nrelease-[0-9]+\n```\n"
        )
        altered = original.replace("## 4. ", mention + "\n## 4. ", 1)
        path.write_text(altered + "\n" + unrelated, encoding="utf-8", newline="\n")
        self.assertEqual(self.errors(), [])

    def test_root_search_gate_rejects_search_tool_spellings(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        for tool in ("egrep", "fgrep", "/usr/bin/grep", "/usr/bin/egrep", "grep.exe",
                     "RG.EXE", '"C:\\Tools\\grep.exe"', "'/opt/search tools/rg'",
                     "'/opt/search tools/FGREP.EXE'"):
            command = tool + " -n YYYY-MM-DD README.md"
            for snippet in ("```sh\n" + command + "\n```\n", "`" + command + "`\n"):
                with self.subTest(tool=tool, snippet=snippet):
                    path.write_text(original.replace("## 4. ", snippet + "\n## 4. ", 1),
                                    encoding="utf-8", newline="\n")
                    self.assert_error("maintainer guide must not define an independent placeholder search")

    def test_root_search_gate_rejects_shell_wrapped_searches(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        for command in (
            '''sh -c "git grep -nE 'YYYY-MM-DD|Customize for the project' -- '*.md'"''',
            '''bash -lc "grep -rnE 'YYYY-MM-DD' ."''',
            '''/bin/bash --norc -euo pipefail -c "grep -rnE 'YYYY-MM-DD' ."''',
            '''bash --rcfile /tmp/bashrc -c "grep -rnE 'YYYY-MM-DD' ."''',
            '''env LC_ALL=C SH.EXE -c "grep.exe -rnE 'YYYY-MM-DD' ."''',
            '''"C:\\Tools\\bash.exe" -c "egrep -rn 'YYYY-MM-DD' ."''',
            '''sh -c "bash -c 'git grep -nE YYYY-MM-DD'"''',
            '''sh -c "grep -rnE 'YYYY-MM-DD ."''',
        ):
            for snippet in ("```sh\n" + command + "\n```\n", "`" + command + "`\n"):
                with self.subTest(command=command, snippet=snippet):
                    path.write_text(original.replace("## 4. ", snippet + "\n## 4. ", 1),
                                    encoding="utf-8", newline="\n")
                    self.assert_error("maintainer guide must not define an independent placeholder search")

    def test_root_search_gate_rejects_other_search_tools_and_vocabulary(self) -> None:
        # C51-001: no search-tool list can be complete, so any spelling must be rejected.
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        for snippet, reason in (
            ("```sh\nsed -n '/YYYY-MM-DD\\|Customize for the project/p' README.md\n```\n", "code line"),
            ("```sh\nawk '/YYYY-MM-DD|Customize for the project/' README.md\n```\n", "code line"),
            ('```sh\npython3 -c "import re, sys; print(re.findall(\'x\', sys.argv[1]))" README.md\n```\n',
             "code line"),
            ("```sh\nugrep -rn 'Customize for the project' --include='*.md' .\n```\n", "code line"),
            ("```powershell\nGet-ChildItem -Recurse -Filter *.md | Select-String 'x'\n```\n", "code line"),
            ('```sh\npwsh -c "grep -rn x ."\n```\n', "code line"),
            ("```sh\nsh -c \"printf '%s' release\"\n```\n", "code line"),
            ("```sh\npython3 scripts/check-docs.py --root .\n```\n", "code line"),
            ("적용 뒤 `sed -n '/YYYY-MM-DD/p' README.md`를 실행합니다.\n", "search pattern"),
            ("    sed -n '/YYYY-MM-DD/p' README.md\n", "search pattern"),
            ("`{{PROJECT_NAME}}`과 날짜를 root에서 따로 확인합니다.\n", "search pattern"),
            ("`template-example:project-invariant` 표식도 root에서 찾습니다.\n", "search pattern"),
            # C51-002: locale-only vocabulary without the shared tokens.
            ("적용 뒤 `grep -rn 'Customize for the project' --include='*.md' .`를 실행합니다.\n",
             "search pattern"),
            ("적용 뒤 `grep -rn '프로젝트에 맞게 작성' --include='*.md' .`를 실행합니다.\n", "search pattern"),
            ("`rg 'Adapt to the project' .`\n", "search pattern"),
            ("root에서도 예시 결정 행을 따로 찾습니다.\n", "search pattern"),
        ):
            with self.subTest(snippet=snippet):
                path.write_text(original.replace("## 4. ", snippet + "\n## 4. ", 1),
                                encoding="utf-8", newline="\n")
                errors = self.errors()
                self.assert_error("independent placeholder search in section 3", errors)
                self.assertTrue(any(reason in error for error in errors), errors)

    def test_root_search_gate_follows_the_declared_locale_patterns(self) -> None:
        # The root text check reads each locale declaration instead of a copied word list.
        guide = self.path("locales/en/docs/TEMPLATE_GUIDE.md")
        pattern = self.search_pattern("en")
        guide.write_text(guide.read_text(encoding="utf-8").replace(pattern, pattern + "|Fill in later", 1),
                         encoding="utf-8", newline="\n")
        self.assertEqual(self.errors(), [])
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        path.write_text(original.replace("## 4. ", "root에서 `Fill in later`도 찾습니다.\n\n## 4. ", 1),
                        encoding="utf-8", newline="\n")
        self.assert_error("text matches a locale placeholder search pattern: root에서 `Fill in later`")

    def test_root_search_gate_allows_only_maintainer_checks_in_code(self) -> None:
        path = self.path("docs/TEMPLATE_GUIDE.md")
        original = path.read_text(encoding="utf-8")
        allowed = (
            "`egrep`·`fgrep`·`grep.exe`·`sh -c` 이름 언급입니다.\n"
            "```sh\n# Run each check from the repository root.\n\n"
            "python3 scripts/check-locales.py --require-stable\n"
            "  python3 scripts/check-docs.py\n```\n"
        )
        path.write_text(original.replace("## 4. ", allowed + "\n## 4. ", 1),
                        encoding="utf-8", newline="\n")
        self.assertEqual(self.errors(), [])

    def assert_search_engine(self, engine: str) -> None:
        program = shutil.which(engine)
        if program is None:
            self.skipTest("%s is unavailable; no search tool is installed by this test" % engine)
        if engine == "grep":
            version = subprocess.run([program, "--version"], capture_output=True, timeout=5)
            if b"GNU grep" not in version.stdout:
                self.skipTest("GNU grep is required for the documented fallback")
        common = ["{{PROJECT_NAME}}", "unfinished {{", "- **Last reviewed:** YYYY-MM-DD",
                  "<!-- template-example:project-invariant -->"]
        vocabulary = {
            "en": ["- **Owner:** Adapt to the project", "- **Owner:** Customize for the project",
                   "Describe as appropriate for the project", "Briefly describe the boundaries",
                   "| Example |", "Example decision", "Example completion", "**Example:**"],
            "ko": ["- **Owner:** 프로젝트에 맞게 작성", "간단히 작성", "| 예시 |",
                   "예시 결정", "예시 완료", "**예시:**"],
        }
        filled = ["# Project overview", "- **Owner:** Chae Sangwon", "- **Last reviewed:** 2026-09-28"]
        for tag in ("en", "ko"):
            with self.subTest(tag=tag, engine=engine):
                expected = common + vocabulary[tag]
                guide = self.path("locales/%s/docs/TEMPLATE_GUIDE.md" % tag).read_text(encoding="utf-8")
                lines = guide.splitlines()
                start = next(index for index, line in enumerate(lines) if line.startswith(engine + " "))
                command = lines[start]
                for continuation in lines[start + 1:]:
                    if not command.endswith("\\"):
                        break
                    command = command[:-1] + continuation
                # Invoke only the chosen executable with data arguments; never evaluate shell code.
                arguments = [self.search_pattern(tag) if value == "$template_placeholder_pattern" else value
                             for value in shlex.split(command)]
                matches = {
                    "README.md": expected,
                    ".cursor/BUGBOT.md": ["{{PROJECT_NAME}}"],
                    "docs/changes/_template/01-CHANGE.md": ["{{PROJECT_NAME}}"],
                }
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    for relative, content in {
                        "README.md": filled + expected,
                        ".cursor/BUGBOT.md": ["{{PROJECT_NAME}}"],
                        "docs/changes/_template/01-CHANGE.md": ["{{PROJECT_NAME}}"],
                        "docs/TEMPLATE_GUIDE.md": ["YYYY-MM-DD"],
                        "docs/DOCS_GUIDE.md": ["YYYY-MM-DD"],
                        ".git/IGNORED.md": ["YYYY-MM-DD"],
                        "IGNORED.txt": ["YYYY-MM-DD"],
                    }.items():
                        path = root / relative
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text("\n".join(content) + "\n", encoding="utf-8", newline="\n")
                    result = subprocess.run(
                        [program, "--color=never", *arguments[1:]], cwd=root,
                        capture_output=True, text=True, encoding="utf-8", timeout=5,
                    )
                self.assertEqual(result.returncode, 0, result.stderr)
                actual = {}
                for line in result.stdout.splitlines():
                    relative, _, value = line.split(":", 2)
                    relative = relative.replace("\\", "/").removeprefix("./")
                    actual.setdefault(relative, []).append(value)
                self.assertEqual(actual, matches)

    def test_declared_patterns_match_ripgrep_sentinels_and_exclude_filled_values(self) -> None:
        self.assert_search_engine("rg")

    def test_declared_patterns_match_gnu_grep_sentinels_and_exclude_filled_values(self) -> None:
        self.assert_search_engine("grep")

    def test_adoption_policy_covers_exactly_the_artifact_inventory(self) -> None:
        manifest = self.load_manifest()
        policy = manifest["artifact"]["adoption_policy"]
        self.assertEqual(policy["LICENSE"], "decide")
        self.assertEqual(policy["README.md"], "merge")
        self.assertEqual(policy["scripts/check-docs.py"], "copy")
        del policy["LICENSE"]
        policy["docs/UNLISTED.md"] = "copy"
        policy["README.md"] = "overwrite"
        self.write_manifest(manifest)
        errors = self.errors()
        self.assert_error("adoption_policy is missing output path: LICENSE", errors)
        self.assert_error(
            "adoption_policy has path outside the inventory: docs/UNLISTED.md", errors
        )
        self.assert_error("adoption_policy.README.md must be one of copy, decide, merge", errors)

        manifest = self.load_manifest()
        manifest["artifact"]["adoption_policy"] = ["copy"]
        self.write_manifest(manifest)
        self.assert_error("artifact.adoption_policy must be an object")

    def test_manifest_requires_its_minimum_structure_and_unique_keys(self) -> None:
        manifest = self.load_manifest()
        del manifest["contracts"]
        self.write_manifest(manifest)
        self.assert_error("missing required field(s): contracts")

        original = (REPOSITORY_ROOT / "locales/manifest.json").read_text(
            encoding="utf-8"
        )
        self.manifest_path.write_text(
            original.replace(
                '"schema_version": 1,',
                '"schema_version": 1,\n  "schema_version": 1,',
                1,
            ),
            encoding="utf-8",
        )
        self.assert_error("duplicate JSON key")

    def test_manifest_rejects_noncanonical_and_underscore_locale_tags(self) -> None:
        for replacement, expected in (
            ("EN", "outside the supported canonical BCP 47 form"),
            ("en_US", "must use BCP 47 hyphens"),
        ):
            with self.subTest(tag=replacement):
                manifest = self.load_manifest()
                manifest["locales"][replacement] = manifest["locales"].pop("en")
                manifest["required_stable_locales"][0] = replacement
                self.write_manifest(manifest)
                self.assert_error(expected)
                shutil.copy2(REPOSITORY_ROOT / "locales/manifest.json", self.manifest_path)

    def test_supported_bcp47_profile_enforces_canonical_casing(self) -> None:
        for tag in ("en", "en-US", "zh-Hant-TW"):
            with self.subTest(valid=tag):
                self.assertIsNotNone(CHECK_LOCALES.BCP47_RE.fullmatch(tag))
        for tag in ("EN", "en-us", "zh-hant-TW", "en_US", "en-1996"):
            with self.subTest(invalid=tag):
                self.assertIsNone(CHECK_LOCALES.BCP47_RE.fullmatch(tag))

    def test_required_stable_locale_must_be_in_manifest_allowlist(self) -> None:
        manifest = self.load_manifest()
        manifest["required_stable_locales"].append("fr")
        self.write_manifest(manifest)
        self.assert_error("is not in the manifest allowlist")

    def test_missing_and_unexpected_inventory_members_are_rejected(self) -> None:
        self.path("locales/en/README.md").unlink()
        self.assert_error("locale en is missing source file: README.md")

        shutil.copy2(
            REPOSITORY_ROOT / "locales/en/README.md",
            self.path("locales/en/README.md"),
        )
        self.path("locales/en/EXTRA.md").write_text("extra\n", encoding="utf-8")
        self.assert_error("locale en has unexpected source file: EXTRA.md")

    def test_missing_common_inventory_member_is_rejected(self) -> None:
        self.path("template/common/CLAUDE.md").unlink()
        self.assert_error("common is missing source file: CLAUDE.md")

    def test_common_and_locale_cannot_own_the_same_output(self) -> None:
        manifest = self.load_manifest()
        manifest["artifact"]["localized_paths"].append(
            manifest["artifact"]["common_paths"][0]
        )
        self.write_manifest(manifest)
        self.assert_error("duplicate output path is owned by common and locale")

    def test_duplicate_output_entry_is_rejected(self) -> None:
        manifest = self.load_manifest()
        manifest["artifact"]["localized_paths"].append(
            manifest["artifact"]["localized_paths"][0]
        )
        self.write_manifest(manifest)
        self.assert_error("contains duplicate path")

    def test_unsafe_and_casefold_colliding_output_paths_are_rejected(self) -> None:
        manifest = self.load_manifest()
        manifest["artifact"]["localized_paths"].append("../escape")
        self.write_manifest(manifest)
        self.assert_error("normalized relative POSIX path")

        manifest = self.load_manifest()
        manifest["artifact"]["localized_paths"][-1] = "C:/escape.md"
        self.write_manifest(manifest)
        self.assert_error("normalized relative POSIX path")

        manifest = self.load_manifest()
        manifest["artifact"]["localized_paths"][-1] = "agents.md"
        self.write_manifest(manifest)
        self.assert_error("case-fold-colliding paths")

    def test_windows_unsafe_path_components_are_rejected(self) -> None:
        for path in (
            "C:/escape.md",
            "C:escape.md",
            "//server/share.md",
            r"\\server\share.md",
            "docs/CON.md",
            "docs/prn.txt",
            "docs/COM9",
            "docs/LPT1.log",
            "docs/trailing.",
            "docs/trailing ",
        ):
            with self.subTest(path=path):
                self.assertFalse(CHECK_LOCALES._is_safe_relative_path(path))

    def test_undeclared_locale_directory_is_rejected(self) -> None:
        self.path("locales/fr").mkdir()
        self.path("locales/fr/README.md").write_text("bonjour\n", encoding="utf-8")
        self.assert_error("undeclared locale source directory")

    def test_symlink_source_is_rejected(self) -> None:
        agents = self.path("locales/en/AGENTS.md")
        agents.unlink()
        self.symlink_or_skip(agents, "README.md")
        self.assert_error("source contains symlink")

    def test_non_lf_source_is_rejected(self) -> None:
        agents = self.path("locales/en/AGENTS.md")
        agents.write_bytes(agents.read_bytes().replace(b"\n", b"\r\n"))
        self.assert_error("must use LF line endings")

    def test_placeholder_multiset_drift_is_rejected(self) -> None:
        path = self.path("locales/en/AGENTS.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("{{PROJECT_NAME}}", "Project", 1), encoding="utf-8")
        self.assert_error("placeholder multiset differs for AGENTS.md")

        path.write_text(text.replace("{{PROJECT_NAME}}", "{{PROJECT_NAME}}{{PROJECT_NAME}}", 1), encoding="utf-8")
        self.assert_error("placeholder multiset differs for AGENTS.md")

    def test_malformed_placeholder_is_rejected(self) -> None:
        path = self.path("locales/en/AGENTS.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("{{PROJECT_NAME}}", "{{PROJECT-NAME}}", 1),
            encoding="utf-8",
        )
        self.assert_error("contains malformed placeholder syntax")

    def test_valid_but_wrong_relative_link_target_is_rejected(self) -> None:
        path = self.path("locales/en/README.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace(
                "(./docs/TEMPLATE_GUIDE.md)", "(./docs/02-TODO.md)", 1
            ),
            encoding="utf-8",
        )
        self.assert_error("relative-link target sequence differs for README.md")

        path.write_text(
            text.replace(
                "[Template Guide](./docs/TEMPLATE_GUIDE.md)",
                "<!-- [Template Guide](./docs/TEMPLATE_GUIDE.md) -->",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_error("relative-link target sequence differs for README.md")

        path.write_text(
            text.replace(
                "[Template Guide](./docs/TEMPLATE_GUIDE.md)",
                "`[Template Guide](./docs/TEMPLATE_GUIDE.md)`",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_error("relative-link target sequence differs for README.md")

    def test_valid_but_wrong_numbered_heading_is_rejected(self) -> None:
        path = self.path("locales/en/docs/00-PROJECT.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("## 12. Rejected or Deferred Ideas", "## 14. Rejected or Deferred Ideas", 1),
            encoding="utf-8",
        )
        self.assert_error("numbered heading sequence differs for docs/00-PROJECT.md")

        path.write_text(
            text.replace(
                "## 12. Rejected or Deferred Ideas",
                "<!--\n## 12. Rejected or Deferred Ideas\n-->",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_error("numbered heading sequence differs for docs/00-PROJECT.md")

    def test_missing_and_reordered_markers_are_rejected(self) -> None:
        path = self.path("locales/en/docs/REVIEW.md")
        text = path.read_text(encoding="utf-8")
        section = "<!-- template-section:project-invariants -->"
        example = "<!-- template-example:project-invariant -->"
        path.write_text(text.replace(example, "", 1), encoding="utf-8")
        self.assert_error("section marker sequence differs")

        path.write_text(
            text.replace(section, "<!-- swap -->", 1)
            .replace(example, section, 1)
            .replace("<!-- swap -->", example, 1),
            encoding="utf-8",
        )
        self.assert_error("section marker sequence differs")

    def test_section_markers_must_be_visible_and_adjacent(self) -> None:
        path = self.path("locales/en/docs/REVIEW.md")
        text = path.read_text(encoding="utf-8")
        marker = "<!-- template-section:project-invariants -->"
        mutations = (
            (
                text.replace(marker, "```text\n%s\n```" % marker, 1),
                "section marker sequence differs",
            ),
            (
                text.replace(marker, "<!--\n%s\n-->" % marker, 1),
                "section marker sequence differs",
            ),
            (
                text.replace(marker, "Translated guidance\n%s" % marker, 1),
                "must directly follow a Markdown heading",
            ),
        )
        for content, expected in mutations:
            with self.subTest(expected=expected):
                path.write_text(content, encoding="utf-8")
                self.assert_error(expected)

    def test_unknown_marker_is_rejected(self) -> None:
        path = self.path("locales/en/README.md")
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<!-- template-section:undeclared-contract -->\n",
            encoding="utf-8",
        )
        self.assert_error("unknown template marker")

    def test_required_command_drift_is_rejected(self) -> None:
        path = self.path("locales/en/AGENTS.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("python scripts/check-docs.py", "python3 scripts/check-docs.py", 1),
            encoding="utf-8",
        )
        self.assert_error("must contain command docs-check exactly once")

    def test_required_command_cannot_use_an_html_comment_decoy(self) -> None:
        path = self.path("locales/en/AGENTS.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("`python scripts/check-docs.py`", "N/A", 1)
            + "\n<!--\n`python scripts/check-docs.py`\n-->\n",
            encoding="utf-8",
        )
        self.assert_error("must contain command docs-check exactly once")

    def test_undeclared_python_command_and_path_are_rejected(self) -> None:
        path = self.path("locales/en/README.md")
        path.write_text(
            path.read_text(encoding="utf-8") + "\n`python unknown-tool.py`\n",
            encoding="utf-8",
        )
        self.assert_error("Python command inventory differs from manifest")

        manifest = self.load_manifest()
        docs_test = next(
            item
            for item in manifest["contracts"]["required_commands"]
            if item["id"] == "docs-test"
        )
        docs_test["paths"].remove("docs/DOCS_GUIDE.md")
        self.write_manifest(manifest)
        self.assert_error("docs/DOCS_GUIDE.md Python command inventory differs")

    def test_skill_pair_byte_drift_is_rejected(self) -> None:
        path = self.path("locales/en/.claude/skills/design/SKILL.md")
        path.write_text(
            path.read_text(encoding="utf-8") + "\n<!-- drift -->\n",
            encoding="utf-8",
        )
        self.assert_error("skill pair differs for design")

    def test_skill_frontmatter_name_must_match_manifest_id(self) -> None:
        for relative in (
            "locales/en/.agents/skills/design/SKILL.md",
            "locales/en/.claude/skills/design/SKILL.md",
        ):
            path = self.path(relative)
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "name: design", "name: wrong-design", 1
                ),
                encoding="utf-8",
            )
        self.assert_error("front matter name must equal skill id design exactly once")

    def test_review_round_invocation_boolean_is_narrowly_validated(self) -> None:
        relatives = (
            "locales/en/.agents/skills/review-round/SKILL.md",
            "locales/en/.claude/skills/review-round/SKILL.md",
        )
        originals = {
            relative: self.path(relative).read_text(encoding="utf-8")
            for relative in relatives
        }
        mutations = {
            "false": "disable-model-invocation: false",
            "duplicate": (
                "disable-model-invocation: true\n"
                "disable-model-invocation: true"
            ),
            "comment-decoy": (
                "disable-model-invocation: false\n"
                "# disable-model-invocation: true"
            ),
            "quoted": 'disable-model-invocation: "true"',
        }
        for name, replacement in mutations.items():
            with self.subTest(name=name):
                for relative in relatives:
                    self.path(relative).write_text(
                        originals[relative].replace(
                            "disable-model-invocation: true", replacement, 1
                        ),
                        encoding="utf-8",
                    )
                self.assert_error(
                    "must define one unquoted disable-model-invocation: true boolean"
                )
                for relative in relatives:
                    self.path(relative).write_text(
                        originals[relative], encoding="utf-8"
                    )

    def test_common_implicit_invocation_policy_is_narrowly_validated(self) -> None:
        path = self.path(
            "template/common/.agents/skills/review-round/agents/openai.yaml"
        )
        original = path.read_text(encoding="utf-8")
        mutations = {
            "true": "policy:\n  allow_implicit_invocation: true\n",
            "quoted": 'policy:\n  allow_implicit_invocation: "false"\n',
            "duplicate": (
                "policy:\n"
                "  allow_implicit_invocation: false\n"
                "  allow_implicit_invocation: false\n"
            ),
            "comment-decoy": (
                "policy:\n"
                "  allow_implicit_invocation: true\n"
                "  # allow_implicit_invocation: false\n"
            ),
        }
        for name, replacement in mutations.items():
            with self.subTest(name=name):
                path.write_text(replacement, encoding="utf-8")
                self.assert_error(
                    "common config must define policy.allow_implicit_invocation "
                    "as one unquoted false boolean"
                )
                path.write_text(original, encoding="utf-8")

    def test_skill_contract_requires_marker_paths_and_fixture_ids(self) -> None:
        manifest = self.load_manifest()
        manifest["contracts"]["skills"][0]["fixture_ids"] = []
        self.write_manifest(manifest)
        self.assert_error("fixture_ids must be a non-empty array")

        manifest = self.load_manifest()
        manifest["contracts"]["skills"][0]["fixture_ids"] = ["wrong-skill-fixture"]
        self.write_manifest(manifest)
        self.assert_error("does not belong to skill design")

    def test_skill_fixture_registry_rejects_arbitrary_and_missing_consumers(self) -> None:
        manifest = self.load_manifest()
        fixtures = manifest["contracts"]["skills"][0]["fixture_ids"]
        fixtures[0] = "design-made-up"
        self.write_manifest(manifest)
        self.assert_error("has no fixture implementation")

        manifest = self.load_manifest()
        manifest["contracts"]["skills"][0]["fixture_ids"].pop()
        self.write_manifest(manifest)
        self.assert_error("is not declared in the manifest")

    def test_skill_fixture_marker_and_observable_are_enforced(self) -> None:
        skill = self.path("locales/en/.agents/skills/design/SKILL.md")
        peer = self.path("locales/en/.claude/skills/design/SKILL.md")
        for path in (skill, peer):
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "<!-- template-skill-fixture:design-minimal-artifact -->\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
        self.assert_error("skill marker sequence differs")

        for path in (skill, peer):
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace("<!-- template-skill-contract:design:v1 -->\n", "<!-- template-skill-contract:design:v1 -->\n<!-- template-skill-fixture:design-minimal-artifact -->\n", 1)
                .replace("../../../docs/01-DESIGN.md", "../../../docs/00-PROJECT.md"),
                encoding="utf-8",
            )
        self.assert_error("is missing canonical skill link")

    def test_skill_fixture_tokens_and_links_reject_decoys(self) -> None:
        relatives = (
            "locales/en/.agents/skills/design/SKILL.md",
            "locales/en/.claude/skills/design/SKILL.md",
        )
        originals = {
            relative: self.path(relative).read_text(encoding="utf-8")
            for relative in relatives
        }

        for replacement in ("§10", "§1.2", "§1a", "§1-alpha"):
            with self.subTest(section_token=replacement):
                for relative in relatives:
                    self.path(relative).write_text(
                        originals[relative].replace("§1", replacement, 1),
                        encoding="utf-8",
                    )
                self.assert_error("missing skill token(s): §1")
        self.assertTrue(CHECK_LOCALES._contains_observable_token("§1은 범위", "§1"))
        self.assertTrue(CHECK_LOCALES._contains_observable_token("See §1.", "§1"))

        link = "[docs/01-DESIGN.md](../../../docs/01-DESIGN.md)"
        decoy = (
            "docs/01-DESIGN.md"
            "\n\n```markdown\n"
            "[design](../../../docs/01-DESIGN.md)\n"
            "```\n"
        )
        for relative in relatives:
            self.path(relative).write_text(
                originals[relative].replace(link, decoy, 1),
                encoding="utf-8",
            )
        self.assert_error("is missing canonical skill link")

        blockquote_decoy = (
            "docs/01-DESIGN.md"
            "\n\n> ```markdown\n"
            "> [design](../../../docs/01-DESIGN.md)\n"
            "> ```\n"
        )
        for relative in relatives:
            self.path(relative).write_text(
                originals[relative].replace(link, blockquote_decoy, 1),
                encoding="utf-8",
            )
        self.assert_error("is missing canonical skill link")

        root_fence_decoy = (
            "docs/01-DESIGN.md"
            "\n\n```markdown\n"
            "> ```\n"
            "[design](../../../docs/01-DESIGN.md)\n"
            "```\n"
        )
        for relative in relatives:
            self.path(relative).write_text(
                originals[relative].replace(link, root_fence_decoy, 1),
                encoding="utf-8",
            )
        self.assert_error("is missing canonical skill link")

    def test_skill_fixture_assertions_are_exact_and_adjacent(self) -> None:
        cases = (
            (
                "design",
                "MUST_USE_MINIMUM_REQUIRED_DESIGN_ARTIFACTS",
                "MAY_USE_ANY_DESIGN_ARTIFACTS",
            ),
            (
                "design",
                "MUST_NOT_IMPLEMENT_BEFORE_USER_AGREEMENT",
                "MAY_IMPLEMENT_BEFORE_USER_AGREEMENT",
            ),
            (
                "design",
                "MUST_REUSE_ACCEPTED_SCOPE_WITHOUT_REAPPROVAL",
                "MUST_REAPPROVE_ACCEPTED_SCOPE",
            ),
            (
                "project-analysis",
                "MUST_REQUIRE_EXPLICIT_WHOLE_PROJECT_REQUEST",
                "MAY_RUN_WITHOUT_WHOLE_PROJECT_REQUEST",
            ),
            (
                "project-analysis",
                "MUST_DEFAULT_TO_READ_ONLY_ANALYSIS",
                "MAY_MUTATE_DURING_ANALYSIS",
            ),
            (
                "project-analysis",
                "MUST_DISTINGUISH_VERIFIED_INFERRED_UNVERIFIED",
                "MAY_MERGE_ALL_EVIDENCE_STATES",
            ),
            (
                "review-round",
                "MUST_REQUIRE_EXPLICIT_USER_INVOCATION",
                "MAY_USE_IMPLICIT_INVOCATION",
            ),
            (
                "review-round",
                "MUST_GATE_ON_EXACT_HEAD_AND_BASE",
                "MAY_GATE_ON_OLDER_HEAD",
            ),
            (
                "review-round",
                "MUST_REQUIRE_USER_CONFIRMATION_BEFORE_MERGE",
                "MAY_MERGE_WITHOUT_USER_CONFIRMATION",
            ),
        )
        for skill_id, expected, replacement in cases:
            with self.subTest(assertion=expected):
                relatives = (
                    "locales/en/.agents/skills/%s/SKILL.md" % skill_id,
                    "locales/en/.claude/skills/%s/SKILL.md" % skill_id,
                )
                originals = {
                    relative: self.path(relative).read_text(encoding="utf-8")
                    for relative in relatives
                }
                for relative in relatives:
                    self.path(relative).write_text(
                        originals[relative].replace(expected, replacement, 1),
                        encoding="utf-8",
                    )
                self.assert_error("fixture stable assertion sequence differs")
                self.assert_error("has unregistered template contract assertion")
                for relative in relatives:
                    self.path(relative).write_text(
                        originals[relative], encoding="utf-8"
                    )

        marker = "<!-- template-skill-fixture:design-minimal-artifact -->"
        assertion = (
            "> [template-contract:v1] "
            "MUST_USE_MINIMUM_REQUIRED_DESIGN_ARTIFACTS"
        )
        for relative in (
            "locales/en/.agents/skills/design/SKILL.md",
            "locales/en/.claude/skills/design/SKILL.md",
        ):
            path = self.path(relative)
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    "%s\n%s" % (marker, assertion),
                    "%s\n> decoy\n%s" % (marker, assertion),
                    1,
                ),
                encoding="utf-8",
            )
        self.assert_error("must be followed by its exact assertion")

    def test_skill_fixture_marker_and_assertion_cannot_use_fenced_decoys(self) -> None:
        marker = "<!-- template-skill-fixture:design-minimal-artifact -->"
        assertion = (
            "> [template-contract:v1] "
            "MUST_USE_MINIMUM_REQUIRED_DESIGN_ARTIFACTS"
        )
        relatives = (
            "locales/en/.agents/skills/design/SKILL.md",
            "locales/en/.claude/skills/design/SKILL.md",
        )
        originals = {
            relative: self.path(relative).read_text(encoding="utf-8")
            for relative in relatives
        }
        for relative in relatives:
            self.path(relative).write_text(
                originals[relative].replace(
                    "%s\n%s" % (marker, assertion),
                    "```text\n%s\n%s\n```" % (marker, assertion),
                    1,
                ),
                encoding="utf-8",
            )
        self.assert_error("must appear exactly once outside fenced code")
        self.assert_error("fixture stable assertion sequence differs")

        for relative in relatives:
            self.path(relative).write_text(
                originals[relative].replace(
                    assertion, "<!--\n%s\n-->" % assertion, 1
                ),
                encoding="utf-8",
            )
        self.assert_error("must be followed by its exact assertion")
        self.assert_error("fixture stable assertion sequence differs")

        for relative in relatives:
            self.path(relative).write_text(
                originals[relative].replace(
                    marker, "<!--\n%s\n-->" % marker, 1
                ),
                encoding="utf-8",
            )
        self.assert_error(
            "must appear exactly once outside fenced code and enclosing HTML comments"
        )

    def test_review_and_bugbot_invariant_lists_must_match(self) -> None:
        path = self.path("locales/en/.cursor/BUGBOT.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("{{PROJECT_INVARIANT_2}}", "{{PROJECT_INVARIANT_2}} drift", 1),
            encoding="utf-8",
        )
        self.assert_error("REVIEW/BUGBOT project invariants differ")

    def test_review_invariant_example_marker_cannot_hide_a_real_rule(self) -> None:
        path = self.path("locales/en/docs/REVIEW.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("- **Example:**", "- **Rule A:**", 1),
            encoding="utf-8",
        )
        self.assert_error(
            "example marker must immediately precede an English or Korean "
            "template example bullet"
        )

        path.write_text(
            text.replace(
                "<!-- template-example:project-invariant -->\n",
                "<!-- template-example:project-invariant -->\n"
                "Translated guidance\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_error("example marker must immediately precede its bullet")

    def test_indented_code_bullet_is_not_a_source_invariant(self) -> None:
        marker = "<!-- template-section:project-invariants -->"
        text = """# Review
## Invariants
%s

    - **Code example:** not an invariant
 - **Rule A:** first invariant
 - **Rule B:** second invariant
- **Rule C:** shallower invariant
""" % marker
        bounds = CHECK_LOCALES._section_bounds(text, marker)
        self.assertIsNotNone(bounds)
        self.assertEqual(
            CHECK_LOCALES._top_level_bullets(text, *bounds),
            [
                (5, "- **Rule A:** first invariant"),
                (6, "- **Rule B:** second invariant"),
                (7, "- **Rule C:** shallower invariant"),
            ],
        )

    def test_status_rules_and_stable_release_gate_are_separate(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual(CHECK_LOCALES.complete_locales(manifest), ("en", "ko"))
        self.assertEqual(self.errors(), [])

        manifest["locales"]["en"]["status"] = "experimental"
        self.write_manifest(manifest)
        self.assertEqual(CHECK_LOCALES.complete_locales(manifest), ("ko",))
        self.assertEqual(self.errors(), [])
        self.assert_error("is not complete", self.errors(require_stable=True))

        manifest["locales"]["en"]["status"] = "complete"
        self.write_manifest(manifest)
        self.assertEqual(self.errors(require_stable=True), [])

    def test_complete_and_stale_baseline_versions_are_validated(self) -> None:
        manifest = self.load_manifest()
        manifest["locales"]["ko"]["baseline_version"] = "1.6.0"
        self.write_manifest(manifest)
        self.assert_error("is complete but baseline_version")

        manifest["locales"]["ko"]["status"] = "stale"
        manifest["locales"]["ko"]["baseline_version"] = "1.7.1"
        self.write_manifest(manifest)
        self.assert_error("is stale but baseline_version")

        manifest["locales"]["ko"]["baseline_version"] = "1.7.1-rc.1"
        self.write_manifest(manifest)
        self.assertEqual(self.errors(), [])

    def test_semver_rejects_numeric_prerelease_leading_zero(self) -> None:
        manifest = self.load_manifest()
        manifest["locales"]["en"]["baseline_version"] = "1.7.1-01"
        self.write_manifest(manifest)
        self.assert_error("baseline_version must be SemVer")

    def test_unknown_locale_status_is_rejected(self) -> None:
        manifest = self.load_manifest()
        manifest["locales"]["en"]["status"] = "preview"
        self.write_manifest(manifest)
        self.assert_error("status must be one of")

    def test_manifest_objects_reject_unknown_fields(self) -> None:
        manifest = self.load_manifest()
        manifest["unexpected"] = True
        self.write_manifest(manifest)
        self.assert_error("manifest has unexpected field(s)")

        manifest.pop("unexpected")
        manifest["locales"]["en"]["unexpected"] = True
        self.write_manifest(manifest)
        self.assert_error("locales.en has unexpected field(s)")


if __name__ == "__main__":
    unittest.main()
