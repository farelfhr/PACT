---
name: pact-security-review
description: Perform scoped defensive security review of PACT Security source code, MCP tools, test runner isolation, approval handling, provider egress, evidence, and cross-tenant access. Use when reviewing changes or threat models for concrete security risks. Default to review-only; not for unauthorized pentesting.
---

# PACT Security Review Skill

1. Read repository-root `skill.md`, especially **§§1–2, §4, §7 and §8**, and the current `PRD.MD`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `todo.md`, and applicable accepted ADRs.
2. Inspect the actual diff, module boundaries, callers, and data flows. Confirm owner-requested scope. Start in **`mode=review-only`** unless explicit authorization says otherwise.
3. Follow **Workflow B — Security Review** in `skill.md`. Prioritize contract authority/approval forgery, scope validation/SSRF, runner isolation, cross-tenant access, evidence integrity, credentials, and AI egress.
4. Provide accurate file:line references and classify each finding `Confirmed`, `Code-supported`, or `Hypothesis`; never call an untested suspicion a confirmed exploit.
5. Run only authorized, non-destructive validation against local/synthetic fixtures. Stop and request real approval for expanding targets, changing production security controls, contract rules, or executing higher-risk actions.
6. Rank grounded findings by impact and give safe remediations and negative regression tests. Note what was not inspected.
7. Use `skill.md` §7 report format; update `todo.md` with evidence only when permitted. A review does not itself approve a policy or remediate findings.

**Example invocation:** `$pact-security-review task=M0-02 scope=docs/SECURITY.md area="runner trust boundaries" mode=review-only`
