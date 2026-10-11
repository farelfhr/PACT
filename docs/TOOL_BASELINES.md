# M6-05 — Relevant tool baseline applicability

Status: **BLOCKED — evaluations NOT RUN.** Documentation proposal v0.1, 2026-10-11. Trace: PRD §§1.4, 11.3; Architecture M6-05. This report documents applicability, omissions and a conditional plan. It is not a benchmark result, approved protocol or execution grant.

## 1. Actual prerequisites

M6-02 is BLOCKED. The owner keeps the independent held-out corpus **DISABLED — PENDING INDEPENDENT REVIEW AND ACCESS-CONTROL PREREQUISITES** (todo.md EV-0056). Independent ground-truth author/reviewer remain unassigned; custodian assignment and access enforcement are pending. M6-01 protocol/ADR-0009 remain proposed and unfrozen. Fixture/runner, tooling and final threat-model reviews are unresolved.

The inspected worktree contains domain/parser/fake-provider code and unit fixtures, but no independently reviewed benchmark apps, keys, target/fixture pins, tool configurations or application harness. HawkScan, StackHawk, Cerbos and Docker executables were not found on PATH; this is not an exhaustive assertion about the computer. No account entitlement, credential, scanner version, Cerbos runtime, approved tool data-flow profile or trial grant was established. No secrets/global credential stores were inspected.

## 2. Legitimate comparison scope

Official documentation inspected on 2026-10-11; capabilities below are documentation findings, not reproduced results. Pin actual release, configuration and entitlement before trials; mutable documentation cannot substitute for installed-version verification.

StackHawk documents cross-profile resource reads and mutating-operation authorization checks, with OpenAPI and multiple authenticated test profiles. Thus cross-user BOLA/BFLA is a relevant comparison cohort. Record actual scan mode and enabled rules; defaults differ across versions/configurations. Custom scripts can cover more specific workflows, so do not claim temporal or custom assertions are inherently impossible. Their preparation belongs in measured setup. [Business logic testing](https://docs.stackhawk.com/hawkscan/business-logic-testing/), [custom scripting](https://docs.stackhawk.com/scripting/).

Its documented first-scan prerequisites include account, API key, scanner, running app and configuration. Platform analysis makes account/data transmission review necessary even when the target is local; exact destinations, transmitted fields, retention, pricing and entitlement remain unverified. Local execution does not imply zero external data flow. [StackHawk FAQ](https://docs.stackhawk.com/getting-started/faq/).

Cerbos documents YAML tests over principal/resource/action combinations and expected effects, executed during policy compilation. Its decision API accepts contextual principal/resource data and returns action decisions. [Policy testing](https://docs.cerbos.dev/cerbos/latest/tutorial/04_testing-policies.html), [decision API](https://docs.cerbos.dev/cerbos/latest/api/index.html).

**Comparison inference:** policy decisions and HTTP enforcement are different observation levels. Use Cerbos policy tests **plus an application harness** for the PRD comparison. A policy-test pass alone cannot prove route enforcement, session validity or absence of protected-data leakage. Do not translate Cerbos EFFECT_DENY directly into PACT PASS.

| Cohort | StackHawk candidate arm | Cerbos candidate arm | Fairness boundary |
|---|---|---|---|
| Own-resource allow / cross-user deny | Multi-profile business-logic checks on pinned synthetic API | Independently authored policy expectations plus HTTP harness | Same requirements, actors, resources and app/fixture revisions; no performance measured |
| Vulnerable vs correct enforcement | Observe scanner findings and valid controls | Keep policy/expected behavior fixed; harness must distinguish bypassed vs enforced decision | No target rewrite solely to favor an arm; PDP integration changes need a separately labeled matched cohort |
| Non-disclosing 403/404 and ALLOW500 | Validate actual evidence/coverage; custom assertions may be necessary | HTTP harness checks status, body and controls | Unknown route/auth/setup is not successful denial; policy result alone insufficient |
| Revoke, transfer, role change, expiry | Potential reviewed workflow scripts; feasibility not established | Policy contextual cases plus state/session harness | Identify exact unsupported semantics before trials; custom effort/limitations disclosed |
| Ambiguous business intent / contract review | Not established as native parity by these sources | Human-authored policy needed; no PACT review authority implied | Report separately from enforcement testing; no penalty for unmeasured or mismatched workflow |

## 3. Actual trial status and omissions

| Arm / evidence | Status | Concrete reason / value |
|---|---|---|
| StackHawk multi-profile scan | **NOT RUN** | No reviewed corpus/running target/OpenAPI/session bindings; scanner not on PATH; account/entitlement/access and data transmission approval not established |
| StackHawk custom workflow | **NOT RUN** | No reviewed script, supported pinned engine, constrained execution profile or permitted mutation/reset procedures |
| Cerbos policy tests | **NOT RUN** | Binary not on PATH; no independently authored/reviewed policy mapping or answer keys; dependency/corpus/tooling gates open |
| Cerbos plus application harness | **NOT RUN** | No harness, target/app pins, independent sessions, fixture reset or authorized execution profile |
| Same target / fixture / policy identifiers | **NOT AVAILABLE** | No matching reviewed cohort exists; no IDs or parity invented |
| Setup / first valid test / execution time | **NOT MEASURED** | No trials; documentation research time is not benchmark setup time |
| License / service / compute / API cost | **UNKNOWN / NOT MEASURED** | No actual entitlement, quote/invoice, billing or metered run; no zero-cost inference from local/open-source execution |
| Validity, recall, false violations, repeatability | **NOT MEASURED** | No independent adjudication or observed evidence; no ranks or superiority claims |

Unavailable access is an omission, not a negative performance result. Predeclare comparable cohorts and capability exclusions; retain assignment/omission reasons and full intended-cohort coverage alongside eligible-cohort metrics. Do not drop difficult cases after seeing results or silently score NOT RUN as a false negative, true negative or PASS.

## 4. Conditional execution plan — NOT EXECUTED

1. Close actual M6-02/M6-01 DoDs and required security/tooling reviews. Establish independent expected labels and enforced held-out custody without exposing keys to configuration/tuning workflows. No held-out activation request until owner-specified prerequisites are satisfied.
2. Obtain a reviewed tool profile: operator, installed release/digest/license, account entitlement where required, allowed target origins/routes/methods, external service destinations/data/retention, budgets and cleanup. Account/API key/service provisioning, downloads and real requests need separate specific authorization; this document grants none.
3. Pin the common requirements, case/family split, app revision, fixture dataset/semantics, actor credentials references, policy mapping, environment and comparison schedule. Review Cerbos translation independently; never import PACT-generated tests as a competing baseline. If integration changes the target, disclose it and restrict comparison to genuinely matched cohorts.
4. Preserve default/native and custom-assisted profiles separately. Freeze rules, scripts, assistance, workload, repetitions and time/cost/request/resource limits before observing outcomes. Restrict scanner scripts and harness execution through reviewed controls; vendor code/config is not a scope grant. No automatic extra scanners, agentic assistance or model requests.
5. Measure actual cold/warm setup, mapping/script/harness authoring, independent review, time-to-first-valid-test, execution, retries, infrastructure and license/service spend. Keep human effort, subscription allocation and marginal cost separately under the approved protocol; unavailable billing stays UNKNOWN.
6. Retain exact executed commands/configuration hashes, sanitized native outputs, target-side request/identity/effect evidence, independent adjudication, omissions, errors and cleanup. An empty findings list or exit zero alone is not a valid authorization result. Preserve failed runs and report limitations without feature-for-feature superiority claims.

No tool commands are presented as executed installation or scan instructions. Future commands must come from the pinned approved tool/profile and be inspected before execution.

## 5. Acceptance checks — planned, all NOT RUN

| Check | Positive evidence | Adverse / boundary evidence |
|---|---|---|
| TBM-01 scope and parity | Fixed matched requirement/app/fixture pins and declared observation level | Changed target, unsupported feature or policy-only output cannot become equivalent HTTP evidence |
| TBM-02 actor/control validity | Separate authentic sessions, valid own-resource allow and valid denied resource | Missing/wrong token, broken fixture, invalid route404, leaked denial or ALLOW500 cannot qualify successful control |
| TBM-03 findings and classification | Reliable vulnerable leak detected, correct target controls verified independently | No findings, script failure, timeout or missing evidence cannot become compliance PASS; native effects/alerts retained |
| TBM-04 safe execution | Approved isolated targets/methods, budgets, redirects/DNS/network limits, cleanup | Unexpected scanner/plugin/script destination, unauthorized write, credential transmission or budget overrun blocked before unapproved effects |
| TBM-05 provenance and fairness | Frozen version/rules/policy/harness/input/output hashes and held-out separation | Hidden-key/PACT-output leakage, target change, post hoc rule tuning or omitted custom effort invalidates comparison |
| TBM-06 timing/cost/history | Actual retained clock/usage/cost/attempts and repeatable resets | Missing bills/time, censored failure or altered history not replaced by zero metrics or inferred superiority |

## 6. DoD and owner handoff

Exact Architecture DoD: **Feature-scope mismatch documented; same target/fixtures, cost/time and limitations disclosed; no unfair feature-for-feature claim.**

Applicability and mismatched observation levels are documented; trial parity and metrics remain unavailable. M6-05 stays **BLOCKED** (BLK-0047), not DONE. A future tool access/data-flow profile remains required; existing held-out-disabled, protocol and Codex/manual decisions are not reopened. Next M6-06 depends on M6-02..05 and is not eligible. No next task started.

Safe documentation checks and exact results: [todo.md EV-0059](../todo.md). Documentation browsing only; no tool launch/install, account/API connection, target probe, provider call, protected corpus read, deployment or Git mutation occurred.
