import importlib.util
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "verify_published_release", ROOT / ".buildkite" / "verify_published_release.py"
)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)

SOURCE = "6d04b97a2e2fc3da0f007b11a4cc1539bb2b57db"


class ReadInputsTest(unittest.TestCase):
    def test_accepts_release_with_base(self) -> None:
        inputs = helper.read_inputs(
            {
                "RELEASE_VERIFY_VERSION": "2.5.0",
                "RELEASE_VERIFY_SOURCE_COMMIT": SOURCE,
                "RELEASE_VERIFY_BASE_VERSION": "2.4.0",
            }
        )
        self.assertEqual(inputs, ("2.5.0", SOURCE, "2.4.0"))

    def test_base_version_is_optional(self) -> None:
        inputs = helper.read_inputs(
            {"RELEASE_VERIFY_VERSION": "2.5.0", "RELEASE_VERIFY_SOURCE_COMMIT": SOURCE}
        )
        self.assertIsNone(inputs[2])

    def test_rejects_a_version_that_would_change_the_fetch_refspec(self) -> None:
        for version in ("2.5.0:refs/heads/main", "v2.5.0", "2.5", "2.5.0-rc.1", ""):
            with self.subTest(version=version):
                with self.assertRaises(helper.InputError):
                    helper.read_inputs(
                        {
                            "RELEASE_VERIFY_VERSION": version,
                            "RELEASE_VERIFY_SOURCE_COMMIT": SOURCE,
                        }
                    )

    def test_rejects_abbreviated_or_uppercase_commits(self) -> None:
        for source in (SOURCE[:12], SOURCE.upper(), ""):
            with self.subTest(source=source):
                with self.assertRaises(helper.InputError):
                    helper.read_inputs(
                        {"RELEASE_VERIFY_VERSION": "2.5.0", "RELEASE_VERIFY_SOURCE_COMMIT": source}
                    )

    def test_rejects_a_malformed_base_version(self) -> None:
        with self.assertRaises(helper.InputError):
            helper.read_inputs(
                {
                    "RELEASE_VERIFY_VERSION": "2.5.0",
                    "RELEASE_VERIFY_SOURCE_COMMIT": SOURCE,
                    "RELEASE_VERIFY_BASE_VERSION": "2.4.0;rm",
                }
            )


class MainTest(unittest.TestCase):
    def test_invalid_input_stops_before_any_command(self) -> None:
        with mock.patch.object(helper.subprocess, "run") as run:
            code = helper.main({"RELEASE_VERIFY_VERSION": "2.5.0:refs/heads/main"})
        self.assertEqual(code, 2)
        run.assert_not_called()

    def test_verifier_command_passes_base_version_only_when_set(self) -> None:
        worktree = Path("source")
        with_base = helper.verifier_command("python", worktree, "2.5.0", SOURCE, "2.4.0")
        without_base = helper.verifier_command("python", worktree, "2.5.0", SOURCE, None)
        self.assertEqual(with_base[-2:], ["--base-version", "2.4.0"])
        self.assertNotIn("--base-version", without_base)
        self.assertEqual(with_base[2], "published")


if __name__ == "__main__":
    unittest.main()
