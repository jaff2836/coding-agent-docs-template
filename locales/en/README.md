# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

> This is the project-root README template placed by the selected locale artifact. Do not replace it with the template source repository's introduction. Replace the placeholders and guidance below with actual project values, and record the adopted Template source, version, and revision in the [Template Guide](./docs/TEMPLATE_GUIDE.md) and [Documentation Guide](./docs/DOCS_GUIDE.md).

## Requirements

- Describe the runtimes and tools required by the project.

## Setup

Describe the project installation and initial configuration steps.

## Run

```text
{{RUN_COMMAND}}
```

## Build

```text
{{BUILD_COMMAND}}
```

## Test

```text
{{TEST_COMMAND}}
```

## Quality Checks

```text
{{LINT_COMMAND}}
{{TYPECHECK_COMMAND}}
python scripts/check-docs.py
python -m unittest discover -s tests -p 'test_check_docs.py' -v
```

Run the documentation checker regression tests when changing `scripts/check-docs.py` or `tests/test_check_docs.py`. Follow [CI.md](./docs/CI.md) for documentation checks and CI integration. This template does not include YAML for a specific runner. Keep command strings identical to those in [AGENTS.md](./AGENTS.md).

## Project Documentation

- [Template Guide](./docs/TEMPLATE_GUIDE.md): how to apply this template to a project for the first time
- [AGENTS.md](./AGENTS.md): shared project instructions for AI development tools
- [Documentation Guide](./docs/DOCS_GUIDE.md): documentation system, sources of truth, and template completion checklist
- [00-PROJECT.md](./docs/00-PROJECT.md): product overview, base design, current and target structures, decisions, and design index
- [01-DESIGN.md](./docs/01-DESIGN.md): pre-implementation design process for changes to structure or contracts
- [02-TODO.md](./docs/02-TODO.md): project-wide changes, priorities, dependencies, and integration results
- [10-EXTENSION.md](./docs/10-EXTENSION.md): optional long-term extension design and phase-specific completion criteria
- Change template set: combined [01-CHANGE.md](./docs/changes/_template/01-CHANGE.md), split [01-INTENT.md](./docs/changes/_template/01-INTENT.md) and [02-SPEC.md](./docs/changes/_template/02-SPEC.md), and optional [03-PLAN.md](./docs/changes/_template/03-PLAN.md). When applying the template, copy the entire `_template/` set. For an actual change, copy only the necessary format into a separate change-ID folder.
- [REVIEW.md](./docs/REVIEW.md): PR review policy
- [REVIEW_ROUND.md](./docs/REVIEW_ROUND.md): review round process and delegated authority
- [PROJECT_ANALYSIS.md](./docs/PROJECT_ANALYSIS.md): explicitly requested whole-project analysis process
- [CI.md](./docs/CI.md): runner-agnostic quality gate workflow and integration checklist

## Security

Describe how to report vulnerabilities and what information must not be disclosed.

## License

Specify the project's license.

This template itself is provided under the MIT License ([LICENSE](./LICENSE)). A project that adopts the template must choose its own license and replace both the `LICENSE` file and this section. Do not leave the template's MIT notice in place as the project's license.
