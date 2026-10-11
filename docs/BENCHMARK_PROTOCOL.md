# PACT benchmark protocol — M6-01

**Version:** 0.1, 2026-10-11. **Status: PROPOSED / NOT FROZEN.** Owner sign-off is pending; this document is not an approved pre-registration or an execution grant. Trace: OQ-12, [PRD §11.3](../PRD.MD), [Architecture M6-01](ARCHITECTURE.md), [ADR-0009](adr/0009-evaluation.md). Live status: [todo.md](../todo.md).

## 1. Scope, prerequisites and registration

This proposal specifies how to measure contract correctness, time-to-first-valid-test, precision/recall, false violations, reproducibility and cost before tuning PACT. It defines measurements, not authorization policy. Expected access still comes from independently reviewed human intent; model output and target implementation cannot supply the answer key.

M4-09 is BLOCKED/NOT READY (EV-0035): required runtime comparisons, temporal fixtures, remediation and performance evidence are absent. The repository currently has pure domain/normalization/untrusted approval models, a provisional scenario parser and a fake provider, not an executable benchmark system. Existing unit results are not benchmark observations. M6-01 remains BLOCKED. This draft does not close M4-09, the security/tooling reviews or any upstream task.

Before protocol registration, the owner must approve the exact definitions and completed design profile in §10, and the actual M4-09 DoD must be satisfied. Record protocol version, raw file SHA-256, design-profile hash, owner decision and UTC timestamp in an immutable registration record. A digest identifies bytes; it does not prove approval. M6-02 can then construct the corpus to that approved design. Before any tuning or evaluation, additionally retain the reviewed corpus/answer-key/split identities and schedule hashes. Corpus implementation, baseline implementation, trials and analysis belong to subsequent M6 tasks and are not started here; they are execution gates, not circular prerequisites for approving M6-01's definitions.

No real model request, target execution, dependency acquisition or deployment is authorized by protocol acceptance. Each requires its existing action-specific gates. Hosted staging remains **DISABLED — PENDING PREREQUISITES**. No staging profile exists by assertion in this document.

## 2. Units, answer keys and held-out design

- A **case** is one declared requirement/rule and actor/resource/action observation under pinned tenant, fixture, target revision and assertion semantics. The case ID is assigned before results. Multiple request retries or evidence steps cannot create extra true positives.
- A **trial** is one arm's attempt at one case under a fixed budget. A **family** groups an independently created synthetic application and its related safe/vulnerable/temporal cases. Repeated revisions from the same family are not independent applications.
- An **arm** is manual pytest, Codex-only test generation or PACT, with StackHawk/Cerbos added only for a separately documented technically applicable comparison profile. No supported capability or license is presumed.

Each manifest entry must pin case/family/revision IDs, human requirement, policy version/hash, actor/role/tenant/resource relations, intended action, allowed assertion profile, fixture/version/initial state, scenario/schema version, target/environment/runner fingerprints, expected outcome and answer-key provenance. Keep per-step evidence where the case has a sequence. Preserve previous versions rather than silently updating goldens.

An independent human answer-key author/reviewer, not the inference process, defines expected semantics and validates safe/vulnerable revisions with positive and adverse controls. Named assignments are pending (§10). Existing source behavior must not be treated as the normative policy. Evaluators adjudicate against that frozen key; unresolved semantics enter an ambiguity stratum, not a guessed binary label.

The future corpus must include several independent families and allowed/forbidden access, ambiguity, revocation using an old session, sharing/expiry, tenant transfer and role changes. Pre-assign separate strata for binary authorization, ambiguous policy, infrastructure/precondition failures, compatible drift, approved policy revisions and incompatible environments. A policy change or setup error is not a binary vulnerability label. Sampling and fixture creation are M6-02, not delivered here.

Split by family into development/tuning and held-out evaluation; related variants cannot straddle splits. Record content hashes and access controls. Keep answer keys hidden from generation arms. Use development cases for tuning only after registration. Randomize arm/case order within declared family blocks using a recorded seed and hashed schedule before trials; counterbalance operator/session order. Declare any unavoidable operator knowledge or assistance. Exposure of a held-out key quarantines affected trials, records the leak and requires an approved amendment/new held-out set; do not drop unfavorable outcomes post hoc.

## 3. Correct-contract rubric

Score each assigned case as fully correct or not fully correct, with diagnostic reasons retained. Full correctness requires all of:

1. A structurally and semantically valid versioned candidate; declared roles/resources/actions and typed relations are complete and consistent.
2. Expected ALLOW/DENY behavior and non-disclosure profile match the independent human answer key over **all valuations in the predeclared finite synthetic domain**, including cross-tenant and multi-role boundaries. Missing/extra permissions, conflicting rules and invented ownership semantics fail. Finite-domain agreement does not prove correctness outside that domain.
3. Provenance binds the actual requirement and context; generated content remains non-authoritative DRAFT. Agent-supplied approval cannot count as legitimate approval.
4. For ambiguity cases, explicit NEEDS_REVIEW and precise answerable questions identify the missing semantics; the case cannot execute or silently receive guessed policy. Report this stratum separately from determinate contract accuracy.

**Contract correctness rate:** fully correct candidates / all assigned determinate candidate cases. Invalid, absent, timed-out and unsupported candidates remain in the assigned denominator with reason categories. Partial credit is diagnostic only. Report ambiguity-handling correctness separately against its full assigned denominator. Reviewers resolve disagreements before unblinding aggregate results; retain initial judgments, resolution and unresolved cases. An unresolved key blocks that case's scoring and is disclosed rather than counted correct.

## 4. Time-to-first-valid-test and setup

Start the monotonic clock when the same pinned requirement/context and already authorized environment are handed to each arm. Stop at the first retained test artifact that passes independent validation **and actually exercises** its intended behavior under valid preconditions. It must bind the exact reviewed policy/rule, genuine approval or explicitly authorized harness-only origin, declared actor/session/resource, scope/budgets and evidence; both the intended observation and the case's positive/negative controls must succeed as checks. Harness-only timing is a separate labeled cohort and cannot satisfy a real human-approval cohort.

First model text, schema validation, test compilation or an HTTP status alone is not a valid-test endpoint. Failed authentication, absent routes/resources, ALLOW 500, missing evidence or unsafe execution cannot stop the clock as success. A vulnerable case may have a valid test that correctly reports VIOLATION; test validity is distinct from application PASS.

Record end-to-end elapsed seconds, active authoring time, environment setup time, human review/wait time and model/runner time separately without subtracting waits from the primary end-to-end measure. Common pre-staged setup must be identified; also measure cold setup separately. Log setup steps, configuration changes, dependencies, human interventions and failures for setup complexity.

Predeclare a common per-trial deadline in §10. Unfinished trials are right-censored at that deadline or their earlier explicit stop, with cause, not successful tests at zero/deadline seconds. Report completion fraction over all assigned trials, elapsed/censor data for all trials, and conditional median/range among successes labeled as such. Do not compare successful-only speed without completion rates. More complex survival analysis would require a preregistered amendment, not an improvised result claim.

## 5. Detection metrics and adverse outcomes

Binary units have independently validated gold labels **vulnerable** or **safe** under the same scoped policy. A positive prediction is a reliable, evidence-linked VIOLATION for that case. A claim without adequate evidence is an invalid claim, separately retained, not a TP. An unsupported security claim blocks acceptance of the affected benchmark evidence.

| Symbol / metric | Proposed definition |
|---|---|
| P, N | All preassigned eligible vulnerable and safe binary cases respectively; totals fixed before seeing results. |
| TP | Vulnerable case with a valid evidence-backed VIOLATION. |
| FP | Safe case with a valid but incorrect VIOLATION claim. |
| FN | P − TP; break down into reliable misses, missing capability and non-success/abstention. |
| TN | Safe case with a reliable valid non-violation observation. An error/unknown is never a TN. |
| Precision | TP / (TP + FP). Also disclose invalid/unsupported claims outside this valid-evidence denominator. |
| Assigned-case recall | TP / P, including missed and abstained positive cases. |
| False-violation rate | FP / N. This is the safe-case false-positive rate, not the fraction of predictions that are false. |
| False discovery proportion | FP / (TP + FP); report separately to avoid ambiguous “false positives” terminology. |
| Decidable coverage | (TP + FP + reliable misses + TN) / (P + N). |
| Abstention/non-success rate | Cases with ERROR, INCONCLUSIVE, SKIPPED, CANCELED, BLOCKED_SCOPE, missing capability or no result / assigned binary cases. Categories are mutually exclusive by final case disposition; retain the underlying events. |

Zero denominator yields **NOT_ESTIMABLE**, never 0% or 100%. P = TP + reliable misses + positive abstentions; N = FP + TN + negative abstentions. Invalid unsupported claims enter non-success and their own claim counter. Do not silently exclude them to improve precision.

The common eligible binary cohort must be approved before trials. Report the broader assigned capability coverage too. Optional tools that do not implement a capability are explicitly NOT_APPLICABLE for that comparison profile; do not fabricate a zero metric or superior result. A capability-matched secondary cohort may compare tools, but cannot hide unsupported capabilities in the primary report.

Ambiguous policy must remain NEEDS_REVIEW with no execution. Wrong/missing actor token, broken fixtures/routes, timeout, cancellation, infrastructure failure and incomplete evidence must produce the correct non-PASS disposition. Valid 403/404 DENY requires the approved profile, no protected disclosure and valid route/auth/resource controls. Expected ALLOW 500 cannot pass. Record failure handling as separate stratum correctness, not as successful authorization.

Drift/lifecycle strata require same-policy compatibility and preserved history: PASS→VIOLATION is possible implementation drift; genuinely approved policy changes are distinct; changed fixture/environment or missing fingerprints are NOT_COMPARABLE. Revoke/expiry uses the same old session and controlled time. Unknown admin/ownership or transfer semantics block review, not execution. Never infer genuine reapproval from imported JSON.

## 6. Reproducibility and evidence

Predeclare r independent reset/reseed/process repetitions per pinned case (§10). A reproducible case has all r scheduled trials valid and identical in material normalized observations, rule/step verdicts and retained artifact content hashes to the pinned valid baseline. Primary rate: such cases / all scheduled repeat cases. A missing baseline, error or missing repetition prevents success. Report valid-only agreement separately, with its denominator; repeated ERROR does not demonstrate successful reproducibility.

Pin policy/schema/assertion/scenario versions, fixture semantics/seed, target revision, environment/runner fingerprint, tool/package/model/prompt versions and generation settings. Generation reproducibility and deterministic verification reproducibility are separate measures. Incompatible fingerprints produce NOT_COMPARABLE with counts/reasons; do not discard them from scheduled-case accounting.

Normalization may remove only a prelisted set of presentation metadata (display order where non-semantic, run IDs and timestamps). It must preserve material expected/observed data, status/reason, policy scope and step bindings. Retain original sanitized artifact hashes and normalized comparison hashes, with the normalization version. Material evidence cannot be ignored to obtain agreement. Never retain raw secrets to satisfy reproducibility.

Each trial record needs assignment/order, start/stop/censor timestamps, outcome/reason, review provenance, policy/fixture/environment references, request counts, redacted evidence references/checksums and metered cost. Append reruns and amendments; never overwrite a failing baseline. Missing required evidence makes the trial non-success, not an estimated PASS.

## 7. Cost, budgets and fair baselines

Record actual input/output/cached token counters, API calls/retries, billed amount and currency, provider/model/version and dated pricing basis. Keep observed invoices/usage separate from estimates; missing billing is UNKNOWN, not zero. Use integer minor currency units with a declared scale; currencies cannot be aggregated without a preregistered dated conversion basis. No price or bill is asserted here.

Report total actual cost, cost per assigned trial and cost per valid completed test; denominator zero is NOT_ESTIMABLE. Disclose human minutes, cold setup and infrastructure consumption separately. Monetize these only with owner-approved rates. A fake/no-provider trial may have zero API calls and zero API charges; that measures the offline cohort only and cannot estimate paid-provider performance/cost.

Use identical cases/context and predeclared request/time/concurrency/cost budgets for each comparable arm. Record differences in available tools, operator skill, training, assistance and setup. Manual pytest must use independently reviewed expectations; Codex-only cannot read answer keys or self-approve policy; PACT cannot be tuned on held-out cases. Report unavailable tools as omissions, not measured inferiority. No silent provider fallback, hidden paid calls or unauthorized target traffic.

Enforce budget stop and safe cleanup; exhausted budgets, canceled jobs and crashes never become PASS. Actual operator/reviewer, target grant, consent/data allowlist, package licensing, runner isolation and cleanup proof are prerequisites for trials. Existing unaccepted ADRs are not supplied by this protocol. Store only synthetic/redacted artifacts; human timing records need approved privacy handling.

## 8. Analysis, uncertainty and claims

Report raw case counts, all denominators, strata and family-level metrics before aggregate comparisons. Proposed primary outcomes are full contract correctness, assigned-case recall, false-violation rate and valid-test completion; time/cost/reproducibility are companion outcomes. No superiority threshold, hypothesis result or release conclusion is invented.

Proposed uncertainty method: paired family-cluster bootstrap with 10,000 resamples, sampling whole independent families with replacement and keeping all cases/arms/repetitions in each selected family together. Compute the same aggregate statistic or paired difference per resample. For B = 10,000 sorted finite resample values, use one-based nearest ranks ceil(0.025B) and ceil(0.975B) for a nominal 95% percentile interval. Pin algorithm/seed/version. Report undefined resample counts; if any resample statistic is undefined, mark its interval NOT_ESTIMABLE rather than silently dropping resamples. §10 must set the minimum independent-family count and analysis weighting before this procedure is frozen.

This is a proposed analysis procedure, not an assurance of interval calibration for a small toy corpus. Too few independent families, biased selection, model changes, human learning, missing outcomes and leakage limit conclusions. Never treat requests/steps/repeats as independent sample families. No confidence interval has been computed. M6-06 implements and validates analysis later; report omissions and sensitivity/limitations without selecting favorable post hoc subsets. Any confirmatory hypothesis, multiplicity handling, weighting change or decision threshold requires a pre-trial amendment.

Claims must be scoped to tested profiles/cases/versions and their uncertainty. Do not claim universal security, benchmark superiority or a verified product capability from unit totals, protocol existence or mock arithmetic. Publication needs separate licensing/privacy review of fixtures, answer keys and artifacts.

## 9. Paper examples and protocol checks

The following are **invented arithmetic examples only**, not executed benchmark cases, measured runtimes or product verdicts.

```json
{
  "binary": {"positive": 5, "negative": 4, "tp": 3, "fp": 1, "reliable_misses": 1, "tn": 2, "positive_abstentions": 1, "negative_abstentions": 1},
  "time": {"assigned": 2, "valid_seconds": [12], "censored_seconds": [45]},
  "cost": {"actual_minor_units": 400, "assigned_trials": 9, "valid_tests": 2},
  "repeats": {"scheduled_cases": 2, "all_repetitions_valid_identical_cases": 1}
}
```

Expected arithmetic: precision 3/4; recall 3/5; false-violation 1/4; false-discovery 1/4; decidable coverage 7/9; FN 2 (one miss, one abstention); TN 2, not 3. Completion 1/2, successful-only median 12 seconds, censored 45 seconds is not a successful time. Cost 400/9 minor units per assigned trial and 200 per valid test; reproducibility 1/2, not agreement from repeated errors.

| Check | Positive | Negative / boundary / failure | Current execution scope |
|---|---|---|---|
| DOC-01 metric arithmetic | Exact ratios above | Zero denominators NOT_ESTIMABLE; inconsistent, negative/noninteger counts rejected | Local stdlib paper checks only; no benchmark engine |
| DOC-02 accounting | All assigned cases and distinct strata retained | ERROR→TN, censor→success, duplicate predictions, hidden unsupported capability forbidden | Document/static plus paper checks; actual classifier NOT RUN |
| DOC-03 evidence/registration | Required provenance, manifest/profile/digest and owner gates visible | Missing approval, edited frozen protocol or leaked held-out keys cannot permit tuning | Static proposal checks; protected registry NOT RUN |
| BM-01 contract/time | Correct candidate and independently validated test | Forged approval, guessed policy, failed setup/ALLOW 500 never valid-test completion | Planned benchmark cases NOT RUN |
| BM-02 detection | Scoped vulnerable/safe controls | Invalid 404, protected leakage, invalid unsupported claims and abstentions accounted | Planned benchmark cases NOT RUN |
| BM-03 replay/reproducibility | Valid pinned reset runs agree | Changed semantics, overwritten history, missing fingerprint or repeated ERROR not reproducible success | Planned benchmark cases NOT RUN |
| BM-04 containment/cost | Approved budgets/cleanup and actual usage | Unauthorized egress, budget overrun, cancellation/crash, missing bills fail closed | Planned benchmark cases NOT RUN |

Safe document checks and their exact commands/results are recorded in todo.md EV-0054. They cannot satisfy the owner-approval DoD or M4-09.

## 10. Decisions and freeze checklist

| Required field / decision | Current value | Freeze condition |
|---|---|---|
| Protocol definitions/rubric/estimands/analysis | PROPOSED v0.1, owner review pending | Explicit approval of exact document/ADR digest; changes require a reviewed version |
| Independent family/case counts; strata/split; repeats r; minimum families for intervals | UNSET | Owner-approved finite evaluation profile, several independent families, nonempty held-out split and r ≥ 2; no data-dependent sizing |
| Per-trial deadline, requests, concurrency, resource/cost caps; currency/scale | UNSET | Concrete enforced budgets and accounting units, no open-ended trials |
| Arms, common eligible cohort, secondary profiles, aggregation weighting, model/tool versions | UNSET | Same scenarios and disclosed capability/availability; weighting fixed before outcomes |
| Answer-key author/reviewer, trial operator, adjudicator, safety/privacy reviewer | UNASSIGNED | Real named humans/roles with independent key/inference responsibility and scoped authority |
| Practical success/pivot thresholds and any confirmatory hypotheses | UNSET | Owner defines decision rule before trials; protocol never asserts a product outcome |
| M4-09 dependency | BLOCKED / NOT READY | Actual prerequisite DoD and required reviews before M6-01 registration |
| Future executable corpus, baselines, evidence/runner and approval controls | NOT DELIVERED | Future M6 task evidence and required security/tooling reviews before trials/tuning; not prerequisites for drafting or approving definitions |
| Target/provider/setup/publication permissions | NOT GRANTED by this protocol | Separate real grants and technical enforcement; hosted staging stays DISABLED |

Owner review may accept specific proposed methodology choices while leaving the profile/prerequisites open. Such a decision is not completed pre-registration. Once all registration conditions are met, freeze the exact protocol/profile before tuning; execution still requires corpus/baseline and action permissions. Material amendments get a new version/digest, rationale, owner approval and affected-trial accounting; keep the previous registration and evidence. Do not retroactively redefine metrics or erase poor results.

**M6-01 DoD:** definitions approved before tuning. **Actual evidence now:** reviewable definitions only; no owner sign-off/freeze, no benchmark trials or measured metrics. **Next ID:** M6-02 remains gated by M6-01; do not start it in this session.
