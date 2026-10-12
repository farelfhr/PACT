# M0-07 private CI review packet

> **Version/date:** 0.1 / 2026-10-12
> **Status:** PROPOSED. CI remains DISABLED; no upload, push or remote run authorized.
> **Task/trace:** M0-07; FR-PLT-001, NFR-MAINT-001; supporting NFR-COMP-001.
> **Baseline:** `22a3e1c12f465e578936f747150e88d5ade1e92c`.

## 1. Actual state and owner decision

The owner answers **“Origin itu privat; gunakan untuk proposal”**. Record
`github.com/farelfhr/PACT` as the intended private destination, based on that
direct confirmation. Repository visibility, default branch, Actions policy,
account entitlement, remaining quota and remote refs have **not** been queried.
The answer selects this proposal's destination only. It does not grant remote
read access, upload, push, workflow execution, account configuration or spending.

[WORKSPACE_BASELINE.md](WORKSPACE_BASELINE.md) / EV-0071 records three local
Windows minors passing install, installed import smoke, 91 tests / 2730 subtests,
mypy and lint. Linux and remote CI are NOT RUN. The existing
[workflow](../.github/workflows/baseline.yml) is disabled with an additional
deliberate failure step. `tools/workspace.py` rejects Linux execution today.
Do not remove those guards and report skipped Linux jobs as successful coverage.

M0-06 is DONE, satisfying the task dependency. M0-05 remains IN_REVIEW and
REGISTRY_DISABLED; this development CI must not activate product approval,
target execution, provider egress, hosted staging or the held-out corpus.

## 2. Recommended route and alternatives

Prepare locally, then present the exact final commit and transfer scope for
separate remote authorization. Recommend a **single, branch-specific push
trigger** for `codex/m0-07-ci`, with an exact approved event SHA and only the
baseline workflow running. No automatic PR, fork, schedule, workflow_run,
pull_request_target, merge, tag, release or repository protection change.

Manual `workflow_dispatch` needs the workflow to exist on the default branch.
That is an additional change, not something a branch-only upload achieves.
The proposed push trigger avoids making that change merely to run this gate.
The next source packet must show the branch/ref diff and enforce the exact SHA;
other pushes must fail authorization or remain disabled. This trigger is a
proposal, not an enabled workflow. [GitHub manual-run documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).

| Alternative | Trade-off | Recommendation |
|---|---|---|
| Branch-only, one approved push and SHA | Push itself starts CI; source upload and execution must be jointly granted | Initial gate, after final source review |
| Manual workflow on default branch | Extra default-branch update and write grant; useful for subsequent deliberate runs | Defer until requested |
| Locally uploaded wheel/runtime bundle | Avoids repeat upstream acquisition but uploads ~315 MB and needs private artifact storage/retention controls | Defer; no bundle uploaded |
| Reviewed exact upstream files in each fresh job | Separate CI download grant; hash verification followed by offline install; no reusable cache | Initial artifact strategy |
| Self-hosted runner | Requires a separate trusted operator, machine and containment/custody design | Outside M0-07 proposal |

## 3. Source and data recipients

[ci-source-inventory.json](ci-source-inventory.json) inventories the committed
baseline: **84 files / 2,056,726 bytes**, with raw committed SHA-256, Git blob ID
and byte size for every file. There are **11 reachable commits** at that baseline.
These are inspected local Git facts, not an estimate of upload size or proof
that historical content is secret-free.

A normal branch push sends Git objects required for the branch's reachable
history. A checkout's sparse paths or fetch-depth does not limit the history
transmitted by that push. The intended source recipient is the private GitHub
repository and its authorized collaborators/platform administrators; Actions
also processes source on GitHub-managed workers. Product requirements, design
documents, code, synthetic fixtures and tracker history are part of the current
tracked tree. Consent must cover that content and the reviewed reachable history.

Before remote permission is requested, freeze a final candidate commit and
refresh its exact tree/history inventory, ancestry/ref diff, size bounds and
secret review. No source commit for remote execution is approved by this packet.
If historical sensitive data is found, stop the push and propose a clean snapshot
or targeted remediation; do not silently rewrite history or upload it anyway.

Exclude all ignored quarantine/runtimes/wheels/envs/cache, OS credentials,
actual .env files, scratch transcripts and the two preexisting untracked
`LAUNCH_PIVOT_REVIEW.md` / `LOCAL_APPROVAL_FEASIBILITY.md`. The inventory is a
baseline, not a blanket allowlist for newly created files. No external AI or
other vendor receives repository context. No raw target evidence exists or is
needed for this workspace gate.

## 4. Proposed action, images and permissions

| Item | Concrete candidate | Verification and limit |
|---|---|---|
| Checkout | `actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803` (v6.1.0) | Official release points to this commit; pinned action.yml uses Node 24; top-level MIT license. Metadata inspected, execution and bundled-dependency review NOT RUN/unfinished |
| Windows | `windows-2025`, x64 standard hosted runner | Label documented for private repositories; actual image/version must be captured from each run |
| Linux | `ubuntu-24.04`, x64 standard hosted runner | Explicit OS label, glibc; actual image/version must be captured from each run |
| Matrix | Both OS labels × CPython 3.12.15 / 3.13.16 / 3.14.8 | Six mandatory cells; source/helper failures, canceled or skipped cells leave gate incomplete |
| Third-party actions | Checkout only | No setup-python/setup-uv/cache/upload-artifact or mutable tag references proposed |

Pinned action metadata and license were read from the
[exact upstream commit](https://github.com/actions/checkout/commit/d23441a48e516b6c34aea4fa41551a30e30af803),
[action.yml](https://raw.githubusercontent.com/actions/checkout/d23441a48e516b6c34aea4fa41551a30e30af803/action.yml)
and [LICENSE](https://raw.githubusercontent.com/actions/checkout/d23441a48e516b6c34aea4fa41551a30e30af803/LICENSE).
SHA pinning identifies code; it does not establish that bundled code is safe.
Before execution, review the pinned distribution's credential behavior,
dependency notices and relevant advisories; changed action pins require a
recorded revision.

Use `permissions: contents: read`, all unspecified scopes disabled, no OIDC,
PAT, repository secrets, deployments, PR/check publication, package publication
or write token in test processes. Checkout uses event SHA, depth 1, no tags/LFS/
submodules, `persist-credentials: false`, no unsafe PR override, and no global
safe-directory modification unless an actual reviewed need is found. A separate
metadata-only preflight may need `actions: read` to check settings; that token
must not be passed to tests or artifact acquisition. The later upload/dispatch
operator grant is distinct from the workflow's read-only token.

Standard hosted images are moving managed environments, not immutable digest
pinned container images. Record runner OS, architecture, actual ImageVersion,
Git/host bootstrap Python versions, action SHA and all tool/runtime hashes.
Fail if a required platform/version is missing; do not silently substitute
`-latest`, a different Python patch or another binary distribution.
[GitHub runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).

## 5. Bootstrap flow, network and containment limits

After future authorization: fresh runner → exact source checkout → source/profile
preflight → bounded acquisition of the **36 unchanged EV-0068 artifacts** → raw
manifest and complete artifact/lock/build-hash validation → prepare only the
selected OS/Python → offline noneditable install → import/tests/quality/build and
negative checks → bounded sanitized summary → disposable worker cleanup.

Retain the [reviewed manifest](bootstrap-artifacts.json) raw SHA-256
`8FEDFF4BE21ABAC355B8B9251D55608F75C7E2864BB6E7676C53C00CF32DEEFE`,
exact 17 package pins / 30 wheels / six interpreter archives, all URLs, lengths
and hashes. Each cell fetches the full set required by the current global
preflight (314,881,608 bytes), even though it executes only its own artifacts.
Six fresh cells total **1,889,289,648 artifact bytes** before protocol overhead.
No new package, global install, online resolver fallback or automatic retry.

Application-controlled acquisition: HTTPS only, exact manifest URLs on
`files.pythonhosted.org` and GitHub Astral release paths; redirect count ≤3 and
only reviewed GitHub release CDN hosts `release-assets.githubusercontent.com`
or `objects.githubusercontent.com`. Do not send GitHub credentials to these
download URLs. Reject unexpected destinations, status/size/hash, timeout and
partial responses before extraction/execution; retain failure metadata, not
credentials or token-bearing redirect URLs.

GitHub-managed source/action/job/log traffic additionally uses documented
GitHub control endpoints, including github.com, api.github.com,
codeload.github.com and GitHub Actions service domains. This traffic is separate
from dependency acquisition and is not a test-target request. The final profile
must list required endpoint classes from the
[platform communication reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners#communication-requirements-for-github-hosted-runners);
it must not claim the downloader's allowlist is an OS firewall.

Hosted runners have broad network access and administrative capabilities by
default. This proposal does **not** prove OS egress isolation or runner
containment. Execute reviewed development tooling only; no sudo/admin elevation,
Docker/socket/mount change, target service, browser review authority or arbitrary
AI-generated command. Remove provider/target credentials from child environments;
disable pytest plugin autoload, interpreter acquisition and dependency telemetry
where supported. Import socket/process audits and mocked network rejection
tests are application evidence, not a compromised-dependency sandbox guarantee.
If stronger network denial is required before running this source, retain CI
disabled and prepare a separate isolation profile rather than claiming it exists.

## 6. Budgets, privacy, failure and rollback

Propose **one workflow attempt**, matrix serial (`max-parallel: 1`), no automatic
reruns, six jobs with 20-minute timeout each plus at most five minutes metadata
preflight: **125 VM minutes maximum**, not a billing-minute estimate. Queue delay
is excluded. Artifact response bodies ≤2 GiB aggregate; enforce per-file exact
size and aggregate accounting. Per-job project data ≤3 GiB; no shared cache,
artifact bundle or retained environment. These are process/workflow budgets,
not a proven OS disk quota. Cancellation/timeout/failure is non-success and
cannot satisfy a missing cell. Any retry requires its own remaining grant.

Recommend **paid spend ZERO**. Private Actions uses account included quota and
may bill after it is exhausted; the actual plan/quota/billing controls are not
known. Before activation the owner/operator must supply non-secret confirmation
of adequate included capacity and an enforced stop-spending control (not merely
an email alert). If it cannot be established, do not start billable jobs. No
account/subscription/settings changes are authorized here.
[Billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions),
[budget enforcement](https://docs.github.com/en/billing/how-tos/set-up-budgets).

Retain private sanitized job logs and summaries for a proposed **seven days**;
retention setting must be verified/configured under its own owner grant before
activation. Each cell emits ≤1 MiB of summarized identifiers, checks, durations,
exit codes and content hashes; no environment dump, tokens, full target payload,
binary archive upload or sensitive exception body. Git source retention remains
repository lifetime; seven-day log retention does not delete pushed Git history.
No upload-artifact action is proposed. Read back redacted CI evidence into the
local evidence report while the run is available. Unexpected disclosure stops
the affected workflow and follows incident handling.

Fail on wrong repo/public visibility, unexpected branch/SHA/profile/action,
missing cost controls, unsupported image, extraction/hash/lock failure or test
failure. No continue-on-error, broad exception suppression, fallback version or
optional Linux job. Record actual run URL/job IDs/commits and outcomes including
failed/canceled/skipped jobs. Advisory CI status must not become a product
authorization verdict. Rollback: cancel the one active run, retain redacted
failure evidence, disable the branch workflow under a specifically approved
remote change; preserve source/evidence history. Do not alter branch protection
or merge into the default branch.

## 7. Implementation and acceptance checks (all planned)

| Check | Positive evidence required | Adverse/failure evidence required |
|---|---|---|
| Source/profile gate | Exact approved repo, branch, event SHA and private setting | Wrong/public repo, changed SHA, absent billing/settings evidence prevents activation |
| Linux bootstrap | Case-sensitive filesystem, safe relative symlinks, selected Python/uv bytes and retained notices | Traversal, absolute/escaping links, hardlinks/device entries and wrong platform refused; Windows alias defenses preserved |
| Artifact/lock/build | Exact 36 hashes, 28 lock wheel bindings and six build constraints; offline clean noneditable install | Partial/tampered wheel, empty cache, stale/missing lock and wrong/missing build-transitive hash fail without online fallback |
| Imports and quality | Installed import with no unexpected side effects; current 91 tests / 2730 subtests plus new portability tests; strict mypy/lint/scoped format | Import network/write/process attempt, forged APPROVED and existing malformed/security cases remain rejected |
| Build distribution | Wheel/sdist contain only intended package/schema/notices; immutable source version | Synthetic .env/private canary excluded; same-input round trip measured rather than universally asserted |
| CI completeness | Six actual cells, exact commands/exit/results/image/runtime/source/hash evidence, fresh cache | Missing, skipped, canceled or infrastructure-failed cell prevents M0-07 DONE; no fabricated CI pass |

New stdlib mock tests must cover host/platform selection, Linux executable modes
and bounded safe archive links without importing acquired Linux binaries on
Windows. Preserve existing contract schema/digests, validation, fixtures and
approval semantics. Linux runtime proof awaits genuinely authorized Linux CI.
No target/fixture runner or provider network test is part of this workspace gate.

## 8. Decisions and next bounded increment

**Already decided:** private destination for proposal; accepted tooling/design
and artifact set; completed offline Windows grant; six-cell matrix direction.
These are not requested again.

The next decision is acceptance/change/defer of this CI preparation design:
branch-only one-push route, pinned checkout candidate, full-artifact per-cell
downloads followed by offline install, managed-image limitations, serial budgets,
zero-paid-cost preflight and private seven-day sanitized logs.

If accepted, request a **local-only preparation scope**: adapt `tools/workspace.py`
for the proposed Linux layout and safe extraction; add acquisition/CI preflight
and portability tests; prepare a still-disabled pinned workflow and final transfer
inventory/report; update ledger and commit locally. Allowed paths: tools/,
tests/, .github/workflows/baseline.yml, necessary root/core workspace configuration,
CI review/inventory/evidence docs and todo.md. No dependency/policy/schema changes.
Verification uses unchanged, previously inspected Windows artifacts offline,
serial ≤60 minutes, ≤1 GiB additional storage, no new acquisition/network/global/
admin/service/provider/target operations. The prior executable window has ended;
do not silently reuse it. Existing Python 3.14.4 can run non-executable metadata
checks before that grant. If selected controls cannot be implemented within this
profile, report the gap rather than enabling a workaround.

After local preparation, provide the final exact commit/tree/history/digests,
action review, endpoint list, revised actual commands, storage/transfer accounting,
privacy/secret review and owner billing/retention prerequisites. **Only then** ask
for the concrete read/push/download/remote-run grant. Preparation acceptance
does not grant that later operation, update main, run GitHub CI or close M0-07.

## 9. This session's actual checks and limitations

Read local Git/ledger/config/requirements and official public documentation;
generated committed-byte baseline inventory and reviewed the still-disabled
workflow. Local proposal coherence/history/ledger/digest checks and whitespace
results are recorded in todo.md EV-0072. This document's commands and cases in
§§5–7 are **planned**, not executed CI evidence.

**NOT RUN:** private GitHub metadata query, push/source upload, action execution,
CI acquisition/install/tests, all Linux runtime checks, remote quota/retention
verification, OS egress/privilege controls and target/provider requests. The
recorded EV-0071 Windows results are historical local evidence, not rerun here.
M0-07 remains IN_REVIEW; 71 = 9 DONE / 5 IN_REVIEW / 40 BLOCKED / 17 NOT_STARTED.
