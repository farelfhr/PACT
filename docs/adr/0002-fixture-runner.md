# ADR-0002 — Synthetic fixtures and bounded local runner

> **Status: PROPOSED — approval requested; NOT ACCEPTED**
> **Draft version:** 0.3, 2026-10-11; P0 foundation reconciliation, not approval
> **Author / task:** Codex / M0-04
> **Decision owner / security reviewer:** Repository developer; acceptance pending
> **Trace:** OQ-03/06; FR-TST-002; supporting FR-TST-001/003/004/005/006/007, NFR-SEC-001/003/004/005, NFR-REL-001; AC-004/005/006/007/011/015/016/017

## 1. Context, prerequisites and authority

[PRD](../../PRD.MD) requires repeatable synthetic actor/resource setup, genuine authentication, safe teardown and authorization assertions. [Architecture M0-04](../ARCHITECTURE.md) requires actors, a safe target, authentication, teardown, 404 semantics, redirects, budgets and negative examples. Its M0-02 dependency is **unmet**: [SECURITY v1.0.4](../SECURITY.md) remains IN_REVIEW, with changes requested and no final human sign-off. [ADR-0001](0001-contract-dsl.md) has accepted specified DSL choices (EV-0013); this does not accept fixture/runner or human-review architecture.

The owner explicitly authorized: "Draft the PROPOSED ADR only; keep M0-02 and implementation gates unresolved." This is permission to prepare this document, not acceptance of its decisions, a waiver of the dependency, or permission to execute. At intake the actual repository contained fifteen documentation/example files, no source packages, demo, runner, build configuration or executable project tests. Existing working changes are preserved; [todo.md](../../todo.md) records provenance and checks.

**Review history:** Developer requested changes to v0.1, raw SHA-256 `3D8E7593A76C0BDCDF110232DB9656BFA7B8F8384A4BEA6D4151E93C5FBB0A6C`, explicitly withholding approval, M0-02 sign-off, execution/contract authorization and provider egress. Historical v0.2 clarified cross-test isolation, invalid routes, deterministic outcome classification and the §10 decision matrix (EV-0007). ADR-0003 now exists as PROPOSED v0.3, with selected audit-storage/broker design directions but no full acceptance. EV-0005 retains v0.1 history; EV-0065 binds this v0.3 reconciliation.

Every decision and example below is a proposal. There is no running service, selected transport API, approved endpoint, active credential or implemented sandbox. Addresses are illustrative synthetic test bindings, never a grant to contact them. Expected example outcomes are design assertions, not observed test results.

Mandatory TB-08 human authority is retained: AI, CLI/MCP automation, imported JSON and task status cannot approve a contract, grant execution scope, raise budgets, enable provider egress or accept this ADR. Policy approval, fixture trust, target authorization and runner containment are distinct prerequisites. G-01/02/03/04/06 in [workflow.md](../../workflow.md) remain applicable.


**Current repository (2026-10-11):** the preceding M0-04 intake is historical. Domain/normalizer/untrusted approval-model/provisional parser/fake-provider code and unit fixtures exist; no demo marketplace, authentic fixture/session adapter, authorized transport/executor or build/lock/CI exists. This v0.3 updates references only; §6 budget values, all FX cases and verdict semantics are preserved. The owner selects Windows + Linux as tooling targets, not proven runner containment. Each runtime profile remains disabled until its OS-specific isolation, transport and cleanup mechanisms are reviewed and verified. [Foundation review package](../P0_FOUNDATION_REVIEW.md) lists exact open choices and review digests.

## 2. Proposed fixture adapter and deterministic facts

Start with one explicitly selected local FastAPI marketplace **test application**, with safe, intentionally vulnerable and patched variants. It is a disposable synthetic target, not a production template. FastAPI and HTTPX are technology proposals; versions, dependencies, operating systems and enforcement APIs belong to M0-06 and subsequent tasks. No general reconnaissance, arbitrary repository code execution or target discovery is supported.

The application layer uses a typed fixture port; infrastructure owns seeding, authentic target login and transport. Proposed operations are `prepare`, `authenticate_actor`, `verify_snapshot`, `observe_read_state` and `cleanup`. These are interface concepts, not installed commands or a frozen public schema. Do not dynamically import an adapter named by model data. Only operator-selected, reviewed adapter implementations may run, and their setup operations need a separate authorized fixture-control capability.

The initial dataset has seller A / tenant A / order A and seller B / tenant B / order B. Stable logical labels map to target-specific IDs in a run-owned namespace. The snapshot records dataset/version/seed, adapter/version, target variant/build, run/project IDs, role, principal, verified primary tenant, owner, membership and explicit sharing edges. Target tenant IDs, PACT project IDs and reviewer identities are separate types.

Facts must be complete and established by trusted fixture setup plus independent authentication/existence checks, not inferred from the denial response or copied from model claims. Missing facts fail preflight. Explicitly absent sharing/membership in a complete graph means absent; unknown does not mean absent. ADR-0001's accepted relation signatures and conflict/unmatched NEEDS_REVIEW behavior determine DSL semantics; trusted fixture facts and a genuinely approved contract remain separate requirements. Multi-tenant memberships or sharing extensions need complete fixtures and reviewed expected rules; do not invent owner/administrator privileges.

Synthetic fixture illustration, **not an approval record or production adapter payload**:

```json
{
  "fixture_version": "marketplace-read-1",
  "seed": 17,
  "namespace": "run-example-001",
  "actors": [
    {"label": "seller-a", "principal_id": "actor-a", "role": "seller", "primary_tenant_id": "tenant-a", "session_handle": "session-a"},
    {"label": "seller-b", "principal_id": "actor-b", "role": "seller", "primary_tenant_id": "tenant-b", "session_handle": "session-b"}
  ],
  "resources": [
    {"label": "order-a", "resource_id": "1001", "type": "order", "owner_id": "actor-a", "tenant_id": "tenant-a", "protected_marker": "synthetic-order-a"},
    {"label": "order-b", "resource_id": "1002", "type": "order", "owner_id": "actor-b", "tenant_id": "tenant-b", "protected_marker": "synthetic-order-b"}
  ],
  "memberships": [{"actor_id": "actor-a", "tenant_id": "tenant-a"}, {"actor_id": "actor-b", "tenant_id": "tenant-b"}],
  "shares": [],
  "facts_complete": true
}
```

`session_handle` is an opaque local capability reference, never a token in exported fixture data. `facts_complete: true` in untrusted data is insufficient: only the trusted adapter may attest completeness after checking bindings. The protected markers are synthetic canaries, not secrets or evidence to export automatically. Repeated runs preserve logical facts and expected decisions; actual tokens, timestamps and unique namespace IDs may differ. Comparison requires compatible dataset, adapter, contract/profile, target and environment fingerprints; do not compare raw artifacts as if volatile bytes were identical.

Allocate a unique namespace and fresh actor clients/sessions for every run and test case; the illustration's namespace is not a reusable global fixture. Reproduce the logical dataset from its deterministic seed without reusing mutable records, bearer sessions, cookie jars, connection credential state or caches from a prior test. No concurrent tests share writable fixture state. Reject a handle, resource or cleanup request owned by a different run/project/case before use. Check baseline before and after each case; failure quarantines the affected namespace and prevents the next case from inheriting it. Parallel fixture support requires independent namespaces and an accepted concurrency profile; the initial candidate is serial. “Deterministic” describes facts and assertions, not predictable production credentials.

## 3. Authentic independent actor sessions

Propose a target-owned synthetic login endpoint that issues short-lived opaque bearer sessions bound server-side to the seeded principal and tenant. Each actor authenticates through the real demo authentication middleware with its own synthetic credentials. Passwords/tokens stay in the isolated fixture credential store; examples contain handles only. No production accounts, shared administrator session, hard-coded reviewer credential or fake actor header is allowed.

Maintain separate clients, token handles and cookie jars for A and B. Verify non-equal credentials and independent principal/tenant identities; merely different token strings are insufficient. A read-only identity probe through each session and paired owner-resource positive controls must prove that A is A and B is B. Cross-switch checks must demonstrate that each request uses the intended actor's session. Ensure the target itself does not accept client-controlled actor/tenant headers as authentication. The fixture-control identity must never substitute for a scenario actor.

Preflight checks session validity/expiry, project/run binding, resource existence and baseline state; recheck after uncertain authentication failures or expiration. Missing, wrong, expired or revoked tokens, login redirects, broken middleware, identity collisions or a failed owner control yield ERROR (or INCONCLUSIVE when observation is insufficient), never PASS or a verified authorization VIOLATION. A response's 401/403/404 does not prove the request had valid authentication.

The proposed first assertion profile permits 403/404, not 401. ADR-0001's accepted DSL includes an optional 401 profile; that profile remains unsupported for this initial fixture adapter until its use is separately reviewed with a reliable validity observation; an expired session cannot count as a successful denial. Auth protocol selection and identity-probe bindings require developer acceptance; no server endpoint is implemented here.

## 4. Lifecycle, cleanup and containment

### 4.1 Ordered lifecycle and failure handling

1. **Validate before side effects:** resolve authentic contract/profile approval, project access, independent fixture and execution grants, expiry/revocation, complete numeric limits, adapter/version and supported containment. Reject missing approval or scope before any target request, including login and seeding.
2. **Prepare disposable state:** allocate run namespace/workspace; seed only owned synthetic records through the bounded fixture-control capability; record completed stages. No arbitrary SQL, shell, model-supplied setup code or global production reset. Partially prepared state still requires cleanup.
3. **Authenticate and preflight:** independent actor sessions, identity/resource positive controls, complete relation graph and read baseline. Only then move a valid job to READY and RUNNING. Setup failures cannot reach authorization assertions.
4. **Execute declarative reads:** immutable approved contract/profile and verified fixture snapshot; fixed adapter route slots, scoped transport and reserved budgets. No LLM in the verdict path, automatic scope discovery or assertion revision to fit a response.
5. **Finalize in all terminal paths:** success, error, limit, cancellation, expiry and partial setup each enter bounded cleanup. Stop new scenario requests first; kill owned descendants and close transport; revoke actor credentials/grants; destroy owned fixture state/workspace; independently check removal and absence of residual sessions/processes. Persist only sanitized metadata and cleanup status.

Keep a separate narrow fixture-controller cleanup capability and reserved cleanup budget so exhausting the scenario budget or revoking actor sessions cannot prevent teardown. Cleanup cannot reuse a revoked execution grant, extend expiry, escape its namespace or discover new targets. If safe removal cannot complete within its grant/budget, quarantine the fixture, report FAILED_INFRA/job and ERROR or CANCELED with reason for affected scenarios, preserve sanitized diagnostics and require operator recovery. Never reuse a dirty fixture. Previously observed assertions remain historical observations, but a cleanup failure makes the run non-success; it cannot be an all-green run or comparable clean baseline.

Cleanup is idempotent and ownership checked: already removed resources are acceptable only with trusted removal/existence evidence. Never delete arbitrary paths based on untrusted resource IDs. Startup orphan recovery must identify owned abandoned namespaces without touching another run; its authority, grace interval and supported process-termination mechanism remain open in §10. Cancellation and limit stops preserve prior evidence rather than rewriting verdicts to PASS.

### 4.2 Required isolation envelope; mechanisms remain open

Propose a separate disposable, non-root, non-privileged container with a reviewed namespace/syscall profile. On platforms where that envelope cannot be enforced, stop; a dedicated low-privilege account/process alternative requires a documented capability matrix and separate security acceptance. Never silently fall back to the current user's unrestricted process. Windows/Linux support and actual container runtime remain undecided; a container label alone is not containment evidence.

Require read-only runtime/root, a bounded per-run writable workspace, no host home/repository/secret directories, host PID/network namespace, Docker/other control socket, host device, broad mount or privilege/capability elevation. Reject path traversal and symlink escape. Supply only the reviewed adapter and synthetic snapshot, not arbitrary target/repository code mounted into PACT. Control-plane container creation, if eventually chosen, is separate trusted provisioning; untrusted execution receives no provisioning socket.

Network is default denied except exact declared target/fixture-control destinations and an explicitly reviewed resolver path if DNS is needed. No ambient proxy, cloud metadata, provider connection, unrelated private network or internet access. Credentials are run/project scoped and short-lived; no inherited developer/cloud credentials. CPU, memory, processes, file descriptors, disk, response bytes and time are finite and enforced. Host/process/network cleanup and controller survival must be tested on each supported OS; P1 compromised/private-runner result authentication needs ADR-0007, outside this task.

## 5. Independent target grant and bounded transport

### 5.1 Target binding

An authenticated execution grant must bind project/run, issuer identity, approved contract hash/version/profile digest, fixture ID/version, target/environment fingerprint, exact origins and connected IPs, ports, protocols, adapter route/method allowlist, credential handles, budgets, expiry and revocation. A contract or fixture file alone cannot create that grant. Approval receipt format remains ADR-0003 work; no importable `approved: true` shortcut is proposed.

Initial scenarios are GET reads of declared order IDs. A separate fixture-control capability may permit only reviewed login/seed/cleanup/identity operations on disposable state; it must enumerate methods/routes and count requests. GET must not be assumed side-effect free: baseline/after observations and cleanup check the declared protected state. Writes, grant/revoke flows or expanded routes need a new grant and reviewed fixture/profile support.

For an illustrative local profile, one exact origin could be `http://127.0.0.1:8765`, allowed IP set `{127.0.0.1}`, with one adapter-bound route `/orders/{resource_id}` whose slot accepts a verified decimal resource ID only. This is **not** an authorized address. Plain HTTP would be permissible only inside the specifically accepted isolated local synthetic environment, never across LAN or externally reachable interfaces; TLS verification is required for any separately approved HTTPS destination. Initial proposal grants neither wildcard loopback nor the entire RFC1918 range. Namespace-specific port/IP bindings must be verified before the first credential transmission; unexpected target processes fail closed.

The adapter constructs a typed route from verified IDs; models cannot supply a URL or interpolate paths. Normalize scheme, host/IDNA, IP literal, port and allowed path before scope checking. Reject userinfo, fragments, unapproved query keys, encoded path separators/traversal, ambiguous normalization, unsupported schemes (`file`, `ftp`, `gopher`, Unix sockets), broad wildcards and URLs with an out-of-scope host even if a string prefix matches. Do not inherit environment proxy configuration. Exact URL parsing rules and a corpus for IPv4/IPv6/IDNA/percent encoding must be agreed with actual chosen transport; unsupported ambiguous forms are rejected, not guessed.

### 5.2 Redirect and DNS rebinding handling

**Initial redirect budget is zero:** disable automatic redirects; any 3xx, including a login redirect, is a non-PASS transport/authentication outcome, with sanitized reason. Never send a second request merely to inspect `Location`. Out-of-scope redirection is refused before that request (AC-015). Reject in-scope redirects too under this initial profile; do not call an unfollowed redirect an authorization PASS.

Future redirect support needs a separately accepted profile and execution grant: each hop is normalized, resolved and connected within scope; bounded hop/request/time budgets apply; forbid downgrade and forwarding credentials/cookies across origins; strip sensitive headers and re-establish approved actor binding. No redirect acceptance is granted by this ADR proposal.

For DNS destinations, validate all A/AAAA results against the grant and pin a selected approved address for the connection while retaining the verified hostname for TLS identity. Reject empty, mixed permitted/forbidden or changed out-of-scope answer sets. Enforce the actual connection peer against the grant **before any credential/request bytes**; validation followed by unconstrained client re-resolution is insufficient. Repeat destination enforcement for every new/retried connection. Resolution itself must use an authorized resolver path and finite budget; the initial IP-literal-only profile needs no DNS traffic.

Use transport enforcement and isolation/network policy together. Block undeclared loopback/private/link-local/metadata destinations; explicit synthetic local IP exceptions are narrowly granted, never inferred from “localhost.” If proxy routing, connection pinning, peer verification or TLS checks cannot be enforced by the selected library/OS, reject the profile before execution. Exact APIs, DNS TTL/reconnect behavior and enforcement tests remain §10 decisions; no proof of rebinding protection exists today.

## 6. Finite proposed resource budgets

The following **illustrative candidate limits** are finite starting points for a tiny local read fixture. They are not benchmarks, selected configuration, approved privileges or actual enforcement. Developer acceptance and OS-specific measurement are required before use. Missing fields, booleans/floats as integers, zero/unlimited values, unknown fields, inconsistent totals or values above accepted ceilings reject preflight; no fallback to unlimited defaults.

```json
{
  "budget_profile": "local-read-candidate-1",
  "scenario_requests_max": 160,
  "cleanup_requests_reserved": 32,
  "total_requests_max": 192,
  "validation_attempts_max": 384,
  "dns_lookups_max": 0,
  "concurrency_max": 1,
  "requests_per_second_max": 5,
  "connect_timeout_ms": 1000,
  "request_timeout_ms": 3000,
  "execution_wall_ms": 120000,
  "cleanup_wall_ms": 15000,
  "total_wall_ms": 135000,
  "redirects_max": 0,
  "retries_max": 0,
  "request_body_bytes_max": 16384,
  "response_header_bytes_max": 16384,
  "response_body_bytes_max": 65536,
  "aggregate_response_bytes_max": 8388608,
  "cpu_millicores_max": 1000,
  "memory_mib_max": 256,
  "processes_max": 64,
  "file_descriptors_max": 128,
  "workspace_mib_max": 64
}
```

Scenario-request accounting includes seed/login/identity/positive controls and read observations, not just policy assertions. Each attempted outbound request consumes budget before dispatch; denied attempts have bounded validation counts, and connection/DNS costs consume wall time. Cleanup uses only its reserved requests/time; unused capacity is not a reason to expand scope. Total counters span all clients, phases and redirects/retries; no per-actor reset. No automatic retries in the initial profile. Rate limiting and waiting count toward wall time; concurrency includes fixture operations.

Bound compressed and decoded response sizes, header bytes, streaming duration and aggregate bytes while reading, not after full buffering; stop oversized bodies before persistence. All request/query/body sizes and operations are schema bounded. CPU/memory/process/disk limits apply to both target and runner where their isolation profiles require them; the separate trusted cleanup controller also has an accepted finite envelope. Exact controller overhead/profile remains open rather than inheriting unrestricted host resources.

Stop on limit, cancellation, revocation or expiry; never increase budgets automatically. Expiry cannot be extended to finish a request. Record a sanitized reason: preflight invalid scope/limits -> BLOCKED_SCOPE, execution expiry -> EXPIRED, cancellation -> CANCELED, infrastructure/limit failure -> FAILED_INFRA with affected scenarios ERROR/CANCELED/SKIPPED and explicit reasons. An unobserved required assertion cannot become PASS; `COMPLETED` is not a security verdict. Cleanup still follows §4 through its independent capability.

## 7. Denial and intended-function assertions

Use the versioned `object-read-allow-v1` and `object-read-deny-403-404-v1` definitions included in the accepted ADR-0001 design; bind the accepted exact profile digest rather than a mutable name. Profiles are expected behavior only after human policy approval. Initial routes/assertions are adapter-declared; models cannot add fields, scripts, eval, templating or assertions.

For ALLOW, require valid authentication/fixture, known existing intended resource, HTTP 200 and the intended authorized resource fields/function. A 500, login page, missing/wrong resource or empty success body cannot PASS. Infrastructure failures produce ERROR; reliable wrong access behavior can be VIOLATION only against approved rules and verified prerequisites.

For DENY, require those same authentication/existence facts and a reliable complete observation. Accept 403 or 404 only if the exact approved profile permits it **and** no protected resource content or protected state modification occurred. Compare before/after protected-state snapshots through a narrowly scoped trusted observation port. Missing state visibility is INCONCLUSIVE, not proof of no modification. A real missing resource's 404 is not denial evidence: first establish existence with trusted seeding and a successful independent owner control for that same resource/run.

The initial adapter must declare authorized and protected field sets, payload/encoding limits and known resource markers. Inspect bounded decoded body and headers (including redirect/cookie/header disclosure); distinguish the intentional generic denial envelope from protected object fields/values. A generic error body, absence of one canary or lack of a known token is not sufficient proof of non-disclosure. Unexpected content types, unrecognized/partial encodings, opaque payloads or truncated observation yield INCONCLUSIVE/ERROR. A 403/404 with reliable protected data or a state change is VIOLATION with valid prerequisites; redact before persistence/export. Resource IDs/links in responses are assessed according to the approved field profile, never silently presumed public.

This asserts the declared object-read disclosure/state profile only; it does not establish freedom from timing, existence-oracle, covert-channel or whole-application vulnerabilities. If 401 support, additional denial statuses, richer resource fields or side-channel assertions are desired, request reviewed versioned definitions and compatibility rules. No status-only PASS or model-based verdict is allowed.

### 7.1 Route controls and deterministic classification

Bind the requested method/route to the reviewed adapter and target build before assertions. An independent owner GET for **the same existing resource and route** must work through the same routing/authentication layer. A typo, wrong method, unregistered route, stale target build or framework-level 404 is an adapter/precondition ERROR, not successful authorization enforcement. Use an intentionally invalid-route negative control to demonstrate that its 404 cannot be mistaken for the approved object's denial. Do not use the invalid-route body as proof that an actual protected object was safely denied.

| Outcome | Deterministic boundary / example |
|---|---|
| PASS | All policy/grant/auth/fixture/route prerequisites valid, every required observation complete, and the exact approved ALLOW or DENY assertions hold. 403/404 additionally requires approved profile plus no protected body/header/state disclosure. |
| VIOLATION | Valid prerequisites and reliable complete evidence for the violated assertion establish a contradiction of an approved rule, such as cross-tenant protected data or protected state modification. A model hypothesis or status mismatch without valid controls is insufficient. |
| ERROR | Known setup, authentication, route, transport, timeout, decoding/observation-component fault, resource cap or infrastructure failure prevents a valid test. Record the technical reason; never PASS or infer a verified violation from it. |
| INCONCLUSIVE | Preconditions were valid and execution/observation functioned, but available evidence cannot decide a required assertion, e.g. an otherwise bounded response is opaque or the supported observation model cannot determine a protected state effect. Missing evidence is never proof of non-disclosure. |

Known observation-port failure is ERROR; a functioning but insufficient observation model is INCONCLUSIVE. If neither cause can be established, use INCONCLUSIVE with the uncertainty recorded and no compliance claim. A partially observed response cannot PASS; any separately reliable violation evidence may be retained only with verified prerequisites and its exact observation limits. A later cleanup/infrastructure failure makes the job non-success and blocks baseline reuse, but does not rewrite earlier reliably observed assertions into a different historical verdict. Never turn timeout, missing evidence or failed controls into PASS.

## 8. Examples and future verification matrix

The following are **expected design examples, not tests run or approved contracts**. All authorization cases assume a separately approved policy/profile, fixture and execution grant plus genuine A/B preflight unless the row deliberately invalidates one. “Zero request” refers to the forbidden destination; preflight/cleanup requests need their own explicit capabilities. No arbitrary URL is exercised in this task.

| Case ID | Input / observation | Required outcome or check | Trace |
|---|---|---|---|
| FX-01 | A reads existing order A, 200 with intended authorized fields; baseline intact | ALLOW PASS; independent B owner control also succeeds | AC-005; FR-TST-002 |
| FX-02 | A reads existing order B, authentic A; patched target returns generic 403, no protected headers/body/state change | DENY PASS under accepted profile | AC-005; FR-TST-005 |
| FX-03 | Same cross-tenant read, generic 404; B owner control proves order B exists; full no-disclosure/state observation | DENY PASS under accepted 403/404 profile | AC-016; OQ-06 |
| FX-04 | Same read against deliberately vulnerable variant returns B protected data | Reliable approved DENY contradiction -> VIOLATION, sanitized evidence; preserve failed run | AC-004 |
| FX-05 | Missing/expired token, 401 or 404 | ERROR; insufficient validity evidence -> INCONCLUSIVE, no PASS/verified violation | AC-006 |
| FX-06 | A/B tokens equal, or different tokens both identify A, or shared cookie jar contaminates requests | Preflight ERROR; no authorization assertion | FR-TST-002 |
| FX-07 | Missing order B, failed B owner control or incomplete tenant/share facts | ERROR/INCONCLUSIVE; 404 cannot PASS as denial | AC-006; OQ-06 |
| FX-08 | Approved ALLOW, valid fixture, target returns 500 | ERROR, never PASS | AC-017 |
| FX-09 | 403/404 contains protected field/marker/header or changes protected state | VIOLATION with reliable valid prerequisites; not status-only PASS | AC-016; FR-TST-005 |
| FX-10 | 404 opaque/truncated payload or unavailable after-state observation | INCONCLUSIVE/ERROR; no non-disclosure claim | FR-TST-005/006 |
| FX-11 | Unapproved policy/profile/grant or forged imported approval field | Reject before target requests; no run authority from JSON | TB-08; AC-002/007 |
| FX-12 | External origin, ungranted private/metadata IP, wrong port, path escape, Unix scheme or ambient proxy | BLOCKED_SCOPE before forbidden request/credential transmission | AC-007; TH-04 |
| FX-13 | Redirect to external destination; also repeat with in-scope Location | No second request in either case; no PASS, sanitized blocked/unsupported reason | AC-015; TH-04; SEC-T006 |
| FX-14 | Authorized hostname answers approved IP then forbidden IP on reconnect, mixed A/AAAA, or peer differs | Reject before bytes to forbidden peer; no credential leak or permissive re-resolution | TH-04; SEC-T005; extends planned DNS coverage |
| FX-15 | Request/rate/concurrency/time/response/process/disk cap exceeded | Bound resources, halt, non-PASS affected cases; reserved cleanup still attempted | FR-TST-007; TH-13 |
| FX-16 | Cancellation, partial setup, expiry or actor revocation | Stop new execution, revoke/terminate/remove owned state through cleanup grant; no implicit extension | FR-TST-002/007 |
| FX-17 | Cleanup fails, child remains, workspace escapes or fixture not restored | FAILED_INFRA; quarantine and operator recovery; no clean baseline or reuse | TH-06/13/17 |
| FX-18 | Runner asks for host mount/socket/device, elevated identity or unrelated network | Reject containment before execution; no unrestricted fallback | TH-06; SEC-T021 |
| FX-19 | Repeated seed/run with same logical versions and valid cleanup | Equivalent facts/expected decisions; preserve both sanitized runs and compatibility provenance | NFR-REL-001 |
| FX-20 | Target body has agent instructions or fixture credential appears in errors | Treat as data; no instruction execution; withhold uncertain sanitization, no raw export | TH-20/07; AC-011 |
| FX-21 | Invalid route or wrong method returns 404; independent owner request on requested route fails | Adapter/precondition ERROR, never a DENY PASS | OQ-06; AC-006/016 |
| FX-22 | Prior case's actor session, resource or mutable cache is reused; cleanup touches another run | Reject cross-case/run binding; quarantine contamination, no assertion/reuse | FR-TST-002; TH-17 |
| FX-23 | Controlled timeout or failed observation port versus functioning but insufficient observation model | Known technical failure -> ERROR; insufficient evidence -> INCONCLUSIVE; neither outcome may PASS | AC-006/017; FR-TST-006 |

Later M1-04/06 must implement authentic demo and fixture tests; M1-07 must test pre-request destination enforcement with controlled transports/resolvers and then a separately authorized isolated integration environment; M1-08 must exercise vulnerable/patched and false-PASS cases; M1-09/12 must verify redaction, cleanup and offline repeatability. A mock cannot prove real OS/network isolation. Architecture §1.2's demo prototype/error/redirect evidence is **NOT RUN / absent** and required before freezing implementation, not fabricated by this matrix. Runtime tests and approvals remain separate tasks/gates.

## 9. Alternatives, trade-offs and reversible choices

| Alternative | Reason to defer/reject under this proposal |
|---|---|
| In-process target with mocked authentication only | Useful future pure unit tests, but insufficient proof of independent real sessions or network enforcement; cannot replace integration evidence. |
| One admin token plus actor headers | Conflates fixture control with tested identity and can hide IDOR; reject for behavioral authorization evidence. |
| Arbitrary supplied URL, broad private-IP allowance or follow redirects by default | Expands scope and credentials exposure; reject under initial explicit local binding. |
| Generic YAML/shell setup scripts or dynamic adapter import | Executable untrusted data contradicts restricted DSL; reject. |
| Status-only 403/404 assertion | Can conceal leaked objects, broken authentication or nonexistent resources; reject. |
| Current-user process fallback when container unavailable | Host credentials/files/network exposure; stop until a separately reviewed lower-privilege capability profile exists. |

Reversible internal decisions: module/class names behind the typed port, fixture storage layout inside the approved workspace, opaque handle representation, test-helper organization and selection among mechanisms with the **same accepted** isolation and behavior guarantees. Changes still need focused compatibility/negative checks and provenance versions; “reversible” does not authorize networking or weaker protection.

Security sign-off is required before accepting/changing: authentication and fixture-control authority; relation completeness semantics; 401/403/404/non-disclosure profiles; target origin/IP/path/method grants; redirect/retry/DNS/proxy/TLS behavior; containment/fallback, mounted paths, credentials, resource ceilings or cleanup authority; evidence observation/redaction and retention. Raising scope/limits or enabling an additional channel requires renewed approval. Review ADR-0001/0003 where semantics/receipts intersect. No new provider egress or P1 hosted/private-runner design is accepted here.

Rollback: keep runner execution disabled until gates and actual tests pass. If an accepted implementation later fails containment/scope/cleanup, disable that profile, revoke relevant grants, quarantine run-owned fixtures and recover through approved operator procedures. Retain old contract/profile/adapter versions, failed observations and evidence; changing bindings creates a new version and may make runs NOT_COMPARABLE. Never weaken an approved rule, delete evidence or quietly switch mechanisms to obtain PASS. There is no deployed schema or migration to execute today.

## 10. Open decisions, evidence and review request

All recommendations below remain PROPOSED. Tests are requirements for later authorized implementation, **NOT RUN** in this docs-only review. Names refer to §8 cases; existing SECURITY test IDs retain their scope.

| Decision area | Proposed choice | Alternatives | Security implications | Recommended default | Open risks | Required verification tests |
|---|---|---|---|---|---|---|
| Dependencies / human authority | Preserve TB-08 and M0-02 IN_REVIEW; developer reviews exact revisions | Further changes or defer; no AI approval alternative | Proposal cannot grant privileged execution or policy authority | Keep all unaccepted choices gated | M0-02 sign-off absent; ADR-0001 design accepted, ADR-0003 full acceptance pending | FX-11, AP-05/08/15 in ADR-0003; authentic human review required |
| Deterministic fixture/case isolation | Fixed logical seed; unique run/case namespace, fresh clients/sessions and checked baseline | Independent database/container per case; immutable snapshot plus disposable copy | Prevents cross-test state/session contamination; adds setup cost | Serial, isolated per-case mutable state; never reuse dirty state | Namespace/caches/cleanup ownership not implemented | FX-01/06/19/22; repeated seed; attempt cross-run handle/resource/cleanup use; concurrent isolation before enabling parallelism |
| OQ-03 authentication | Target-issued opaque A/B sessions, independent identity and owner controls | Reviewed session-cookie adapter; signed-token adapter with genuine identity checks | Different strings alone do not prove distinct users; setup/control identity cannot be tested actor | Separate credentials/clients; invalid auth stops assertions | Auth endpoints, expiry/revocation/probe capabilities unset | FX-01/05/06/07; swapped token/cookie; wrong/revoked identity -> ERROR |
| OQ-06 403/404 semantics / routing | Approved profile plus known existing object/valid route, no protected body/header/state disclosure | Separately reviewed 401 or richer profiles; never status-only denial | Prevents false PASS for invalid routes, missing fixture or leaked objects | Only 403/404 with successful paired controls and complete observations | Exact fields/state model/profile digest unaccepted; side channels outside profile | FX-02/03/04/07/09/10/21; owner ALLOW, valid denied object, vulnerable disclosure, invalid-route 404 |
| Outcome classification | Pure deterministic assertions with explicit preconditions and reason codes | Additional observation model/version after review; no LLM verdict | Distinguishes reliable policy contradiction from infrastructure failure and uncertainty | §7.1; known fault ERROR, insufficient evidence INCONCLUSIVE, never infer PASS | Error taxonomy/observation completeness not implemented | FX-08/10/15/17/23; timeout, failed probe and functioning insufficient probe; no status-only PASS |
| Target scope / default-deny egress | Exact origin/IP/port/method/route grants, separate fixture-control capability | Explicit isolated HTTPS origin later; no wildcard/private-network blanket | Stops SSRF/pivot and accidental credential transmission | Initial reviewed IP-literal local profile, ambient proxy/DNS/provider egress disabled | Namespace process identity, TLS/normalization/peer API verification missing | FX-11/12/14; SEC-T005; wrong scheme/port/encoded path/peer/proxy; zero forbidden requests/credentials |
| Redirect / DNS / credentials | Zero redirects/retries; any later DNS resolves/pins approved addresses and checks peer before bytes | Explicit per-hop scope/credential-stripping grant with finite budgets after review | Prevents redirect/rebinding races; restricts legitimate redirect-dependent targets | No following redirects; no DNS in initial literal profile | Transport bypass/connection reuse, resolver path and IPv6/IDNA handling unverified | FX-13/14; SEC-T006; out/in-scope redirect, mixed/changing DNS and peer mismatch; credential canary absent |
| Runner containment / commands | Non-root disposable isolation, read-only root, bounded workspace, no host mounts/socket, allowlisted typed operations | Separately reviewed dedicated-account process with capability evidence | A container name is insufficient; arbitrary AI commands and same-user fallback expose host | Disable unsupported containment; reject dynamic shell/Python/adapter code | Supported OS/runtime, namespace/syscall/network policies unset | FX-18/20; SEC-T007/021; shell/template attempt, traversal/symlink, host socket/mount/secret and undeclared network |
| Budgets / cancellation | All §6 limits finite, accounting across clients/phases; cleanup reservation | Tighter measured machine profile; increases need renewed approval | Limits DoS/orphans but overhead can interrupt legitimate tests | Candidate ceilings only, no automatic expansion; halt with non-PASS reason | Actual enforcement and cleanup-controller CPU/memory/clock overhead unset | FX-15/16/23; each cap, streaming/compression, concurrency/rate/time, cancellation/expiry and cleanup reservation |
| Teardown / orphan recovery | Idempotent owned-state removal, credential revocation, child termination; quarantine on failure | Disposable whole-environment destruction where ownership verified | Partial setup/cancel must not leave reusable state or delete another run | Independent narrow cleanup grant and bounded reserve; no dirty reuse | Recovery authority/grace period/expiry and OS termination unsettled | FX-16/17/19/22; partial setup, crash, cleanup failure, residue detection and repeated teardown |
| Evidence / approval bindings | Exact accepted policy/profile/scope and immutable sanitized lineage | Future protected attestation/checkpoints after separate review | Hash/path alone is not authenticity; raw evidence can leak credentials | Fail closed on untrusted receipt or uncertain sanitization | ADR-0001 design accepted; ADR-0003 broader review pending, storage/redaction/integrity implementation absent | FX-09/20; AC-011, SEC-T003/004/011; forged approval, changed profile and planted secret checks |

**Concise review summary:** Confirmed requirements remain deterministic synthetic fixtures, independent actors, complete controls and mandatory human authority. Historical v0.2 added explicit cross-case ownership/cache/session boundaries, an invalid-route 404 control, deterministic ERROR versus INCONCLUSIVE classification, and the proposed-choice/alternatives/security/default/risk/test matrix. Current v0.3 reconciles accepted DSL/current code references and preserves those cases. Transport, containment, observation, numeric enforcement and cleanup mechanisms are still unverified open risks. No runtime test, ADR acceptance, M0-02 sign-off or execution/provider authorization is recorded.

**Current review request:** Developer, review this exact v0.3 revision and the remaining §10 fixture/transport/containment/budget/cleanup choices; state accept, request changes or defer with scope and conditions. [todo.md](../../todo.md) EV-0065 and the foundation package record its SHA-256; EV-0005/0007 preserve v0.1/v0.2 history. Accepted unchanged DSL/audit directions are not requested again. Until an authentic decision is received, this ADR remains PROPOSED and M0-04 remains IN_REVIEW; M0-02 is still IN_REVIEW. A future acceptance must record reviewer identity, exact digest/version, decision/date, accepted choices and conditions; none is fabricated here.

This document supplies drafting coverage, not runtime acceptance or execution authorization. Any accepted design still requires the relevant implementation tests, target grants and sensitive-operation approvals. Current reconciliation is within the owner-requested P0 foundation package; historical v0.2 feedback occurred during M0-05. No next task starts automatically.
