# AI Agent Docs Template

A documentation template that helps people and AI coding agents collaborate with the **same document structure, design process, and review criteria**. It provides project documentation and agent instructions rather than an application framework.

It supports Claude, Codex, Cursor, and [Oh My Pi](https://github.com/can1357/oh-my-pi). Version 2 provides English (`en`) and Korean (`ko`) locales.

[한국어](./README.ko.md)

## Installation

Download `installer.py` from the latest GitHub release, list the supported locales, and install one into a new project.

### 1. Download the installer

On Linux or macOS:

```sh
curl --fail --location --proto '=https' --proto-redir '=https' \
  --output installer.py.part \
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py &&
mv installer.py.part installer.py
```

On Windows PowerShell, call `curl.exe` explicitly to avoid the legacy `curl` alias:

```powershell
curl.exe --fail --location --proto "=https" --proto-redir "=https" --output installer.py.part https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py
if ($LASTEXITCODE -ne 0) { throw "Failed to download installer.py" }
Move-Item -Force -ErrorAction Stop installer.py.part installer.py
```

Continue only after the download block succeeds.

### 2. List the supported locales

```sh
python3 installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
```

On Windows PowerShell, use `py -3`:

```powershell
py -3 installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
```

### 3. Install a locale

```sh
python3 installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root /path/to/new-project
```

On Windows PowerShell:

```powershell
py -3 installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --repo-root C:\path\to\new-project
```

Set `--locale` to `en` or `ko`. The target must be new or empty; if any destination file already exists, the installer writes nothing.

### Existing projects

Do not install directly into a project that already uses v1 or maintains its own documentation. Export v2 into an empty directory, compare it with the existing files, and apply only the changes you need.

```sh
python3 installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --output /path/to/empty-directory
```

On Windows PowerShell:

```powershell
py -3 installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale en --output C:\path\to\empty-directory
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
- The full test suite covers successful and failing paths for the exporter, deterministic packager, and non-destructive installer.

## What's included

- **Shared instructions:** `AGENTS.md`, `CLAUDE.md`, and tool-specific integration files
- **Document system:** project baseline, design, TODO, review, analysis, and CI guidance
- **Skills:** `design` and `review-round`
- **Multilingual delivery:** `template/common/`, `locales/en/`, `locales/ko/`, the manifest, and the schema
- **Tools:** documentation and locale checks, export, release packaging, and installation

See the [Template Guide](./docs/TEMPLATE_GUIDE.md) for the complete structure and adoption checklist, and the [Documentation Guide](./docs/DOCS_GUIDE.md) for document ownership and operating rules. This repository does not include application code or pipelines for a specific CI product.

## License

This template is distributed under the [MIT License](./LICENSE). Projects that adopt it should define their own license and security reporting process.
