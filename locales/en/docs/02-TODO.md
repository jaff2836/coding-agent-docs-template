# Project Work List

> This document manages project-wide changes, milestones, priorities, and dependencies. Follow [00-PROJECT.md](./00-PROJECT.md) for the product baseline and decisions, and [DOCS_GUIDE.md](./DOCS_GUIDE.md) for ownership of detailed status.
>
> The items below are copyable examples. Replace them with actual work when adopting the template, and do not count the examples as completed work.

## Metadata

- **Status:** Active
- **Owner:** Describe as appropriate for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When work scope, priorities, dependencies, or integration results change
- **Integration target:** Describe as appropriate for the project — baseline branch or local completion target

## Current Milestone

- **Name:** Milestone name
- **Goal:** Verifiable outcome
- **Target:** YYYY-MM-DD or TBD
- **Status:** Planned / In Progress / Blocked / Complete

## Operating Rules

- When a change-specific PLAN exists, this document manages only its link, priority, prerequisites, and integration status. Do not duplicate detailed checkboxes or verification logs.
- For a small task without a PLAN, manage its scope, implementation order, completion criteria, and verification within the item below.
- `In Progress` means the project has selected the work to proceed. It does not guarantee real-time status for another branch or open PR. When starting work, inspect the actual Git and PR state and the PLAN for that change.
- Each branch updates the detailed records for its own change. Do not use a stale copy to reverse another branch's work from complete to incomplete or vice versa.
- Update shared items only when scope, dependencies, or integration results change. Resolve conflicts by comparing the latest baseline and change-IDs, then recheck affected contracts and verification assumptions.
- Put only items whose required verification and integration into the specified target have been confirmed under `Completed`. Distinguish branch implementation completion, review-round pass, merge, release, and support verification, and evaluate the item against its own completion criteria.
- `T-nnn` is a global task ID in this document. It has a different scope from change-IDs, PROJECT `D-nnn`, and change-folder `R-nnn`/`W-nnn`. Follow the identifier scopes in [DOCS_GUIDE.md](./DOCS_GUIDE.md) for issuance and collision handling. `T-001` and similar IDs below are placeholders.
- Keep cancelled changes under Cancelled and retain their change folders. Do not read a completed SPEC as the current product baseline; after integration, reflect implemented contracts in PROJECT.
- A remote repository or PR is not required. For local work, preserve evidence using the baseline revision and the target branch or reviewed worktree scope. Do not claim that an uncommitted result is reproducible from a commit SHA.
- Documentation updates do not grant commit, push, or merge authority. Follow [REVIEW_ROUND.md](./REVIEW_ROUND.md) §9 for updates deferred until after a review round passes.

## In Progress

- [ ] **T-001 Change title**
  - Change-ID: unique ID of the change folder
  - Scope and priority: change-level summary
  - Prerequisites: related change-ID or condition
  - Related decisions and SPEC: PROJECT decision ID and canonical link
  - Canonical source for detailed execution: change-specific PLAN link
  - Integration completion criteria: target to update and required final verification

## Next

- [ ] **T-002 Small task title**
  - Scope:
  - Affected files and implementation order:
  - Completion criteria:
  - Verification method:
  - Dependencies and related decisions:
  - Canonical source for detailed execution: this item (no separate PLAN)

## Blocked

- [ ] **T-003 Change title**
  - Canonical source for detailed execution: PLAN link or this item
  - Blocking cause:
  - Required decision or external action:
  - Resume condition:

## Backlog

- [ ] Candidate not included in the current milestone — distinguish approval status and reconsideration conditions

## Cancelled

Include only cancelled changes. Record the change-ID, cancellation rationale, `Rejected` evidence in the Intent or Spec, and retained change-folder path. Do not mix them with completed or active items, and do not delete their folders.

## Completed

Add only actually completed items. Record the change-ID, integration target, verified revision or worktree scope, and location of verification evidence. Retain the change folder, and update PROJECT when an implemented contract becomes part of the current support scope. If a PR exists, confirm the actual merge result; do not invent a PR or merge SHA for local work.

When the completion history grows long, link to an existing CHANGELOG or milestone-specific archive document instead of duplicating its contents.
