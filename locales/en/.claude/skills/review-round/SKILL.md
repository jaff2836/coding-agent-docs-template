---
name: review-round
description: Run a review round. Repeat wait for reviews → inspect reviews → fix → commit, then finish according to the on_pass default when the round passes (merge a PR after user confirmation; do not merge when there is no PR). Run only when the user explicitly invokes it.
argument-hint: "[number of rounds]"
disable-model-invocation: true
---

# Review Round
<!-- template-skill-contract:review-round:v1 -->

The following `[template-contract:v1]` assertions are normative. Localized prose must not contradict them.

<!-- template-skill-fixture:review-round-explicit-only -->
> [template-contract:v1] MUST_REQUIRE_EXPLICIT_USER_INVOCATION
<!-- template-skill-fixture:review-round-exact-head-gate -->
> [template-contract:v1] MUST_GATE_ON_EXACT_HEAD_AND_BASE
<!-- template-skill-fixture:review-round-user-confirmed-merge -->
> [template-contract:v1] MUST_REQUIRE_USER_CONFIRMATION_BEFORE_MERGE

**Run only when the user explicitly invokes this skill.** Do not run it automatically based on model judgment. This procedure performs commits and merges.

1. Read `docs/REVIEW_ROUND.md` and follow its procedure exactly. → [docs/REVIEW_ROUND.md](../../../docs/REVIEW_ROUND.md)
2. Use `docs/REVIEW.md` as the decision criteria. → [docs/REVIEW.md](../../../docs/REVIEW.md)
3. Use defaults only for parameters the user did not specify: 5 rounds, threshold `all P0 = 0, all P1 = 0, blocking P2 = 0`, `rereview = auto`, and no branch deletion. If external reviewers are used and the reviewer table (§2.1) is empty, do not start; request registration. `reviewers = self` starts without registration and neither requests nor waits for external reviews. When there is no PR, default to `on_pass = do not merge`.
4. Read back all confirmed parameters, including the user-specified threshold, before starting. If the user explicitly changes one during the round, record and reevaluate it under §2; do not arbitrarily enforce or relax the defaults.
5. After a pass, freeze the head and record remaining items in the session handoff list. Do not add a record-only commit or push to the current PR; update repository documentation in the next task according to §9.

This file is an adapter. The two documents above are canonical for the procedure and policy; if they conflict with this file, follow the documents.
