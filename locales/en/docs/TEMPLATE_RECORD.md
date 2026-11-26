# Template Adoption Record

> This project-owned document records the template source this project applied and how it was applied. On upgrade, preserve the existing content and merge only the template sections. Template-owned documents and templates are in `docs/template/`, and their ownership rules follow "Template-Owned Folder" in [DOCS_GUIDE.md](./template/DOCS_GUIDE.md).

## Metadata

- **Status:** Active
- **Owner:** Describe as appropriate for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When first adopting the template or upgrading to a new version

## Adoption Baseline

`Template version` in `docs/template/` is the version of that folder's contents, so do not repeat it here. To determine these values, follow "Recording the Copy Baseline with Git" in TEMPLATE_GUIDE §5.

- **Template source:** Adapt to the project — URL of the original template repository, or another location you can open again later
- **Template revision:** Adapt to the project — full SHA of the source commit used for copying (if uncommitted changes were included, `Unconfirmed (baseline commit: <full SHA>, includes uncommitted changes)`)
- **Template release:** Adapt to the project — `release` if the source exactly matches a release tag; otherwise `Unreleased (latest tag: v1.2)` or `Unreleased (no tag)`

## Template Adoption Record

Fill this in at the first adoption and at each upgrade to a new release. Write `None` for items that do not apply.

- **Previous baseline:** For an upgrade, the previous version and its source and revision. Pass this version to `adopt --base-version`
- **Starting revision:** The commit of this project where the merge started
- **Path adaptations:** Template documents kept under existing names or moved elsewhere, and how they map
- **Kept or excluded:** Paths where the project version was kept instead of the template version, or that were not applied, and why. Record here if you deleted `docs/template/TEMPLATE_GUIDE.md`
- **Changes to template-owned files:** If any `copy`-policy file (including `docs/template/`, the check script, and its tests) was changed, what changed and why. At the next upgrade, start from the artifact version and reapply these changes
- **Unverified:** Tool loading, commands, or CI items that could not be confirmed
