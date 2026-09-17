# Documentation Operations Guide

## Metadata

- **Status:** Active
- **Template version:** 1.7.1
- **Template source:** Describe the original template repository URL or another retrievable archive location as appropriate for the project
- **Template revision:** Describe the full SHA of the copied source commit as appropriate for the project; if the copy includes uncommitted changes, record it as `Unconfirmed`
- **Owner:** Describe as appropriate for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When the documentation system changes

The root [README.md](../README.md) contains project usage instructions for the adopting repository. The locale artifact places the project README template at that path. Follow [TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) for initial adoption and migration from an existing structure. This document defines ownership and usage rules for the shared template documentation.

## Document Map

| Document | Responsibility | When to Read |
|---|---|---|
| [00-PROJECT.md](./00-PROJECT.md) | Product overview, current structure, base design, decisions, and design index | Relevant sections when judging product context, structure, or contracts |
| [01-DESIGN.md](./01-DESIGN.md) | Process for confirming intent, specifying, planning execution, and reaching user agreement | Design-scope change or explicit invocation |
| [02-TODO.md](./02-TODO.md) | Project-wide changes, priorities, dependencies, and integration results | When selecting, starting, or handing off relevant work |
| [10-EXTENSION.md](./10-EXTENSION.md) or an existing extension document (optional) | Extension contracts, phase dependencies, and completion criteria shared by multiple changes | Relevant work in a project with a long-term extension |
| Change-specific `01-CHANGE.md` (combined) | Intent and Spec in one file | Reviewing or implementing a typical design change |
| Change-specific `01-INTENT.md` | Request source, problem, expected outcome, scope, and constraints | Confirming intent or reviewing a specification |
| Change-specific `02-SPEC.md` | Requirements, scenarios, design, alternatives, and compatibility | Implementation or change review |
| Change-specific `03-PLAN.md` (optional) | Implementation order, detailed work, and verification status | Executing or handing off that change |
| [REVIEW.md](./REVIEW.md) | Review judgment criteria and trust boundaries | PR, diff, or commit review |
| [REVIEW_ROUND.md](./REVIEW_ROUND.md) | Requested review round remediation and integration process | When the user starts a round. For a previous handoff, apply only §9 |
| [PROJECT_ANALYSIS.md](./PROJECT_ANALYSIS.md) | Whole-project analysis criteria | Explicit request for whole-project analysis |
| [CI.md](./CI.md) | Runner-agnostic quality gate order and integration verification | Connecting CI or aligning it with local gates |

The [CHANGE](./changes/_template/01-CHANGE.md), [INTENT](./changes/_template/01-INTENT.md), [SPEC](./changes/_template/02-SPEC.md), and [PLAN](./changes/_template/03-PLAN.md) files in `changes/_template/` are one set of copyable templates. Keep all four files when applying the template to a project. Manage an actual change in a separate change-ID folder, and copy only the format appropriate to that change's scale. Do not count the templates themselves as approved designs or incomplete work.

## Numbers and File Count

- `00-PROJECT.md` → `01-DESIGN.md` → `02-TODO.md` is the shared discovery order. It does not mean all three documents must be read for every task.
- Within a change folder, files sort as `01-INTENT.md` → `02-SPEC.md` → optional `03-PLAN.md`. Do not close a numbering gap when an optional file is omitted.
- Use uppercase names and hyphens for new shared artifacts. Numbers are for sorting and do not represent decision IDs, approval, priority, or versions.
- Omit language suffixes when operating in a single language. If translations already exist, preserve their language relationships and links.
- Do not number instruction entry points or fixed policy paths such as `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, or `docs/REVIEW.md`. First check whether code, tools, or tests depend on the path.
- Use only a TODO item for small tasks. A typical design change may combine Intent and Spec sections in `01-CHANGE.md`. Follow [01-DESIGN.md](./01-DESIGN.md) §2 and §4 for split criteria and formats.
- A phase implementing an approved parent design may link that section and create only the necessary PLAN. Do not rewrite intent and specification merely to satisfy a file format.
- If there is no long-term extension, remove `10-EXTENSION.md` and incoming links. If an existing extension document is retained, link it instead of creating a new file with the same content.

### Identifier Scope

| ID | Scope | Issued When and Where | Reference from Another Document |
|---|---|---|---|
| Change-ID | Repository-wide; unique across parallel branches | When creating a change folder. Use `<UTC date>-<unique slug>` or an existing issue ID | The change-ID itself |
| `D-nnn` | Global within PROJECT §8 | When adding a decision to PROJECT §8. Do not renumber existing IDs | `D-nnn` |
| `T-nnn` | Global TODO | When adding an item to [02-TODO.md](./02-TODO.md) | `T-nnn` |
| `R-nnn`, `W-nnn`, etc. | Within one change folder | In that change's SPEC or PLAN | `<change-ID>/R-001` |

- Issue the next global `D-` or `T-` number based on the current table at the integration target. If parallel branches use the same number, preserve the side already integrated and renumber only the side not yet integrated. Do not renumber a change-ID.
- Do not reserve a `D-nnn` for a decision not yet in PROJECT. Refer to it by change-ID, and by a change-local ID when needed. Use the `D-nnn` only after registration.
- `D-001` and `T-001` in `_template/` and the global TODO are placeholders, not actual issuance records.

## Sources of Truth

| Information | Canonical Source | Representation Elsewhere |
|---|---|---|
| Product goals, current structure, and verified support scope | PROJECT or an existing product design designated by PROJECT | Link and summary |
| Decision status and canonical location | PROJECT §8 | Decision ID and link |
| Detailed decision rationale, contracts, and completion criteria | Product or extension design, or change SPEC, referenced by the decision | Reference without duplicating content |
| Original request and requirement changes | Change INTENT or the Intent section of a combined document | Source and link |
| Change-level priority, prerequisites, and integration result | Global TODO | Related change-ID |
| Detailed work and verification status | Change-specific PLAN when one exists; otherwise the global TODO item | Do not duplicate checkboxes or logs |
| Completed release history | Existing CHANGELOG when one exists | TODO Completed links to evidence |
| Review judgments and exceptions | REVIEW | Maintain only necessary tool-specific copies |
| Execution command strings | AGENTS.md and the adopting project's README | Do not keep commands only in CI jobs |
| Quality gate order and integration verification | [CI.md](./CI.md) | Runner YAML is owned by the adopting project and is not provided by this template |
| Round judgment and post-pass handoff | REVIEW_ROUND §7 session record and original review result | Apply in the next relevant task according to §9 |
| Cancelled and deferred changes | Global TODO Cancelled/Blocked and the corresponding Intent/Spec status | Retain the change folder and do not count it as current work |

Do not put project designs, contracts, or completion criteria in process documents. Process documents define where information belongs and how to handle it.

The product design is a living current baseline, while a change INTENT and SPEC preserve the requirements and agreement for a specific change. Identify the scope an extension design replaces by parent decision ID and section. Do not always prefer one document in its entirety. Even when integrating an existing design into PROJECT, preserve decision rationale and approved contracts.

## Execution and Handoff

The normal flow is to inspect the product and parent designs → agree on necessary intent and specification → create the execution plan → implement and verify. Apply review, review round, whole-project analysis, and CI integration according to each request's applicability conditions; do not treat them as one mandatory sequential pipeline.

- Approval state (`Draft / Accepted / Superseded / Rejected`) is separate from implementation and integration state.
- Completed checkboxes in a change-specific PLAN mean implementation and verification on that branch are complete. For work requiring integration, release, or support verification, confirm each completion criterion and its evidence separately.
- If code and description diverge, first determine whether the approved contract changed or the implementation is wrong. Do not alter the specification to match the result merely to make verification pass.
- Document authoring, agreement, or completed checkboxes do not grant commit, push, merge, or deployment authority.
- Freeze tracked files, including the PLAN, after a review round passes. Do not change the head to add records; carry judgments and handoff information into the next relevant task according to [REVIEW_ROUND.md](./REVIEW_ROUND.md) §7 and §9.

### Lifecycle of Change Documents

- Retain completed change folders. They preserve historical agreement and approval evidence; do not delete them when implementation finishes.
- The current product baseline is PROJECT or an existing design designated by PROJECT. Do not read a completed SPEC as the current contract. Move implemented contracts into PROJECT's current architecture and contracts only after they reach the specified integration target and change the support scope.
- Cancellation: mark the Intent or Spec `Rejected`, and record the rationale and retained path under global TODO Cancelled. Keep the folder but do not count it as current work.
- Deferral: record it under TODO Blocked with a resume condition. Do not move a `Draft` or `Proposed` item into the target architecture.
- Keep a replaced decision as `Superseded` and link it to the new decision instead of deleting it.

## Local Git and Parallel Branches

A remote repository, PR, and CI are optional. Record the adopting project's integration branch or local completion target in the global TODO.

- The global TODO at the integration target reflects plans and results integrated into that revision. It does not provide real-time status for a work branch copy or an unmerged PR.
- Each branch updates its own change folder. Use a non-duplicated change-ID for new work, and do not restate another branch's detailed status in the shared TODO. Resolve global `D-` and `T-` number collisions according to Identifier Scope above.
- Update the global TODO only when scope, priority, prerequisites, or integration results change. Inspect open PRs, actual branches, and commit status with the relevant Git tools.
- Before starting or integrating work, compare the latest inspected baseline with your own baseline. Leave the status of inaccessible work unverified.
- If another change has been integrated first, inspect not only file conflicts but also changes to shared contracts, completion criteria, and verification assumptions. Rerun only affected checks. This rule does not grant authority for automatic rebase or merge.
- Resolve conflicts in baseline documents or the shared TODO by preserving both changes' IDs, decisions, and evidence. Do not overwrite the entire file with one side's copy.
- Local verification may record a baseline revision and the changed worktree scope. Do not invent PRs, merge SHAs, or approvers, and do not claim an uncommitted result is reproducible from one SHA.
- If a post-pass documentation update is deferred to the next task, hand it off as `Documentation update pending`. Until it is applied, inspect both the actual integration result and the handoff report when determining current status.

## Metadata Convention

`Status`, `Owner`, `Last reviewed`, and `Review cadence` in maintained documents describe the document's own status and responsibility. Change documents add the request source, parent design, approval evidence, and verification target revision as appropriate to their roles. Fill in guidance text and placeholders from the original template during adoption.

- `Template source`: Original repository URL or another retrievable archive location.
- `Template version`: Exact source release version. Distinguish changes after a tag as `Unreleased (latest tag: ...)`.
- `Template revision`: Full SHA of the copied source commit, not the adopting project's HEAD. If uncommitted changes are included or the revision cannot be verified, record `Unconfirmed` together with the baseline and additional changes.
- If two guidance documents exist, keep these three values identical. If only part of the template was applied, record inclusions and exclusions in this document. Ordinary project documentation edits do not change the source baseline.
- REVIEW's `Policy version` is independent of the template version.
- Dates use UTC `YYYY-MM-DD` by default. If another convention is used, document it here. Update `Last reviewed` only when the content was actually reviewed.
- Record the approver, scope, and evidence. Do not treat file authorship or a Git commit itself as approval.

## Template Adoption Checklist

- [ ] Checked prior filenames, sections, code, tests, and tool references using the migration process in TEMPLATE_GUIDE.
- [ ] Replaced placeholders in the root README.md with actual project usage instructions and did not copy the template source repository's introduction.
- [ ] If using the release installer, verified the final asset URL, exact version, and locale; if using the source checkout exporter, recorded the exact source revision and whether uncommitted changes were included.
- [ ] For an existing project, exported the artifact to a separate empty directory and merged it manually without automatically overwriting existing documents, commands, decisions, or the license.
- [ ] Replaced project information, commands, owners, and examples with actual values. Did not count source templates as actual work.
- [ ] Retained all four combined, split, and PLAN templates in `docs/changes/_template/`. Copied only the necessary format into each actual change folder.
- [ ] Verified Template source, version, revision, and partial adoption details. Marked anything undetermined as undetermined.
- [ ] If manually adapting a language other than `en` or `ko`, did not claim official locale support and recorded the changed language policy and document scope.
- [ ] Replaced `LICENSE` with the project's license, or removed it and left the README License section undecided if a license has not been chosen. Did not leave the template's MIT notice as the project's license.
- [ ] Verified Run, Build, Test, Lint, and Typecheck, or recorded `N/A` or the reason they remain unverified.
- [ ] Distinguished the current product baseline from approved targets in PROJECT, and either linked canonical existing product and extension designs or performed an agreed integration.
- [ ] Removed unnecessary optional documents, sections, and links, while retaining all four `_template/` files. Did not leave decision or task examples as actual completions or approvals.
- [ ] Separated ownership of change-level status and detailed execution status, without duplicating checklists in the global TODO and PLAN.
- [ ] Defined the integration target and verification and completion evidence for local and parallel work.
- [ ] If using CI, integrated gates into the existing runner using the [CI.md](./CI.md) checklist. This template does not provide product-specific YAML; did not create one before the user specified a runner. If not using CI, recorded local execution of the same gates and why CI is not used.
- [ ] Recorded project invariants and only actually approved deferrals in REVIEW. When using Bugbot, copied §6 and §9, plus the relevant settled decisions.
- [ ] If REVIEW or PROJECT section numbers changed, compared section references in DESIGN, REVIEW_ROUND, BUGBOT, and WATCHDOG. `scripts/check-docs.py` checks document-qualified references, but a person checks ambiguous references within the same file.
- [ ] Preserved review-round user-defined thresholds, same-head pass, session handoff, and the next task's documentation update rules.
- [ ] When using an external reviewer, recorded the verified publication location, head identification, arrival cadence, no-finding behavior, and the `Rereview request method` (parameter `rereview`) in the registry. A local self-review does not require registration.
- [ ] Verified that instructions and skills load in the tools being used. Did not assume a Markdown link triggers automatic loading.
- [ ] Verified identical skill contents at both paths and copied the Codex [explicit invocation setting](../.agents/skills/review-round/agents/openai.yaml). `policy.allow_implicit_invocation` is the boolean `false`.
- [ ] When using OMP, verified the [WATCHDOG](../.omp/WATCHDOG.md) import with the version in use.
- [ ] Verified relative file links, required anchors, and import paths. `scripts/check-docs.py` passes without error. Broken links, divergent skill copies, missing or non-`false` Codex explicit invocation policy, invalid imports, inconsistent invariant lists, invalid section references, and version mismatches fail the check.
- [ ] Distinguished global `D-` and `T-` IDs from change-local IDs. Did not delete completed or cancelled change folders, and kept the current baseline in PROJECT.
- [ ] If CODEOWNERS exists, considered protecting shared instructions, policies, skills, and baseline design documents.
- [ ] When using an external methodology tool, assigned canonical sources and instruction file ownership according to TEMPLATE_GUIDE §4.
- [ ] Recorded owners, review cadences, and dates for the documents actually reviewed.

## Maintenance

When moving or renaming documentation, update incoming links and code, test, and tool references together. Changing a file number also counts as a rename. As decisions accumulate, split them into the existing ADR system or detailed designs and link the canonical source from PROJECT. Verify links, skill copies, Codex explicit invocation policy values, imports, invariant copies, section references, and Template version with `scripts/check-docs.py`. When modifying the checker, run its regression tests with `python -m unittest discover -s tests -p 'test_check_docs.py' -v`.

For template updates, compare source revisions according to [TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) §5 and preserve intentional modifications in the adopting project. Do not overwrite existing files wholesale.
