# Long-Term Extension Design

> This is an optional template. Use it when multiple changes share an extension contract and phase-specific completion criteria. If it is not needed, remove this file and incoming links. If a document already serves the same role, link it from [00-PROJECT.md](./00-PROJECT.md) instead of duplicating it.
>
> Design approval does not mean implementation, integration, release, or support verification is complete. Manage work status in [02-TODO.md](./02-TODO.md) and the designated change-specific PLAN.

## Metadata

- **Status:** Draft
- **Owner:** Describe as appropriate for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When extension scope, contracts, or completion criteria change
- **Parent:** Path, revision, and applicable sections of the parent design
- **Approval:** Approved scope and verifiable evidence, or Not approved
- **Decisions:** Related decision IDs from PROJECT §8

## 1. Purpose and Scope

Describe why the extension is needed, its expected outcomes, non-goals, and constraints.

## 2. Relationship to the Parent Design

| Parent Decision/Section | Preserve / Extend / Replace | Change and Rationale | Applicability |
|---|---|---|---|
| Example | Preserve | Existing contract | Applicability condition |

Do not replace the entire parent document merely because this document has a higher number or was written later.

## 3. Requirements and Design

Describe requirements and verification scenarios, components and responsibilities, data flow, contracts, error handling, and alternatives. Distinguish the current implementation from the approved target.

## 4. Compatibility and Transition

Describe compatibility, migration and deployment order, rollback for each phase, parallel operation, and removal conditions.

## 5. Phase-Specific Completion Criteria

| Phase ID | Scope | Prerequisites | Completion Criteria and Verification | Canonical Execution Source |
|---|---|---|---|---|
| Example | Extension unit | Prior phase | Observable result | TODO item or change-specific PLAN link |

Keep phase definitions and completion criteria here. Manage current progress and execution checkboxes only in the canonical execution source. Implementation of an approved phase may reference this section without creating a new INTENT or SPEC.

## 6. Risks and Open Decisions

Describe risks, owners, mitigations, observable signals, and reevaluation conditions. Distinguish items requiring measurement from design choices that have not yet been agreed.

## 7. Support Verification Criteria

Describe the targets, environments, revisions, and evidence required before declaring an implemented feature supported. Link actual support status and its evidence from PROJECT's current state. Do not reuse success in one environment as evidence for another environment or revision.
