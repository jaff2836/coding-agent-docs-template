from __future__ import annotations

import hashlib
import http.server
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
import installer as INSTALLER  # noqa: E402
import package_release as PACKAGE_RELEASE  # noqa: E402


REAL_INSTALLER_BYTES = (REPOSITORY_ROOT / "scripts/installer.py").read_bytes()
VERSION_DIR = "/releases/2.0.0"
DEFAULT_MEMBERS = {
    "AGENTS.md": b"# agent contract\n",
    "README.md": b"# project readme\n",
    "docs/REVIEW.md": b"# review policy\n",
    ".agents/skills/design/SKILL.md": b"---\nname: design\n---\nbody\n",
}
DEFAULT_POLICIES = {
    "AGENTS.md": "merge",
    "README.md": "merge",
    "docs/REVIEW.md": "merge",
    ".agents/skills/design/SKILL.md": "copy",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _tree_state(root: Path) -> tuple[tuple[str, int], ...]:
    state = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            state.append((relative, -2))
        elif path.is_dir():
            state.append((relative, -1))
        else:
            state.append((relative, stat.S_IMODE(path.lstat().st_mode)))
    return tuple(state)


def _tree_snapshot(root: Path) -> tuple[tuple[str, str, int, bytes], ...]:
    """Capture paths, kinds, modes, file bytes and symlink targets under *root*."""

    snapshot = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            snapshot.append((relative, "symlink", mode, os.readlink(path).encode()))
        elif path.is_dir():
            snapshot.append((relative, "dir", mode, b""))
        else:
            snapshot.append((relative, "file", mode, path.read_bytes()))
    return tuple(snapshot)


def build_release_payloads(
    *,
    locale: str = "ko",
    members: dict[str, bytes] | None = None,
    policies: dict[str, str] | None = None,
    version: str = "2.0.0",
    source_commit: str = "a" * 40,
    archive: bytes | None = None,
    locale_record_overrides: dict | None = None,
    installer_record_overrides: dict | None = None,
    sums: bytes | None = None,
    schema_version: int = 2,
    repository: str = "jaff2836/coding-agent-docs-template",
    installer_bytes: bytes = REAL_INSTALLER_BYTES,
    publish_latest: bool = True,
) -> dict[str, bytes]:
    """Build a synthetic release asset map mirroring package-release output."""

    member_items = tuple(sorted((members or DEFAULT_MEMBERS).items()))
    member_policies = {
        path: (policies or {}).get(path, DEFAULT_POLICIES.get(path, "copy"))
        for path, _ in member_items
    }
    if archive is None:
        archive = PACKAGE_RELEASE._zip_bytes(member_items)
    member_records = PACKAGE_RELEASE._member_records(member_items, member_policies)
    if schema_version == 1:
        member_records = [
            {key: value for key, value in member.items() if key != "policy"}
            for member in member_records
        ]
    locale_record = {
        "status": "complete",
        "asset": "coding-agent-docs-template-%s-v%s.zip" % (locale, version),
        "sha256": _sha256(archive),
        "bytes": len(archive),
        "compression": "stored",
        "members": member_records,
    }
    locale_record.update(locale_record_overrides or {})
    installer_record = {
        "asset": "installer.py",
        "sha256": _sha256(installer_bytes),
        "bytes": len(installer_bytes),
    }
    installer_record.update(installer_record_overrides or {})
    manifest = {
        "schema_version": schema_version,
        "version": version,
        "source_commit": source_commit,
        "repository": repository,
        "locales": {locale: locale_record},
        "installer": installer_record,
    }
    manifest_data = (
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")
    if sums is None:
        names = sorted(["release-manifest.json", "installer.py", locale_record["asset"]])
        digests = {
            "release-manifest.json": _sha256(manifest_data),
            "installer.py": _sha256(installer_bytes),
            locale_record["asset"]: _sha256(archive),
        }
        sums = "".join("%s  %s\n" % (digests[name], name) for name in names).encode("ascii")
    version_dir = "/releases/%s" % version
    payloads = {
        "%s/release-manifest.json" % version_dir: manifest_data,
        "%s/SHA256SUMS" % version_dir: sums,
        "%s/%s" % (version_dir, locale_record["asset"]): archive,
        "%s/installer.py" % version_dir: installer_bytes,
    }
    if publish_latest:
        payloads["/releases/latest/release-manifest.json"] = manifest_data
    return payloads


class FakeReleaseServer:
    """Serve release assets from an in-memory path map on localhost."""

    def __init__(
        self,
        payloads: dict[str, bytes],
        redirects: dict[str, str] | None = None,
    ) -> None:
        served = payloads
        redirected = redirects or {}
        self.requests: list[str] = []
        requests = self.requests

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                requests.append(self.path)
                location = redirected.get(self.path)
                if location is not None:
                    self.send_response(302)
                    self.send_header("Location", location)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                payload = served.get(self.path)
                if payload is None:
                    self.send_response(404)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *_args) -> None:
                pass

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def base_url(self) -> str:
        return "http://127.0.0.1:%d/releases" % self.server.server_port

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="template-install-test-")
        self.addCleanup(self.temporary.cleanup)

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

    def assert_materialized_file_mode(self, path: Path) -> None:
        mode = stat.S_IMODE(path.lstat().st_mode)
        if os.name == "nt":
            self.assertTrue(mode & stat.S_IWRITE)
        else:
            self.assertEqual(mode, 0o644)

    def publish(self, **overrides) -> str:
        payloads = build_release_payloads(**overrides)
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)
        return server.base_url

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(REPOSITORY_ROOT / "scripts/installer.py"), *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

    # -- success paths -----------------------------------------------------

    def test_builds_github_latest_and_exact_release_asset_urls(self) -> None:
        release_url = "https://github.com/jaff2836/coding-agent-docs-template/releases"
        self.assertEqual(
            INSTALLER._validated_release_url(release_url + "/"),
            release_url,
        )
        self.assertEqual(
            INSTALLER._asset_url(release_url, "latest", "installer.py"),
            release_url + "/latest/download/installer.py",
        )
        self.assertEqual(
            INSTALLER._asset_url(release_url, "2.0.0", "release-manifest.json"),
            release_url + "/download/v2.0.0/release-manifest.json",
        )
        self.assertTrue(
            INSTALLER._is_github_release_asset_url(
                release_url + "/latest/download/installer.py"
            )
        )
        self.assertTrue(
            INSTALLER._is_github_release_asset_url(
                release_url + "/download/v2.0.0/release-manifest.json"
            )
        )
        self.assertFalse(
            INSTALLER._is_github_release_asset_url(
                release_url + "/latest/download/installer.py?unexpected=1"
            )
        )

    def test_github_redirect_handler_allows_only_its_https_chain(self) -> None:
        initial = (
            "https://github.com/jaff2836/coding-agent-docs-template/"
            "releases/latest/download/installer.py"
        )
        handler = INSTALLER._GitHubReleaseRedirects(initial)
        first = handler.redirect_request(
            urllib.request.Request(initial),
            None,
            302,
            "Found",
            {},
            "https://release-assets.githubusercontent.com/signed?token=value",
        )
        self.assertIsNotNone(first)
        second = handler.redirect_request(
            first,
            None,
            302,
            "Found",
            {},
            "https://objects.githubusercontent.com/final",
        )
        self.assertIsNotNone(second)
        self.assertIsNone(
            handler.redirect_request(
                urllib.request.Request("https://example.invalid/untrusted"),
                None,
                302,
                "Found",
                {},
                "https://objects.githubusercontent.com/final",
            )
        )
        self.assertIsNone(
            handler.redirect_request(
                urllib.request.Request(initial),
                None,
                302,
                "Found",
                {},
                "http://release-assets.githubusercontent.com/insecure",
            )
        )
        self.assertIsNone(
            handler.redirect_request(
                urllib.request.Request(initial),
                None,
                302,
                "Found",
                {},
                "https://user:secret@example.invalid/asset",
            )
        )

    def test_install_writes_the_verified_locale_into_the_target_root(self) -> None:
        base = self.publish()
        target = self.temp_root() / "project"
        completed = self.run_cli(
            "install",
            "--release-url",
            base,
            "--version",
            "2.0.0",
            "--locale",
            "ko",
            "--repo-root",
            str(target),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Installed ko locale with 4 files", completed.stdout)
        self.assertEqual((target / "AGENTS.md").read_bytes(), b"# agent contract\n")
        self.assert_materialized_file_mode(target / "docs/REVIEW.md")

    def test_install_resolves_latest_through_the_immutable_namespace(self) -> None:
        base = self.publish()
        target = self.temp_root() / "project"
        completed = self.run_cli(
            "install",
            "--release-url",
            base,
            "--version",
            "latest",
            "--locale",
            "ko",
            "--repo-root",
            str(target),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue((target / "AGENTS.md").exists())

    def test_export_materializes_a_verified_artifact_into_an_empty_directory(self) -> None:
        base = self.publish()
        output = self.temp_root() / "exported"
        completed = self.run_cli(
            "export",
            "--release-url",
            base,
            "--version",
            "2.0.0",
            "--locale",
            "ko",
            "--output",
            str(output),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue((output / ".agents/skills/design/SKILL.md").exists())

    def test_list_locales_reports_release_identity_and_status(self) -> None:
        base = self.publish()
        completed = self.run_cli(
            "list-locales",
            "--release-url",
            base,
            "--version",
            "2.0.0",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Release 2.0.0 (source commit %s" % ("a" * 40), completed.stdout)
        self.assertIn("ko: complete", completed.stdout)

    # -- target protection -------------------------------------------------

    def test_install_refuses_conflicts_and_preserves_the_target_tree(self) -> None:
        base = self.publish()
        target = self.temp_root() / "project"
        target.mkdir()
        existing = target / "AGENTS.md"
        existing.write_bytes(b"# user document\n")
        readme = target / "README.md"
        readme.write_bytes(b"# user readme\n")
        nested = target / "docs"
        nested.mkdir()
        (nested / "keep.txt").write_bytes(b"keep\n")
        before = _tree_state(target)
        completed = self.run_cli(
            "install",
            "--release-url",
            base,
            "--version",
            "2.0.0",
            "--locale",
            "ko",
            "--repo-root",
            str(target),
        )
        self.assertEqual(completed.returncode, 1)
        self.assertIn("AGENTS.md", completed.stderr)
        self.assertIn("README.md", completed.stderr)
        self.assertIn("2 conflicting path(s)", completed.stderr)
        self.assertIn("run 'adopt'", completed.stderr)
        self.assertEqual(existing.read_bytes(), b"# user document\n")
        self.assertEqual(readme.read_bytes(), b"# user readme\n")
        self.assertEqual((nested / "keep.txt").read_bytes(), b"keep\n")
        self.assertEqual(_tree_state(target), before)

    def test_install_rejects_a_symlinked_target_root(self) -> None:
        base = self.publish()
        target = self.temp_root() / "elsewhere"
        target.mkdir()
        link = self.temp_root() / "project"
        self.symlink_or_skip(link, target, target_is_directory=True)
        completed = self.run_cli(
            "install",
            "--release-url",
            base,
            "--version",
            "2.0.0",
            "--locale",
            "ko",
            "--repo-root",
            str(link),
        )
        self.assertEqual(completed.returncode, 1)
        self.assertIn("symlink", completed.stderr)
        self.assertEqual(_tree_state(target), ())

    def test_export_refuses_a_nonempty_output_directory(self) -> None:
        base = self.publish()
        output = self.temp_root() / "exported"
        output.mkdir()
        marker = output / "user.md"
        marker.write_bytes(b"user content\n")
        before = _tree_state(output)
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER.export_artifact(base, "2.0.0", "ko", output)
        self.assertIn("empty", str(context.exception))
        self.assertEqual(_tree_state(output), before)
        self.assertEqual(marker.read_bytes(), b"user content\n")

    # -- adoption ------------------------------------------------------------

    ADOPTION_MEMBERS = {
        ".agents/skills/design/SKILL.md": b"skill\n",
        ".cursor/BUGBOT.md": b"# bugbot\n",
        ".omp/WATCHDOG.md": b"# watchdog\n",
        "AGENTS.md": b"# agent contract\n",
        "LICENSE": b"template license\n",
        "README.md": b"# template readme\n",
        "docs/01-DESIGN.md": b"# design procedure\n",
        "docs/CI.md": b"# ci\n",
        "docs/REVIEW.md": b"# review policy\n",
        "scripts/check-docs.py": b"print('check')\n",
        "tests/test_check_docs.py": b"# tests\n",
    }
    ADOPTION_POLICIES = {
        ".agents/skills/design/SKILL.md": "copy",
        ".cursor/BUGBOT.md": "decide",
        ".omp/WATCHDOG.md": "decide",
        "AGENTS.md": "merge",
        "LICENSE": "decide",
        "README.md": "merge",
        "docs/01-DESIGN.md": "copy",
        "docs/CI.md": "merge",
        "docs/REVIEW.md": "merge",
        "scripts/check-docs.py": "copy",
        "tests/test_check_docs.py": "copy",
    }

    def publish_adoption_release(self) -> str:
        return self.publish(members=self.ADOPTION_MEMBERS, policies=self.ADOPTION_POLICIES)

    def existing_repository(self) -> Path:
        root = self.temp_root() / "existing"
        root.mkdir()
        (root / "AGENTS.md").write_bytes(b"# agent contract\n")
        (root / "README.md").write_bytes(b"# existing project\n")
        (root / ".cursor").mkdir()
        (root / ".cursor/BUGBOT.md").write_bytes(b"# project bugbot\n")
        (root / "docs").mkdir()
        (root / "docs/01-DESIGN.md").write_bytes(b"# customized design\n")
        (root / "docs/ci.md").write_bytes(b"# lowercase ci\n")
        outside = self.temp_root() / "outside-skills"
        outside.mkdir()
        (outside / "keep.md").write_bytes(b"outside\n")
        self.symlink_or_skip(
            root / ".agents", outside, target_is_directory=True
        )
        (root / ".omp").mkdir()
        self.symlink_or_skip(root / ".omp/WATCHDOG.md", outside / "keep.md")
        (root / "scripts").mkdir()
        (root / "scripts/check-docs.py").mkdir()
        (root / "tests").write_bytes(b"not a directory\n")
        (root / "src.py").write_bytes(b"print('app')\n")
        return root

    def test_adopt_classifies_every_path_without_modifying_the_target(self) -> None:
        base = self.publish_adoption_release()
        target = self.existing_repository()
        before = _tree_snapshot(target)
        outside_before = _tree_snapshot(self.temp_root() / "outside-skills")
        output = self.temp_root() / "adoption"
        completed = self.run_cli(
            "adopt",
            "--release-url",
            base,
            "--version",
            "2.0.0",
            "--locale",
            "ko",
            "--repo-root",
            str(target),
            "--output",
            str(output),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(_tree_snapshot(target), before)
        self.assertEqual(_tree_snapshot(self.temp_root() / "outside-skills"), outside_before)
        self.assertIn("The target repository was not modified", completed.stdout)
        self.assertTrue(
            completed.stdout.startswith(
                "Adoption plan for ko 2.0.0: 11 paths "
                "(missing 1, identical 1, merge 2, decision 2, blocked 5)\n"
            )
        )
        self.assertNotIn("Upgrade classification", completed.stdout)
        self.assertEqual(sorted(path.name for path in output.iterdir()), ["adoption-plan.json", "artifact"])
        for name, data in self.ADOPTION_MEMBERS.items():
            self.assertEqual((output / "artifact" / name).read_bytes(), data)

        plan = json.loads((output / "adoption-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["format"], "coding-agent-docs-template/adoption-plan")
        self.assertEqual(plan["format_version"], 1)
        self.assertEqual(plan["stability"], "experimental")
        self.assertEqual(
            plan["release"],
            {
                "repository": "jaff2836/coding-agent-docs-template",
                "version": "2.0.0",
                "source_commit": "a" * 40,
                "locale": "ko",
            },
        )
        entries = {entry["path"]: entry for entry in plan["paths"]}
        self.assertEqual([entry["path"] for entry in plan["paths"]], sorted(entries))
        expected = {
            ".agents/skills/design/SKILL.md": ("blocked", "parent-symlink"),
            ".cursor/BUGBOT.md": ("decision", "file"),
            ".omp/WATCHDOG.md": ("blocked", "symlink"),
            "AGENTS.md": ("identical", "file"),
            "LICENSE": ("decision", "absent"),
            "README.md": ("merge", "file"),
            "docs/01-DESIGN.md": ("merge", "file"),
            "docs/CI.md": ("blocked", "case-variant"),
            "docs/REVIEW.md": ("missing", "absent"),
            "scripts/check-docs.py": ("blocked", "special"),
            "tests/test_check_docs.py": ("blocked", "parent-not-directory"),
        }
        self.assertEqual(
            {path: (entry["status"], entry["target"]) for path, entry in entries.items()},
            expected,
        )
        self.assertEqual(
            plan["summary"],
            {"missing": 1, "identical": 1, "merge": 2, "decision": 2, "blocked": 5},
        )
        self.assertEqual(entries["README.md"]["policy"], "merge")
        self.assertEqual(entries["README.md"]["target_sha256"], _sha256(b"# existing project\n"))
        self.assertEqual(
            entries["README.md"]["artifact_sha256"], _sha256(b"# template readme\n")
        )
        self.assertIsNone(entries["LICENSE"]["target_sha256"])
        self.assertIn("keep the existing content", entries["README.md"]["reason"])
        self.assertIn("start from the artifact version", entries["docs/01-DESIGN.md"]["reason"])
        self.assertIn("explicitly decides", entries["LICENSE"]["reason"])
        self.assertNotIn(str(target), (output / "adoption-plan.json").read_text(encoding="utf-8"))

        repeated = self.temp_root() / "adoption-latest"
        INSTALLER.adopt(base, "latest", "ko", target, repeated, installer_bytes=REAL_INSTALLER_BYTES)
        self.assertEqual(
            (repeated / "adoption-plan.json").read_bytes(),
            (output / "adoption-plan.json").read_bytes(),
        )
        self.assertEqual(_tree_snapshot(target), before)

    def test_adopt_requires_an_existing_repository_and_a_separate_output(self) -> None:
        base = self.publish_adoption_release()
        target = self.existing_repository()
        before = _tree_snapshot(target)
        for output in (target / "adoption", target / "docs" / "adoption"):
            with self.assertRaises(INSTALLER.InstallerError) as context:
                INSTALLER.adopt(base, "2.0.0", "ko", target, output)
            self.assertIn("outside the repository", str(context.exception))
        self.assertEqual(_tree_snapshot(target), before)

        empty = self.temp_root() / "empty-project"
        empty.mkdir()
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER.adopt(base, "2.0.0", "ko", empty, empty)
        self.assertIn("outside the repository", str(context.exception))

        missing = self.temp_root() / "missing-project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER.adopt(base, "2.0.0", "ko", missing, self.temp_root() / "out-a")
        self.assertIn("use 'install'", str(context.exception))
        self.assertFalse(missing.exists())

        link = self.temp_root() / "linked-project"
        self.symlink_or_skip(link, target, target_is_directory=True)
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER.adopt(base, "2.0.0", "ko", link, self.temp_root() / "out-b")
        self.assertIn("symlink", str(context.exception))
        self.assertFalse((self.temp_root() / "out-a").exists())
        self.assertFalse((self.temp_root() / "out-b").exists())

    def test_adopt_verifies_the_release_before_publishing(self) -> None:
        base = self.publish(
            members=self.ADOPTION_MEMBERS,
            policies=self.ADOPTION_POLICIES,
            locale_record_overrides={"sha256": "0" * 64},
        )
        target = self.existing_repository()
        before = _tree_snapshot(target)
        output = self.temp_root() / "adoption"
        with self.assertRaises(INSTALLER.InstallerError):
            INSTALLER.adopt(base, "2.0.0", "ko", target, output)
        self.assertFalse(output.exists())
        self.assertEqual(_tree_snapshot(target), before)

    def test_adopt_publish_failure_leaves_no_output_or_stage(self) -> None:
        base = self.publish_adoption_release()
        target = self.existing_repository()
        before = _tree_snapshot(target)
        output = self.temp_root() / "adoption"
        real_replace = os.replace

        def failing_replace(source, destination):
            raise OSError("simulated publish failure")

        INSTALLER.os.replace = failing_replace
        try:
            with self.assertRaises(INSTALLER.InstallerError) as context:
                INSTALLER.adopt(base, "2.0.0", "ko", target, output)
        finally:
            INSTALLER.os.replace = real_replace
        self.assertIn("cannot publish", str(context.exception))
        self.assertFalse(output.exists())
        self.assertEqual(
            [path.name for path in self.temp_root().iterdir() if path.name.startswith(".template-install-")],
            [],
        )
        self.assertEqual(_tree_snapshot(target), before)

    def test_adopt_marks_unreadable_directories_as_blocked(self) -> None:
        target = self.temp_root() / "project"
        (target / "docs").mkdir(parents=True)
        real_listdir = os.listdir

        def failing_listdir(path):
            if Path(path) == target / "docs":
                raise PermissionError("simulated unreadable directory")
            return real_listdir(path)

        INSTALLER.os.listdir = failing_listdir
        try:
            state = INSTALLER._adoption_target(
                target, INSTALLER.PurePosixPath("docs/REVIEW.md"), {}
            )
        finally:
            INSTALLER.os.listdir = real_listdir
        self.assertEqual(state, ("unreadable", None))
        self.assertEqual(INSTALLER._adoption_status("merge", "unreadable", None, "a" * 64), "blocked")

    def test_adopt_base_version_classifies_the_inventory_union(self) -> None:
        base_members = {
            "unchanged.md": b"same\n",
            "template.md": b"base\n",
            "project.md": b"same\n",
            "converged.md": b"base\n",
            "diverged.md": b"base\n",
            "removed-kept.md": b"old\n",
            "removed-deleted.md": b"old\n",
            "blocked.md": b"same\n",
        }
        current_members = {
            "unchanged.md": b"same\n",
            "template.md": b"current\n",
            "project.md": b"same\n",
            "converged.md": b"current\n",
            "diverged.md": b"current\n",
            "added.md": b"current\n",
            "blocked.md": b"same\n",
        }
        payloads = build_release_payloads(
            version="2.0.0",
            members=base_members,
            schema_version=1,
            installer_bytes=b"this is historical data, not Python\n",
            source_commit="b" * 40,
            publish_latest=False,
        )
        payloads.update(
            build_release_payloads(
                version="2.1.0",
                members=current_members,
                policies={name: "merge" for name in current_members},
                source_commit="c" * 40,
            )
        )
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)

        target = self.temp_root() / "upgrade-target"
        target.mkdir()
        target_values = {
            "unchanged.md": b"same\n",
            "template.md": b"base\n",
            "project.md": b"project\n",
            "converged.md": b"current\n",
            "diverged.md": b"project\n",
            "removed-kept.md": b"old\n",
        }
        for name, data in target_values.items():
            (target / name).write_bytes(data)
        outside = self.temp_root() / "outside-blocked"
        outside.write_bytes(b"outside\n")
        self.symlink_or_skip(target / "blocked.md", outside)
        before = _tree_snapshot(target)
        output = self.temp_root() / "upgrade-output"

        completed = self.run_cli(
            "adopt",
            "--release-url",
            server.base_url,
            "--version",
            "2.1.0",
            "--base-version",
            "2.0.0",
            "--locale",
            "ko",
            "--repo-root",
            str(target),
            "--output",
            str(output),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(_tree_snapshot(target), before)
        plan = json.loads((output / "adoption-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["format_version"], 2)
        self.assertEqual(plan["base_release"]["version"], "2.0.0")
        self.assertEqual(plan["release"]["version"], "2.1.0")
        entries = {entry["path"]: entry for entry in plan["paths"]}
        self.assertEqual([entry["path"] for entry in plan["paths"]], sorted(entries))
        self.assertEqual(
            {name: entry["upgrade_status"] for name, entry in entries.items()},
            {
                "added.md": "template-only",
                "blocked.md": "blocked",
                "converged.md": "converged",
                "diverged.md": "diverged",
                "project.md": "project-only",
                "removed-deleted.md": "converged",
                "removed-kept.md": "template-only",
                "template.md": "template-only",
                "unchanged.md": "unchanged",
            },
        )
        self.assertEqual(
            plan["summary"],
            {"missing": 1, "identical": 2, "merge": 3, "decision": 0, "blocked": 1},
        )
        self.assertEqual(
            plan["upgrade_summary"],
            {
                "unchanged": 1,
                "template-only": 3,
                "project-only": 1,
                "converged": 2,
                "diverged": 1,
                "blocked": 1,
            },
        )
        for name in ("removed-kept.md", "removed-deleted.md"):
            self.assertIsNone(entries[name]["policy"])
            self.assertIsNone(entries[name]["status"])
            self.assertIsNone(entries[name]["artifact_sha256"])
            self.assertIn("absent from the current release", entries[name]["reason"])
        self.assertEqual(
            sorted(path.relative_to(output / "artifact").as_posix() for path in (output / "artifact").rglob("*") if path.is_file()),
            sorted(current_members),
        )
        lines = completed.stdout.splitlines()
        self.assertTrue(lines[0].startswith("Upgrade classification assumes"))
        self.assertIn("Adoption plan for ko 2.1.0: 7 paths", completed.stdout)
        self.assertIn("Upgrade classification: 9 paths", completed.stdout)
        headings = [
            line
            for line in lines
            if line.startswith("upgrade ") and line.endswith(":")
        ]
        self.assertEqual(
            headings,
            [
                "upgrade template-only:",
                "upgrade project-only:",
                "upgrade converged:",
                "upgrade diverged:",
                "upgrade blocked:",
            ],
        )

    def test_base_version_uses_semver_precedence(self) -> None:
        ordered = (
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-alpha.beta",
            "1.0.0-beta",
            "1.0.0-beta.2",
            "1.0.0-beta.11",
            "1.0.0-rc.1",
            "1.0.0",
        )
        for lower, higher in zip(ordered, ordered[1:]):
            with self.subTest(lower=lower, higher=higher):
                self.assertLess(INSTALLER._compare_semver_precedence(lower, higher), 0)
                self.assertGreater(INSTALLER._compare_semver_precedence(higher, lower), 0)
        self.assertEqual(
            INSTALLER._compare_semver_precedence("1.0.0+build.1", "1.0.0+build.2"),
            0,
        )
        for value in ("latest", "v1.0.0", "1.0"):
            with self.subTest(value=value):
                with self.assertRaises(INSTALLER.InstallerError):
                    INSTALLER._validated_base_version(value)
        for base, current in (("2.1.0", "2.1.0"), ("2.2.0", "2.1.0"), ("2.1.0+old", "2.1.0+new")):
            with self.subTest(base=base, current=current):
                with self.assertRaises(INSTALLER.InstallerError):
                    INSTALLER._require_older_base_version(base, current)

    def test_invalid_base_versions_leave_target_and_output_unchanged(self) -> None:
        payloads = build_release_payloads(
            version="2.1.0",
            members={"AGENTS.md": b"current\n"},
            policies={"AGENTS.md": "merge"},
        )
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)
        target = self.temp_root() / "invalid-base-target"
        target.mkdir()
        (target / "keep.txt").write_bytes(b"keep\n")
        before = _tree_snapshot(target)
        for index, base_version in enumerate(
            ("latest", "v2.0.0", "2.0", "2.1.0", "2.2.0")
        ):
            output = self.temp_root() / ("invalid-base-output-%d" % index)
            with self.subTest(base_version=base_version):
                with self.assertRaises(INSTALLER.InstallerError):
                    INSTALLER.adopt(
                        server.base_url,
                        "2.1.0",
                        "ko",
                        target,
                        output,
                        installer_bytes=REAL_INSTALLER_BYTES,
                        base_version=base_version,
                    )
                self.assertFalse(output.exists())
                self.assertEqual(_tree_snapshot(target), before)

    def test_base_release_requires_exact_assets_and_keeps_failures_read_only(self) -> None:
        base_payloads = build_release_payloads(
            version="2.0.0",
            members={"AGENTS.md": b"base\n"},
            schema_version=1,
            installer_bytes=b"historical installer bytes\n",
            publish_latest=False,
        )
        sums_path = "/releases/2.0.0/SHA256SUMS"
        base_payloads[sums_path] += ("0" * 64 + "  unexpected.sig\n").encode("ascii")
        base_payloads.update(
            build_release_payloads(
                version="2.1.0",
                members={"AGENTS.md": b"current\n"},
                policies={"AGENTS.md": "merge"},
            )
        )
        server = FakeReleaseServer(base_payloads)
        self.addCleanup(server.close)
        target = self.temp_root() / "strict-base-target"
        target.mkdir()
        (target / "keep.txt").write_bytes(b"keep\n")
        before = _tree_snapshot(target)
        output = self.temp_root() / "strict-base-output"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER.adopt(
                server.base_url,
                "2.1.0",
                "ko",
                target,
                output,
                installer_bytes=REAL_INSTALLER_BYTES,
                base_version="2.0.0",
            )
        self.assertIn("asset inventory", str(context.exception))
        self.assertEqual(_tree_snapshot(target), before)
        self.assertFalse(output.exists())

    def test_base_schema_two_checks_all_locale_digests_without_downloading_them(self) -> None:
        payloads = build_release_payloads(
            version="2.1.0",
            members={"AGENTS.md": b"base\n"},
            policies={"AGENTS.md": "merge"},
            publish_latest=False,
        )
        manifest_path = "/releases/2.1.0/release-manifest.json"
        manifest = json.loads(payloads[manifest_path].decode("utf-8"))
        ko_record = manifest["locales"]["ko"]
        en_record = json.loads(json.dumps(ko_record))
        en_record["asset"] = "coding-agent-docs-template-en-v2.1.0.zip"
        manifest["locales"]["en"] = en_record
        manifest_data = (
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
            + "\n"
        ).encode("utf-8")
        payloads[manifest_path] = manifest_data
        ko_archive = payloads["/releases/2.1.0/%s" % ko_record["asset"]]
        en_path = "/releases/2.1.0/%s" % en_record["asset"]
        payloads[en_path] = ko_archive
        digests = {
            "release-manifest.json": _sha256(manifest_data),
            "installer.py": _sha256(payloads["/releases/2.1.0/installer.py"]),
            ko_record["asset"]: _sha256(ko_archive),
            en_record["asset"]: _sha256(ko_archive),
        }
        payloads["/releases/2.1.0/SHA256SUMS"] = "".join(
            "%s  %s\n" % (digests[name], name) for name in sorted(digests)
        ).encode("ascii")
        payloads.update(
            build_release_payloads(
                version="2.2.0",
                members={"AGENTS.md": b"current\n"},
                policies={"AGENTS.md": "merge"},
            )
        )
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)
        target = self.temp_root() / "schema-two-target"
        target.mkdir()
        output = self.temp_root() / "schema-two-output"
        INSTALLER.adopt(
            server.base_url,
            "2.2.0",
            "ko",
            target,
            output,
            installer_bytes=REAL_INSTALLER_BYTES,
            base_version="2.1.0",
        )
        self.assertTrue(output.is_dir())
        self.assertNotIn(en_path, server.requests)

    def test_base_manifest_rejects_unknown_keys_at_every_schema_layer(self) -> None:
        payloads = build_release_payloads(
            version="2.0.0",
            members={"AGENTS.md": b"base\n"},
            schema_version=1,
            publish_latest=False,
        )
        manifest = json.loads(
            payloads["/releases/2.0.0/release-manifest.json"].decode("utf-8")
        )
        mutations = (
            lambda value: value.update({"unexpected": True}),
            lambda value: value["installer"].update({"unexpected": True}),
            lambda value: value["locales"]["ko"].update({"unexpected": True}),
            lambda value: value["locales"]["ko"]["members"][0].update(
                {"unexpected": True}
            ),
        )
        for mutate in mutations:
            candidate = json.loads(json.dumps(manifest))
            mutate(candidate)
            with self.assertRaises(INSTALLER.InstallerError):
                INSTALLER._validated_base_manifest(candidate)

    def test_base_installer_tamper_fails_without_publishing(self) -> None:
        payloads = build_release_payloads(
            version="2.0.0",
            members={"AGENTS.md": b"base\n"},
            schema_version=1,
            installer_bytes=b"historical installer\n",
            publish_latest=False,
        )
        payloads["/releases/2.0.0/installer.py"] += b"tampered\n"
        payloads.update(
            build_release_payloads(
                version="2.1.0",
                members={"AGENTS.md": b"current\n"},
                policies={"AGENTS.md": "merge"},
            )
        )
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)
        target = self.temp_root() / "tampered-base-target"
        target.mkdir()
        before = _tree_snapshot(target)
        output = self.temp_root() / "tampered-base-output"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER.adopt(
                server.base_url,
                "2.1.0",
                "ko",
                target,
                output,
                installer_bytes=REAL_INSTALLER_BYTES,
                base_version="2.0.0",
            )
        self.assertIn("base installer.py", str(context.exception))
        self.assertEqual(_tree_snapshot(target), before)
        self.assertFalse(output.exists())

    def test_non_base_commands_do_not_enter_the_legacy_parser(self) -> None:
        base = self.publish()
        original = INSTALLER._verified_base_release

        def forbidden(*_args, **_kwargs):
            raise AssertionError("legacy parser was called")

        INSTALLER._verified_base_release = forbidden
        try:
            INSTALLER.list_locales(base, "2.0.0", installer_bytes=REAL_INSTALLER_BYTES)
            INSTALLER.install(
                base,
                "2.0.0",
                "ko",
                self.temp_root() / "isolated-install",
                installer_bytes=REAL_INSTALLER_BYTES,
            )
            INSTALLER.export_artifact(
                base,
                "2.0.0",
                "ko",
                self.temp_root() / "isolated-export",
                installer_bytes=REAL_INSTALLER_BYTES,
            )
            target = self.temp_root() / "isolated-adopt-target"
            target.mkdir()
            INSTALLER.adopt(
                base,
                "2.0.0",
                "ko",
                target,
                self.temp_root() / "isolated-adopt-output",
                installer_bytes=REAL_INSTALLER_BYTES,
            )
        finally:
            INSTALLER._verified_base_release = original

    def test_manifest_members_require_a_known_adoption_policy(self) -> None:
        for policy, message in ((None, "invalid member record"), ("overwrite", "adoption policy")):
            member = {
                "path": "README.md",
                "sha256": "a" * 64,
                "bytes": 1,
                "mode": 0o644,
                "timestamp": "1980-01-01T00:00:00Z",
            }
            if policy is not None:
                member["policy"] = policy
            with self.assertRaises(INSTALLER.InstallerError) as context:
                INSTALLER._validated_member_record("ko", member)
            self.assertIn(message, str(context.exception))

    # -- validation and integrity failures ---------------------------------

    def call_install(self, base: str, target: Path, **overrides) -> None:
        kwargs = {
            "release_url": base,
            "version": "2.0.0",
            "locale": "ko",
            "repo_root": target,
        }
        kwargs.update(overrides)
        INSTALLER.install(**kwargs)

    def test_rejects_unsupported_locales_before_writing(self) -> None:
        base = self.publish()
        target = self.temp_root() / "project"
        for locale in ("fr", "en_US"):
            with self.assertRaises(INSTALLER.InstallerError) as context:
                self.call_install(base, target, locale=locale)
            self.assertIn("unsupported locale", str(context.exception))
            self.assertIn("English bundle", str(context.exception))
        self.assertFalse(target.exists())

    def test_schema_mismatch_explains_how_to_pair_the_installer(self) -> None:
        base = self.publish(schema_version=1)
        completed = self.run_cli(
            "list-locales",
            "--release-url",
            base,
            "--version",
            "2.0.0",
        )
        self.assertEqual(completed.returncode, 1)
        self.assertIn("unsupported release manifest schema_version", completed.stderr)
        self.assertIn(
            "installer.py from the same release version",
            completed.stderr,
        )

    def test_rejects_a_running_installer_that_differs_from_the_manifest(self) -> None:
        base = self.publish()
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(base, target, installer_bytes=b"#!/usr/bin/env python3\nother\n")
        self.assertIn("installer", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_an_archive_that_differs_from_its_manifest_checksum(self) -> None:
        payloads = build_release_payloads()
        asset_name = next(
            name
            for name in payloads
            if name.startswith(VERSION_DIR + "/coding-agent-docs-template-")
        )
        payloads[asset_name] = payloads[asset_name] + b"tampered"
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(server.base_url, target)
        self.assertIn("does not match", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_a_manifest_not_covered_by_sha256sums(self) -> None:
        payloads = build_release_payloads(source_commit="b" * 40)
        reference = build_release_payloads(source_commit="a" * 40)
        payloads["%s/SHA256SUMS" % VERSION_DIR] = reference["%s/SHA256SUMS" % VERSION_DIR]
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(server.base_url, target)
        self.assertIn("SHA256SUMS", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_archive_members_that_differ_from_the_manifest_inventory(self) -> None:
        archive = PACKAGE_RELEASE._zip_bytes(
            (
                ("AGENTS.md", b"# agent contract\n"),
                ("README.md", b"# readme\n"),
                ("docs/extra.md", b"extra\n"),
            )
        )
        payloads = build_release_payloads(
            archive=archive,
            locale_record_overrides={"sha256": _sha256(archive), "bytes": len(archive)},
        )
        server = FakeReleaseServer(payloads)
        self.addCleanup(server.close)
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(server.base_url, target)
        self.assertIn("differ from the manifest", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_member_paths_that_escape_the_target(self) -> None:
        base = self.publish(members={"../evil.txt": b"escape\n", "AGENTS.md": b"# ok\n"})
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(base, target)
        self.assertIn("..", str(context.exception))
        self.assertFalse((self.temp_root() / "evil.txt").exists())
        self.assertFalse(target.exists())

    def test_rejects_non_regular_archive_members(self) -> None:
        archive = _zip_with_symlink_member("AGENTS.md", b"target")
        base = self.publish(
            members={"AGENTS.md": b"target"},
            archive=archive,
        )
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(base, target)
        self.assertIn("regular file", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_case_fold_colliding_member_paths(self) -> None:
        base = self.publish(members={"Docs/a.md": b"a\n", "docs/a.md": b"b\n"})
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(base, target)
        self.assertIn("case-fold", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_member_path_prefix_conflicts_before_writing(self) -> None:
        base = self.publish(members={"docs": b"file\n", "docs/a.md": b"nested\n"})
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(base, target)
        self.assertIn("prefix conflict", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_duplicate_archive_members(self) -> None:
        archive = _zip_with_duplicate_members("AGENTS.md", (b"first\n", b"second\n"))
        base = self.publish(members={"AGENTS.md": b"first\n"}, archive=archive)
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(base, target)
        self.assertIn("duplicate", str(context.exception))
        self.assertFalse(target.exists())

    def test_enforces_declared_size_limits(self) -> None:
        base = self.publish(
            locale_record_overrides={"bytes": INSTALLER.ARCHIVE_MAX_BYTES + 1},
        )
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(base, target)
        self.assertIn("download limit", str(context.exception))
        self.assertFalse(target.exists())

    def test_rejects_insecure_hosts_and_invalid_versions(self) -> None:
        target = self.temp_root() / "project"
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install("http://example.com/releases", target)
        self.assertIn("https", str(context.exception))
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install("https://example.invalid/releases", target)
        self.assertIn("github.com", str(context.exception))
        with self.assertRaises(INSTALLER.InstallerError) as context:
            self.call_install(
                "https://github.com/jaff2836/coding-agent-docs-template/releases",
                target,
                version="2.0",
            )
        self.assertIn("SemVer", str(context.exception))

        invalid_release_urls = (
            "https://github.com:443/jaff2836/coding-agent-docs-template/releases",
            "https://github.com/jaff2836/coding-agent-docs-template",
            "https://github.com/jaff2836/coding-agent-docs-template/releases?x=1",
            "https://github.com/jaff2836/coding-agent-docs-template/releases#fragment",
        )
        for release_url in invalid_release_urls:
            with self.subTest(release_url=release_url):
                with self.assertRaises(INSTALLER.InstallerError):
                    INSTALLER._validated_release_url(release_url)

    def test_rejects_local_fixture_redirects(self) -> None:
        payloads = build_release_payloads()
        manifest_path = "%s/release-manifest.json" % VERSION_DIR
        redirected_path = "%s/redirected-manifest.json" % VERSION_DIR
        payloads[redirected_path] = payloads[manifest_path]
        server = FakeReleaseServer(
            payloads,
            redirects={manifest_path: redirected_path},
        )
        self.addCleanup(server.close)
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER.list_locales(server.base_url, "2.0.0")
        self.assertIn("HTTP 302", str(context.exception))

    def test_rejects_a_manifest_for_another_github_repository(self) -> None:
        release_url = "https://github.com/jaff2836/coding-agent-docs-template/releases"
        manifest = {
            "repository": "someone/another-template",
        }
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER._require_matching_repository(release_url, manifest)
        self.assertIn("does not match", str(context.exception))

    def test_mid_write_failure_rolls_back_created_files(self) -> None:
        base = self.publish()
        target = self.temp_root() / "project"
        target.mkdir()
        before = _tree_state(target)
        real_chmod = os.chmod

        def failing_chmod(path, mode):
            if "README.md" in str(path):
                raise OSError("simulated write failure")
            return real_chmod(path, mode)

        INSTALLER.os.chmod = failing_chmod
        try:
            with self.assertRaises(INSTALLER.InstallerError) as context:
                self.call_install(base, target)
        finally:
            INSTALLER.os.chmod = real_chmod
        self.assertIn("left unchanged", str(context.exception))
        self.assertEqual(_tree_state(target), before)

    def test_parent_directory_chmod_failure_rolls_back_created_directories(self) -> None:
        target = self.temp_root() / "project"
        target.mkdir()
        before = _tree_state(target)
        failing_directory = target / ".agents" / "skills"
        real_chmod = os.chmod

        def failing_chmod(path, mode):
            if Path(path) == failing_directory:
                raise OSError("simulated parent directory chmod failure")
            return real_chmod(path, mode)

        INSTALLER.os.chmod = failing_chmod
        try:
            with self.assertRaises(INSTALLER.InstallerError) as context:
                INSTALLER._write_members(
                    target,
                    {".agents/skills/design/SKILL.md": b"test\n"},
                )
        finally:
            INSTALLER.os.chmod = real_chmod
        self.assertIn("left unchanged", str(context.exception))
        self.assertEqual(_tree_state(target), before)

    def test_installer_error_mid_write_rolls_back_created_files(self) -> None:
        target = self.temp_root() / "project"
        target.mkdir()
        before = _tree_state(target)
        with self.assertRaises(INSTALLER.InstallerError) as context:
            INSTALLER._write_members(
                target,
                {"docs": b"file\n", "docs/a.md": b"nested\n"},
            )
        self.assertIn("left unchanged", str(context.exception))
        self.assertEqual(_tree_state(target), before)

    def test_cli_requires_a_release_url(self) -> None:
        missing = self.run_cli("list-locales", "--version", "2.0.0")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("--release-url", missing.stderr)

    # -- helpers -----------------------------------------------------------

    def temp_root(self) -> Path:
        return Path(self.temporary.name)


def _zip_with_symlink_member(name: str, payload: bytes) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as handle:
        info = zipfile.ZipInfo(name, date_time=PACKAGE_RELEASE.ARCHIVE_TIMESTAMP)
        info.create_system = 3
        info.compress_type = zipfile.ZIP_STORED
        info.external_attr = (stat.S_IFLNK | 0o644) << 16
        handle.writestr(info, payload)
    return output.getvalue()


def _zip_with_duplicate_members(name: str, payloads: tuple[bytes, ...]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as handle:
        for payload in payloads:
            info = zipfile.ZipInfo(name, date_time=PACKAGE_RELEASE.ARCHIVE_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            handle.writestr(info, payload)
    return output.getvalue()


if __name__ == "__main__":
    unittest.main()
