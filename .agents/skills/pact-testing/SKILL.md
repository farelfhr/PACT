---
name: pact-testing
description: Create, extend, execute, and assess PACT Security unit, integration, authorization, contract, and regression tests. Use for test coverage, fixture setup, verification semantics, and acceptance checks on an identified PACT task. Do not use for generic offensive penetration testing or unauthorized external targets.
---

# PACT Testing Skill

1. Read the repository-root `skill.md`, especially **§§1–3, §7 and §8**, plus `PRD.MD`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `todo.md`, and any relevant accepted ADRs.
2. Inspect real repository state and locate the requested `M0–M6` / `ISS` issue. If the issue or source documents cannot be found, report the blocker; never invent implementation.
3. Run **Workflow A — Testing** from `skill.md` on the user's requested scope. Form a positive/negative/error matrix and tie assertions to independently approved contracts, never to model guesses.
4. Use synthetic identities, seeded fixtures, authorized local test targets and existing project test tools. Do not execute scans against production or unrelated hosts.
5. Verify `PASS`, `VIOLATION`, `INCONCLUSIVE`, and `ERROR` accurately; 403 and 404 may both implement DENY if no protected data is disclosed and the approved profile permits it.
6. Run actual tests before claiming success. Preserve failing evidence and distinguish tests not run from passing tests.
7. Report with `skill.md` §7 handoff template. Update `todo.md` only when repository write access and sufficient evidence exist, respecting approval/review requirements.

**Example invocation:** `$pact-testing task=M1-06 scope=authorization tests focus="cross-tenant deny and invalid fixture errors"`
