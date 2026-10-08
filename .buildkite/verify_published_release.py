#!/usr/bin/env python3
"""Run the published-release verifier for a release named at build creation.

The Windows pipeline runs this only on a manually created build that sets
RELEASE_VERIFY_VERSION and RELEASE_VERIFY_SOURCE_COMMIT, and optionally
RELEASE_VERIFY_BASE_VERSION. The verifier needs remotes named origin (Origin)
and github (GitHub), the annotated release tag and the synchronized main
locally, and a clean exact checkout of the tag source. This script prepares
those and runs the tag source's own verifier in a temporary worktree, so an
already published release can be checked from a newer pipeline commit.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Mapping, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "jaff2836/coding-agent-docs-template"
GITHUB_URL = "https://github.com/%s.git" % REPOSITORY
RELEASE_URL = "https://github.com/%s/releases" % REPOSITORY
# The version also becomes part of a fetch refspec, so accept plain SemVer only.
SEMVER = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
COMMIT = re.compile(r"[0-9a-f]{40}")


class InputError(ValueError):
    """A build environment value that must not reach git or the verifier."""


def read_inputs(environ: Mapping[str, str]) -> Tuple[str, str, Optional[str]]:
    version = environ.get("RELEASE_VERIFY_VERSION", "")
    source = environ.get("RELEASE_VERIFY_SOURCE_COMMIT", "")
    base = environ.get("RELEASE_VERIFY_BASE_VERSION", "")
    if not SEMVER.fullmatch(version):
        raise InputError("RELEASE_VERIFY_VERSION must be a plain SemVer such as 2.5.0")
    if not COMMIT.fullmatch(source):
        raise InputError("RELEASE_VERIFY_SOURCE_COMMIT must be a full lowercase commit SHA")
    if base and not SEMVER.fullmatch(base):
        raise InputError("RELEASE_VERIFY_BASE_VERSION must be a plain SemVer when set")
    return version, source, base or None


def verifier_command(
    python: str, worktree: Path, version: str, source: str, base: Optional[str]
) -> List[str]:
    command = [
        python,
        str(worktree / "scripts" / "verify-release.py"),
        "published",
        "--version",
        version,
        "--source-commit",
        source,
        "--repository",
        REPOSITORY,
        "--release-url",
        RELEASE_URL,
    ]
    if base is not None:
        command += ["--base-version", base]
    return command


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )


def _prepare_refs(version: str) -> None:
    # Compare the configured URL, not `get-url`, which applies insteadOf rewrites.
    configured = _git("config", "--get", "remote.github.url", check=False)
    if configured.returncode != 0:
        _git("remote", "add", "github", GITHUB_URL)
    elif configured.stdout.strip() != GITHUB_URL:
        # Never echo the configured URL: it may embed a token.
        raise InputError("existing github remote is not %s; remove or fix it" % GITHUB_URL)
    _git("fetch", "--no-tags", "origin", "+refs/heads/main:refs/remotes/origin/main")
    tag = "refs/tags/v%s" % version
    _git("fetch", "--no-tags", "github", "+%s:%s" % (tag, tag))


def main(environ: Mapping[str, str] = os.environ) -> int:
    try:
        version, source, base = read_inputs(environ)
    except InputError as exc:
        print("release verification input error: %s" % exc, file=sys.stderr)
        return 2
    try:
        # Keep token details out of the build log; only the exit status matters.
        subprocess.run(
            ["gh", "auth", "status"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        print(
            "gh must be installed and authenticated (for example with a read-only GH_TOKEN "
            "in the agent environment)",
            file=sys.stderr,
        )
        return 1
    try:
        _prepare_refs(version)
    except InputError as exc:
        print("release verification setup error: %s" % exc, file=sys.stderr)
        return 1
    temporary = Path(tempfile.mkdtemp(prefix="release-verify-"))
    worktree = temporary / "source"
    try:
        _git("worktree", "add", "--detach", str(worktree), source)
        env = dict(environ, PYTHONDONTWRITEBYTECODE="1")
        command = verifier_command(sys.executable, worktree, version, source, base)
        return subprocess.run(command, cwd=worktree, env=env).returncode
    finally:
        _git("worktree", "remove", "--force", str(worktree), check=False)
        shutil.rmtree(temporary, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
