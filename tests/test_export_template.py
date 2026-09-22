from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
import export_template as EXPORT_TEMPLATE  # noqa: E402


def _ignore_generated(_directory: str, names: list[str]) -> list[str]:
    return [name for name in names if name == "__pycache__" or name.endswith(".pyc")]


class ExportTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="template-export-test-")
        self.temp_root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def symlink_or_skip(
        self, link: Path, target: str | Path, *, target_is_directory: bool = False
    ) -> None:
        try:
            link.symlink_to(target, target_is_directory=target_is_directory)
        except (NotImplementedError, OSError) as exc:
            self.skipTest("symlink creation is unavailable: %s" % exc)

    def assert_materialized_file_mode(self, path: Path) -> None:
        mode = stat.S_IMODE(path.stat().st_mode)
        if os.name == "nt":
            self.assertTrue(mode & stat.S_IWRITE)
        else:
            self.assertEqual(mode, 0o644)

    def expected_paths(self) -> tuple[str, ...]:
        manifest = json.loads(
            (REPOSITORY_ROOT / "locales/manifest.json").read_text(encoding="utf-8")
        )
        return tuple(
            sorted(
                manifest["artifact"]["common_paths"]
                + manifest["artifact"]["localized_paths"]
            )
        )

    def test_exports_each_locale_with_exact_inventory_and_bytes(self) -> None:
        for locale in ("en", "ko"):
            with self.subTest(locale=locale):
                output = self.temp_root / locale
                members = EXPORT_TEMPLATE.export_locale(
                    REPOSITORY_ROOT, locale, output, require_complete=True
                )
                self.assertEqual(members, self.expected_paths())
                actual = tuple(
                    sorted(
                        path.relative_to(output).as_posix()
                        for path in output.rglob("*")
                        if path.is_file()
                    )
                )
                self.assertEqual(actual, members)
                self.assertFalse((output / "locales").exists())
                self.assertFalse((output / "docs/changes/2026-09-09-multilingual-template").exists())
                for relative in members:
                    source_root = (
                        REPOSITORY_ROOT / "template/common"
                        if (REPOSITORY_ROOT / "template/common" / relative).is_file()
                        else REPOSITORY_ROOT / "locales" / locale
                    )
                    target = output / relative
                    self.assertEqual(target.read_bytes(), (source_root / relative).read_bytes())
                    self.assert_materialized_file_mode(target)

                completed = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "unittest",
                        "discover",
                        "-s",
                        "tests",
                        "-p",
                        "test_check_docs.py",
                        "-v",
                    ],
                    cwd=output,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_accepts_an_existing_empty_output(self) -> None:
        output = self.temp_root / "empty"
        output.mkdir()
        EXPORT_TEMPLATE.export_locale(REPOSITORY_ROOT, "en", output)
        self.assertTrue((output / "AGENTS.md").is_file())

    def test_rejects_unsupported_locale_and_nonempty_output(self) -> None:
        with self.assertRaisesRegex(EXPORT_TEMPLATE.ExportError, "unsupported locale"):
            EXPORT_TEMPLATE.export_locale(REPOSITORY_ROOT, "fr", self.temp_root / "fr")

        output = self.temp_root / "occupied"
        output.mkdir()
        (output / "keep.txt").write_text("keep\n", encoding="utf-8")
        with self.assertRaisesRegex(EXPORT_TEMPLATE.ExportError, "empty directory"):
            EXPORT_TEMPLATE.export_locale(REPOSITORY_ROOT, "en", output)
        self.assertEqual((output / "keep.txt").read_text(encoding="utf-8"), "keep\n")

    def test_source_failure_does_not_publish_partial_output(self) -> None:
        fixture = self.temp_root / "repository"
        shutil.copytree(
            REPOSITORY_ROOT / "locales", fixture / "locales", ignore=_ignore_generated
        )
        shutil.copytree(
            REPOSITORY_ROOT / "template", fixture / "template", ignore=_ignore_generated
        )
        (fixture / "locales/en/README.md").unlink()
        output = self.temp_root / "failed-output"
        with self.assertRaisesRegex(EXPORT_TEMPLATE.ExportError, "missing source file"):
            EXPORT_TEMPLATE.export_locale(fixture, "en", output)
        self.assertFalse(output.exists())

    def test_rejects_output_inside_source_repository(self) -> None:
        with self.assertRaisesRegex(EXPORT_TEMPLATE.ExportError, "outside"):
            EXPORT_TEMPLATE.export_locale(
                REPOSITORY_ROOT, "en", REPOSITORY_ROOT / "generated-artifact"
            )

    def test_rejects_a_symlink_output_without_touching_its_target(self) -> None:
        target = self.temp_root / "target"
        target.mkdir()
        output = self.temp_root / "linked-output"
        self.symlink_or_skip(output, target, target_is_directory=True)
        with self.assertRaisesRegex(EXPORT_TEMPLATE.ExportError, "symlink"):
            EXPORT_TEMPLATE.export_locale(REPOSITORY_ROOT, "en", output)
        self.assertEqual(tuple(target.iterdir()), ())

    def test_cli_help_is_available(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(REPOSITORY_ROOT / "scripts/export-template.py"), "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--locale", completed.stdout)


if __name__ == "__main__":
    unittest.main()
