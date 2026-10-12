# M6-08 — Launch/pivot decision readiness and proposed backlog

**Status: BLOCKED — owner launch/pivot decision PENDING; launch NOT READY.**
Draft v0.1, 2026-10-11. Trace: OQ-12, [PRD §§11.3, 22](../PRD.MD),
[Architecture M6-08](ARCHITECTURE.md). Author: Codex. This is a decision memo
proposal, not an accepted product direction, measured market-fit conclusion,
release approval or amendment of the PRD.

## 1. Evidence available for the decision

Repository inspection: clean `main` at intake, HEAD
`943cd681c15fe88ff1657478016216ea83da7c0c`, 64 project files and 19 directories
excluding `.git`. These are repository observations, not user or benchmark
measurements. Historical report commit references remain historical.

| Evidence sought | Actual evidence and decision limit |
|---|---|
| Implemented behavior | Typed domain, contract normalization, untrusted approval-state model, provisional scenario parser and offline fake provider exist. [Core README](../packages/pact-core/README.md) limits their authority. They do not establish a runnable approved verification journey |
| Comparative correctness, recall, false alarms, time and cost | [M6-06 report](EVALUATION_REPORT.md): evaluation/statistical analysis NOT RUN; raw trials NOT AVAILABLE, metrics NOT MEASURED, billing UNKNOWN and uncertainty NOT_ESTIMABLE. No comparative advantage or inferiority can be inferred |
| Developer usability, accessibility and deployed security | M6-07 is NOT_STARTED in the canonical ledger. No study report, observed full persona journey, accessibility results or deployment review evidence exists in the inspected repository. No satisfaction, task-completion or conformance result is inferred |
| Independent benchmark validity | M6-01 protocol unapproved/unfrozen; M6-02 corpus DISABLED pending independent review/access controls. Keys, independent personnel, tested custody and matched baseline trials are absent |
| Release safety | M1-12, M2-09, M5-16 gates remain blocked. SECURITY remains DRAFT/REVIEW REQUIRED; developer is the designated M0-02 reviewer but final sign-off is pending. No security clearance or remote CI pass established |
| Market evidence | No recorded customer demand, adoption, willingness-to-pay or retention study found in the repository. Absence of such records is not proof of lack of demand |

ADR-0001 accepts specified DSL design choices only. ADR-0002/0003/0004/0007/0009
remain PROPOSED; scoped audit-storage and ID conventions do not accept their
remaining trust decisions. Old ADR context saying no ADR is accepted is historical
or stale, not authority to reverse ADR-0001's current acceptance.

PRD §2.3 numerical targets are provisional goals, not results. Existing unit
evidence and protocol paper arithmetic are not benchmark trials. No percentages,
confidence intervals, zero spend, observed developer improvements or product-fit
claims are manufactured from missing observations.

## 2. Options and recommendation — owner decision not recorded

| Option | What would support it | Assessment from current evidence |
|---|---|---|
| Continue the current product hypothesis | A working safe P0 journey, independently evaluated correctness/cost and useful observed developer outcomes | Possible future choice; available evidence does not establish success |
| Refocus delivery on a smaller validated local workflow | Repeated observations showing a valuable local niche and excessive broader-platform burden; reviewed scope/roadmap changes | A provisional work-prioritization proposal is reasonable; a product-scope change is not justified or approved here |
| Pivot the product hypothesis | Independently reviewed failed utility/safety/economic assumptions, meaningful alternative evidence and owner decision | No measured basis currently exists; blocked prerequisites alone do not prove the hypothesis false |

**Recommendation (proposal only): prioritize gathering safe P0 vertical-slice
evidence before platform expansion or a launch/pivot conclusion.** This follows
the PRD's existing sequencing and actual missing controls; it is not a new
product positioning claim. Keep the current PRD unchanged until the owner
explicitly selects a scope change through §22 change control.

Owner decision: **PENDING**. A task prompt, this memo, an agent recommendation or
unit-test total cannot supply the required measured-data-based owner decision.
An owner may review provisional backlog priorities now; that would not close
M6-08 or approve launch, a contract, an execution target or external egress.

## 3. Prioritized backlog proposal using existing task IDs

Order expresses dependencies and evidence needs, not permission to start tasks.
No duplicate work items or future schedule, cost or staff availability is assumed.

| Priority | Existing tasks / proposed responsible role | Evidence required to advance |
|---|---|---|
| 1 — unblock foundations | M0-02/04/05/06/07; developer/security reviewer and tooling owner | Final scoped threat review; fixture/approval/tooling decisions resolved; accepted tooling, reproducible lock/install and actual CI evidence. Retain existing review requests; no repeated acceptance of unchanged choices |
| 2 — prove local deterministic verification | M1-04..12; fixture/runner/evidence owners | Real synthetic demo, separate sessions, safe scope transport and assertions; vulnerable VIOLATION, fixed PASS, valid 404 denial, ALLOW500/auth/fixture/network failures non-PASS; redaction, immutable history and compatible comparison. Provisional parser does not waive dependencies |
| 3 — prove trusted human intent | M2-02..09; human-review/security/intent owners | Safe context and draft/ambiguity handling, genuine hash-bound human approval, protected audit continuity and offline rerun; forgery/replay/tampering/egress denials. Audit Authority direction remains selected; identity/presence and implementation verification remain open |
| 4 — prove usable local interfaces | M3-01..08 and minimal P0 M4 comparison/policy-change proof; interface owners | Actual CLI/MCP parity, offline export/install and retained failed evidence; all mandatory P0 ACs proven. Extended temporal work remains behind its dependencies |
| 5 — prepare independent evaluation | M6-01..05; evaluation owners and independent key reviewers | Owner-approved preregistration before tuning; reviewed independent families, protected held-out custody, matched manual/Codex/tool profiles and actual baseline trials. Held-out stays DISABLED; external tool profile stays PLANNED/UNCONFIGURED |
| 6 — obtain measured analysis | M6-06; evaluation owner | Redacted raw assignments/attempts, failures and abstentions, denominator/cost/setup provenance, reproducibility and defensible uncertainty under frozen methodology |
| 7 — obtain deployed human/security evidence | M5-01..16 then M6-07; platform operator, persona participant and scoped reviewers | Actual accepted hosted controls and authorized disposable setup, followed by full persona observations, manual/automated accessibility review and security triage. Staging stays DISABLED until the owner’s existing prerequisites and future concrete activation proposal are satisfied |
| 8 — make product decision | M6-08; actual project owner | Review measured M6-06 and M6-07 evidence, residual risks and alternatives; record dated continue/refocus/pivot decision with its supporting measurements and limits; amend PRD/roadmap only if scope changes |

Roles are proposed responsibility categories, not appointments. Backlog item 5
can include safe planning already authorized by the owner; it cannot activate
the held-out corpus or bypass any unfinished task.

## 4. Gates, limitations and conditional decision checks

Hosted staging remains **DISABLED — PENDING PREREQUISITES** (EV-0052). Held-out
corpus remains owner **DISABLED** (EV-0056). External benchmark profile remains
**PLANNED / UNCONFIGURED**, requests/data transmission DISABLED/NONE and external
time/cost budgets ZERO (EV-0062). Budgets are prohibitions, not measured results.
No provisioning, deployment, target request, model/provider call, paid tool use,
participant contact or public publication is performed for this memo.

| Conditional review check | Positive evidence needed | Adverse case that prevents acceptance | Execution |
|---|---|---|---|
| LP-01 measurement integrity | Independently adjudicated, pinned raw observations and traceable denominators | Missing data, toy/unit totals substituted for trials, selective omissions or unreviewed keys | NOT RUN |
| LP-02 safety and release | Actual mandatory acceptance/review evidence, triaged critical/high findings and scoped release decision | Forged approval, unsafe execution, leakage, unresolved critical/high issue or missing tests | NOT RUN |
| LP-03 usability/accessibility | At least one appropriate persona completing actual setup; privacy-consented observations and meaningful status/keyboard/label checks | Agent-simulated participant, absent deployment, color-only status or non-PASS presented as safe | NOT RUN |
| LP-04 owner authority/change control | Dated real owner decision citing measurements; approved PRD/roadmap diff if scope changes | Agent self-acceptance, a planning acknowledgment called launch approval or silent scope amendment | NOT RUN |

These are future decision checks, not executed benchmark, accessibility or
security tests. Documentation checks recorded in [todo.md EV-0063](../todo.md)
only verify memo/tracker coherence and preservation.

Public-facing limitations must remain explicit before any future publication:
there is no validated full local or hosted workflow, independent accuracy or
superiority result, observed persona study, WCAG conformance determination or
release security clearance. Repository coverage is partial. No universal
security or demonstrated product-market fit follows from current artifacts.

## 5. DoD and owner handoff

Exact Architecture DoD: **Owner documents continue/refocus/pivot decision grounded
in measurements; roadmap and PRD updated if product scope changes.** It is unmet:
M6-06 is BLOCKED without measurements and M6-07 is NOT_STARTED without its review
deliverables. M6-08 is **BLOCKED / BLK-0049**, not DONE. This draft supplies a memo
and prioritized proposal only; PRD and architecture scope remain unchanged.

New owner input may concern this proposed backlog ordering or specific changes
to the memo. Existing unchanged security/benchmark/staging/profile decisions
are not reopened. A final launch/pivot request requires actual prerequisite
evidence first. There is no next eligible successor ID in the canonical WBS;
resume existing blocked work only after its specific gates are resolved. No
next task is started in this session.
