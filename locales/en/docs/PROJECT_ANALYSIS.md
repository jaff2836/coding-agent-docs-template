# Project Analysis Procedure

Apply this document only when the user explicitly requests a whole-project analysis, technical due diligence, architecture assessment, or acquisition-feasibility assessment. Do not apply this entire procedure to ordinary feature implementation, bug fixes, question answering, or PR reviews.

## Metadata

- **Status:** Active
- **Owner:** Customize for the project
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** When the analysis criteria or project documentation system changes

## 1. Purpose

The purpose of an analysis is to answer the following questions using evidence from the repository's actual code and configuration.

- What problem does this project solve, and for whom?
- How do the currently implemented features differ from the documented goals?
- What technologies and architecture does it use, and how does core data flow through the system?
- What is required for local execution and testing, and for deployment and operations?
- What are the primary correctness, security, performance, and maintainability risks?
- Is it ready to adopt or extend now? If not, what must be improved first?

Analysis is not a coding or refactoring task. Do not modify files, install dependencies, run migrations, deploy, call external services, or change documentation status unless the user explicitly requests it.

## 2. Analysis Principles

### 2.1 Evidence First

- Use the repository's actual code, configuration, tests, CI, and deployment files as primary evidence.
- Use the README and planning documents to understand intent and operating procedures, but verify separately whether they agree with the actual code.
- For important judgments, provide repository-relative paths and relevant symbols, configuration keys, or sections whenever possible.
- Do not state unverified information as fact.

### 2.2 Distinguish Facts, Inferences, and Unverified Items

Classify analysis results as follows.

- **Confirmed:** A fact verified directly in code or configuration
- **Inference:** A judgment reasonably derived from multiple pieces of evidence but not verified by execution
- **Unverified:** Something that cannot be verified because a required file, environment, credential, or execution result is unavailable

### 2.3 User Request Takes Priority

- The analysis scope, exclusions, and output format specified by the user take precedence over this document.
- If the user requests only a particular module, do not analyze the entire repository unnecessarily.
- Items in [02-TODO.md](./02-TODO.md) do not authorize automatic expansion of the user's request.

### 2.4 Safe Analysis

- Perform analysis read-only by default.
- Do not expose secret values. Record only environment-variable names and whether they are required.
- Run relevant tests, type checks, or lint only when existing dependencies are ready and doing so will not change external state.
- If dependency installation, a database migration, a long-running service, or access to external infrastructure is required, do not perform it; record it as a prerequisite.
- If you cannot run tests, state why and describe the limitations of the validation scope.

## 3. Evidence Priority

When information conflicts, use the following priority order.

1. Current code and actual configuration
2. Automated tests and CI configuration
3. Schemas, API specifications, migrations, and deployment configuration
4. [00-PROJECT.md](./00-PROJECT.md), linked product and extension designs, approved INTENT and SPEC documents, and ADRs
5. README files, operations documentation, examples, and comments
6. [02-TODO.md](./02-TODO.md), change-specific PLANs, and other planning checklists

When a lower-priority document differs from stronger evidence, record it as a documentation-code mismatch. Determine separately whether the code violates the document's intent or the document is outdated.

## 4. Establish the Analysis Scope

At the start of the analysis, establish the following scope internally.

- Whether the target is the entire repository or a particular service, package, or directory
- Whether this is an analysis of the current state or a comparison against a particular branch, commit, or release
- Which perspectives matter most: architecture, security, operations, or adoption
- Whether runtime validation is required or static analysis is sufficient
- Whether the intended reader is a developer, manager, security specialist, or adoption decision-maker

Even if the scope is not fully explicit, proceed using safe and reasonable defaults. Ask the user only when required information is missing and would substantially change the result.

## 5. Analysis Procedure

### 5.1 Confirm the Repository Baseline

Check the following first.

- The repository root and major subprojects
- The current branch or target state for the analysis
- Existing changes in the worktree
- [AGENTS.md](../AGENTS.md) and instructions in subdirectories
- [00-PROJECT.md](./00-PROJECT.md), [02-TODO.md](./02-TODO.md), linked product and extension designs, actual change-specific INTENT, SPEC, and PLAN documents, and ADRs
- README files, the license, contribution guides, and the security policy

Keep existing user changes separate from the analysis target; do not modify or revert them. Do not count copy templates in `changes/_template/` as actual designs or active work.

### 5.2 Build a Project Inventory

Explore the following files first to identify the technical composition.

- Package and dependency declarations
- Lockfiles and workspace configuration
- Build, test, lint, and type-check configuration
- Container, IaC, CI/CD, and release configuration
- Application entry points and primary library entry points
- Environment-variable examples and configuration schemas
- Database schemas and migrations
- API specifications, event schemas, and protocol definitions

Read low-analysis-value areas such as generated output, caches, vendored code, and complete lockfile contents in detail only when necessary.

### 5.3 Verify the Product Purpose and Features

Do not merely repeat the documentation. Verify implementation through actual entry points, routes, commands, public APIs, and major UI flows.

Summarize the following.

- The problem being solved and primary use cases
- Target users and operators
- Implemented core features
- Features described in documentation but lacking implementation evidence
- Experimental features, features behind flags, and incomplete paths
- Explicitly unsupported scope

### 5.4 Analyze the Technology Stack and Execution Model

Check the following.

- Languages, runtimes, frameworks, and core libraries
- Minimum or pinned versions and compatibility ranges
- Package managers and build systems
- Whether the architecture is a single application, monolith, modular monolith, separated services, or a library
- Synchronous and asynchronous execution models and background work
- Boundaries among processes, threads, queues, schedulers, and external services
- Use of data stores, caches, message brokers, and file systems

Do not merely list technology names. Explain what responsibility each technology serves.

### 5.5 Trace Architecture and Data Flow

Select at least one representative user or system flow and trace it end-to-end.

For example:

1. Where does input enter?
2. Where is it authenticated, validated, and normalized?
3. Which layers and modules does it pass through?
4. Where is state stored or cached?
5. Under what contracts does it communicate with external systems?
6. How are success, failure, retry, and cancellation results returned?

Check the following structural properties.

- Separation of responsibilities among layers and modules
- Dependency direction and circular dependencies
- Coupling between domain logic and framework code
- Boundaries between public interfaces and internal implementations
- Duplicate implementations and de facto single points of failure
- Extension points, plugins, or adapter structures

Use a simple Mermaid diagram or directory tree only when the relationships are complex. Do not add relationships to the diagram that are not verified in code.

### 5.6 Evaluate Code Quality and Design

Examine representative and high-risk modules from the following perspectives.

- Clarity of names and responsibilities
- Function and module size and cohesion
- Duplicate logic and the scope of change propagation
- Error classification, propagation, recovery, and logging
- Input validation and handling of null, empty, false, and zero values
- State management, concurrency, transactions, and idempotency
- Resource lifetime and cleanup paths
- Configuration defaults and precedence
- Stability and backward compatibility of public APIs
- Architectural and design patterns in use and their actual consistency

Prioritize structural problems that affect failure risk and change cost over stylistic preferences.

### 5.7 Evaluate Tests and Quality Gates

Check the following.

- The presence and role of unit, integration, contract, E2E, and regression tests
- Coverage of critical success and failure paths
- Test isolation, determinism, and external dependencies
- Realism of fixtures, mocks, and test data
- Checks actually run in CI
- Steps whose failures are ignored or which do not run because of conditions
- Agreement between local and CI commands
- If coverage figures exist, their meaning and limitations

Do not treat the absence of tests as a defect by itself. Explain specifically that risky behavior lacks a validation mechanism and what impact that has.

### 5.8 Evaluate Security and Trust Boundaries

Prioritize the following.

- Where authentication and authorization are applied
- Validation and encoding of user-controlled and external input
- Possibilities for command, SQL, template, path, URL, and prompt injection
- File access and path traversal
- SSRF and external-request restrictions
- Exposure of secrets in storage, transit, logs, and build artifacts
- Deserialization and upload handling
- Session, token, cookie, and CORS configuration
- Dependency and supply-chain trust boundaries
- CI workflow permissions and pinning of external Actions
- Validation when model or automation output leads to privileged actions

Do not state an assumption as a security vulnerability unless an attack path and impact have been confirmed; classify it as an unverified risk instead.

### 5.9 Evaluate Performance and Scalability

Check the following.

- Time and space complexity per request or task
- Repeated I/O, N+1 queries, and unnecessary serial execution
- Large inputs, pagination, batching, and backpressure
- Cache keys, invalidation, and consistency
- Connection pools, queues, workers, and rate limits
- Timeouts, retries, exponential backoff, and duplicate execution
- Memory leaks and unbounded collection or log growth

If benchmarks or operational metrics are unavailable, do not state performance problems conclusively. Distinguish bottleneck candidates visible in the code from methods for validating them.

### 5.10 Evaluate Run and Deployment Readiness

Check the following.

- Required runtimes, tools, and external services
- Required and optional environment variables and their defaults
- Differences among development, test, staging, and production configurations
- Initialization, seed, migration, and rollback procedures
- Health checks, readiness, and graceful shutdown
- Logs, metrics, tracing, and alerting
- Backup, recovery, and incident-response procedures
- Container images, deployment artifacts, and files that must be included
- Operational permissions and network requirements

State when actual operating procedures are undocumented or differ from the automation.

### 5.11 Check Documentation-Code Alignment

When [00-PROJECT.md](./00-PROJECT.md), linked product and extension designs, approved change specifications, [02-TODO.md](./02-TODO.md), or a change-specific PLAN that owns detailed execution state exists, compare the following.

- Goals and current implementation
- The accepted architecture and actual dependency structure
- Items marked complete and supporting code and test evidence, including the revision or worktree to which that evidence applies
- Completion of branch implementation and validation versus completion of integration, release, and support validation for the designated target
- Duplication of detailed task and validation state between the global TODO and a change-specific PLAN
- Planned items versus already deployed implementations
- Whether rejected or deferred designs remain presented as current work
- Run and deployment documentation versus actual commands and configuration

If documentation is missing, you may propose a draft in the analysis result, but do not create files unless the user requested it.

### 5.12 Prioritize Risks and Technical Debt

Include the following information for each risk.

- Severity: Critical, High, Medium, Low
- Status: Confirmed, Inference, Unverified
- Evidence: file, symbol, configuration, or execution result
- Triggering condition
- Impact
- Recommended action
- Timing: Immediate, Before adoption, Next release, Long-term improvement

Do not inflate the list with multiple symptoms that derive from the same root cause.

### 5.13 Make an Adoption Decision

Conclude with one of the following.

- **GO:** Suitable for the current purpose with no critical prerequisites
- **CONDITIONAL GO:** Suitable after the stated prerequisites are met
- **NO-GO:** Too risky to adopt in its current state and requires structural improvements
- **INSUFFICIENT EVIDENCE:** The decision must be deferred because critical evidence is unavailable

The conclusion must include all of the following.

- Rationale for the decision
- Applicable use scope
- Required actions before adoption
- Acceptable residual risks
- Conditions for reevaluation

## 6. Rules for Analyzing Large Repositories

Do not attempt to read every file to the same depth. Allocate depth in this order.

1. Entry points, authentication and authorization, data storage, and external communication
2. Core domain logic and public APIs
3. Build, deployment, CI, and migrations
4. Tests and shared libraries
5. Examples, auxiliary scripts, and generated output

If you sample only representative files, state the sampling criteria and unreviewed areas. Do not claim to have analyzed the whole repository merely because the repository is large.

## 7. Recommended Output Format

Write the final result in English and use the following order.

### 1. Executive Summary

- Project purpose and current level of completion
- Most important strength
- Most important risk
- Final adoption decision

### 2. Analysis Scope and Validation Level

- Areas examined
- Checks performed
- Checks not performed and why
- Sampling or excluded areas

### 3. Project Overview and Core Features

- Problem, users, and primary use cases
- Distinction among implemented, partially implemented, and planned states

### 4. Technology Stack and Execution Structure

- Technologies, versions, and roles
- Build, execution, and deployment model

### 5. Architecture and Data Flow

- Major components and responsibilities
- Representative flow
- External systems and trust boundaries

### 6. Code Quality and Design

- Strengths
- Structural problems
- Major patterns and consistency

### 7. Tests, CI/CD, and Operational Readiness

- Quality gates
- Deployment and recovery capability
- Observability

### 8. Security and Performance

- Confirmed risks
- Risks requiring further validation

### 9. Risk Register

Summarize severity, status, evidence, impact, and recommended actions in a table.

### 10. Documentation-Code Alignment

- Comparison with [00-PROJECT.md](./00-PROJECT.md)
- Comparison with [02-TODO.md](./02-TODO.md)
- Comparison with README and operations documentation

### 11. GO/NO-GO Decision

- Conclusion
- Prerequisites
- Residual risks

### 12. Recommended Next Work

- Immediate work
- Short-term work
- Long-term improvements
- If necessary, proposed drafts for [00-PROJECT.md](./00-PROJECT.md) and [02-TODO.md](./02-TODO.md)

## 8. Completion Conditions

Finish the analysis when all of the following are true.

- You can explain the project's purpose and primary users
- You traced at least one execution path or major data flow
- You identified the core technologies and the role of each
- You examined test, CI, and deployment configuration
- You prioritized security, correctness, and operational risks with evidence
- You identified the major mismatches between documentation and code
- You stated the areas that could not be validated
- You provided an adoption decision and its prerequisites

If further exploration would not change the conclusion or risk priorities, finish the analysis and write the result.
