# M1 offline checks and executor gate

> **Date:** 2026-10-11  
> **Task:** M1-12, PRD §11 / NFR-SEC-001–005  
> **Gate result:** NOT READY; task BLOCKED, not DONE  
> **Evidence:** [todo.md EV-0024](../todo.md), including retained adverse results

This runbook describes the checks that actually exist. The repository has pure
domain types, canonical candidate contracts, an untrusted approval-state model
and a provisional scenario parser. There is no executable demo, fixture/session
adapter, scope transport, assertion executor, redaction/report pipeline, run store
or comparator. No runnable executor golden suite exists. Examples are candidate
policy and mock declarations, never approved contracts or target grants.

M1-05 remains IN_REVIEW. All six prerequisites M1-06–11 are BLOCKED.
ADR-0001's specified DSL choices are accepted; ADR-0002/0003/0004 and final
M0-02 security sign-off remain unresolved. Existing unanswered owner requests
remain open; this gate does not accept them or resubmit unchanged decisions.

## Existing safe command

From the actual repository root, using the inspected local interpreter:

```powershell
Set-Location -LiteralPath 'D:/Dev/PACT'
& 'C:/Program Files/Python314/python.exe' -I -B -m unittest discover -s packages/pact-core/tests -v
```

This command ran on Python 3.14.4: **67 tests passed**, zero failures/errors/skips.
It requires no package installation. Tests add the uninstalled package to their
own import path, read synthetic fixtures and use two known isolated Python child
processes for import/parser audits. These checks are not a clean-install, pytest,
CI, live HTTP or sandbox result. Inspect tests before rerunning a changed checkout.

| Existing module | Tests | What ran; practical limit |
|---|---:|---|
| test_domain | 19 | Strict entities/references/enums and privileged-field rejection; no target policy enforcement. |
| test_contracts | 20 | Canonical golden digest, round trips, decoding bounds and conflict checks against independent fixture-fact worlds; no approved contract receipt. |
| test_approval_model | 9 | Invalid transitions, edited/replayed/forged claims and immutable model history; authenticated approval always unavailable. |
| test_imports | 2 | Domain import dependencies and fresh-process side-effect audit; not runner containment. |
| test_scenarios | 17 | Closed mock grammar, malformed/privileged input, seeded valid/negative mutations and fresh-process audit; no operation executes. |

The existing golden contract digest test is
`test_contracts.ContractTests.test_golden_digest_and_exact_canonical_bytes`.
Seeded parser property tests are
`test_seeded_valid_round_trip_property_cases` and
`test_seeded_negative_property_mutations`. They verify candidate data and parser
behavior; they are not the vulnerable/patched HTTP golden cases.

## Additional audited invocation

A one-off **scratch-only** wrapper was used, without editing project tests:

```powershell
& 'C:/Program Files/Python314/python.exe' -I -B 'C:/Users/user/AppData/Local/Temp/PACT-M1-12-a3be10da-225f-4ffb-875b-9b7072bcba3c/guarded_existing_suite.py'
```

The corrected invocation passed all 67 existing tests, zero failures/errors/skips.
The parent audit recorded zero socket/DNS/HTTP/native-call attempts and zero
provider/client imports; only the two exact inspected isolated child commands
were admitted. Both existing child guards deny socket/ctypes/process and filesystem
write activity during their import/construction/parser checks and passed unchanged.
There is no provider adapter/model invocation or live target request in these
executed paths. No real AI API call or outbound request was made by this suite.

Five **simulated audit events** separately verified rejection of socket connection,
HTTP connection, native library load, provider import and an unknown child command.
They invoked audit callbacks only, not real sockets, imports or subprocesses.
The summary keeps these negative checks separate from observed suite counters.

The initial wrapper invocation exited 1 with two errors: it incorrectly rejected
the known children because Windows can supply `executable=None` and derive it from
the exact command line. Corrected only that scratch handling, retaining the full
interpreter/script/argument allowlist and temporary-directory checks. No repository
test or product security assertion was weakened. The failed transcript and summary
remain alongside the corrected results.

This is scoped Python audit/source evidence, not OS packet capture, protection
against hostile native code, executor isolation or acceptance of the absent runner.
The wrapper is a temporary evidence artifact, not an installed PACT command; it
must be reinspected against exact source/interpreter paths before reuse.

Retained local evidence directory:
`C:/Users/user/AppData/Local/Temp/PACT-M1-12-a3be10da-225f-4ffb-875b-9b7072bcba3c`.
It contains baseline-python314.txt, guarded-initial.txt,
guarded-summary-initial.json, guarded-python314.txt, guarded-summary.json and the
final scope/whitespace check transcripts. The initial scope checker counted a
hypothetical task example as a duplicate; its failed transcript is retained.
Restricting that scratch parser to the canonical ledger produced a passing check:
49 original file hashes, 70 other task rows and all historical evidence/journals
preserved; 51 files and consistent 71-task totals. `git diff --check` exited 0.
These temporary logs are not committed
product run artifacts, trusted audit records or durable CI evidence.

## Required executor cases — none executed

| PRD AC | Required positive/negative evidence | Actual result and blocker |
|---|---|---|
| AC-004 | Vulnerable synthetic cross-tenant response discloses protected data; reliable VIOLATION with redacted rule/step evidence. | NOT RUN: demo, authentic fixture sessions, executor and redactor absent; M1-04/06/08/09. |
| AC-005 | Fixed variant denies cross-tenant access while own-tenant intended behavior still passes under the same contract. | NOT RUN: no vulnerable/fixed demo or executor; M1-04/06/08. |
| AC-006 | Missing/wrong/swapped/expired auth or failed fixture setup yields ERROR/INCONCLUSIVE, never PASS or reliable VIOLATION; teardown verified. | NOT RUN: no fixture/session adapter or assertion engine; M1-06/08. |
| AC-007 | Unapproved target rejected before any request, with safe reason. | NOT RUN: no target grant, scope guard or transport; M1-07/08. Parser URL rejection is insufficient. |
| AC-008 | Compatible same-policy PASS->VIOLATION links both preserved runs, rule and step; changed policy/fixture/environment does not become drift. | NOT RUN: no actual outcomes, immutable store or comparator; M1-08/10/11. |
| AC-011 | Seeded fake tokens/private fields absent from actual logs, JSON, HTML and errors while useful lineage remains. | NOT RUN: no executor evidence/redaction/report pipeline; M1-08/09. Safe parser errors are insufficient. |
| AC-015 | Out-of-scope redirect is not followed or given credentials; DNS/IP swaps and budgets tested. | NOT RUN: no scope-enforcing transport; M1-07/08. |
| AC-016 | Valid existing fixture/route and independent actor; approved 404-denial profile plus no protected disclosure/state change can PASS. | NOT RUN: profile names exist, but fixture controls/HTTP observations/assertions do not; M1-06/08. |
| AC-017 | Expected ALLOW with HTTP 500, network/timeout or broken setup never passes. | NOT RUN: no actual assertion executor; M1-06/08. |

No listed executor case failed at runtime because none could run. Their missing
implementation/evidence and unresolved prerequisites are **gate blockers**, not
passing, skipped-by-the-test-runner or confirmed vulnerable-target results.

NFR-SEC-001 has only untrusted approval-model negatives, not real approval/scope
enforcement. NFR-SEC-002 lacks runtime redaction evidence. NFR-SEC-003 has explicit
model/data authority limits but no executor verdict path. NFR-SEC-004 has executed
restricted-parser negatives; repository/provider/runtime injection boundaries are
unverified. NFR-SEC-005 lacks transport/DNS/redirect/budget/cancellation evidence.
None of these broader requirements is closed by the 67-test total.

## Resuming the actual offline demo gate

The following is a future verification sequence, **not runnable commands today**:

1. Close/review actual M1-05–11 prerequisites and unresolved fixture/runner/tooling
   boundaries. Verify genuine harness-only preauthorization or approved contract
   origin, exact target/method/budget scope, session isolation and containment.
2. Supply deterministic disposable vulnerable/fixed demo variants and independent
   synthetic actors, positive fixture/route controls and reliable setup/teardown.
3. Execute the nine cases above using a guarded offline path with providers disabled;
   include error, redirect/rebinding, disclosure despite denial status and budget
   negatives. Measure actual model/network activity at the implemented boundaries.
4. Validate sanitized artifacts, checksums, history preservation and comparator
   compatibility; retain failures and uncertainty, never rewrite a baseline.
5. Record exact supported commands, per-case outcomes, artifact links, cleanup,
   containment and independent review evidence. Reassess the exact M1-12 DoD.

Do not start a server, contact a target, mint an approval/grant or install tooling
from this runbook. No such operation occurred during this audit. M1 and P0 remain
NOT READY; M1-12 remains BLOCKED. No next implementation task was started.
