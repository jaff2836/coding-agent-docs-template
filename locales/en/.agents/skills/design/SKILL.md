---
name: design
description: Design changes involving structure, the technology stack, public contracts, schemas, migrations, or trade-offs between alternatives, as well as feature changes whose requirements are ambiguous or whose intent must be preserved across sessions. Confirm Intent → define the Spec, alternatives, and design → create an execution plan → reach user agreement. Use minimal documentation for small changes, and do not repeat the full procedure when implementing an approved design. Apply when explicitly invoked.
argument-hint: "[change summary]"
---

# Design
<!-- template-skill-contract:design:v1 -->

1. Check the applicability criteria in [docs/01-DESIGN.md](../../../docs/01-DESIGN.md) §1. If the change does not require the full procedure, review only the relevant parent design and necessary execution plan, then carry out the request.
2. If it does, select the minimum deliverable format in §2 and proceed with §3. Use [docs/00-PROJECT.md](../../../docs/00-PROJECT.md) and its linked product and extension designs for context, and [docs/REVIEW.md](../../../docs/REVIEW.md) §6 for invariants.
3. Do not implement before agreement. Proceed without renewed approval for a scope already approved in the existing conversation. Connect the intent, specification, and decision rationale to [docs/02-TODO.md](../../../docs/02-TODO.md) as described in §4.
4. When a change-specific PLAN exists, record detailed task and validation status only there. Do not rewrite INTENT or SPEC while implementing an approved stage, and do not require all three files for every change.

This file is an adapter. `docs/01-DESIGN.md` is canonical for the procedure and document lifecycle, while [docs/DOCS_GUIDE.md](../../../docs/DOCS_GUIDE.md) is canonical for ownership and branch operations.
