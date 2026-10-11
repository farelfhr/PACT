# ADR-0001 — Restricted contract and authorization policy DSL

> **Status: ACCEPTED — specified DSL design choices only (2026-10-10)**
> **Draft version:** 0.1, 2026-10-10
> **Author:** Codex, task M0-03
> **Decision owner / reviewer:** Repository developer; specified choices accepted 2026-10-10
> **Trace:** OQ-02; FR-AUT-001/002; supporting FR-INT-002/003, FR-CON-001/002/003, FR-TST-004/005/006, NFR-SEC-001/003/004; AC-001/002/010/016/017

## Context and scope

[PRD §§6.4/7](../../PRD.MD) requires typed principals, roles, tenants, resources, actions and relations; explicit ALLOW/DENY; declarative conditions; immutable approved versions; no executable expressions. The PRD's §7.3 sample is illustrative, including its `APPROVED` field and dotted strings. It is not a frozen schema or approval proof. [Architecture M0-03](../ARCHITECTURE.md) requires a draft and valid/invalid examples; M0-01 is DONE with EV-0001. M0-02 remains IN_REVIEW after the developer requested changes, not sign-off.

At intake there were twelve Markdown files, no source packages, tests, build configuration, schemas or ADRs. Git is initialized on main; pre-existing SECURITY.md/todo.md changes are preserved. No accepted ADR was found. This document proposes policy data, not an executor, public API or runtime approval mechanism. Example validation is a temporary local experiment, not implementation of M1-01/02/05.

**Every decision below is proposed.** “Accepted example” means acceptable under this draft grammar, never a human-approved Security Contract. No import, digest, `source_ref`, role label or task status grants execution authority.

## Proposed decision

### 1. Representation and bounded decoding

Canonical interchange is UTF-8 JSON with the exact `schema_version` string `1.0` and `canonicalization` identifier `pact-json-1`. These names describe the proposed first version; no deployed schema is claimed.

For the initial bounded YAML surface, accept only the **JSON-compatible flow representation**: the same JSON text can be authored as YAML, but is decoded by the strict JSON path. Block-style YAML, implicit scalar coercion, comments, anchors/aliases, merge keys, explicit/custom tags, multiple documents and YAML object constructors are rejected. This trades YAML ergonomics for a single auditable decoder without an unapproved dependency. Full safe block-YAML support needs an owner choice and tooling/dependency review in M0-06; it must produce exactly the same typed tree and canonical JSON before review. It is not silently enabled by a file extension.

Proposed input bounds: 64 KiB UTF-8, nesting depth 16, 64 rules, eight predicates per rule, 64 declarations per category, 32 source references, 96 characters per identifier, version 1 through 2,147,483,647. Reject duplicate object keys at every depth, invalid JSON, nonfinite numbers, floats, booleans used as integers, nulls, unknown versions and excess input before semantic evaluation. No comments/trailing commas, remote schema resolution, file includes or import hooks. Limits are policy-parser bounds, not target execution budgets; ADR-0002 owns the latter.

### 2. Closed typed shape

All fields below are required; objects reject every additional field. Arrays are nonempty and obey the bounds above. Identifiers use ASCII `[A-Za-z][A-Za-z0-9._-]{0,95}`; declarations and rule IDs are unique within their category. No arbitrary field path, URL, expression, template, credential or prose condition is an identifier.

| Object | Exact fields / types |
|---|---|
| Contract policy content | `schema_version: "1.0"`, `canonicalization: "pact-json-1"`, `contract_id: Identifier`, `project_ref: Identifier`, `version: bounded integer`, `source_refs: Identifier[]`, `roles: Identifier[]`, `resource_types: Identifier[]`, `actions: ["read"]`, `combining: "reject_conflicts"`, `on_unmatched: "NEEDS_REVIEW"`, `rules: Rule[]` |
| Rule | `rule_id: Identifier`, `actor: {role: declared RoleId}`, `resource: {type: declared ResourceTypeId}`, `action: declared Action`, `when: Predicate[]`, `expect: "ALLOW" or "DENY"`, `assertion_profile: allowed ProfileId` |
| Predicate | `relation: closed RelationId`, `subject: exact allowed symbol`, `object: exact allowed symbol`; signatures below |

P0's first executable profile is an object **read**. `actions` therefore contains exactly `read` once; writes, lifecycle/time rules, recursive predicates and arbitrary attributes are not included in this draft. This is a bounded increment, not removal of FR-AUT-001: other actions need typed action/profile contracts and the applicable fixture/runner review before support is added. Unsupported actions return an explicit error, never a degraded read test.

Principals, tenant identities, roles, resources, owners and sharing/membership facts are supplied by a trusted synthetic fixture snapshot. This policy declares **logical types and selectors**, not synthetic passwords or real user identities. `actor.role` matches a declared target-app role; it does not authenticate a PACT reviewer. Target tenant IDs and PACT project IDs are separate types, never interchangeable.

### 3. Relation signatures and meaning

| Relation | Only valid `(subject, object)` | Deterministic meaning under complete trusted fixture facts |
|---|---|---|
| `owns` | `(actor, resource)` | The actor principal ID equals the resource's declared owner principal ID. |
| `member_of` | `(actor, resource.tenant)` | The actor has an explicit membership edge to the resource tenant. |
| `shared_with` | `(resource, actor)` | The resource has an explicit share edge to the actor. Ownership or same-tenant membership does not create this edge. |
| `same_tenant` | `(actor.tenant, resource.tenant)` | The actor's verified primary tenant ID equals the resource tenant ID. Membership in several tenants is not primary-tenant equality. |
| `different_tenant` | `(actor.tenant, resource.tenant)` | Both verified tenant IDs exist and differ. A missing tenant is not inequality. |

The dotted symbols are **enumerated binding tokens**, not paths to evaluate. They are resolved by a fixed typed fixture interface; no `getattr`, expression interpreter or string interpolation is authorized. Wrong operand kinds, undeclared selectors and unknown predicates reject validation.

`when` is a bounded conjunction. Every predicate must be true to match. There is no implicit negation, arbitrary OR, callback, SQL, Python, shell, regex expression, Jinja or `${...}` evaluation. Disjunction may be expressed as separate explicit rules, subject to conflict handling. All values are data. A string that happens to look like executable code is never executed; it is rejected wherever typed policy fields cannot accept it.

Known absence of a share/membership edge in a **complete** fixture means false. Missing/incomplete ownership, membership, tenant, role, resource existence or authentication facts yield a precondition error, not false, DENY, ALLOW or PASS. Validate fixture completeness before evaluating any rule, including rules whose role selector would otherwise fail.

### 4. Matching, conflicts and missing policy

1. Validate the full document and declared references; validate all required fixture facts and action/resource bindings.
2. Select rules matching the actor role, resource type and requested action. Evaluate each typed conjunction using the same immutable fixture snapshot.
3. If all matching rules agree on the decision **and profile**, return that expected decision and every matching rule ID in sorted order. Rule-array order never grants priority.
4. If matching rules disagree on decision or profile, return `NEEDS_REVIEW` / `CONFLICTING_RULES`; do not run a scenario or choose an order-dependent winner.
5. If no rule matches, return `NEEDS_REVIEW` / `UNSPECIFIED_POLICY`; do not invent expected ALLOW or expected DENY. Required coverage has to be filled by a human-reviewed rule.

`NEEDS_REVIEW` describes the draft/compiler outcome. It is not an observed scenario verdict. **Execution is default-denied** until policy/fixture/scope prerequisites and trusted approval are valid; that safety guard does not turn unspecified business policy into an expected DENY. No implicit administrator bypass or `deny overrides` policy is proposed. If the owner wants priority/deny-overrides, it needs explicit reviewed semantics and paired conflict tests.

### 5. Decisions and assertion profiles

Profile IDs are immutable versioned references, with their exact assertion definitions included in the trusted approval binding designed in ADR-0003. Renaming an assertion while keeping its ID is prohibited. Profile/digest storage and execution are not implemented here.

| Allowed profile / expected decision | Required observed behavior; valid preconditions always required |
|---|---|
| `object-read-allow-v1` / ALLOW | HTTP 200, intended resource identity and required authorized fields observed through the declared fixture/assertion adapter; intended functionality works. Empty/wrong-resource bodies cannot silently PASS. |
| `object-read-deny-403-404-v1` / DENY | Approved 403 or 404 response, no protected-resource disclosure and no protected state modification. A status alone is insufficient. |
| `object-read-deny-401-403-404-v1` / DENY | Same assertions, also permits 401 **after actor authentication/setup validity has been established**. Missing/expired fixture credentials remain ERROR/INCONCLUSIVE, not a successful denial. |

Reject an ALLOW rule using a DENY profile or vice versa. A DENY returning protected data can be VIOLATION only with valid prerequisites and reliable observation. HTTP 500/timeout on ALLOW or DENY cannot be PASS; distinguish ERROR and INCONCLUSIVE using the future executor's error taxonomy. If absence of disclosure/state modification cannot be observed, report INCONCLUSIVE, not PASS. Target capability, field bindings and exact 401/404 acceptance need ADR-0002 review (OQ-03/OQ-06); no approved denial profile is created by this proposal.

### 6. Identity, approval and execution separation

The policy-content shape rejects `status`, `approved`, `review`, `reviewer`, receipts, signatures, target URLs, target grants, credentials and runner settings. Import yields candidate data only. Human review, draft state, timestamps, source text/questions/provenance and attestations are separate registry records, not writable approval fields in policy JSON. `source_refs` link separately stored provenance; they cannot authorize or define missing semantics.

Approval must bind exact canonical policy bytes/digest, schema/profile definitions, contract version, human identity and project. That record is validated independently of imports by the future ADR-0003 service. The target grant/fixture/network budget remains a separate authority under ADR-0002. Even a valid contract digest is not a signature, review receipt or permission to execute. M0-02's mandatory TB-08 remains in force; AI cannot self-approve any sensitive action.

The proposed shape intentionally differs from illustrative PRD/Architecture samples (`when` string paths, `status`, `target_binding`). This is a reviewable refinement of nonfinal samples, not a silent change to normative PRD requirements. No compatibility migration from a deployed API is claimed.

### 7. Canonicalization, immutable versions and schema evolution

After strict decoding and complete structural validation, serialize the typed policy tree with lexicographically sorted ASCII object keys, compact separators `,` and `:`, no whitespace, UTF-8 without BOM, no trailing newline, ordinary JSON string escaping and decimal integers. All strings/keys in this version are ASCII; non-ASCII is rejected, avoiding an unstated Unicode normalization choice. Preserve array order exactly. SHA-256 of those bytes is the proposed `pact-json-1` content digest.

JSON/YAML-format input and object-key order do not affect the digest. Rule order does not affect policy evaluation, but **changing any array order changes the reviewed bytes/digest**, intentionally requiring a fresh version/review; canonicalization does not silently rewrite a human's ordered document. Whitespace outside JSON values is irrelevant. Unknown properties are rejected rather than dropped before hashing. Hash/profile/version/project comparison must precede execution and drift analysis.

`contract_id` identifies a logical policy; integer `version` identifies its content revision; `schema_version` identifies grammar/semantics; profile version identifies assertion semantics; `canonicalization` identifies hashing rules. All four version dimensions are distinct. Approved content remains immutable: any change creates a new draft version; old policy bytes, receipts and failed evidence remain accessible.

Readers support an explicit exact-version allowlist. Unknown or newer major/minor schemas fail `UNSUPPORTED_SCHEMA`; no best-effort fallback. Adding predicates, fields, profile behavior or action support requires a new explicitly supported schema/profile version and conformance fixtures. Breaking meaning or canonicalization requires a new version and ADR review. Even backward-compatible additions need explicit decoder support. Migration is a reviewed transformation into a new draft, not in-place mutation: retain old bytes/digest, show semantic diff, revalidate, request fresh human approval, preserve old execution/read paths where supported. Unsupported old versions fail visibly with migration instructions. No migrations are run in M0-03.

## Examples and acceptance/rejection evidence

[Valid JSON example](examples/0001-valid-contract.json) contains seller/order same-tenant ALLOW and different-tenant DENY with an explicit safe-404 profile. It is **not approved or runnable**. [Case data](examples/0001-cases.json) supplies another accepted sharing-rule example, typed relation examples, rejected field/predicate/import examples and expected local matching outcomes. The case format is local documentation data, not a public patch/scenario API.

The valid JSON file is also the accepted **JSON-compatible YAML** example: the exact same text through the bounded YAML entry surface normalizes to the same JSON bytes. This rejected block-YAML example is syntactically outside that proposed subset (even if a general YAML library could load it):

```yaml
schema_version: "1.0"
when: !!python/object/apply:os.system ["synthetic-command-do-not-execute"]
```

Representative valid typed condition (only as part of a full valid rule/document):

```json
{"relation":"shared_with","subject":"resource","object":"actor"}
```

Representative rejected condition:

```json
{"relation":"owns","subject":"__import__('os').system('synthetic-command-do-not-execute')","object":"resource"}
```

The rejection is `INVALID_RELATION_BINDING`, not execution followed by redaction. Likewise a JSON `when` string containing `actor.tenant == resource.tenant`, `${...}`, shell or template text is not a typed predicate array. JSON decoding may accept the string syntactically; **the policy validation stage rejects it before evaluation**. A bare JSON parser is insufficient to satisfy this security boundary.

| Check group | Required local success / failure evidence |
|---|---|
| Representation / grammar | Valid JSON and JSON-compatible YAML; reordered object keys normalize identically; duplicate keys, nonfinite/float/boolean versions, unknown schema/field, missing field and oversized input rejected. |
| Typed relations | owns, member_of, shared_with, same/different tenant signatures accepted; undeclared role/resource/action, wrong operand type, unknown relation and executable strings rejected. |
| Policy outcomes | Own tenant/order ALLOW; other tenant DENY; explicitly shared document ALLOW; agreeing rules preserve all rule IDs; rule order irrelevant; conflict/unmatched yield NEEDS_REVIEW; missing facts yield precondition error. |
| Approval / profiles | Forged status/reviewer/target/credentials rejected; decision/profile mismatch rejected; profiles explicitly versioned; 404 and ALLOW-500 semantics documented. |
| Repository | Only the allowed document/example paths and tracker changed; prior docs/history preserved; exact statuses/counts and review digests checked; no code/dependency/target side effects. |

Actual command/results, temporary checker limitations and digests are recorded as EV-0003 in [todo.md](../../todo.md). The checker validates these proposed examples and matching semantics using local standard-library code outside the repository. It is not the production parser, JSON Schema implementation, authenticated approval system, fixture adapter, HTTP assertion engine or proof that runtime rejection exists. Runtime/HTTP/security tests are NOT RUN; source/tests/toolchain are absent. Full YAML loading is NOT RUN and intentionally excluded.

## Alternatives and trade-offs

| Alternative | Reason for this proposal / remaining trade-off |
|---|---|
| Python, shell, templates or arbitrary expression language | Reject: conflicts with PRD §7 and NFR-SEC-004; creates code execution and unclear authority. |
| General policy engine / complete ABAC graph language | Defer: more semantics, dependencies and integration than needed for the first bounded read cases. Revisit after a specific unsupported business need. |
| First-match, numeric priority or deny-overrides | Reject as initial proposal: hides contradictory human intent. Explicit conflict review costs convenience but avoids inferred policy. |
| Full block-YAML safe loader | Potential ergonomics; parser dependencies/coercion/aliases require separate audited limits. Proposed JSON-compatible subset is deliberately narrow; owner may request a different design. |
| Sort every array / adopt a broader canonicalization standard | Could reduce hash changes on semantic reorder, but changes reviewed bytes and increases normalization assumptions. This draft preserves array order; a future choice needs compatibility review. |

## Security, privacy and dependency effects

TH-01/02/03/05/08/11/15 and TB-01/03/04/08 are relevant. Typed parsing prevents this proposed data format from conferring arbitrary execution/approval authority; actual enforcement remains absent. No target URLs, credentials, raw source, personal records or external provider calls are needed by examples. Local hashes are integrity references only. Bounds protect parser workload but do not prove runner containment. No packages, services or project tooling are installed/selected; Python 3.14.4 observed locally is only an available scratch-check interpreter, not approval of the proposed project Python matrix.

## Pending decisions, handoff and rollback

Owner acceptance is requested for: **(a)** typed relation signatures/complete fixture facts; **(b)** explicit conflict/unmatched outcomes; **(c)** read-only initial action/profile vocabulary; **(d)** JSON-compatible YAML subset and parser limits; **(e)** canonical byte/version/evolution rules. No decision is Accepted until an explicit owner response identifies this exact ADR/example revision; digests are in EV-0003. Approval of ADR-0001 does not sign off M0-02 or authorize a real contract, runner, target or provider.

ADR-0002 must settle fixture completeness, resource/field bindings, 401/404 denial observation, transport and runner isolation. ADR-0003 must settle genuine reviewer identity, profile/hash binding, immutable receipts and replay behavior. ADR-0004/M0-06 must settle package matrix and any full-YAML dependency. Those ADR files are not created in this bounded session; the owner explicitly requested separate task prompts. Hosted browser/runner/identity decisions remain ADR-0007/P1. M0-02 reviewer clarification summary is in SECURITY §18.4.

Before normative implementation, require owner-accepted applicable ADRs and the M0-02 boundary review gate. Future M1-01/02/05 must implement and test the real parser/normalizer against these reviewed cases, including negative inputs and error semantics. M0-08 will formalize coverage; M0-09 will align data/public interfaces. This document does not start those tasks.

Rollback for this draft is to revise/reject the proposal while retaining journal/evidence. No deployed state/schema exists to migrate. After acceptance, supersede via a new ADR/schema and reviewed migrations; never erase historical policy/evidence to hide a failure.

## Historical draft review record (before owner decision)

- **Decision:** PROPOSED, awaiting developer review.
- **Approval identity/date/evidence:** None.
- **M0-03 status:** IN_REVIEW; the temporary example checks do not prove a production parser exists.
- **Change scope:** This ADR, its two example-data files, requested M0-02 document clarifications and tracker only; no other ADR or implementation task started.

## Owner decision — 2026-10-10

The developer/repository owner directly answered **“Accept the specified ADR-0001 design choices”** to the M1-01 prerequisite review request. That request explicitly identified v0.1 and EV-0003, covering typed relation signatures, conflict/unmatched outcomes, action/denial profiles, JSON-compatible YAML subset/limits and canonicalization/versioning rules. Before recording, the ADR and both examples matched EV-0003: reviewed ADR `FA7269848DC9AD749CBB990B420AB7089D98F715E227C58F5853F0C217735E3A`; valid example `F80D9CFCC2F73EF747C464D443F7BBFBEDEF5F5112956C8BE79534326941274B`; cases `C891C856D414A4C930A2718704F8DE2E4505C11F5D8841F93185563830082808`. EV-0013 retains the exact pre-decision ADR bytes and acceptance provenance.

The specified design choices are now accepted; proposal language above records the original reviewed draft. No design text or example content was changed by recording this decision. This is **not** a Security Contract approval, M0-02 sign-off, target/scope authorization, acceptance of other ADRs, tooling acquisition permission or provider-egress grant. Pure M1-01 types may encode the accepted vocabulary; privileged approval, runner and transport implementations remain gated. The new document hash includes this decision record and is not the hash of the original reviewed bytes.

## Owner normalization clarification — M1-02, 2026-10-10

The developer directly answered **“Reject possible conflicts during normalization”** after review of a concrete boundary: V-02's ownership predicate is structurally valid, but can coexist with different-tenant DENY; M1-01 also permits explicit multiple actor roles. Structural validity therefore does not certify an unambiguous policy. Preserve the original example/case bytes and structural validation expectations; semantic normalization must reject any possible matching disagreement in decision or profile with NEEDS_REVIEW, rather than assume role exclusivity or owner/tenant equivalence. The reviewed initial vocabulary has only positive conjunctions; same_tenant and different_tenant are complementary, while owns/member_of/shared_with are explicit independent facts. Different resource types are mutually exclusive for one resource; different role selectors alone do not establish disjointness. Unsatisfiable same/different-tenant conjunctions require review as unusable rules. This static check supplies no trusted fixture, actual access decision or observed verdict.

The developer also explicitly authorized **“Complete JSON Schema/stdlib scope; defer Pydantic”** for M1-02 after isolated interpreter metadata checks found Pydantic unavailable. This is a bounded deliverable choice, not acceptance of ADR-0004, dependency acquisition, runtime approvals or egress. Canonical byte/hash/array-order rules above remain unchanged. EV-0014 retains the original ADR decision record and direct clarification provenance.
