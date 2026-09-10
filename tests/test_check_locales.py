from __future__ import annotations

import json
import shutil
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

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @property
    def manifest_path(self) -> Path:
        return self.root / "locales/manifest.json"

    def load_manifest(self) -> Dict[str, Any]:
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, manifest: Dict[str, Any]) -> None:
        self.manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
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

    def test_symlink_and_non_lf_source_are_rejected(self) -> None:
        agents = self.path("locales/en/AGENTS.md")
        agents.unlink()
        agents.symlink_to("README.md")
        self.assert_error("source contains symlink")

        agents.unlink()
        shutil.copy2(REPOSITORY_ROOT / "locales/en/AGENTS.md", agents)
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

    def test_review_and_bugbot_invariant_lists_must_match(self) -> None:
        path = self.path("locales/en/.cursor/BUGBOT.md")
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("{{PROJECT_INVARIANT_2}}", "{{PROJECT_INVARIANT_2}} drift", 1),
            encoding="utf-8",
        )
        self.assert_error("REVIEW/BUGBOT project invariants differ")

    def test_status_rules_and_stable_release_gate_are_separate(self) -> None:
        manifest = self.load_manifest()
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
