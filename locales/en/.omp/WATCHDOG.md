# Advisor Review Priorities

This file contains instructions only for the OMP advisor (watchdog model). It is not included in the primary agent's context and does not behave like `AGENTS.md`. The canonical document for review decision criteria is `docs/REVIEW.md`, which is imported verbatim below. When changing the policy, edit only `docs/REVIEW.md`.

@../docs/REVIEW.md

## Pay Particular Attention to These Items in This Session

- Changes that violate `docs/REVIEW.md` §6 Project-specific Invariants. If the primary agent passes over an invariant without mentioning it, raise it as a `concern`.
- Changes that reverse, without justification, a decision recorded as `Accepted` in `docs/00-PROJECT.md` §8. If there is evidence that the decision's premise has broken, include that evidence.
- Violations of the Change Rules in `AGENTS.md` — refactoring beyond the requested scope, a new production dependency without agreement, a commit or push without an explicit request, or secrets left in code, logs, or documentation.
- Cases where the primary agent proceeds based on assumptions about code it has not read. Changing a function signature without checking its callers is a representative example.
- Cases where the primary agent starts implementing a change covered by the applicability criteria in `docs/01-DESIGN.md` §1 without following the design procedure.

## Do Not Report

- Items covered by `docs/REVIEW.md` §8 Do Not Report
- Requests to reverse deferred items recorded in §9 Accepted Deferrals and `docs/00-PROJECT.md` §12
- Problems the primary agent has already identified and is addressing
