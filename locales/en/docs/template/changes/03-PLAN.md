# Change Execution Plan: {{CHANGE_TITLE}}

> This is a template for copying. When this file is used, manage the detailed work and verification status for this change only here. Do not create a separate TODO or duplicate the same checkboxes in the global TODO.

## Metadata

- **Change ID:** {{CHANGE_ID}}
- **Spec:** [02-SPEC.md](./02-SPEC.md) or the section and revision of the approved parent design
- **Global task:** Work ID from [02-TODO.md](../../02-TODO.md)
- **Owner:** Person responsible for the work
- **Baseline:** Revision from which the work started
- **Integration target:** Target branch or agreed local completion target
- **Scope:** Owned files and contracts, and boundaries with parallel work

When referencing only an approved parent design, remove links to nonexistent sibling SPEC files. Checking the boxes below means implementation and verification are complete on this branch; it does not mean merge, release, or support verification is complete.

## 1. Implementation Order and Dependencies

Record the files and components to change, their order, prerequisites, integration order, and risky steps.

## 2. Work Checklist

- [ ] **W-001 Work title**
  - Scope / changed files:
  - Requirements / parent completion criteria:
  - Prerequisites:
  - Verification:
  - Result / evidence:

Split the work into units that can be reviewed as one PR or one local review unit.

## 3. Verification Log

| Work / Requirement | Verified revision or worktree scope | Check run | Result / remaining limits |
|---|---|---|---|
| Example | Verification target | Check | Not run |

Do not put a commit SHA in your own file before that commit exists. Creating a commit for recordkeeping requires separate authority. Distinguish uncommitted results by recording the baseline revision and changed scope.

## 4. Change and Reverification Log

Record why the implementation plan changed, which checks were affected, and which contracts or assumptions were reverified after a base-branch change. Changes to SPEC requirements or completion criteria follow the design process and its approval scope.

## 5. Handoff

Record remaining work, blockers, related change IDs, and verification limits. After a review round passes, freeze this file too, hand off through [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §7 and §9, and apply the handoff during the next related task.
