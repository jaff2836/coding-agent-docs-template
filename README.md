# AI Agent Docs Template

A documentation template that helps people and AI coding agents collaborate with the **same document structure, design process, and review criteria**. It provides project documentation and agent instructions rather than an application framework.

It supports Claude, Codex, Cursor, and [Oh My Pi](https://github.com/can1357/oh-my-pi). Version 2 provides English (`en`) and Korean (`ko`) locales.

[한국어](./README.ko.md)

## Installation

Download `installer.py` from the latest GitHub release and list the supported locales. For an existing repository, run `adopt` to get the verified files and a per-path plan without touching the repository. For a new project, run `install`.

### 1. Download the installer

On Linux or macOS:

```sh
curl -fL --proto-redir '=https' -o installer.py.part \
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py &&
mv installer.py.part installer.py
```

On Windows PowerShell:

```powershell
curl.exe -fL --proto-redir "=https" -o installer.py.part `
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py
if ($LASTEXITCODE -ne 0) { throw "Failed to download installer.py" }
Move-Item -Force -ErrorAction Stop installer.py.part installer.py
```

Continue only after the download block succeeds.

### 2. List the supported locales

```sh
python3 installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
```

On Windows PowerShell:

```powershell
python installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
```

### 3. Adopt into an existing project

```sh
python3 installer.py adopt --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root /path/to/existing-project --output /path/to/empty-directory
```

On Windows PowerShell:

```powershell
python installer.py adopt --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root C:\path\to\existing-project --output C:\path\to\empty-directory
```

`adopt` never writes to the project. It creates `artifact/` with the verified locale files and `adoption-plan.json`, which marks each path as `missing`, `identical`, `merge`, `decision` (for example `LICENSE`), or `blocked`. Merge the files yourself or with a coding agent by following the adoption steps in `artifact/docs/TEMPLATE_GUIDE.md`. The output directory must be outside the project; delete it to cancel. The plan format is experimental and may change in a minor release. `adopt` is available in the release after `v2.0.0`; with `v2.0.0`, run `export` below and compare the files manually.

### 4. Install into a new project

```sh
python3 installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root /path/to/new-project
```

On Windows PowerShell:

```powershell
python installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root C:\path\to\new-project
```

Set `--locale` to `en` or `ko`. The target must be new or empty; if any destination file already exists, the installer writes nothing.

### Export the artifact only

To inspect the verified files without a plan, export them into an empty directory.

```sh
python3 installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --output /path/to/empty-directory
```

On Windows PowerShell:

```powershell
python installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --output C:\path\to\empty-directory
```

The installer never overwrites existing files and does not provide automatic updates, locale switching, or `--force`. It follows only the HTTPS redirect chain initiated by a verified GitHub release asset URL, then validates the exact tagged release's manifest, checksums, and its own bytes. For another language, you can localize the English artifact's project instructions and documents, but the result is outside the officially verified locales.

## After installation

1. Replace the placeholders, project information, and commands in `README.md` and `AGENTS.md`.
2. Record the product baseline in `docs/00-PROJECT.md` and current work in `docs/02-TODO.md`.
3. Use the `design` process for changes to architecture or public contracts.
4. Follow `docs/REVIEW.md` for PR reviews, and invoke `review-round` explicitly only when you need an iterative fix-and-rereview cycle.

Each tool reads the same contract through fixed paths in `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/skills/`, `.cursor/`, and `.omp/`.

## Verifying the template

Repository development and release preparation use only the Python 3 standard library, with no production dependencies.

```text
python3 scripts/check-docs.py
python3 scripts/check-locales.py --require-stable
python3 -m unittest discover -s tests -v
```

To inspect a locale artifact directly from a source checkout, export it into an empty directory.

```text
python3 scripts/export-template.py --locale en --output /path/to/empty-directory
```

- `check-docs.py` checks links, imports, skill copies, invariants, and document version metadata.
- `check-locales.py` checks locale inventories, placeholders, markers, and skill contracts.
- The full test suite covers successful and failing paths for the exporter, deterministic packager, and the non-destructive installer's `install`, `export`, and read-only `adopt`.

## What's included

- **Shared instructions:** `AGENTS.md`, `CLAUDE.md`, and tool-specific integration files
- **Document system:** project baseline, design, TODO, review, and CI guidance
- **Skills:** `design`, `project-analysis`, and `review-round`
- **Multilingual delivery:** `template/common/`, `locales/en/`, `locales/ko/`, the manifest, and the schema
- **Tools:** documentation and locale checks, export, release packaging, and installation

See the [Template Guide](./docs/TEMPLATE_GUIDE.md) for the complete structure and adoption checklist, and the [Documentation Guide](./docs/DOCS_GUIDE.md) for document ownership and operating rules. This repository does not include application code or pipelines for a specific CI product.

## Bundled skills

- **`design`:** turns structural or public-contract changes into the minimum necessary intent, specification, and execution plan before implementation.
- **`project-analysis`:** performs an explicitly requested, evidence-based whole-project assessment in read-only mode by default and reaches a GO, conditional, no-go, or insufficient-evidence decision.
- **`review-round`:** runs an explicitly invoked review/fix cycle against the exact PR head and merges only after the configured gate passes and the user confirms.

`project-analysis` becomes a bundled skill in the release after `v2.0.0`. The `v2.0.0` artifacts provide this process as `docs/PROJECT_ANALYSIS.md` instead.

Codex, Cursor, and OMP load the `.agents/skills/` copies; Claude Code loads the byte-identical `.claude/skills/` copies.

## License

This template is distributed under the [MIT License](./LICENSE). Projects that adopt it should define their own license and security reporting process.
