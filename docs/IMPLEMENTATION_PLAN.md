# PACT completion plan — 71 canonical tasks

> **Version / date:** 0.1 / 2026-10-12
> **Authority:** Owner's direct “PLEASE IMPLEMENT THIS PLAN” instruction in the current chat.
> **Baseline:** `a000fe5cd47284c81ccceb0b4f08c38ff45ac070`; 9 DONE, 4 IN_REVIEW, 40 BLOCKED, 18 NOT_STARTED.
> **Live status:** [todo.md](../todo.md). This plan does not replace the ledger, architecture DoDs, or genuine approvals.

## 1. Delivery agreement

Execute small, dependency-checked waves with a chat checkpoint and local commit after verification. Use a `codex/` branch; push and remote CI require separately reviewed authorization. Keep PACT private until mandatory P0 acceptance is proven; publication licensing remains open. No completion date is promised before installation, review capacity, and feasibility are measured.

The owner selected Windows/Linux × standard CPython 3.12/3.13/3.14, future GitHub Actions for the six cells, and a separate local approval broker. The first human-review candidate is a browser on a separate device, HTTPS over restricted LAN, and a device-bound passkey. The owner will perform reviewed administrative steps. Begin hosted delivery with a private pilot. These are planning directions, not evidence of isolation or permission to enroll devices, provision accounts, change privileges, or activate product approval.

Preserve accepted DSL, typed ID/job-run conventions, tooling design, threat-model assumptions, fixture/runner design, Dedicated Audit Authority/checkpoint direction, and backlog priorities. [DECISIONS.md](DECISIONS.md) binds the accepted foundation snapshots. Do not request unchanged decisions again. M0-05 remains IN_REVIEW and REGISTRY_DISABLED; staging and held-out corpus remain DISABLED; the external benchmark profile remains PLANNED/UNCONFIGURED.

## 2. Existing completed work and gaps

The nine baseline DONE tasks are **M0-01, M0-02, M0-03, M0-04, M0-06, M1-01, M1-02, M1-03, M2-01**. Preserve their evidence and approved semantics. Their completion does not prove an integrated product.

Actual code comprises stdlib domain entities, contract schema/normalization, an untrusted approval-state model, provisional scenario parser, provider port/fake, and component tests. At intake there is no pyproject.toml, lock, CI, demo, executor, authentic fixture/session adapter, protected review authority, CLI/MCP, or hosted implementation. M1-02's Pydantic adapter was explicitly deferred; adding it is a bounded compatibility follow-up, not reopening canonical hash rules.

The two existing untracked files `LOCAL_APPROVAL_FEASIBILITY.md` and `LAUNCH_PIVOT_REVIEW.md` remain unchanged and excluded from this wave's commit. A proposed document or test plan is not executed evidence.

## 3. All remaining work, by wave

The 62 remaining canonical IDs are covered below. M0-07 appears in two phases of the same task; do not create another WBS row or count preparation as DONE. Each row remains conditional on its actual [Architecture §7](ARCHITECTURE.md#7-detailed-implementation-work-breakdown-wbs) dependencies and all relevant security gates.

| Wave | WBS scope | Deliverable and exit evidence | Gate before dependent implementation |
|---|---|---|---|
| 1 | M0-07 preparation | Exact bootstrap pins, primary metadata, artifact/hash/license review, offline/build strategy and concrete acquisition proposal | Owner decision before distribution download; this packet is [BOOTSTRAP_REVIEW.md](BOOTSTRAP_REVIEW.md), not a workspace |
| 2 | M0-07 workspace | Core member, shared lock, isolated install, pytest/Ruff/mypy, build constraints, smoke and CI skeleton; stale-lock/cache/hash negatives | Artifact inspection/acquisition and installation scope; real local and CI smoke before DONE |
| 3 | M0-05 | Browser/broker identity, enrollment, trusted display/challenge, principal separation, audit/anchor/recovery; synthetic feasibility evidence | Concrete OS/device lab proposal and full mechanism review; unsupported profile disabled |
| 4 | M0-08, M0-09 | Final AC coverage/release blockers and domain/wire/API boundaries; schema.md historical relationship retained | Prerequisites and outstanding document reviews; accepted IDs/job semantics retained |
| 5 | M1-04, M1-05, M1-06 | Synthetic FastAPI vulnerable/fixed target; deterministic seed, declared parser bindings, independent A/B sessions and cleanup | Demo dependency acquisition and explicit synthetic execution profile; fixture/auth failures and contamination tested |
| 6 | M1-07, M1-08 | Allowlist/path/destination guards, bounded HTTPX transport, cancellation and deterministic ALLOW/DENY assertions | Start with simulated/in-process transport; actual socket/OS/peer/cleanup profile needs concrete evidence and scope |
| 7 | M1-09, M1-10, M1-11 | One redacted outcome model, JSON/HTML, immutable SQLite run/events/artifacts, checksums and compatible-run matching | Preserve failed evidence; changed policy/environment is NOT_COMPARABLE; no trusted approval fabricated |
| 8 | M1-12 | Offline golden/negative/property gate for AC-004–008, 011, 015–017 | Authorized synthetic harness; zero provider calls and no unauthorized outbound; critical failure blocks advancement |
| 9 | M2-02, M2-03, M2-04, M2-05 | Scoped reader/provenance/privacy, opt-in OpenAI adapter, candidate generation and ambiguity questions | SDK reviewed separately; mocks first, egress OFF; output DRAFT or NEEDS_REVIEW |
| 10 | M2-06, M2-07 | Genuine human approval and protected immutable registry; durable audit event and independent anchor before activation | M0-05 acceptance and protected identity/presence/custody; real human positive plus forged/replay/stale/revoked/anchor negatives |
| 11 | M2-08, M2-09 | Credential-free offline rerun and security/conformance review | Approved fixture/suite and AC-001/002/003/010/013 evidence; ambiguity never starts execution |
| 12 | M3-01, M3-02, M3-03, M3-04, M3-05, M3-06, M3-07, M3-08 | Shared-service CLI/MCP, Skill, parity, portable export, installation/runbook | SDK/interface review; no agent approval tool; genuine approved journey and fresh-install evidence |
| 13 | M4-01, M4-02, M4-03, M4-04, M4-05, M4-06, M4-07, M4-08, M4-09 | Compatibility fingerprints, drill-down drift, new draft/reapproval, temporal DSL/fixtures/corpus, impact/remediation and runtime report | Human owns changed policy/patch approval; preserve historical failures; advanced P1 scope follows its gate |
| 14 | M5-01, M5-02, M5-03, M5-04, M5-05 | Accepted hosted trust design, PostgreSQL/migrations, OIDC/RBAC/RLS, API and private artifact retention | P0 gates, concrete backend/identity/residency/custody; disposable DB and recovery/isolation evidence |
| 15 | M5-06, M5-07, M5-08 | Durable jobs/leases/fencing/crash recovery, scoped runner credentials and sandbox | Actual revoked/foreign job, mount/socket/network/write/exfiltration/budget/cleanup tests |
| 16 | M5-09, M5-10, M5-11, M5-12, M5-13, M5-14, M5-15 | Accessible authenticated UI, review/history/evidence, GitHub, optional merge gate, extra providers and quotas/telemetry | Local/mock integrations first; real GitHub/provider/services and repository protection separately authorized |
| 17 | M5-16 | Hosted E2E/runbook and J-01–05/security clearance | Staging DISABLED until concrete disposable profile/operator/targets/limits/cleanup approved; no critical/high release blockers |
| 18 | M6-01, M6-02 | Owner-approved preregistered protocol; independent reviewed corpus and protected custody | After M4-09; freeze before tuning; author/reviewer/access separation required before holdout activation |
| 19 | M6-03, M6-04, M6-05, M6-06 | Manual/Codex/tool baselines and PACT evaluation; redacted raw data, uncertainty/errors/cost/setup | Accepted protocol/corpus and actual bounded baseline profiles; fair capability scope; unauthorized tools NOT RUN |
| 20 | M6-07, M6-08 | Observed persona flow, accessibility/security triage and measured continue/refocus/pivot memo | Actual setup/participant/reviewer and measurements; only owner accepts product decision |

This is an execution route, not a dependency waiver. For example, M0-08/09 still depend on approval-design closure; M5/M6 cannot become eligible merely because their row is later in the table. Safe independent documentation may be prepared while a gate is pending, without freezing security-critical implementation.

## 4. Boundaries and decision packets

Keep domain stdlib, canonical hash/normalization, conservative possible-conflict rejection, and accepted schema/version behavior intact. Boundary Pydantic must preserve strict types and hashes; no coercion into a changed contract. Providers remain behind `generate_structured_contract`; deterministic verifier must not call SDKs. Add explicit fixture/session, scoped transport, evidence/storage and trusted-lookup ports as their tasks require them. CLI/MCP/API call shared services and review schema/error/exit/idempotency compatibility before freezing interfaces.

Current approval models and imported receipts remain untrusted. Proposed browser path: immutable draft → authenticated reviewer/trusted display → exact hash/version/scope challenge → fresh user verification → pending audit event → independently retained signed checkpoint → current eligibility/anchor recheck → activation. Agent-controlled terminals, APPROVED JSON, hashes or automatable button clicks cannot establish human authority. Device-bound validation must consider backup eligibility, not merely current backup state; unsupported devices have no silent synced-passkey/terminal fallback. [WebAuthn specification](https://www.w3.org/TR/webauthn-3/).

Concrete decision packets must contain version/digest, exact candidate/alternatives, diagram/data flow, risks, positive/negative/failure checks, limits, rollback, required operator actions and task-closure effects:

1. Bootstrap artifacts/licenses/acquisition, then actual installation and separate CI upload/run scope.
2. Broker device/OS lab, enrollment/revocation, TLS/RP origin, protected custody and audit/freshness/recovery protocol.
3. Runner OS/transport/cleanup envelope and exact synthetic execution scope.
4. MCP/provider boundaries and interface compatibility.
5. Hosted identity/backend/residency/retention/runner architecture.
6. Benchmark protocol, independent reviewer/custody, baseline profiles and participant consent.
7. Concrete staging activation and eventual release/launch decision.

Final pins and third-party binary acquisition remain pending. A review decision on this roadmap does not approve these packets. Do not repeat accepted unchanged choices. Ask only when the next concrete gated operation is ready for review.

## 5. Required checks and checkpoint contract

For each increment: inspect actual ledger/Git/dependencies, claim one scope, specify positive/negative/boundary/failure/security cases, implement minimum behavior, run focused then affected checks, review diff/redaction/permissions/cleanup/compatibility, record exact commands/results/NOT RUN, recount ledger/board, then commit locally. Preserve independent review findings and failure evidence. Rollback uses the prior verified source/lock configuration without rewriting immutable contracts/results.

Mandatory check families include schema/canonicalization/conflicts; fixture/session/cleanup; vulnerable vs patched outcomes and valid 403/404 vs ALLOW 500; scope/redirect/DNS/peer/budgets; malicious DSL/source; approval forgery/replay/expiration/revocation/audit rollback; secret canaries; immutable history and compatible comparison; retry/cancel/parity/export; hosted RLS/migrations/runner/retention/webhooks/quotas/a11y; and independent/fair reproducible benchmark conditions.

Mock checks prove modeled behavior only. They do not substitute for operating-system isolation, genuine human interaction, remote CI, hosted E2E, or independent benchmark evidence. No mandatory P0 AC failure, approval/scope bypass, leak or unproven regression validity may be presented as completed release.

Chat checkpoint format: **completed ID/scope → actual evidence → progress count → blocker/new owner decision → next conditional wave**. DONE requires actual task DoD and required review. Milestone gates are read-only reassessments; no universal security or measured superiority claims.

## 6. First checkpoint

Wave 1 creates review documentation/data only; M0-07 workspace DoD is unmet. See [bootstrap packet](BOOTSTRAP_REVIEW.md), [artifact candidates](bootstrap-artifacts.json) and todo EV-0068 for actual checks and the specific next owner decision. Later waves have not been executed by recording this plan.
