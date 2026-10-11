# PACT Security — Initial public interface boundaries

> **Status:** PROVISIONAL / IN_REVIEW; scoped conventions accepted with conditions; ALL endpoints and commands PROPOSED
> **Version / date:** 0.2 / 2026-10-10
> **Task / trace:** M0-09; PRD §§7, 9, 13; FR-IFC-001/002/004/006, FR-CON-001/002, FR-TST-007, FR-EVD-002/003
> **Implementation / review:** No API, CLI, MCP service or authenticated approval path exists; developer review and M0-03/05 closure pending.

## 1. Scope, sources and shared identity

Read [PRD.MD](../PRD.MD), [DATA_MODEL.md](DATA_MODEL.md), [SECURITY.md](SECURITY.md), [ARCHITECTURE.md](ARCHITECTURE.md), [workflow.md](../workflow.md) and [todo.md](../todo.md). All transport adapters call the same application services/state guards/assertion model. P0 supplies planned local CLI/MCP boundaries; HTTP/hosted organization authentication is P1. No endpoint table below authorizes implementation of privileged components.

M0-03/05 and ADR-0001/0003 remain IN_REVIEW/PROPOSED; ADR-0002/0004 and threat-model sign-off also remain unresolved. Developer permits provisional documents only, preserving schema.md. DATA_MODEL §3 is the shared dictionary: contract_id is a project-local logical key, contract_version_id an immutable registry record, review_id a pending request, review_event_id a protected decision, fixture_adapter_id a definition and fixture_instance_id a per-case setup instance. job_id is scheduling state; run_id is one verification attempt; artifact_id is an authorized sanitized object handle. No ID/hash/client JSON confers authority.

On 2026-10-10 the developer accepted the canonical DATA_MODEL reference, typed opaque-ID approach and one-job/one-run direction with authorization, lifecycle, traceability and compatibility conditions. EV-0011 records the exact reviewed v0.1 hashes and exclusions. Full document content, concrete schemas/endpoints, previously unresolved ADRs and runtime enforcement are not finally approved. [DATA_MODEL.md §3.1](DATA_MODEL.md#31-surface-mapping-and-compatibility-validation-plan) maps database, API, CLI, MCP and evidence fields and required future ID serialization/backward-compatibility tests; adapters must not invent alternate spellings or treat handles as capabilities. Unchanged accepted directions are not reopened for approval.

Policy schema_version 1.0 / canonicalization pact-json-1 are ADR-0001 proposals; wire schema_version pact.interface/0.1 is separate. /api/v1 remains a PROPOSED P1 route generation from PRD §9.3. Freeze neither a GA schema nor route spelling before review. Strict fields/enums/bounds and unsupported-version errors apply to every adapter.

## 2. Caller authority and trust boundaries

| Caller / channel | Proposed allowed operations | Mandatory restrictions |
|---|---|---|
| Local CLI / MCP agent | Scoped read-only inspection, candidate submission, request review, plan, separately authorized verification, compare/export/get status | Map caller to trusted local project capability; stdio, OS username, environment variables or an ID alone are not authorization. No automatic provider call/egress, secret-file access or approval. |
| Independent authenticated human review client | Deliberate approve/reject of exact immutable displayed snapshot binding | ADR-0003 protected channel and fresh human verification; no machine/PTY/CI/MCP impersonation. Identity/enrollment and OS separation unresolved; disable authority until proven. |
| P1 browser/API user | Current authenticated org/project permissions for each read/write/job/artifact | TB-09 proposed: trusted issuer/audience/session and server membership checks; browser mutation CSRF/Origin defenses and safe inert rendering; actual mechanisms await review. |
| P1 scoped runner | Assigned job/lease observation ingest and cancellation acknowledgement | No approval/target grant, policy mutation, cross-job/project access, provider secrets or direct general database writes; runner registration does not authorize arbitrary execution. |

Contract approval and execution grants are independent. Review applicability does not grant network access. Before setup/request, resolve approved immutable contract + accepted fixture/profile + current target/fixture grant, normalized origin/peer/port, containment and budgets. Deny unauthorized access by default. No request body supplies raw target URL, shell command, proxy or credential override. Exact scope checks, zero-redirect proposal, DNS/peer/rebinding/egress and cleanup gates remain ADR-0002 decisions.

No model, MCP tool, background job or CI workflow can approve_contract, reject_contract on a human's behalf, enroll reviewers, import authoritative receipts or call a generic privileged service bypass. An MCP request_review only creates a pending review. Human chat approval of a document is not a product contract approval event. Provider data transmission requires separate approved destination/data/purpose; no silent fallback or egress via arbitrary URLs/callbacks.

## 3. Proposed CLI and MCP operations

Each row is **PROPOSED**, with typed input/output using DATA_MODEL vocabulary. Names retain PRD intent; no command can currently run.

| Status | CLI / MCP | Input and output boundary |
|---|---|---|
| PROPOSED | init / project registration service | Local root/project_ref -> project_id; reject traversal/secret roots; registration alone grants no target access. No MCP registration shortcut assumed. |
| PROPOSED | inspect / pact.inspect_project | Authorized project_id or resolved project_ref + selected safe relative paths -> provenance inventory or job_id; scoped read-only, secret/large-file exclusions. |
| PROPOSED | propose / pact.propose_contract | Project + source requirement + optional separately enabled provider_config_ref -> draft_id, revision, candidate/questions or job_id; Codex candidate input can avoid a second model. |
| PROPOSED | review / pact.request_review | draft_id + expected revision/digest -> review_id; CLI hands off to independent human client, cannot pipe yes or pass a bypass flag to approve. |
| PROPOSED | get / pact.get_contract | Authorized project_id + contract_id/version or contract_version_id -> sanitized draft/immutable snapshot projection; state/hash returned is not a portable bearer grant. |
| PROPOSED | plan / pact.plan_scenarios | ContractRef + registered fixture definition -> candidate scenario IDs/coverage/questions; no execution. |
| PROPOSED | verify / pact.run_verification | RunCreate §4 + authenticated idempotency key -> job_id and run_id; separate eligibility/scope checks. |
| PROPOSED | get / pact.get_run | Typed run_id or separately typed job_id selector -> scoped progress/results/coverage; never treat both ID types as interchangeable. |
| PROPOSED | compare / pact.compare_runs | baseline_run_id + current_run_id -> compatibility, rule/result/artifact links; same-policy drift only with compatible fingerprints. |
| PROPOSED | export / pact.export_results | Authorized run_id + allowlisted JSON/HTML format (portable definitions separate typed option) -> artifact_id or export job_id; redaction and safe path/rendering checks. |

CLI proposed --json uses the same normalized DTOs. Noninteractive review cannot approve. Proposed exit classes: 0 requested operation completed (not blanket security), 1 reliable violations, 2 input/authority/coverage/infrastructure failure; exact integer mapping and precedence await interface task review. Mixed violation/error coverage must expose both, never look fully verified. MCP uses typed domain errors and explicit coverage, not an AI confidence verdict.

## 4. PROPOSED RunCreate schema and examples

Only handles to registered approved records are submitted. A request is not an execution grant. ContractRef below must pass DATA_MODEL §6 structure and authoritative lookup; body/path project mismatch is rejected. No caller can select a fixture_instance_id, job_id, run_id, verdict or state.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RunCreate",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "project_id", "contract_ref", "fixture_adapter_id", "fixture_version", "fixture_digest", "target_scope_id", "execution_grant_id"],
  "properties": {
    "schema_version": {"const": "pact.interface/0.1"},
    "project_id": {"type": "string", "pattern": "^prj_[0-9a-f]{32}$"},
    "contract_ref": {"$ref": "DATA_MODEL.md#ContractRef"},
    "fixture_adapter_id": {"type": "string", "pattern": "^fxa_[0-9a-f]{32}$"},
    "fixture_version": {"type": "string", "minLength": 1, "maxLength": 64},
    "fixture_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "target_scope_id": {"type": "string", "pattern": "^scp_[0-9a-f]{32}$"},
    "execution_grant_id": {"type": "string", "pattern": "^grt_[0-9a-f]{32}$"}
  }
}
```

The $ref above is a **documentation reference**, not an executable schema URI: future schema files need a reviewed resolver/registry. Never resolve untrusted schema references over a network. Single-contract RunCreate is the bounded initial proposal; a later bounded contract-set DTO would need explicit version/compatibility review.

Structurally valid synthetic request; all referenced records are absent, so authoritative validation must reject it without target access:

```json
{
  "schema_version": "pact.interface/0.1",
  "project_id": "prj_00000000000000000000000000000001",
  "contract_ref": {
    "schema_version": "pact.interface/0.1",
    "project_id": "prj_00000000000000000000000000000001",
    "contract_id": "orders.read",
    "contract_version_id": "cv_00000000000000000000000000000002",
    "version": 1,
    "policy_schema_version": "1.0",
    "canonicalization": "pact-json-1",
    "content_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  },
  "fixture_adapter_id": "fxa_00000000000000000000000000000003",
  "fixture_version": "synthetic-demo/0.1",
  "fixture_digest": "0000000000000000000000000000000000000000000000000000000000000000",
  "target_scope_id": "scp_00000000000000000000000000000004",
  "execution_grant_id": "grt_00000000000000000000000000000005"
}
```

Rejected untrusted input example, even if otherwise augmented with valid required fields:

```json
{"schema_version":"pact.interface/0.1","status":"APPROVED","reviewer_subject":"human:developer","target_url":"https://example.invalid","command":"print('execute')","verdict":"PASS"}
```

Reasons are extra privileged fields, forbidden raw destination/command/verdict and missing references. JSON parsing success is not semantic acceptance. Rejection of complete valid input plus each individual forbidden field is a required future security test, not merely rejection of an incomplete example.

## 5. P1 REST endpoint proposal

**Every endpoint is PROPOSED; HTTP auth, SDK, server and hosted storage are absent.** Resolve all indirect IDs back to an authorized project/org; route selectors are not trusted ownership. PRD §9.3 paths are retained or explicitly qualified to disambiguate the logical contract key.

| Status | Method / path | Proposed contract and authority |
|---|---|---|
| PROPOSED | POST /api/v1/projects | Typed registration, derived organization ownership; authenticated project-creation permission. |
| PROPOSED | GET /api/v1/projects/{project_id} | Scoped sanitized ProjectView; no secret configuration. |
| PROPOSED | POST /api/v1/projects/{project_id}/inspect | Safe selected paths -> job_id; no arbitrary host path/URL or code execution. |
| PROPOSED | POST /api/v1/projects/{project_id}/contract-drafts | Closed candidate envelope -> draft_id/revision; no client status/reviewer/approval mutation. |
| PROPOSED | GET /api/v1/projects/{project_id}/contracts/{contract_id}/versions | Project-qualified logical key; replaces ambiguous unqualified PRD contracts path for this proposal; immutable sanitized versions, bounded pagination. |
| PROPOSED | POST /api/v1/projects/{project_id}/contracts/{contract_id}/reviews | General callers request pending review only -> review_id. PRD review intent retained; this route cannot approve. |
| PROPOSED | POST /api/v1/human-reviews/{review_id}/decisions | Distinct protected human channel only; exact draft/hash/version/profile/scope/challenge binding plus fresh eligible user action. Mechanism unresolved, disabled until accepted; no MCP/machine reachability. |
| PROPOSED | POST /api/v1/projects/{project_id}/contracts/{contract_id}/scenarios:plan | Exact version/fixture references -> scenarios/coverage or job_id; no execution. |
| PROPOSED | POST /api/v1/verification-runs | RunCreate + idempotency -> job_id/run_id after eligibility checks; cannot grant its own target scope. |
| PROPOSED | GET /api/v1/verification-runs/{run_id} | RunView including actual coverage/results/cleanup; COMPLETED is not safe. |
| PROPOSED | GET /api/v1/jobs/{job_id} | JobView + typed linked run, bounded progress; same project permission even if no run exists. |
| PROPOSED | POST /api/v1/jobs/{job_id}:cancel | Authorized scoped cancellation; request/ack/cleanup and actual final state recorded, no invented instantaneous stop. |
| PROPOSED | POST /api/v1/verification-runs:compare | Authorized baseline/current IDs -> compatibility/drift links, never compare a foreign project. |
| PROPOSED | GET /api/v1/verification-runs/{run_id}/artifacts | Sanitized authorized metadata, opaque artifact IDs, pagination. |
| PROPOSED | GET /api/v1/artifacts/{artifact_id}/content | Reauthorize artifact and all parents, stream sanitized bounded bytes; no caller path/object-key/redirect destination. |
| PROPOSED | GET /api/v1/projects/{project_id}/drift-events | Scoped compatible comparisons and policy revision distinctions. |
| PROPOSED | POST /api/v1/runners/register | Privileged runner enrollment with reviewed identity/capability proof; machine credentials distinct from humans, no target grant by registration. |

A request-review DTO is closed and contains draft_id, expected_revision, expected_content_hash and schema_version; decision/reviewer/session/challenge authority belongs only to the protected human channel. Exact human decision/authentication schema is deferred until ADR-0003's actual mechanism is accepted. No generic PATCH status, approval receipt import, arbitrary SQL, scope override or target discovery route exists in this proposal.

## 6. Errors, async delivery and events

Proposed sanitized error envelope: schema_version, error_code, safe message, correlation_id, retryable. No stack trace, raw response, credentials or foreign existence details. Proposed HTTP mappings: 400 malformed/duplicate-key request; 422 invalid/unsupported schema/semantics; 401 unauthenticated; 403 unavailable permission, or uniform 404 concealment under reviewed API disclosure policy; 409 stale revision/idempotency mismatch; 429 bounded request limit; 503 infrastructure unavailable. These interface statuses are **not target authorization assertion profiles**. Failure cannot create an approved record or PASS.

Every mutation is scoped/audited; failed access retains minimized attempted-action evidence where safe. Collections use proposed bounded limit 1–100, default 20, scoped opaque cursor and allowlisted filters. Cursor manipulation cannot expand scope; numeric ceilings need interface review. Length/depth/request/time/rate limits are explicit configuration proposals, not measured enforcement. Unknown fields/enum/schema/duplicate JSON keys fail closed before mutation. Read-only response additions require reviewed compatible versioning; permissive decoding must never import authority fields.

Authenticated idempotency binds caller/project/operation/key to exact normalized request digest; mismatch conflicts. Async 202/job response acknowledges scheduling only. DATA_MODEL §5 separates job delivery from run execution; duplicate delivery cannot repeat target side effects or manufacture verdicts. Token/lease expiry, storage failure, cancellation uncertainty and missing required observations remain non-success and visible coverage gaps. Safe retry recommendations never bypass a revoked grant.

RunView must explicitly distinguish admission from actual execution: execution_started, admitted_at, nullable started_at/ended_at, executed_scenarios, coverage, cleanup outcome and frozen contract/scope/fixture/version context. The admitted run_id is an attempt handle, not evidence that verification occurred. Initially rejected submissions return only error/correlation and sanitized audit (no runnable job/run or run.started event); an admitted attempt later blocked/canceled/expired before execution keeps its job/run handles, execution_started=false and zero executed coverage. Do not emit a verification verdict for a never-executed attempt. Existing per-scenario observations survive later cancellation, scope loss, timeout or FAILED_INFRA. Cancellation acknowledgement is distinct from a request; timeout and cleanup failure cannot be reported as successful verification. [DATA_MODEL.md §5.1](DATA_MODEL.md#51-attempt-admission-execution-and-terminal-records) defines the proposed lifecycle matrix and recovery limits. Transport replay returns the same committed handle; deliberate retry creates a new linked attempt and revalidates grants. Concurrent/uncertain lease delivery cannot silently rerun or replace evidence.

PRD §9.4 event names remain PROPOSED: project.created, contract.proposed, contract.approved, contract.rejected, run.queued, run.started, run.completed, run.failed, finding.verified, drift.detected, policy.change.approved, runner.revoked. Each envelope binds event_id, timestamp, organization_id (hosted), project_id, authenticated actor provenance, its own schema_version and correlation_id; payload holds typed handles/minimal metadata. Local namespace is explicit, not counterfeit org membership. Only the trusted service emits approval/finding events after validated transitions/assertions; consuming an event/imported payload cannot authorize execution. Replay/dedup/integrity and broker transport are unimplemented; no service or queue added.

## 7. Positive, negative and failure verification plan

| Planned case | Required behavior / evidence; ALL NOT RUN |
|---|---|
| Authorized local draft/read and P1 own-project access | Same normalized core DTOs across adapters; no import/network side effects; AC-001/012. |
| Forged APPROVED, fake reviewer, PTY/CI/MCP human decision, hash without protected event | Reject before authority/network; authentic human positive control plus stale/consumed challenge negatives; AC-002/003. |
| Foreign project/contract/review/fixture/job/run/artifact/cursor IDs | Server ancestor/current-role checks deny read/write/run/content; sanitized attempted-access audit; AC-014 P1. |
| Valid grant versus missing/revoked/expired/expanded scope | Positive isolated fixture control; zero prohibited requests/credential forwarding on rejection; AC-007/015. |
| Correct denial and allow controls versus bad setup/status | Valid 404 profile + no disclosure can PASS; 500 ALLOW, failed login, missing fixture/route and timeout cannot PASS; AC-006/016/017. |
| Redaction/export and non-comparable runs | Canary absent before persistence/download; authorized metadata remains reproducible; no false drift after policy/fixture change; AC-008/009/011. |
| Retry/race/crash/cancel or failed cleanup | Same committed idempotent handle; no duplicate decision/execution/changed verdict; new attempt gets new IDs/current grants; explicit non-success recovery. |
| Unknown version, duplicate keys, excessive bounds, wrong ID type, cross-project nested refs | Structural and semantic rejection before mutations; typed explicit errors. Production enforcement NOT RUN. |

Documentation checks parse these JSON examples, check shared schema/ID fields, all endpoint statuses, local references and mutations; they cannot prove authenticated routes, OS separation, actual schema tooling, runner containment or CI. [TEST_PLAN.md](TEST_PLAN.md) separates future AC evidence from executed static checks. todo.md EV-0010 retains reviewed v0.1 evidence; EV-0011 records scoped acceptance and current clarification checks/digests. M0-09 remains IN_REVIEW because prerequisites/full-content review remain open; no migrations or privileged implementation occur. Accepted unchanged architectural conventions are not requested again.
