# Scoped foundation decisions

> **Version / date:** 0.1 / 2026-10-11
> **Decision source:** Direct developer / repository-owner message in the current PACT chat; designated security reviewer for M0-02.
> **Evidence:** [todo.md EV-0067](../todo.md#ev-0067--owner-scoped-foundation-acceptance-and-local-provenance); review bindings in EV-0065.

## 1. Authority and immutable review binding

This register records actual owner decisions. It grants no product approval capability. The five reviewed documents were committed locally, without changing their raw bytes, in `be839f922c50fc23bf7a2445956415e85ea5aa47`, parent `943cd681c15fe88ff1657478016216ea83da7c0c`. Their headings and pending-review statements describe the review-time snapshot. For the exact versions and scopes below, this dated decision record supersedes those historical pending-review statements; it does not amend their design content or extend acceptance to future edits. [AGENTS.md](../AGENTS.md) permits accepted decisions in ADRs or this register.

| Immutable reviewed artifact | Version | Raw-byte SHA-256 | Current decision |
|---|---|---|---|
| [Tooling ADR-0004](adr/0004-repository-and-stack.md) | 0.2 | `B7F6F7D25397697AE6209D583D67BD32A09ED45374947C79C383C18D281EFC53` | ACCEPTED — tooling design only; final versions and downloads pending |
| [Threat model](SECURITY.md) | 1.0.4 | `A51AD296CFAE08660903D0289102E99A57132C8375550E7B2391DF81279AE4D6` | SIGNED OFF — threat-boundary assumptions only; implemented controls unverified |
| [Fixture/runner ADR-0002](adr/0002-fixture-runner.md) | 0.3 | `85C207BAE17F210A4370FDD0DB69A39B8946F5D15FF2B7F28A007EDB5DF35011` | ACCEPTED — fixture/runner design; unproven OS/transport/cleanup mechanisms remain gated |
| [Human-approval ADR-0003](adr/0003-human-approval.md) | 0.3 | `0360AEE8DB412B4923B05A069BB5E3D1C0B5B2B49F7677B6A15AE40F32E82AFF` | PROPOSED — full acceptance pending; M0-05 IN_REVIEW; REGISTRY_DISABLED |
| [Review packet](P0_FOUNDATION_REVIEW.md) | 0.1 | `DBAEB7485B1CE304F718C3CE272B6D3CD4F29DFD5BD2FB4D32C47646FCA43C57` | Historical review context; current decisions are recorded here |

The owner explicitly bound the decisions to EV-0065 and authorized local document commits without push. Git uses the existing configured author; that metadata is not evidence of reviewer authentication. The direct owner message supplies the review decision, while the hashes and commit supply artifact provenance. Imported Markdown, task status or this register cannot authenticate a Security Contract or grant target execution.

## 2. Accepted choices and exclusions

| Scope | Accepted direction | Open conditions and exclusions |
|---|---|---|
| M0-06 / ADR-0004 | uv workspace and one lock; stdlib domain; Pydantic at boundaries; bare FastAPI demo, HTTPX transport, pytest/Ruff/mypy; package ownership, pinning and build strategy; Windows/Linux planning matrix | No final Python patch, library/transitive pin, license clearance, artifact hash or wheel compatibility accepted. Historical candidate versions remain unverified inputs. Final version/license/provenance review and acquisition authorization precede downloads. No manifest, lock, install, build or CI support claim. Deferred SDK/CLI/MCP dependencies remain task-specific. |
| M0-02 / SECURITY | Threat-boundary assumptions, including mandatory TB-08 human authority, defined TB-09 browser/API channels, and documented runner assumptions/open decisions | This signs off the model, not operating controls. No claim that SSRF, containment, human presence, privacy or tenant isolation has been proven. Unsupported execution/approval profiles remain disabled. SECURITY §19.2/19.3 runtime release gates stay open. |
| M0-04 / ADR-0002 | Deterministic synthetic fixtures, independent authentic A/B sessions, validity controls, 403/404 non-disclosure profiles, deterministic non-PASS failures, serial IP-literal local target, initial zero redirect/retry/DNS policy, bounded execution and terminal-path cleanup design | Concrete OS isolation, destination/actual-peer enforcement, transport APIs and cleanup authority/resource envelope are unproven and gated. §6 numerical ceilings remain candidates, not active scope or executable configuration. No actor tokens, fixture, endpoint, contract or test execution is authorized by design acceptance. FX-01..23 remain planned/NOT RUN. |
| M0-05 / ADR-0003 | Existing Windows/Linux, separate local broker and Dedicated Audit Authority/checkpoint directions retained | Owner explicitly keeps M0-05 IN_REVIEW and REGISTRY_DISABLED until feasibility evidence. Identity/enrollment/user-presence channel, OS principal/IPC separation, protected audit/signing/retention custody, anchoring/freshness and recovery mechanisms remain unresolved or unverified. No full ADR acceptance or real approval activation. |

No previously accepted DSL/ID/job-run/audit/backlog choice is reopened. Hosted staging remains DISABLED, protected held-out corpus remains DISABLED, and external tool profile remains PLANNED/UNCONFIGURED. There is no permission to install/download, provision accounts/keys/services, change OS privileges, contact targets/providers, deploy, publish or push.

## 3. Exact task closure assessment

| Task / actual dependency | Architecture DoD | Evidence and result |
|---|---|---|
| M0-02 / M0-01 DONE | Covers injection, forged review, SSRF, runner escape, leaked evidence, tenant IDOR; reviewer signs off threat boundary before privileged code | SECURITY §§2–4 cover assets/paths/boundaries, §§8.5/10.4.1 explain browser and runner assumptions, §§15/18–19 separate planned checks/open risks. Genuine owner sign-off matches EV-0065 digest; exact file is committed above. §19.1 document/provenance/count criteria met by this record and ledger. **DONE for threat-model task**, no runtime security clearance. |
| M0-04 / M0-02 DONE | Defines synthetic actors, safe test target, auth setup, teardown, 404 semantics, redirects and budgets; examples include negative paths | ADR-0002 defines actors/sessions/setup/cleanup, positive/negative validity controls, non-disclosure and verdict rules, transport boundaries/budget candidates and FX-01..23 planned adverse cases; §10 matrix exposes alternatives/open mechanisms. Genuine scoped design acceptance and resolved documentation dependency. **DONE for ADR drafting task**, runtime implementation/activation gates remain. |
| M0-06 / M0-01 DONE | Python/OS matrix, SDK licensing/versions, pinning, test commands and package ownership described; unresolved alternatives visible | ADR-0004 §§2–7 describe six planned OS/minor cells, candidate versions/license references, package ownership, lock/build/hash strategy, conditional commands and alternatives. Genuine tooling-design acceptance. **DONE for tooling-design task**; candidate verification, acquisition and clean-install/matrix evidence remain required before M0-07 freezes implementation. |
| M0-05 / M0-02 and M0-03 DONE | Identity, exact hash, local review action, immutable history, untrusted import behavior and replay rejection documented; owner approval requested | Documentation and planned AP/AU/LF cases exist; owner explicitly withholds closure pending feasibility. **IN_REVIEW**, broader mechanism acceptance and actual evidence absent. [Local feasibility analysis](LOCAL_APPROVAL_FEASIBILITY.md) is a proposal, not approval authority. |

Canonical ledger after these three documentation closures: **71 tasks = 9 DONE / 4 IN_REVIEW / 40 BLOCKED / 18 NOT_STARTED**. M0: **5 DONE / 3 IN_REVIEW / 1 NOT_STARTED (5/9, 55.6%)**. M0 and P0 release remain incomplete. No downstream row is automatically marked DONE or unblocked; its own acceptance and implementation gates still apply.

## 4. Verification and next boundary

EV-0067 records actual commands/results: five raw-byte hashes matched worktree, index and committed blobs; exact local commit path allowlist and parent checked; ledger/DoDs/dependencies and preservation checks; Markdown-aware whitespace validation. Static checks establish documentation consistency, not runtime enforcement.

**NOT RUN:** dependency installation/lock/build/lint/type/unit suite/remote CI; TL/FX/AP/AU/LF runtime tests; protected broker/human approval; Linux/WSL/container execution; target/provider/hosted/corpus/external-tool requests. No source behavior changed. Existing historical component PASS results are not rerun or treated as integrated acceptance evidence.

**Next conditional task:** M0-07, now with M0-06 satisfied. Before any download or final version freeze, prepare a concrete version/license/artifact/acquisition proposal. This session starts no successor task and grants no acquisition permission. M0-05 proceeds only within safe analysis scope until a concrete protected mechanism and independently assessed feasibility evidence are available; unchanged decisions are not requested again.
