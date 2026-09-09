# CI Quality Gates

This document defines **what to run, in what order, and how to determine success or failure**. The adopting project chooses whether to use GitHub Actions, Buildkite, or another runner. This template does not include product-specific pipeline files, workflow YAML, or plugin lists.

Remote CI is optional. If CI is not used, run the same gates locally and record why CI is not used and what verification replaces it in the integration completion criteria in [02-TODO.md](./02-TODO.md) or in the project README.

## Metadata

- **Status:** Active
- **Owner:** Describe as appropriate for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When the quality gate configuration or local commands change

The canonical command strings are in the root [AGENTS.md](../AGENTS.md) and the adopting project's README. Do not change only one of them. Enforce mechanical rules through these gates, not as review findings. The judgment criteria are in [REVIEW.md](./REVIEW.md) §12.

## 1. Responsibilities

| Does | Does Not |
| --- | --- |
| Runs deterministic and repeatable checks (documentation links, tests, lint, type checking, and builds) | Reaches design agreement or makes review and review-round judgments |
| Records pass or failure for the revision under test | Writes secrets or tokens to logs |
| Runs the commands documented in [AGENTS.md](../AGENTS.md) exactly | Keeps commands only in CI but not in documentation, or reports a CI-only command as a documented success |
| Fails the pipeline with a nonzero exit code when a check fails | Ignores a required gate and treats it as passing |

Reviewer bots, advisors, and skills do not replace CI jobs. Conversely, do not report formatting or lint issues caught by CI as review findings.

## 2. Workflow

Implement the following sequence on the runner chosen by the adopting project. Step names may change, but do not skip the sequence.

1. **Select the target.** Run the pipeline for every change headed to the integration target. This includes a branch push, opening or updating a change request (PR or MR), and the point immediately before merging into the integration branch. Test the **exact revision** of that change.
2. **Checkout.** Check out only that revision. Do not mix in another branch or uncommitted local state.
3. **Runtime.** Prepare the runtime required by the project README and AGENTS.md. Its major version must match the local environment. For documentation gates alone, a standard-library Python installation is sufficient (use `python3` if `python` is unavailable).
4. **Dependencies.** Install dependencies only if a subsequent gate requires them. Keep the installation command identical to Install in AGENTS.md. The “do not install automatically” rule for analysis and review **sessions** is separate from dependency installation on a CI runner.
5. **Run gates.** Follow the §3 table from top to bottom. Skip rows that are `N/A` or whose applicability conditions are not met, and only when the skip rationale has been documented.
6. **Propagate failure.** If a required gate exits with a nonzero code, mark the pipeline failed and block integration. Do not reduce a failure to a warning and pass the pipeline.
7. **Attach results.** Attach logs and pass or failure status to the tested revision. Do not reuse a green result from an earlier commit as evidence that the current head passes.

The project may choose whether a job stops at the first failure or runs all gates and collects the results. In either case, any required gate failure must make the final result a failure.

```text
change arrives → revision checkout → runtime → (if needed) install
  → documentation check → (conditional) documentation checker regression
  → only the documented lint / type checking / test / build gates
  → block integration on any failure; otherwise mark passed
```

## 3. Gate List

| ID | Gate | Canonical Command | Required When | Skip When |
| --- | --- | --- | --- | --- |
| G-docs | Documentation check | `python scripts/check-docs.py` | Repository retains this template's `scripts/check-docs.py` | Script was removed from the adopting repository. If removed, also clean up incoming guidance links |
| G-docs-test | Documentation checker regression | `python -m unittest discover -s tests -p 'test_check_docs.py' -v` | Change modifies `scripts/check-docs.py` or `tests/test_check_docs.py`. Always required in the original template repository | Routine change in an adopting repository that does not modify the checker. If the test file was removed, keep only G-docs |
| G-lint | Lint | Lint from AGENTS.md / README | Command is not `N/A` and has been verified | Unconfigured placeholder, `N/A`, or recorded as unverified |
| G-type | Type check | Typecheck from AGENTS.md / README | Same as above | Same as above |
| G-test | Project tests | Test from AGENTS.md / README | Same as above | Same as above |
| G-build | Build | Build from AGENTS.md / README | An artifact exists and the command is not `N/A` | Same as above |
| G-adopt | Placeholder search | `rg`/`grep` from [TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) §3 | Once immediately after applying the template | Original template repository; every pipeline after values have already been filled in. If TEMPLATE_GUIDE was removed, use the search command copied at adoption time or the [DOCS_GUIDE.md](./DOCS_GUIDE.md) checklist |

G-docs does not treat placeholders remaining in the original template as a failure. Check placeholders in an adopting repository with G-adopt and the [DOCS_GUIDE.md](./DOCS_GUIDE.md) checklist.

When adding a project gate, add a row to this table and use the exact same command string as in AGENTS.md and README. Do not keep a check only in this table with no corresponding documented command.

## 4. Integration Checklist

Use this checklist when selecting a new runner or attaching this template to an existing pipeline. The product name need not be recorded. Add the gates to an existing pipeline when one exists; otherwise, create a pipeline only for a product the user has specified.

### Triggers and Revisions

- [ ] The pipeline starts for every change headed to the integration target.
- [ ] The checked-out commit matches the revision under test.
- [ ] A result from another commit is not reused as the current head's pass status.

### Commands and Documentation

- [ ] Every gate's command string matches AGENTS.md and README.
- [ ] A command with a remaining placeholder is not run; an `N/A` command is skipped in this table with its rationale.
- [ ] If G-docs is retained, documentation and the pipeline use the same available command, either `python` or `python3`.
- [ ] When dependency installation is required, the Install command appears only before the gates.

### Failure and Permissions

- [ ] A nonzero exit code from a required gate fails the pipeline. No option that ignores failures is used on a required gate.
- [ ] Failure logs are accessible from the relevant change request or commit.
- [ ] Secrets and tokens do not remain in logs, artifacts, or caches.
- [ ] Runner credentials have only the minimum permissions required for the checks. Quality gate jobs do not have deployment or release authority.

### Original Template and Adopting Repository

- [ ] **Original template repository:** Always run G-docs and G-docs-test. Do not add G-adopt (placeholder search).
- [ ] **Adopting repository:** Retain G-docs. Run G-lint, G-type, G-test, and G-build only for configured commands. Run G-adopt once immediately after adoption.
- [ ] If CI is not used, record local execution of the same gates and the reason CI is not used.
- [ ] Do not create `.github/workflows/`, a Buildkite pipeline file, or another product-specific configuration before the user specifies a runner product.

## 5. Local Consistency

When agent and human commands run locally differ from CI, the result is “works locally, fails only in CI.”

- A gate reported as successful locally must be runnable with the same command in CI.
- If a check passes only in CI and is absent from local documentation, add the command to AGENTS.md and README or remove it from CI.
- After changing `scripts/check-docs.py`, run G-docs-test locally before reporting completion.

## 6. Not Provided

- GitHub Actions workflow files, Buildkite pipeline files, or configuration for another runner
- Automated review jobs, review prompts, or bot token configuration
- Deployment, release, or tag jobs. Do not mix quality gate and deployment permissions in one job
- A duplicate reimplementation of `scripts/check-docs.py` in another language
