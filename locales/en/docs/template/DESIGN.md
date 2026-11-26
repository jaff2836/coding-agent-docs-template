# Change Design Process

> This document defines the shared process for producing designs. The product baseline is in [00-PROJECT.md](./00-PROJECT.md), global work is in [02-TODO.md](./02-TODO.md), and document ownership and branch operation are in [DOCS_GUIDE.md](./DOCS_GUIDE.md).

## Metadata

- **Status:** Active
- **Owner:** Describe as appropriate for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When the design process itself changes

## 1. When to Apply This Process

Apply this process to the following changes.

- A change to structure, technology stack, public contracts, or data schemas, or one that requires a migration
- A change with at least two reasonable alternatives that requires a trade-off decision
- A new feature or user behavior change whose requirements are ambiguous, or whose intent and requirements must be preserved across multiple sessions
- A request in which the user explicitly invokes the `design` skill

Do not repeat the full process for the following.

- A clear bug fix whose cause is not structural
- A clear change within one module that does not alter an external contract
- A clear change limited to documentation, tests, or comments
- Implementation of an already approved product or extension SPEC or decision. Link its requirements and completion criteria and write only the necessary implementation plan. If the requirements, contracts, or completion criteria need to change, apply this process to that change.

An explicit `design` invocation takes precedence over the exceptions. Use the minimum deliverables below for a small request. When the request is unclear, ask only the questions needed to make a decision, and do not ask the user to reapprove something already agreed in the conversation.

## 2. Scale and Deliverables

Separate document roles first, then choose the number of files appropriate to the scale of the work. Do not create three files for every change.

| Change | Deliverables |
|---|---|
| Clear, small task | Global TODO item or work report. Do not create a new design file when the design process does not apply |
| Typical design change | A single `docs/changes/<change-ID>/01-CHANGE.md` with Intent and Spec sections; implementation plan in the global TODO |
| Change spanning multiple sessions, components, or contracts | `01-INTENT.md` and `02-SPEC.md` in the change folder; add `03-PLAN.md` when a detailed execution plan is needed |
| Phased implementation of an approved product or extension design | Reference the applicable section and completion criteria in the parent design. Write only a TODO or change-specific PLAN; do not mechanically rewrite the INTENT and SPEC |

Prefer the split format for migrations, public contract changes, or work that requires multiple PRs or local review units. Do not judge safety or design completeness by the number of files alone.

Copyable templates are in `docs/changes/_template/`. Keep the combined, split, and PLAN templates in that folder when adopting the template. The folder itself is not work and must not be counted as a project decision or progress. For an actual change, copy only the needed files into a new change-ID folder and replace the examples. If only `03-PLAN.md` is needed, point it to the parent SPEC and remove links to sibling files that do not exist.

In both formats, link the decision and canonical location from [00-PROJECT.md](./00-PROJECT.md) §8, and add one change-level item to [02-TODO.md](./02-TODO.md). Do not duplicate design details in both places. When a PLAN exists, manage detailed work and verification status for that change only in the PLAN, and leave only links and integration-level information in the global TODO.

If a decision affects review judgments, update both [REVIEW.md](./REVIEW.md) §6 Project-specific Invariants or §9 Accepted Deferrals and the corresponding copy in [.cursor/BUGBOT.md](../.cursor/BUGBOT.md). Existing commit authority rules still apply.

## 3. Stages

### 3.1 Confirm Intent — Intent

- Record the request source, current pain point, expected outcome, target users, scope and non-scope, constraints, and open questions.
- If the user specifies an implementation approach, preserve it as a constraint. Do not turn an implementation method that has not yet been selected into a requirement.
- Compare the intent with [00-PROJECT.md](./00-PROJECT.md) §1–§4 and the relevant parent designs.
- If the original conversation is unavailable, summarize only what existing materials establish, and identify it as `Reconstructed from existing materials` with its evidence. Do not invent past requests, approvals, or dates.

### 3.2 Requirements and Scenarios — Spec

- Give every requirement an identifier and verifiable conditions.
- Link each requirement to at least one situation, input, and observable result. Cover relevant failure and boundary conditions as well as success.
- Read actual code and the callers and consumers of the contract, and expose conflicting requirements or unresolved questions.
- Keep requirements and implementation methods in separate sections.

### 3.3 Compare Alternatives

- Consider options in this order: can it be avoided → does the codebase already provide it → standard library → platform capability → installed dependency. Then propose the minimum necessary change.
- Compare at least two alternatives. If there is only one, include making no change as an alternative.
- Record scope, risk, compatibility, rollback, new dependencies, and rejection rationale. A new production dependency requires user agreement.

### 3.4 Design — Spec

- Define components, responsibilities, boundaries, data flow, public contracts, error and failure handling, migration and deployment order, and rollback.
- Link a verification method to each requirement.
- Compare the design with the invariants in [REVIEW.md](./REVIEW.md) §6 and the current and target structures in [00-PROJECT.md](./00-PROJECT.md).
- Identify the exact decision ID and section in the parent design that this design extends or replaces. Do not replace an entire parent design merely because this is a new document or has a higher number.

### 3.5 Execution Plan — Plan

- List affected files and components, order, prerequisites, and verification methods.
- Divide the work into units that can each be reviewed in one PR or local review unit.
- Choose either the global TODO or a change-specific PLAN as the canonical source for detailed work. Do not add a separate TODO inside the change folder.
- For parallel work, divide ownership by change-ID and file scope. Define the integration order and re-verification conditions for work that changes the same files or contracts.

### 3.6 User Agreement

Present the problem and scope, requirements, alternatives and selection rationale, design, risks and rollback, work and verification plan, and deliverable locations together. **Do not begin implementation before agreement.**

Proceed without renewed approval for scope already approved in the conversation. Confirm only newly discovered decisions that have not been agreed. For phased implementation of an approved design, confirming the parent approval and completion criteria is sufficient. Record the agreement according to §4 when it is reached. Keep a proposal requested only for documentation as `Draft` or `Proposed`.

## 4. Deliverables and Update Rules

### Identification and Approval

- A change-ID is a stable identifier independent of branch names and PR numbers. Use a collision-resistant `<UTC date>-<unique slug>` or an existing issue ID. Do not reuse it anywhere in the repository, including parallel branches.
- Issue `D-nnn` globally when adding a decision to [00-PROJECT.md](./00-PROJECT.md) §8. Issue `T-nnn` globally when adding an item to [02-TODO.md](./02-TODO.md). Do not reserve a `D-nnn` for a decision not yet in PROJECT; refer to it by change-ID instead.
- `R-nnn` and `W-nnn` in a SPEC or PLAN need only be unique within that change folder. Refer to them from another document as `<change-ID>/R-001`.
- If global `D-` or `T-` IDs collide across parallel branches, preserve the number already integrated and renumber only the side that has not yet been integrated. Do not renumber change-IDs or existing global IDs.
- Record the approval state of an Intent and Spec as `Draft / Accepted / Superseded / Rejected`. Record the approver, scope, and verifiable evidence such as a conversation or document revision.
- PROJECT §8 is authoritative for decision status; a document's approval status applies to that document. Link the approval records. Do not treat a new proposal added to an approved SPEC as part of the existing approval.
- Do not infer user approval from Git authorship or the existence of a commit. Authoring or approving a file does not delegate commit, push, merge, or deployment authority.

### Combined and Split Formats

Copy the [combined template](./changes/_template/01-CHANGE.md) for `01-CHANGE.md` and use the following sections. The details are the same as in the split templates.

1. Metadata — change-ID, approval state and evidence, parent design, decision ID, and location of execution work
2. Intent — request, problem, outcome, scope, constraints, and open questions
3. Spec — requirements, scenarios, design, alternatives, compatibility, and verification

The split format uses the [INTENT template](./changes/_template/01-INTENT.md), [SPEC template](./changes/_template/02-SPEC.md), and [PLAN template](./changes/_template/03-PLAN.md). When converting from the combined format to the split format, move the content and do not leave the old file as a canonical source. Update references and approval evidence to point to the new location.

### Document Lifecycle

- Intent preserves the original request. If requirements change, record why and what needs reapproval; do not silently overwrite the original request.
- If contracts or completion criteria in a Spec change, confirm the impact and user agreement before implementation. In PROJECT, preserve a changed decision as `Superseded` and link it to the new decision.
- An approved version must remain identifiable by a Git revision or a separate preserved copy. If it has not been committed, preserve the existing approved content and distinguish the unagreed new content. Do not create a commit automatically for recordkeeping.
- A Plan is updated to match implementation. Maintain work order and verification results, but do not use it to change the Spec's requirements or completion criteria.
- Product baselines and long-term extension designs are living documents. Do not freeze their entire contents after implementation starts. Distinguish the historical agreement for an individual change from the current product description.
- Completion of change-specific checkboxes means implementation and verification on that branch. It does not mean integration, release, or support verification is complete.
- Keep folders for completed and cancelled changes. Do not delete them when implementation finishes. PROJECT is the current product baseline; do not read a completed SPEC as the current contract.
- Move an implemented contract into PROJECT's current architecture and contracts only after it has reached the specified integration target and changed the supported scope. For cancellation, mark the Intent or Spec `Rejected` and the global TODO item Cancelled. For deferral, use TODO Blocked and record the resume condition.
- After a review round passes, do not change tracked documentation, including the PLAN, in a way that changes the head. Carry judgments and handoff records into the next relevant task according to [REVIEW_ROUND.md](./REVIEW_ROUND.md) §7 and §9.

## 5. Do Not

- Require INTENT, SPEC, and PLAN for every small request or implementation phase of an approved design
- Duplicate the same detailed checklist and progress status in both the global TODO and a change-specific PLAN
- Treat design approval, branch implementation, integration, release, and support verification as the same kind of completion
- Interpret file numbers as priority or decision IDs
- Use change-local IDs as global `D-` or `T-` IDs, or read a completed change SPEC as the current product baseline
- Record unagreed content as the current product or decided target architecture
- Put project-specific design or operational status in this process document

## 6. Existing Product and Extension Designs

- Preserve an existing design document by default and link it from PROJECT's design index. Do not recast historical records as a new INTENT or move all content into a change folder.
- If the user requests integration, merge the base product design into PROJECT. Consolidate duplicate explanations and work status while preserving decision IDs, rationale, contracts, verification conditions, and references.
- For long-term extensions, use the optional [10-EXTENSION.md](./10-EXTENSION.md) or link an existing extension document. Do not maintain the same design in two places.
- In an extension design, record the applicable parent revision and sections, preserved and replaced scope, phase dependencies, and completion criteria. Refer to TODO or PLAN for the current status of each phase.
- If an existing design has its own checklist, state which document owns detailed status and replace duplicates elsewhere with links. If a phase has already been approved, its implementation remains an exception under §1.

## 7. External Specification Tools

Change artifacts from an external tool may replace the INTENT, SPEC, and PLAN serving the same roles. PROJECT retains the index of decisions and canonical locations, and the global TODO retains the change-level plan. Manage detailed design and execution status only in the designated tool artifact. Follow [TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) §4 for coexistence rules.
