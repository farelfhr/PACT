---
name: pact-refactor
description: Safely refactor PACT Security implementation with behavior preservation, characterization tests, clean module boundaries, and explicit compatibility checks. Use for code cleanup, extracting pure domain logic, dependency inversion, type safety, and reducing duplication without changing approved security contract semantics.
---

# PACT Refactor Skill

1. Read repository-root `skill.md`, especially **§§1–2, §5, §7 and §8**, plus `PRD.MD`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `todo.md`, and relevant accepted ADRs.
2. Inspect actual source, callers, saved formats, tests, and Git status. Confirm scope and specific maintainability problem. Default to **`behavior=preserve`**.
3. Execute **Workflow C — Refactor** in `skill.md`. Capture current behavior with characterization tests, including authorization-negative and infrastructure-error outcomes.
4. Keep contract rules, approval provenance, verification verdicts, target scope, historical evidence and versioned public interfaces unchanged unless explicitly approved with a migration plan/ADR.
5. Apply bounded changes that preserve separation between domain, adapters, AI provider, MCP/CLI, and runner. Never weaken tests to hide failures.
6. Run targeted checks and relevant regression tests. Use identical fixture/contract versions for before/after comparison; report any skipped verification.
7. Produce the §7 handoff and update `todo.md` accurately if writable; incomplete verification remains `IN_REVIEW` or `BLOCKED`, not DONE.

**Example invocation:** `$pact-refactor task=M1-11 scope=packages/pact_core/verification.py goal="extract pure assertions" behavior=preserve`
