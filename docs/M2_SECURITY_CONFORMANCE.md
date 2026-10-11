# M2-09 security and conformance review — 2026-10-11

Status: **BLOCKED / NOT READY**. This is a component review and test report, not human security sign-off, contract approval or permission to execute targets. Reviewer/author: Codex; the designated human security reviewer is the repository developer. No final human review is recorded. Trace: PRD §§11–12; exact Architecture DoD: “Relevant AC-001/002/003/010/013 pass; unresolved ambiguity never triggers tests.”

## 1. Scope and actual prerequisites

Read PRD.MD, AGENTS.md, workflow.md, Architecture/SECURITY/todo, relevant ADRs and actual domain, scenario and provider code/tests. Applied repository testing/security-review skills in review mode. Allowed edits: this report and todo.md only. No source behavior, schemas, dependencies, approvals, real secrets, execution scope or retention changed.

Git: dirty main tracking cached origin/main; HEAD `ddf945dad8e7aaab0b052a22f37f57d3e0373295`. Existing work preserved; no remote or mutating Git command. Intake: 55 files/19 directories, excluding root/Git. Final: 56 files/19 directories; this Markdown report is the only new project file.

| Required dependency | Actual status | Evidence and missing implementation |
|---|---|---|
| M2-01 | DONE | EV-0025; typed draft/error port and scripted offline fake, no live provider. |
| M2-02 | BLOCKED | EV-0026/BLK-0018; repository context/privacy reader absent, M0-02 final sign-off pending. |
| M2-03 | BLOCKED | EV-0027/BLK-0019; OpenAI adapter absent, SDK acquisition/tooling and privacy gates unresolved. |
| M2-04 | BLOCKED | EV-0028/BLK-0020; requirement compiler/seeded merchant integration absent. |
| M2-05 | BLOCKED | EV-0029/BLK-0021; answerable clarification/review workflow absent; pure conflict detection exists. |
| M2-06 | BLOCKED | EV-0030/BLK-0022; protected authenticated human review/receipt absent. |
| M2-07 | BLOCKED | EV-0031/BLK-0023; trusted registry/audit and protected storage/recovery absent. |
| M2-08 | BLOCKED | EV-0032/BLK-0024; approved offline verifier, executable fixtures and measured baseline absent. |

ADR-0001 specified DSL choices are ACCEPTED. ADR-0002 fixture/runner v0.2, ADR-0003 human approval v0.1 and ADR-0004 tooling v0.1 remain PROPOSED. M0-02 remains IN_REVIEW. Scoped accepted data/ID/job conventions are unchanged; they do not approve contracts or targets. This review does not close prerequisites or replace the developer's pending decisions.

## 2. Executed checks and adverse cases

Installed Python 3.14.4 and standard library only. A scratch launcher passed ONLY `SystemRoot`, `TEMP`, `TMP` to the audited suite; no provider configuration/credential environment was inherited, and the caller environment was unchanged. No real secrets were inspected/deleted. The wrapper inspected exact existing child scripts from their test ASTs and admitted only their complete commands with isolated Python, expected fixture arguments and temporary directories.

| Actual command / check | Result |
|---|---|
| `git status --short --branch`; `git rev-parse HEAD`; `rg --files --hidden -g '!.git/**'` | Exit 0; actual dirty state/files/dependencies inspected; no remote. |
| `& 'C:/Program Files/Python314/python.exe' -I -B 'C:/Users/user/AppData/Local/Temp/PACT-M2-09-31e40528-7a88-43f2-baf0-d18933245c32/run_review_checks.py'` | Exit 0; runs the next command with minimal child environment; validates saved summary and counts. |
| `& 'C:/Program Files/Python314/python.exe' -I -B 'C:/Users/user/AppData/Local/Temp/PACT-M2-09-31e40528-7a88-43f2-baf0-d18933245c32/guarded_existing_suite.py'` (launched by the scratch launcher) | 77 tests PASS; zero failures/errors/skips. Uses unittest discovery/TextTestRunner over all six existing test modules. No new repository tests added. |
| Parent Python audit during that suite | Zero socket/DNS/HTTP/native-call attempts; zero provider/client SDK import attempts; no blocked real-suite events; three exact inspected child scripts admitted. Those children independently install rejection guards and passed. |
| Five simulated audit events | Socket connect, HTTP connect, native library load, OpenAI import and unknown child command rejected. These are callbacks via sys.audit only, separate from suite counters; no real connection/import/process attempted. |
| Preservation/ledger/report and `git diff --check` | Exact final results recorded in todo.md EV-0033 after checks. These are documentation checks, not runtime security certification. |

| Existing module | Actual tests | Positive/adverse behavior exercised |
|---|---:|---|
| test_domain | 19 PASS | Strict typed actor/tenant/resource/relation/rule boundaries; missing/unknown/privileged fields and invalid references rejected. |
| test_contracts | 20 PASS | Canonical valid bodies/digests/round trips; malformed/duplicate/unsupported/forged input and possible decision/profile conflicts rejected; independent synthetic conflict worlds. |
| test_approval_model | 9 PASS | Untrusted transition/history/version/hash invariants; imported, forged, stale, replayed and transplanted claims never satisfy approval guard; edits retain old in-memory history. |
| test_scenarios | 17 PASS | Provisional typed mock grammar; unknown operations/privileged fields/undeclared references/malicious strings/template/origin/path attempts rejected; seeded mutation/property checks. No scenario executes. |
| test_providers | 10 PASS | Scripted valid DRAFT; malformed/conflicting/privileged/cross-project output -> typed non-success; simulated timeout/transport failure; fixed errors, bounded input, safe repr/log behavior and no SDK/generation side effects. |
| test_imports | 2 PASS | Domain stdlib dependency direction and audited fresh import/normalization/untrusted-state construction; no approval authority. |

No executed test failed. There is consequently no failing product case reproduced by this suite. Required missing acceptance tests below still block advancement; a unit-pass total cannot make them PASS.

Evidence directory: `C:/Users/user/AppData/Local/Temp/PACT-M2-09-31e40528-7a88-43f2-baf0-d18933245c32`. Retained `before.json`, `todo.before.md`, `guarded_existing_suite.py`, `run_review_checks.py`, `guarded-tests.txt` (all test names/results), `guarded-summary.json` (counts/guard observations), `review-results.txt` and final `check_scope.py`/`scope-results.txt`. Scratch artifacts are local evidence, not installed product commands or portable CI results.

## 3. Acceptance and security coverage

“Component evidence” means executed checks of actual local code. “NOT RUN” means the required integrated acceptance proof is absent, not a successful security verdict.

| Required AC | Exact required behavior | Actual evidence | Acceptance result / release blocker |
|---|---|---|---|
| AC-001 | Seeded FastAPI merchant app/business rule produces valid same-tenant ALLOW and cross-tenant DENY draft. | Typed candidate fixtures and fake output validate. | **NOT RUN**: demo/context/compiler absent (M1-04, M2-02/03/04). Close only with genuine seeded journey and provenance; scripted fixture text is not requirement compilation. |
| AC-002 | Unreviewed model/tool execution rejected **and audit entry written**. | Forged/model states rejected by universal approval guard; closed schemas reject privileged extras. | **PARTIAL component evidence; full AC NOT RUN**: execution/audit producers absent (M2-06/07, M1-07/08). Require rejected application entry-point attempts, zero unauthorized requests and durable denial audit. |
| AC-003 | Permitted actual human approval creates immutable hash-bound version. | Untrusted immutable model/hash tests only. | **NOT RUN**: protected review/broker/identity/storage absent. Require developer action through real protected flow plus forged/replay/tamper/permission negatives; AI must not perform the positive approval. |
| AC-010 | Malformed/conflicting model output fails safely or NEEDS_REVIEW; no unauthorized test. | Existing normalizer and FakeProvider reject malformed output/conflicts; no model-provided approval accepted. | **PARTIAL component evidence; full AC NOT RUN**: compiler/questions/execution integration absent. Require reviewed clarification behavior and proof of no execution on all ambiguous/error paths. |
| AC-013 | Saved approved suite reruns without configured provider/inference. | Credential-free fake/domain/parser imports and generation pass, scoped audit observations above. | **NOT RUN**: no approved suite/executor/fixtures/measured baseline. Require genuine compatible baseline/rerun equality and zero model calls, with history/cleanup preserved. |

| Review area | Executed positive/negative checks | Unverified boundary and next necessary checks |
|---|---|---|
| Prompt injection | Scenario malicious string leaves/unknown operations rejected; closed contract/provider output cannot supply approval or commands. | Repository comments/prompts, context selection and actual model adapter absent. Test synthetic injected source/tool responses cannot alter capabilities, include excluded files, approve or authorize execution once those paths exist. String rejection is not proof of a live prompt compiler. |
| Provider failure | Fake transport/timeout/malformed output -> typed non-success, no fallback or authoritative draft. | Real SDK adapter/retry/cost/egress OFF implementation absent. Mock conformance must precede any separately authorized live request; live testing not needed or authorized here. |
| Forged approval | Imported APPROVED/receipt/reviewer fields rejected; all untrusted state rejected by approval guard; stale/hash/project replay model tests pass. | No authenticated service/durable nonce/audit. Test actual callers, current permissions, protected presence, concurrency/crash/rollback and tamper once accepted mechanisms exist. |
| Privacy/redaction | Existing fake-provider tests omit synthetic request/completion canary from repr, fixed messages and observed provider log output. | No context filter, evidence redactor, HTML/JSON report serializer or exception/export boundary. AC-011/NFR-SEC-002/PRV-001 **NOT RUN** end to end. Test seeded fake tokens/private fields absent from logs/artifacts/exceptions/prompts, preserving useful lineage and failing closed on uncertain sanitization. |
| Scope/SSRF | Provisional parser rejects untyped URL/origin/template paths and undeclared mock references. | No scope grant, DNS/peer/redirect transport, budget/cancellation or runner. AC-007/015/NFR-SEC-005 **NOT RUN**. Test synthetic allowlisted destination, redirect/IP swap/DNS/path/credential leakage and limits before any real request. |
| No-provider behavior | Pure/fake suite runs with no inherited provider credentials; audited scoped calls/imports show no network/client SDK activity. | Actual approved deterministic verifier absent. Credential absence alone is neither execution permission nor evidence of runtime offline verdict equivalence. |
| Ambiguity versus execution | normalize_contract raises NEEDS_REVIEW on possible conflict; fake returns GenerationError, never authoritative CandidateDraft. | No application planner/executor exists to spy on. Require assertion/runner invocation count zero for conflict, undefined ownership/admin/tenant semantics and malformed output; no guessed fallback policy. |

## 4. Grounded findings and open high-risk issues

These are implementation/coverage blockers, not claims of reproduced exploits in components that do not exist.

| Finding | Confidence / impact | Source and remediation |
|---|---|---|
| Review/authorization trust root and audit are absent. | **Confirmed absence / HIGH gate blocker**, BLK-0022/23. | [approval_model.py:210](../packages/pact-core/pact_core/domain/approval_model.py#L210) universally rejects approval; it provides no authenticated receipt. Preserve that fail-closed guard. Close ADR-0003/M0-02 review and mechanism decisions, implement protected flow/store, then AP-01/05–15/18 and real human positive. |
| Privacy/context/evidence proof cannot be completed. | **Confirmed absence / HIGH gate blocker**, BLK-0014/18. | Actual tree has no context reader/evidence pipeline; [provider tests:127](../packages/pact-core/tests/test_providers.py#L127) cover only fake repr/log canary behavior. Add reviewed scoped context/evidence implementations in their tasks and test every actual sink; do not claim general redaction from silence. |
| Execution-scope and approved-offline verification proof are absent. | **Confirmed absence / HIGH gate blocker**, BLK-0012/13/17/24. | No execution adapter/demo/baseline; [scenario parser:153](../packages/pact-core/pact_core/scenarios/parser.py#L153) validates data only. Close actual fixture/transport/golden suite prerequisites and scope authorization before controlled verification; preserve non-PASS errors/cleanup evidence. |
| Candidate conflict/authority separation is implemented locally but lacks application conformance. | **Code-supported and tested / integration gap**, BLK-0020/21. | [contracts.py:226](../packages/pact-core/pact_core/domain/contracts.py#L226), [fake.py:31](../packages/pact-core/pact_core/providers/fake.py#L31), [port.py:54](../packages/pact-core/pact_core/providers/port.py#L54). Keep conservative conflict rejection, DRAFT/non-authoritative output and typed errors; test compiler questions and zero executor calls after actual integration. |

No new confirmed approval bypass or secret leak was reproduced in this bounded review. Missing components/independent human review leave material risks unresolved. This does not establish universal security, native/OS containment, packet-level isolation or resistance to a privileged host attacker. Python audit/source checks cover the inspected pure-code paths and exact guarded children only; intentional simulated rejection events are not observed unauthorized traffic.

## 5. Gates, NOT RUN limitations and handoff

Full AC-001/002/003/010/013 remains unverified; unresolved ambiguity has no actual planner/executor integration to test. Therefore M2-09 is **BLOCKED**, M2 advancement **NOT READY**. Required critical failures would block advancement; currently required critical proofs are missing rather than failed executed tests.

Not run: real AI/provider requests, third-party or live demo probes, actual reviewer interaction, OS/account/key/service provisioning, real secrets checks, protected registry/recovery, repository context privacy, execution/SSRF/budgets, evidence HTML/JSON/exception redaction, approved verifier comparison, remote CI, installation/lock/lint/mypy/pytest, and Python 3.12 rerun this session. Their historical or planned status is not promoted to PASS.

Developer decisions already requested and still pending: M0-02 threat-model sign-off; ADR-0002 fixture/transport/containment choices; ADR-0003 protected identity/human presence/audit custody/recovery; tooling/acquisition boundaries. No new M2-09-specific design decision identified and no unchanged question repeated. Only genuine owner decisions and actual prerequisite evidence can unblock affected implementation; this report is not that approval. No real contract, execution scope, provider egress or privileged operation approved.

Changed files: this new report and todo.md (EV-0033/BLK-0025, task row, counters/focus and dated journal). Final totals from the ledger: 6 DONE, 7 IN_REVIEW, 16 BLOCKED, 42 NOT_STARTED, 71 total. M2: 1 DONE/8 BLOCKED/0 NOT_STARTED. No dependency-ready new implementation WBS; ISS-0003 is eligible local documentation only. No next task started.
