# PACT Security — Project Progress Tracker & Local Issue Memory

> **Canonical path:** `todo.md` (repository root)  
> **Created:** 2026-10-10  
> **Tracker version:** 1.0.0  
> **Current state:** `DOCS-ONLY / M0-01 VERIFIED; PRODUCT NOT IMPLEMENTED`  
> **Owner:** Unassigned; project owner to allocate contributors  
> **Authority:** This is the **operational status ledger**, not a replacement for product requirements, accepted ADRs, or test evidence.

## 0. How Codex / Any AI Agent MUST Use This File

**Read every coding session, before editing:** `PRD.MD` → `AGENTS.md` → `docs/ARCHITECTURE.md` → **`todo.md`** → relevant accepted ADRs → actual Git state. If repo facts contradict this tracker, **investigate and correct the tracker with evidence**, never fake repository state.

1. Locate an issue/task by its stable ID (`M0-01` … `M6-08`, or `ISS-0001` …). Do not introduce duplicate work items with new IDs.
2. Check task dependencies and any required **human-accepted ADR**; do not implement security-critical semantics solely from draft proposals.
3. Claim **one bounded task**: change `NOT_STARTED` → `IN_PROGRESS`, fill `Owner`, `Last updated` and the active session log. Multiple agents may own separate tasks but must coordinate files and interfaces.
4. Record code paths, PRD/AC IDs, expected failure cases, tests to run, and security boundary before making changes; put detailed design in ADR/PR rather than bloating this tracker.
5. If blocked, use `BLOCKED`, record the **specific unblock condition** in Blocker Register, and stop unauthorized activity; never convert an unapproved action into a background assumption.
6. After code changes, run appropriate actual checks, preserve negative/security test output, and record command results with commit/PR/file paths in the **Evidence Log**. Do not mark a task DONE when checks have not run or an approval is missing.
7. Use `IN_REVIEW` for completed work awaiting validation/approval. Mark `DONE` only when the architecture task's concrete **Done when** statement is supported by accessible evidence and required review is complete.
8. At the end of **every session**, update the task row(s), milestone summary, Current Focus, Open Issues/Blockers and Session Journal with exact facts and next task. Never claim unseen results.
9. Preserve historical log entries and immutable evidence. If work regresses, reopen the task with an explicit explanation; do **not** erase past DONE/evidence events.
10. Do not let this document become a security authorization token. Task status `DONE` or a written approval note in Markdown **does not** authorize running tests, approving contracts, sending data to an LLM, or changing production policy.

**Status vocabulary — synchronized with `docs/ARCHITECTURE.md` §7:**

| Status | Meaning | Entry / exit rule |
|---|---|---|
| `NOT_STARTED` | Planned, no verified task execution yet | Default on creation; can be selected when prerequisites are satisfied |
| `IN_PROGRESS` | Someone is actively working on it | Must have owner, scope and journal entry |
| `BLOCKED` | Stopped by a concrete unmet prerequisite or decision | Blocker ID, unblock condition and next responsible person required |
| `IN_REVIEW` | Work exists, review/tests/evidence gate pending | Include artifact paths, tests, reviewer, unresolved checks |
| `DONE` | Exact work-item DoD and required reviews genuinely met | Verified evidence log + dates + PRD/AC trace required |
| `DEFERRED` | Intentionally postponed by owner | Record rationale, approver and revisit trigger; not counted as done |

**Transitions:** `NOT_STARTED → IN_PROGRESS → IN_REVIEW → DONE`; `IN_PROGRESS/IN_REVIEW → BLOCKED`; `BLOCKED → IN_PROGRESS` after documented resolution; `DONE → IN_PROGRESS` only with explicit reopening event; `NOT_STARTED → DEFERRED` when authorized. Never jump directly from `NOT_STARTED` to `DONE` without logging executed work and verification.

## 1. Current Verified Snapshot

**Snapshot date:** 2026-10-10. M0-01 inspected the actual filesystem and Git state. The 71-item plan still derives from `docs/ARCHITECTURE.md` v1.0.0; documentation checks are not product execution or security evidence.

- **Documents verified on disk:** `PRD.MD`, `AGENTS.md`, `workflow.md`, `skill.md`, this tracker, `docs/ARCHITECTURE.md`, `docs/SECURITY.md`, `docs/schema.md`, and three `.agents/skills/*/SKILL.md` manifests. M0-01 added [docs/REPOSITORY_INVENTORY.md](docs/REPOSITORY_INVENTORY.md); the draft design documents remain unapproved.
- **Actual application repository/code status:** **INSPECTED — DOCS ONLY**. Initial tree: 11 Markdown files and six directories excluding the root; current tree: 12 Markdown files and the same directories. Git is **not initialized**. No source packages, tests, build configuration, migrations, CI workflows, demo application or PACT MCP implementation exist in this workspace.
- **Product baseline:** Proposed; security contract approval, authorized runner, and verified outcome are **not yet implemented/validated**.
- **Completed task:** `M0-01` — verified documentation inventory, reconciliation, gap list and pending decision register (`EV-0001`). `M0-02` claimed for a bounded documentation review; no other task started.
- **Critical decisions pending:** ADR-0001 (contract DSL), ADR-0002 (fixtures/runner/denial semantics), ADR-0003 (human approval); none is represented as Accepted.
- **Task count:** **1/71 DONE**; 69 `NOT_STARTED`; 0 `BLOCKED`, 1 `IN_PROGRESS`, 0 `IN_REVIEW`, 0 `DEFERRED`. Only M0-01 documentation work is complete; the initial all-NOT_STARTED state remains in the initialization journal.
- **P0 gate:** Not met. **P1 and launch gates:** Not met. No tests are claimed to have run.

### 1.1 Milestone completion board

| Milestone | Priority / focus | Total | `NOT_STARTED` | `IN_PROGRESS` | `BLOCKED` | `IN_REVIEW` | `DONE` | `DEFERRED` | Progress |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **M0** | P0 · architecture/security foundations | 9 | 7 | 1 | 0 | 0 | 1 | 0 | **1/9 (11.1%)** |
| **M1** | P0 · deterministic verification core | 12 | 12 | 0 | 0 | 0 | 0 | 0 | **0/12 (0%)** |
| **M2** | P0 · AI drafting + trusted approval | 9 | 9 | 0 | 0 | 0 | 0 | 0 | **0/9 (0%)** |
| **M3** | P0 · CLI, MCP, Codex Skill | 8 | 8 | 0 | 0 | 0 | 0 | 0 | **0/8 (0%)** |
| **M4** | P0/P1 · drift and permission lifecycle | 9 | 9 | 0 | 0 | 0 | 0 | 0 | **0/9 (0%)** |
| **M5** | P1 · hosted platform, runners, web, CI | 16 | 16 | 0 | 0 | 0 | 0 | 0 | **0/16 (0%)** |
| **M6** | P1/P2 · evidence-based benchmark and launch decision | 8 | 8 | 0 | 0 | 0 | 0 | 0 | **0/8 (0%)** |
| **TOTAL** | | **71** | **69** | **1** | **0** | **0** | **1** | **0** | **1/71 (1.4%)** |

> **Maintenance rule:** The board is manually updated from the task ledger after every session; verify the counts instead of assuming a cached number is correct. Never mark a milestone `DONE` if any mandatory task/release criterion is unresolved. M4 contains both early P0 comparable-run requirements and later P1 lifecycle work: refer to PRD acceptance gates for release scope.

## 2. Current Focus and Handoff

| Field | Current value |
|---|---|
| Active work item | `M0-02 IN_PROGRESS` — Codex / threat-model review / 2026-10-10 |
| Next task | M0-03 recommended; M0-06 also dependency-ready. Neither started. |
| Suggested owner | Codex for documentation; developer (repository owner) designated themselves security reviewer in the current conversation; sign-off pending |
| Immediate prerequisites | M0-01 DONE (`EV-0001`); no accepted ADRs or implementation exist; drafting is allowed, privileged decisions remain gated |
| Success evidence | Existing assets/TH/TB review, six attacker paths, NFR-SEC-001–005 trace, local document checks and exact artifact digest; human boundary sign-off required |
| Must not do yet | Mark ADRs accepted; approve contracts; execute third-party/production tests; claim CLI/MCP/runner functionality |
| Next handoff after task | Request genuine review of the exact M0-02 document; await a separate prompt for any next task. ADRs and runtime grants remain unapproved. |

**Session-start script for Codex (guidance, not an existing command):**

```text
Read PRD.MD, AGENTS.md, docs/ARCHITECTURE.md and todo.md.
Inspect git status and filesystem; don't assume any feature exists.
Pick M0-01, check prerequisites, mark IN_PROGRESS with owner/date.
Perform ONLY its acceptance scope; record evidence and update todo.md.
Show tests performed, remaining decisions and the next unblocked work item.
Do not claim DONE without proof or self-approve an ADR.
```

## 3. Implementation Task Ledger — 71 Canonical Issues

**Source:** `docs/ARCHITECTURE.md` §7. IDs, dependency descriptions, expected deliverables, criteria and PRD traces are transcribed from that document. **DoD** means the work item is closable when its acceptance evidence is verified. This ledger starts with zero completed work items, regardless of existing plans/document drafts.

**Table conventions:** `Owner: —` means unassigned; `Evidence: —` means no completion proof is recorded. Dependencies must be checked against actual DONE tasks and approved ADRs before implementation. Descriptions such as `M1-05..11` or `M0-02/03` use the shorthand from the architecture document and include each referenced task.

### M0 — Architecture, security and repository foundations (P0)

| Task ID | Work item / deliverable | Dependencies | Status | Owner | DoD / required proof | Evidence / last updated |
|---|---|---|---|---|---|---|
| `M0-01` | **Inventory repository and reconcile docs**<br>Deliverable: Repository inventory, gaps list, decision register<br>Trace: PRD §§0,14,17 | — | `DONE` | Codex / M0-01 inventory session | Actual paths checked; discrepancies against PRD/AGENTS recorded; no invented implementation claims | `EV-0001`; [inventory](docs/REPOSITORY_INVENTORY.md); 2026-10-10 — local checks and document review satisfy documentation-only DoD; no ADR/runtime approval implied |
| `M0-02` | **Define core threat model**<br>Deliverable: `docs/SECURITY.md` initial assets, attacker paths, trust diagram<br>Trace: NFR-SEC-001–005 | M0-01 | `IN_PROGRESS` | Codex / M0-02 threat-model review | Covers injection, forged review, SSRF, runner escape, leaked evidence, tenant IDOR; reviewer signs off threat boundary before privileged code | 2026-10-10 — developer designated themselves reviewer; no sign-off yet; only docs/SECURITY.md and todo.md allowed |
| `M0-03` | **Draft contract and policy DSL ADR**<br>Deliverable: `docs/adr/0001-contract-dsl.md` + valid/invalid examples<br>Trace: OQ-02, FR-AUT-001/002 | M0-01 | `NOT_STARTED` | — | Includes typed relations, ALLOW/DENY, versioning and denial profiles; JSON parsing rejects executable expressions; approval requested | — |
| `M0-04` | **Draft fixture/runner ADR**<br>Deliverable: `docs/adr/0002-fixture-runner.md`<br>Trace: OQ-03/06, FR-TST-002 | M0-02 | `NOT_STARTED` | — | Defines synthetic actors, safe test target, auth setup, teardown, 404 semantics, redirects and budgets; examples include negative paths | — |
| `M0-05` | **Draft human approval ADR**<br>Deliverable: `docs/adr/0003-human-approval.md`<br>Trace: OQ-04/14, FR-CON-001/002 | M0-02/03 | `NOT_STARTED` | — | Identity, exact hash, local review action, immutable history, untrusted import behavior and replay rejection documented; owner approval requested | — |
| `M0-06` | **Decide tooling and dependency boundaries**<br>Deliverable: ADR + proposed lock/build strategy<br>Trace: NFR-MAINT-001 | M0-01 | `NOT_STARTED` | — | Python/OS matrix, SDK licensing/versions, pinning, test commands and package ownership described; unresolved alternatives visible | — |
| `M0-07` | **Set up workspace baseline**<br>Deliverable: `pyproject.toml`, minimal importable packages, CI skeleton and lint/type/test config<br>Trace: FR-PLT-001, NFR-MAINT-001 | M0-06 | `NOT_STARTED` | — | Clean checkout installs from lock; one smoke test runs locally and in CI; import causes no side effects; no `.env` secret committed | — |
| `M0-08` | **Define traceability/test plan**<br>Deliverable: `docs/TEST_PLAN.md` + requirements/AC matrix<br>Trace: PRD §11 | M0-03/04/05 | `NOT_STARTED` | — | AC-001..017 each has planned test owner/fixture; `AC-014` correctly flagged P1; owner can identify release blocker | — |
| `M0-09` | **Specify initial data model and public interface boundaries**<br>Deliverable: Draft `docs/DATA_MODEL.md`, `docs/API_SPEC.md`<br>Trace: PRD §§7,9,13 | M0-03/05 | `NOT_STARTED` | — | Names/semantics of contract, review, fixture, run, artifact and job IDs aligned; endpoints marked PROPOSED | — |

### M1 — Deterministic verification core (P0)

| Task ID | Work item / deliverable | Dependencies | Status | Owner | DoD / required proof | Evidence / last updated |
|---|---|---|---|---|---|---|
| `M1-01` | **Define typed domain**<br>Deliverable: Enums/entities for actor, tenant, resource, relation, rule and verdict<br>Trace: FR-AUT-001/002 | M0-03 | `NOT_STARTED` | — | Schema tests cover valid roles/tenants and reject unknown predicates, extra privileged fields and missing expected action | — |
| `M1-02` | **Canonical contract schema and normalizer**<br>Deliverable: Versioned Pydantic/JSON Schema + fixtures<br>Trace: FR-CON-001, FR-INT-002 | M1-01 | `NOT_STARTED` | — | Identical logical contracts hash identically under documented canonicalization; malformed/ambiguous contracts rejected; examples round-trip | — |
| `M1-03` | **Approval state-machine model (without fake trusted approval)**<br>Deliverable: Transition guards, immutable approved snapshot interface<br>Trace: FR-CON-001/002, AC-002 | M1-02 | `NOT_STARTED` | — | Invalid transitions and modifying approved content fail tests; no untrusted JSON `APPROVED` bypass | — |
| `M1-04` | **Seed local marketplace demo**<br>Deliverable: Deterministic FastAPI app with seller A/B, order A/B, intentionally flawed vs fixed authorization variants<br>Trace: FR-PLT-001, FR-TST-002 | M0-04 | `NOT_STARTED` | — | Repeated seeding reproduces resource ownership; independent identities isolated; both allow and deny examples exercised | — |
| `M1-05` | **Restricted scenario DSL parser**<br>Deliverable: Typed `fixture.setup`, `http.request`, assertions, teardown schema<br>Trace: FR-TST-001/003, NFR-SEC-004 | M1-01/04 | `NOT_STARTED` | — | Rejects arbitrary shell/Python/host interpolation; allows only typed references and declared paths; fuzz/negative tests pass | — |
| `M1-06` | **Fixture/session adapter**<br>Deliverable: Safe seeded fixture registry and independent auth sessions<br>Trace: FR-TST-002, AC-006 | M1-04/05 | `NOT_STARTED` | — | Actor A/B tokens genuinely distinct; invalid auth setup -> ERROR; each run restores baseline with cleanup evidence | — |
| `M1-07` | **Scope guard and request-budget policy**<br>Deliverable: Strict target allowlist, destination/redirect checks, budget enforcing transport<br>Trace: NFR-SEC-001/005, AC-007/015 | M0-04/M1-05 | `NOT_STARTED` | — | Disallowed external URL, redirect, DNS/IP swap and unsafe path blocked **before** unapproved request; limits yield non-PASS outcome | — |
| `M1-08` | **HTTP executor and authorization assertions**<br>Deliverable: Bounded HTTPX runner and `ALLOW`/`DENY` evaluation<br>Trace: FR-TST-004/005/006, AC-004/005/016/017 | M1-05/06/07 | `NOT_STARTED` | — | Vulnerable demo yields evidence-backed VIOLATION; patched yields PASS; valid 404-denial can PASS; expected ALLOW with 500 not PASS | — |
| `M1-09` | **Evidence redaction + serializers**<br>Deliverable: Normalized run model, JSON + HTML report, token scrubbers<br>Trace: FR-EVD-001/002/003/005, AC-011 | M1-08 | `NOT_STARTED` | — | Seeded API keys/bearer tokens/private fixture fields absent from logs, HTML, JSON and exceptions; same result is rendered consistently | — |
| `M1-10` | **Local run persistence and artifact pointers**<br>Deliverable: SQLite-backed run records and local artifact directory<br>Trace: FR-DRF-001, NFR-REL-001 | M1-02/08/09 | `NOT_STARTED` | — | Query by run ID returns contract/fixture/commit identifiers and artifact checksum; re-run doesn't overwrite old artifacts | — |
| `M1-11` | **Minimal compatible-run comparator**<br>Deliverable: Compatibility validator + drift JSON<br>Trace: FR-DRF-001/002, AC-008 | M1-10 | `NOT_STARTED` | — | Same-policy compatible PASS->VIOLATION reports **possible** drift; changed policy/env gives NOT_COMPARABLE; both run records preserved | — |
| `M1-12` | **P0 executor security regression gate**<br>Deliverable: Golden and property tests, offline demo runbook<br>Trace: PRD §11, NFR-SEC-001–005 | M1-05..11 | `NOT_STARTED` | — | AC-004..008, 011, 015..017 demonstrably pass for constrained test-harness path; **zero AI calls**; no unapproved network requests | — |

### M2 — AI drafting and real human policy approval (P0)

| Task ID | Work item / deliverable | Dependencies | Status | Owner | DoD / required proof | Evidence / last updated |
|---|---|---|---|---|---|---|
| `M2-01` | **Stable AI provider port**<br>Deliverable: `generate_structured_contract` interface and fake provider<br>Trace: FR-AI-001/002 | M1-02 | `NOT_STARTED` | — | Typed valid draft/structured error contract; no provider SDK leaks into core/domain; offline mocks pass | — |
| `M2-02` | **Safe context selection**<br>Deliverable: Scoped source reader and privacy filter<br>Trace: FR-PRJ-002, NFR-PRV-001 | M0-02/M1-02 | `NOT_STARTED` | — | Sample repo inventory includes file/line provenance but excludes `.env`, secrets, keys and unrelated files; prompt injection ignored as instructions | — |
| `M2-03` | **Initial OpenAI provider adapter**<br>Deliverable: Configurable SDK adapter with explicit permission boundary<br>Trace: FR-AI-001/002, AC-010 | M2-01/02 | `NOT_STARTED` | — | Valid response normalized; offline fake tests pass; disabled egress => no API call; timeout/bad response => structured non-success | — |
| `M2-04` | **Intent parser and candidate generation**<br>Deliverable: Candidate contract with role/resource/action/tenant and provenance<br>Trace: FR-INT-001/002/004, AC-001 | M2-01/02/03 | `NOT_STARTED` | — | Merchant requirement creates same-tenant ALLOW and cross-tenant DENY as DRAFT; no agent-supplied approval; covers AC-001 | — |
| `M2-05` | **Ambiguity/conflict review path**<br>Deliverable: `NEEDS_REVIEW` and questions, conflict detection<br>Trace: FR-INT-003, AC-010 | M2-04 | `NOT_STARTED` | — | Admin/ownership ambiguity and conflicting rules do not silently become enforceable; invalid model JSON fails closed | — |
| `M2-06` | **Real authenticated local human review**<br>Deliverable: Local review UI/CLI flow, hash-bound review receipt<br>Trace: FR-CON-001/002, AC-002/003 | M0-05/M1-03/M2-05 | `NOT_STARTED` | — | Deliberate human approval yields immutable version; forged/imported/replayed/modified review cannot authorize test | — |
| `M2-07` | **Trusted approval registry/audit**<br>Deliverable: Append-only audit events, reviewer provenance, immutable version reference<br>Trace: FR-CON-003, NFR-SEC-001 | M2-06/M1-10 | `NOT_STARTED` | — | Audit shows who/what/when/hash; same content mutation creates new draft; denied/unapproved execution is logged | — |
| `M2-08` | **Offline verifier after AI drafting**<br>Deliverable: Full separation of draft-time LLM and run-time assertions<br>Trace: FR-AI-003, AC-013 | M1-12/M2-06 | `NOT_STARTED` | — | Remove model credentials after approval; existing fixture and suite still execute; verdicts identical to no-AI baseline | — |
| `M2-09` | **Security and conformance review**<br>Deliverable: Test report for prompt injection, provider failure, approval forgery and privacy<br>Trace: PRD §§11–12 | M2-01..08 | `NOT_STARTED` | — | Relevant AC-001/002/003/010/013 pass; unresolved ambiguity never triggers tests | — |

### M3 — Developer experience: CLI, MCP, Codex (P0)

| Task ID | Work item / deliverable | Dependencies | Status | Owner | DoD / required proof | Evidence / last updated |
|---|---|---|---|---|---|---|
| `M3-01` | **CLI command skeleton**<br>Deliverable: Typer `pact` with `init`, `inspect`, `propose`, `review`, `plan`, `verify`, `compare`, `export`<br>Trace: FR-IFC-001 | M2-09 | `NOT_STARTED` | — | `--help` documented; invalid flags and noninteractive mode yield stable exit errors; no unexpected network work on import | — |
| `M3-02` | **CLI project + policy journey**<br>Deliverable: `init`/`inspect`/`propose`/`review` CLI handlers<br>Trace: FR-PRJ-001/002, FR-CON-002 | M3-01/M2-06 | `NOT_STARTED` | — | A local authorized project progresses through human-approved draft with clear `NEEDS_REVIEW`; no synthetic reviewer shortcut | — |
| `M3-03` | **CLI verification + export journey**<br>Deliverable: `plan`/`verify`/`compare`/`export`, `--json`<br>Trace: FR-IFC-001, FR-EVD-003/004 | M3-02/M1-12 | `NOT_STARTED` | — | JSON matches serialized core models; success, VIOLATION, ERROR, BLOCKED_SCOPE exits distinguishable and documented | — |
| `M3-04` | **Restricted MCP server adapter**<br>Deliverable: MCP `inspect`, `propose`, `get_contract`, `plan`, `run`, `get_run`, `compare`, `export`<br>Trace: FR-IFC-002/004 | M2-09 | `NOT_STARTED` | — | Local stdio tool discovery works; schemas validated; no `approve_contract` privileged tool; untrusted caller cannot authorize targets | — |
| `M3-05` | **Codex Skill instructions**<br>Deliverable: `integrations/codex-skill/SKILL.md`<br>Trace: FR-IFC-003 | M3-04 | `NOT_STARTED` | — | Skill gives Codex exact step order and prompt guidance; tool outputs cannot bypass approval or authorization gates | — |
| `M3-06` | **CLI/MCP parity test**<br>Deliverable: Adapter conformance suite against one approved run<br>Trace: AC-012 | M3-03/04 | `NOT_STARTED` | — | Same pinned contract/fixture yields matching normalized verdict and evidence hashes (ignoring presentation metadata) via CLI and MCP | — |
| `M3-07` | **Portable scenario/test export**<br>Deliverable: JSON/YAML scenario and runnable pytest export with documented prerequisites<br>Trace: FR-EVD-004, AC-013 | M3-03 | `NOT_STARTED` | — | Exported suite reruns without model API; test expectations point to immutable approved rule versions; imports cannot forge approval | — |
| `M3-08` | **Installation and smoke demo**<br>Deliverable: `README.md`, `.env.example`, platform installation instructions<br>Trace: FR-PLT-001, NFR-COMP-001 | M3-05..07 | `NOT_STARTED` | — | Fresh checkout reproduces full flow on documented supported OS; clean demo finishes without claiming universal security | — |

### M4 — Continuous verification, drift, temporal permissions (P0/P1)

| Task ID | Work item / deliverable | Dependencies | Status | Owner | DoD / required proof | Evidence / last updated |
|---|---|---|---|---|---|---|
| `M4-01` | **Run/commit metadata completeness**<br>Deliverable: Stable commit, policy hash, fixture and environment fingerprints<br>Trace: FR-DRF-001 | M1-10/M3-03 | `NOT_STARTED` | — | Comparing different fixture semantics is rejected or flagged; same pinned run can be reproduced | — |
| `M4-02` | **Drill-down drift comparison**<br>Deliverable: Rule/step-level evidence links and historical status<br>Trace: FR-DRF-002, AC-008 | M4-01 | `NOT_STARTED` | — | Compatible PASS->VIOLATION labels possible implementation drift; other transitions explicitly categorized | — |
| `M4-03` | **Intentional policy version change flow**<br>Deliverable: Policy diff, draft version N+1, human reapproval<br>Trace: FR-CON-004, FR-DRF-005, AC-009 | M2-07/M4-02 | `NOT_STARTED` | — | Historical contract immutable; v1 vs v2 output says approved policy change, not same-policy drift | — |
| `M4-04` | **Typed temporal DSL**<br>Deliverable: Sequenced precondition/state-transition vocabulary<br>Trace: FR-AUT-003, FR-TST-008 | M0-03/M1-05 | `NOT_STARTED` | — | Can express grant/revoke/role change via approved synthetic fixture operations only; unsafe transitions refused | — |
| `M4-05` | **Stateful fixture adapter**<br>Deliverable: Grant -> read -> revoke -> read with stale session<br>Trace: FR-DRF-006, J-04 | M4-04 | `NOT_STARTED` | — | Repeatable before/after expected decisions; tear-down resets state; wrong/stale session permissions caught | — |
| `M4-06` | **Property/regression test suite**<br>Deliverable: Positive/negative lifecycle corpus<br>Trace: FR-DRF-006, FR-TST-009 | M4-04/05 | `NOT_STARTED` | — | Covers expiration, tenant transfer, sharing and role changes; ambiguous semantics are review-blocking | — |
| `M4-07` | **Change-impact mapper**<br>Deliverable: Route/file-to-contract candidate mapping<br>Trace: FR-INT-005, FR-DRF-003 | M2-02/M4-02 | `NOT_STARTED` | — | Provides explanation/confidence; full-suite option always available; miss risk explicitly reported | — |
| `M4-08` | **Baseline-preserving remediation journey**<br>Deliverable: Before/after test workflow and immutable history<br>Trace: J-02, J-03, AC-005 | M4-02/03/05 | `NOT_STARTED` | — | Code patch causes rerun to PASS without modifying contract; failed run remains accessible; human owns patch approval | — |
| `M4-09` | **Repeatability/benchmark gate**<br>Deliverable: Temporal golden fixtures + report<br>Trace: NFR-REL-001, PRD §11 | M4-01..08 | `NOT_STARTED` | — | Separate compatible drift, policy change, infra error, not-comparable case all demonstrate expected outcomes; performance measured | — |

### M5 — Hosted control plane, web, CI, private runners (P1)

| Task ID | Work item / deliverable | Dependencies | Status | Owner | DoD / required proof | Evidence / last updated |
|---|---|---|---|---|---|---|
| `M5-01` | **Accept hosted threat model and architecture ADR**<br>Deliverable: Accepted ADR on queue/store/runner controls and identity<br>Trace: OQ-08/09/13, NFR-SEC-006/007 | M0-02/M3-08 | `NOT_STARTED` | — | Reviewer approves control/execution plane boundaries and failure/replay handling; no premature compliance promises | — |
| `M5-02` | **PostgreSQL persistence and migrations**<br>Deliverable: SQLAlchemy mappings, Alembic migration/rollback plans<br>Trace: PRD §13, NFR-COMP-002 | M1-10/M5-01 | `NOT_STARTED` | — | Fresh install migrates; old immutable contract versions and evidence relationships survive update; rollback/recovery documented | — |
| `M5-03` | **Organizations, projects and RBAC**<br>Deliverable: OIDC integration and role-based project access<br>Trace: FR-PRJ-004, FR-PLT-002, AC-014 | M5-02 | `NOT_STARTED` | — | Org A cannot enumerate/read/change Org B contracts, runs or artifact handles; ID tampering rejected and audited | — |
| `M5-04` | **Service API v1**<br>Deliverable: FastAPI versioned API, auth, errors, pagination, idempotent jobs<br>Trace: FR-IFC-006, NFR-SEC-007 | M5-03 | `NOT_STARTED` | — | OpenAPI schema validated; unauthorized API action fails; create/run duplicates do not create unsafe duplicate executions | — |
| `M5-05` | **Artifact retention and object storage**<br>Deliverable: Private object store adapter, encryption config, short-lived downloads<br>Trace: FR-EVD-008, FR-PLT-006 | M5-02/03 | `NOT_STARTED` | — | Org-crossing artifact IDs denied; secrets redacted; deletion/retention respects policy and legal holds; export tested | — |
| `M5-06` | **Durable job coordinator**<br>Deliverable: Queue-backed jobs with lease, retry, cancellation and crash recovery<br>Trace: FR-PLT-003, NFR-REL-002 | M5-04 | `NOT_STARTED` | — | Worker crash never marks PASS; cancellation stops/safely times out runner; idempotency protects repeated messages | — |
| `M5-07` | **Private runner registration and auth**<br>Deliverable: Runner identity, short-lived scoped credentials, capability negotiation<br>Trace: FR-PLT-005, NFR-SEC-001/007 | M5-01/06 | `NOT_STARTED` | — | Revoked runner cannot fetch jobs; unauthorized host/network execution fails; jobs cryptographically/operationally bound to project, scope and contract | — |
| `M5-08` | **Harden runner isolation**<br>Deliverable: Container/network/fs policies, scoped token access and secret rotation<br>Trace: NFR-SEC-004/005/006 | M5-07 | `NOT_STARTED` | — | Tests show no prohibited host mount/socket, redirect escape, uncontrolled DNS/IP destination, unauthorized writes or report exfiltration | — |
| `M5-09` | **Web app skeleton and auth**<br>Deliverable: Next.js typed client and accessible navigation<br>Trace: FR-IFC-005, NFR-A11Y-001 | M5-04 | `NOT_STARTED` | — | Signed-in developer can list own projects; unauthorized org data not rendered; keyboard nav/labels assessed | — |
| `M5-10` | **Contract review + editor UI**<br>Deliverable: Version diff, review, approval provenance and ambiguity UI<br>Trace: FR-CON-004/005, J-03 | M5-09/M5-03 | `NOT_STARTED` | — | Reviewer explicitly approves exact hash via backend; AI/caller cannot impersonate reviewer; intentional changes create new version | — |
| `M5-11` | **Run history / drift / evidence UI**<br>Deliverable: Reports, findings, statuses, coverage and artifact viewer<br>Trace: FR-IFC-005, FR-EVD-003 | M5-05/09 | `NOT_STARTED` | — | Displays PASS, VIOLATION, INCONCLUSIVE, ERROR, SKIPPED, CANCELED without misleading green; run reproductions linked | — |
| `M5-12` | **GitHub App and CI checks**<br>Deliverable: Scoped GitHub installation, verified webhook handler, PR annotations<br>Trace: FR-IFC-007, FR-DRF-004 | M5-04/06 | `NOT_STARTED` | — | Invalid signature/replay/mismatched repository rejected; checks include evidence link and non-PASS statuses; advisory default | — |
| `M5-13` | **Policy-based optional merge gate**<br>Deliverable: Admin-configured gate rules<br>Trace: OQ-11, FR-DRF-004 | M5-12/M5-03 | `NOT_STARTED` | — | Only authorized admin enables blocking; missing runs/infra errors not silently green; documented safe rollback of gate | — |
| `M5-14` | **Provider registry and additional model adapters**<br>Deliverable: Gemini/Claude and optionally local-provider adapters<br>Trace: FR-AI-004/005/006 | M5-03/M2-01 | `NOT_STARTED` | — | Same draft-or-error conformance cases pass; provider egress consent enforced; no unapproved fallback or hidden bills | — |
| `M5-15` | **Operational audit, quotas, traces**<br>Deliverable: Structured audit stream, rate/quota limits, sanitized telemetry<br>Trace: FR-PLT-004, NFR-OBS-002 | M5-04/06 | `NOT_STARTED` | — | Cost/run limits enforced; incident can be correlated without raw secrets; quotas isolate noisy organizations | — |
| `M5-16` | **Hosted E2E / deployment security gate**<br>Deliverable: Tested deploy/runbook + threat-review findings<br>Trace: PRD §§5,11,15 | M5-03..15 | `NOT_STARTED` | — | J-01..05 on supported hosted profile; full RBAC/SSRF/runner/evidence tests pass; no critical/high unresolved release blockers | — |

### M6 — Independent evaluation, benchmarking and validation (P1/P2)

| Task ID | Work item / deliverable | Dependencies | Status | Owner | DoD / required proof | Evidence / last updated |
|---|---|---|---|---|---|---|
| `M6-01` | **Pre-register benchmark protocol**<br>Deliverable: Test protocol and metrics definitions<br>Trace: OQ-12, PRD §11.3 | M4-09 | `NOT_STARTED` | — | Definitions for correct contract, time-to-first-valid-test, precision/recall, false violation, cost and reproducibility approved before tuning | — |
| `M6-02` | **Independent authorization fixture corpus**<br>Deliverable: Multiple seeded safe/vulnerable apps, temporal and ambiguous policy cases<br>Trace: FR-DRF-006, PRD §11.3 | M6-01 | `NOT_STARTED` | — | Fixture answer keys independently reviewed; train/tuning examples separate from held-out tests | — |
| `M6-03` | **Manual pytest baseline**<br>Deliverable: Recorded manually written test workflow<br>Trace: G-10, PRD §11.3 | M6-02 | `NOT_STARTED` | — | Same requirements and app versions used; time, code volume, test validity and errors captured | — |
| `M6-04` | **Codex-only baseline**<br>Deliverable: Coding-agent-only test-generation evaluation<br>Trace: G-10, PRD §11.3 | M6-02 | `NOT_STARTED` | — | Model access, prompts, context limits and allowed iterations documented; blinded held-out cases used where possible | — |
| `M6-05` | **Relevant tool baselines**<br>Deliverable: StackHawk/Cerbos comparisons where applicable<br>Trace: PRD §1.4, §11.3 | M6-02 | `NOT_STARTED` | — | Feature-scope mismatch documented; same target/fixtures, cost/time and limitations disclosed; no unfair feature-for-feature claim | — |
| `M6-06` | **PACT run and statistical analysis**<br>Deliverable: Reproducible evaluation report and raw redacted metrics<br>Trace: PRD §11.3 | M6-02..05 | `NOT_STARTED` | — | Results include errors, inconclusive cases, confidence/uncertainty, spend and setup overhead; claims match measured coverage | — |
| `M6-07` | **Usability/accessibility and security reviews**<br>Deliverable: Developer observation study, a11y review, security report<br>Trace: NFR-A11Y-001, PRD §11 | M5-16/M6-06 | `NOT_STARTED` | — | At least one full persona flow tested on actual setup; critical issues triaged; public limitations explicitly listed | — |
| `M6-08` | **Launch/pivot review**<br>Deliverable: Decision memo and prioritized backlog<br>Trace: OQ-12, PRD §22 | M6-06/07 | `NOT_STARTED` | — | Owner documents continue/refocus/pivot decision grounded in measurements; roadmap and PRD updated if product scope changes | — |

## 4. Approval and Architecture Decision Register

**This table tracks the decision workflow; it does not constitute authenticated approval.** An ADR becomes authoritative only after an actual owner/security reviewer accepts its exact contents via the established review process.

| ADR ID | Related questions | Decision area | Status | Reviewer / proof | Blocks |
|---|---|---|---|---|---|
| `ADR-0001` | OQ-02 | Canonical contract/authorization DSL, rule syntax, DENY semantics | `NOT_STARTED` | — | Binding domain semantics after M0-03 |
| `ADR-0002` | OQ-03, OQ-06 | Authorized target, FastAPI fixtures, runner, 404 profile, redirect controls | `NOT_STARTED` | — | Runner/test execution trust after M0-04 |
| `ADR-0003` | OQ-04, OQ-14 | Trusted human review, hash-bound approval, audit and immutability | `NOT_STARTED` | — | Binding contract approval after M0-05 |
| `ADR-0004` | PRD §8.3 | Stack/workspace packaging and compatibility | `NOT_STARTED` | — | Stable package layout/CI policy |
| `ADR-0005` | OQ-05 | MCP / Codex trust and tool boundaries | `NOT_STARTED` | — | Codex integration trust |
| `ADR-0006` | OQ-10 | Provider consent, egress and adapter interface | `NOT_STARTED` | — | External model usage |
| `ADR-0007` | OQ-08, OQ-13 | Hosted control plane and private runner trust | `NOT_STARTED` | — | M5 hosted runner |
| `ADR-0008` | OQ-11 | Webhooks, CI statuses, optional merge gate | `NOT_STARTED` | — | Merge enforcement |
| `ADR-0009` | OQ-12 | Benchmark methodology and acceptable claims | `NOT_STARTED` | — | Competitive evidence claims |

**When proposing ADRs:** replace a `NOT_STARTED` status with a factual workflow note such as `PROPOSED — awaiting review`; record the reviewer and artifact. Never write `ACCEPTED` on behalf of the coding agent.

**M0-01 reconciliation:** None of the nine ADR files or `docs/DECISIONS.md` exists. All rows above remain `NOT_STARTED`; no acceptance was recorded. Schema §11 additionally proposes ADR-0010 for hosted RLS, but no file or new canonical task exists. The inventory §7 records pending canonical document-path, Git, workflow-owner and PRD open-question decisions; these are not blockers for documentation inventory.

## 5. Blocker Register

Use this for **actual blockers encountered**, not every normal dependency. If a task is BLOCKED, reference its blocker ID here. Initial state: **no task actively blocked; critical ADRs pending by design**.

| Blocker ID | Task(s) | Description / actual observation | Unblock condition | Owner | Status | Last updated |
|---|---|---|---|---|---|---|
| _No active blockers recorded_ | — | — | — | — | — | — |

**New blocker ID sequence:** `BLK-0001`, `BLK-0002`, …; never reuse IDs or delete resolved history.

## 6. Local Issue Register (bugs, discoveries, technical debt)

The 71 `M#-##` records above are the **canonical planned implementation issues**. Use `ISS-0001`, `ISS-0002`, … only for **new issues discovered during work**, and link each to its parent WBS ID; do not duplicate planned work.

| Issue ID | Type / severity | Title & reproduced observation | Related task / PRD | Status | Owner | Evidence / resolution |
|---|---|---|---|---|---|---|
| `ISS-0001` | DOCS / LOW | Database draft at `docs/schema.md` declares missing `docs/DATA_MODEL.md` canonical | M0-01; PRD §§13,14; follow-up M0-09 | `NOT_STARTED` | Unassigned | Inventory §5/6; preserve file; canonical-path choice pending |
| `ISS-0002` | DOCS / LOW | Architecture header retains delivery-copy wording and AGENTS v1.0.0 reference; actual AGENTS is v1.0.2 | M0-01; PRD §14 | `NOT_STARTED` | Unassigned | Inventory §6; metadata correction not performed |
| `ISS-0003` | DOCS / LOW | Architecture §7 points status to roadmap/issue tracker; AGENTS and todo designate root `todo.md` canonical | M0-01; AGENTS §12; todo §9 | `NOT_STARTED` | Unassigned | Inventory §6; use existing instruction precedence; no duplicate ledger created |
| `ISS-0004` | DOCS / MEDIUM | TB-08 labels differ: Human -> Approval in architecture, Browser -> Hosted API in security | M0-01; follow-up M0-02 | `NOT_STARTED` | Unassigned | Inventory §6; shared boundary identity needs review; no implementation vulnerability claimed |
| `ISS-0005` | DOCS / MEDIUM | Security §15 has inconsistent AC mappings for SEC-T008/010/012/025 | M0-01; PRD §11; follow-up M0-02/M0-08 | `NOT_STARTED` | Unassigned | Inventory §6 lists exact mismatches; preserve PRD criteria; no tests claimed |

**Issue types:** `BUG`, `SECURITY`, `TECH_DEBT`, `RESEARCH`, `DOCS`. Severity for defects: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Issue status uses the same six values as task status. A security issue is not closed merely because the AI says it is fixed: include regression evidence, scope, and reviewer decision.

## 7. Evidence Log — Required Before Closing Any Task

Append an entry for each task completing review. Never store raw API keys, authentication tokens, PII or private application responses here.

| Evidence ID | Task | Date | Changed artifact(s) | Exact test command / result | Commit/PR/reviewer | Decision / notes |
|---|---|---|---|---|---|---|
| `EV-0001` | M0-01 | 2026-10-10 | Added `docs/REPOSITORY_INVENTORY.md`; updated `todo.md`; ten other original files unchanged by SHA-256 | Inventory §8 contains exact commands/transcripts. Local checks PASS: 12 files/six directories, 23 absent paths, 25 relative file links, negative link detection, 71 unique task IDs/WBS/board consistency, original task/ADR rows and initialization journal. First checker attempt failed on bold numeric formatting; parser corrected and rerun passed. Application/security tests NOT RUN (no implementation/toolchain). | No branch/commit/PR or human ADR acceptance; Codex reviewed inventory and local `git diff --no-index`; direct owner authorized M0-01 only | Documentation-only DoD met; no required ADR or security approval for inventory. Future approvals remain pending; no other task started. Temporary baseline/check transcripts recorded in inventory §8. |

**Evidence IDs:** `EV-0001`, `EV-0002`, …; include actual test output path when available and specify `NOT RUN` if not run. `NOT RUN` is **not** sufficient for completion of a test-dependent task. Documentation-only tasks may close with reviewed document diff, link, and explicit reviewer evidence where required.

### Definition of DONE (check every item)

- [ ] Exact scope and DoD from corresponding `M#-##` architecture row achieved.
- [ ] Related `FR-...` / `NFR-...` / `AC-...` trace identified.
- [ ] Required ADR(s) approved by a **real owner/reviewer**, not by an LLM or imported JSON.
- [ ] Positive and relevant failure/negative tests actually run; exact commands/results recorded.
- [ ] Any unexecuted checks noted as `NOT RUN` and task stays review/blocked if required checks are missing.
- [ ] No approval bypass, unauthorized testing, unexpected model egress, unsafe target, secret leakage or false `PASS` introduced.
- [ ] Git diff/commit and relevant changed files recorded; unrelated changes preserved.
- [ ] Evidence row added; task status changed to `DONE`; summary board and journal updated.

## 8. Session Journal — Persistent Project Memory

**Write one concise entry per meaningful AI/developer session** (especially after changing any task state). Append entries in chronological order; never overwrite earlier observations. Keep only facts observed in the repo, decisions approved, and explicit unknowns. Put large logs in linked artifacts rather than in this Markdown.

### 2026-10-10 — Tracker initialization (documentation-only)

- **Session type:** Preparation / tracker creation, before repository execution.
- **Inputs reviewed:** `PRD.MD`, `AGENTS.md`, `docs/ARCHITECTURE.md`.
- **Observed facts:** 71 canonical work items across M0–M6; documents supplied; architecture marked DRAFT; no runnable PACT implementation or test evidence verified.
- **Action:** Created `todo.md` task ledger and status update protocol; all implementation work items initialized `NOT_STARTED`.
- **Approvals:** None recorded; no ADR accepted.
- **Tests:** None executed for PACT application (tracker consistency checks only, if separately recorded).
- **Next:** Inspect actual project repository for `M0-01`; record inventory, gaps and Git state before touching production code.

### 2026-10-10 — M0-01 / repository inventory task claim

- **Owner / session:** Codex / M0-01 inventory session; authorized by the direct task prompt.
- **Git:** Not initialized; no branch, commit or Git diff available.
- **Before state:** 11 Markdown files, six directories excluding the root; no source, tests, build configuration or ADR files; all 71 canonical tasks `NOT_STARTED`.
- **Allowed edits:** Create `docs/REPOSITORY_INVENTORY.md`; update this tracker. Preserve other document bytes and existing journal history.
- **Trace / criteria:** PRD §§0,14,17; Architecture M0-01 requires checked actual paths, recorded discrepancies and no invented implementation claims. No runtime AC is exercised by this documentation task.
- **Checks planned:** Inventory including hidden entries, Git absence, expected-path and relative-link checks, ledger/WBS/count consistency, preservation of original-file hashes and initialization journal.
- **Safety / decisions:** No target tests, provider egress, dependency installs, schema moves, ADR approvals or Git initialization. Later design decisions remain pending.
- **Transition:** `M0-01 NOT_STARTED -> IN_PROGRESS`; no other task claimed.

### 2026-10-10 — M0-01 / verified inventory and handoff

- **Owner / session:** Codex / M0-01 inventory session.
- **Files changed:** Added `docs/REPOSITORY_INVENTORY.md`; updated `todo.md` only. Ten other original files, all other task rows/DoD, nine pending ADR rows and the initialization journal were preserved.
- **Observed state:** Docs-only workspace; Git not initialized; no implementation, tests, build configuration or ADR files. `docs/schema.md` is the existing database draft; declared `docs/DATA_MODEL.md` remains missing. No move or duplicate copy performed.
- **Trace:** M0-01; PRD §§0,14,17. Documentation-only rationale: no runtime AC or security guarantee claimed.
- **Checks / review:** Exact commands and local transcript paths are in inventory §8 and `EV-0001`. Path/link/negative-link checks, ledger/WBS/board counts and SHA-256 preservation checks passed. Reviewed the inventory and `git diff --no-index` comparison against the saved tracker. First checker attempt failed parsing the bold TOTAL cells; corrected the temporary checker, preserved project assertions and reran successfully. Final `-ExpectedStatus DONE` verification passed; M0 1/9 and total 1/71 are consistent with the ledger.
- **Not run:** Application, integration/security tests, linters and type checks; no implementation/test configuration exists. Git diff against repository history, commit and PR unavailable; local no-index comparison is not a commit or approval.
- **Review / approvals:** No ADR, policy, target, provider, migration or security-boundary decision was approved. The task-specific documentation DoD prescribes no separate ADR acceptance or human security sign-off. Codex local document review is not represented as a human approval. Later review/authorization gates remain pending.
- **Issues / blockers:** Added ISS-0001–0005 for observed document inconsistencies; each NOT_STARTED and unassigned. Planned missing artifacts and later ADR decisions are not new M0-01 blockers.
- **Transitions:** `NOT_STARTED -> IN_PROGRESS` at claim; `IN_PROGRESS -> IN_REVIEW` when the inventory existed; `IN_REVIEW -> DONE` after safe checks and document review. M0 board: 1/9 DONE (11.1%); total: 1/71 DONE (1.4%); all other canonical tasks NOT_STARTED.
- **Next:** M0-02 recommended; M0-03/M0-06 also dependency-ready. Await a separate owner task prompt; none started automatically.

### 2026-10-10 — M0-02 / threat-model review task claim

- **Owner / authorization:** Codex / M0-02 threat-model review; direct owner prompt authorizes only this documentation task. Developer (the repository owner) designated themselves security reviewer in the current conversation; designation is not sign-off.
- **Prerequisites observed:** M0-01 DONE with EV-0001; 12 Markdown files, six directories; Git not initialized; no actual code, tests, build configuration or accepted ADRs.
- **Allowed edits / trace:** Only `docs/SECURITY.md` and `todo.md`; NFR-SEC-001–005. Preserve all other bytes and historical records. Use pact-security-review Workflow B from `skill.md`.
- **Plan / positive checks:** Retain the existing asset and threat registers; label diagram boundaries, reconcile TB-08, map six mandatory attacker paths and NFRs to planned controls/tests, correct grounded AC-reference errors. Check ID uniqueness/reference resolution, planned versus implemented claims, ledger counts and file hashes.
- **Negative checks:** In-memory mutations with missing/duplicate threat IDs, wrong TB-08, absent NFR trace and wrong AC mappings must be detected; no target, provider or runner is executed.
- **Approval gates / completion:** Do not freeze DSL, approval or runner ADRs. Human sign-off on exact reviewed bytes is required by Architecture M0-02 and SECURITY §19.1; Git commit/review provenance is also unavailable. Stop those affected actions; prepare the reviewable draft and truthful IN_REVIEW handoff.
- **Baseline:** Original hashes and copies stored outside the repository at `C:\Users\user\AppData\Local\Temp\PACT-M0-02-e16686aa-60c1-4cb1-a15f-74e05503ea6d`; claim transition NOT_STARTED -> IN_PROGRESS, M0 1/9 DONE, total 1/71 DONE. No other task started.

### Template — append for each next session

```markdown
### YYYY-MM-DD — <Work item IDs> / <purpose>
- Owner / agent:
- Git branch + commit (or "uncommitted"):
- Before state / discovered facts:
- Files created/changed:
- PRD / AC trace:
- Tests actually run (command and result):
- Security review / authorization / ADR status:
- Issues or blockers added / resolved:
- Tracker status transitions:
- Next smallest ready task:
```

## 9. Change Control and Multi-Agent Coordination

- Prefer **one source of status truth**: this root `todo.md`. Do not keep a separate hand-edited `docs/ROADMAP.md` status ledger; that file, if created, should summarize or link to the live tracker.
- `PRD.MD` defines requirements; `AGENTS.md` agent conduct; `docs/ARCHITECTURE.md` WBS and DoD; ADRs approved choices; **this file records actual work evidence and current status**.
- Agent must inspect repo state and this ledger before picking a task; if work-in-progress owner/task already exists, coordinate ownership rather than edit the same files.
- In parallel work, claim explicit paths/modules and agree schema changes first. Use independent branches/PRs for conflicting areas. Merge the task tracker carefully and recompute milestone counts after resolving conflicts.
- All status and evidence changes belong in version control. Never silently delete a blocked/disputed issue, approval history or prior test failure.
- Changing WBS scope/priority/dependencies requires an update to `docs/ARCHITECTURE.md`/`PRD.MD` through the documented change process first; this ledger only mirrors the authoritative approved plan.
- New unexpected bugs go into `ISS-####`; newly approved feature work must first appear in architecture WBS (or an explicitly approved extension section), then the tracker.
- Do not edit tracked acceptance wording to make unfinished work look finished.
- Before ending a session, publish a handoff: task, status, diff, tests, security implications, blockers and next task.

### Example status update (illustration only — not completed work)

```markdown
| `M1-07` | Scope guard and request-budget policy | M0-04/M1-05 | `IN_REVIEW` | @security-agent | Out-of-scope redirect blocked before outbound request | `EV-0021`; tests/security/test_scope.py; PR #42 |
```

This example is **hypothetical**, not a record of executed work.

---

**End of PACT `todo.md` v1.0.0. Last verified state (2026-10-10): docs-only filesystem inspected; Git not initialized; M0-01 documentation inventory verified; 1/71 canonical work items DONE; no PACT implementation or runtime acceptance tests verified.**
