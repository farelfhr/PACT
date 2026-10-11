# PACT Security — Initial data model and identity boundaries

> **Status:** PROVISIONAL / IN_REVIEW — scoped conventions accepted with conditions; full schema/content review pending
> **Version / date:** 0.3 / 2026-10-11
> **Task / trace:** M0-09; PRD §§7, 9, 13; FR-CON-001/002/003, FR-TST-002/006/007, FR-EVD-001/002
> **Reviewer:** Developer; scoped design-direction acceptance recorded in todo.md EV-0011, not final content approval
> **Implementation:** Candidate domain/parser/fake-provider packages exist; these registry/wire/storage proposals have no tables, migrations, public endpoints or trusted approval implementation.

## 1. Authority and canonical location

This is the canonical reference location for proposed PACT domain and wire structures, accepted as a **design direction** by the developer on 2026-10-10. [PRD.MD](../PRD.MD) controls requirements. [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY.md](SECURITY.md), [workflow.md](../workflow.md) and [todo.md](../todo.md) supply boundaries and actual progress. [API_SPEC.md](API_SPEC.md) uses the identity vocabulary below. This scoped decision does not approve every schema field or replace accepted ADR requirements.

The existing [schema.md](schema.md) v1.0.0 remains historical storage/RLS/migration design input. Its entire original content is preserved after an added historical-reference notice. Old downloadable/identical-copy/canonical wording in that retained text is historical and no longer controls document ownership. DATA_MODEL.md owns the current domain/wire proposal; schema.md supplies storage design context and cannot override it, the PRD or genuinely accepted ADRs. This reconciliation is not an identical delivery copy. No rename, deletion, SQL execution or migration occurs. The owner has settled this document relationship; ISS-0001 closure requires the actual notice/path/preservation checks recorded in EV-0011, not approval of all model semantics.

M0-03/ADR-0001 specified DSL choices are DONE/ACCEPTED; M0-05 and ADR-0003 remain IN_REVIEW/PROPOSED. ADR-0002/0004 are PROPOSED. Existing accepted canonical reference, typed opaque IDs and one-job/one-run directions retain their conditions. On 2026-10-11 the developer separately selected dedicated Audit Authority/append-only history/independently signed checkpoint storage direction (EV-0034), not all record fields/protocols or full document approval. This does not grant contracts, execution, egress, privileges, deployment or M0-02/full-ADR sign-off. Remaining wire/backend/identity/security mechanisms need actual accepted decisions and tests.

## 2. Reconciliation of the existing draft

| Existing source / discrepancy | Proposed reconciliation / approval gate |
|---|---|
| schema.md §§0–1: canonical-copy wording and SQLAlchemy/Alembic initial stack | Historical notice precedes preserved original bytes; accepted document relationship above governs. ADR-0004 instead proposes stdlib SQLite ports initially, ORM/migrations deferred; both stack proposals are unaccepted. Do not install an ORM or create migrations from these examples. |
| PRD §7.3: illustrative policy contains status/review/target binding | Separate restricted policy content from trusted registry/review/execution records. ADR-0001's closed policy does not accept those extra fields. PRD's own approval invariant forbids trusting imported APPROVED. |
| contract_versions.id versus contract_key; policy contract_id and project_ref | contract_id is the project-local logical policy key; contract_version_id is the opaque immutable registry row identity. contract_key is a proposed storage mapping for contract_id, not a second policy key. project_ref is an untrusted alias resolved to an authorized project_id. |
| schema.md §4.3: CONVERTED draft storage marker and inline approved_by | Use PRD lifecycle states in public projections; CONVERTED, if ever needed internally, is not a new public approval state. Reviewer/time originate from the protected decision event; copied columns are checked projections, not authority. |
| approval_events versus review request/receipt | review_id identifies a pending request; review_event_id identifies one protected decision event. A pending request, nonce, hash or exported receipt grants no approval. |
| fixture_adapters versus fixture_ref / fingerprint | Separate adapter definition/version from run/scenario fixture_instance_id and synthetic actor/resource refs. Fingerprint is integrity metadata, not proof of authentic sessions or fixture authorization. |
| verification_runs.status contains the job lifecycle; PRD §9 returns run/job handles | Separate scheduling job_id from execution run_id; retain legacy run.status only as a checked job-state projection if exposed. Define retry/delivery behavior explicitly in §5. |
| evidence_refs / StepEvidence / artifact handle | artifact_id identifies sanitized stored/exported bytes; scenario_result_id identifies verdict; step evidence supplies observations. Internal object_key is never a public handle or download authorization. |
| schema.md §§5–7 SQL/RLS/migration examples and ADR-0010 reference | P1 examples only. ADR-0010 and migration/config files do not exist. Hosted roles/RLS/storage/retention decisions remain open; no implied acceptance or task creation. |
| schema.md §10.3 task links | Actual WBS places SQLite persistence at M1-10, RLS migration at M5-02, RBAC at M5-03. Future owning tasks are trace, not executable tests or completed features. |

## 3. Identity dictionary

Identifiers are references, **never capabilities**. The typed opaque-ID approach is accepted subject to consistent documentation, authorization, validation, serialization and backward compatibility tests. Current candidate record spelling uses the listed prefix plus 32 lowercase hexadecimal characters from a trusted UUID generator, e.g. prj_00000000000000000000000000000001 is synthetic example data. This is not final approval of every DTO field or physical database representation; database UUID versus text mapping and generator enforcement need implementation evidence. Prefix/type checks supplement server ownership lookup. No security property relies on an ID being difficult to guess, and unchanged accepted ID conventions are not reopened for approval.

| Name / proposed prefix | Meaning, uniqueness and ownership |
|---|---|
| organization_id / org_ | PACT hosted organization (P1); maps schema.md org_id. Never target-app tenant_ref. P0 has a local project/identity namespace, not fabricated hosted membership. |
| project_id / prj_ | Trusted local/hosted project record; resolved from authenticated access and optional project_ref alias. Hosted ownership is organization_id + project_id. |
| contract_id / logical key | ADR-0001 policy key, e.g. orders.read, scoped to project_id; also storage contract_key. Not a UUID, reviewer or approval handle. Grammar follows accepted DSL later. |
| draft_id / drf_ | Editable candidate envelope; revision is optimistic concurrency counter. Claimed version is not an approved allocation. |
| contract_version_id / cv_ | Immutable approved-version record; unique project_id + contract_id + version. version is positive integer, separate from draft revision/schema version. |
| review_id / rev_ | Pending human review request bound to exact draft revision/policy/profile/applicability; no authority. |
| review_event_id / dec_ | Append-only protected approval/rejection/withdrawal event; authenticated reviewer_subject has issuer + subject, never target actor_ref or user-supplied email. |
| fixture_adapter_id / fxa_ | Registered typed adapter definition; immutable fixture_version + fixture_digest select its fixture specification. No credentials in definition DTO. |
| fixture_instance_id / fix_ | One disposable setup instance within run/scenario namespace, recorded after authentic setup; never a reusable shared login. |
| scenario_id / scn_ | Immutable typed plan record for exact contract version; scenario_key and rule_id are scoped logical keys. |
| scenario_result_id / sres_ | One scenario execution/result within one run; distinguishes repeated executions of the same scenario. Maps scenario_runs.id. |
| run_id / run_ | One attempted verification on frozen contract/fixture/profile/target/revision fingerprints; never a baseline overwrite. |
| job_id / job_ | Orchestration/lifecycle identity for a bounded async operation; verification job links exactly one run attempt. Other job kinds have no verification verdicts. |
| artifact_id / art_ | Sanitized evidence/report/portable-suite object record; authorized parent lineage and content digest required. Maps evidence_refs.id when step evidence. |
| target_scope_id / scp_ | Versioned normalized destination/scope definition; not permission by itself. |
| execution_grant_id / grt_ | Independently authenticated target/fixture execution authorization bound to scope/fixture/budgets/expiry; policy approval is insufficient. Exact grant representation awaits ADR-0002. |
| event_id / evt_ | Append-only audit/domain event identity with correlation_id, trusted actor and scoped entity references. Review event and audit event remain distinct linked records. |
| source_requirement_id / src_ | SecurityIntent provenance record; not the business source_refs string or an approved policy. |
| finding_id / fnd_ | Verified violation or explicitly informational inconsistency, linked to exact rule/result/evidence; AI hypothesis cannot create a verified finding. |
| drift_event_id / dft_ | Retained comparison of authorized baseline/current runs with compatibility/reason and rule links. |
| policy_change_id / pch_ | Intentional human-reviewed policy revision linking old/new immutable versions and rationale; never same-policy drift. |

Target actor_ref, tenant_ref, resource_ref and rule_id are typed logical fixture/policy references within their definitions. An actor may belong to a target tenant without being a PACT user. Actor sessions are independent ephemeral secret handles kept behind the fixture adapter; these DTOs never contain cookies/tokens or secret-store locations.

Legacy scenario fixture_ref/fixture_adapter aliases resolve to the registered fixture_adapter_id and exact immutable fixture version; generated setup selects a new fixture_instance_id. resource.fixture_ref names a typed synthetic resource binding within that instance, never an artifact path or PACT project ID. Ambiguous/undeclared aliases fail validation instead of selecting a default.

### 3.1 Surface mapping and compatibility validation plan

| Surface | Consistent ID representation / planned checks (NOT RUN) |
|---|---|
| Database/repository ports | Map table id to the typed dictionary field (e.g. contract_versions.id -> contract_version_id, verification_runs.id -> run_id, evidence_refs.id -> artifact_id); contract_key -> logical contract_id and org_id -> organization_id. Physical UUID/text conversion must round-trip without dropping type/project lineage; no schema or migration exists. |
| API DTOs and URLs | Exact documented string/field names; strict type/prefix/length/case checks plus server ancestor/org/project authorization. URI encoding cannot change decoded ID/type/ownership. contract_id remains the project-local logical key. |
| CLI and MCP | Same parsed typed DTOs, --json field names and handles as API/core; no alias coercion between job_id/run_id or fixture adapter/instance. CLI text presentation cannot mutate serialized IDs. |
| Evidence, events and portable exports | Preserve exact IDs, project/organization lineage and original schema/version/hash context; import resolves trusted records separately and cannot establish approval. Storage path/object key is never substituted for artifact_id. |

Planned ID checks: accepted synthetic values round-trip through each surface and repository mapper; malformed/uppercase/unknown prefixes, boolean/numeric/null IDs, wrong namespace and ambiguous legacy aliases fail explicitly. Cross-project/organization tests use well-formed known IDs to prove format is not permission. Serialization preserves exact spelling; repeated retrieval/export has stable identity. Known supported old DTOs are read through an explicit version adapter preserving original bytes and hashes; unsupported/new versions or changing an ID's meaning are rejected. Any future representation change needs a reviewed compatibility map and golden old/new examples; never silently regenerate retained historical IDs. These validation/serialization/backward-compatibility tests are planned, not executed product tests.

## 4. Records, lineage and version dimensions

SecurityIntent(source_requirement_id, provenance) -> ContractDraft(draft_id, revision, candidate policy/questions) -> ReviewRequest(review_id) -> protected ReviewEvent(review_event_id) + immutable ContractVersion(contract_version_id). The proposed human path atomically stores snapshot/nonce/decision event; approval stays pending/non-effective until independently signed durable checkpoint anchoring is verified and current eligibility rechecked. Cross-store commit/anchor/activation recovery protocol remains open; no atomic transaction across separate authorities is claimed. Versions cannot be approved by copying JSON; unresolved questions/conflicts remain NEEDS_REVIEW.

An approved snapshot binds project_id, contract_id/version, exact canonical policy bytes/digest, policy_schema_version, canonicalization, assertion profile definitions/digests, applicability scope, reviewer issuer/subject, decision time and review/audit IDs. Changes create a new candidate; revocation/superseding append events and preserve original bytes. No destructive cascade or silent rehash of approved history.

An authorized verification job freezes ContractRef(s), scenario-set digest/version, approved fixture definition/version/digest, execution grant/scope digest, assertion profiles, target/environment fingerprint, source commit (or explicit unavailable provenance), engine version and isolation image/config reference. Fixture setup adds per-case instance/session provenance without changing frozen expectations. scenario_result_id links run_id + scenario_id + rule_id; artifact_id links its result/step or run-level report. Every joined ancestor must belong to the same authorized project/organization.

| Additional record | Minimal initial semantics / fields |
|---|---|
| Actor / Tenant / Resource / Relationship | Typed actor_ref + roles + tenant_ref; resource_ref/type/owner/tenant; allowlisted subject/relation/object and explicit validity. Fixture facts are authenticated preconditions, not policy inferred from target code. |
| Scenario / StepEvidence | Immutable scenario_key/spec/schema/digest/version/rule links; bounded allowlisted steps; sanitized step_id/request/response summaries, assertions and actual observation time. A step observation cannot assign its own verdict. |
| Finding | finding_id, rule/version/result/artifact references, severity/status and observed first_seen_run_id; verified versus informational/hypothesis labels kept distinct. |
| DriftEvent / PolicyChange | Baseline/current run IDs, comparison algorithm and compatible policy/fixture/profile/environment/runner dimensions, reason/classification; policy revision links reviewed old/new versions and rationale. Missing compatibility -> NOT_COMPARABLE/review, never false regression. |
| AuditEvent | event_id, stream_id, monotonic sequence, previous_event_hash, canonical event/content_hash, actor issuer/subject or explicit scoped machine/unverified identity, project/org namespace, operation/entity/outcome/correlation and trusted UTC timestamp. Approval events bind reviewer/action, immutable contract version/content digest and scope/digest. Fields/wire bounds remain proposed; authority is established by protected service and verified checkpoint, not JSON. |
| AuditCheckpoint | stream_id, last_committed_sequence, chain_tip, created_at UTC, signing_key_id and signature over exact canonical checkpoint payload; separately retained outside audit DB. Namespace/generation, predecessor/history/freshness/trust-anchor fields and byte/signature profiles remain to be specified. |
| AuditRecoveryRecord | Correlates incident/recovery authorization, protected backup identity, independently trusted checkpoint reference, restored sequence/tip, detected missing/unanchored events, recovery outcome and evidence references. Recovery is separately authorized; cannot create reviewer authority or silently replace history. |

Proposed persisted/wire timestamps are timezone-aware UTC with explicit Z; monotonic clocks govern runtime freshness, trusted UTC records chronology. Exact precision/clock recovery is pending ADR-0003. Counters/versions use bounded integers (boolean is not integer); enum/operation sets are closed. Hashes reference a named canonicalization or byte content, never an unspecified digest of arbitrary JSON. No secret authentication proof/challenge is exported with audit metadata.

| Version dimension | Proposed field / interpretation |
|---|---|
| Policy grammar | policy_schema_version = 1.0 refers to ADR-0001's schema_version; independent of transport. |
| Policy canonicalization | canonicalization = pact-json-1 under specified accepted ADR-0001 choices; no silent algorithm change. Canonical digest is 64 lowercase hex SHA-256 for wire examples; normalize hex case only, not policy bytes. Audit/review/checkpoint byte profiles remain separate proposals. |
| Approved policy revision | version positive integer; allocation and exact canonical policy version agree at approval. |
| Draft concurrency | revision nonnegative integer; edits invalidate old challenges. |
| Entity/wire DTO | schema_version = pact.interface/0.1 for these provisional examples; exact match, unsupported versions rejected. Future stable v1 requires review. |
| Scenario/fixture/assertion/evidence | Distinct named schema/profile/fixture versions and immutable digests; never substitute policy version. |
| REST route / events / storage | /api/v1 is PRD's PROPOSED P1 route generation, not accepted DTO v1; events have their own schema_version; migration revision is separate and currently absent. |

Supported historical readers may adapt presentation without altering retained original bytes/digests. Unknown future schema, enum, operation, missing reference or privileged extra field fails validation with no partial mutation. A semantic change requires new policy version and authentic review; no upcaster can infer approval. No migration files or contracts/schema-v1.json exist in this task.

## 5. State and scheduling boundaries

Public contract projection follows DRAFT -> NEEDS_REVIEW -> APPROVED or REJECTED, with immutable approved versions later SUPERSEDED/DEPRECATED. Input schemas cannot write lifecycle states. Draft and approved objects remain distinct records, even when shown in one UI.

Verification job states remain QUEUED, VALIDATING, READY, RUNNING, COMPLETED, CANCELED, FAILED_INFRA, BLOCKED_SCOPE, EXPIRED. Preconditions are revalidated before setup/network access. Job completion never means all scenarios passed. Proposed verification job/run pairing is one-to-one per admitted attempt; initially malformed/unauthorized submissions return an error/audit without allocating a runnable job. An admitted job blocked by later revocation/revalidation retains its run record with actual coverage zero. Inspection/proposal/export jobs carry job_kind and no run_id unless they merely reference an existing run.

Transport retry of an identical authenticated request returns the same committed job/run under an idempotency key; changed payload under the same key conflicts. Duplicate queue delivery/result ingestion cannot execute a scenario again or alter stored verdicts. No automatic target rerun/retry is proposed. A deliberate new attempt creates new job_id/run_id linked to previous attempt and rechecks current grants. Lease/recovery/exactly-once side-effect mechanism remains open; uncertainty yields non-success, not invented execution evidence.

### 5.1 Attempt admission, execution and terminal records

The one-job/one-run design direction is accepted with conditions; the following clarifies its records rather than claiming an executor exists. Run is an **attempt record**, not proof that target verification occurred. Proposed RunView execution_started is initially false, started_at is null until actual verification begins, and executed_scenarios is derived from recorded execution. Preserve admitted_at and current job state, exact contract/version/digest, scope/grant/budgets, fixture/profile/environment context and all later timestamps/observations. Missing preflight context is recorded as unavailable, never fabricated. Actual UTC times and per-scenario verdicts come from the engine, not request fields. No top-level PASS is inferred from zero coverage.

| Condition | Job / run / audit record and required outcome |
|---|---|
| Initially malformed/unauthorized submission | Sanitized rejected-submission audit/correlation only; no admitted job_id/run_id, no run.started event, no assertion or verification verdict. If safe audit persistence fails, return explicit non-success and admit no job. |
| Admitted, still QUEUED/VALIDATING/READY | Exactly one job_id/run_id with frozen authorized references; execution_started=false, started_at=null, executed_scenarios=0. This is scheduled/preflight, not executed coverage. |
| Scope expired/revoked/mismatched during preflight | Job BLOCKED_SCOPE or EXPIRED as appropriate; retain admitted attempt/context, ended_at/reason and audit, no target request. No per-scenario PASS. Scope loss during execution stops remaining operations and preserves already-recorded coverage; cleanup uncertainty is explicit. |
| Cancel before execution | Job CANCELED, execution_started=false, no execution verdict; preserve cancellation request/ack/time/reason and context. Planned unexecuted coverage is not counted as executed. |
| Cancel after execution starts | Record request and acknowledgement separately; CANCELED only after stop acknowledgement and safe cleanup. Preserve actual completed verdicts and canceled/unstarted coverage reasons; inability to stop/clean is FAILED_INFRA with uncertainty, not an invented successful cancellation. |
| Request/step timeout | Known transport/tool fault -> affected scenario ERROR, never PASS; functioning insufficient observation remains INCONCLUSIVE. A completed executor may contain ERROR. |
| Job budget/deadline expiry | Stop new operations, reserve cleanup, record EXPIRED if stopping/cleanup succeed; preserve executed verdicts and explicit unexecuted coverage. Failed cleanup/unknown execution takes FAILED_INFRA with reason rather than falsely claiming clean expiry. |
| Fixture/runner/storage/crash/cleanup infrastructure failure | FAILED_INFRA with available execution_started/start/end/cleanup facts, exact frozen context and historical results retained. Missing observations remain missing; recovery never rewrites an earlier run. |
| All planned work finished and cleanup confirmed | COMPLETED plus actual per-scenario counts/verdicts/coverage; VIOLATION/ERROR/INCONCLUSIVE may still be present. Completion cannot certify security. |
| Same authenticated idempotent transport retry | Return identical committed job_id/run_id; digest mismatch -> conflict; no second attempt, nonce use or target side effect. |
| Deliberate retry/new execution attempt | New job_id/run_id and prior_attempt reference; current eligibility/grants rechecked, own immutable context/timestamps/verdicts/evidence. No overwrite of prior attempt, even after failure. |
| Concurrent delivery/result submission | One guarded execution claim and append-only deduplicated observations; conflicting/stale/foreign lease submission rejected and audited. Crash/lease ambiguity blocks replay until reconciled; no claim of exactly-once target effects without proof. |

The precedence above is a proposal for failure classification, not acceptance of a concrete lease/containment/recovery implementation. Before execution each owning task must prove atomic admission, guarded claims, monotonic deadline handling, cancellation/cleanup and durable evidence through positive/negative/race/crash tests. Historical audit/integrity/checkpoint and active-job revocation mechanisms remain the existing ADR-0002/0003 review gates.

Per-scenario verdicts remain PASS, VIOLATION, INCONCLUSIVE, ERROR, SKIPPED, CANCELED. Known infrastructure/auth/fixture failures are ERROR; insufficient reliable observation is INCONCLUSIVE. SKIPPED/CANCELED retain reasons. Missing token, timeout, 500 on ALLOW, invalid route or absent resource never yields PASS. DENY requires the approved status profile plus no protected disclosure/state change and valid positive controls. Store cleanup failure/job FAILED_INFRA independently of already-observed verdicts; never erase them.

## 6. Provisional versioned schema examples

The following closed JSON Schema-shaped definitions are **PROPOSED** design examples, not a shipped schema validator. Local checks parse JSON and exercise a narrow structural checker; real schema/semantic/authority enforcement belongs to later tasks. Record lookup and authorization are mandatory beyond structural validity.

ContractRef (immutable version reference; no proof of approval):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ContractRef",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "project_id", "contract_id", "contract_version_id", "version", "policy_schema_version", "canonicalization", "content_hash"],
  "properties": {
    "schema_version": {"const": "pact.interface/0.1"},
    "project_id": {"type": "string", "pattern": "^prj_[0-9a-f]{32}$"},
    "contract_id": {"type": "string", "minLength": 1, "maxLength": 96},
    "contract_version_id": {"type": "string", "pattern": "^cv_[0-9a-f]{32}$"},
    "version": {"type": "integer", "minimum": 1, "maximum": 2147483647},
    "policy_schema_version": {"const": "1.0"},
    "canonicalization": {"const": "pact-json-1"},
    "content_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
  }
}
```

Example structurally valid reference; identifiers/digest are deliberately synthetic and **NOT an approved record**:

```json
{
  "schema_version": "pact.interface/0.1",
  "project_id": "prj_00000000000000000000000000000001",
  "contract_id": "orders.read",
  "contract_version_id": "cv_00000000000000000000000000000002",
  "version": 1,
  "policy_schema_version": "1.0",
  "canonicalization": "pact-json-1",
  "content_hash": "0000000000000000000000000000000000000000000000000000000000000000"
}
```

Other record DTOs use the same exact schema_version, typed ID prefixes, bounded fields and closed-property rules. API_SPEC §4 defines RunCreate. ReviewRequest contains draft_id + expected_revision + expected_content_hash and non-authoritative review_id; only the protected store adds reviewer/decision/snapshot/event bindings. JobView contains job_id/job_kind/state/reason/correlation, plus run_id for verification. RunView contains frozen references, actual scenario counts/coverage and cleanup outcome. ArtifactView contains artifact_id, parent run/result/step IDs, digest/media/size/redaction profile and availability; no internal object_key, raw body, token, presigned URL or secret_ref.

## 7. Storage, privacy and approval decisions

P0: minimal local ports for project, draft/version/review events, frozen runs/scenario results, sanitized artifacts and audit. In-memory fakes exercise mechanics, never human authority. SQLite durability/transaction design awaits accepted tooling/approval choices. P1: organizations/users/membership, hosted RBAC, least-privilege DB roles, composite scoped FKs, RLS, private object custody and runner identity require separate accepted designs and actual isolation tests. RLS is additional defense, not proof that a SQL session variable authenticates a user.

Service checks derive ownership from trusted ancestors, check current principal/project permissions and grant eligibility, and authorize metadata and artifact bytes separately. Retention, backup/key custody and deletion durations remain TBD. Withhold uncertain sanitization before storage/export; preserve exact approvals and historical failures under approved retention. Provider opt-in is a separate grant, never implied by a project, candidate or run record.

Owner decisions remain: broader ADR-0003 acceptance and M0-02/M0-05 closure; concrete human identity/presence, fixture/profile/grant, containment/budgets and audit/backend/signature/freshness/recovery protocol choices; hosted RBAC/identity/RLS/retention when authorized. Already accepted DSL, canonical reference, typed opaque IDs, job/run direction and selected audit architecture are not resubmitted unchanged. Full document review and actual implementation/compatibility evidence remain open; no security-sensitive execution is requested or granted.

### 7.1 Selected protected audit storage direction

Dedicated Audit Authority owns the protected store; append/admin/sign/checkpoint-retention/recovery permissions are separate. Agents/runners/ordinary application processes cannot edit/delete historical records. Canonical events bind stream/org/project and immutable review/version/scope references; revocation and supersession append events. Every ancestor/checkpoint read and append must enforce current authorized organization/project, independent of opaque IDs. Separate principal retains signed checkpoints outside audit DB; separate signing authority/managed KMS protects keys. Hosted WORM/versioning/retention is preferred design, not provisioned infrastructure or a selected retention duration.

Wire shapes above are **PROPOSED**, not migrations/shipped parsers or signed receipts. Future bounded closed schemas must reject unknown versions/algorithms/privileged fields, booleans as sequence counters, duplicate keys, missing linkage, cross-stream/project transplants and inconsistent hashes. Event/checkpoint canonical bytes are distinct from policy `pact-json-1`; exact event/hash/signature encoding and genesis/generation semantics remain open. A caller-provided key ID/signature/latest flag cannot supply trust. Signing/checkpoint history cannot alone authenticate a human or authorize an execution target.

Approval activation requires durable event plus verified independently retained anchor; pending/unanchored records cannot authorize. Current eligibility/revocation and latest checkpoint/history must be rechecked. Database restore, missing/conflicting/stale checkpoints or invalid chain/signature enter restricted recovery and disable privileged approvals/dependent operations. Preserve backup/chain/checkpoint/recovery evidence and no automatic reset/new trusted genesis. Storage failure must be surfaced without claiming an unwritten durable incident event. Concrete commit->anchor->activation/retry/crash consistency remains a protocol gate.

Local synthetic events/test-only identities may exercise detectors; same-user DB/checkpoint/key control cannot establish strong tamper/rollback resistance. Keep **REGISTRY_DISABLED** for real privileged approvals until actual separation, identity/user-presence and protected recovery are approved/proven. No DB, key, account/service, migration or privileged handler is created here. See [ADR-0003 §6](adr/0003-human-approval.md#6-immutable-snapshots-and-append-only-audit) and [TEST_PLAN §11](TEST_PLAN.md#11-selected-audit-architecture-and-required-verification), AU-01..10 planned/NOT RUN.

## 8. Verification plan and completion limits

Positive static checks: all six required identities defined and shared with API_SPEC; closed/versioned ContractRef and RunCreate examples parse; synthetic cross-document reference types agree; local links/PRD IDs resolve. Negative checks: unknown/missing/version/type/bound/hash fields and forged status rejected structurally; mutated cross-project/type references and duplicate AC rows detected by documentation checks. These checks do not implement a production parser, service or authentication.

Future tests: forged approval/correct-hash-without-receipt, stale review/race/replay/revocation, cross-project lineage including artifacts/jobs, authentic isolated fixture sessions, ID serialization/backward compatibility, admitted-but-unexecuted records, idempotent queue/result recovery, cancellation/timeout/concurrency, cleanup failure, unknown schema and immutable historical bytes. AC-002/003/006/007/011/014/015/016/017 remain NOT RUN; [TEST_PLAN.md](TEST_PLAN.md) supplies the broader planned matrix and ten-area coverage assessment. EV-0010 retains reviewed v0.1 hashes; todo.md EV-0011 records scoped acceptance, safe follow-up checks and current digest. M0-09 stays IN_REVIEW with unresolved dependencies and full-content review; accepted directions alone do not close it.
