# Project Baseline and Design

> This document is the index for the product overview, current structure, base design, decisions, and detailed designs. When integrating an existing product design, preserve decisions, contracts, and rationale while consolidating duplicate explanations and work status. Manage execution plans in [02-TODO.md](./02-TODO.md) or a change-specific PLAN.
>
> §1–§5, §8, and §11 are required. Keep the remaining sections only when applicable. If an existing detailed design is retained, link to its canonical source from §13 instead of duplicating its content. When removing or renumbering a section, update incoming section references as well.

## Metadata

- **Project:** {{PROJECT_NAME}}
- **Status:** Draft
- **Owner:** Describe as appropriate for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When architecture or scope changes, or at the end of a milestone

## 1. Context

### Problem

{{PROJECT_DESCRIPTION}}

### Target Users

- Primary users and operators

### Current State

- Current implementation status
- Existing systems or alternatives
- Known constraints

Record the currently implemented and verified support scope and its evidence. Distinguish design approval, code implementation, integration, release, and support verification. Do not duplicate detailed status for open PRs or individual branches here.

## 2. Goals

- Measurable outcomes that must be achieved

## 3. Non-goals

- Items intentionally excluded from this scope

## 4. Constraints

- Technical constraints
- Security and regulatory constraints
- Compatibility requirements
- Schedule or operational constraints

## 5. Current Architecture

Record the structure that exists in the current code and actual deployment configuration. Do not describe a target state that has not yet been implemented as current architecture.

### Components

| Component | Responsibility | Dependencies | Owner |
| --------- | -------------- | ------------ | ----- |
| Example   | Example        | Example      | Example |

### Data Flow

Describe how a representative request or task moves from input to result.

### External Boundaries

- Databases
- External APIs
- Message queues or schedulers
- Files and object storage
- Authentication and authorization systems

### Contracts and Core Design

Describe public contracts, data models, error handling, major trust boundaries, and the base design. Link to a separate canonical source when one exists, such as a configuration reference or security model. Record decision rationale only once, in §8 or in the detailed document designated there.

## 6. Target Architecture

Record the target structure that has been agreed but is not yet fully implemented. **Do not put items here that are only proposed and have not been agreed.** Keep unagreed items in §11 Open Questions or §12 Rejected or Deferred Ideas, and move them into this table only after a decision is made. A reader of this table will assume that every item in it has already been decided.

### Target Components

| Component | Intended Responsibility | Replaces/Extends | Completion Signal |
|---|---|---|---|
| Example | Target responsibility | Current component | Evidence of completion |

### Target Data Flow

Describe representative flows in the target state and the boundaries that differ from the current architecture.

### Compatibility Requirements

- API, data, and operational compatibility that must be preserved during the transition
- Conditions for parallel operation or a phased rollout
- Legacy paths to remove and the conditions that make removal safe

## 7. Transition Plan

Describe the sequence and safety conditions for moving from the current architecture to the target architecture. Define phases and completion criteria here; manage detailed execution checkboxes in TODO or a change-specific PLAN. If an extension document defines the same transition, reference that section.

| Phase | Change | Preconditions | Compatibility/Rollback | Completion Evidence |
|---|---|---|---|---|
| 1 | Transition work | Prerequisites | Compatibility and rollback approach | Test and deployment evidence |

## 8. Decisions

Use one of `Proposed`, `Accepted`, `Superseded`, or `Rejected` for decision status.

| ID | Date | Status | Decision | Rationale / Canonical source | Alternatives / Consequences | Approval |
|---|---|---|---|---|---|---|
| D-001 | YYYY-MM-DD | Proposed | Decision summary | Rationale or canonical link to a detailed SPEC or existing design | Alternatives and impact, or canonical reference | Not approved |

When the number of important decisions grows, move them into individual ADR documents and leave only links and summaries here.

This table is the authority for decision status and canonical location. Issue `D-nnn` globally when adding a decision to this table. The `D-001` row is a placeholder; delete it or replace it with an actual decision when adopting the template. It does not share a number space with change-folder IDs such as `R-001`. If rationale, alternatives, and impact are recorded in a detailed design, leave only a link and summary here. Link the approver, scope, and verifiable evidence. When superseding an existing decision, keep it with `Superseded` status instead of deleting it. Do not renumber an existing decision ID to match a file number.

## 9. Delivery Strategy

### Phase 1

- Goal
- Deliverables
- Completion criteria

### Phase 2

- Goal
- Deliverables
- Completion criteria

## 10. Risks

| Risk | Likelihood | Impact | Mitigation | Trigger/Signal |
| ---- | ---------- | ------ | ---------- | -------------- |
| Example | Medium | High | Mitigation approach | Observable signal |

## 11. Open Questions

- [ ] An unresolved question

## 12. Rejected or Deferred Ideas

Record why an idea was rejected or deferred and the conditions for reconsidering it so that it is not mistaken for the current plan.

## 13. Design Document Index

| Scope | Canonical Source | Relationship to Parent Design | Applicability |
|---|---|---|---|
| Base product design | This document or a retained existing design document | Base contracts and structure | Actual scope of application |
| Long-term extension (optional) | [10-EXTENSION.md](./10-EXTENSION.md) or an existing extension document | Decisions and sections preserved, extended, or replaced | Approved scope and prerequisites |

If the optional document is not used, remove its row and incoming links. Link individual change SPECs from decisions in §8. Do not treat a higher document number or later authoring date as replacing another design in its entirety.
