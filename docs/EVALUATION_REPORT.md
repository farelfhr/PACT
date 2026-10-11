# M6-06 — PACT evaluation evidence and analysis readiness

**Status: BLOCKED — PACT evaluation and statistical analysis NOT RUN.** Documentation draft v0.1, 2026-10-11. Trace: PRD §11.3; Architecture M6-06. No measured benchmark, comparative ranking, confidence interval or raw trial dataset is delivered by this report.

## 1. Repository and dependency evidence

Inspected main at HEAD `145f89f6c1123d6ae245390a6bd83e55c05efcbe`. Actual code implements typed domain validation, normalization, untrusted approval-state models, a provisional scenario parser and a scripted fake provider. It has no complete candidate-generation/human-review/fixture/session/HTTP-verification/evidence-persistence evaluation path. Unit fixtures and historical unit totals are not independently reviewed benchmark observations.

| Required dependency | Actual status and missing evidence |
|---|---|
| M6-02 | BLOCKED; independent held-out corpus owner DISABLED (EV-0056). No independently reviewed keys, benchmark apps or tested custody/access separation; key author/reviewer unassigned |
| M6-03 | BLOCKED; human-manual baseline not executed, genuine author/operator and matched requirements/app versions unavailable |
| M6-04 | BLOCKED; Codex baseline not executed; owner selected future bounded profile direction only (EV-0060), actual model/settings/limits unspecified; current PACT-exposed chat not blinded |
| M6-05 | BLOCKED; tool applicability documented, no matched tool trials. Latest owner clarification: external profile PLANNED / UNCONFIGURED, no verified operational profile or external authorization (EV-0062) |

M6-01 remains BLOCKED; [protocol v0.1](BENCHMARK_PROTOCOL.md) and [ADR-0009](adr/0009-evaluation.md) are unapproved/unfrozen. Required family/split/repetition/budget/weighting/role fields are unset. M4-09 is NOT READY; final M0-02 security sign-off and fixture/approval/tooling ADR reviews remain unresolved. A task prompt or tracker status cannot substitute for these gates.

No raw trial files or evaluation metric artifacts were found in the actual repository inventory. There is no benchmark corpus, execution manifest, pinned approved or authorized harness-only trial, verified baseline, observation/evidence store or metered billing record. Protocol §9 arithmetic examples are explicitly invented paper examples and are excluded from measured data. No placeholder JSONL/CSV trial rows or synthetic numbers are presented as raw results.

## 2. Current results — unavailable, not zero

| Requested result | Current value | Why unavailable |
|---|---|---|
| Assigned cases/families/arm coverage | UNSET / NOT MEASURED | No approved assignment manifest or executed cohort; no completion percentage inferred |
| Correct contracts / true positives / false alarms / reliable misses / true negatives | NOT MEASURED | No independent keys or evidence-backed case observations |
| ERROR, INCONCLUSIVE, SKIPPED, CANCELED, BLOCKED_SCOPE trial counts | NOT MEASURED | No trials; prerequisite blocking is task state, not a fabricated run/verdict |
| Precision / recall / false-violation rate / completion | NOT ESTIMATED | Counts and denominators absent; no 0% or 100% claim |
| Confidence/uncertainty intervals / arm differences | NOT_ESTIMABLE | No independently sampled family observations, frozen weighting or validated estimator |
| Setup complexity / authoring / review wait / first valid test / runtime | NOT MEASURED | No actual trial clock events; documentation work is not benchmark setup timing |
| Token/API usage, billed spend, subscription allocation, compute | UNKNOWN / NOT MEASURED | No metered trial or billing data; no zero actual-cost inference |
| Valid pinned reruns and material evidence agreement | NOT MEASURED | No baseline, reset repetitions or compatible fingerprints |
| Redacted raw trial records and checksums | NOT AVAILABLE | No observed records exist; redaction effectiveness not tested on a benchmark |

The owner-imposed external time/cost **budgets of zero** in §5 prohibit activity; they are not measured durations or spend. No trial omissions are silently treated as successful tests, safe cases or competitor inferiority.

## 3. Methodology candidate and conditional analysis plan — NOT EXECUTED

The existing proposed protocol is the methodology candidate, not an accepted analysis specification. Keep its digest binding in todo.md EV-0054 unchanged; do not tune, freeze defaults or select favorable cohorts under this report.

1. Close actual M6-02..05 DoDs and M6-01 profile/review gates. Establish independently reviewed ground truth and approved matched arms, preassigned families/cases, randomized order, held-out separation, actual model/tool versions, finite budgets and operators. Optional capability-matched cohorts and omissions must be declared before outcomes.
2. Collect actual authorized PACT trials only when its required workflow and controls exist. Each valid attempt must bind exact requirement/contract version/hash and genuine approval or separately authorized harness-only origin, scope, rule/scenario, target revision, fixture/session/environment fingerprints and control evidence. A fake-provider normalization is not an inference trial; harness-only evidence cannot satisfy real human-review acceptance.
3. Retain every assigned attempt, error, abstention, infrastructure failure, missing result and repair in immutable sanitized records. No raw secret may be emitted pending later cleanup. Redaction uncertainty withholds the affected segment and invalidates required evidence; preserve forensic metadata without disclosure. Verify artifact digests and independent case adjudication before scoring.
4. Follow protocol §§4–7 for denominators and measurement: precision TP/(TP+FP), assigned-case recall TP/P, false-violation FP/N, completion and decidable coverage with full assignment accounting. Undefined denominators are NOT_ESTIMABLE. ERROR/unknown is never TN; positive abstentions remain recall misses, with reason breakdown. Invalid unsupported claims remain separately visible and cannot qualify as TP.
5. Separate ambiguous-policy correctness, failure handling, drift/lifecycle and binary detection strata. Valid authorization observation requires working authentication/resource/route controls and approved denial semantics. ALLOW500, missing evidence or infrastructure failure is not a successful check. Incompatible policy/fixture/environment remains NOT_COMPARABLE; retain all scheduled case dispositions.
6. Record actual monotonic timing and UTC provenance: cold/warm setup, mapping/authoring, human waits, model/runner time and independent first-valid-test endpoint. Incomplete trials are censored, not successes at zero/deadline seconds. Report successful-only timing alongside full completion rates. Separate actual billing from estimates, human effort, subscription allocation and compute under preapproved units/rates.
7. Validate repeatability through scheduled independent reset/reseed/process trials against pinned material observations and artifact hashes. Separate generation from deterministic verification repeatability; repeated ERROR is not successful reproducibility. Normalize only prelisted presentation fields, never material evidence.
8. Implement and verify analysis after the protocol is accepted. Its current proposal is paired family-cluster bootstrap, retaining all cases/arms/repetitions within sampled families, with specified seed/algorithm/resample count and weighting. Insufficient families or any undefined resample statistic makes the relevant interval NOT_ESTIMABLE under that proposal. Do not treat requests, steps or repeats as independent sample families, invent interval calibration, or silently discard undefined resamples.
9. Publish raw denominators, family/stratum counts, omissions, costs, confidence/limitations and only claims supported by actual profiles/versions. No superiority, universal-security, hosted-readiness or launch conclusion follows from this blocked report. Publication requires separate privacy/licensing review.

## 4. Future redacted record requirements — no actual records

These are planning fields, not a new implemented wire schema or approval receipt format. Conditional future paths: `benchmarks/evaluation/{manifests/,trial-records.jsonl,analysis/,artifacts/}`; no such directories or datasets were created here.

| Record group | Required retained evidence |
|---|---|
| Assignment and provenance | Frozen protocol/profile digest, arm/family/case/attempt, randomized order, held-out classification and input/prompt provenance without protected keys |
| Policy and execution authority | Contract version/body digest/origin, reviewer and scope references verified independently, rule/scenario/assertion versions; no serialized status grants execution |
| Environment and controls | App revision, fixture seed/semantics, actor/session labels without tokens, target/runner fingerprint, valid control observations, request counts and cleanup |
| Observation and disposition | Sanitized expected/observed evidence, verdict/reason, infrastructure/ambiguity/invalid-claim/censor details, adjudication reference |
| Timing and cost | Actual start/stop/censor clock events, setup/authoring/wait components, usage/billing source and currency/scale, explicit missing values |
| Integrity and analysis | Original redacted artifact digest, material normalization version/hash, immutable rerun links, denominator/stratum eligibility and independent scoring provenance |

## 5. Owner-directed external tool template

The owner clarified the selected future-profile direction during this task: **PLANNED / UNCONFIGURED; no verified operational profile or external benchmark authorization available.** [benchmark-tool-profile.template.json](benchmark-tool-profile.template.json) is the requested reusable documentation template. It is not read by a runtime and cannot authenticate approval, activate a provider or authorize targets.

- Identifier NOT ASSIGNED; tool/name/version NOT VERIFIED; references PENDING. JSON null/empty references represent unresolved values, not populated defaults.
- Responsible operator and security reviewer NOT YET ASSIGNED. The owner may coordinate future setup without becoming an authorized operator automatically.
- StackHawk entitlement NOT PROVIDED; no subscription/account/license/API access assumed.
- External target origins, service destinations, staging authorization and permitted transmitted data: NONE. External requests DISABLED; retention policy PENDING.
- External execution time budget ZERO and external service cost budget ZERO until separate authorization. Currency is null because no spend is authorized or priced. No account, purchase, subscription, infrastructure or cost incurred.
- Synthetic local data may be used only within existing authorized development boundaries; this does not satisfy reviewed held-out independence or grant new target execution.

Missing activation evidence: owner-initiated concrete profile ID and pinned/licensed tool references; appointed operator/reviewer; actual M6-02..05/M6-01 gate closure; reviewed independent keys and tested custody; specific approved target/service/data/retention/scope; enforceable resource budgets and cleanup/isolation tests. Do not label this profile VERIFIED, READY or AUTHORIZED. Do not request these unchanged missing fields again until the owner initiates external benchmark setup or provides new details.

## 6. Positive/adverse acceptance checks — planned, all NOT RUN

| Check | Positive proof | Negative/error/boundary |
|---|---|---|
| EA-01 raw provenance | Real independently reviewed assignments, pins, evidence digests and immutable attempts | Invented paper rows, forged approvals, mismatched fixtures or lost attempts cannot qualify as raw results |
| EA-02 outcome accounting | Valid TP/FP/TN/miss and mutually exclusive final dispositions plus event history | ERROR→TN, unknown→PASS, unsupported claim→TP, duplicate case or hidden omitted stratum refused |
| EA-03 timing/cost | Actual first independently validated test, censor times, usage and billing source | Response/compile-only success, missing bill→zero cost or timeout→successful completion refused |
| EA-04 uncertainty | Frozen paired family sampling/seed/weighting; reproducible defined estimates | Repetition treated as independent family, small/missing cohort or undefined denominator/resample cannot produce a confidence claim |
| EA-05 privacy and scope | Redacted retained data, authorized isolated target, key separation, bounded cleanup | Secret/answer-key leak, unauthorized outbound/runner operation or failed cleanup blocks affected trial/evidence |
| EA-06 comparison/repeatability | Matched policy/environment, reset trials and material-hash agreement | Changed policy or fixture is NOT_COMPARABLE; repeated errors, normalized-away failure or overwritten evidence not successful agreement |

Safe AST/JSON/template/document/ledger checks are recorded in [todo.md EV-0061](../todo.md); they are not executions of EA-01..06. No benchmark model, target or provider request was made by evaluation tooling; this Codex chat is not an evaluation trial.

## 7. DoD and handoff

Exact Architecture DoD: **Results include errors, inconclusive cases, confidence/uncertainty, spend and setup overhead; claims match measured coverage.** Actual results and required execution evidence are absent; the DoD is unmet. M6-06 is **BLOCKED / BLK-0048**, not DONE. Existing methodology and baseline review requests remain pending without repetition. The latest external-profile clarification is recorded in EV-0062; no external activation is requested.

M6-07 depends on M5-16/M6-06 and remains gated. M6-08 requires M6-06/07. No next eligible new implementation or next task started. Retain failed/history evidence and all existing owner decisions.
