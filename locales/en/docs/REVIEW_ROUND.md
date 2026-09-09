# Review Round Protocol

Apply this document **only when the user explicitly starts a review round**. For an ordinary PR or diff review, apply only [REVIEW.md](./REVIEW.md), not this procedure.

As an exception, in the **next related implementation or documentation task** that receives a session handoff list from an earlier round, apply only the documentation update procedure in §9. That alone does not restart the round or delegate the authority described in §1.

While [REVIEW.md](./REVIEW.md) defines **what counts as a defect**, this document defines **who fixes, commits, and merges the results, and when**.

## Metadata

- **Status:** Active
- **Owner:** Customize for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When the round policy or scope of delegated authority changes

## 1. Delegated Authority

[AGENTS.md](../AGENTS.md) prohibits commits, pushes, branch deletion, and deployment without an explicit request. Starting a round creates a **scope-limited exception** to that prohibition.

**Delegated actions** — only within the parameters confirmed at the start or explicitly changed later by the user:

- Fixing code for valid findings
- A commit for each round
- A non-force push to the target branch. In configurations where a reviewer is triggered by pushes, a push usually starts the next round. The actual condition that starts a round is defined by §3 and §4 (a base change starts a new round even without a push)
- When `rereview = request`, **requesting a rereview** through a method registered in the §2.1 table — posting a trigger comment or calling a reviewer-request API. Use the registered text or call exactly and do not alter it arbitrarily
- Marking **inline threads for addressed findings as resolved** under §6. Do not close threads for findings that were not addressed
- On pass, merging **after user confirmation**

**Actions not delegated:**

- Branch deletion, local or remote
- Force pushes and history rewriting
- Changes to files or branches outside the target branch
- PR comments other than rereview requests, and mentions instructing a reviewer to modify code. Some reviewers interpret extra words after a trigger phrase as a coding task rather than a review, then push to the branch. Such a push is outside the delegated scope
- Deployment, release publication, tag creation, migration execution, and dependency installation
- Arbitrary changes to the number of rounds or threshold
- Merge without user confirmation

In any run that has not read this document, the default prohibitions in [AGENTS.md](../AGENTS.md) continue to apply.

## 2. Parameters

| Parameter | Default | Description |
|---|---|---|
| `rounds` | `5` | Maximum number of rounds |
| `threshold` | `all P0 = 0, all P1 = 0, blocking P2 = 0` | This default may be changed by the user. Count valid, unresolved findings; by default, count all P0 and P1 findings and P2 findings with `blocking=true` under [REVIEW.md](./REVIEW.md) §4.3 Blocking |
| `target` | Current branch or PR | Target of the rounds |
| `reviewers` | All standing reviewers in §2.1 | Reviewers whose results must be awaited. Registered entries are in §2.1. When set to `self`, the executor reviews directly under [REVIEW.md](./REVIEW.md) without registration. External review requests and waiting, along with the quorum, timeout, and head-alignment rules in §4, do not apply. Follow §7 for the ledger location |
| `reviewer_timeout` | `45 minutes` | Maximum time to wait for one reviewer's result |
| `rereview` | `auto` | How to obtain a rereview after a push within a round. `auto` relies only on the reviewer's own triggers. With `request`, the executor directly requests reviews only from reviewers with a method registered under `Rereview request method` in the §2.1 table (§3). Use `request` only when the user specifies it |
| `on_pass` | For a PR, merge after user confirmation; without a PR, `do not merge` | With `do not merge`, report the passing result and handoff items, then stop. In all modes, update repository documentation during the next task under §9 |
| `close_branch` | Do not close | Not within delegated authority |

**A user-specified threshold takes precedence over the default.** Use the table's default only when the user did not specify one. The pass decision, items to fix, and items to hand off must all use the threshold actually confirmed. For example, if the user requires only `all P0 = 0, all P1 = 0`, a P2 finding may be handed off even when `blocking=true`. Conversely, if the user requires zero P2 and P3 findings as well, those findings must be resolved. Changing severity or `blocking` classification is separate from changing the threshold.

If the user explicitly changes the threshold while work is in progress, record the old value, new value, effective point, and request in the session ledger; read back the new value; and reevaluate current findings. The executor must not relax it arbitrarily to force convergence. A threshold change does not alter quorum, required validation, or merge authority.

Before starting, read the confirmed parameters back to the user. Do not begin a round without this readback. If external reviewers are used with `rereview = auto` and none of the standing reviewers in §2.1 has `automatic on push` as its `Rereview request method`, include in the readback that the standing-reviewer quorum may be impossible from the second round onward, and ask whether to change to `request`. If the user keeps `auto`, proceed as specified. With `reviewers = self`, do not use `rereview` or `reviewer_timeout`. Merging between branches without a PR requires separate instructions for the target branch and method.

The actual number of rounds required varies substantially with PR size and reviewer count. `rounds` is only a starting budget; when it is exhausted, propose an extension under §6.

The default threshold is stricter than the verdict rules in [REVIEW.md](./REVIEW.md) §10 Review Conclusion. A verdict becomes `request_changes` only for blocking P0 or P1 findings, but under the default round threshold every P0 and P1 finding and every Blocking P2 prevents a pass. Keep `blocking` as the relationship between the change and the defect; do not change `false` to `true` merely because a finding prevents a pass.

A single valid, unresolved finding affects the default threshold as follows. Do not count an invalid finding or one confirmed as resolved in the current code.

| Severity | `blocking=true` | `blocking=false` |
|---|---|---|
| P0 | Does not pass | Does not pass |
| P1 | Does not pass | Does not pass |
| P2 | Does not pass | Does not prevent a pass |
| P3 | Does not prevent a pass | Does not prevent a pass |

### 2.1 Reviewer Registration

The Maintainer fills in this table when applying the template. Investigate and record **every** reviewer that actually runs in the repository. Omitting a reviewer makes the §4 quorum calculation incorrect. Do not edit this document during a round. If external reviewers are being used and the table is empty, do not start the round; ask for reviewers to be registered. `reviewers = self` does not use this table and may start even when it is empty.

Reviewers are classified by **arrival cadence**. This distinction determines **only whether to wait**, not the value of a finding.

- **Standing reviewer:** Leaves a result for every change. Included in the §4 quorum.
- **Intermittent reviewer:** Leaves a result only for some changes, or only once per PR. Not included in the quorum; add it to the pool only in rounds where a result arrives. If a reviewer that runs once per PR is included in the quorum, the quorum can never be reached from the second round onward.

| Reviewer | Publication location | Head identification method | Arrival cadence | Behavior when no problems exist | Rereview request method |
|---|---|---|---|---|---|

Record the following in each column.

- **Publication location:** Whether results appear in a PR comment, PR review body, or inline thread. **If a reviewer writes in multiple places, list all of them.** For PR comments, state whether it creates a new comment for each head or overwrites one comment (sticky). Reviewers that overwrite have different ledger rules under §7
- **Head identification method:** How to determine which commit a result examined, such as a marker comment, SHA in the body, or round number
- **Arrival cadence:** Standing or intermittent. For an intermittent reviewer, state the condition under which it runs
- **Behavior when no problems exist:** Whether it still leaves a result. The §4 timeout handling depends on this value
- **Rereview request method:** How to obtain another review for a new push. Record one of the following:
  - `automatic on push` — Reruns by itself on every push. Also record the trigger condition, such as a ruleset or workflow event
  - Request method — The exact trigger-comment body or API call and **how to confirm that the request was accepted** (for example, a reaction emoji, the reviewer appearing in REST `requested_reviewers`, or the reviewer appearing in GraphQL `reviewRequests`. A reviewer may disappear from the request list once it starts running, so check immediately after the call). Use field values from the relevant API verbatim as identifiers. REST bot usernames often include `[bot]`, while GraphQL `Bot.login` often does not. Do not treat spellings from different APIs as the same string. With `rereview = request`, the executor carries out this column exactly
  - `unavailable` — There is no rereview mechanism. This reviewer must have an intermittent arrival cadence

If this column is empty for a public reviewer that runs "once per PR," even `rereview = request` cannot obtain another review. Automatic review usually runs only when a PR is opened, not on every push, so confirm the rerequest method in the tool documentation and record it here.

## 3. The Four Steps of One Round

```text
[1. Wait for reviews] → [2. Inspect reviews] → [3. Fix] → [4. Commit]
```

**1. Wait for reviews** — Request reviews and freeze the target code until results arrive. Because reviewers take different amounts of time, wait until the quorum condition in §4 is met or `reviewer_timeout` is reached. Use the following request behavior.

With `reviewers = self`, instead of making external requests or waiting, review the current target directly under [REVIEW.md](./REVIEW.md), then proceed to step 2. The external-request branches below do not apply.

- **Round 1:** Use an existing result that reviewed the current head and do not request it again. Reviewers that run automatically when a PR is opened often have already left a result. With `rereview = request`, only for confirmed `reviewers` that have an **explicitly executable request method** such as a comment or API in §2.1 and do not have a result for the current head, execute that method even without a push and confirm acceptance as described for `request` below. Do not request a reviewer whose only registered method is `automatic on push` at this stage.
- **A round after a push:** For a reviewer whose `Rereview request method` in §2.1 is `automatic on push`, the push itself is the request. For all other reviewers, follow `rereview`:
  - `auto` — Do not request; wait. If no result arrives, apply the timeout rules in §4.
  - `request` — Immediately after the push, and only for confirmed `reviewers` with a request method other than `automatic on push`, execute the method in the table **exactly**. A trigger comment must contain only the registered body, with no added sentence. Confirm acceptance using the method from the table. When the confirmation signal is included in the request response, such as GraphQL `reviewRequests`, decide from that response immediately. When the signal arrives separately, such as a comment reaction, check once immediately; do not treat its absence as failure; then recheck until the signal appears or the acceptance-confirmation limit is reached (2 minutes by default, separate from `reviewer_timeout`). If the limit is exceeded without a signal, report it to the user immediately without waiting for `reviewer_timeout`. Some reviewer APIs return a success response while doing nothing, so do not use the response code alone as proof of acceptance. **A reviewer whose request was confirmed counts toward the §4 quorum for that round** — wait until its result arrives or `reviewer_timeout` expires. Passing without waiting merely because standing reviewers arrived first defeats the purpose of this mode.
- **A round without a push:** Do not request a rereview. A second review of the same head is not a new round. The exception is a **base change** under §4. Because a base change alters the diff even when the head is unchanged, handle it like a round after a push — request under `rereview = request`, or wait under `auto`. If an `automatic on push` reviewer's trigger excludes base changes (retargeting is `edited`, not `synchronize`), its result will not arrive; record `no result` under the §4 timeout rules and disclose it at the §6 confirmation step.

**2. Inspect reviews** — Combine arrived results under §4, decide whether each finding is valid or invalid (§5), and evaluate the threshold. **Make the pass decision at this point.**

**3. Fix** — Fix valid, unresolved findings required to meet the confirmed threshold. Under the default, these are every P0, every P1, and every Blocking P2. Other findings may be fixed as well, and those changes will be reviewed in the next round. Under the default, a pre-existing or carried-over P0 or P1 still prevents a pass; if fixing it requires work beyond delegated scope, stop under §8 and await user direction.

**4. Commit** — Run the Build, Test, Lint, and Typecheck commands from [AGENTS.md](../AGENTS.md) in proportion to risk and record the results. In a repository with generated files, validation includes regeneration and generated-output checks. Do not run validation that incurs charges or calls external services during the round. Rounds repeat the same validation, so costs and side effects accumulate. If validation fails, do not commit; report the failure. Include the round number and addressed finding IDs in the commit message.

## 4. Combining Results from Multiple Reviewers

With `reviewers = self`, skip this section and proceed to §5.

The purpose of multiple reviewers is for one to catch what another misses. Therefore, **collect every finding from every reviewer and never discard one because of which reviewer reported it.** Do not assign reviewer-specific weights to findings. The standing/intermittent classification in §2.1 determines **only whether to wait**, not the value of a finding.

**Collection:** Collect findings from every reviewer whose result arrived into one pool. **One reviewer's result may be split across several locations.** Read at least all of the following.

- PR comments, including sticky bot comments
- The top-level body of a PR review
- **Inline review threads attached to lines**, both unresolved and resolved
- Follow-up replies in threads. Reading only the first comment can miss withdrawals or additional evidence
- **Collapsed `<details>` blocks** in a review body. Some reviewers put low-confidence findings in a collapsed block such as "Suppressed comments." A collapsed finding is still a finding and must be decided under §5

**Do not assume the top-level summary contains every finding from that reviewer.** In practice, a summary may say "no defects" or `approve` while an inline thread contains a blocking finding. When a summary conflicts with an inline comment, the inline comment has the more specific evidence.

The unresolved-thread list is itself a signal. Check it both when starting a round and when making the pass decision.

**Head alignment:** Determine which head each result reviewed. Do not use a result for a different head to decide the current round. As an exception, for a reviewer that leaves no head identifier and runs only once per PR, directly verify whether its findings are resolved at the current head and record the evidence. Do not discard them merely because they are old.

**Base changes:** If the PR base changes — through retargeting to another branch, merging or rebasing the base branch, or merging the lower PR in a stacked PR — the diff examined by reviewers differs from the current diff. Even if the head SHA appears unchanged, do not use prior results as decision evidence; count a new round. The only base update the executor may perform is to **merge** the base branch into the target branch, within the non-force-push authority in §1. Rebasing requires a force push and is not delegated; retargeting and merging the lower PR happen outside the round. Every such case consumes one round.

**Review scope:** If a reviewer self-reports **partial review** in its result, such as a truncated diff, only some files reviewed, or reconstruction after a parsing failure (salvage), record that result as a `partial result`. A partial result still meets quorum, and the round may proceed to a pass. However, through the same flow as an invalidity decision under §5, disclose before merge **which reviewer's result was partial and what it did not review**. An `approve` on a partial result approves only the reviewed scope. If the same reviewer produces a partial result in every round, the PR is too large for that reviewer; propose splitting it under §8.

**Quorum:** Make a pass decision **only after every standing reviewer has produced a result for the same head**. Do not declare a pass from only the results that arrived. A late reviewer may have a blocking finding.

**Timeout:** If a reviewer has not produced a result after `reviewer_timeout`, record `no result` for that reviewer and continue the round. Silence means different things for different reviewers.

- Silence from a reviewer that does not leave a result when there are no problems is normal and may be treated as `no findings`.
- Silence from a reviewer that always leaves a result even when there are no problems is a failure signal. Do not treat it as `no findings`.

Do not automatically declare a pass when a standing reviewer has `no result`. Even if every other reviewer meets the pass condition, identify **which reviewer's result is missing** at the §6 merge-confirmation step and obtain the user's decision. With `on_pass = do not merge`, do not report a pass without merge; report that the decision is deferred for insufficient results and that you are **waiting for direction**.

**Severity normalization:** When a reviewer does not use the P scale from [REVIEW.md](./REVIEW.md), whether it uses its own High/Medium/Low labels or none, the executor reclassifies the finding using the "Severity" definitions in REVIEW.md. Preserve the reviewer's original label in the reviewer column of the decision record. Reclassification means comparing against definitions, not downplaying findings — if the triggering condition and impact are traced end-to-end, assign the matching value; otherwise use P2 or below, while deciding `blocking` separately. If a reviewer's P classification clearly conflicts with the definitions, reclassify it in the same way and record the rationale.

**Deduplication:** Combine findings with the same root cause into one.

- Use the **highest severity**.
- Set `blocking` to `true` **if any instance is `true`**.
- Record what each reviewer reported and how it classified the finding.

**Do not combine verdicts.** A reviewer's `approve` or `request_changes` verdict is only a reference signal and is not used in threshold calculation. Divergent reviewer verdicts are not a decision conflict; they mean one side has a finding the other did not see. Decide that finding under §5 and the conflict disappears.

## 5. Deciding Findings

Classify every finding as either **valid** or **invalid**. Do not include invalid findings in threshold calculations.

A finding may be classified as invalid when:

- It falls under [REVIEW.md](./REVIEW.md) §8 Do Not Report
- The reported behavior does not occur in the actual code
- Another code path already handles it

`blocking=false` is not a reason to mark a finding invalid. Determine validity for confirmed defects in existing code, carried-over work, and intentionally staged designs, then classify `blocking` separately. Do not mark end-to-end verified P0 or P1 findings that [REVIEW.md](./REVIEW.md) §3 Review Scope allows as invalid merely because they are unrelated existing problems. **Under the default threshold, count P0 and P1 findings even when `blocking=false`; only non-blocking P2 and every P3 do not prevent a pass.** An approved deferral is not a P0 or P1 exception under the default threshold. If the user specified another threshold, decide under the value confirmed in §2.

An invalidity decision must include all of the following.

- **Counterevidence:** A file and line number, or the command run and its output
- Which of the reasons above applies
- The conditions under which the counterevidence holds and what would break those conditions

This document refers to [REVIEW.md](./REVIEW.md) using both section numbers and heading names. If it has been merged into an existing repository whose REVIEW.md has different or missing numbers, correct each reference using the heading name. A number alone may prevent a round executor from finding the supporting section.

Make invalidity decisions without user confirmation. Record the evidence in the ledger and present **every** invalidity decision at the confirmation step immediately before merge. **If you cannot write the evidence, treat the finding as valid.**

When a finding with the same root cause recurs, compare it against the prior decision and evidence. If the relevant code, contract, and assumptions have not changed and there is no new evidence, reuse the prior decision. If new evidence exists or a fix changed an assumption, verify it again; do not discard it merely because it is repeated.

## 6. Pass Decision and Exit Branches

```text
[2. Inspect reviews] quorum met → combine → decide → evaluate confirmed threshold
        │
        ├─ pass → freeze head · finalize session handoff list
        │           ├─ do not merge → report pass without merge → finish
        │           └─ merge → user confirmation → status check → merge same head → finish
        │                (documentation is updated in the next task)
        │
        └─ does not pass → [3. Fix] → [4. Commit]
                              │
                              ├─ rounds remain ─→ [1. Wait for reviews]
                              │
                              └─ rounds exhausted ─→ do not merge; propose extension and wait for direction
```

**When the round passes:**

1. **Freeze the passing head.** Treat the review used for the pass decision as the final review of this head. After the pass, do not modify code, add a record-only commit or push, or request another rereview.
2. **Record remaining valid findings in the session handoff list.** Items may be handed off only when the confirmed threshold allows them to remain. Under the default these are non-blocking P2 and every P3; a user-specified threshold may differ. Do not modify tracked files such as [02-TODO.md](./02-TODO.md) or [REVIEW.md](./REVIEW.md), and do not post a PR decision comment at this stage. Follow §7 for the handoff format.

With `on_pass = do not merge`, report the passing revision, validation results, invalidity evidence, missing and partial reviews, and handoff list; then finish with **pass without merge**. If there is no PR, also state the comparison baseline revision and the scope of local changes reviewed. If merge is requested later, recheck the target state and merge conditions then; do not interpret this result as approval to merge.

With `on_pass = merge after user confirmation`, do the following.

1. Request confirmation from the user before merging. Include the target head and base, the **threshold actually applied**, number of rounds completed, validation results, reviewers whose results arrived, reviewers recorded as `no result`, **reviewers recorded as `partial result` and the unreviewed scope**, **every invalid finding and its evidence**, and the handoff list.
2. After confirmation, **check only the pre-merge status**. Verify that head and base still match the approved target, required checks are satisfied, and no new review result has arrived. If the head or base changed, return to review under §3 and §4. Decide any new result using §5 and the confirmed threshold; if it prevents a pass, return to the fix step. Add a new item that does not prevent a pass to the session handoff list and tell the user. Do not merge while required checks are failing or pending.
3. **Merge only the commit matching the approved head.** If the merge is rejected because of a head mismatch, do not merge the new head automatically; return to the previous step. Record the actual merge result and merge commit SHA in the final session report. Do not delete the branch.

Mark inline threads for addressed findings as resolved. Some repositories require no unresolved threads before merge, and leaving them open may cause an addressed finding to be counted again in the next round. **Do not close threads for unaddressed findings merely to tidy them up.**

Write handoff and completion records to repository files **during the next task** under §9. Do not restart review on the current PR with a record-only push. Do not substitute a handoff record for fixing a new defect that prevents a pass or a failed required validation.

**Does not pass and rounds exhausted:** Perform only the fixes and commit, do not merge. Report all of the following and await direction.

- Unresolved findings that prevent a pass under the confirmed threshold and their status (under the default, this includes P0 and P1 findings with `blocking=false`)
- Why the rounds are not converging — whether the same root cause recurs or every fix introduces another defect
- Whether extending the round budget is appropriate and the proposed number of additional rounds

Under the default threshold, the round does not pass while a non-blocking P0 or P1 remains. Reporting it or registering it as follow-up work does not make the round pass. If the user changes the threshold, reevaluate using the new criteria under §2.

## 7. Ledger

Because a session may be handed off while waiting for reviews, preserve the progress state.

**When the review tool already posts results on the PR, those comments are the ledger.** Do not duplicate the same content.

However, a reviewer that overwrites one comment for every head (sticky) removes the results from earlier rounds. Preserve each such reviewer's finding IDs, summaries, and severities in the decision record so later rounds can compare whether they were resolved. This is why §2.1 records in `Publication location` whether content is overwritten.

**Decision-record location.** Regardless of whether a PR exists or which execution mode is used, keep the decision record inside the executor's session and report it to the user after every round (§10). Do not create a temporary ledger in [02-TODO.md](./02-TODO.md), because writing to a tracked file changes the review target. Do not post a PR decision comment. If a handoff to another session is required, pass along the latest §10 report as input and reconstruct the ledger from reviewer results on the PR, if one exists.

- **Read:** Read each reviewer's results aligned by head SHA. Most review tools include a head SHA or round number in the comment. Use it to determine round boundaries and the §4 quorum.
- **Write:** Preserve only the **decision results** separately for each round. Do not duplicate finding bodies already written by reviewers.
- Use the "Decision-record location" above.
- **Lifetime:** Preserve the final report as handoff material for the next task. Update repository documentation during the next task under §9. Do not record `pass without merge` as merged.

The decision record includes the target, confirmed parameters and the history of user-requested changes, current and maximum round counts, each round's head and base, reviewers whose results arrived (including `partial result` and `no result` labels), reviewers requested in each round and the acceptance confirmation when `rereview = request`, and validation results. Summarize findings in the following format.

| ID | Round | head | Reviewer | Severity | confidence | blocking | Decision | Evidence | Handling | commit |
|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | 1 | `abc123` | A, B | P1 | 0.9 | true | Valid | Evidence | Fixed | SHA |

In the `Reviewer` column, list every reviewer that reported the same finding; if their severities differed, preserve each value.

**Session handoff list:** Include the original PR, head, and base (or the comparison baseline and changed scope for a local review), the threshold actually applied, original finding link or ID, severity, `blocking`, decision evidence, remaining work, and completion conditions. Mark every item as `documentation update pending`, and link an existing tracking item when present. At exit, also record whether a merge occurred and the actual merge SHA. Creating a handoff list or merging does not start the next task or complete the repository documentation update.

## 8. Early Stop

Stop and await direction even if rounds remain when:

- Every round produces a new P0 or P1 in the same module that prevents a pass under the confirmed threshold — this signals a design problem rather than an isolated defect
- A fix conflicts with an accepted decision in [00-PROJECT.md](./00-PROJECT.md)
- A fix requires broad refactoring beyond the requested scope
- Required validation commands cannot be run, so the fix cannot be shown to be safe
- A standing reviewer times out in every round — this signals a review-pipeline failure rather than an isolated defect
- The same reviewer produces a `partial result` in every round — this signals that the PR exceeds the reviewer's processing limit. Propose splitting it

## 9. Documentation Update in the Next Task

- **The current round ends with the final session report.** Do not automatically create another branch, PR, or issue for documentation updates, and do not add a post-merge commit or push.
- When the user starts the next related implementation or documentation task, inspect the session handoff list first and incorporate it into that task's documentation changes. In a different session, receive the prior final report as input. If the handoff details are unavailable, restore only items verifiable from sources such as the original GitHub content and state which decision evidence is missing. Do not modify documentation when the user requests only analysis, an ordinary review, or an answer to a question.
- Link remaining items as change units in the `Backlog` of [02-TODO.md](./02-TODO.md). Record the original PR or local baseline revision, finding ID, decision evidence, remaining work, and completion conditions exactly once: in an existing change-specific PLAN when one exists, otherwise in the TODO item. Do not create duplicates of existing items. Add an item to [REVIEW.md](./REVIEW.md) §9 Accepted Deferrals only when it meets that policy's approval requirements. Do not turn one round's threshold change into a permanent deferral.
- Update global TODO completion only after verifying the previous task's actual integration and completion conditions. In a change-specific PLAN, record implementation and validation state on the verified branch; do not interpret it as merged or released. For work without a PR, verify against the agreed local target and the reviewed revision or worktree scope. Do not mark `pass without merge` as integration complete or a handoff item as resolved.
- Update [00-PROJECT.md](./00-PROJECT.md) only when actual decisions, implementation, or supported scope changed. Review documentation updates as part of the next PR or local review unit; do not reopen the previous review's passing state. If there is no follow-up task yet, keep the handoff item as `documentation update pending`.

## 10. Final Report

When the round ends, report the following in English.

- Number of rounds completed and final state (merge / pass without merge / waiting for direction / stopped)
- Threshold actually applied and history of user-requested changes
- For each round: head, reviewers whose results arrived, reviewers marked as `partial result` or `no result`, number of findings, and decisions
- Findings reported differently by reviewers and the combined result
- Invalid findings and a summary of their counterevidence
- Fixes performed and commits
- Validation run and results, plus validation not run and why
- Session handoff list for the next task, pending documentation-update status, and actual merge result
