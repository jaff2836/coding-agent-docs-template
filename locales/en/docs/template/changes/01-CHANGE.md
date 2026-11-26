# Change: {{CHANGE_TITLE}}

> This is a combined-form template for copying, not an actual work or approval record. Use it to manage Intent and Spec in one file for a typical design change. For changes spanning multiple sessions, components, or contracts, use the split-form `01-INTENT.md` and `02-SPEC.md`. Follow [01-DESIGN.md](../../01-DESIGN.md) §2 and §4 for the selection criteria and process.

## Metadata

- **Change ID:** {{CHANGE_ID}}
- **Status:** Draft
- **Originator:** Requester or source of the request
- **Source:** Verifiable request, conversation, or issue. For a reconstruction, record the source material and that it was reconstructed
- **Parent:** Applicable revision and section of the [Product Baseline](../../00-PROJECT.md), or the parent design
- **Decision:** Decision ID from PROJECT §8
- **Approval:** Not approved — when approved, record the person, scope, document version, and verifiable evidence
- **Execution:** Work item in the [Global TODO](../../02-TODO.md). If a separate detailed execution plan is needed, use `03-PLAN.md`

When converting from the combined form to the split form, move the content and do not leave this file as the source of truth.

## 1. Intent

### 1.1 Problem

Describe the current problem, the affected users or systems, and verified evidence.

### 1.2 Expected Outcome

Describe the result that would resolve the problem. Keep it distinct from implementation approaches that have not yet been selected.

### 1.3 Scope and Non-goals

Describe what this request includes and excludes.

### 1.4 Constraints

Preserve compatibility, security, schedule, and operational constraints, along with implementation requirements explicitly stated by the user.

### 1.5 Open Questions

Separate questions that must be answered before the next step from those that can be deferred.

## 2. Spec

### 2.1 Requirements and Scenarios

| Requirement ID | Requirement | Situation / Input | Observable Result | Verification |
|---|---|---|---|---|
| R-001 | Example requirement | Condition | Result | Check |

Cover success, failure, and boundary conditions, and confirm that the questions in Intent have been resolved. `R-nnn` is unique only within this change directory.

### 2.2 Alternatives and Rationale

Record alternatives, including making no change, along with the reasons for the selection and rejection.

### 2.3 Design and Contracts

Describe components, responsibilities, data flow, public contracts, error handling, and parent invariants. Keep requirements distinct from implementation methods.

### 2.4 Impact on Parent Design

Record the decision IDs and sections that this change preserves, extends, or replaces, and why. Do not establish an unconditional priority over the entire document.

### 2.5 Risks, Compatibility, and Rollback

Describe compatibility, transition and deployment order, recovery after failure, and verification conditions.

### 2.6 Completion Criteria and Open Items

State the conditions for verifying this change and the remaining questions. Specify which kind of completion is required: implementation, merge, release, or support verification. Keep execution checkboxes and current status only in the execution source of truth.

## 3. Change Log

When requirements change, record the reason and scope of reapproval. When contracts or completion criteria change, record the superseded decision and revision. Do not silently overwrite the original request or fold new requirements into a prior approval.
