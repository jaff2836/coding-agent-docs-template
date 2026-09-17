# {{PROJECT_NAME}} Project Instructions

## Project Overview

- **Purpose:** {{PROJECT_DESCRIPTION}}
- **Primary users:** Describe as appropriate for the project
- **Core runtime/framework:** Describe as appropriate for the project
- **Repository structure:** Briefly describe the boundaries between the main applications, packages, and services

Follow the instructions below unless the user's current request conflicts with this document. Do not arbitrarily expand the user's request into all work listed in [`docs/02-TODO.md`](./docs/02-TODO.md).

## Communication

- Write explanations, work reports, and review prose for the user in English.
- Preserve code identifiers, file paths, configuration keys, protocol names, and code quotations in their original form.
- Distinguish verified facts, reasonable inferences, and unverified items.
- If this bundle is used as a fallback for an unsupported language, intentionally change this section and the project-owned documents, and do not claim official locale support or locale-parity verification.

## Commands

- **Install:** Describe as appropriate for the project. Do not automatically install dependencies during analysis or review work.
- **Run:** `{{RUN_COMMAND}}`
- **Build:** `{{BUILD_COMMAND}}`
- **Test:** `{{TEST_COMMAND}}`
- **Lint:** `{{LINT_COMMAND}}`
- **Typecheck:** `{{TYPECHECK_COMMAND}}`
- **Docs:** `python scripts/check-docs.py`
- **Docs test:** `python -m unittest discover -s tests -p 'test_check_docs.py' -v`

Treat commands that still contain a `{{...}}` placeholder as unconfigured and do not attempt to run them. If a command is `N/A` or the execution environment is not ready, do not assume success; report why it could not be verified.

## Document System

### [`docs/00-PROJECT.md`](./docs/00-PROJECT.md) — Context and Decisions

- Records project goals, scope, architecture, constraints, and decision rationale.
- Read the relevant sections for work that requires structural changes, technology stack changes, or important trade-off decisions.
- Update it only when a decision has been agreed with the user or the actual implementation or support scope has changed. Keep the base product design and existing design index together, and do not duplicate detailed work status.
- Keep rejected, deferred, and proposed states distinct from current decisions.

### [`docs/01-DESIGN.md`](./docs/01-DESIGN.md) — Change Design Process

- Read and apply it before implementation for changes involving structure, the technology stack, public contracts, data schemas, migrations, or trade-offs, or for feature changes whose requirements are ambiguous or whose intent must persist across sessions.
- Do not apply it to a bug fix whose cause is not structural, a change contained within one module that does not alter an external contract, or implementation of an already `Accepted` design. Do not expand a small user request into this process.
- Deliverables are a change-specific INTENT and SPEC (or a combined document) proportionate to the work, a PLAN when needed, the PROJECT §8 decision index, and a global TODO item. For implementation of an approved phase, refer to the parent design and supplement only the execution plan. Do not change code before reaching agreement with the user; scope already approved in an earlier conversation may proceed without renewed approval.

### [`docs/02-TODO.md`](./docs/02-TODO.md) — Execution Status

- Manages project-wide changes, milestones, priorities, and dependencies. When a change-specific PLAN exists, that PLAN owns detailed checklists and verification status; the global TODO retains only links and integration-level information. Manage details for a small change without a PLAN in its TODO item.
- Read and update it only when the user's request relates to tracked work.
- Mark an item complete only after verifying the actual implementation and required checks. Completion in a change-specific PLAN means implementation and verification on that branch; global completion also requires confirming integration into the specified target. For local Git work, record the baseline revision and worktree scope; do not invent a PR or merge.
- Do not arbitrarily take on new work that materially expands the scope; propose it to the user.
- Do not modify it when only performing a PR review, analysis, or answering a question.

### Product and Extension Designs and Change Documents

- Use the optional [`docs/10-EXTENSION.md`](./docs/10-EXTENSION.md) or an existing design linked from PROJECT for long-term extensions. State what it preserves, extends, or replaces in the base design.
- Store the intent, specification, and optional execution plan for a change in `docs/changes/<change-ID>/`. `docs/changes/_template/` contains copyable templates and is not approved or active work. Do not require every file for every task.
- In a new session, compare the relevant change documents on the current branch with the integration target. Do not treat the global TODO as real-time status for another branch. Numbers control sorting; they do not indicate approval or priority.
- Keep folders for completed and cancelled changes, and treat PROJECT as the current product baseline. Do not mix global decision and task IDs (`D-`/`T-`) with change-local IDs.

### [`docs/REVIEW.md`](./docs/REVIEW.md) — PR Review Policy

- Read and apply it before reviewing a PR, diff, or commit.
- Do not make modifications during a normal review.
- Update it only when a review policy change has been explicitly requested or agreed.

### [`docs/REVIEW_ROUND.md`](./docs/REVIEW_ROUND.md) — Review Round Process

- Read and apply it only when the user explicitly starts a review round.
- Do not apply it to a normal PR or diff review. In that case, apply only [`docs/REVIEW.md`](./docs/REVIEW.md).
- As an exception, if the handoff list from a previous round is relevant to the current implementation or documentation request, read and apply only the documentation update process in §9. This does not restart the round or delegate commit, push, or merge authority.
- This process performs commits and merges, so apply it together with the delegation provisions in Change Rules below.

### [`docs/PROJECT_ANALYSIS.md`](./docs/PROJECT_ANALYSIS.md) — Whole-Project Analysis Process

- Read and apply it only when the user explicitly requests whole-project analysis, technical due diligence, an architecture assessment, or an adoption decision.
- Do not apply the full process to ordinary implementation, bug fixes, question answering, or PR reviews.

### [`docs/CI.md`](./docs/CI.md) — Quality Gates

- This template does not choose a CI runner product. Follow this document for what to run, in what order, and how to verify the integration.
- Do not create workflow YAML or pipeline files for a specific runner such as GitHub Actions or Buildkite unless the user names that runner.
- Do not report mechanically checked issues (documentation checks, tests, lint, or type checking) as review findings. Run the same command in CI or locally.

## Core Workflow

1. **Confirm scope:** Check the user's request, relevant code, and the current worktree state.
2. **Review context:** Read only the documents and subdirectory instructions directly relevant to the work.
3. **Execute:** Make the smallest coherent change within the requested scope.
4. **Verify:** Run relevant tests, type checks, lint, or builds in proportion to the risk.
5. **Maintain documentation consistency:** Update relevant documents only when an actual decision or completion status changes.
6. **Report:** Concisely report in English what changed, verification results, and remaining limitations.

## Change Rules

- Preserve the user's existing changes in unrelated files.
- Do not commit, push, delete branches, or deploy unless explicitly requested.
- The sole exception to the preceding rule is a review round. When the user starts a round, authority is delegated within that branch and PR scope to commit, make non-force pushes, request re-review when specified as a parameter (using a registered trigger comment or API call), mark addressed finding threads as resolved, and merge after user confirmation. This authority does not extend beyond the parameters established when the round starts or explicitly changed later by the user. Branch deletion, force pushes, and any other PR comments are not delegated.
- Do not add configuration files for a specific CI product such as GitHub Actions or Buildkite unless the user specifies the product. Follow [`docs/CI.md`](./docs/CI.md) for quality gates.
- Before adding a new production dependency, explain the need and alternatives and obtain user agreement.
- Do not record secrets, tokens, or real credentials in code, logs, documentation, or examples.
- For data migrations and public API changes, verify compatibility, deployment order, and rollback impact.
- Do not edit generated files directly when the canonical source or official generation process should be changed instead.
- Do not expand the work into a broad refactor the user did not request.
- Before writing new code, check in this order: can it be avoided → does this codebase already contain it → can the standard library do it → does the platform provide it → can an installed dependency do it. Only then write the minimum necessary code.
- Do not add unrequested abstractions, boilerplate, or configurability. Deletion is better than addition, and straightforward code is better than clever code.
- Fix the cause of a bug, not the symptom. Check all callers of the function being modified and fix the issue once at the shared point.
- Do not minimize input validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything the user explicitly requested. For non-obvious logic, leave one check that fails if the logic breaks.

## Code Review Rules

- Before starting a review, read [`docs/REVIEW.md`](./docs/REVIEW.md) and apply it as the repository's canonical review policy. It takes precedence over conflicting adapters.
- Prioritize correctness, security, data integrity, compatibility, reliability, and performance defects newly introduced or directly worsened by the change.
- Every finding must include severity, `confidence`, `blocking`, the exact file and location, a concrete trigger condition, impact, and remediation direction.
- Do not create findings from unverified speculation, personal style preferences, praise, or formatting and lint issues checked by CI.
- Do not include unrelated pre-existing issues in the normal review scope. However, report verified P0 and P1 issues under [docs/REVIEW.md](./docs/REVIEW.md) §3 Review Scope with `blocking=false`.
- Reviews are read-only by default. Do not modify code or project documentation unless explicitly requested.
