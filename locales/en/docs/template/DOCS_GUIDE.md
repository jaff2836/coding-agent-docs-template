# Documentation Operations Guide

## Metadata

- **Status:** Active
- **Template version:** 3.3.1
- **Review cadence:** When the documentation system changes

The root [README.md](../../README.md) contains project usage instructions for the adopting repository. The locale artifact places the project README template at that path. Follow `docs/template/TEMPLATE_GUIDE.md` for initial adoption and migration from an existing structure. This document defines ownership and usage rules for the shared template documentation.

## Document Map

| Document | Responsibility | When to Read |
|---|---|---|
| [00-PROJECT.md](../00-PROJECT.md) | Product overview, current structure, base design, decisions, and design index | Relevant sections when judging product context, structure, or contracts |
| [DESIGN.md](./DESIGN.md) | Process for confirming intent, specifying, planning execution, and reaching user agreement | Design-scope change or explicit invocation |
| [02-TODO.md](../02-TODO.md) | Project-wide changes, priorities, dependencies, and integration results | When selecting, starting, or handing off relevant work |
| [TEMPLATE_RECORD.md](../TEMPLATE_RECORD.md) | Applied template source, revision, release status, and adoption details | When adopting or upgrading the template |
| `docs/10-EXTENSION.md` or an existing extension document (optional) | Extension contracts, phase dependencies, and completion criteria shared by multiple changes | Relevant work in a project with a long-term extension |
| Change-specific `01-CHANGE.md` (combined) | Intent and Spec in one file | Reviewing or implementing a typical design change |
| Change-specific `01-INTENT.md` | Request source, problem, expected outcome, scope, and constraints | Confirming intent or reviewing a specification |
| Change-specific `02-SPEC.md` | Requirements, scenarios, design, alternatives, and compatibility | Implementation or change review |
| Change-specific `03-PLAN.md` (optional) | Implementation order, detailed work, and verification status | Executing or handing off that change |
| [REVIEW.md](../REVIEW.md) | Review judgment criteria and trust boundaries | PR, diff, or commit review |
| [REVIEW_ROUND.md](../REVIEW_ROUND.md) | Requested review round remediation and integration process | When the user starts a round. For a previous handoff, apply only §9 |
| [`project-analysis`](../../.agents/skills/project-analysis/SKILL.md) | Evidence-based whole-project analysis and adoption decision | Explicit request for whole-project analysis |
| [`bugfix`](../../.agents/skills/bugfix/SKILL.md) | Finding bugs and quality improvements and reporting them in one report | Explicit user invocation |
| [`refactor`](../../.agents/skills/refactor/SKILL.md) | Structural diagnosis and a refactoring design-proposal draft | Explicit user invocation |
| [`pr-review`](../../.agents/skills/pr-review/SKILL.md) | Static review of a named PR and publication of the review | Explicit user invocation |
| [CI.md](../CI.md) | Runner-agnostic quality gate order and integration verification | Connecting CI or aligning it with local gates |
| [CHANGELOG_GUIDE.md](./CHANGELOG_GUIDE.md) | Boundaries and maintenance rules for optional project release notes | Introducing or updating a project changelog |

The [CHANGE](./changes/01-CHANGE.md), [INTENT](./changes/01-INTENT.md), [SPEC](./changes/02-SPEC.md), and [PLAN](./changes/03-PLAN.md) files in `docs/template/changes/` are one set of copyable templates. Keep all four files when applying the template to a project. Manage an actual change in a separate change-ID folder, and copy only the format appropriate to that change's scale. Do not count the templates themselves as approved designs or incomplete work.

## Template-Owned Folder

The guide documents in `docs/template/` (this document, [DESIGN.md](./DESIGN.md), `TEMPLATE_GUIDE.md`, and [CHANGELOG_GUIDE.md](./CHANGELOG_GUIDE.md)) and the change templates are owned by the template (`copy`). All other documents are owned by the project.

- Keep this folder byte-identical to the artifact. An upgrade replaces the files in this folder with the new artifact version; do not put project files in this folder.
- Two differences are allowed: deleting `TEMPLATE_GUIDE.md`, and the edits recorded under "Changes to template-owned files" in [TEMPLATE_RECORD.md](../TEMPLATE_RECORD.md). On upgrade, start each edited file from the artifact version and reapply those edits.
- Documents in this folder do not link to files that may be deleted (`LICENSE`, `docs/10-EXTENSION.md`, `.cursor/BUGBOT.md`, `.omp/WATCHDOG.md`, and `TEMPLATE_GUIDE.md`), and do not put a section number after such a path or file name. When deleting one of those files, clean up links only in project-owned documents.
- Keep the values the project fills in (the template source, revision, release status, and adoption details) in [TEMPLATE_RECORD.md](../TEMPLATE_RECORD.md). `Template version` in this folder is the version of the folder's contents, and the project does not change it.

## Numbers and File Count

- `00-PROJECT.md` → `02-TODO.md` is the shared discovery order. It does not mean both documents must be read for every task. The design process moved to `docs/template/DESIGN.md`, leaving `01` unused; do not close the numbering gap.
- Within a change folder, files sort as `01-INTENT.md` → `02-SPEC.md` → optional `03-PLAN.md`. Do not close a numbering gap when an optional file is omitted.
- Use uppercase names and hyphens for new shared artifacts. Numbers are for sorting and do not represent decision IDs, approval, priority, or versions.
- Omit language suffixes when operating in a single language. If translations already exist, preserve their language relationships and links.
- Do not number instruction entry points or fixed policy paths such as `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, or `docs/REVIEW.md`. First check whether code, tools, or tests depend on the path.
- Use only a TODO item for small tasks. A typical design change may combine Intent and Spec sections in `01-CHANGE.md`. Follow [DESIGN.md](./DESIGN.md) §2 and §4 for split criteria and formats.
- A phase implementing an approved parent design may link that section and create only the necessary PLAN. Do not rewrite intent and specification merely to satisfy a file format.
- If there is no long-term extension, remove `10-EXTENSION.md` and incoming links from project-owned documents. If an existing extension document is retained, link it instead of creating a new file with the same content.

### Identifier Scope

| ID | Scope | Issued When and Where | Reference from Another Document |
|---|---|---|---|
| Change-ID | Repository-wide; unique across parallel branches | When creating a change folder. Use `<UTC date>-<unique slug>` or an existing issue ID | The change-ID itself |
| `D-nnn` | Global within PROJECT §8 | When adding a decision to PROJECT §8. Do not renumber existing IDs | `D-nnn` |
| `T-nnn` | Global TODO | When adding an item to [02-TODO.md](../02-TODO.md) | `T-nnn` |
| `R-nnn`, `W-nnn`, etc. | Within one change folder | In that change's SPEC or PLAN | `<change-ID>/R-001` |

- Issue the next global `D-` or `T-` number based on the current table at the integration target. If parallel branches use the same number, preserve the side already integrated and renumber only the side not yet integrated. Do not renumber a change-ID.
- Do not reserve a `D-nnn` for a decision not yet in PROJECT. Refer to it by change-ID, and by a change-local ID when needed. Use the `D-nnn` only after registration.
- `D-001` and `T-001` in the change templates and the global TODO are placeholders, not actual issuance records.

## Sources of Truth

| Information | Canonical Source | Representation Elsewhere |
|---|---|---|
| Product goals, current structure, and verified support scope | PROJECT or an existing product design designated by PROJECT | Link and summary |
| Decision status and canonical location | PROJECT §8 | Decision ID and link |
| Detailed decision rationale, contracts, and completion criteria | Product or extension design, or change SPEC, referenced by the decision | Reference without duplicating content |
| Original request and requirement changes | Change INTENT or the Intent section of a combined document | Source and link |
| Change-level priority, prerequisites, and integration result | Global TODO | Related change-ID |
| Detailed work and verification status | Change-specific PLAN when one exists; otherwise the global TODO item | Do not duplicate checkboxes or logs |
| Completed release history | Existing CHANGELOG when one exists; follow [CHANGELOG_GUIDE.md](./CHANGELOG_GUIDE.md) | TODO Completed links to evidence |
| Review judgments and exceptions | REVIEW | Maintain only necessary tool-specific copies |
| Execution command strings | AGENTS.md and the adopting project's README | Do not keep commands only in CI jobs |
| Quality gate order and integration verification | [CI.md](../CI.md) | Runner YAML is owned by the adopting project and is not provided by this template |
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
- Freeze tracked files, including the PLAN, after a review round passes. Do not change the head to add records; carry judgments and handoff information into the next relevant task according to [REVIEW_ROUND.md](../REVIEW_ROUND.md) §7 and §9.

### Lifecycle of Change Documents

- Retain completed change folders. They preserve historical agreement and approval evidence; do not delete them when implementation finishes.
- The current product baseline is PROJECT or an existing design designated by PROJECT. Do not read a completed SPEC as the current contract. Move implemented contracts into PROJECT's current architecture and contracts only after they reach the specified integration target and change the support scope.
- Cancellation: mark the Intent or Spec `Rejected`, and record the rationale and retained path under global TODO Cancelled. Keep the folder but do not count it as current work.
- Deferral: record it under TODO Blocked with a resume condition. Do not move a `Draft` or `Proposed` item into the target architecture.
- Keep a replaced decision as `Superseded` and link it to the new decision instead of deleting it.

## Local Git and Parallel Branches

A remote repository, PR, and CI are optional. Record the adopting project's integration branch or local completion target in the global TODO.

- The global TODO at the integration target reflects plans and results integrated into that revision. It does not provide real-time status for a work branch copy or an unmerged PR.
- A work branch's TODO and PLAN may describe the state that becomes true when that branch's final head is integrated into the integration target (a merge-bound description). For example, move the branch's own item to `Completed` and cite this change's PR or integration commit as evidence. The only condition a merge-bound description may assume is the integration of its own final head; do not read an unintegrated branch copy as the current state.
- Events that happen after integration (release publication, synchronization of another remote, other PRs, external or support verification) are recorded by the task that performs them, after they finish. Describing them as complete in advance is allowed only when the user explicitly requests it; record the requester, time, and scope in the PR description (or in the task report when there is no PR).
- Keep facts that arise after a head is fixed (its CI builds, review decisions and comment IDs, and the merge SHA) in the PR (or the task report when there is no PR) as the ledger, and keep only a reference in the documents. Do not create a record-only commit for these facts; record an earlier version's decisions only in a commit that carries an actual fix.
- Each branch updates its own change folder. Use a non-duplicated change-ID for new work, and do not restate another branch's detailed status in the shared TODO. Resolve global `D-` and `T-` number collisions according to Identifier Scope above.
- Update the global TODO only when scope, priority, prerequisites, or integration results change. Inspect open PRs, actual branches, and commit status with the relevant Git tools.
- Before starting or integrating work, compare the latest inspected baseline with your own baseline. Leave the status of inaccessible work unverified.
- If another change has been integrated first, inspect not only file conflicts but also changes to shared contracts, completion criteria, and verification assumptions. Rerun only affected checks. This rule does not grant authority for automatic rebase or merge.
- Resolve conflicts in baseline documents or the shared TODO by preserving both changes' IDs, decisions, and evidence. Do not overwrite the entire file with one side's copy.
- Local verification may record a baseline revision and the changed worktree scope. Do not invent PRs, merge SHAs, or approvers, and do not claim an uncommitted result is reproducible from one SHA.
- Hand off records that a merge-bound description could not carry, and findings newly raised on the final head, to the next relevant task as `Documentation update pending`. Until it is applied, inspect both the actual integration result and the handoff report when determining current status.

## Metadata Convention

`Status`, `Owner`, `Last reviewed`, and `Review cadence` in project-owned documents describe the document's own status and responsibility. Documents in `docs/template/` carry only the `Status` and `Review cadence` set by the template, and the project does not change them. Change documents add the request source, parent design, approval evidence, and verification target revision as appropriate to their roles. Fill in guidance text and placeholders from the original template during adoption.

- `Template version`: The version of the folder's contents, present only in the two guide documents in `docs/template/`. It changes when the folder is replaced, so do not repeat it in the project record.
- `Template source`, `Template revision`, `Template release`: The original location, the full SHA of the copied source commit, and whether it is a release, recorded in [TEMPLATE_RECORD.md](../TEMPLATE_RECORD.md). The revision is not the adopting project's HEAD. If uncommitted changes are included or the revision cannot be verified, record `Unconfirmed` with the baseline and additional changes in the revision; for a commit after a tag or a source with no tag, record `Unreleased (...)` in the release.
- If only part of the template was applied, record inclusions and exclusions in the Template Adoption Record in [TEMPLATE_RECORD.md](../TEMPLATE_RECORD.md). Ordinary project documentation edits do not change the source baseline.
- REVIEW's `Policy version` is independent of the template version.
- Dates use UTC `YYYY-MM-DD` by default. If another convention is used, document it here. Update `Last reviewed` only when the content was actually reviewed.
- Record the approver, scope, and evidence. Do not treat file authorship or a Git commit itself as approval.

## Placeholder Search

Find placeholders and examples remaining in the adopted repository in one pass. The table of values to replace is in "Values to Replace" in TEMPLATE_GUIDE.

These search commands use **Bash**; on Windows, use Git Bash or WSL. From the repository root, run the declaration first, then either search command in the **same shell**. The declaration is the single source for both patterns.

```bash
template_placeholder_pattern='\{\{|Adapt to the project|Describe as appropriate for the project|Customize for the project|Briefly describe|YYYY-MM-DD|\| Example|Example decision|Example completion|\*\*Example:\*\*|template-example:project-invariant'
```

```bash
rg --hidden -n --glob '*.md' --glob '!**/.git/**' --glob '!docs/template/**' \
  "$template_placeholder_pattern" .
```

If `rg` is unavailable, use the following in the same shell after the declaration:

```bash
grep -rnE "$template_placeholder_pattern" \
  --include='*.md' --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv . \
  | grep -v '^\./docs/template/'
```

Run this check against the **adopted repository after filling in project values**. The source template intentionally retains placeholders and examples. Use `--hidden` to search hidden directories such as `.cursor/BUGBOT.md`, while excluding `.git` internals.

`docs/template/` is excluded as a whole because its documents explain placeholders or hold them as copyable templates. This document is also in that folder, so the declaration above does not match itself. Values the project fills in are in the other documents (including [TEMPLATE_RECORD.md](../TEMPLATE_RECORD.md)); if values copied from the templates remain in an actual change folder, replace them. Even a zero-result search does not verify README guidance outside this pattern, owner, milestone, or task examples, command executability, or evidence for completion claims. Check the Template Adoption Checklist below too.

## Template Adoption Checklist

- [ ] Checked prior filenames, sections, code, tests, and tool references using the migration process in TEMPLATE_GUIDE.
- [ ] Replaced placeholders in the root README.md with actual project usage instructions and did not copy the template source repository's introduction.
- [ ] Decided whether the project needs a root `CHANGELOG.md`; preserved its existing format when present and applied [CHANGELOG_GUIDE.md](./CHANGELOG_GUIDE.md) without treating planned work as published history.
- [ ] If using the release installer, verified the final asset URL, exact version, and locale; if using the source checkout exporter, recorded the exact source revision and whether uncommitted changes were included.
- [ ] For an existing project, used `adopt` to create the artifact and report in an empty directory outside the target, resolved every `merge`, `decision`, and `blocked` path, and merged manually without automatically overwriting existing documents, commands, decisions, or the license.
- [ ] Replaced project information, commands, owners, and examples with actual values. Did not count source templates as actual work.
- [ ] Kept `docs/template/` identical to the artifact version. The only allowed differences are deleting `TEMPLATE_GUIDE.md` and the edits recorded in TEMPLATE_RECORD. Copied only the necessary templates into each actual change folder.
- [ ] Verified Template source, revision, and release and recorded them in [TEMPLATE_RECORD.md](../TEMPLATE_RECORD.md), and filled in the Template Adoption Record. Marked anything undetermined as undetermined.
- [ ] If manually adapting a language other than `en` or `ko`, did not claim official locale support and recorded the changed language policy and document scope.
- [ ] Replaced `LICENSE` with the project's license, or removed it and left the README License section undecided if a license has not been chosen. Did not leave the template's MIT notice as the project's license.
- [ ] Verified Run, Build, Test, Lint, and Typecheck, or recorded `N/A` or the reason they remain unverified.
- [ ] Distinguished the current product baseline from approved targets in PROJECT, and either linked canonical existing product and extension designs or performed an agreed integration.
- [ ] Removed unnecessary optional documents and sections, and their links in project-owned documents. Did not edit `docs/template/`. Did not leave decision or task examples as actual completions or approvals.
- [ ] Separated ownership of change-level status and detailed execution status, without duplicating checklists in the global TODO and PLAN.
- [ ] Defined the integration target and verification and completion evidence for local and parallel work.
- [ ] If using CI, integrated gates into the existing runner using the [CI.md](../CI.md) checklist. This template does not provide product-specific YAML; did not create one before the user specified a runner. If not using CI, recorded local execution of the same gates and why CI is not used.
- [ ] Recorded project invariants and only actually approved deferrals in REVIEW. When using Bugbot, copied §6 and §9, plus the relevant settled decisions.
- [ ] If REVIEW or PROJECT section numbers changed, compared section references in DESIGN, REVIEW_ROUND, BUGBOT, and WATCHDOG, and recorded any edit to DESIGN in TEMPLATE_RECORD. `scripts/check-docs.py` checks document-qualified references, but a person checks ambiguous references within the same file.
- [ ] Preserved review-round user-defined thresholds, same-head pass, session handoff, and the next task's documentation update rules.
- [ ] When using an external reviewer, recorded the verified publishing account, publication location, head identification, arrival cadence, no-finding behavior, and the `Rereview request method` (parameter `rereview`) with any same-head rerun method in the registry. A local self-review does not require registration.
- [ ] Verified that instructions and skills load in the tools being used. Did not assume a Markdown link triggers automatic loading.
- [ ] Verified byte-identical copies of each `design`, `project-analysis`, `review-round`, `bugfix`, `refactor`, and `pr-review` skill and copied the Codex [review-round explicit invocation setting](../../.agents/skills/review-round/agents/openai.yaml) together with the same setting for `bugfix`, `refactor`, and `pr-review`. `policy.allow_implicit_invocation` is the boolean `false`.
- [ ] When using OMP, verified the `.omp/WATCHDOG.md` import with the version in use.
- [ ] Verified relative file links, required anchors, and import paths. `scripts/check-docs.py` passes without error. Broken links, divergent skill copies, missing or non-`false` Codex explicit invocation policy, invalid imports, inconsistent invariant lists, invalid section references, and version mismatches fail the check.
- [ ] Distinguished global `D-` and `T-` IDs from change-local IDs. Did not delete completed or cancelled change folders, and kept the current baseline in PROJECT.
- [ ] If CODEOWNERS exists, considered protecting shared instructions, policies, skills, and `docs/template/`.
- [ ] When using an external methodology tool, assigned canonical sources and instruction file ownership according to TEMPLATE_GUIDE §4.
- [ ] Recorded owners, review cadences, and dates for the project-owned documents actually reviewed.

## Maintenance

When moving or renaming documentation, update incoming links and code, test, and tool references together. Changing a file number also counts as a rename. As decisions accumulate, split them into the existing ADR system or detailed designs and link the canonical source from PROJECT. Verify links, skill copies, Codex explicit invocation policy values, imports, invariant copies, section references, and Template version with `scripts/check-docs.py`. When modifying the checker, run its regression tests with `python -m unittest discover -s tests -p 'test_check_docs.py' -v`.

For template updates, compare source revisions according to TEMPLATE_GUIDE §5. Replace `docs/template/` with the new artifact version; in project-owned documents, preserve intentional modifications in the adopting project and do not overwrite them wholesale.
