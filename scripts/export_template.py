#!/usr/bin/env python3
"""Materialize one locale artifact from the closed source inventory."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Optional, Sequence

import check_locales


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = Path("locales/manifest.json")
FILE_MODE = 0o644


class ExportError(ValueError):
    """Raised when source validation or artifact materialization fails."""


def load_validated_manifest(
    repository_root: Path, *, require_stable: bool = False
) -> Mapping[str, Any]:
    """Return the manifest after running the complete locale source gate."""

    repository_root = Path(repository_root).resolve()
    errors = check_locales.check_locales(
        repository_root, require_stable=require_stable
    )
    if errors:
        raise ExportError("locale source check failed:\n- " + "\n- ".join(errors))
    try:
        value = json.loads(
            (repository_root / MANIFEST_PATH).read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ExportError("cannot read validated locale manifest: %s" % exc) from exc
    if not isinstance(value, dict):
        raise ExportError("validated locale manifest must be an object")
    return value


def artifact_sources(
    repository_root: Path,
    manifest: Mapping[str, Any],
    locale: str,
    *,
    require_complete: bool = False,
) -> tuple[tuple[str, Path], ...]:
    """Resolve the exact output-path to source-path mapping for *locale*."""

    locales = manifest["locales"]
    if locale not in locales:
        raise ExportError("unsupported locale: %s" % locale)
    entry = locales[locale]
    if require_complete and locale not in check_locales.complete_locales(manifest):
        raise ExportError("locale %s is not complete" % locale)

    artifact = manifest["artifact"]
    common_root = repository_root / artifact["common_root"]
    locale_root = repository_root / entry["source_root"]
    sources = [
        (path, common_root / PurePosixPath(path))
        for path in artifact["common_paths"]
    ]
    sources.extend(
        (path, locale_root / PurePosixPath(path))
        for path in artifact["localized_paths"]
    )
    return tuple(sorted(sources, key=lambda item: item[0]))


def _validate_output(repository_root: Path, output: Path) -> tuple[Path, bool]:
    output = output.absolute()
    parent = output.parent
    if not parent.is_dir() or parent.is_symlink():
        raise ExportError("output parent must be an existing non-symlink directory")
    resolved_root = repository_root.resolve()
    resolved_output = output.resolve(strict=False)
    try:
        resolved_output.relative_to(resolved_root)
    except ValueError:
        pass
    else:
        raise ExportError("output must be outside the source repository")

    existed = output.exists() or output.is_symlink()
    if output.is_symlink():
        raise ExportError("output must not be a symlink")
    if existed:
        if not output.is_dir():
            raise ExportError("output must be an empty directory")
        try:
            next(output.iterdir())
        except StopIteration:
            pass
        else:
            raise ExportError("output must be an empty directory")
    return output, existed


def _copy_sources(stage: Path, sources: tuple[tuple[str, Path], ...]) -> None:
    for relative, source in sources:
        if source.is_symlink() or not source.is_file():
            raise ExportError("source must be a regular non-symlink file: %s" % source)
        try:
            data = source.read_bytes()
        except OSError as exc:
            raise ExportError("cannot read source %s: %s" % (source, exc)) from exc
        target = stage / PurePosixPath(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            target.write_bytes(data)
            target.chmod(FILE_MODE)
        except OSError as exc:
            raise ExportError("cannot write staged artifact %s: %s" % (relative, exc)) from exc


def _check_artifact(stage: Path) -> None:
    checker = stage / "scripts/check-docs.py"
    completed = subprocess.run(
        [sys.executable, str(checker), "--root", str(stage)],
        cwd=stage,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise ExportError("materialized artifact check failed: %s" % detail)


def export_locale(
    repository_root: Path,
    locale: str,
    output: Path,
    *,
    require_complete: bool = False,
) -> tuple[str, ...]:
    """Atomically write one validated locale artifact to an empty output."""

    repository_root = Path(repository_root).resolve()
    manifest = load_validated_manifest(
        repository_root, require_stable=require_complete
    )
    sources = artifact_sources(
        repository_root,
        manifest,
        locale,
        require_complete=require_complete,
    )
    output, existed = _validate_output(repository_root, Path(output))
    stage = Path(tempfile.mkdtemp(prefix=".template-export-", dir=output.parent))
    published = False
    try:
        _copy_sources(stage, sources)
        _check_artifact(stage)
        if existed:
            output.rmdir()
        os.replace(stage, output)
        published = True
    except OSError as exc:
        raise ExportError("cannot publish artifact: %s" % exc) from exc
    finally:
        if not published:
            shutil.rmtree(stage, ignore_errors=True)
    return tuple(relative for relative, _ in sources)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", required=True, help="manifest locale tag")
    parser.add_argument("--output", required=True, type=Path, help="empty output directory")
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="source repository root (default: exporter parent directory)",
    )
    args = parser.parse_args(argv)
    try:
        members = export_locale(args.root, args.locale, args.output)
    except ExportError as exc:
        print("Export failed: %s" % exc, file=sys.stderr)
        return 1
    print("Exported %s locale with %d files to %s" % (args.locale, len(members), args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
