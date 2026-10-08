# AI Agent Docs Template

A documentation template for people and AI coding agents to collaborate with the **same document structure, design process, and review criteria**. It provides project documentation and agent instructions, not an application framework.

It supports Claude, Codex, Cursor, and [Oh My Pi](https://github.com/can1357/oh-my-pi).

[한국어](./README.ko.md)

## Installation

### Prerequisites

- Python 3 (3.12 or newer on Windows)
- `curl` (`curl.exe` on Windows)
- Network access to GitHub
- Optional: GitHub CLI (`gh`) for the attestation check in step 2

### 1. Download the installer

Linux or macOS:

```sh
curl -fL --proto-redir '=https' -o installer.py.part \
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py &&
mv installer.py.part installer.py
```

Windows PowerShell:

```powershell
curl.exe -fL --proto-redir "=https" -o installer.py.part `
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py
if ($LASTEXITCODE -ne 0) { throw "Failed to download installer.py" }
Move-Item -Force -ErrorAction Stop installer.py.part installer.py
```

Continue only if the download succeeds. On Windows, use `python` instead of `python3` and Windows paths in the commands below.

### 2. Check (optional)

Locales in the current release:

| Locale | Language | Status |
| --- | --- | --- |
| `en` | English | complete |
| `ko` | Korean | complete |

```sh
python3 installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
gh release verify-asset installer.py --repo jaff2836/coding-agent-docs-template
```

`list-locales` lists the locales of a release. `gh release verify-asset` checks the installer against the attestation that GitHub signs for the latest release; put a tag such as `v2.5.0` before the file name to check a specific release. The attestation does not protect against a compromised publishing account.

### 3. Apply the template

Choose one option and set `--locale` to a supported locale.

#### Option A: Existing project (`adopt`)

```sh
python3 installer.py adopt --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root /path/to/existing-project --output /path/to/empty-directory
```

`adopt` does not write to the project. In an output directory outside the project, it creates `artifact/` with the verified files and `adoption-plan.json`, which classifies each path as `missing`, `identical`, `merge`, `decision`, or `blocked`. Merge the files by following `artifact/docs/TEMPLATE_GUIDE.md`. To upgrade a project adopted from an exact earlier release, add `--base-version <older-exact-semver>`; the report then classifies paths as `unchanged`, `template-only`, `project-only`, `converged`, `diverged`, or `blocked`. The plan format is experimental.

#### Option B: New project (`install`)

```sh
python3 installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root /path/to/new-project
```

The target must be a new path or an empty directory. If it does not exist yet, its parent must be an existing directory that is not a symlink or junction. Run `git init` after installing; a directory that already contains `.git` is not empty, so use Option A for it.

#### Option C: Files only (`export`)

```sh
python3 installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --output /path/to/empty-directory
```

`export` writes the verified files to an empty directory without a plan.

The installer verifies the release manifest, checksums, and its own bytes before writing, and never overwrites existing files. It has no `--force`, automatic update, or locale switching. For another language, localize the English artifact; the result is not an officially verified locale.

## After installation

1. Replace the placeholders, project information, and commands in `README.md` and `AGENTS.md`.
2. Record the product baseline in `docs/00-PROJECT.md` and current work in `docs/02-TODO.md`.
3. Use the `design` process for changes to architecture or public contracts.
4. Follow `docs/REVIEW.md` for PR reviews; invoke `review-round` only for an iterative fix-and-rereview cycle.

Each tool reads the same contract through fixed paths in `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/skills/`, `.cursor/`, and `.omp/`.

## Verifying the template

Repository development and release tooling use only the Python 3 standard library.

```text
python3 scripts/check-docs.py
python3 scripts/check-locales.py --require-stable
python3 -m unittest discover -s tests -v
python3 scripts/export-template.py --locale en --output /path/to/empty-directory
```

- `check-docs.py`: links, imports, skill copies, invariants, and document version metadata
- `check-locales.py`: locale inventories, placeholders, markers, and skill contracts
- `export-template.py`: writes a locale artifact from the source checkout into an empty directory
- Tests: success and failure paths of the exporter, the deterministic packager, and the installer's `install`, `export`, and read-only `adopt`

Maintainers verify a human-prepared draft before publication and the immutable Latest release afterwards, from a clean exact-source checkout. Both commands are read-only with respect to remotes and require `git` and `gh`.

```text
python3 scripts/verify-release.py candidate --version {{VERSION}} --source-commit {{EXACT_COMMIT}} --repository {{OWNER/NAME}}
python3 scripts/verify-release.py published --version {{VERSION}} --source-commit {{EXACT_COMMIT}} --repository {{OWNER/NAME}} --release-url https://github.com/{{OWNER/NAME}}/releases
```

## What's included

- **Shared instructions:** `AGENTS.md`, `CLAUDE.md`, and tool-specific integration files
- **Document system:** project baseline, design, TODO, review, and CI guidance
- **Skills:** `design`, `project-analysis`, and `review-round`
- **Multilingual delivery:** `template/common/`, `locales/en/`, `locales/ko/`, the manifest, and the schema
- **Tools:** documentation and locale checks, export, release packaging and verification, and installation

Structure and adoption checklists: [English Template Guide](./locales/en/docs/TEMPLATE_GUIDE.md) and [Documentation Guide](./locales/en/docs/DOCS_GUIDE.md), or [Korean Template Guide](./locales/ko/docs/TEMPLATE_GUIDE.md) and [Documentation Guide](./locales/ko/docs/DOCS_GUIDE.md). The root [Template Guide](./docs/TEMPLATE_GUIDE.md) and [Documentation Guide](./docs/DOCS_GUIDE.md) are maintainer addenda. This repository contains no application code and no pipelines for a specific CI product.

## Bundled skills

- **`design`:** turns structural or public-contract changes into the minimum necessary intent, specification, and execution plan before implementation.
- **`project-analysis`:** performs an explicitly requested, evidence-based whole-project assessment, read-only by default, and reaches a GO, conditional, no-go, or insufficient-evidence decision.
- **`review-round`:** runs an explicitly invoked review/fix cycle against the exact PR head and merges only after the configured gate passes and the user confirms.

Codex, Cursor, and OMP load the `.agents/skills/` copies; Claude Code loads the byte-identical `.claude/skills/` copies.

## Release notes

Version-specific changes are in the [release notes](./CHANGELOG.md) ([Korean](./CHANGELOG.ko.md)).

## License

This template is distributed under the [MIT License](./LICENSE). Projects that adopt it should define their own license and security reporting process.
