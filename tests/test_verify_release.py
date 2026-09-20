from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
import package_release as PACKAGE_RELEASE  # noqa: E402
import verify_release as VERIFY_RELEASE  # noqa: E402


VERSION = "2.1.0"
SOURCE_COMMIT = "a" * 40
MAIN_COMMIT = "b" * 40
REPOSITORY = "jaff2836/coding-agent-docs-template"


class VerifyReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="verify-release-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_compare_assets_requires_exact_inventory_and_bytes(self) -> None:
        expected = {"one": b"1", "two": b"2"}
        VERIFY_RELEASE._compare_assets(expected, dict(expected), "fixture")
        with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "inventory"):
            VERIFY_RELEASE._compare_assets(expected, {"one": b"1"}, "fixture")
        with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "bytes differ: two"):
            VERIFY_RELEASE._compare_assets(
                expected, {"one": b"1", "two": b"changed"}, "fixture"
            )

    def test_repeated_package_must_be_byte_identical(self) -> None:
        first = PACKAGE_RELEASE.ReleaseArtifacts(
            files={"asset": b"one"}, manifest={"version": VERSION}
        )
        second = PACKAGE_RELEASE.ReleaseArtifacts(
            files={"asset": b"two"}, manifest={"version": VERSION}
        )
        with patch.object(
            VERIFY_RELEASE.package_release,
            "build_release_artifacts",
            side_effect=(first, second),
        ):
            with self.assertRaisesRegex(
                VERIFY_RELEASE.VerificationError, "repeated package asset bytes differ"
            ):
                VERIFY_RELEASE._build_reproducible_assets(
                    self.root,
                    version=VERSION,
                    source_commit=SOURCE_COMMIT,
                    repository=REPOSITORY,
                )

    def test_remote_refs_bind_annotated_tag_and_synchronized_main(self) -> None:
        tag_ref = "refs/tags/v%s" % VERSION

        def command(arguments, *, cwd):
            self.assertEqual(cwd, self.root)
            if arguments[:3] == ["git", "cat-file", "-t"]:
                return b"tag\n"
            if arguments[:2] == ["git", "rev-parse"]:
                return (SOURCE_COMMIT + "\n").encode("ascii")
            if arguments[:3] == ["git", "merge-base", "--is-ancestor"]:
                return b""
            self.fail("unexpected command: %r" % (arguments,))

        with patch.object(
            VERIFY_RELEASE,
            "_ls_remote",
            side_effect=(
                {"refs/heads/main": MAIN_COMMIT},
                {
                    "refs/heads/main": MAIN_COMMIT,
                    tag_ref: "c" * 40,
                    tag_ref + "^{}": SOURCE_COMMIT,
                },
            ),
        ), patch.object(VERIFY_RELEASE, "_command", side_effect=command):
            self.assertEqual(
                VERIFY_RELEASE._verify_remote_refs(
                    self.root,
                    version=VERSION,
                    source_commit=SOURCE_COMMIT,
                    origin_remote="origin",
                    github_remote="github",
                ),
                MAIN_COMMIT,
            )

    def test_remote_refs_reject_main_drift_and_lightweight_tag(self) -> None:
        with patch.object(
            VERIFY_RELEASE,
            "_ls_remote",
            side_effect=(
                {"refs/heads/main": "a" * 40},
                {"refs/heads/main": "b" * 40},
            ),
        ):
            with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "main differ"):
                VERIFY_RELEASE._verify_remote_refs(
                    self.root,
                    version=VERSION,
                    source_commit=SOURCE_COMMIT,
                    origin_remote="origin",
                    github_remote="github",
                )

        with patch.object(
            VERIFY_RELEASE,
            "_ls_remote",
            side_effect=(
                {"refs/heads/main": MAIN_COMMIT},
                {
                    "refs/heads/main": MAIN_COMMIT,
                    "refs/tags/v%s" % VERSION: SOURCE_COMMIT,
                },
            ),
        ):
            with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "annotated tag"):
                VERIFY_RELEASE._verify_remote_refs(
                    self.root,
                    version=VERSION,
                    source_commit=SOURCE_COMMIT,
                    origin_remote="origin",
                    github_remote="github",
                )

    def test_release_shape_separates_draft_and_immutable_publication(self) -> None:
        tag = "v%s" % VERSION
        VERIFY_RELEASE._require_release_shape(
            {"tag_name": tag, "draft": True, "immutable": False},
            tag=tag,
            draft=True,
            immutable=False,
        )
        VERIFY_RELEASE._require_release_shape(
            {
                "tag_name": tag,
                "draft": False,
                "immutable": True,
                "prerelease": False,
            },
            tag=tag,
            draft=False,
            immutable=True,
        )
        with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "draft state"):
            VERIFY_RELEASE._require_release_shape(
                {"tag_name": tag, "draft": False, "immutable": False},
                tag=tag,
                draft=True,
                immutable=False,
            )
        with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "immutable state"):
            VERIFY_RELEASE._require_release_shape(
                {
                    "tag_name": tag,
                    "draft": False,
                    "immutable": False,
                    "prerelease": False,
                },
                tag=tag,
                draft=False,
                immutable=True,
            )

    def test_draft_metadata_uses_draft_aware_release_view(self) -> None:
        tag = "v%s" % VERSION
        output = (
            b'{"databaseId":42,"tagName":"v2.1.0","isDraft":true,'
            b'"isImmutable":false,"isPrerelease":false}'
        )
        with patch.object(VERIFY_RELEASE, "_command", return_value=output) as command:
            metadata = VERIFY_RELEASE._draft_release_metadata(
                self.root, REPOSITORY, tag
            )
        command.assert_called_once_with(
            [
                "gh",
                "release",
                "view",
                tag,
                "--repo",
                REPOSITORY,
                "--json",
                "databaseId,tagName,isDraft,isImmutable,isPrerelease",
            ],
            cwd=self.root,
        )
        self.assertEqual(
            metadata,
            {
                "id": 42,
                "tag_name": tag,
                "draft": True,
                "immutable": False,
                "prerelease": False,
            },
        )

    def test_download_release_assets_reads_only_regular_files(self) -> None:
        expected = {"asset-one": b"one", "asset-two": b"two"}

        def command(arguments, *, cwd):
            self.assertEqual(cwd, self.root)
            destination = Path(arguments[arguments.index("--dir") + 1])
            for name, data in expected.items():
                (destination / name).write_bytes(data)
            return b""

        with patch.object(VERIFY_RELEASE, "_command", side_effect=command):
            self.assertEqual(
                VERIFY_RELEASE._download_release_assets(
                    self.root, REPOSITORY, "v%s" % VERSION
                ),
                expected,
            )

    def test_candidate_orchestrates_gates_refs_and_draft_comparison(self) -> None:
        artifacts = PACKAGE_RELEASE.ReleaseArtifacts(
            files={"asset": b"bytes"}, manifest={"version": VERSION}
        )
        metadata = {
            "tag_name": "v%s" % VERSION,
            "draft": True,
            "immutable": False,
        }
        with patch.object(VERIFY_RELEASE, "_run_local_gates") as gates, patch.object(
            VERIFY_RELEASE, "_build_reproducible_assets", return_value=artifacts
        ) as build, patch.object(
            VERIFY_RELEASE, "_verify_remote_refs", return_value=MAIN_COMMIT
        ) as refs, patch.object(
            VERIFY_RELEASE, "_draft_release_metadata", return_value=metadata
        ) as release, patch.object(
            VERIFY_RELEASE, "_download_release_assets", return_value=dict(artifacts.files)
        ) as download:
            with redirect_stdout(io.StringIO()):
                VERIFY_RELEASE.verify_candidate(
                    self.root,
                    version=VERSION,
                    source_commit=SOURCE_COMMIT,
                    repository=REPOSITORY,
                    origin_remote="origin",
                    github_remote="github",
                )
        gates.assert_called_once_with(self.root.resolve(), SOURCE_COMMIT)
        build.assert_called_once()
        refs.assert_called_once()
        release.assert_called_once_with(self.root.resolve(), REPOSITORY, "v%s" % VERSION)
        download.assert_called_once_with(self.root.resolve(), REPOSITORY, "v%s" % VERSION)

    def test_published_requires_latest_identity_and_runs_e2e(self) -> None:
        artifacts = PACKAGE_RELEASE.ReleaseArtifacts(
            files={"installer.py": b"installer", "asset": b"bytes"},
            manifest={"version": VERSION, "locales": {}},
        )
        metadata = {
            "id": 42,
            "tag_name": "v%s" % VERSION,
            "draft": False,
            "immutable": True,
            "prerelease": False,
        }
        release_url = "https://github.com/%s/releases" % REPOSITORY
        with patch.object(
            VERIFY_RELEASE.package_release, "verify_source_revision"
        ) as source, patch.object(
            VERIFY_RELEASE.package_release,
            "build_release_artifacts",
            return_value=artifacts,
        ), patch.object(
            VERIFY_RELEASE, "_verify_remote_refs", return_value=MAIN_COMMIT
        ), patch.object(
            VERIFY_RELEASE, "_release_metadata", return_value=metadata
        ), patch.object(
            VERIFY_RELEASE, "_latest_release_metadata", return_value=dict(metadata)
        ), patch.object(
            VERIFY_RELEASE, "_download_release_assets", return_value=dict(artifacts.files)
        ), patch.object(VERIFY_RELEASE, "_verify_published_e2e") as e2e:
            with redirect_stdout(io.StringIO()):
                VERIFY_RELEASE.verify_published(
                    self.root,
                    version=VERSION,
                    source_commit=SOURCE_COMMIT,
                    repository=REPOSITORY,
                    release_url=release_url,
                    origin_remote="origin",
                    github_remote="github",
                )
        self.assertEqual(source.call_count, 2)
        e2e.assert_called_once_with(
            self.root.resolve(),
            release_url=release_url,
            version=VERSION,
            artifacts=artifacts,
        )

        stale = dict(metadata, id=99, tag_name="v2.0.0")
        with patch.object(
            VERIFY_RELEASE.package_release, "verify_source_revision"
        ), patch.object(
            VERIFY_RELEASE.package_release,
            "build_release_artifacts",
            return_value=artifacts,
        ), patch.object(
            VERIFY_RELEASE, "_verify_remote_refs", return_value=MAIN_COMMIT
        ), patch.object(
            VERIFY_RELEASE, "_release_metadata", return_value=metadata
        ), patch.object(
            VERIFY_RELEASE, "_latest_release_metadata", return_value=stale
        ), patch.object(
            VERIFY_RELEASE, "_download_release_assets", return_value=dict(artifacts.files)
        ):
            with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "not the current"):
                VERIFY_RELEASE.verify_published(
                    self.root,
                    version=VERSION,
                    source_commit=SOURCE_COMMIT,
                    repository=REPOSITORY,
                    release_url=release_url,
                    origin_remote="origin",
                    github_remote="github",
                )

    def test_published_e2e_compares_all_materializations_and_preserves_targets(self) -> None:
        members = {"AGENTS.md": b"agents\n", "README.md": b"readme\n"}
        archive = PACKAGE_RELEASE._zip_bytes(tuple(sorted(members.items())))
        artifacts = PACKAGE_RELEASE.ReleaseArtifacts(
            files={"installer.py": b"installer", "locale.zip": archive},
            manifest={
                "version": VERSION,
                "locales": {"ko": {"asset": "locale.zip"}},
            },
        )

        def write_members(root: Path) -> None:
            root.mkdir(parents=True, exist_ok=True)
            for name, data in members.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                target.chmod(0o644)

        def source_export(_root, _locale, output, **_kwargs):
            write_members(Path(output))
            return tuple(sorted(members))

        invoked_installer_bytes = []

        def command(arguments, *, cwd):
            self.assertGreaterEqual(len(arguments), 4)
            installer_path = Path(arguments[2])
            invoked_installer_bytes.append(installer_path.read_bytes())
            command_name = arguments[3]
            if command_name == "list-locales":
                return ("Release %s (source commit fixture)\n" % VERSION).encode()
            if command_name == "install":
                root = Path(arguments[arguments.index("--repo-root") + 1])
                if (root / "AGENTS.md").exists():
                    raise VERIFY_RELEASE.VerificationError(
                        "verification command failed: 1 conflicting path(s)"
                    )
                write_members(root)
                return b""
            if command_name == "export":
                write_members(Path(arguments[arguments.index("--output") + 1]))
                return b""
            if command_name == "adopt":
                output = Path(arguments[arguments.index("--output") + 1])
                write_members(output / "artifact")
                (output / "adoption-plan.json").write_text(
                    '{"summary":{"missing":1,"identical":0,"merge":1,'
                    '"decision":0,"blocked":0}}',
                    encoding="utf-8",
                )
                return b""
            self.fail("unexpected command: %r" % (arguments,))

        with patch.object(
            VERIFY_RELEASE.export_template, "export_locale", side_effect=source_export
        ), patch.object(
            VERIFY_RELEASE, "_command", side_effect=command
        ), patch.object(VERIFY_RELEASE, "_check_artifact") as artifact_check:
            VERIFY_RELEASE._verify_published_e2e(
                self.root,
                release_url="https://example.test/releases",
                version=VERSION,
                artifacts=artifacts,
            )
        self.assertTrue(invoked_installer_bytes)
        self.assertEqual(set(invoked_installer_bytes), {b"installer"})
        self.assertEqual(artifact_check.call_count, 1)

    def test_remote_names_reject_option_or_url_injection(self) -> None:
        for value in ("--upload-pack=bad", "https://example.test/repo", "bad name"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(VERIFY_RELEASE.VerificationError, "remote"):
                    VERIFY_RELEASE._validated_remote_name(value)

    def test_cli_help_exposes_only_candidate_and_published_verification(self) -> None:
        completed = __import__("subprocess").run(
            [
                sys.executable,
                str(REPOSITORY_ROOT / "scripts/verify-release.py"),
                "--help",
            ],
            stdout=__import__("subprocess").PIPE,
            stderr=__import__("subprocess").PIPE,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("{candidate,published}", completed.stdout)


if __name__ == "__main__":
    unittest.main()
