# Release Notes

<!-- template-section:release-history -->

[한국어](./CHANGELOG.ko.md)

This file records version-specific changes. See [README.md](./README.md) for current installation and usage instructions, and [GitHub Releases](https://github.com/jaff2836/coding-agent-docs-template/releases) for immutable assets.

## [v2.3.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.0) — Documentation ownership and changelog guidance

- Locale artifacts include `docs/CHANGELOG_GUIDE.md`, which separates current README behavior, published release history, future TODO or PLAN work, and template adoption provenance without creating a project-owned root changelog.
- The bundled `project-analysis` skill no longer carries project-specific owner and review-date metadata.
- Locale guides are the canonical artifact guidance; source-root guides contain only maintainer-specific addenda.
- Source and artifact documentation checks validate their release histories from the appropriate canonical files.

## [v2.2.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.2.0) — Base-aware adoption reports

- `adopt --base-version <older-exact-semver>` verifies an older exact release without running its installer and compares the base release, current release, and target tree.
- The opt-in format 2 report classifies `base ∪ current` paths as `unchanged`, `template-only`, `project-only`, `converged`, `diverged`, or `blocked`. It remains read-only and does not merge or delete files.
- Published-release verification covers format 2 invariants and the public `en` and `ko` upgrade paths. Consumer verification independently compares the generated report with the three input trees.
- The root READMEs describe current behavior only; release-specific history is kept here.

## [v2.1.1](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.1.1) — Checker and installer diagnostics

- `scripts/check-docs.py` treats `docs/TEMPLATE_GUIDE.md` as optional only when the path is absent and rejects external symlinks and non-file entries.
- Manifest schema mismatches explain how to use `installer.py` from the selected release.
- The first live candidate and published verification run completed against immutable release assets.

## [v2.1.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.1.0) — Existing-repository adoption

- Added the read-only `adopt` command and adoption-policy metadata for existing repositories.
- Bundled the self-contained `project-analysis` skill for Claude, Codex, Cursor, and OMP.
- Hardened the artifact documentation checker and verified `en` and `ko` installation, export, and adoption paths.

## [v2.0.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.0.0) — Locale artifacts

- Introduced deterministic, versioned `en` and `ko` release artifacts with manifests and checksums.
- Added the non-destructive installer and the GitHub Releases distribution contract.
