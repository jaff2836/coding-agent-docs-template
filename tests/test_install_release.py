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


def build_release_payloads(
    *,
    locale: str = "ko",
    members: dict[str, bytes] | None = None,
    version: str = "2.0.0",
    source_commit: str = "a" * 40,
    archive: bytes | None = None,
    locale_record_overrides: dict | None = None,
    installer_record_overrides: dict | None = None,
    sums: bytes | None = None,
) -> dict[str, bytes]:
    """Build a synthetic release asset map mirroring package-release output."""

    member_items = tuple(sorted((members or DEFAULT_MEMBERS).items()))
    if archive is None:
        archive = PACKAGE_RELEASE._zip_bytes(member_items)
    locale_record = {
        "status": "complete",
        "asset": "coding-agent-docs-template-%s-v%s.zip" % (locale, version),
        "sha256": _sha256(archive),
        "bytes": len(archive),
        "compression": "stored",
        "members": PACKAGE_RELEASE._member_records(member_items),
    }
    locale_record.update(locale_record_overrides or {})
    installer_record = {
        "asset": "installer.py",
        "sha256": _sha256(REAL_INSTALLER_BYTES),
        "bytes": len(REAL_INSTALLER_BYTES),
    }
    installer_record.update(installer_record_overrides or {})
    manifest = {
        "schema_version": 1,
        "version": version,
        "source_commit": source_commit,
        "repository": "jaff2836/coding-agent-docs-template",
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
            "installer.py": _sha256(REAL_INSTALLER_BYTES),
            locale_record["asset"]: _sha256(archive),
        }
        sums = "".join("%s  %s\n" % (digests[name], name) for name in names).encode("ascii")
    return {
        "%s/release-manifest.json" % VERSION_DIR: manifest_data,
        "%s/SHA256SUMS" % VERSION_DIR: sums,
        "%s/%s" % (VERSION_DIR, locale_record["asset"]): archive,
        "%s/installer.py" % VERSION_DIR: REAL_INSTALLER_BYTES,
        "/releases/latest/release-manifest.json": manifest_data,
    }


class FakeReleaseServer:
    """Serve release assets from an in-memory path map on localhost."""

    def __init__(
        self,
        payloads: dict[str, bytes],
        redirects: dict[str, str] | None = None,
    ) -> None:
        served = payloads
        redirected = redirects or {}

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
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
        self.assertEqual(
            stat.S_IMODE((target / "docs/REVIEW.md").lstat().st_mode), 0o644
        )

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
        self.assertIn("export", completed.stderr)
        self.assertEqual(existing.read_bytes(), b"# user document\n")
        self.assertEqual(readme.read_bytes(), b"# user readme\n")
        self.assertEqual((nested / "keep.txt").read_bytes(), b"keep\n")
        self.assertEqual(_tree_state(target), before)

    def test_install_rejects_a_symlinked_target_root(self) -> None:
        base = self.publish()
        target = self.temp_root() / "elsewhere"
        target.mkdir()
        link = self.temp_root() / "project"
        link.symlink_to(target, target_is_directory=True)
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
            self.call_install("https://example.invalid/releases", target, version="2.0")
        self.assertIn("SemVer", str(context.exception))

    def test_rejects_release_asset_redirects(self) -> None:
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
