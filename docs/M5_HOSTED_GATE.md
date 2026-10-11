# M5-16 — Hosted E2E and deployment security gate

> Date: 2026-10-11
> Gate result: **NOT READY — M5-16 BLOCKED; hosted staging execution DISABLED**
> Trace: PRD §§5,11,15; Architecture §7 M5-16 and §8 G5
> Evidence: todo.md EV-0051 / BLK-0042
> Scope: repository inspection, documentary gate and conditional runbook only

## 1. Intake and exact completion rule

Allowed changes: this report and M5-16 tracking/evidence/milestone/session entries in [todo.md](../todo.md). Source, tests, schemas, dependencies, ADR status, existing evidence and other task rows remain untouched. Temporary inspection/check scripts reside outside the repository. No accounts/keys/services/DB/container/cloud provisioned, no deployment/listener, real credentials or private platform configuration read, target/model/GitHub request, privileged test or Git mutation.

Architecture dependencies: **M5-03..15** (thirteen tasks). Deliverable: **Tested deploy/runbook + threat-review findings**. Exact DoD:

> J-01..05 on supported hosted profile; full RBAC/SSRF/runner/evidence tests pass; no critical/high unresolved release blockers

| DoD clause | Actual evidence | Result |
|---|---|---|
| J-01..05 on supported hosted profile | No hosted implementation, runnable journeys, supported profile or staging authorization recorded | NOT RUN |
| Full RBAC/SSRF/runner/evidence tests pass | No hosted suites/backend/runner or evidence pipeline; pure component tests do not substitute | NOT RUN |
| No critical/high unresolved release blockers | Mandatory high-impact trust/control proofs and final independent review absent; cannot establish clearance | NOT SATISFIED |

Documentation is not a tested deployment or a passing hosted gate. Runtime work stops until prerequisites, implementation, concrete staging grant and required reviews exist. A passing future gate still requires a separate genuine human deployment/release decision.

## 2. Actual repository and approvals

Git initialized: main, HEAD **145f89f6c1123d6ae245390a6bd83e55c05efcbe**. At intake:58 project files/19 directories excluding root and .git; modified todo.md and untracked docs/M4_REPEATABILITY_GATE.md/docs/adr/0007-hosted-trust.md preserved. This report adds one Markdown file: expected final59files/19directories.

Actual implementation: pure domain entities/enums/contract normalization, expressly untrusted approval state, provisional scenario parsing and provider port/fake.23 Python files and77 test methods statically inventoried; tests NOT RERUN for this documentation gate. Historical unit PASS evidence in EV-0033/0049 remains component evidence only, not authentic approval, RBAC, runner containment, E2E or CI. No pyproject/lock/CI/deployment manifest, hosted API/UI/OIDC/RLS, PostgreSQL/object/audit store, durable coordinator, runner/executor, evidence redactor or drift implementation.

Code-supported observations: [approval_model.py](../packages/pact-core/pact_core/domain/approval_model.py) require_authenticated_approval always rejects modeled claims; serialized APPROVED is not authenticated approval. [parser.py](../packages/pact-core/pact_core/scenarios/parser.py) parses fixture.setup/http.request/fixture.teardown without executing requests or temporal operations. [fake.py](../packages/pact-core/pact_core/providers/fake.py) uses scripted candidates/errors; it cannot establish provider egress or real authorization. See [core README](../packages/pact-core/README.md) for explicit limitations.

ADR-0001 specified DSL choices ACCEPTED. ADR-0002/0003/0004/0007 remain PROPOSED; ADR-0006/0008 absent. M0-02 final developer security sign-off absent. Canonical DATA_MODEL/opaque IDs/attempt conventions and dedicated Audit Authority/append-only history/independent signed checkpoints retain prior scoped acceptance; none grants execution or approves all hosted design. No unchanged owner decision requested again. Older ADR/security intake assertions saying no code/ADRs exist are historical and inconsistent with the current tree; they cannot be used as current status. EV-0034's detailed-evidence gap remains unresolved.

## 3. Every direct dependency and exact DoD

| Task | Ledger status | Dependencies | Exact architecture DoD | Evidence and limitation |
|---|---|---|---|---|
| M5-03 | BLOCKED | M5-02 | Org A cannot enumerate/read/change Org B contracts, runs or artifact handles; ID tampering rejected and audited | EV-0038/BLK-0029; runtime DoD NOT RUN |
| M5-04 | BLOCKED | M5-03 | OpenAPI schema validated; unauthorized API action fails; create/run duplicates do not create unsafe duplicate executions | EV-0039/BLK-0030; runtime DoD NOT RUN |
| M5-05 | BLOCKED | M5-02/03 | Org-crossing artifact IDs denied; secrets redacted; deletion/retention respects policy and legal holds; export tested | EV-0040/BLK-0031; runtime DoD NOT RUN |
| M5-06 | BLOCKED | M5-04 | Worker crash never marks PASS; cancellation stops/safely times out runner; idempotency protects repeated messages | EV-0041/BLK-0032; runtime DoD NOT RUN |
| M5-07 | BLOCKED | M5-01/06 | Revoked runner cannot fetch jobs; unauthorized host/network execution fails; jobs cryptographically/operationally bound to project, scope and contract | EV-0042/BLK-0033; runtime DoD NOT RUN |
| M5-08 | BLOCKED | M5-07 | Tests show no prohibited host mount/socket, redirect escape, uncontrolled DNS/IP destination, unauthorized writes or report exfiltration | EV-0043/BLK-0034; runtime DoD NOT RUN |
| M5-09 | BLOCKED | M5-04 | Signed-in developer can list own projects; unauthorized org data not rendered; keyboard nav/labels assessed | EV-0044/BLK-0035; runtime DoD NOT RUN |
| M5-10 | BLOCKED | M5-09/M5-03 | Reviewer explicitly approves exact hash via backend; AI/caller cannot impersonate reviewer; intentional changes create new version | EV-0045/BLK-0036; runtime DoD NOT RUN |
| M5-11 | BLOCKED | M5-05/09 | Displays PASS, VIOLATION, INCONCLUSIVE, ERROR, SKIPPED, CANCELED without misleading green; run reproductions linked | EV-0046/BLK-0037; runtime DoD NOT RUN |
| M5-12 | BLOCKED | M5-04/06 | Invalid signature/replay/mismatched repository rejected; checks include evidence link and non-PASS statuses; advisory default | EV-0047/BLK-0038; runtime DoD NOT RUN |
| M5-13 | BLOCKED | M5-12/M5-03 | Only authorized admin enables blocking; missing runs/infra errors not silently green; documented safe rollback of gate | EV-0048/BLK-0039; runtime DoD NOT RUN |
| M5-14 | BLOCKED | M5-03/M2-01 | Same draft-or-error conformance cases pass; provider egress consent enforced; no unapproved fallback or hidden bills | EV-0049/BLK-0040; runtime DoD NOT RUN |
| M5-15 | BLOCKED | M5-04/06 | Cost/run limits enforced; incident can be correlated without raw secrets; quotas isolate noisy organizations | EV-0050/BLK-0041; runtime DoD NOT RUN |

Every direct dependency remains BLOCKED, zero of thirteen DONE. The authority/persistence chain is M0-02/M3-08 -> M5-01, M1-10/M5-01 -> M5-02 -> M5-03 -> M5-04 -> M5-06. Storage/UI/integration/runner/provider/operational branches converge at M5-16. Thus resolving only a staging address or one branch cannot satisfy the gate. M1/M2/M3/M4 integrated acceptance also lacks requisite runtime evidence. See immutable earlier entries rather than treating a later task prompt as closure.

Milestone recalculation after this intake: M5 **16 BLOCKED,0 DONE,0 IN_REVIEW,0 IN_PROGRESS,0 NOT_STARTED**; whole WBS **71 =6DONE+7IN_REVIEW+33BLOCKED+25NOT_STARTED**. Local ISS rows are excluded from WBS totals. M6 tasks remain NOT_STARTED; no next task runs.

## 4. J-01..05 and security test design — PLANNED ONLY

These are required future assertions and evidence, not executable test names or observed outcomes. Each needs owner-reviewed expectations, the actual supported build/profile and independent synthetic identities; no AI or test double supplies trusted human approval.

| Planned family / level | Positive evidence | Negative, boundary or failure evidence | Actual result |
|---|---|---|---|
| HE-01 J-01 / hosted E2E; AC-001..007/011/013/014 | Own-org onboarding, bounded repository provenance, DRAFT -> genuine exact-hash review, independent fixtures, approved target, sanitized immutable baseline with pinned revision | Foreign IDs/extra reviewer fields, forged/replayed/stale approval, undefined scope, bad fixture/token and injected source cannot execute; provider disabled rerun valid | NOT RUN |
| HE-02 J-02 / drift and remediation; AC-004/005/008 | Compatible same-policy PASS -> VIOLATION links actual rule/step evidence; authorized patch restores PASS and own-tenant ALLOW; original failing run retained | Changed environment/fixture/schema NOT_COMPARABLE; missing evidence/infra failure not drift/PASS; patch cannot rewrite expected policy or failing history | NOT RUN |
| HE-03 J-03 / policy revision; AC-003/009 | New immutable draft version/diff, deliberate qualified human reapproval, policy-change label, old version/evidence retained | Caller/AI/button/import cannot approve; tampered hash/revoked reviewer/replay fails; unapproved v2 never mislabeled approved policy change | NOT RUN |
| HE-04 J-04 / stateful target lifecycle | Same recipient old session DENY -> GRANT -> ALLOW -> REVOKE -> DENY under approved lifecycle semantics; verified reset | Wrong actor/session, expired share, role/tenant transfer, failed cleanup and unknown semantics cannot inherit access or silently execute; state contamination detected | NOT RUN |
| HE-05 J-05 / failure and ambiguity; AC-006/010/017 | Precise NEEDS_REVIEW questions, typed fixture/transport failures, explicit cancellation/scope outcomes and coverage | Malformed/conflicting policy, missing resource/login, ALLOW500, incomplete observation, timeout/crash/store failure never PASS or invented violation; unresolved rules yield zero execution | NOT RUN |
| HE-06 RBAC/IDOR / actual API+PostgreSQL+browser; AC-014 | Valid Org A own-project access, least-privilege app role without BYPASSRLS, authenticated context and private scoped handles | Org B ID tampering/enumeration/read/write/run/artifact/pagination/cache paths rejected with durable denial audit; stale/invalid signature/session/current membership blocked | NOT RUN |
| HE-07 Scope/SSRF / isolated disposable transport; AC-007/015 | Authorized origin and resolved destination only, safe approved relative path | Out-of-scope redirects/protocol/port/path, DNS/IP swap/rebinding and credential forwarding blocked before connection; explicit transport counters and network boundary evidence; no live third-party probes | NOT RUN |
| HE-08 Runner / disposable supported isolation | Scoped short-lived runner/job binding, actual fs/network/mount/socket/privilege/resource/cancel/cleanup controls | Revoked/cross-project/stale lease/replayed/forged result, forbidden host mounts/socket/write, escape destination/budget exhaustion denied; no host privilege escalation tests | NOT RUN |
| HE-09 Evidence/privacy / all actual sinks; AC-011 | Same normalized verdicts/coverage/reproduction/checksums in UI/API/JSON/HTML; approved retention and legal holds | Seeded fake keys/token/cookie/private fields absent from logs/artifacts/trace/errors/queue/export; stored/DOM injection escaped, foreign/expired downloads denied, tampering detected | NOT RUN |
| HE-10 Recovery/audit/jobs / protected authority and backend | Anchored required review events, independently trusted latest checkpoint, recoverable DB relationships, fenced idempotent attempts | Event modification/gaps/rollback/signature/store outage/key access/audit-write failure disable approvals; worker crash/retry/duplicate/recovery cannot produce PASS, overwrite history or extend scope | NOT RUN |
| HE-11 Operations/CI/provider / shared services | Bounded noisy-org quotas, incident correlation, advisory signed scoped GitHub event and local fake provider conformance | Bad webhook/replay/repository/installation, missing/inconclusive runs, foreign quota context, secret telemetry and unapproved provider/fallback cause no dispatch/export; no real GitHub or paid calls | NOT RUN |
| HE-12 Deployment reproducibility / approved disposable profile | Fresh pinned lock/build/migration/start/full-flow/cleanup/recovery run on exact documented OS/runtime, accessible primary persona flow and sanitized logs | Supply-chain/profile mismatch, missing tests, rollback failure, failed cleanup, unsupported claims or unresolved critical/high finding blocks release; no successful installation/CI assertion from static inventory | NOT RUN |

The complete mandatory P0 AC set (AC-001..013 and015..017) plus hosted AC-014 must have appropriate integrated evidence; a subset, passing schema tests or unexecuted planned cases cannot establish release readiness. Mock denial alone cannot prove current authorization, PostgreSQL RLS or network/container isolation.

## 5. Threat-review findings and factual release blockers

No hosted vulnerability was reproduced: no hosted system was executed. The following are **confirmed missing prerequisites/control evidence and approvals**, with high-impact threat implications; they are not assigned invented exploit severity/CVSS or a claim about a running service. Absence of a reproduced exploit is not clearance of the critical/high review gate.

| Finding / blocker | Repository-supported fact and risk | Measurable closure evidence |
|---|---|---|
| HG-01 Prerequisites | All13 direct tasks BLOCKED; hosted design/tooling/install/persistence baseline absent | Each exact dependency DoD and relevant accepted design independently evidenced; clean install/build/migration profile measured |
| HG-02 Identity/approval/tenant authority | No current OIDC/RBAC/RLS, human-presence review or protected registry; M0-02 unsigned | Genuine human exact-hash review and anchored audit; all cross-org/project indirect access and replay/revocation negatives pass; reviewer signs relevant boundary |
| HG-03 Scope/containment | No authorized scope guard/runner/fs/network policy or transport; proposed isolation not validated | Approved staging grant and reviewed supported containment; actual blocked-before-request, destination, credential and budget checks plus verified cancellation/cleanup |
| HG-04 Privacy/evidence/history | Redaction/storage/retention/traces and compatible drift missing | Canary suite across all sinks, immutable checksum/history and permission tests; real compatible drift vs policy change/NOT_COMPARABLE demonstrated |
| HG-05 Recovery/availability/operations | Durable jobs/audit/checkpoints/quota/integration controls absent | Injected crash/store/signature/rollback/replay/cancellation cases yield honest non-success, preserved forensic evidence and human-authorized recovery; noisy-org isolation measured |
| HG-06 Staging authorization/profile | No concrete supported authorized staging profile/target or cleanup grant recorded | Responsible operator/reviewer records bounded non-production org/project/origins/resolved-network/data/budget/time/cleanup grant and independent controls verified before any request |
| HG-07 Test/review/release evidence | Hosted E2E, full security suites, fresh deploy/recovery and critical/high clearance NOT RUN; no real release approval | Retained actual logs/artifact hashes/command exits for all required cases; independent reviewer triages every critical/high item with retest evidence; genuine scoped human release decision on exact candidate |

Unknown/ERROR/INCONCLUSIVE/SKIPPED/CANCELED/missing evidence remains visibly incomplete coverage and cannot become green security status. Genuine observed VIOLATION blocks the relevant release scope until fixed and retested without changing approved expectations. No risk waiver or silent dependency bypass is issued by this report.

## 6. Conditional runbook — NOT EXECUTED

No hosted startup/deploy/test commands exist in the current workspace, so none are fabricated here. Only inspection/check commands actually used are listed in §7. Populate an executable runbook from the reviewed installed build when it genuinely exists.

1. Close the exact dependency and threat-boundary reviews. Confirm current staging grant, designated reviewer/operator, exact candidate commit and dirty-tree treatment, pinned dependency/schema/profile versions, scope fixture and limits. Read-only grant inspection must not acquire or print secrets. Refuse missing/stale permissions; do not provision to bypass missing prerequisites.
2. Before any authorized start/request, independently verify isolation, fail-closed egress/allowlist/DNS/redirect, protected identity/reviewer/audit authorities, private stores and redaction. Record initial fixture/state hashes and preservation/cleanup plan using synthetic data. Do not expose vulnerable fixture publicly or use real customer data.
3. With explicit bounded staging permission and implemented commands, run fresh installation/migration and safe own-project controls first, then all HE-01..12 and J-01..05 with immutable evidence, exact command/exit/negative case/call counts. Model egress stays OFF unless separately consented; drafting uses fakes where appropriate, runtime verifier never needs inference. GitHub writes, provisioning, privileged operations and production targets remain separate gates.
4. Stop on scope/credential/identity/containment/privacy/integrity failure; cancel/fence jobs and verify approved cleanup. Preserve redacted failing history; no automatic rollback/reset of trusted genesis, no secret-bearing diagnostic export and no unattended privilege expansion. Record NOT RUN/unknowns and recovery responsibility honestly.
5. Reconcile fixture reset, remaining processes/leases/resources, audit continuity, artifact hashes and reproduction identifiers. Cleanup failure is an unresolved blocker. Write measured test/runtime/resource results without extrapolating toy performance or compliance.
6. Independent human security reviewer evaluates exact candidate/evidence and residual findings. Do not clear critical/high issues without accepted resolution and genuine retests. Present a concrete reviewed deployment/release candidate and rollback plan for action-specific human approval only after this work exists. A gate result never itself authorizes production or changes repository protection.

## 7. Actual safe checks and limitations

- `git status --short --branch`: exit0; main, modified todo.md, two pre-existing untracked docs as above. `git rev-parse HEAD`: exit0, exact HEAD above. `rg --files --hidden -g '!.git'`: exit0, actual paths inspected.
- `& 'C:/Program Files/Python314/python.exe' -I -B 'C:/Users/user/AppData/Local/Temp/PACT-M5-16-20261011-145f89f/intake.py'`: exit0, Python3.14.4;58files/19dirs at intake,23 ASTs/77 statically counted test methods,71 ledger rows. Isolated importlib.metadata only: OpenTelemetry API/SDK, prometheus-client, redis, SQLAlchemy, FastAPI, Pydantic and pytest NOT VISIBLE. This is environment-specific, not a machine-wide installed-software inventory. No package import or installation.
- Targeted `Get-Content`/`rg` read source/spec/evidence. Initial `rg ... docs/adr/*.md` failed with Windows path-glob error123 (later shell commands still succeeded); corrected `rg ... docs/adr -g '*.md' -g '!examples/**'` succeeded. Do not record the initial search as a successful ADR inventory.
- `& 'C:/Program Files/Python314/python.exe' -I -B 'C:/Users/user/AppData/Local/Temp/PACT-M5-16-20261011-145f89f/check_gate.py'`: exit0;59files/19dirs,57 prior non-tracker hashes/70 other task rows/96 register rows/116 historical evidence-journal sections and HEAD preserved;13 dependency DoDs match architecture,12 families remain NOT RUN,7 blockers present, local references resolve, eight simulated report/ledger errors detected. Report trailing-whitespace/NUL checks included. `git diff --check`: exit0 for tracked diff. Validation repeated after recording results; report raw SHA-256 recorded in todo.md EV-0051. These checks do not satisfy E2E/security DoD.
- **NOT RUN:**J-01..05, HE-01..12, all hosted RBAC/RLS/SSRF/runner/evidence/approval/privacy/recovery/drift/quota/provider/CI tests, fresh install/deployment/rollback/benchmark, historical77 unit tests, formatter/linter/type checks (no configured baseline), remote CI, external security/provider/API calls and real human contract/deployment/release approval. No runtime metrics measured, no validated supported hosted OS/profile or no-critical/high certification.

## 8. Owner decision and next eligible work

**Direct developer decision — 2026-10-11:** hosted staging **DISABLED — PENDING PREREQUISITES**. No existing disposable hosted profile is provided or authorized. Recorded in todo.md EV-0052, superseding the pending-question state of the original EV-0051 report. No staging configuration/runtime exists or was activated; no profile IDs, target origins or authorization records invented. No cloud/services/provisioning/deployment/hosted E2E/external targets/privileges/contract approval/provider egress authorized. Do not request this unchanged decision again.

Before any future activation request, document and independently verify:

- Accepted architecture/security ADRs and the actual hosted implementation prerequisites/DoDs.
- A concrete disposable staging proposal identifying environment, non-secret configuration and bounded project/organization scope; independent human profile approval must precede execution.
- Explicit allowlisted target origins, resolved network boundaries and isolated synthetic test data.
- Enforced resource, time and cost limits; verified cleanup/reset and recovery procedures.
- Responsible operator and security reviewer; verified runner isolation, current authorization, genuine human approval and protected audit controls.

Only when these prerequisites are satisfied and the concrete proposal exists should the developer receive a new action-specific activation request with environment identity/configuration/origins, operator/reviewer, testing bounds, limits and cleanup plan. Separate provisioning/deployment/release or egress grants are never inferred. The safe-continuation permission covers local unit/integration/mock tests, synthetic fixtures in already-authorized environments, templates/docs/offline CI and reviews within actual workflow dependencies; it is not a new target grant or dependency waiver. Prior unchanged audit/ID/model directions and remaining ADR/identity/runner/retention/quota decisions stay open without resubmission.

ISS-0003 canonical tracker-reference reconciliation is complete under this safe continuation; its exact checks/status are recorded in todo.md EV-0053. No new dependency-ready implementation WBS identified. M6 remains gated by its own dependencies. M5 remains **NOT READY**, M5-16 **BLOCKED**, J-01..05 and full hosted suites **NOT RUN**; no release boundary crossed. Earlier actual check results in §7/EV-0051 are historical; raw digest of this updated report and follow-up checks are recorded in EV-0053.
