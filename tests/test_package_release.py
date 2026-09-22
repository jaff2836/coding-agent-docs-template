from __future__ import annotations

import hashlib
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
import export_template as EXPORT_TEMPLATE  # noqa: E402
import package_release as PACKAGE_RELEASE  # noqa: E402


# The packager requires the release version to equal the guides' Template version.
SOURCE_VERSION = PACKAGE_RELEASE.TEMPLATE_VERSION_RE.search(
    (REPOSITORY_ROOT / "locales/en/docs/TEMPLATE_GUIDE.md").read_text(encoding="utf-8")
).group(1)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ignore_generated(_directory: str, names: list[str]) -> list[str]:
    return [name for name in names if name == "__pycache__" or name.endswith(".pyc")]


class PackageReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="template-package-test-")
        self.temp_root = Path(self.temporary.name)
        self.repository = self.temp_root / "repository"
        shutil.copytree(
            REPOSITORY_ROOT / "locales",
            self.repository / "locales",
            ignore=_ignore_generated,
        )
        shutil.copytree(
            REPOSITORY_ROOT / "template",
            self.repository / "template",
            ignore=_ignore_generated,
        )
        self.installer = self.repository / "scripts/installer.py"
        self.installer.parent.mkdir()
        self.installer.write_bytes(
            b"#!/usr/bin/env python3\nraise SystemExit('fixture only')\n"
        )
        self.kwargs = {
            "version": SOURCE_VERSION,
            "source_commit": "a" * 40,
            "repository": "jaff2836/coding-agent-docs-template",
        }

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

    def build(self) -> PACKAGE_RELEASE.ReleaseArtifacts:
        return PACKAGE_RELEASE.build_release_artifacts(self.repository, **self.kwargs)

    def test_two_builds_are_byte_identical_and_manifest_bound(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(first.files, second.files)
        self.assertEqual(
            tuple(first.files),
            (
                "SHA256SUMS",
                "coding-agent-docs-template-en-v%s.zip" % SOURCE_VERSION,
                "coding-agent-docs-template-ko-v%s.zip" % SOURCE_VERSION,
                "installer.py",
                "release-manifest.json",
            ),
        )

        manifest = json.loads(first.files["release-manifest.json"])
        self.assertEqual(manifest["schema_version"], 2)
        self.assertEqual(manifest["version"], SOURCE_VERSION)
        self.assertEqual(manifest["source_commit"], "a" * 40)
        self.assertEqual(
            manifest["repository"], "jaff2836/coding-agent-docs-template"
        )
        self.assertEqual(tuple(manifest["locales"]), ("en", "ko"))
        self.assertEqual(
            manifest["installer"]["sha256"], _sha256(first.files["installer.py"])
        )

        checksum_lines = first.files["SHA256SUMS"].decode("ascii").splitlines()
        expected_names = sorted(name for name in first.files if name != "SHA256SUMS")
        self.assertEqual([line.split("  ", 1)[1] for line in checksum_lines], expected_names)
        for line in checksum_lines:
            digest, name = line.split("  ", 1)
            self.assertEqual(digest, _sha256(first.files[name]))

    def test_artifact_members_use_posix_relative_path_order(self) -> None:
        output = self.temp_root / "exported"
        EXPORT_TEMPLATE.export_locale(
            self.repository, "en", output, require_complete=True
        )
        path_type = type(output)

        def casefolded_native_order(left: Path, right: Path) -> bool:
            return left.as_posix().casefold() < right.as_posix().casefold()

        with patch.object(path_type, "__lt__", casefolded_native_order):
            members = PACKAGE_RELEASE._artifact_members(output)

        actual = tuple(path for path, _ in members)
        self.assertEqual(actual, tuple(sorted(actual)))

    def test_archives_have_exact_members_hashes_modes_and_timestamps(self) -> None:
        artifacts = self.build()
        manifest = artifacts.manifest
        policies = json.loads(
            (self.repository / "locales/manifest.json").read_text(encoding="utf-8")
        )["artifact"]["adoption_policy"]
        for locale, record in manifest["locales"].items():
            archive_data = artifacts.files[record["asset"]]
            self.assertEqual(record["sha256"], _sha256(archive_data))
            self.assertEqual(record["bytes"], len(archive_data))
            archive_path = self.temp_root / (locale + ".zip")
            archive_path.write_bytes(archive_data)
            with zipfile.ZipFile(archive_path) as archive:
                infos = archive.infolist()
                expected_paths = [item["path"] for item in record["members"]]
                self.assertEqual(archive.namelist(), expected_paths)
                self.assertEqual(expected_paths, sorted(expected_paths))
                for info, member in zip(infos, record["members"]):
                    data = archive.read(info)
                    self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                    self.assertEqual(info.date_time, PACKAGE_RELEASE.ARCHIVE_TIMESTAMP)
                    self.assertEqual(stat.S_IMODE(info.external_attr >> 16), 0o644)
                    self.assertEqual(member["sha256"], _sha256(data))
                    self.assertEqual(member["bytes"], len(data))
                    self.assertEqual(member["mode"], 0o644)
                    self.assertEqual(
                        member["timestamp"], PACKAGE_RELEASE.ARCHIVE_TIMESTAMP_TEXT
                    )
                    self.assertEqual(member["policy"], policies[member["path"]])
                self.assertEqual(
                    {member["path"] for member in record["members"]}, set(policies)
                )

    def test_member_records_require_an_adoption_policy_for_every_path(self) -> None:
        members = (("LICENSE", b"license\n"), ("README.md", b"readme\n"))
        records = PACKAGE_RELEASE._member_records(
            members, {"LICENSE": "decide", "README.md": "merge"}
        )
        self.assertEqual([record["policy"] for record in records], ["decide", "merge"])
        with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, "no adoption policy: README.md"):
            PACKAGE_RELEASE._member_records(members, {"LICENSE": "decide"})

    def test_publishes_only_to_an_empty_directory(self) -> None:
        artifacts = self.build()
        output = self.temp_root / "release"
        output.mkdir()
        names = PACKAGE_RELEASE.write_release_artifacts(
            self.repository, output, artifacts
        )
        self.assertEqual(names, tuple(sorted(artifacts.files)))
        self.assertEqual(
            tuple(sorted(path.name for path in output.iterdir())), names
        )

        occupied = self.temp_root / "occupied"
        occupied.mkdir()
        (occupied / "keep").write_text("keep\n", encoding="utf-8")
        with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, "empty directory"):
            PACKAGE_RELEASE.write_release_artifacts(
                self.repository, occupied, artifacts
            )
        self.assertEqual((occupied / "keep").read_text(encoding="utf-8"), "keep\n")

        unsafe = PACKAGE_RELEASE.ReleaseArtifacts(
            files={"../escape": b"bad"}, manifest={}
        )
        unsafe_output = self.temp_root / "unsafe-release"
        with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, "safe basename"):
            PACKAGE_RELEASE.write_release_artifacts(
                self.repository, unsafe_output, unsafe
            )
        self.assertFalse((self.temp_root / "escape").exists())

    def test_rejects_a_symlink_output_without_touching_its_target(self) -> None:
        artifacts = self.build()
        target = self.temp_root / "target"
        target.mkdir()
        linked = self.temp_root / "linked-release"
        self.symlink_or_skip(linked, target, target_is_directory=True)
        with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, "symlink"):
            PACKAGE_RELEASE.write_release_artifacts(
                self.repository, linked, artifacts
            )
        self.assertEqual(tuple(target.iterdir()), ())

    def test_stable_gate_rejects_an_incomplete_required_locale(self) -> None:
        fixture = self.temp_root / "incomplete-repository"
        shutil.copytree(
            REPOSITORY_ROOT / "locales", fixture / "locales", ignore=_ignore_generated
        )
        shutil.copytree(
            REPOSITORY_ROOT / "template", fixture / "template", ignore=_ignore_generated
        )
        fixture_installer = fixture / "scripts/installer.py"
        fixture_installer.parent.mkdir()
        shutil.copy2(self.installer, fixture_installer)
        manifest_path = fixture / "locales/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["locales"]["en"]["status"] = "experimental"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        with self.assertRaisesRegex(EXPORT_TEMPLATE.ExportError, "is not complete"):
            PACKAGE_RELEASE.build_release_artifacts(fixture, **self.kwargs)

    def test_rejects_invalid_release_identity_and_installer(self) -> None:
        cases = (
            ({"version": "v2.0.0"}, "SemVer"),
            ({"version": "2.0.1"}, "does not match release version"),
            ({"source_commit": "ABC"}, "40 lowercase"),
            ({"repository": "https://example.test/repo"}, "OWNER/NAME"),
        )
        for replacement, message in cases:
            with self.subTest(replacement=replacement):
                arguments = dict(self.kwargs)
                arguments.update(replacement)
                with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, message):
                    PACKAGE_RELEASE.build_release_artifacts(
                        self.repository, **arguments
                    )

        self.installer.write_bytes(b"print('crlf')\r\n")
        with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, "LF"):
            self.build()

    def test_source_revision_binding_requires_exact_clean_git_root(self) -> None:
        repository = self.temp_root / "git-repository"
        repository.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
        subprocess.run(
            ["git", "config", "user.email", "fixture@example.test"],
            cwd=repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture"], cwd=repository, check=True
        )
        tracked = repository / "tracked.txt"
        tracked.write_text("clean\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=repository, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repository, check=True)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repository,
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout.strip()
        PACKAGE_RELEASE.verify_source_revision(repository, head)
        with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, "does not match"):
            PACKAGE_RELEASE.verify_source_revision(repository, "b" * 40)
        tracked.write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(PACKAGE_RELEASE.ReleaseError, "must be clean"):
            PACKAGE_RELEASE.verify_source_revision(repository, head)

    def test_schema_and_cli_help_are_available(self) -> None:
        schema = json.loads(
            (REPOSITORY_ROOT / "schemas/release-manifest.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["properties"]["schema_version"]["const"], 2)
        self.assertIn("policy", schema["$defs"]["member"]["required"])
        self.assertEqual(
            schema["$defs"]["member"]["properties"]["policy"]["enum"],
            ["copy", "decide", "merge"],
        )
        self.assertEqual(
            schema["properties"]["installer"]["properties"]["bytes"]["$ref"],
            "#/$defs/positiveInteger",
        )
        self.assertEqual(
            schema["$defs"]["member"]["properties"]["bytes"]["$ref"],
            "#/$defs/nonNegativeInteger",
        )
        completed = subprocess.run(
            [sys.executable, str(REPOSITORY_ROOT / "scripts/package-release.py"), "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--source-commit", completed.stdout)
        self.assertIn("--output", completed.stdout)


if __name__ == "__main__":
    unittest.main()
