# Local human-approval broker feasibility study

> **Version / date:** 0.1 / 2026-10-11
> **Status:** PROPOSED / ANALYSIS ONLY — protected feasibility NOT PROVEN
> **Task / trace:** M0-05; OQ-04/14, FR-CON-001/002, NFR-SEC-001, AC-002/003; TB-08 and proposed TB-09
> **Authority state:** REGISTRY_DISABLED — no effective approvals or target permission
> **Evidence:** todo.md EV-0066; base HEAD `943cd681c15fe88ff1657478016216ea83da7c0c`

## 1. Purpose and unchanged review bindings

Continue the owner-authorized foundation work with a concrete design/verification proposal for the selected **separate protected local broker** and **Windows + Linux** direction. This is not acceptance of [ADR-0003 v0.3](adr/0003-human-approval.md), a new ADR, implementation of M2-06/07 or permission to set up accounts, services, keys, ACLs, networks or dependencies. The current [foundation package](P0_FOUNDATION_REVIEW.md) and four digest-bound review revisions remain unchanged. “Continue” is not final security sign-off or tooling/fixture acceptance.

Only this document and todo.md change. Read-only platform facts and primary documentation support design analysis; no broker/client/registry exists and no human approval, IPC security, hardware capability, Linux runtime or audit-integrity test runs. An API's documented capability is not proof that the PACT profile enforces it.

## 2. Current feasibility evidence

| Observation on 2026-10-11 | Actual result | What it does not establish |
|---|---|---|
| Environment.OSVersion / architecture | Microsoft Windows NT 10.0.26300.0; OS and process 64-bit | Windows/Linux support or isolated execution profile |
| WindowsIdentity.IsAuthenticated | true for current process token | Named human reviewer, enrollment, current project permission or deliberate review |
| WindowsPrincipal.IsInRole(Administrator) | false for current token | Absence of all elevated capabilities, ability to isolate reviewer from agent or protection against host administrator |
| Environment.UserInteractive | true | Human user-presence, trusted display or transaction consent |
| Get-Command wsl.exe / docker.exe | WSL found on PATH; Docker not found on PATH | Installed/runnable Linux distribution, container availability elsewhere, isolation or permission to start either |
| Repository inspection | Untrusted domain approval model only; no protected broker, credential verifier, audit registry or workspace tooling | Real receipt, trusted reviewer or AC-003 completion |

No username/SID, credential, key material, biometric data or unrelated machine inventory is collected for this study. The existing developer reviewer assignment is a project review role, not OS enrollment. Linux verification is NOT RUN; WSL presence is not a substitute for a separately reviewed Linux host profile.

## 3. Proposed authorities and permitted messages

Labels below identify logical roles, not created accounts, service names, credentials or assigned operators. Deployment identities, storage paths and IPC addresses are UNCONFIGURED.

| Proposed role | Permitted actions | Forbidden coupling / required proof |
|---|---|---|
| Agent/CLI/MCP/runner principal | Submit typed draft or review request; read access-scoped sanitized status | Cannot enroll humans, approve, edit snapshots/history/checkpoints, use signer keys, control reviewer display/process or override profile state |
| Human reviewer principal and protected review client | Fetch immutable pending snapshot, inspect complete escaped policy/diff/profiles/scope, deliberately approve/reject with fresh verification | Separate from agent identity/session/automation authority; identity derived from authenticated channel plus protected enrollment, never client JSON |
| Approval Broker principal | Validate/recompute binding, enforce current project permission, consume challenge, coordinate pending decision/anchor/activation | No automatic self-enrollment or machine-to-human role conversion; verifier fails closed if reviewer channel/custody is uncertain |
| Dedicated Audit Authority | Authenticate bounded append intents, serialize monotonic events and immutable snapshot references | Ordinary clients cannot alter/delete history; audit administration and review permission are different |
| Checkpoint signing and retention authorities | Verify committed stream continuity, sign exact checkpoint, independently retain latest trusted history | Separate signing/retention custody; no blind signing of caller-supplied hash, agent-readable private key or caller-selected latest checkpoint |
| Security administration / exceptional recovery authority | Protected enrollment/revocation and separately authorized forensic recovery | Cannot silently rewrite history, create trusted genesis, infer contract approval or grant scope through recovery |

Separate machine request/status and protected human decision interfaces. Both use the same core validation and project checks; endpoint names are not authorization. No generic method dispatcher, approve_contract MCP tool, transferable approval bearer token or imported authoritative status. A reviewer client must authenticate the broker as well as the broker authenticating the caller: a counterfeit local endpoint/display can substitute a different review.

Trust in the OS, protected human client and administrative custody is explicit. If the agent can control the reviewer's session, IPC/enrollment/approval store, signing authority or trusted display, the supported profile is unavailable and privileged approval stays REGISTRY_DISABLED. A non-admin token alone does not resolve same-user control. Host administrator/root compromise is outside a proposed local separation guarantee, not solved by a socket ACL.

## 4. Platform mechanisms to investigate, not activate

### 4.1 Windows candidate

Propose dedicated non-agent service principals, protected immutable installation/enrollment/state locations, and local named-pipe IPC with explicitly minimal DACL rights. Microsoft documents that default pipe descriptors can grant read access to Everyone/anonymous and that generic write rights include pipe-instance creation; therefore use reviewed explicit rights and test endpoint ownership/name-squatting rather than assuming a pipe name is trusted. [Named-pipe security and access rights](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights).

Authenticate the connected security context through reviewed OS APIs, not a supplied SID/process name. If client impersonation is used for identification, limit its purpose and privilege, reject failure, and restore the original thread context on every path; never continue a privileged operation after identity verification fails. Microsoft describes the token/impersonation behavior and API failure results. [Client impersonation](https://learn.microsoft.com/en-us/windows/win32/ipc/impersonating-a-named-pipe-client), [ImpersonateNamedPipeClient](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-impersonatenamedpipeclient).

Remaining proof: local-only endpoint enforcement; server authentication; connection/handle inheritance and impersonation-level constraints; separate reviewer desktop/session/process authority; enrollment/registry/checkpoint/key ACLs; inability of the agent to inject or automate trusted review; account lifecycle, cancellation and recovery. No named-pipe API is invoked or service/privilege/ACL changed to test these claims here. Windows token metadata is discovery evidence only.

### 4.2 Linux candidate

Propose separate non-agent service UIDs, a pathname AF_UNIX stream socket under a protected directory, explicit owner/group permissions, and kernel-derived peer credentials mapped to protected enrollment. Linux man-pages documents pathname/directory permission checks and SO_PEERCRED's credentials at connection establishment. Avoid abstract sockets as a substitute for filesystem permissions; connection-time credentials do not prove fresh human action or current project permission. These are Linux-specific capabilities, not portability or PACT integration guarantees. [unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html).

Remaining proof: namespace/UID mapping, socket replacement/symlink/stale endpoint resistance, server authentication, current role rechecks, separation from reviewer session/IPC/display and ptrace/debug/credential access, descriptor inheritance, service hardening, storage/checkpoint/key ownership and recovery. No world-writable endpoint or same-UID fallback. Exact host/kernel/service profile is UNCONFIGURED; Linux and WSL tests are NOT RUN.

### 4.3 Fresh human verification and trusted display

Two unaccepted mechanism candidates remain:

| Candidate | Proposed role in the broker flow | Open feasibility issue / recommendation |
|---|---|---|
| Protected native human client in independently controlled reviewer session, fresh OS-backed verification | Reviewer identity and explicit decision bound to broker challenge; signed or authenticated client evidence under protected custody | Concrete Windows/Linux verification APIs, trusted display, transaction binding, client custody and automation resistance not proven. Avoid password/PIN collection in agent-controlled CLI or a reusable login flag. Do not select an API merely because it reports an interactive user. |
| Protected reviewer browser/client plus enrolled WebAuthn authenticator requiring user verification | Potential common authentication ceremony bound to broker-generated challenge; broker validates enrolled credential, signature, challenge, RP ID/origin and current permission | Requires additional TB-09 origin/session/browser/CSRF/certificate and authenticator custody design; no listener, browser, RP identity or key is configured. Authenticator/hardware/browser availability and genuine anti-automation tests remain unknown. Investigate only as a proposal, not an automatic dependency or hosted-service requirement. |

WebAuthn distinguishes presence from verification and uses relying-party challenges in authentication assertions. Its credential/UV result does not by itself name an authorized reviewer; protected enrollment is necessary. **Inference for PACT:** authentication evidence also cannot prove the human saw and accepted specific policy bytes without a trusted display and exact broker transaction binding. Require fresh verification and complete displayed policy/diff/scope; reject substituted challenges or an agent-controlled reviewer channel. This proposal refers to the Level 2 Recommendation as a documented protocol baseline, not a claim that it is the latest level or a chosen implementation. [W3C WebAuthn Level 2](https://www.w3.org/TR/webauthn-2/).

No “touch only,” TTY, environment flag, correct hash, signed-looking file or automatable button fallback. A shared authenticator/PIN or compromised human client is a residual custody risk. Selecting a verification mechanism requires capability/identity/display evidence and owner acceptance, not just enabling userVerification in an example.

## 5. Proposed exact-bound flow and failure handling

This refines the flow for review; byte/signature/clock protocols remain PROPOSED and unimplemented. No new policy canonicalization replaces accepted pact-json-1. Review binding, audit event and checkpoint profiles remain separate and must be specified/tested before acceptance.

1. The broker rejects malformed/ambiguous policy, extra privileged fields or unknown profile/scope references. It snapshots immutable canonical policy bytes and recomputes the accepted policy digest. Bind project, contract/version/schema, draft revision, profile IDs/versions/digests, applicability-scope digest, operation and registry generation.
2. Independently authenticate/enroll the reviewer and recheck project permission. Create a cryptographically random single-use challenge referencing the exact immutable review binding and requested APPROVE/REJECT operation. A challenge returned to an agent is not a capability to decide. Preserve ADR-0003's proposed ten-minute challenge/sixty-second fresh-verification ceilings as candidates, not activated limits.
3. The separate human client authenticates the broker and displays complete escaped policy, change diff, unresolved questions, applicability, policy/review digests and exact version. The human deliberately selects an operation and performs fresh protected verification. Changed displayed content, decision, scope or draft revision invalidates the challenge.
4. The broker verifies the ceremony/channel, reviewer enrollment/current permission, exact challenge/binding and expiry, then compare-and-swaps the reviewed NEEDS_REVIEW revision. Persist immutable decision/snapshot intent and consume the nonce through the protected authority. The outcome is PENDING_ANCHOR, not effective approval.
5. The signing authority verifies committed sequence/canonical bytes/previous hash against its trusted history and produces a signed checkpoint. A separately controlled store durably retains it. The broker verifies the latest trusted anchor and unchanged reviewer/policy/scope eligibility before activation. Never infer a distributed atomic commit or latest trusted history from caller input.
6. Only a verified anchored decision becomes eligible for later lookup. Return an opaque status handle; a separate target/fixture/execution grant is still required. Revocation/supersession is append-only. Failed/canceled/expired review stays non-authoritative; corruption/unavailable authority enters disabled or restricted-recovery state and cannot mint approval.

Crash after append but before anchoring preserves pending history/consumed nonce. An authenticated exact retry reconciles the same intent rather than creating a second approval. Stale permission or changed binding during reconciliation blocks activation. Anchor outage, signing failure or an unavailable latest-history authority cannot downgrade to local hash-chain trust. Recovery requires separate authorization, protected backup/latest checkpoint reconciliation and retained incident evidence; no automatic genesis reset.

## 6. Required feasibility and acceptance evidence

All rows are **PLANNED / NOT RUN**; they extend the AP/AU coverage plan without implying new executable tests. Record platform/profile, exact expected outcome, actual sanitized trace and limitations for each future run.

| Case / existing trace | Positive check | Adverse/failure check and required result |
|---|---|---|
| LF-01 / AP-07/18 | Enrolled reviewer authenticated through approved Windows/Linux channel | Supplied identity, wrong principal/project, revoked role or endpoint spoofing rejected before decision |
| LF-02 / AP-08/16/18 | Genuine human sees complete exact transaction and completes fresh verification | Agent PTY, stdin/flags, UI automation, reused login, request/display/challenge substitution or malicious source text cannot approve; unsupported separation disables profile |
| LF-03 / AP-05/06/09/15 | Exact approved schema/version/profile/applicability binding | Forged APPROVED import, extra privileged fields, edited body, version/scope/profile swap or missing execution grant cannot authorize |
| LF-04 / AP-04/10/11/14 | One atomic nonce consumption; exact lost-response retry reconciles same event | Replay/expired/canceled/cross-project nonce, concurrent conflicting decisions, permission removal or clock uncertainty fails closed |
| LF-05 / AP-12/13, AU-01..09 | Durable committed event and independently retained latest signed anchor precede activation | Append/sign/store/lookup failures, crash at each stage, forged/stale/conflicting anchor, gap or rollback cannot activate approval |
| LF-06 / AP-18, AU-06/08 | Actual tested storage/signing/retention/enrollment separation | Agent edits history/checkpoint/enrollment, reads signer key or controls human client: deny or mark unsupported, never claim local tamper resistance |
| LF-07 / AU-10 | Authorized restricted recovery reconstructs exact trusted continuity | Old backup, missing/unanchored suffix, rollback or unauthorized reset preserves evidence and leaves approvals disabled |
| LF-08 / AC-002/003 | Real deliberate human approval creates one immutable version and truthful lineage | CLI/MCP/CI machine callers cannot invoke privileged decision; logs disclose no credentials/proof secrets; no target/provider call from approval |

LF-02 requires a real human positive and an independently controlled machine-caller negative under the accepted profile. Mocked identity, flags, WebAuthn-shaped JSON or a simulated reviewer cannot satisfy it. Source/static checks of this proposal cannot satisfy any LF/AP/AU runtime row.

## 7. Bounded continuation and owner gates

1. Finish documentation and protocol/interface planning while preserving pending review digests and REGISTRY_DISABLED; done only for this analysis increment.
2. After the required ADR/threat/tooling gates and a concrete bounded task are authorized, implement pure synthetic challenge/anchoring state and injected failure tests with test-only identities. No mocked result becomes a trusted approval; do not start M2-06/07 from this proposal.
3. Prepare a concrete Windows/Linux profile: real principal/operator/admin assignment, enrollment/revocation, local endpoint custody, trusted human client/verification method, storage/signer/checkpoint protocol and threat limits. Obtain necessary mechanism/setup scope before any protected provisioning.
4. Under that scope, independently verify OS/channel/storage separation and run genuine human plus adverse cases. Record failed/missing checks. Ask for final mechanism acceptance only with capability evidence and exact revised digest; keep unsupported profiles disabled.

Read-only analysis can show candidate mechanisms exist in documentation. It cannot establish operational separation or protected human intent on the current machine. No new owner decision is requested in this session; the existing tooling/threat/fixture review is pending, and broker/OS/audit directions are already selected. Full M0-05/M2-06 acceptance remains open. M0-07 still waits for actual M0-06 closure and tooling/acquisition scope.

## 8. Actual checks, limitations and provenance

Read-only Git/task/requirement/ADR inspection and current-process platform/token metadata ran. Public primary documentation was read using generic API queries only; no repository/source/evidence/credential content was sent to a provider or benchmark service. Direct man7 and CreateNamedPipe page fetches failed; unix(7) facts were available through the primary-source search excerpt. Do not claim an unread API page or failed fetch as verified implementation evidence.

Local document/digest/link/ledger/history/file-preservation and whitespace checks are recorded with exact command/results in EV-0066. Runtime/unit/install/build/lint/type/CI, IPC/ACL/OS/user-presence/credential ceremony, Linux/WSL, signing/anchoring/recovery and genuine approval tests are NOT RUN. No account, service, credential, key, ACL, target, deployment or dependency was created or activated. Current foundation review documents remain byte-identical to EV-0065.
