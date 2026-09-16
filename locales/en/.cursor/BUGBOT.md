# Bugbot Review Rules

Bugbot reads only this file for the project's review rules. The decision criteria from [`docs/REVIEW.md`](../docs/REVIEW.md) are therefore duplicated below. If the two documents conflict, `docs/REVIEW.md` is canonical. Update both files together when changing the policy.

## Language

- Write all review explanations and summaries in English.
- Preserve code identifiers, file paths, configuration keys, and code quotations in their original form.

## Severity

- **P0:** Data loss, data corruption, a security hole, or a crash on a common path.
- **P1:** A defect that has a real user impact under normal usage conditions — incorrect results, a hang, a leak, a stuck state machine, or functionality that cannot work in production with the current configuration.
- **P2:** A defect with limited impact or rare triggering conditions, or a meaningful robustness gap.
- **P3:** Worth noting, but not serious enough to block a merge.

Assign P0 or P1 only after tracing the defect end-to-end from its triggering condition through its impact.

## Confidence

Estimate how certain you are, after reading the code, that the defect is real.

- `0.9` or higher: You traced it end-to-end and it holds.
- Below `0.6`: It is speculation. Do not report it; discard it.

## Blocking

Mark every finding as blocking or non-blocking. This value is independent of severity.

- **blocking:** This PR introduced the defect or directly touched and worsened an existing defect.
- **non-blocking:** The defect is pre-existing and untouched, is superficial, or is explicitly recorded in repository instructions as known, deferred, or a planned follow-up.

Report non-blocking findings as well; they provide useful context. The default review-round pass condition requires zero P0 findings, zero P1 findings, and zero blocking P2 findings, so P0 and P1 findings block a pass by default even when non-blocking. The user may change the threshold, and the review-round executor decides what passes, what must be fixed, and what may be handed off, using the confirmed threshold. Do not change a finding's blocking classification merely because it prevents a pass. A defect the author is already tracking as carried-over work must be non-blocking. Compare findings against the items under "Accepted Design Decisions and Approved Deferrals" below. An approved deferral does not exempt a P0 or P1 finding from the default threshold. Do not relitigate a design that the instructions explicitly describe as intentionally staged across multiple PRs.

## This Repository's Invariants
<!-- template-section:project-invariants -->

Bugbot cannot read `docs/REVIEW.md` §6, so the same list is included here. Every item must include the incorrect behavior, its impact, and the safe path, and the lists in the two files must always match. `scripts/check-docs.py` compares them.

- **{{PROJECT_INVARIANT_1}}**
- **{{PROJECT_INVARIANT_2}}**

## Accepted Design Decisions and Approved Deferrals

Duplicate here the items from `docs/REVIEW.md` §9 Accepted Deferrals and `docs/00-PROJECT.md` §8 Decisions that affect review decisions. A request to **reverse** a decision listed here is not new information and should not be reported. **Evidence that a decision's premise has broken** (the code behaves differently from what the document promises, or a condition assumed by the decision no longer holds) is new information and should be reported with that evidence.

- Approved deferrals: leave this list empty when there are no actually approved `DFR-*` items
- Accepted decisions: list only `D-*` items for which a finding demanding reversal must not be created

## Required Finding Fields

Severity, confidence, blocking status and rationale, exact changed location, reproducible triggering condition, impact, minimal safe fix direction, and exact lines of code that provide the evidence.

## Do Not Report

- Problems deterministically detected by a formatter or linter
- Speculation without a concrete triggering condition (confidence below 0.6)
- Personal style or architecture preferences
- Pre-existing problems unrelated to this PR (except end-to-end verified P0 and P1 findings, which must be reported as non-blocking)
- Naming or comment preferences with no behavioral impact
- Findings based only on the number of tests being low
- Findings based only on an implementation of an approved parent design lacking INTENT or SPEC files
- Duplicate findings with the same root cause
- Requests to reverse a decision recorded under "Accepted Design Decisions and Approved Deferrals" above

Do not infer approval or completion from a design document's filename or checkboxes alone. Verify completion claims against code and validation evidence, and distinguish branch implementation and validation completion in a change-specific PLAN from integration, release, and support validation completion in the global TODO.

If there are no significant problems, do not invent one. Explain the scope reviewed and its limitations.
