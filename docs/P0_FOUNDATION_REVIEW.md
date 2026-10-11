# P0 foundation review package

> **Version / date:** 0.1 / 2026-10-11
> **Status:** IN_REVIEW — documentation reconciled; owner decisions pending
> **Tasks / trace:** M0-06, M0-02, M0-04, M0-05; NFR-MAINT-001, NFR-SEC-001–005, OQ-03/04/06/14, FR-TST-002, FR-CON-001/002
> **Reviewer:** Developer / repository owner (already designated)
> **Evidence:** todo.md EV-0065; base Git HEAD `943cd681c15fe88ff1657478016216ea83da7c0c`

## 1. Scope and current facts

The owner requests implementation of the review-package plan through safe documentation reconciliation. Allowed paths are this packet, SECURITY.md, ADR-0002/0003/0004 and todo.md. Source/tests, PRD/architecture, accepted DSL and other design conventions remain unchanged. No dependency download/install, workspace scaffolding, privileged component, account/key/ACL provisioning, target/provider/service request, commit or push occurs. This package cannot authorize product approvals or execution.

Actual intake: main tracks origin/main at the HEAD above; todo.md was modified and LAUNCH_PIVOT_REVIEW.md untracked. There were 65 project files/19 directories, 23 Python files, six unit modules with 77 declared unit-test methods. Domain/normalizer/untrusted approval-model/provisional parser/fake-provider components exist. There is no pyproject.toml, uv.lock, CI, marketplace demo, authentic session adapter, authorized executor, CLI/MCP service or protected approval registry. Historical component test results are not rerun or converted into integrated runtime evidence here.

The owner selected **Windows + Linux** as the proposed tooling support matrix and **a separate protected local broker** as the human-approval design direction. These directions are recorded without accepting entire ADRs, declaring platform containment or activating privileged approval. Preserve existing accepted DSL/ID/job-run conventions, Dedicated Audit Authority/checkpoint direction and temporary backlog order. Hosted staging remains DISABLED; held-out corpus remains DISABLED; external benchmark profile remains PLANNED/UNCONFIGURED. Unchanged decisions are not requested again.

## 2. Exact current review bindings

SHA-256 covers raw file bytes, including line endings. A later edit invalidates these bindings; historical digests remain evidence of older revisions, not acceptance of new content. The packet's own digest is recorded separately in EV-0065 to avoid a self-referential hash.

| Review artifact | Current version | Current raw SHA-256 | Historical binding |
|---|---|---|---|
| [Tooling ADR](adr/0004-repository-and-stack.md) | PROPOSED v0.2 | `B7F6F7D25397697AE6209D583D67BD32A09ED45374947C79C383C18D281EFC53` | v0.1 / EV-0008: `A79B424F1F871CAB7FF06CFC32BA5C8E34AC149B258E498807FCD4995DEC899F` |
| [Threat model](SECURITY.md) | DRAFT v1.0.4 | `A51AD296CFAE08660903D0289102E99A57132C8375550E7B2391DF81279AE4D6` | v1.0.3 / EV-0034: `4EDA9D150E8425E5D31B3B03BC281255B0C2365F98839C99565AA11FC40CCA9B` |
| [Fixture/runner ADR](adr/0002-fixture-runner.md) | PROPOSED v0.3 | `85C207BAE17F210A4370FDD0DB69A39B8946F5D15FF2B7F28A007EDB5DF35011` | v0.2 / EV-0007: `F661F0893B1915D47886A157B96D04322E80A6D274FD820B4C96F4B2C16075CB` |
| [Human-approval ADR](adr/0003-human-approval.md) | PROPOSED v0.3 | `0360AEE8DB412B4923B05A069BB5E3D1C0B5B2B49F7677B6A15AE40F32E82AFF` | v0.2 / EV-0034: `232AD5AA47B2729AAC10D3AC0CF4261165045DCB33E297203FB0B0D8F9EFD199` |

## 3. Recommendations, alternatives and actual owner decisions

| Task | Recommended direction / alternative | Decision genuinely needed now | Conditions still open after design review |
|---|---|---|---|
| M0-06 | uv workspace, one lock, stdlib domain; Pydantic boundaries; bare FastAPI demo; HTTPX transport; pytest/Ruff/mypy. Alternative: request specific changes to packaging/tool ownership. CLI/MCP/provider SDKs arrive in their own tasks. | Accept, change or defer **the reconciled tooling design**, explicitly excluding approval of candidate pins/downloads. Windows/Linux direction is already selected. | Reverify exact maintained Python patches, package APIs/versions/transitives/licenses/notices/artifact provenance, build-hash enforcement and wheel compatibility before freeze/acquisition. No final version or download is authorized here. Product publication license remains undecided; private development need not publish. |
| M0-02 | Keep TB-08 mandatory human authority; explicitly review proposed TB-09 browser/API/egress and runner assumptions. Alternative: give specific threat-boundary corrections. | Sign off or request changes on **v1.0.4 threat-model assumptions**, particularly §§2–3, 8.5, 10.4.1, 15, 18–19. | Model acceptance is not implemented protection, ADR acceptance, contract/target/provider permission or security clearance. Exact reviewed/committed provenance remains required by §19.1. |
| M0-04 | Deterministic synthetic fixtures; independently authenticated A/B sessions; serial local IP-literal target; zero redirects/retries/DNS initially; complete validity controls and terminal-path cleanup. Alternatives: stricter budgets or different observation/containment profile through an explicit revision. | Accept, change or defer **ADR-0002 v0.3 design choices** in §10. Identify any conditions on observation, transport, containment, budgets and cleanup. | Concrete OS profile, destination/actual-peer enforcement, cleanup authority/envelope and runtime tests remain unverified; unsupported profiles stay disabled. M0-02 closure remains a dependency. |
| M0-05 | Preserve selected protected local broker and independent Audit Authority/checkpoints. Alternative confirmation channels may be investigated, not activated. | **No repeated broker/storage-direction approval needed.** Review can request corrections or defer broader ADR acceptance while the concrete identity/enrollment/user-presence proposal is prepared. Do not ask for blanket mechanism acceptance before evidence. | ADR-0003 §10.1 specifies Windows/Linux feasibility evidence. Protected principals, IPC/ACL, trusted display/transaction-bound human presence, enrollment/revocation, backend/key custody/latest-checkpoint freshness/anchoring/recovery remain concrete design/verification work. REGISTRY_DISABLED persists. |

The consolidated immediate review therefore has three decision scopes: tooling design, threat-model assumptions and fixture/runner design. Full human-approval mechanism acceptance is a later review of a concrete proposal. A scoped acceptance must name accepted choices, excluded choices and conditions; unfinished conditions do not silently become accepted or satisfy task DoD.

## 4. Detailed limits and unresolved risks

Tooling proposes Python `>=3.12,<3.15`, standard GIL CPython, Windows 11 x86-64 and Linux Ubuntu 24.04 x86-64/glibc, minors 3.12/3.13/3.14: **six required future cells**. Installed isolated interpreter is CPython 3.14.4. ADR-0004's 3.14.8 and package pins remain historical candidate references, not verified final releases or installed project dependencies. Isolated metadata found no listed third-party distributions visible; this is not machine-wide absence. No public index/release verification occurred. A later isolated install uses reviewed direct/transitive pins and hashes, no system-site inheritance, and fails on cache miss, stale lock or wrong artifact hash without online fallback.

ADR-0002 §6 budgets are unchanged **candidate ceilings**, never active configuration: concurrency 1; 160 scenario requests + 32 reserved cleanup = 192 total; request timeout 3 s; execution 120 s + cleanup 15 s. All other finite limits in the existing JSON remain unchanged. The trusted cleanup controller's CPU/memory/process/filesystem envelope is still open. Candidate numbers may need a reviewed revision after measurement; no automatic expansion.

Tokens must map to independent authentic synthetic identities, not merely differ as strings. DENY 403/404 can PASS only under the genuinely approved assertion profile with valid authentication, route/resource existence and no protected disclosure/state change. Invalid route, missing fixture or failed authentication is not a denial success. ALLOW 500, timeout and infrastructure failure cannot PASS. Missing observation is INCONCLUSIVE; invalid precondition/infrastructure is ERROR. The accepted DSL's optional 401 profile does not activate it in the initial fixture adapter.

High-risk unresolved controls are human identity/presence and protected broker custody; audit durability and latest independently trusted checkpoint verification; SSRF/actual-peer/redirect/proxy enforcement; OS filesystem/network/privilege containment; budgets/cancellation/orphan cleanup; sensitive evidence redaction/integrity and tenant access. Same-user writable storage, a hash chain, terminal confirmation, imported APPROVED JSON, environment flags or an automatable button do not establish approval authority. Authority or checkpoint failure keeps approval disabled. No exploit, mitigation success or release clearance is reproduced in this documentation session.

## 5. Reconciliation findings and provenance

| Confidence / impact | Confirmed documentation discrepancy | Correction / remaining limitation |
|---|---|---|
| Confirmed / documentation | SECURITY's current v1.0.3 requests still named v1.0.2; current ADR tables described accepted DSL as proposed and existing code as absent | Current review headers/requests and ADR contexts now name actual accepted DSL and partial components. Original intake/review events remain explicitly historical. No full integrated controls are inferred. |
| Confirmed / documentation | SECURITY stated ADR-0002/0007 files did not exist despite actual drafts | Current §10.4.1 and §18 now distinguish existing PROPOSED files from accepted controls. |
| Confirmed / documentation | BLK-0002 treated the earlier final SECURITY revision as uncommitted | At intake, v1.0.3 raw bytes matched HEAD; last SECURITY path commit `145f89f6c1123d6ae245390a6bd83e55c05efcbe`. The **new v1.0.4** is uncommitted and unsigned; no unnecessary old-file commit requested, and BLK-0002 is not automatically resolved. |
| Confirmed / evidence limitation | ADR-0004 historical interpreter/library observations could be read as current resolved-project support | Label historical observations/candidates; separate isolated 3.14.4 metadata from project installation and future matrix proof. Exact pins/licenses/provenance must be reverified before freezing. |

Preserve prior review digests, owner responses, evidence/journal entries and the pre-existing launch memo. EV-0034's historical detailed-log gap remains a gap; do not invent its missing checks or acceptance. The only new proof here concerns document reconciliation and preservation.

## 6. Task closure and dependency impact

All four tasks remain **IN_REVIEW**. Their exact architecture DoDs and dependency graph are preserved:

| Task / dependency | Exact architecture DoD | Present evidence / unmet closure |
|---|---|---|
| M0-06 ← M0-01 DONE | Python/OS matrix, SDK licensing/versions, pinning, test commands and package ownership described; unresolved alternatives visible | Reconciled proposal supplies planning coverage; genuine design review and trustworthy candidate-version/license provenance remain pending. Actual bootstrap/lock/CI proof belongs to M0-07, not fabricated here. |
| M0-02 ← M0-01 DONE | Covers injection, forged review, SSRF, runner escape, leaked evidence, tenant IDOR; reviewer signs off threat boundary before privileged code | Threat-model coverage exists; genuine final sign-off and current committed/reviewed provenance absent. Runtime control verification is an implementation gate, not a claim of this document review. |
| M0-04 ← M0-02 IN_REVIEW | Defines synthetic actors, safe test target, auth setup, teardown, 404 semantics, redirects and budgets; examples include negative paths | Existing FX-01..23 and §10 matrix preserved, no runtime results; dependency and genuine design acceptance pending. |
| M0-05 ← M0-02 IN_REVIEW / M0-03 DONE | Identity, exact hash, local review action, immutable history, untrusted import behavior and replay rejection documented; owner approval requested | AP-01..18/AU plan exists, selected directions recorded; broader mechanism review and M0-02 dependency open. No human positive or protected registry exists. |

Canonical 71-task recount remains **6 DONE / 7 IN_REVIEW / 40 BLOCKED / 18 NOT_STARTED**; M0 **2 DONE / 6 IN_REVIEW / 1 NOT_STARTED (2/9)**. This package closes no task or milestone. M0-07 is the next conditional ID after genuine M0-06 closure and concrete tooling/acquisition scope; it is NOT_STARTED. Runner and human-approval work waits for its own actual dependencies/reviews. No successor starts here.

## 7. Verification: actual checks versus required future evidence

Actual commands and results are recorded in EV-0065. They cover Git/file discovery, raw digests, isolated interpreter metadata, static AST/JSON parsing, document/link/version consistency, canonical ledger/DoD/dependency recount, prior history/untouched-file preservation and whitespace. These do not execute product functionality or certify isolation. Source behavior is unchanged; the existing unit suite was not rerun solely for prose changes.

| Future proof / case references | Positive evidence required | Negative/failure evidence required | This session |
|---|---|---|---|
| Tooling TL-01..08 | Clean install from lock on six required cells; real import smoke, lint/type/unit checks; reviewed distribution artifacts and measured build reproducibility | Missing/stale lock, empty cache, tampered or missing/transitive hash, unsupported interpreter, host-package/secret contamination all fail | NOT RUN; no manifests/lock/cache/acquisition approval |
| Fixture/runner FX-01..23 | Stable ownership, authentic independent actors, valid controls; vulnerable VIOLATION vs fixed PASS; valid 404 non-disclosure | Missing/wrong token/fixture/route, ALLOW 500, leaks, redirect/DNS/peer/proxy escape, arbitrary commands, caps/cancel/cleanup failure cannot PASS | NOT RUN; demo/adapter/executor/containment absent |
| Approval AP-01..18 | Real enrolled human confirms exact hash/version/scope/nonce; durable immutable history with verified independent anchor | Forged/imported/replayed/stale/tampered review, agent caller, revoked identity, authority/audit/anchor failure rejected before activation | NOT RUN; concrete broker/presence mechanism and protected authority absent |
| Audit AU-01..10 in TEST_PLAN §11 | Latest independent trusted checkpoint, continuity and restricted recovery established | Modification/deletion/reordering/forged or stale checkpoints/rollback/outage/key or tenant violations/append failure detected or fail closed | NOT RUN; same-user mocks do not prove protected anti-rollback |

Runtime security, Linux support, broker feasibility, genuine human approval, install/build/lint/mypy/pytest/CI and external services are **NOT RUN**. None is marked PASS from static documentation checks.

## 8. Review response and next bounded work

For each immediate scope in §3, the owner may **accept specified design choices**, **request changes**, or **defer** against the exact §2 version/digest. Acceptance records the reviewer, date, accepted choices and remaining conditions. It grants no contract approval, execution scope, dependency acquisition, provider egress, hosted staging, spending or deployment.

After review, reconcile the exact acceptance conditions before any task closure. Prepare final maintained pins/license/artifact/build-constraint evidence separately before download or M0-07 bootstrap. Prepare broker identity/enrollment/presence and audit-protocol feasibility proposals before requesting mechanism acceptance. An eventual local commit must bind the actually reviewed revised bytes; this session makes none. Keep unsupported execution/approval profiles disabled throughout.
