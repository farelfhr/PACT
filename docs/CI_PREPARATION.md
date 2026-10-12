# M0-07 local CI preparation and remaining remote gates

> **Version/date:** 0.1 / 2026-10-12
> **Status:** Local preparation reviewed scope; remote CI DISABLED / NOT RUN.
> **Trace:** M0-07; FR-PLT-001, NFR-MAINT-001; supporting NFR-COMP-001.
> **Source checkpoint:** `9a2a21950bb0a80c1c06ce63849329cfae7e23c3`.

## 1. Genuine scope and current result

The owner answers **“Setujui desain dan persiapan lokal offline”** to
[CI_REVIEW v0.1 §8](CI_REVIEW.md#8-decisions-and-next-bounded-increment), commit
1d398ea, EV-0072 digest
`0D7008649F5A0F1ABA67DBA6258B0C29EA77324AE88B7A0843462EEC6917DB19`.
The raw reviewed bytes still match. This accepts the preparation design and
permits existing inspected Windows tooling offline, a 60-minute executable
verification window and 1 GiB additional storage. It grants no new downloads,
private GitHub access, push, remote CI, target/provider requests or privileged
approval. REGISTRY_DISABLED and other disabled profiles are unchanged.

The local source increment is committed. All three installed Windows minors pass
the final regression/quality suite. Linux archive plans and extraction mechanics
are validated with metadata and mocks; **Linux binaries were not extracted or
executed**. The new clean-checkout install fails for insufficient disk space.
Remote CI is deliberately disabled and cannot be made functional by removing
just the workflow's false condition.

## 2. Exact changed paths and behavior

| Path | Actual change |
|---|---|
| `.gitattributes` | Preserve exact CI review/inventory bytes across Windows/Linux; existing manifest rules retained |
| `tools/workspace.py` | Explicit Windows/Linux x64 layout; complete bounded tar plan before writes; safe relative Linux link and executable-mode handling; case-sensitive filesystem check; unique command logs |
| `tools/ci.py` | Offline injected-response acquisition model, strict destination/hash/length/redirect/time/cancellation checks, source-event metadata validator and disabled CLI gate |
| `tests/test_ci_preparation.py` | 64 parameterized cases for portable layout, archive and CI model boundaries; existing tests unchanged |
| `.github/workflows/baseline.yml` | Pinned checkout candidate, exact proposed CI branch, both OS/minor cells, serial matrix and 20-minute job timeout; false condition and explicit failure gate retained |
| `todo.md` | Genuine decision, task claim/status, current focus, evidence, blocker and dated journal |
| `docs/CI_PREPARATION.md` | This report and exact command evidence |
| `docs/ci-transfer-inventory.json` | Exact committed source tree/reachable history inventory for the disabled source checkpoint |

No domain/package/schema/lock/dependency version, expected policy, approved
contract, fixture or historical reviewed document was changed. The two old
untracked documents remain excluded. Existing manifests have no new dependency.

Linux runtime preparation and remote CI have separate hard-coded disabled
flags, with no environment/CLI approval switch. A JSON event can be validated
as metadata but cannot authorize CI, target execution or a Security Contract.
The CI model has **no live HTTP or private GitHub adapter**. Its receiver is
injected for offline tests only. Implementing and reviewing a bounded live
adapter remains a necessary preparation step before an activation proposal.

The six-cell workflow remains a proposal. It has no current authenticated
repo/billing/retention preflight or effective exact-SHA execution authority.
It must fail closed until those are implemented and reviewed; no skipped job
is acceptance evidence. Tests check the disabled gates and pinned settings,
not GitHub's actual YAML execution or hosted containment.

## 3. Actual positive, adverse and failure results

| Actual check | Result |
|---|---|
| Before-change characterization | 91 tests / 2730 subtests PASS |
| Final Windows 3.12.15 | 155 tests / 2730 subtests, installed smoke, mypy17 core files, repository lint and tools/tests format PASS |
| Final Windows 3.13.16 | Same PASS |
| Final Windows 3.14.8 | Same PASS; offline locked sync and wheel/sdist build also PASS |
| Six reviewed interpreter archive plans | PASS without Linux extraction/execution: Windows3344/3309/2190 members; Linux4534/4526/4569 members and1049/1048/1048 safe relative links |
| Linux uv wheel executable metadata | Selected uv/uvx entries have mode0755; inspected only |
| Mock negative corpus | Unsafe paths/links/cycles/devices/privileged modes/expansion, unknown platform/patch, false private flag, wrong/forged event, unsafe redirects, response hashes/lengths, timeout/cancel rejected |
| Host configuration/credentials | Synthetic API key/token/proxy/PYTHONPATH/index settings excluded from build/test child environment |
| Log preservation | Two failed synthetic invocations retain distinct records; rerun does not overwrite a command log |
| `tools/ci.py inventory` | Exit0, explicitly DISABLED_NOT_RUN; no live client |
| `tools/ci.py preflight` / `acquire` | Exit1 expected REMOTE_CI_DISABLED; no request performed |
| Fresh local Git clone | Clone exit0, exact source checkpoint checked; new install exit1 due ENOSPC, not a clean-install PASS |

Mypy evidence covers the configured 17 core source files; it is not a strict-type
claim for every tooling/test file. Format evidence covers tools/tests, preserving
legacy core formatting. The previous EV-0071 clean-install proof remains
historical proof at its exact earlier source revision, not a pass for this new
checkout. No fixture/executor/provider/human/hosted acceptance is inferred.

The initial new test collection failed with a decorator SyntaxError (exit2).
It was corrected without removing cases; the failed transcript is retained.
One formatter invocation overlapped an active Windows check (tool runtime0.038s),
violating the serial constraint. This is disclosed rather than described as
strictly serial. Subsequent final three-minor checks were serial; the final
fixed-source rerun supersedes that early check as regression evidence.

## 4. Disk failure, cleanup and budgets

The new disposable checkout copied the same 36 inspected artifacts locally.
Its bootstrap stopped with **No space left on device** before installation.
D: had only528384 bytes free after the attempt; the grant's 1 GiB ceiling did
not imply 1 GiB physical free capacity.

Before cleanup, independently verified all36 copied hashes/sizes and original
artifact presence. Removed only those36 **session-created duplicate files**
(314881608 bytes), using literal PowerShell paths constrained to the exact
disposable quarantine root. No recursive workspace removal, original artifact
deletion, source reset or history rewrite. Clone source, partial runtime and
failure transcripts remain. D: then had315285504 bytes free. No fresh-install
retry, symlink/hardlink sharing workaround or runtime/environment relocation
onto another volume occurred.

Maximum measured additional storage during the attempt: **360351071 bytes**,
below1 GiB. The fresh-checkout verification attempt failed inside the60-minute
window; exact elapsed durations are in the command records. Metadata/report
bookkeeping is distinct from native execution. No new acquisition, service,
global/admin install, account/key setup, paid call, target/provider or remote
activity occurred. The serial deviation above remains a real limitation.

Before another fresh install, the operator should make at least1 GiB free on
the project volume and recheck available capacity against the proposed scratch
needs. Do not delete unrelated user files or silently use C:/cloud storage to
route around the approved environment. Any further executable run must still
have a valid remaining/new time and storage grant.

## 5. Exact source/history transfer review

[ci-transfer-inventory.json](ci-transfer-inventory.json) binds source checkpoint
`9a2a21950bb0a80c1c06ce63849329cfae7e23c3`:

- **88 committed files / 2134791 bytes**, each with raw committed hash/blob/size.
- **13 reachable commits / 191 Git objects / 9555698 uncompressed object bytes**;
  **120 reachable blobs** have content hashes and example paths.
- Narrow local regex screening for four token/private-key patterns found zero
  candidates. This is **not comprehensive secret clearance** or proof of clean
  historical data.
- No remote refs, repository settings, quota or visibility were queried. A push
  can transfer missing reachable history; these numbers are not measured network
  transfer, compressed pack size or service billing.

This is the **disabled prepared source**, not a source version approved to run
remotely. The final documentation commit will also be a distinct source revision.
Before any push, refresh inventory for the exact intended activation commit,
check remote ancestry without force, review newly included documentation/history,
and bind the genuine owner grant to that exact source and operation. Do not treat
this packet, Git author or an APPROVED JSON field as that grant.

## 6. Remaining gates and task closure

| Gate | Current state | Required next evidence |
|---|---|---|
| Destination | Owner confirms farelfhr/PACT PRIVATE for proposal | Read-only independent repo/ref/Actions settings verification under its own grant |
| Action code | Exact v6.1.0 commit/Node24/top-level MIT metadata inspected in EV-0072 | Pinned bundled JS/dependency notices/advisory review; no action execution yet |
| Live acquisition/preflight | Offline models only; CLI disabled | Implement bounded TLS/proxy-free/auth-isolated receiver and real metadata/cost/retention preflight; mocks first |
| Source transfer | Exact disabled checkpoint inventory exists | Reviewed activation SHA/tree/history/ref diff and explicit push grant |
| Cost/retention | Zero-paid-cost/seven-day private-log design accepted; actual settings unknown | Verified included capacity, enforced spending stop and retention setting before dispatch; no account changes implied |
| Fresh checkout | New source clone installed NOT successfully | Free local disk then authorized retry; preserve failed evidence |
| Linux/CI | NOT RUN, intentionally disabled | Authorized six real cells with import/install/negative/quality results and actual image identity; skipped/error cells do not count |

**M0-07 stays IN_REVIEW, not DONE.** Its exact DoD still requires real CI smoke.
71 =9DONE/5IN_REVIEW/40BLOCKED/17NOT_STARTED;62remain. No successor task starts.
M0/P0, real human approval, runner containment, hosted staging and benchmark
release gates remain incomplete.

## 7. Proposed next read-only preparation scope

No push or activation is requested yet. A useful next grant would permit only:

- HTTPS GET of non-secret metadata for farelfhr/PACT: repo visibility/default
  branch, proposed ref/commit ancestry and Actions permissions/retention metadata
  available to existing read-only access. No token/account creation or permission
  elevation; unsupported or forbidden endpoints are recorded NOT VERIFIED.
- Static reading of the pinned public checkout commit's `action.yml`, `LICENSE`,
  `package.json`, `package-lock.json` and `dist/index.js` on
  `raw.githubusercontent.com`; no JS/action execution or package installation.
- Maximum20requests/32MiB/10minutes, TLS validation, no retries, no source or
  evidence upload, zero paid cost. Authentication goes only to api.github.com;
  public source retrieval receives no private credential. Unexpected redirect
  or destination stops the read.

The owner may instead supply non-secret settings and defer network reads. Billing
capacity/hard-stop and retention evidence still need the responsible operator;
do not invent accessible billing data or interpret a notification-only budget
as cost enforcement. Existing destination/design decisions are not reopened.
After the action/metadata review, finish the remaining local adapter and present
the complete exact-source push/download/CI proposal. Remote activation stays
disabled until that later specific grant and its controls are genuinely ready.

## 8. Exact executed command records

Records below contain native argv/exit, not illustrative commands. Raw stdout,
stderr and durations remain in ignored `.bootstrap/workspace-checks/EV-0073/`.
Exit1 for disabled preflight/acquire is expected rejection; exit1 for the clean
install is an infrastructure failure. Initial collection exit2 is a real failure.
These cases are not CI PASS results. Metadata-only Git/hash/preservation/whitespace
checks are listed in todo.md EV-0073.

| Record | Exact argv | Native exit / seconds |
|---|---|---|
| characterization.json | `["D:/Dev/PACT/.venv/Scripts/python.exe", "-I", "-B", "-m", "pytest", "-q"]` | 0 / 9.99 |
| ci-acquire-disabled.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/ci.py", "acquire"]` | 1 / 0.113 |
| ci-inventory.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/ci.py", "inventory"]` | 0 / 0.13 |
| ci-preflight-disabled.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/ci.py", "preflight"]` | 1 / 0.113 |
| clean-checkout.json | `["C:/Program Files/Python314/python.exe", "-X", "utf8", "-I", "-B", "C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/check_ci_clean_checkout.py"]` | 1 / 5.901 |
| clone-source.json | `["git", "-c", "protocol.file.allow=always", "-c", "core.hooksPath=D:\\Dev\\PACT\\.bootstrap\\workspace-checks\\EV-0073\\empty-hooks", "clone", "--no-hardlinks", "D:\\Dev\\PACT\\.git", "D:\\Dev\\PACT\\.bootstrap\\workspace-checks\\EV-0073\\clean-checkout"]` | 0 / 0.509 |
| clone-sync.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/workspace.py", "sync", "--python", "3.14.8"]` | 1 / 4.153 |
| focused-fixed.json | `["D:/Dev/PACT/.venv/Scripts/python.exe", "-I", "-B", "-m", "pytest", "-q", "tests/test_ci_preparation.py", "tests/test_workspace.py"]` | 0 / 2.158 |
| focused.json | `["D:/Dev/PACT/.venv/Scripts/python.exe", "-I", "-B", "-m", "pytest", "-q", "tests/test_ci_preparation.py", "tests/test_workspace.py"]` | 2 / 1.724 |
| format-final.json | `["D:/Dev/PACT/.venv/Scripts/ruff.exe", "format", "tools/workspace.py", "tools/ci.py", "tests/test_ci_preparation.py"]` | 0 / 0.036 |
| format-final2.json | `["D:/Dev/PACT/.venv/Scripts/ruff.exe", "format", "tools/workspace.py", "tools/ci.py", "tests/test_ci_preparation.py"]` | 0 / 0.04 |
| format-logs.json | `["D:/Dev/PACT/.venv/Scripts/ruff.exe", "format", "tools/workspace.py"]` | 0 / 0.038 |
| format.json | `["D:/Dev/PACT/.venv/Scripts/ruff.exe", "format", "tools/workspace.py", "tools/ci.py", "tests/test_ci_preparation.py"]` | 0 / 0.71 |
| static-archives.json | `["C:/Program Files/Python314/python.exe", "-X", "utf8", "-I", "-B", "C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/inspect_ci_static.py"]` | 0 / 14.58 |
| win312-check.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/workspace.py", "check", "--python", "3.12.15"]` | 0 / 88.345 |
| win313-check.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/workspace.py", "check", "--python", "3.13.16"]` | 0 / 91.526 |
| win314-build.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/workspace.py", "build", "--python", "3.14.8"]` | 0 / 22.095 |
| win314-check.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/workspace.py", "check", "--python", "3.14.8"]` | 0 / 87.863 |
| win314-final.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/workspace.py", "check", "--python", "3.14.8"]` | 0 / 86.256 |
| win314-sync.json | `["C:/Program Files/Python314/python.exe", "-I", "-B", "tools/workspace.py", "sync", "--python", "3.14.8"]` | 0 / 41.422 |
