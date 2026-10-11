# ADR-0003 — Human-bound approval and immutable contract history

> **Status: PROPOSED — scoped storage design direction selected; full ADR NOT ACCEPTED**
> **Draft version:** 0.2, 2026-10-11
> **Author / task:** Codex / M0-05
> **Decision owner / security reviewer:** Repository developer; storage direction selected 2026-10-11; broader review pending
> **Trace:** OQ-04/14; FR-CON-001/002; supporting FR-CON-003/004/005/006, NFR-SEC-001/003/007, AC-002/003

## 1. Context, actual prerequisites and bounded scope

**Current decision (2026-10-11):** The developer selects **Dedicated Audit Authority + Append-Only Audit Log + Independently Signed Checkpoints** as the required storage architecture direction. §§4/6/8/10 below incorporate that scoped decision. It does not accept this ADR in its entirety, sign off M0-02, choose M2-06 human identity/user presence, approve any contract/target/privileged operation, provision accounts/keys/cloud services, enable provider egress or approve deployment. Safe documentation and local synthetic/mock work are permitted; real privileged approval stays disabled. Exact decision scope, prior/new document digests and remaining gates are recorded in todo.md EV-0034. Unchanged selected storage choices will not be requested again without material new evidence.

[PRD §6.3/7.3](../../PRD.MD) distinguishes candidate policy, human-approved intent and observed behavior. [Architecture M0-05](../ARCHITECTURE.md) requires identity, exact hash, local review, immutable history, untrusted imports, replay rejection and an owner approval request. Dependencies M0-02 and M0-03 remain IN_REVIEW; neither final threat-boundary sign-off nor accepted DSL semantics exist. [ADR-0001](0001-contract-dsl.md) and [ADR-0002](0002-fixture-runner.md) remain PROPOSED. No accepted ADR, code, approval service, identity broker, test suite or build configuration exists.

The current task authorizes a **draft**, and the developer permits safe documentation/local non-privileged work. It does not close dependencies or freeze privileged approval design. [workflow §3.2](../../workflow.md) allows reviewable proposals while those decisions are open; G-01/02/03/04/06 remain gates. [SECURITY §6](../SECURITY.md) and mandatory TB-08 forbid AI self-approval. Reviewer designation in this conversation identifies the developer reviewing this ADR; it is not an implemented product identity, contract receipt or sign-off on M0-02.

The original v0.1 intake above is historical. Currently ADR-0001's specified DSL choices are accepted and pure candidate/model/parser/fake-provider packages exist; M0-02/M0-05 reviews and M2-06/M1-10 remain unresolved. The storage direction stated above is selected; remaining protocol/implementation choices below are proposed. No real approval client, broker, audit registry, checkpoint signer/store or trust root exists. No actual contract is approved here. Hosted identity/browser and concrete signing/key infrastructure require separate design and provisioning authorization; the selected signed-checkpoint requirement cannot silently be dropped in a local approval path.

## 2. Authority, identities and trust model

Use one application approval service for all adapters. Agents may create candidates and **request review**; only the separate authenticated human interface may issue a decision to that service. A reviewer must have current project-specific permission at decision time. Viewer, runner, provider, CI and machine/MCP identities cannot become human reviewers by supplying a role flag, email, username or environment variable.

For local P0, propose an OS-protected approval broker/registry and a human-operated review client with verified OS identity, separate from the agent/runner identity and writable workspace. Bind a stable OS security subject (SID/UID plus verified host/identity namespace) to an explicit protected reviewer/project enrollment; do not trust `getpass`, `$USER`, process arguments or client JSON as authentication. Enrollment and permission changes are human security-administrator actions, not automatic self-enrollment by whoever starts the CLI. Authentication, role checks and enrollment storage mechanisms require acceptance in §10 before implementation.

**TTY presence is not human presence.** An AI tool can launch a process, allocate a PTY and type a confirmation phrase. A CLI `--approve`, `--yes`, stdin line, environment variable or interactive prompt alone must not approve. The local CLI may open/request a human review, but final confirmation must use a protected interactive channel with fresh user verification outside agent automation authority. The selected OS authentication/user-presence mechanism must bind its result to the exact review challenge and prevent a machine token or agent-controlled process from invoking the confirmation path unattended. If those capabilities are unavailable, leave the contract NEEDS_REVIEW; no terminal-only fallback.

The broker/registry must deny agent and runner write access to reviewer enrollment, pending decision consumption, approved snapshots and audit. An agent sharing the reviewer's full OS privileges can edit files, impersonate processes or control prompts; file permissions, a process name and a hash cannot solve that. Supported execution must separate those authorities or keep approval disabled. A compromised host administrator, reviewer session or trusted review client is a residual trust-root risk, not protection proven by this ADR. Do not silently claim hostile-same-user resistance. OS-specific separation and user-presence evidence remain required tests, not assumptions of completion.

The human interface displays inert, escaped policy and source text; untrusted repository instructions, control characters or model prose cannot alter capabilities or hide the decision. The reviewer inspects unresolved questions, rule/profile definitions, project/scope and complete policy bytes/diff. No auto-approval based on confidence, a green CI result or a previous approval of a similar policy.

## 3. Exact canonical binding and separate execution permission

Use ADR-0001's accepted strict JSON and `pact-json-1` policy algorithm: sorted ASCII object keys, compact UTF-8 JSON without BOM/newline, integer normalization, preserved array order; reject duplicate keys, executable fields, unknown schema/canonicalization and ambiguity. Recompute the SHA-256 from stored immutable canonical policy bytes, not a supplied digest. Whitespace/key order can normalize identically; a change to rules, version, project or array order creates different approved content. Preserve raw source/provenance separately; do not treat it as policy authority. Separate review/event/checkpoint byte profiles remain to be specified; policy canonicalization is not a signature protocol.

Construct a separate versioned **review binding** in the trusted service. Proposed canonicalization `pact-review-binding-1` uses the same restricted sorted-key JSON byte rules and fixed typed fields, but is not the policy's root schema. Domain-separated `kind`/`operation` fields prevent approval/rejection/scope-grant messages being interchangeable. The review binding must contain:

| Bound value | Required meaning |
|---|---|
| Project and policy | Protected project identifier, contract ID, exact version, schema/canonicalization, recomputed policy digest and immutable draft revision ID |
| Assertion definitions | Sorted unique profile ID/version/digest tuples; digests cover exact immutable definitions, not just mutable names; any conflict or missing definition blocks review |
| Review scope | Exact immutable policy applicability/scope revision and digest, including intended environment/fixture/adapter constraints; no hidden target or privilege expansion |
| Decision and reviewer | Explicit `APPROVE` or `REJECT`, authenticated human subject and current protected permission revision; identity derived by broker, never authoritative client input |
| Freshness | Review request ID, securely generated single-use nonce, issued/expiry times, authentication-context reference and registry generation; clock/enrollment facts independently verified |

Hash the canonical review binding and show both it and the policy digest in the trusted human confirmation. Hashes are integrity references, **not signatures or proof of human approval**. Bind full bytes as well as their references in the protected record; validate profile/scope hashes against the approved registries. Unknown identifiers or matching hashes without trusted records do not grant authority.

Policy applicability scope is **not an execution grant**. Approval of the exact contract/scope does not authorize network requests, runner privileges, provider egress or future expanded targets. Each job still requires ADR-0002's independent authentic execution/fixture grants and limits, within the approved policy applicability; unrelated target URLs in a receipt or imported JSON cannot grant scope. Profile/fixture/scope changes require a new review binding and, if approved semantics change, a new policy version; preserve historical links.

## 4. Explicit local human action and atomic commit

Proposed local interaction, not existing commands:

1. A CLI/MCP candidate or review request enters DRAFT/NEEDS_REVIEW without authority. The broker validates complete typed policy, provenance/questions and fixed profile/scope references. Ambiguity, unresolved conflicts or missing definitions cannot enter an approvable state.
2. The broker snapshots the exact revision and creates a pending, finite-lived challenge bound to authenticated intended reviewer, project, registry generation and requested decision. Obtain nonce randomness from the platform cryptographic random source; never model text, a predictable counter or a reused fixture seed.
3. The human independently opens the protected review client, authenticates and sees complete rules, profile definitions, applicability, canonical policy/review hashes, version and differences. Redact sensitive provenance for display without changing the bound policy. Editing creates a new draft revision and cancels outstanding challenges; never edit approved bytes in the review window.
4. After deliberate review, the human selects APPROVE or REJECT and completes fresh protected user verification bound to the challenge. A generic login, an agent-controlled terminal phrase or an unrelated OS prompt does not establish this transaction. No noninteractive approval option. Close/cancel/timeout leaves NEEDS_REVIEW and a non-authoritative event.
5. Revalidate authenticated reviewer/project permission, freshness/revocation, nonce, decision, draft revision, all canonical hashes and registry generation. Compare-and-swap the expected NEEDS_REVIEW revision; atomically record immutable snapshot, nonce consumption and decision/audit intent through the protected authority. A database commit alone is **pending and non-effective**, not trusted APPROVED. Durably anchor the exact committed event through the independent signed-checkpoint authority, verify the anchor and all bindings/current eligibility, then make approval effective. No cross-store atomic transaction is assumed: commit/anchor/activation, retry and crash reconciliation must be specified and tested before privileged implementation. Missing/uncertain anchor keeps approval ineffective; consumed nonce/history may remain durable for reconciliation, never silently erased or retried as a new approval.
6. Return an opaque registry handle and truthful pending/effective/disabled status, not a bearer approval capability. Later execution resolves the protected records, verifies current independently trusted checkpoint history, exact bindings and eligibility plus independent target/fixture grants. An unanchored snapshot, file path, signed checkpoint alone or echoed APPROVED string never authorizes execution. Any required checkpoint-authority outage fails closed, with no unanchored fallback.

Candidate freshness defaults for review: challenge lifetime at most ten minutes, final user verification at most sixty seconds old, bounded pending requests per project/reviewer. These numbers are **proposed ceilings**, not accepted configuration. If review takes longer, cancel and issue a fresh challenge for the current bytes; never extend the old nonce automatically. Trusted UTC timestamps and monotonic freshness checks must reject rollback/clock uncertainty; actual OS clock and user-verification mechanisms remain open. No automatic timeout approval.

## 5. Replay, races, revocation and re-use

Nonce consumption is atomic, unique and scoped to request/project/reviewer/registry generation. An expired, already used, canceled, unknown or transplanted challenge is rejected. Concurrent decisions for the same expected revision cannot create two approvals; one valid transaction can win, the other receives an explicit stale/conflict result. Changing the decision, profile, scope, policy version/hash, project or authentication context invalidates the binding.

Transport retry after a lost success response may retrieve the **same committed event** only with the same authenticated caller, operation/idempotency key and exact binding. It must not consume a new nonce, create another approval or apply to another revision. Reusing a review request/receipt as a new authorization event is a replay, not legitimate idempotency. A runner using the same approved snapshot for a later separately authorized job is policy re-use, not replay of a human decision.

Reviewer privilege removal, project/scope revocation or explicit approval withdrawal prevents new job eligibility under this proposal; recheck current protected permission/approval eligibility before job creation. Preserve the original historical approval bytes and decision. Record suspension/withdrawal as a new event rather than rewriting APPROVED history or silently approving a replacement. A past review session's normal expiration is not by itself a revocation of the immutable policy, but the challenge/authentication must have been valid at commit. If permission is later restored, require a fresh human reaffirmation event; no automatic resurrection of suspended eligibility. These revocation/reaffirmation semantics require owner acceptance.

Active-job cancellation and propagation latency are ADR-0002/hosted-runner concerns, not instantaneous guarantees. Block new privileged work until authoritative revocation checks are available; preserve earlier outcomes and report uncertain state explicitly. Backup restore/registry rollback must not revive consumed nonces or withdrawn grants: freeze approval/re-use pending protected recovery and a new registry generation/reconciliation. A generation value in untrusted JSON cannot perform recovery.

## 6. Immutable snapshots and append-only audit

### 6.1 Selected architecture and permissions

The developer's scoped storage direction requires a dedicated **Audit Authority security principal** to control protected append-only history. AI agents, runners, ordinary application processes and untrusted repository code cannot update/delete historical records. They may submit bounded requests through authenticated, authorized interfaces; supplying actor/project/reviewer fields cannot establish identity or grant append/admin access.

Separate event-appending, audit administration, checkpoint signing, checkpoint retention and exceptional recovery permissions. Use a separately controlled principal for the independently retained checkpoint store; signing keys belong to a dedicated signing authority or managed KMS and are inaccessible to agents/runners. Audit administration is not human contract review. Database constraints support validation but do not establish administrator/compromised-service-account resistance. Concrete OS/backend/KMS/ACL/delegation and least-privilege implementation remain unselected and unprovisioned.

Approved snapshots include immutable canonical policy bytes, all definition/scope bytes or immutable verified references, their hashes/versions, source provenance references, reviewer/authentication provenance, decision time and audit/event ID. Exact author/reviewer identities are distinct. Modifying policy creates a NEW DRAFT VERSION; approved versions and historical evidence remain intact. Rejected/superseded/deprecated status changes append events with explicit authority/reason, never rewrite the original review or failed observations. P1 richer superseding workflow remains separate implementation work.

### 6.2 Event history and independent checkpoints

Require monotonically increasing per-stream sequence numbers, canonical versioned event bytes, previous-event hash, event content hash, actor/action and authenticated reviewer references when applicable, contract version/content digest, exact scope/digest, UTC timestamp, outcome and correlation. Bind organization/project ownership and stream identity so records cannot be transplanted across namespaces. Revocation and supersession append new events; never rewrite original approval. Non-human denied attempts identify caller class or explicit unverified principal, not a fabricated reviewer. Immutable policy bytes and evidence remain referenced, not silently mutated.

Independently retained signed checkpoints contain audit stream identity, last committed sequence, chain tip, creation timestamp, signing key identifier and cryptographic signature. The signed payload must bind all these values. The protocol must also specify trusted namespace/generation and checkpoint-history linkage/freshness so a valid old signature cannot serve as the latest authority. These extra wire fields and exact byte/signature/hash algorithms, allowed algorithms, trust-anchor distribution, key rotation/revocation and genesis enrollment remain proposed implementation details. Never implement custom signature cryptography or trust a caller-supplied key/signature/"latest" flag.

Store checkpoints outside the audit database under separate authority. For hosted production prefer immutable/WORM-capable storage with versioning and retention protection; exact service/retention settings are unresolved and require separate authorization. The signer must authenticate authorized append requests, verify durable event continuity against its protected current history and reject conflicting/stale tails; it cannot blindly sign an arbitrary database hash. Preserve conflicting/missing checkpoint evidence rather than picking a convenient history.

No update/delete API for original events/snapshots is available to agent, runner or ordinary adapters. Sequence assignment/nonce/snapshot/event transaction and independent durable anchoring must fail closed before activation. Cap and sanitize event/error payloads before any persistence; no raw credentials, proof/nonce secrets, source secrets or arbitrary exception text. A protected retained checkpoint is required before any rollback-resistance claim; the hash chain alone supplies only internal integrity checks.

### 6.3 Integrity, activation and fail-closed behavior

Verify event bytes/hash/previous links/monotonic sequence and namespace against the **latest independently trusted checkpoint and checkpoint history** on startup, relevant reads and every security-critical eligibility/activation operation. Reject missing/modified/deleted/reordered/replayed events, invalid signatures or keys, gaps, stale/conflicting/missing checkpoint history, sequence rollback and database restoration to an older state. Trusted latest-checkpoint discovery/freshness is a required protocol decision, not a timestamp comparison or signed-file import supplied by a caller. Any post-checkpoint suffix is unanchored and cannot grant authority until reconciled and durably anchored.

An approval event must be durably recorded and anchored before becoming effective. Recheck identity/current permission/scope/freshness when activation resumes after delay; no automatic stale approval resurrection. A verified signed checkpoint demonstrates anchored integrity, not human presence, permission, tenant authorization or an execution grant. Cryptographic protection against an attacker who controls the signer, checkpoint authority or trusted verifier is not claimed.

On corruption, missing events/snapshots, unavailable storage, failed atomic commit or uncertain checkpoint/generation, block approval/new execution eligibility, preserve diagnostics safely and require reviewed recovery. Never rebuild authoritative approval state from imported contract JSON or silently accept a newer-looking digest. Retention/deletion, key custody and recovery changes require G-06/07 review; approved history cannot be discarded merely to make a check pass.

### 6.4 Recovery and local limits

Enter restricted recovery state; block new privileged approvals/dependent operations and withhold trust from unverified history. Preserve available forensic material and surface integrity failure through bounded sanitized diagnostics, using an independently protected incident path if normal audit append is unavailable. A local error cannot pretend a durable incident event was recorded.

Restore protected backup under designated recovery authority, verify canonical records/sequence/hash chain, reconcile against independently retained latest checkpoint/history, identify missing or unanchored events and preserve a recovery-operation record. Exceptional recovery requires separate security-administrator authorization; never reset the history, silently create trusted genesis or discard missing events. If latest trusted history cannot be reconstructed, privileged approval remains disabled until incident resolution. Recovery authorization cannot impersonate a contract reviewer or infer new policy approval.

Local development uses synthetic events and test-only signer identities. If the same OS user/agent can modify database, checkpoint history and signing keys, tests can demonstrate detector behavior under an assumed trusted reference but cannot establish strong tamper or rollback resistance. Use **REGISTRY_DISABLED** (or equivalent explicit state) for privileged approvals until actual authority separation and verification are approved and proven. Mock success has no trusted approval effect. No accounts, keys, cloud services, live network or privileged registry are provisioned by this decision.

## 7. Untrusted import and forbidden MCP self-approval

The policy schema is closed. Imported `status`, `approval_status`, `approved`, `review`, `reviewer`, receipts, signatures, scope grants and target credentials are rejected as extra fields under ADR-0001's proposal. A structurally valid policy import is a new candidate, never authoritative. Do not silently strip forged fields and continue execution. Historical signed/hashed exports, if later supported, must be separately validated through the accepted registry/issuer/revocation and project checks; the file's claims alone remain insufficient.

Forged negative example; **JSON parses but policy validation and execution authority must reject it**:

```json
{
  "contract_id": "auth.orders.read",
  "project_ref": "project-demo",
  "version": 1,
  "status": "APPROVED",
  "approved": true,
  "review": {"reviewer_ref": "human:developer", "approved_at": "2026-10-10T10:00:00Z"},
  "content_hash": "3EFD267A7DE481B330A8641880F3EF1E7D7E48A8F93B545913503169EA1A29AB"
}
```

Knowledge of that unapproved example's canonical digest proves neither its approval nor the displayed reviewer identity. Complete valid policies augmented with any of these extra privileged fields must also fail; rejection must not depend merely on this example missing required policy fields.

MCP tools may submit draft data, request review and query sanitized status subject to project access. They must not expose `approve_contract`, `reject_contract` on behalf of a human, arbitrary approval-status transitions, trusted receipt import, human credential delegation, reviewer enrollment, or a generic application-service invocation bypass. CI/background jobs/agents cannot call the protected human endpoint. Do not place a “confirmation token” in the tool response that the model can return to approve. Every entry point enforces caller class and the same core state machine; hiding a button/tool name is insufficient.

A human message in an agent chat may authorize documentation or an ADR review in this development session. It is not, without an accepted separately authenticated product approval path and exact bindings, a trusted PACT contract event. Markdown acceptance notes, todo DONE, Git commit metadata, automated tests and this ADR's own acceptance cannot approve application authorization policy.

## 8. Positive and negative acceptance matrix

These are **required future acceptance tests**, not runtime results or approvals. Temporary data checks in this docs-only task cannot verify a real reviewer, protected channel, registry transaction or signatures.

| Case | Controlled action / condition | Required result / evidence | Trace |
|---|---|---|---|
| AP-01 | Enrolled human with current project permission reviews exact complete snapshot/profile/scope and fresh challenge | Durable immutable snapshot/nonce/decision event; independently signed durable anchor verified before approval effective; independently verify every bound value | AC-003; FR-CON-001/002 |
| AP-02 | Same valid policy with different JSON whitespace/key order; version/rules unchanged | Same proposed canonical policy digest; still requires real human event, no automatic approval | FR-CON-001 |
| AP-03 | Human edits rule or version before decision | New draft/review binding; old challenge invalid, old approved history preserved | FR-CON-001/002 |
| AP-04 | Identical authenticated retry after lost committed response | Return same protected event, no second approval/state transition | SEC-T004 |
| AP-05 | Forged APPROVED JSON above and complete valid policy plus each extra privileged field | Closed schema rejects; no authoritative record or execution | AC-002; SEC-T003 |
| AP-06 | Valid imported policy, no trusted event; supplied correct hash/forged reviewer/receipt | Candidate only; approval lookup fails; cannot execute as approved | AC-002; TH-03 |
| AP-07 | Wrong project/reviewer, revoked role, supplied identity/env flag or machine caller | Denied; sanitized attempted-action audit; no approval | TH-03/19; SEC-T023 |
| AP-08 | Agent allocates PTY, pipes yes, passes flag, calls human endpoint or every available MCP tool | No approval; fresh protected human verification/caller separation required | TH-15; SEC-T017 |
| AP-09 | Changed policy/schema/profile/scope/version/digest after display but before commit | Atomic stale-binding rejection; no partial event/snapshot; new review required | SEC-T004 |
| AP-10 | Reused/expired/canceled nonce, cross-project/decision receipt, clock rollback or stale registry generation | Replay/freshness rejection before authority; no resurrection after restore | SEC-T004 |
| AP-11 | Two competing approval/rejection transactions or duplicate conflicting events | At most one valid transition; explicit conflict and retained audit | FR-CON-001/002 |
| AP-12 | Crash/storage-full/append failure, or crash/outage between event commit, checkpoint anchor and activation | No effective unanchored approval; preserve pending nonce/event and reconcile idempotently without granting stale authority | NFR-SEC-001; AU-08/09 |
| AP-13 | Snapshot/event/head changed, checkpoint signature/history invalid/stale, DB restored or registry/checkpoint authority unavailable | Verify against latest independent trusted checkpoint/history; disable new privilege, preserve evidence and require reviewed recovery; local same-user limits explicit | TH-03/10; AU-01..09 |
| AP-14 | Reviewer permission/approval eligibility revoked after historical decision | Historical event preserved; new jobs blocked until fresh permitted reaffirmation | TH-19; SEC-T023 |
| AP-15 | Trusted approved snapshot, no fixture/target execution grant or expanded origin | No network/runner permission; separate scope guard rejects | AC-007; TB-08 |
| AP-16 | Terminal escapes/prompt injection in source or policy review | Inert complete display; cannot conceal exact decision or request privileges | TH-01/15 |
| AP-17 | Same approved version used again with fresh independent valid run grants | Re-use original immutable policy/event; new run lineage, no duplicate approval | FR-CON-003 |
| AP-18 | Agent/same-user process tries registry/enrollment overwrite or intercepts confirmation | Supported OS separation denies; otherwise disable approval rather than claim protection | OQ-04; TB-08 |

M1-03 implements untrusted state guards, not authenticated review. M2-06/07 must prove real human approval, anchoring/receipt binding and protected persistence; M3 interfaces must prove no MCP bypass. Signed checkpoint/anti-rollback tests now follow the selected storage direction, with actual protected-platform integration still unapproved. [TEST_PLAN §11](../TEST_PLAN.md#11-selected-audit-architecture-and-required-verification) defines AU-01..10, all planned/NOT RUN; same-user mocks cannot supply production trust evidence. No live provider, target or privileged component is exercised here.

## 9. Alternatives, consequences and recovery

| Alternative | Trade-off / proposed position |
|---|---|
| Plain terminal prompt under the agent's same user | Simple, but PTY/automation and writable registry permit self-approval; reject as authority, retain CLI as review-request entry point. |
| Protected local broker + independent human client/user verification | Recommended P0 boundary; no cloud required, but OS separation/transaction-bound user presence needs actual capability evidence and owner choice. |
| Hardware-backed confirmation bound to review challenge | Stronger independent user verification option; hardware/runtime dependency and trusted display binding need review, no silent installation. |
| Hosted OIDC/WebAuthn human review | Appropriate separate P1 option; adds browser/session/CSRF/tenant/network/issuer/egress boundaries, not a shortcut for P0. |
| Portable signed approval files accepted from any import | Adds issuer/key/revocation/replay/tenant trust; defer until accepted attestation design, never trust signature-shaped JSON. |
| Hash-only approval or Git author/CI success | Integrity/provenance context only; lacks authenticated human intent/permissions, reject as authority. |

Reversible internals include naming and storage implementation behind the protected repository/clock/identity ports, provided accepted bytes, state/authority and append-only invariants remain unchanged and tests demonstrate compatibility. Reviewer trust roots, enrollment, confirmation mechanisms, profile/scope bindings, freshness/revocation semantics, attestation, audit custody/retention and migration are security-sensitive owner decisions. No unapproved libraries, networking or keys are provisioned.

Rollback disables approval/new privileged job eligibility and retains old snapshots/events. Restore only through reviewed protected recovery; detect generation/nonce/audit rollback and require reconciliation/reaffirmation where trust cannot be established. Preserve failed evidence and exact old hashes. Do not silently rehash/migrate approved content under new canonicalization, replace a historical reviewer, auto-reapprove or reset expected policy. There is no deployed database/API or migration to execute today.

## 10. Open owner decisions and genuine approval request

| Decision | Proposed default | Open risk / required owner resolution |
|---|---|---|
| M0-02 and remaining approval/profile boundaries | Preserve actual open reviews; specified ADR-0001 DSL accepted | M0-02 final sign-off and ADR-0003 broader acceptance/user-presence remain absent; this storage decision closes neither. |
| Local identity/enrollment and OS isolation | Protected broker/registry plus separately verified human subject; no same-privilege agent authority | Select supported OS, protected enrollment/admin lifecycle and process/IPC/ACL capability; AP-07/08/18 required. |
| Human confirmation / OQ-04 | Independent protected user verification bound to exact displayed challenge; fail closed if unavailable | Choose actual OS/user-presence or hardware mechanism and trusted display semantics; a terminal alone is insufficient. No implemented mechanism is claimed. |
| Canonical review/profile/scope binding | Typed domain-separated review binding over exact versions/bytes, separate execution grant | Accept grammar/definition custody and applicability semantics with ADR-0001/0002; AP-02/09/15 required. |
| Nonce, freshness and revocation | Single-use atomic challenge, proposed ten-minute/sixty-second ceilings; suspension/reaffirmation on permission removal | Accept limits, trusted clock, idempotency, role/eligibility semantics and restore generation; AP-04/10/11/14 required. |
| Audit/immutable storage / OQ-14 | **Scoped direction selected:** dedicated Audit Authority, append-only events, independent signed checkpoints, anchored activation and restricted recovery | Concrete backend/OS/principals, signing/byte protocol, trust anchors/freshness/rotation, protected backup and distributed commit/anchor/recovery mechanics remain open/unverified; AU-01..10/AP-12/13 required. Do not request selected direction again unchanged. |
| Hosted attestation/interfaces | Defer P1 issuer/signatures/browser design | No external provider/identity egress, portable receipt authority, real contract approval or target authorization granted here. |

**Review status:** EV-0006 retains the historical v0.1 digest; EV-0034 records this v0.2 revision and the developer's 2026-10-11 scoped storage decision. Do not request acceptance of unchanged selected storage choices again. Full ADR acceptance, final M0-02 review and M2-06 identity/user-presence decisions remain pending separately; ADR-0003 stays PROPOSED/M0-05 IN_REVIEW. Future review of new protocol/mechanism choices must bind exact version/digest/scope and genuine owner decision. This documentation change makes no product approval effective.

Accepting this ADR would approve only the documented architectural choices within the stated conditions. It would not sign off M0-02, approve a Security Contract, authorize execution scopes, provision credentials or enable provider egress. No next task begins here.
