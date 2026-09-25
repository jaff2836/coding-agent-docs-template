# Template Guide

This document explains how to adopt the documentation-centered project template for the first time. In this locale artifact, the root [README.md](../README.md) is the adopting project's overview, setup, and run template. It does not include the template source repository's introductory README.

The template does not include an initialization script, review prompts or automatic review configuration for GitHub Actions, or pipeline files for a particular CI product. Copy the files and fill in the project values yourself. Follow [CI.md](./CI.md) for quality-gate order and integration checks.

## Metadata

- **Status:** Active
- **Template version:** 2.3.2
- **Template source:** Adapt to the project — URL of the original template repository, or another location you can open again later
- **Template revision:** Adapt to the project — full SHA of the source commit used for copying (§5)
- **Owner:** Adapt to the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When the template structure or tool integration changes

`Template version` records the release used for copying; `Template source` and `Template revision` record its original location and exact commit. Do not change these values for ordinary documentation edits in the adopted repository. Fill in the source and revision guidance from the original template when copying; do not try to place the adopted repository's own future commit SHA here. Recording rules are in §5, and release-specific changes are in §6.

## 1. Included Layout

```text
.
├── README.md                  # Project README template in the selected locale
├── AGENTS.md                  # Shared project instructions for AI development tools
├── CLAUDE.md                  # Reference to @AGENTS.md
├── LICENSE                    # MIT license for the template itself; replace with project license
├── .gitignore
├── scripts/
│   └── check-docs.py          # Dependency-free docs checks: links, skill policy, imports, version
├── tests/
│   └── test_check_docs.py     # Regression tests for documentation-check failure paths
├── .agents/
│   └── skills/
│       ├── design/
│       │   └── SKILL.md       # Entry point for change design: Codex, Cursor, OMP
│       ├── project-analysis/
│       │   └── SKILL.md       # Whole-project analysis process: Codex, Cursor, OMP
│       └── review-round/
│           ├── SKILL.md       # Entry point for review rounds: Codex, Cursor, OMP
│           └── agents/openai.yaml  # Explicit-invocation-only configuration for Codex
├── .claude/
│   └── skills/
│       ├── design/
│       │   └── SKILL.md       # Entry point for change design: Claude Code
│       ├── project-analysis/
│       │   └── SKILL.md       # Whole-project analysis process: Claude Code
│       └── review-round/
│           └── SKILL.md       # Entry point for review rounds: Claude Code
├── .cursor/
│   └── BUGBOT.md              # Optional: copy of the review decision criteria
├── .omp/
│   └── WATCHDOG.md            # Optional: OMP advisor review priorities; imports REVIEW.md
└── docs/
    ├── CHANGELOG_GUIDE.md     # Boundaries for optional project release notes
    ├── DOCS_GUIDE.md          # Document index, operating rules, and adoption checklist
    ├── TEMPLATE_GUIDE.md      # This document: first-time adoption instructions
    ├── 00-PROJECT.md          # Product baseline, base design, decisions, and design index
    ├── 01-DESIGN.md           # Shared design process
    ├── 02-TODO.md             # Global changes, priorities, dependencies, and integration results
    ├── 10-EXTENSION.md        # Optional extension design and phased completion criteria
    ├── changes/
    │   └── _template/        # Copyable templates; actual work uses a separate change-ID directory
    │       ├── 01-CHANGE.md   # Combined form: Intent and Spec in one file
    │       ├── 01-INTENT.md   # Request, problem, and expected outcome
    │       ├── 02-SPEC.md     # Requirements, scenarios, and design
    │       └── 03-PLAN.md     # Optional detailed work and verification record
    ├── REVIEW.md              # Shared PR review policy
    ├── REVIEW_ROUND.md        # Review-round process and delegated authority
    └── CI.md                  # Runner-agnostic quality-gate workflow and integration checklist
```

## 2. Applying to a Project

For an official release, use `installer.py` from GitHub Releases. Use the latest installer with the latest version, or a versioned tag's installer with that same exact version. The installer follows only an HTTPS redirect chain initiated by a GitHub release asset URL, then verifies the checksums and manifest from the exact tag.

On Windows, the installer from this template source revision requires Python 3.12 or newer to check directory junctions. Previously published releases retain their own Python support range.

```sh
(
  set -e
  curl --fail --location --proto '=https' --proto-redir '=https' \
    --output installer.py.part \
    https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py
  mv installer.py.part installer.py
  python3 installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version {{VERSION}}
)
```

Use `latest` or a full SemVer value for `{{VERSION}}`.

For an existing repository, use `adopt`. It verifies the release the same way as `install`, never writes to the target repository, and creates only the verified artifact (`artifact/`) and a per-path plan (`adoption-plan.json`) in an empty directory outside the target.

```sh
python3 installer.py adopt --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version {{VERSION}} --locale {{LOCALE}} --repo-root {{EXISTING_REPOSITORY}} --output {{EMPTY_OUTPUT_DIR}}
```

`adopt` does not apply any file. A person or coding agent merges according to each report status and then completes steps 1-13 below.

| Status | Meaning | Action |
|---|---|---|
| `missing` | Not present in the target | Add the file from `artifact/` and fill in the project values. |
| `identical` | Already matches the artifact | No action. |
| `merge` | The target file differs | For policy `merge` (project-owned), keep the existing content and merge in the template sections. For `copy` (template-owned), start from the artifact version and reapply only intentional project edits. |
| `decision` | The project decides whether to adopt it | Decide whether to add, keep, or remove `LICENSE` under the license rule in §3, `docs/10-EXTENSION.md` under step 5, and `.cursor/BUGBOT.md` and `.omp/WATCHDOG.md` under step 8. |
| `blocked` | A symlink, Windows directory junction, non-regular entry, case-only name variant, or similar | Clean up the target path by hand, then run `adopt` again. |

`adoption-plan.json` uses the `stability: experimental` format; its fields may change in a minor release. To cancel an adoption, delete the output directory.

To upgrade a repository that was previously derived from an exact release, pass that older full SemVer as the base. Do not use `latest` for the base, and omit `--base-version` for a first adoption.

```sh
python3 installer.py adopt --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version {{VERSION}} --base-version {{OLDER_EXACT_VERSION}} --locale {{LOCALE}} --repo-root {{EXISTING_REPOSITORY}} --output {{EMPTY_OUTPUT_DIR}}
```

Base mode validates the historical release without importing or running its installer. It assumes the target was derived from that exact base; file bytes alone cannot distinguish a project deletion from a file that was never applied.

| Upgrade status | Meaning |
|---|---|
| `unchanged` | The base, current artifact, and target agree. |
| `template-only` | The template changed while the target still matches the base, including template additions and removals. |
| `project-only` | Only the target differs from the unchanged template path. |
| `converged` | The target already matches the changed current artifact. |
| `diverged` | The template and target changed to different results. |
| `blocked` | The target path cannot be compared safely and needs manual cleanup. |

In format 2, `summary` still counts only current artifact paths, while `upgrade_summary` counts the `base ∪ current` union. A path removed from the current release appears only in the upgrade list with null `policy`, `status`, and `artifact_sha256`; review it by hand rather than treating it as an automatic deletion. The staged `artifact/` contains only the current release, and no classification authorizes an automatic merge, overwrite, or removal.

For a new project, use `install` with a new path or an empty directory. If the target contains any file or directory, including paths unrelated to the artifact, it writes nothing and stops with guidance to use `adopt` for an existing repository.

```sh
python3 installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version {{VERSION}} --locale {{LOCALE}} --repo-root {{EMPTY_OR_NEW_TARGET}}
```

To obtain only the verified artifact without a plan, export it to an empty directory.

```sh
python3 installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version {{VERSION}} --locale {{LOCALE}} --output {{EMPTY_OUTPUT_DIR}}
```

1. In a new project created with `install`, or in a repository merged according to the `adopt` report, record its version and source commit in both guide documents as described in §5. Confirm that the artifact inventory includes the hidden `.agents/`, `.claude/`, `.cursor/`, and `.omp/` entries, `.gitignore`, and all four templates under `docs/changes/_template/`. Do not copy the source repository root directly.
2. The root [README.md](../README.md) is already the project template in the selected locale. Fill in the project name, description, requirements, installation, execution and verification instructions, security guidance, and license.
   Decide separately whether the project needs a root `CHANGELOG.md`. Preserve an existing format and follow [CHANGELOG_GUIDE.md](./CHANGELOG_GUIDE.md); the template does not create or overwrite that file.
3. Adapt the project information and commands in [AGENTS.md](../AGENTS.md) to the actual repository. Confirm that they agree with the README's execution instructions.
4. Replace the placeholders and example items listed below. When deleting the example invariant in [REVIEW.md](./REVIEW.md) or turning it into a real rule, also delete the `template-example:project-invariant` marker immediately above it.
5. In [00-PROJECT.md](./00-PROJECT.md), distinguish the current product baseline from approved goals and link the sources of truth for existing designs. In [02-TODO.md](./02-TODO.md), record the integration target and change-level work items for the first milestone. If a change has a PLAN, keep its detailed work and verification status only in that PLAN. If there is no long-term extension, remove `10-EXTENSION.md` and incoming links to it.
6. Record only project-specific invariants and actually approved exceptions in [REVIEW.md](./REVIEW.md).
7. Check the default round count and pass threshold in [REVIEW_ROUND.md](./REVIEW_ROUND.md), and list every reviewer that runs in this repository in §2.1. The user may change the threshold; use the confirmed values in an actual round. Follow §6, §7, and §9 for handoff and documentation updates after a pass. Use the "Reviewer Research Hints" below as a starting point, but verify actual behavior directly.
8. If you use Cursor Bugbot, fill the invariants and settled-decisions sections of [.cursor/BUGBOT.md](../.cursor/BUGBOT.md) with the same content as [REVIEW.md](./REVIEW.md) and [00-PROJECT.md](./00-PROJECT.md). If you use an OMP advisor, verify that the import in [.omp/WATCHDOG.md](../.omp/WATCHDOG.md) works. Delete these files when their respective tools are not used.
9. [01-DESIGN.md](./01-DESIGN.md) is a shared process document. Adapt its Metadata to the project, but do not put product design content there. Create only the artifacts required by §1 and §2, and do not treat `_template/` as active work. Do not rewrite INTENT or SPEC to implement an already approved phase.
10. Verify that each development tool you use reads the shared instructions and related documents as intended.
11. If you use an external methodology or behavioral-rules tool, first apply the coexistence rules in §4, "External Methodology and Behavioral-Rules Tools."
12. Use the Template Adoption Checklist in the [Documentation Guide](./DOCS_GUIDE.md) to confirm adoption is complete.
13. Repositories that use CI should connect the quality gates to their existing runner using the workflow and checklist in [CI.md](./CI.md). This template does not include product-specific pipeline files for GitHub Actions, Buildkite, or another runner. Do not create YAML until the user selects a runner. If the repository has no CI, run the same gates locally and record why CI is not used.

For an existing project, do not run `install` directly into its tree. Compare the `adopt` report and `artifact/` above with the existing instructions, documents, and ignore rules, then merge them manually. The installer stops the entire installation when the target is not empty, even if its existing paths do not overlap the artifact, and does not provide `--force`, automatic updates, or automatic locale switching. Preserve existing code, project-specific values, and user changes; record included and excluded files next to the Template revision. If something goes wrong, return to the pre-change branch or backup.

The official locales are `en` and `ko`. For another language, use the English artifact as a starting point and intentionally change the Communication policy in [AGENTS.md](../AGENTS.md) and the project-owned documents. Do not present this manual adaptation as an officially supported locale or as having passed locale-parity verification.

If merging an existing `REVIEW.md` changes section numbers, or if you remove optional sections from [00-PROJECT.md](./00-PROJECT.md), update section-number references in [REVIEW_ROUND.md](./REVIEW_ROUND.md), [01-DESIGN.md](./01-DESIGN.md), [.cursor/BUGBOT.md](../.cursor/BUGBOT.md), and [.omp/WATCHDOG.md](../.omp/WATCHDOG.md) to match the actual headings. Repositories that already have a large design document should read [01-DESIGN.md](./01-DESIGN.md) §6 first. Preserve existing documents by default; merge them only when the user requests it, preserving their evidence and references.

### Migrating to the Numbered System

| Previous File | New Default File | Migration Scope |
|---|---|---|
| `docs/PLAN.md` | `docs/00-PROJECT.md` | Product context, current architecture, base design, decisions, and source-of-truth links |
| `docs/DESIGN.md` | `docs/01-DESIGN.md` | Shared process; separate from actual design artifacts |
| `docs/TODO.md` | `docs/02-TODO.md` | Global change list; convert details into a link when a PLAN exists |
| Existing product or extension designs | Keep existing paths by default | Link them from the PROJECT index; do not rewrite or move without agreement |
| Existing change designs | Preserve existing approval records | Use the Intent, Spec, and optional Plan format for new changes |

- Numbers, uppercase names, and hyphens help sorting and role identification. Numbers alone do not determine design priority or approval, and existing decision IDs are not renumbered.
- Do not globally replace old filenames. A change-specific `03-PLAN.md`, tool-generated files, and historical `PLAN.md` records have different roles. Search links, imports, skills, checker code, and fixed policy paths, then change only the actual migration targets.
- Keep entry-point and contract paths such as `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, and `docs/REVIEW.md`. Renaming them requires a separate consumer-compatibility and tool-configuration review.
- When integrating existing product designs, keep execution status in TODO or PLAN and completed history in the existing CHANGELOG. Preserve contracts, decision rationale, and approval evidence. In extension designs, state which parts of the parent document are preserved, extended, or replaced.
- Preserve any historical rule that freezes the body of past change files. For the new format, apply the approved-version preservation and update rules in 01-DESIGN.md §4. Preserve previously approved content even in an uncommitted state.
- Do not determine scope from the number of PRs alone. Split local Git work into reviewable change units and record either the integration target or the local completion target in the global TODO. A remote service or automatic commit is not required.
- Confirm that active work does not point to the templates directory as its source of truth. Use only the templates needed for small work and implementations of parent designs.

### Reviewer Research Hints

The §2.1 table differs by repository, so the template does not fill it in. However, behavior for widely used public GitHub reviewers is defined at the product level. The following was observed as a starting point for investigation (as of 2026-09; verify directly with the version you use).

| Reviewer | Observed Characteristics | Rereview Request Method (Official Documentation) |
|---|---|---|
| Codex (`chatgpt-codex-connector`) | Identifies the head through `Reviewed commit:` in the PR review body. Automatic review runs once when the PR is opened in review-requested state, not on every push. It leaves a review body even with no findings. Because inline findings cite `AGENTS.md` line numbers, the Code Review Rules in `AGENTS.md` affect output format | Put exactly `@codex review` in the PR comment body. Acceptance is indicated by an 👀 reaction on the comment. **Do not append anything after `review`** — if another sentence follows `@codex`, Codex may start a cloud task with the PR as context rather than a review, and that task can push to the branch |
| Copilot (`copilot-pull-request-reviewer`) | **Once per PR**, with no head identifier. Low-confidence comments also appear in the collapsed `<details>` section named "Suppressed comments" in the review body | Move the "Copilot Rereview Command" below into §2.1 and run it. Per-push automation exists only through the repository ruleset option "Review new pushes" |
| Self-hosted GitHub App reviewer (for example, a webhook bot) | Commonly handles the `pull_request` actions opened, reopened, ready_for_review, and synchronize, runs on every push, and records the head in a PR comment marker such as `<!-- <name>:v1 head:<SHA> -->`. Whether it creates one comment per head or overwrites one depends on the bot; record that in the table's `Publication location` column | `automatic on push` — record the trigger event as well. Verify whether it leaves a result when there are no findings; this changes the timeout handling in §4 |

**Copilot Rereview Command** (`<n>` is the PR number. For `rereview = request`, the §2.1 table must contain this command or a reference to this block. Bot ID `BOT_kgDOCnlnWA` is current as of 2026-09; verify it again with `gh api users/copilot-pull-request-reviewer%5Bbot%5D --jq .node_id`. Only this REST URL uses `[bot]`):

```bash
gh api graphql \
  -f query='mutation($pr:ID!,$bot:ID!){ requestReviews(input:{pullRequestId:$pr, botIds:[$bot], union:true}) { pullRequest { reviewRequests(first:10) { nodes { requestedReviewer { ... on Bot { login } } } } } } }' \
  -f pr="$(gh pr view <n> --json id --jq .id)" \
  -f bot="BOT_kgDOCnlnWA"
```

Confirm acceptance by checking that GraphQL `Bot.login` in the response's `reviewRequests` is `copilot-pull-request-reviewer` (without `[bot]`). Do not use REST `requested_reviewers`, which can be a no-op even with a 200 response. Once review begins, the reviewer leaves the request list, so a later `gh pr view` may show an empty list.

Self-hosted bots and GitHub Actions-based reviewers differ by repository and version. Verify their marker comments and trigger conditions directly. The first two public reviewers do not run on every push in their default configuration, so a repository with only those reviewers cannot obtain a standing-reviewer result from the second round onward unless `rereview = request`.

## 3. Values to Replace

Replacement targets are not limited to the `{{...}}` form. Instructional placeholders also remain, so find them together with this command.

```bash
rg --hidden -n --glob '*.md' --glob '!**/.git/**' --glob '!docs/TEMPLATE_GUIDE.md' --glob '!docs/DOCS_GUIDE.md' \
  "\{\{|Adapt to the project|Describe as appropriate for the project|Customize for the project|Briefly describe|YYYY-MM-DD|\| Example|Example decision|Example completion|\*\*Example:\*\*|template-example:project-invariant" .
```

If `rg` is unavailable, use:

```bash
grep -rnE "\{\{|Adapt to the project|Describe as appropriate for the project|Customize for the project|Briefly describe|YYYY-MM-DD|\| Example|Example decision|Example completion|\*\*Example:\*\*|template-example:project-invariant" \
  --include='*.md' --exclude=TEMPLATE_GUIDE.md --exclude=DOCS_GUIDE.md \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv .
```

Run this check against the **adopted repository after filling in project values**. The source template intentionally retains placeholders and examples. Use `--hidden` to search hidden directories such as `.cursor/BUGBOT.md`, while excluding `.git` internals.

The two guide documents are excluded from the search because they contain these phrases to explain the placeholders. Inspect their Metadata directly instead. Placeholders in `changes/_template/` may remain for copying, but replace them in actual change directories. Even a zero-result search does not verify README guidance outside this pattern, owner, milestone, or task examples, command executability, or evidence for completion claims. Check the Template Adoption Checklist in [DOCS_GUIDE.md](./DOCS_GUIDE.md) too.

After adoption or document moves, run `scripts/check-docs.py`. It checks relative links, `.agents`/`.claude` skill copies and the Codex explicit-invocation policy value, `@` imports in `CLAUDE.md` and `.omp/WATCHDOG.md`, the invariant lists in [REVIEW.md](./REVIEW.md) §6 and [.cursor/BUGBOT.md](../.cursor/BUGBOT.md), section-number references that identify a document, and `Template version` in the guide documents. A failure produces a nonzero exit code. It uses only the standard library.

```bash
python scripts/check-docs.py
```

When changing the checker in the source template, also run its failure-path regression tests.

```bash
python -m unittest discover -s tests -p 'test_check_docs.py' -v
```

Use `python3` if `python` is unavailable. Moving a file can break links even without changing its content. The checker continues to work if this document is removed as described in §5; in that case, it checks the version record only in [DOCS_GUIDE.md](./DOCS_GUIDE.md). The section-number check only considers references that identify a document (`REVIEW.md §6`, `PROJECT §8`, and similar). It excludes ambiguous same-file references such as `§4` and old section numbers in the §6 release history. It skips generated directories such as `dist`, `build`, `target`, and `vendor`. The checker does not fail because placeholders remain in the source template; use the `rg` or `grep` command above for that.

The checker does not implement all of CommonMark; it interprets only the following scope. Section numbers are read only from ATX headings (`## 2. Title`). An inline link must keep its link text on one line, and at most one line break is allowed before its destination and before its title. A reference definition keeps its label, destination, and optional title on one line. Text inside fenced or indented code blocks, inline code spans, HTML comments, and HTML blocks that start with `<pre>`, `<script>`, `<style>`, `<textarea>`, or a block-level HTML tag is not treated as a link or section reference. URLs with a scheme and paths that start with `/` are not checked as file links. Setext headings, link text or reference definitions that span lines, and other HTML block forms are not interpreted, so use the forms above in checked documents.

| Placeholder | Content to Provide |
|---|---|
| `{{PROJECT_NAME}}` | Project name |
| `{{PROJECT_DESCRIPTION}}` | Problem solved and core functionality |
| `{{CHANGE_ID}}`, `{{CHANGE_TITLE}}` | Unique ID and title for an actual change directory. Keep them as copyable placeholders in `_template/` |
| `{{RUN_COMMAND}}` | Development or execution command |
| `{{BUILD_COMMAND}}` | Build command |
| `{{TEST_COMMAND}}` | Test command |
| `{{LINT_COMMAND}}` | Lint command |
| `{{TYPECHECK_COMMAND}}` | Type-check command |
| `{{PROJECT_INVARIANT_1}}`, `{{PROJECT_INVARIANT_2}}` | Project-specific rules that must hold. Use the same content in both [REVIEW.md](./REVIEW.md) §6 and [.cursor/BUGBOT.md](../.cursor/BUGBOT.md) |

- Mark unused commands `N/A` and record the reason in [AGENTS.md](../AGENTS.md). Do not leave nonexistent commands looking like runnable examples.
- Replace `Adapt to the project`, `Describe as appropriate for the project`, `Customize for the project`, `YYYY-MM-DD`, and owner, milestone, and task examples with actual information.
- Examples in the global TODO and change templates are not actual completion history. Record the integration target and required verification for global completion; in a PLAN, record implementation and verification evidence from that branch.
- Keep unresolved items in [00-PROJECT.md](./00-PROJECT.md) unresolved; do not turn proposals into agreed decisions. Delete the example decision row (`D-001`) or replace it with a real decision. Sections §1–§5, §8, and §11 are required; the others may be deleted when not applicable. Clean up incoming section references at the same time. Do not leave empty sections containing placeholders.
- Delete the example invariant in [REVIEW.md](./REVIEW.md) together with the `template-example:project-invariant` marker immediately above it. Do not automatically adopt commented-out exceptions as project policy.
- Write `Last reviewed` using the **UTC date** on which the content was actually reviewed. Copying the template alone does not establish completed verification. A local-time date can appear later than a PR timestamp shown by GitHub and prompt reviewer findings.
- Do not invent an undecided license, security-reporting channel, or operational information. The bundled `LICENSE` is the MIT license for the template itself. Replace it once the project license is decided; if it is undecided, delete the file and mark the README License section as undecided.

### Caution with `@` Tokens

Claude Code treats tokens beginning with `@` in `CLAUDE.md` and its imported files as file imports. Wrap email addresses and `@handle` values in backticks when placing them in `Owner` fields or contact information. An `@` inside a code span or code block is not imported.

## 4. Development Tool Integration Files

The source of truth for shared rules is [AGENTS.md](../AGENTS.md). This layout avoids maintaining a separate copy of the same rules for each tool.

### Instruction Files

- Keep only `@AGENTS.md` in [CLAUDE.md](../CLAUDE.md). This template does not require a symbolic link. On Windows, symbolic links may require administrator privileges or Developer Mode, so the import form is safer.
- Codex and Cursor read the root `AGENTS.md` directly. Claude Code reads only `CLAUDE.md`, so it needs the import above.
- In a repository that **uses OMP**, do not create `.claude/CLAUDE.md`, `.agents/AGENTS.md`, or `.github/copilot-instructions.md`. At the same directory depth, OMP masks lower-priority providers with higher-priority providers, and the root `AGENTS.md` has the lowest priority. If any of these files exists, OMP may not load the root `AGENTS.md`. (Source: provider priority table in OMP `docs/context-files.md`; verify directly with the version you use.)
- In a repository that **does not use OMP**, you may keep tool-specific instruction files required by that tool. Keep shared rules in the root `AGENTS.md`. In a tool-specific file, include only the connection needed when the tool cannot read the root file (an import or one-line reference); do not duplicate the body. Before adopting OMP later, check whether these files mask the root `AGENTS.md`.
- This template does not include `.cursorrules` or `.omp/AGENTS.md`. If an existing project has tool-specific instructions, check for duplication or conflict with the shared rules.
- If the repository uses CODEOWNERS, add `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.cursor/`, `.omp/`, `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `docs/01-DESIGN.md`, and `docs/CI.md` to owner rules. These files determine agent commit and merge authority and review decisions, so protect them at the same level as source code. This template does not itself include a CODEOWNERS file.

### Review-related Files

- [.cursor/BUGBOT.md](../.cursor/BUGBOT.md) is specific to Cursor Bugbot. Bugbot reads neither `.cursor/rules/` nor linked documents; it uses only this file for project rules. The review criteria from [REVIEW.md](./REVIEW.md) are therefore intentionally duplicated here. To produce the same blocking decision as the canonical policy, duplicate not only the decision criteria but also **the §6 invariants, §9 Accepted Deferrals, and settled decisions that must not be reverted**. Update both files whenever the review policy changes.
- [.omp/WATCHDOG.md](../.omp/WATCHDOG.md) is specific to the OMP advisor, a second model that monitors the primary agent. OMP appends this file only to the advisor's system prompt, not to the primary agent context, and does not treat it as a context file like `AGENTS.md`. Unlike Bugbot, it expands `@path` imports, so it imports [REVIEW.md](./REVIEW.md) through `@../docs/REVIEW.md` instead of duplicating it. OMP discovers `<dir>/WATCHDOG.md` or `<dir>/.omp/WATCHDOG.md`; this template uses the latter to keep the root uncluttered. Do not place `AGENTS.md` in `.omp/` (see "Instruction Files" above). The companion `WATCHDOG.yml` (advisor list, models, and tools) is a project-specific choice involving models and cost, so the template does not include it. (Source: OMP `docs/advisor-watchdog.md`; verify `..` resolution in import paths with the version you use.)
- Skills (`design`, `project-analysis`, `review-round`) contain the same content at two paths. Codex, Cursor, and OMP read `.agents/skills/`; Claude Code reads `.claude/skills/`. `design` and `review-round` are adapters to canonical procedures in `docs/`, while `project-analysis` contains the full analysis process so it can load independently. Cursor loads both paths, so slash commands may appear twice. Their identical content means there is no behavioral difference. If a repository does not use Claude Code, it may omit the `.claude/skills/` copy.
- `review-round` is explicit-invocation-only. Claude Code, Cursor, and OMP use `disable-model-invocation: true`; Codex uses the separate configuration below. Because `design` is read-only until agreement, its automatic invocation is not blocked. `project-analysis` is also not blocked from automatic selection, but its description and body require an explicit whole-project analysis request. A model may select a process for a matching request, while [01-DESIGN.md](./01-DESIGN.md) §1 determines design applicability.
- The automatic-invocation blocking key is `disable-model-invocation` for both Cursor and Claude Code, and OMP recognizes the same spelling. For Codex, [.agents/skills/review-round/agents/openai.yaml](../.agents/skills/review-round/agents/openai.yaml) blocks implicit invocation with `policy.allow_implicit_invocation: false` while allowing explicit `$review-round` invocation ([official documentation](https://learn.chatgpt.com/docs/build-skills)). This configuration is Codex-specific, so do not copy it into `.claude/skills/`. Keep the two `SKILL.md` files identical and retain the explicit-invocation requirement in their bodies. `argument-hint` is a Claude Code-specific field and other tools ignore it.
- Codex's GitHub review cites `AGENTS.md` line numbers in inline findings and follows that file's format for `confidence` and `blocking`. The Code Review Rules in `AGENTS.md` therefore affect the GitHub reviewer's output, not only the local agent. Do not replace the body with a link alone. It is not verified whether Codex follows the linked `docs/REVIEW.md`.

### External Methodology and Behavioral-Rules Tools

Keep short rules that always apply in the root `AGENTS.md`. A conditional process is owned either by a thin skill that points to a canonical document in `docs/`, or by one self-contained skill such as `project-analysis` when no separate document is canonical. Do not duplicate the same process across both a document and a skill when using external methodology or behavioral-rules tools.

- This template owns `AGENTS.md` and `CLAUDE.md`. If external initialization or update rewrites either file, disable that feature or reconsider adoption. Follow "Instruction Files" above for additional instruction files.
- A tool artifact may replace the role of INTENT, SPEC, or PLAN. Keep the decision index in PROJECT and the change-level plan in TODO, and keep each contract or detailed status in only one source of truth.
- If a tool creates its own instruction directory or managed block, check it for conflicts with `AGENTS.md`. Its runtime and updates are not tracked by `Template version`, so review any diff that rewrites instruction files.

### Shared Guidance

- Verify instruction-loading behavior directly with the tool version and local configuration you use. Do not assume that Markdown links automatically load every linked document.
- [`project-analysis`](../.agents/skills/project-analysis/SKILL.md) is a self-contained skill loaded only when whole-project analysis is explicitly requested. Do not automatically import its full process into shared instructions.
- [01-DESIGN.md](./01-DESIGN.md) is also a process document. Put only its applicability conditions and artifact locations in `AGENTS.md`; do not import the process itself. Loading design procedure into every task encourages models to inflate small requests into process work.

## 5. Post-adoption Maintenance

- Use the [Documentation Guide](./DOCS_GUIDE.md) as the source of truth for ordinary documentation maintenance and per-document edit authority.
- [DOCS_GUIDE.md](./DOCS_GUIDE.md) is intentionally not named `README.md`. Naming it `docs/README.md` would conflict with the common practice of putting a root README translation at a path such as `docs/README.ko.md`. Do not rename it back to `docs/README.md`.
- Use relative paths from the containing file for all repository-internal Markdown links. When moving or renaming a file, update incoming links too.
- You may retain this document as the template-adoption record. If you delete it after adoption, also remove links to it from the adopted project's [README.md](../README.md) and [Documentation Guide](./DOCS_GUIDE.md).
- If you remove [.cursor/BUGBOT.md](../.cursor/BUGBOT.md) because Cursor Bugbot is unused, or [.omp/WATCHDOG.md](../.omp/WATCHDOG.md) because OMP is unused, also clean up their links and layout descriptions in this guide and [DOCS_GUIDE.md](./DOCS_GUIDE.md).

### Recording the Copy Baseline with Git

Before copying, run the following in the **original template checkout**. The adopted project's HEAD is not the source revision.

```bash
git rev-parse HEAD
git describe --tags --always --dirty
git status --short --untracked-files=all
```

- In `Template source`, record a repository URL or storage location from which the original can be opened again. In `Template revision`, record the **full commit SHA** from the first command.
- If the source exactly matches a release tag, record the version number in `Template version` (for example, tag `v1.2` → `1.2`). Resolve the tag with `git rev-parse 'v1.2^{commit}'` and compare it with the source SHA. Classify a commit after the tag as `Unreleased (latest tag: v1.2)`, or a repository with no tag as `Unreleased (no tag)`, and retain the exact SHA.
- `git describe` is supporting evidence that shows the number of commits after a tag and an abbreviated SHA; it does not replace the full SHA. Even without `-dirty`, new files may be absent, so inspect untracked files in `git status`. If copying uncommitted changes, mark `Template revision` as `Unconfirmed (baseline commit: <full SHA>, includes uncommitted changes)` and record the included changes. Do not claim the entire copy is reproducible from one SHA. Also retain `Unconfirmed` when the source history is unavailable. ([Git describe](https://git-scm.com/docs/git-describe), [Git status](https://git-scm.com/docs/git-status))
- If both guide documents remain, keep their source, version, and revision values identical. If you delete this document, retain the record and any partial-adoption details in [DOCS_GUIDE.md](./DOCS_GUIDE.md). These values identify the source document; they do not demonstrate tool compatibility. Record tool version, verification date, and result separately when instruction loading has been checked.
- At release time, the template maintainer tags the commit that updates the version and revision history with `v<version>`. Do not move a published tag; record later changes in a new commit and subsequent version. Reading this procedure or copying the template does not delegate commit, tag creation, or push authority.

### Template Behavior Verification Cases

When changing instructions, skills, or the checker, confirm that these cases still behave as described. `scripts/check-docs.py` does not replace this verification. If a case fails, correct the relevant sentence or skill description.

| Case | Expected Behavior | Failure | Basis |
|---|---|---|---|
| Small bug fix | Make the fix without design files | Require INTENT and SPEC | [01-DESIGN.md](./01-DESIGN.md) §1 |
| Implementing an approved design | Link the parent section and create only a PLAN if needed; no reapproval | Require the full design process or reapproval | [01-DESIGN.md](./01-DESIGN.md) §1 and §3.6 |
| Completing PLAN checkboxes | Report only implementation and verification complete on that branch | Report integration, release, or support verification complete | [DOCS_GUIDE.md](./DOCS_GUIDE.md), [01-DESIGN.md](./01-DESIGN.md) §4 |
| Tool-specific instructions in a repository without OMP | Allow dedicated files that do not duplicate shared rules | Prohibit them in every project | This document §4 |
| CI request with no runner selected | Write and connect only the workflow and checklist in [CI.md](./CI.md) | Create product-specific YAML for GitHub Actions, Buildkite, or another runner | [CI.md](./CI.md) §4 and §6 |

### Applying Template Revisions

- Read the revision history in §6 and select the changes to apply. Because the history is a summary, compare the recorded previous and new SHAs **in the source repository** with `git diff <previous source SHA> <new source SHA> -- <file>`. When both baselines exactly match tags, you may use `git diff v1.1 v1.2 -- <file>`. If the existing record contains only a version, resolve its tag SHA and supplement the record. Do not treat it as a confirmed copy baseline if you cannot determine whether unreleased changes were included at the time.
- Compare the result with files in the adopted repository (`git diff --no-index <template file> <adopted file>`). Do not revert intentional project changes. For differences absent from the history, distinguish a template omission from an intentional project change.
- After applying changes, update version and revision in both guide documents to the new copy baseline. Update the revision even when adopting another commit from the same version. If applying only part of a source revision, record the included and excluded items and the reason in [DOCS_GUIDE.md](./DOCS_GUIDE.md), so the full SHA is not mistaken for fully adopted content. If `CHANGELOG.md` exists, summarize the new baseline and applied items there.

## 6. Template Revision History

<!-- template-section:release-history -->

Use this history to identify changes that an adopted repository has not yet applied. Each entry records only what changed and what to verify in the adopted repository. The template repository preserves each version with a Git tag (`v1.1`, `v1.2`, and so on), so inspect the source summarized here with `git diff v1.1 v1.2`. Versions before `v1.1` have no tag.

### v2.3.2 — New-or-Empty Install Target

- `installer.py install` accepts only a new path or a readable empty directory. It rejects every non-empty or unreadable target before writing template members, including paths unrelated to the artifact.
- For an existing repository, use the selected release's read-only `adopt` command to produce an artifact and a per-path plan outside the target; it never merges, deletes, or writes the target automatically.
- The artifact changes to apply in an adopted repository are limited to `docs/TEMPLATE_GUIDE.md` and `docs/DOCS_GUIDE.md`; the selected release's separate `installer.py` asset enforces the new-or-empty `install` target.
- Verify in the adopting repository: use `adopt` for its existing tree, and reserve `install` for a separate new path or empty directory.

### v2.3.1 — Windows Release Tool Portability

- Release packaging orders artifact members by POSIX relative path, and materialized-tree verification uses Windows writable semantics while preserving the ZIP Unix mode `0644` contract.
- Repository text checkout is pinned to LF, and symlink-dependent tests skip only when the platform lacks the required capability or Windows privilege. Non-symlink checks remain separate and continue to run.
- The functional artifact change to apply is `tests/test_check_docs.py`; this guide and `docs/DOCS_GUIDE.md` carry the version record, while the release packager and verifier changes are maintainer tools outside the artifact.
- Verify in the adopting repository: replace the bundled checker test, rerun the documentation checker and its tests, and treat symlink-only skips on Windows as an explicit coverage limitation.

### v2.3.0 — Documentation Ownership and Changelog Guidance

- Added locale-specific `docs/CHANGELOG_GUIDE.md` without creating a project-owned root changelog. It separates current README behavior, published release history, future TODO or PLAN work, and template provenance.
- Removed project-specific Metadata placeholders from the bundled `project-analysis` skill.
- The locale guides are the canonical artifact guidance; the source repository keeps only maintainer-specific addenda instead of manually duplicating the artifact guides.
- When adopting this version, add the guide and related links, preserve any existing changelog format, replace both skill copies together, and rerun the documentation checks.

### v2.2.0 — Base-aware Adoption Reports

- `adopt --base-version <older-exact-semver>` verifies an older exact release without running its installer and compares the base release, current release, and target tree.
- The opt-in format 2 report classifies `base ∪ current` paths as `unchanged`, `template-only`, `project-only`, `converged`, `diverged`, or `blocked`; it never merges or deletes target files automatically.
- The release verifier checks the public `en` and `ko` upgrade paths and format 2 invariants.
- The artifact changes to apply in an adopted repository are limited to `docs/TEMPLATE_GUIDE.md` and `docs/DOCS_GUIDE.md`; the selected release's `installer.py` provides the `--base-version` functionality.
- Verify in the adopting repository: use `--base-version` only when the target was derived from that exact base, and review `diverged`, `blocked`, and base-only paths manually.

### v2.1.1 — Documentation Checker and Installer Diagnostic Fixes

- `scripts/check-docs.py` now treats `docs/TEMPLATE_GUIDE.md` as an allowed omission only when the path is absent; an external symlink or directory at that path is an error.
- A release-manifest schema mismatch now tells users to download and run `installer.py` from the same release version.
- Verify in the adopting repository: replace `scripts/check-docs.py` and `tests/test_check_docs.py` together and rerun the checker. If a schema mismatch occurs, use the installer from the selected release version.

### v2.1.0 — `adopt` for Existing Repositories, Project Analysis Skill, and Checker Hardening

- Added a read-only `adopt` command to the installer for existing repositories. It never writes to the target repository; it creates the verified `artifact/` and an experimental `adoption-plan.json` with per-path statuses in an empty directory outside the target. The release manifest is now `schema_version` 2, and each member carries an adoption policy (`copy`, `merge`, or `decide`).
- Verify in the adopting repository: when applying the next version, review the `merge`, `decision`, and `blocked` paths in the `adopt` report. The status table in §2 is the handling rule.
- Moved the whole-project analysis process from `docs/PROJECT_ANALYSIS.md` into the locale's self-contained `.agents/skills/project-analysis/SKILL.md` and added the matching `.claude/skills/` copy for Claude Code.
- The skill applies only to explicit whole-project analysis requests and runs read-only by default. The README, manifest, and checkers now verify that contract and both skill paths.
- Verify in the adopting repository: remove the old `docs/PROJECT_ANALYSIS.md` and its references, then apply the selected locale's two skill copies and the related `AGENTS.md`, README, and documentation-checker changes together.
- `scripts/check-docs.py` now interprets links, HTML blocks, reference definitions, section numbers, `Template version`, and optional-file symlinks more strictly. §3 states the supported Markdown scope.
- Verify in the adopting repository: replace `scripts/check-docs.py` and `tests/test_check_docs.py` together and rerun the checker. Fix any newly reported broken links, ambiguous short document-name references, or optional files that point outside the repository in the documents.

### v2.0.0 — Locale Artifacts and Non-destructive Installation

- Apply a verified artifact for one selected locale, `en` or `ko`, instead of copying the source repository root. Root paths and tool entry points remain stable.
- The release installer verifies the version, locale, manifest, checksums, and member inventory and writes nothing when a target path already exists. Existing projects and locale changes use export to an empty directory followed by a manual merge.
- Repositories already using `v1.7.1` are not migrated automatically. Preserve project-specific values and user changes, and compare the new artifact file by file before selecting updates.
- In the adopting repository, record Template source, version, and revision from the actual artifact; record the selected locale and manual adaptations; then complete §2 and the DOCS_GUIDE checklist.

### v1.7.1 — Canonical Documentation Gates and Corrected Regression-test Scope

- Added the G-docs and G-docs-test commands to `AGENTS.md` and the adopted-project README template, matching the canonical command rule in [CI.md](./CI.md).
- Restricted the G-docs-test discovery pattern to `test_check_docs.py`, so it does not run unrelated `test*.py` files in an adopted project.
- Verify in the adopted repository: if retaining the documentation checker, keep both command strings identical in project instructions and the README, and update the existing CI G-docs-test to the restricted pattern.

### v1.7 — Separate Template-introduction README and Runner-agnostic CI Gates

- Made the root `README.md` the introduction for the template repository and separated the adopted-project README template into `README-PROJECT.md`. Opening the source repository on Origin or another host now shows the template description rather than project placeholders.
- Changed step 2 of adoption §2: place `README-PROJECT.md` as `README.md`, remove its adoption comment at the top, and then fill the placeholders. Do not leave the template-introduction README or `README-PROJECT.md` in the adopted repository.
- Added the README replacement item to the adoption checklist in [DOCS_GUIDE.md](./DOCS_GUIDE.md).
- Added [CI.md](./CI.md): it contains only the quality-gate workflow and integration checklist, without product-specific YAML for GitHub Actions, Buildkite, or another runner. Step 13 of adoption §2, AGENTS.md, and the adoption checklist point to it.
- Verify in the adopted repository: do not replace an already completed project `README.md` with this version's template introduction. Only a new copy follows the `README-PROJECT.md` → `README.md` replacement. Existing adopted repositories keep their own README. If using CI, verify that [CI.md](./CI.md) gates are connected to the existing runner and that no workflow file was created before the user selected a product.

### v1.6.1 — Follow-up Fixes after the v1.6 Review

- Corrected the mistyped `v1.31` tag and history entry to `v1.3.1`, preventing numeric version sorting from selecting it as newer than `v1.6`.
- Updated `scripts/check-docs.py` to validate the boolean `policy.allow_implicit_invocation: false`, avoid being affected by excluded directory names outside the repository, and check multiline invariants, deep section numbers, and missing document targets.
- Fixed these failure paths and standalone use of the combined form in `tests/test_check_docs.py`.
- Kept all four templates under `_template/` during adoption, while clarifying that an actual change directory uses only the templates it needs.

### v1.6 — Expanded Documentation Checks and Combined Change Form

- `scripts/check-docs.py`: changed root detection to `AGENTS.md` and made version comparison optional, so the checker works in repositories that delete this document under §5. Previously, a missing TEMPLATE_GUIDE ended with exit code 2.
- `scripts/check-docs.py`: expanded link checks beyond `.md` targets and fails when a `review-round` skill exists without Codex explicit-invocation configuration (`agents/openai.yaml`). Omitting that configuration enables implicit invocation in Codex.
- `scripts/check-docs.py`: compares invariant lists in [REVIEW.md](./REVIEW.md) §6 and [.cursor/BUGBOT.md](../.cursor/BUGBOT.md). It finds the sections by heading text rather than number, so it works after section numbers change during a merge.
- `scripts/check-docs.py`: compares section-number references that identify a document (`REVIEW.md §6`, `PROJECT §8`, and similar) with actual headings. It skips ambiguous same-file references, old numbers in the §6 release history, and generated directories such as `dist`, `build`, `target`, and `vendor`.
- Added [`docs/changes/_template/01-CHANGE.md`](./changes/_template/01-CHANGE.md), which provides the combined-form section layout defined by [01-DESIGN.md](./01-DESIGN.md) §4. It combines the change-log sections from the split INTENT and SPEC forms.
- [DOCS_GUIDE.md](./DOCS_GUIDE.md): added a `LICENSE` replacement item to the adoption checklist so the template's own MIT notice is not retained as the project license.
- Verify in the adopted repository: replace `scripts/check-docs.py` with the new version; determine whether newly reported invariant or section-number mismatches are real documentation inconsistencies (they may be previously undetected rather than false positives); remove `01-CHANGE.md` and incoming links if the combined form is unused; and replace `LICENSE`.

### v1.5.1 — Generalized Coexistence Guidance and Refined Copilot Hints

- `docs/TEMPLATE_GUIDE.md` §4: removed product-specific examples from the external methodology and behavioral-rules section, leaving only ownership: always-on rules in `AGENTS.md`, conditional processes in `docs/`, and skills as adapters.
- Split the Copilot rereview hint into a table and command block. Retained the GraphQL request and acceptance check and the REST no-op warning.
- Verify in the adopted repository: ensure the coexistence section is not tied to one product name and that §2.1 includes the command block or its reference when Copilot is used.

### v1.5 — Tool Conditions, Documentation Checks, and Identifier Lifetimes

- `docs/TEMPLATE_GUIDE.md` §4: made the prohibition on additional instruction files such as `.claude/CLAUDE.md` conditional on OMP use. Tool-specific files are allowed without OMP, but shared rules must not be duplicated.
- `scripts/check-docs.py`: checks relative links, skill copies, `CLAUDE.md`/WATCHDOG imports, and Template version in both guide documents using only the standard library, and returns a nonzero exit code on failure. This replaced the inline link-check example.
- Defined issuance scopes and parallel-branch collision handling for change IDs, `D-nnn`, `T-nnn`, and change-internal IDs. Completed, cancelled, and deferred change directories remain, while implemented contracts enter the current PROJECT baseline only after integration.
- Added behavior-verification cases for instruction, skill, and checker changes.
- Verify in the adopted repository: ensure there is no blanket prohibition on tool-specific instruction files when OMP is unused; copy `scripts/check-docs.py`; do not mix `D-` or `T-` IDs with change-internal IDs; and do not treat a completed SPEC as the current product baseline.

### v1.4 — Numbered Documents and Per-change Artifacts

- Migrated shared documents to `00-PROJECT.md`, `01-DESIGN.md`, and `02-TODO.md`. PROJECT now contains the base product design and existing-design index.
- Added the optional `10-EXTENSION.md` and uppercase INTENT, SPEC, and PLAN templates under `changes/_template/`. Small work uses minimal documentation; implementation of an approved phase references its parent design.
- Defined ownership of the global change list and detailed execution status, along with local Git, parallel branches, integration completion, and approval evidence. The new format distinguishes updating a spec or execution plan while preserving approved versions.
- Updated instruction, skill, review, and analysis paths and handoff targets. After a review round passes, the PLAN is also frozen and its records are applied during the next related task.
- Verify in the adopted repository: use the §2 migration table to check fixed policy paths, checker code, skill references, and duplicate status.

The old filenames and section numbers in the release history below describe the structure at that time. They are not instructions to execute at current paths; follow the migration table and current process above.

### v1.3.1

- `docs/DESIGN.md`: resolved a wording conflict between the prohibition on project-specific information in §5 and the one-line exception in §6 for an existing design-document path.
- `.agents/skills/review-round/`, `.claude/skills/review-round/`: updated the skill description to reflect the default `on_pass`. Merge a PR only after user confirmation; without a PR, finish with `do not merge`. Keep both `SKILL.md` files identical.
- Verify in the adopted repository: ensure no project-specific information other than the existing-design-document path remains in `DESIGN.md`, and ensure both review-round skill descriptions match the default `on_pass`.

### v1.3

- `docs/REVIEW_ROUND.md`: changed the default pass condition to `all P0 = 0, all P1 = 0, blocking P2 = 0`. Under the default, any valid unresolved P0 or P1 blocks a pass even if `blocking=false` or covered by an approved deferral. A user-selected threshold takes precedence and applies to fixes, carryover, early stop, and exhaustion reports. Added rules for recording and reevaluating an explicit mid-run change and added the default decision table.
- `.agents/skills/review-round/`, `.claude/skills/review-round/`: updated the default threshold. Keep both `SKILL.md` files identical.
- `docs/REVIEW.md` (`Policy version` 1.2), `.cursor/BUGBOT.md`, `AGENTS.md`: aligned the exception for reporting verified pre-existing P0 and P1 issues with the round pass condition. Preserved `blocking` classification and single-review verdict rules.
- `.agents/skills/review-round/agents/openai.yaml`: added `policy.allow_implicit_invocation: false` to allow only explicit invocation in Codex. Preserved frontmatter for Claude, Cursor, and OMP and equality of both `SKILL.md` files.
- `docs/REVIEW_ROUND.md` and both `review-round/SKILL.md` files: `self` runs without reviewer registration, external requests, or waiting and keeps its ledger in the session. `do not merge` ends with pass and no merge; it is the default when there is no PR.
- `docs/TEMPLATE_GUIDE.md`, `docs/DOCS_GUIDE.md`: included hidden directories in placeholder searches and distinguished checks in the source template from checks in an adopted repository. Zero search results do not mean adoption is complete.
- `docs/REVIEW_ROUND.md` and both `review-round/SKILL.md` files: preserve the passing head and hand off remaining findings and decision evidence in the session handoff list. Immediately before merge, check only state and new results; do not push another record-only commit. Move repository-document updates from §9 into the next related implementation or documentation task started by the user, and added an entry condition to `AGENTS.md` that applies only §9 without restarting the round.
- `docs/TEMPLATE_GUIDE.md`, `docs/DOCS_GUIDE.md`: added `Template revision` and Git inspection steps to record source location, version, and full SHA together. Distinguished unreleased changes, uncommitted changes, and partial adoption, and based revision comparison on source SHAs.
- Verify in the adopted repository: ensure the default does not exclude nonblocking P0 or P1; ensure user-selected thresholds also apply to fixes and carryover; ensure no clause updates TODO immediately after a pass. Update both skills, the Bugbot copy, and the source revision record together. Increment the source template's `Template version` at the next release.

### 1.2

- `docs/DESIGN.md`: generalized the §1 exclusion to "implementation of a design recorded as accepted" (PLAN.md §8 `Accepted` or a settled phase in an existing design document). Added comparison targets in §3.4 for repositories that remove optional sections. Added §6, "Repositories with Existing Design Documents": do not move them; interpret artifacts in repositories where PLAN.md is an index; and define the relationship with their own checklists. Moved the former §6 external-specification tools to §7.
- `.agents/skills/design/`, `.claude/skills/design/`: added "do not use for implementation of a design already recorded as accepted" to the description. Because this affects automatic invocation, update both files in adopted repositories too.
- `.agents/skills/review-round/`, `.claude/skills/review-round/`: added `rereview = auto` to the third default.
- `docs/REVIEW_ROUND.md`: added release publication and tag creation to the list of undelegated actions in §1. Added whether a comment is overwritten (sticky) to the §2.1 `Publication location`. Added Build and generated-output regeneration to verification in §3 step 4. Added a rule in §7 to retain findings from reviewers that overwrite comments in the decision record.
- `docs/DOCS_GUIDE.md`: expanded section-number comparison to cover `DESIGN.md`, `WATCHDOG.md`, and removal of optional PLAN.md sections. Added an existing-design-documents item, mentioned the `Rereview request method` column in the reviewer table, and added tag comparison and CHANGELOG recording to Maintenance.
- `docs/TEMPLATE_GUIDE.md`: added references to four section-numbered files to the §2 merge instructions, along with the DESIGN.md §6 guidance. Added a self-hosted GitHub App row to reviewer hints. Added tag-to-tag `git diff` comparison to §5 and tag guidance to this history section.
- Began managing the template repository with Git. `v1.1` is the final 1.1 state and `v1.2` is this release.
- Included fixes from two review rounds of the first adoption PR (claude-code-pr-review #33) in the same release:
  - `docs/REVIEW_ROUND.md`: added "mark handled finding's inline thread resolved" to delegated authority in §1 (required by §6 but absent from the delegation list). Distinguished REST `requested_reviewers` from GraphQL `reviewRequests` in §2.1 acceptance examples and recorded when to check. In §3 `request`, counted reviewers with confirmed acceptance toward that round's quorum. Added base changes as an exception to the no-push round rule. In §4, clarified that only non-force merge is delegated for base changes, not rebase. In §7, defined where PR decision records live (session plus the §10 report).
  - `AGENTS.md`: narrowed DESIGN exceptions to the canonical §1 conditions ("a bug whose cause is not structural" and "a change within one module that does not alter an external contract"). Added thread resolution to delegated authority.
  - `.agents/skills/design/`, `.claude/skills/design/`: applied the same conditions to description exceptions.
  - `docs/DESIGN.md` §4: allowed `Superseded by <link>` in `Status` for `docs/changes/` files. Only the body is frozen.
  - `docs/DOCS_GUIDE.md`: added `Template source` to Metadata, including the template repository location and tag rules. Without it, the tag comparison in §5 cannot be reproduced.
  - `docs/TEMPLATE_GUIDE.md`: made GraphQL `requestReviews` the primary Copilot rereview path after observing the REST no-op, and added a copyable `gh api graphql` command block.
  - Third-round additions: removed the assertion in `docs/REVIEW_ROUND.md` §1 that a round cannot start without a push because it conflicted with base-change handling. Added "Severity normalization" in §4: a finding from a reviewer that does not use the P scale is reclassified using REVIEW.md Severity definitions, while the original label remains in the ledger. Added the design-detail location `docs/changes/` to the `docs/DESIGN.md` preamble and "Shared by Both Sizes" to §2: regardless of size, a decision affecting review outcomes updates REVIEW.md §6 and §9 and BUGBOT.md in the same commit.
  - Later round: in `docs/REVIEW_ROUND.md` §3 round 1 with `rereview = request`, request without a push only from reviewers that are in the confirmed `reviewers`, have an explicit request method, and lack a current-head result. Do not request reviewers whose only method is `automatic on push`. If acceptance is signaled outside the request response, such as a comment reaction, do not fail immediately; recheck for the default two-minute limit. Use the identifier value from that API and do not treat a REST `[bot]` username and GraphQL `Bot.login` as the same string. Explicit invocation of `design` takes precedence over the exception list in `docs/DESIGN.md` §1.
- Verify in the adopted repository: ensure the `design` skill description is updated, record whether PR-comment reviewers overwrite their comments in the `Publication location` column of REVIEW_ROUND.md §2.1, verify references in the four section-numbered files against actual headings, and fill `Template source` in `DOCS_GUIDE.md`.

### 1.1

- `AGENTS.md`: explicitly delegated non-force push, rereview requests selected by parameters, and merge after user confirmation for review rounds. Other PR comments remain undelegated. Added the rule not to execute command-table placeholders in `{{...}}` form. Added `docs/DESIGN.md` to the Document System. Added four Change Rules covering reuse order, minimal code, root-cause fixes, and limits on minimization (migrated from the ponytail rules).
- Added `docs/DESIGN.md`: pre-implementation design process for structural and contract changes (applicability, size selection, six phases, artifact rules). Added adapters under `.agents/skills/design/` and `.claude/skills/design/`. `docs/changes/` is created only for large changes.
- Added `.omp/WATCHDOG.md`: OMP advisor-specific review priorities importing `REVIEW.md`.
- `docs/REVIEW_ROUND.md`: added `reviewers = self`; refuse to start when a reviewer is unregistered; include REVIEW.md section titles in references; collect collapsed `<details>` blocks; start a new round after a base change; record reviewer self-reported partial inspection as a `partial result` and present it at merge confirmation. Added the `rereview` parameter (`auto` by default, `request` when selected by the user), added the `Rereview request method` column to the §2.1 table, and rewrote §3 step 1 as per-round request rules.
- `docs/REVIEW.md`: no change (`Policy version` 1.1 retained).
- `.cursor/BUGBOT.md`: added project invariants, settled design decisions, and approved deferrals.
- `docs/PLAN.md`: added guidance distinguishing required from optional sections.
- `docs/DOCS_GUIDE.md`: specified that `Last reviewed` uses UTC; added Bugbot invariant comparison, section-number checking, CODEOWNERS, and link checking to the adoption checklist.
- `docs/DOCS_GUIDE.md`: added `DESIGN.md` to Document Map, Flow, and Source of Truth; added WATCHDOG import checking, the `design` skill, and external methodology coexistence to the checklist; added `.omp/` and `docs/DESIGN.md` to the CODEOWNERS list.
- `docs/TEMPLATE_GUIDE.md`: corrected the placeholder search command; added a link checker, guidance for `disable-model-invocation` and Cursor's two skill paths, reviewer research hints, CODEOWNERS guidance, §4 "External Methodology and Behavioral-Rules Tools" (coexistence rules for ponytail, OpenSpec, BMAD, and Kiro), and this history entry.
- `LICENSE`: distributes the template itself under MIT. Adopted repositories replace it with their project license.
- Verify in the adopted repository: ensure the corresponding `SKILL.md` files under `.agents/skills/` and `.claude/skills/` are byte-identical; ensure the REVIEW_ROUND.md §2.1 reviewer table is filled in and has a `Rereview request method` column; ensure BUGBOT.md invariants match REVIEW.md §6; and, when using OMP, ensure `.omp/WATCHDOG.md` expands its import.

### 1.0

- Initial release. No history before this release was recorded.
