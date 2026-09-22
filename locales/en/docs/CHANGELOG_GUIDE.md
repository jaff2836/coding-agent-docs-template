# Changelog Guide

> Use this guide when a project introduces or maintains release notes. A root
> `CHANGELOG.md` is project-owned and optional; adopting this template does not
> create or overwrite one.

## Metadata

- **Status:** Active
- **Owner:** Customize for the project
- **Last reviewed:** Replace with the review date when adopting
- **Review cadence:** When the release process or documentation ownership changes

## 1. Document Boundaries

Keep each kind of information in one canonical place:

| Information | Canonical document |
| ----------- | ------------------ |
| Current installation, usage, and supported behavior | `README.md` |
| User-visible changes in published releases | Root `CHANGELOG.md`, when the project chooses to maintain one |
| Planned or unfinished work | `docs/02-TODO.md` or a change-specific PLAN |
| Template adoption source, version, and revision | `docs/DOCS_GUIDE.md` and `docs/TEMPLATE_GUIDE.md` |

Do not describe planned behavior as current README behavior or published
release history. Do not use the product changelog as the detailed task tracker.

## 2. Starting or Preserving a Changelog

- First determine whether the repository already has release notes and preserve
  its established file name and format unless the project explicitly decides to
  migrate them.
- For a new changelog, use `CHANGELOG.md` at the repository root unless the
  project has another documented convention.
- Do not add an empty `Unreleased` section by default. TODO or PLAN owns future
  work. A project may deliberately use an `Unreleased` section, but its contents
  must remain distinguishable from published releases.
- Template upgrades do not require a product changelog entry unless they change
  user-visible behavior. Record template provenance separately in the guide
  documents.

## 3. Published Release Entries

Add an entry only after the release exists. Record the exact version and release
date, and link to the immutable release page when one is publicly available.
Order versions newest first.

Use only categories that contain meaningful items. Common categories are
`Added`, `Changed`, `Fixed`, `Removed`, and `Security`. A compact release may use
an ungrouped list instead.

Include:

- user-visible behavior and supported workflows;
- compatibility or migration requirements;
- security and operational changes users must act on;
- deprecations and removals.

Exclude raw commit lists, review history, and internal refactors that do not
affect users.

Example:

```markdown
## [v1.4.0](https://example.com/releases/tag/v1.4.0) — 2026-06-15

### Added

- Added read-only reports for existing repositories.

### Changed

- Documented the required migration step for legacy configuration.
```

## 4. Release Checklist

- [ ] README statements describe the released current behavior.
- [ ] The release entry matches the version, date, and published assets.
- [ ] Compatibility, migration, security, and removal impacts are explicit.
- [ ] Planned work remains in TODO or PLAN, not in a published entry.
- [ ] Existing changelog structure and project-owned content were preserved.
- [ ] Template provenance is accurate in the guide documents.
