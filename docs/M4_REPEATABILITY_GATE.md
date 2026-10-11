# M4-09 — Repeatability and benchmark gate

> Date: 2026-10-11
> Status: **BLOCKED — M4 NOT READY**
> Trace: NFR-REL-001; PRD §11; supporting AC-005/008/009, FR-DRF-001/002/005/006
> Scope: repository inspection and documentation only; no M4 implementation or runtime approval
> Evidence: todo.md EV-0035 / BLK-0026

## 1. Intake, allowed changes and completion rule

Only this report and the corresponding row, evidence, board and dated journal in [todo.md](../todo.md) may change. Source, tests, ADRs, schemas, approved policy, fixtures, dependency configuration and Git history remain untouched. Scratch inspection/check scripts and logs are outside the repository. No dependency download, listening service, target request, external AI request, privileged authority setup or approval action is authorized or performed.

[Architecture §7](ARCHITECTURE.md) gives M4-09 dependencies **M4-01..08**, deliverable **Temporal golden fixtures + report**, and exact DoD:

> Separate compatible drift, policy change, infra error, not-comparable case all demonstrate expected outcomes; performance measured

Success requires executable independently reviewed golden fixtures, genuine policy/version/scope provenance, retained immutable runs and sanitized observations demonstrating each outcome, plus measured runtime data. A documentation report or passing schema tests cannot satisfy that DoD. Stop runtime benchmarking while required dependencies and human gates are unresolved. No next task starts in this session.

## 2. Actual repository and evidence boundary

Intake Git: initialized, branch main, HEAD **145f89f6c1123d6ae245390a6bd83e55c05efcbe**, clean worktree. Recent history contains this externally created commit and ddf945d; no commit/fetch/push or history change performed in this session. Inventory at intake: **56 files, 19 directories** excluding root and .git; 22 Markdown, 11 JSON, 23 Python files. This report adds one Markdown file.

Actual core contains only domain, provisional scenarios and providers packages. Six unit modules define 77 test methods (static count, not execution): domain 19, contracts 20, untrusted approval 9, scenarios 17, providers 10, imports 2. Existing fixture JSON is candidate contract/parser data, not temporal execution goldens or human-approved contracts.

Absent inspected paths: pact_core/execution, evidence, persistence, drift, security and intent; apps/demo-marketplace; packages/pact-cli and pact-mcp; fixtures/authorization-benchmark; pyproject.toml, uv.lock and .github/workflows. No actual run/artifact store, compatibility fingerprints, diff engine, temporal interpreter/session adapter, remediation workflow, runner/assertion engine or M4 benchmark command was found in the inventory or source.

Code observations:

- [approval_model.py](../packages/pact-core/pact_core/domain/approval_model.py): immutable state is expressly untrusted; require_authenticated_approval always raises ApprovalRequiredError. A modeled APPROVED status is not an authenticated review. new_draft_version retains domain history only, not a trusted policy revision workflow.
- [scenarios/parser.py](../packages/pact-core/pact_core/scenarios/parser.py): closed operation vocabulary is fixture.setup, http.request and fixture.teardown. grant/revoke/role-change/expiry/tenant-transfer execution is absent. Parsing does not perform requests or evaluate predicates.
- [providers/fake.py](../packages/pact-core/pact_core/providers/fake.py): scripted candidate JSON and simulated provider failure only; no target execution, approval, runtime assertion or model inference.
- [core README](../packages/pact-core/README.md) expressly states these limitations. The [M2 report](M2_SECURITY_CONFORMANCE.md) records missing integrated runtime acceptance.

EV-0033 records a historical 77-test PASS with guarded component checks and a 2.444-second unit-suite duration. Those tests were **NOT RERUN** here. That duration is not fixture/executor/drift/temporal performance, and does not establish any M4 outcome, clean install or CI result.

## 3. Every M4 prerequisite and its exact DoD

| ID | Ledger status at intake | Dependencies | Exact architecture DoD | Actual required evidence |
|---|---|---|---|---|
| M4-01 | NOT_STARTED | M1-10/M3-03 | Comparing different fixture semantics is rejected or flagged; same pinned run can be reproduced | No persisted run fingerprints or reproduced run; M1-10 BLOCKED, M3-03 NOT_STARTED. NOT RUN. |
| M4-02 | NOT_STARTED | M4-01 | Compatible PASS->VIOLATION labels possible implementation drift; other transitions explicitly categorized | No comparator or rule/step evidence links. NOT RUN. |
| M4-03 | NOT_STARTED | M2-07/M4-02 | Historical contract immutable; v1 vs v2 output says approved policy change, not same-policy drift | No genuine reapproval, protected registry or tested revision comparison; M2-07 BLOCKED. NOT RUN. |
| M4-04 | NOT_STARTED | M0-03/M1-05 | Can express grant/revoke/role change via approved synthetic fixture operations only; unsafe transitions refused | Accepted restricted DSL exists; M1-05 provisional parser IN_REVIEW. No temporal vocabulary/capabilities or approved temporal fixture binding. NOT RUN. |
| M4-05 | NOT_STARTED | M4-04 | Repeatable before/after expected decisions; tear-down resets state; wrong/stale session permissions caught | No stateful adapter, genuine sessions, controlled clock or cleanup evidence. NOT RUN. |
| M4-06 | NOT_STARTED | M4-04/05 | Covers expiration, tenant transfer, sharing and role changes; ambiguous semantics are review-blocking | No temporal golden/property corpus or ambiguity-to-execution guard integration. NOT RUN. |
| M4-07 | NOT_STARTED | M2-02/M4-02 | Provides explanation/confidence; full-suite option always available; miss risk explicitly reported | No context reader (M2-02 BLOCKED), change mapper or full-suite execution option. NOT RUN. |
| M4-08 | NOT_STARTED | M4-02/03/05 | Code patch causes rerun to PASS without modifying contract; failed run remains accessible; human owns patch approval | No synthetic app, actual patch/rerun, immutable failed artifact or human patch-review evidence. NOT RUN. |

All eight direct prerequisites remain NOT_STARTED. M4-09 changes from NOT_STARTED to BLOCKED after intake only, with no implementation claim. All other WBS row statuses and exact dependencies/DoD are preserved.

Dependency graph: M1-10 + M3-03 -> M4-01 -> M4-02; M2-07 + M4-02 -> M4-03; M0-03 + M1-05 -> M4-04 -> M4-05; M4-04 + M4-05 -> M4-06; M2-02 + M4-02 -> M4-07; M4-02 + M4-03 + M4-05 -> M4-08; all M4-01..08 -> M4-09. M1-10 depends on the missing executor/evidence path; M3-03 depends on unimplemented CLI and blocked M1-12; M2-07 depends on blocked human-review/run-storage paths. A task prompt or scoped design direction does not close an edge.

## 4. Positive, adverse and failure gate cases

These are **planned verification oracles**, not generated execution fixtures or observed verdicts. Every row is NOT RUN.

| Case / trace | Positive control and expected result | Negative, boundary or failure control | Missing executable evidence |
|---|---|---|---|
| Compatible drift / AC-008 | Same authenticated policy/hash and compatible scenario/assertion/fixture/environment; reliable PASS -> VIOLATION yields possible implementation drift with rule/scenario/step evidence links | Different policy/version/profile, incomplete provenance or missing baseline cannot be proven drift; changed revision alone must not erase comparison semantics | Stored baseline/current runs, compatibility validator, observations/diff: NOT RUN |
| Approved policy revision / AC-009 | Real human approves exact v2; preserve v1 and both histories; label approved policy change separately | Unapproved draft, imported APPROVED, stale/replayed/edited receipt remains non-authoritative; never relabel as approved change | Genuine review/audit plus diff and actual v1/v2 runs: NOT RUN |
| Fixture/environment incompatibility / NFR-REL-001 | Identical pinned semantics compare; repeated run keeps immutable artifacts | Change fixture ownership/version, scenario/assertion schema or target environment; output NOT_COMPARABLE with reason, never proven drift | Fingerprint persistence and comparison: NOT RUN |
| Infrastructure failure / AC-006/017 | Valid fixture/auth and expected own-resource ALLOW provides working control | Missing/wrong token, setup/teardown failure, timeout/cancel, missing evidence or ALLOW 500 produces classified non-PASS, never compliance or an unverified violation | Executor/assertions, failure injection, evidence and cleanup: NOT RUN |
| Temporal stale-session flow / J-04 | Same authenticated old session: DENY -> GRANT -> ALLOW -> REVOKE -> DENY; repeat after reset reproduces ownership/state | Revoked permission still usable, wrong actor/token, invalid transition or undeclared capability fails safely; forbidden code/interpolation rejected | Approved synthetic capabilities, sessions, state adapter and independent answer key: NOT RUN |
| Temporal corpus / FR-DRF-006 | Controlled time and reviewed expiry, sharing, tenant transfer and role-change expectations | Exact expiry boundary, stale token, cross-tenant transfer and conflicting admin/ownership; unknown semantics NEEDS_REVIEW and no execution | Golden/property fixtures and review-blocking planner: NOT RUN |
| Preserved remediation / AC-005 | Actual reviewed synthetic code fix, same policy, own-resource control remains PASS; failed run/checksum stays accessible | Patch changes policy or overwrites baseline; decline comparison/acceptance, preserve history | Target revisions, human patch decision, immutable artifacts: NOT RUN |
| Impact mapping / FR-DRF-003 | Explain confidence/evidence and permit full-suite fallback | Missing dependency or uncertain route mapping must disclose miss risk; no unsupported coverage claim | Reader, mapper, runnable full suite: NOT RUN |

Golden fixtures are **NOT DELIVERED**: no temporal adapter/capability binding, reviewed answer keys, safe executable target or genuine approved policy run exists. Writing static desired outcomes would not demonstrate the deliverable. Failures are missing prerequisite/acceptance evidence; no runtime security test failure or exploit is asserted.

## 5. Runtime metrics and reproducibility

| Metric | Actual M4 result | Required measurement once eligible |
|---|---|---|
| Successful full-flow repetitions / equivalence | NOT MEASURED; 0 M4 runs executed | Record attempt count and verdict/evidence equivalence under pinned inputs; retain all failed/error/canceled attempts |
| Setup / scenario / teardown / comparison elapsed time | NOT MEASURED | Monotonic elapsed times with units, individual samples, median/range; separate cold startup and warmed repetitions |
| Requests / concurrency / timeout / cancellation | NOT MEASURED | Actual request counters and reviewed budget enforcement; stop/cleanup evidence for each exceeded limit |
| Peak memory / resource use | NOT MEASURED | Instrumented observation with collector/OS limitations stated; do not infer from wall time |
| Model calls / unapproved runner outbound requests | No M4 runtime exists to measure | Independently observe zero model calls and no unapproved destination in executable gate; documentation tooling is not transport isolation proof |
| Artifact checksums / preserved history | NOT MEASURED | Compare reproducible normalized material evidence and retained immutable run/artifact hashes; exclude presentation fields only |

Proposed bounded procedure after prerequisite closure: pin commit, policy/version/hash, scenario/schema/assertion profile, fixture version/semantics, environment and runner profile; independently review each golden oracle; obtain any remaining execution grant and reviewed budgets; execute at least five repeats per case with deterministic clock and fresh independent fixture state; preserve setup/teardown/cancel logs, every run ID and redacted evidence; measure each phase and disclose failed samples. Five repeats is a planning suggestion, not an accepted benchmark protocol, new scope grant or statistical accuracy claim. Performance pass thresholds and supported hardware/OS must be agreed before an acceptance claim. Broader comparative benchmarks/claims remain M6 scope.

Logs retained outside the repository at C:/Users/user/AppData/Local/Temp/PACT-M4-09-20261011-145f89f: inspect_gate.py, before.json, todo.before.md, inspection.json, validate_gate.py and validation.json. before.json records the full path/hash inventory, exact Git state and all 71 rows. These local scratch files are reproducibility aids, not immutable product evidence or authenticated authority.

## 6. Safe checks, adverse results and omissions

| Exact command / action | Actual result | Limit |
|---|---|---|
| git status --short --branch; git rev-parse HEAD; git log -3 --oneline; rg --files | Exit 0; clean main at the intake HEAD above, actual docs/pure packages inventoried | Cached Git tracking is not remote synchronization or CI proof |
| Task-scoped Get-Content / rg on PRD, AGENTS, workflow, skill, SECURITY, ARCHITECTURE, todo, all four ADRs and actual code | Read existing dependencies, authority/semantic gates and component limitations | Historical proposal paragraphs do not override genuine owner-scoped decisions |
| & 'C:/Program Files/Python314/python.exe' -I -B 'C:/Users/user/AppData/Local/Temp/PACT-M4-09-20261011-145f89f/inspect_gate.py' | Exit 0: 56-file/19-directory inventory, 71-row recount, all nine exact M4 DoD/dependencies, AST parsing of 23 Python files, closed operation list and absent runtime paths verified | Static test-method count 77; no unit, target or temporal test executed |
| PowerShell ConvertFrom-Json on before.json without -AsHashtable | Failed: .md and .MD are case-distinct keys; no repository mutation | Corrected with ConvertFrom-Json -AsHashtable, exit 0; metadata tooling failure, not a product verdict |
| & 'C:/Program Files/Python314/python.exe' -I -B 'C:/Users/user/AppData/Local/Temp/PACT-M4-09-20261011-145f89f/validate_gate.py' | Exit 0, PASS: 57 files, 55 original hashes and 70 other WBS rows preserved; 64 historical EV/BLK/ISS rows and 83 sections retained; exact M4 dependencies/DoD, recount, local links/case matrix and report digest verified | Documentation consistency only; no runtime acceptance. Final --final rerun binds the updated report digest in EV-0035 |
| git diff --check | Exit 0, no whitespace errors | Untracked report additionally checked by validate_gate.py |
| All eight gate case rows, temporal golden/property tests and M4 runtime metrics | NOT RUN / NOT MEASURED: implementations, approved inputs, scope and reviewed goldens absent | M4-09 DoD unmet; milestone NOT READY |
| Unit suite, pytest/lint/mypy/install/build, OS support matrix, remote CI, protected audit/human approval, real model/target tests | NOT RUN this session; unchanged component suite not substituted for gate and workspace configuration absent | No CI, local trust guarantee or security sign-off inferred |

## 7. Ledger integrity and recalculated totals

At intake the authoritative 71 WBS rows yield **6 DONE, 7 IN_REVIEW, 16 BLOCKED, 42 NOT_STARTED**, matching the cached board. An initial scratch scan accidentally included the illustrative M1-07 row under §9; it was corrected to count only the WBS section. The actual M1-07 task remains BLOCKED; the example is not task evidence. Two tracker-generation attempts stopped on count assertions before writing; the corrected recount is retained.

EV-0034's table entry references detailed checks/digests below, but there is **no EV-0034 detailed section or storage-decision journal** in the intake tracker. Its current snapshot still says ddf945d and dirty work although intake is now clean 145f89f. The owner storage direction and four document revisions do exist; the unrecorded preservation/digest/test assertions are not adopted as verified evidence. This report records the discrepancy without fabricating prior check execution or repairing those documents outside M4-09.

After recording only M4-09 as BLOCKED:

| Milestone | Total | NOT_STARTED | IN_PROGRESS | BLOCKED | IN_REVIEW | DONE | DEFERRED |
|---|---:|---:|---:|---:|---:|---:|---:|
| M0 | 9 | 1 | 0 | 0 | 6 | 2 | 0 |
| M1 | 12 | 0 | 0 | 8 | 1 | 3 | 0 |
| M2 | 9 | 0 | 0 | 8 | 0 | 1 | 0 |
| M3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| M4 | 9 | 8 | 0 | 1 | 0 | 0 | 0 |
| M5 | 16 | 16 | 0 | 0 | 0 | 0 | 0 |
| M6 | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| TOTAL | 71 | 41 | 0 | 17 | 7 | 6 | 0 |

M4: **0/9 DONE (0%) — NOT READY**. All WBS: **6/71 DONE (8.5%)**. No DONE or approval status is added. Intervening M3/M4 task prompts do not establish completed work; this bounded session does not execute their implementations or a separate M2/M3 milestone review.

## 8. Human gates and next eligibility

Accepted ADR-0001's specified restricted DSL/canonicalization choices and accepted canonical data/opaque-ID/job conventions remain settled. The developer-selected dedicated Audit Authority/append-only log/independent signed-checkpoint storage direction is also settled within its explicit scope. None is reopened here.

Missing gates remain: final M0-02 threat-boundary sign-off; fixture/runner ADR-0002 and concrete temporal capability/denial/transport/containment review; full ADR-0003 and protected human identity/user presence plus concrete signing/freshness/activation/recovery verification; tooling ADR-0004/acquisition/workspace evidence. Policy v2 and patch approval require genuine human actions on exact reviewable content; target execution requires separate scope. No actual policy v2, patch or executable target is ready to approve in this gate. Existing pending questions are not repeatedly submitted; no new M4-09-specific owner decision or boundary crossing is attempted.

Unblock by completing actual M4-01..08 and upstream runtime/approval dependencies, then supplying reviewed goldens, genuine safe execution inputs, retained per-case evidence and measured performance. A dependency waiver or mock-only exception alone cannot make this gate DONE. [ISS-0003](../todo.md) is dependency-ready for safe documentation work only, not started; no new M4 implementation ID is dependency-ready (M4-04 still depends on M1-05 IN_REVIEW). M6-01 remains gated on M4-09. Await the appropriate bounded task/remaining genuine reviews before advancing.
