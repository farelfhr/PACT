# ADR-0009 — Independent benchmark methodology and claims

**Status: PROPOSED — owner approval pending.** Version 0.1, 2026-10-11.
Author: Codex, M6-01. Decision owner: repository developer; independent evaluation roles unassigned. Trace: OQ-12, PRD §11.3; [Architecture M6-01](../ARCHITECTURE.md). This is not benchmark registration, an accepted ADR or an execution grant.

## Context

PACT's differentiation is a hypothesis. M4-09 is BLOCKED/NOT READY; executable baselines, temporal goldens and performance samples are absent. Existing domain/parser/fake-provider tests cannot establish product performance or superiority. Ground truth must remain separate from model inference, and definitions must be approved before tuning.

## Proposed decision

Adopt the versioned [BENCHMARK_PROTOCOL.md v0.1](../BENCHMARK_PROTOCOL.md) as the single detailed methodology candidate. Review binds the exact raw SHA-256 in todo.md EV-0054, together with this ADR's digest. The protocol defines full contract correctness against independent finite-domain answer keys; end-to-end first valid test with censoring; assigned-case recall, valid-evidence precision and explicit false-violation denominators; non-success accounting; material-evidence reproducibility; actual/estimated cost separation; independent held-out families, fair baselines, randomization and family-level uncertainty.

Required protocol §10 profile values and owner sign-off must be recorded before registration/freeze/tuning. Close M4-09's actual gate; never waive it through this proposal. Corpus/baseline implementation and evaluation remain later tasks, not started here. Material amendments require a new retained version and real owner approval before further affected trials.

## Alternatives and trade-offs

| Alternative | Consequence | Proposed choice |
|---|---|---|
| One memorized demo and model-described correctness | Biased sample and no independent oracle | Several independent synthetic families and human answer keys |
| Schema validity or first generated test as success | Invalid policy/setup may look fast | Independent semantic rubric and actual valid controls |
| Drop unknown/error/missing-capability cases | Inflates apparent recall and speed | Fixed assignment denominators, censoring and explicit abstention/coverage |
| Count every request/retry as an independent detection | Inflates sample and uncertainty claims | Preassigned case units; retain family clustering |
| Evaluate new scopes/providers opportunistically | Unsafe egress and incomparable costs | Frozen comparison profile; separate action-specific permissions |
| Tune on all cases before selecting metric definitions | Leakage and post hoc selection | Approved definitions and held-out splits before tuning |

## Security, privacy and consequences

Use synthetic data, approved target/fixture/scope and bounded runner controls. Preserve genuine human approval and immutable failed evidence. No AI-callable review authority, downloaded dependencies, account/key/service provisioning, real provider request, hosted staging activation or deployment is authorized. Hosted staging stays DISABLED. Selected DSL/data/audit directions and unresolved security/identity/tooling ADR reviews remain unchanged.

Paper arithmetic and static checks validate the proposal only; actual model/runner/cost/benchmark results are NOT RUN. The profile must expose missing capabilities, uncertain billing and limited toy-corpus inference. No competitive, compliance or universal-security promise follows. Publication requires licensing/privacy review.

## Owner decision and implementation plan

Request review of these new metric/rubric/methodology choices, not renewed approval of unchanged security/storage decisions. Owner may request changes, defer or give scoped methodology acceptance. Until the exact definitions and completed profile are approved and M4-09 is met, M6-01 stays BLOCKED and no tuning/freeze occurs.

Bounded next steps after genuine gate closure: complete registration/profile; M6-02 builds independently reviewed corpus; subsequent M6 tasks implement baselines, collect authorized trials and analyze retained results. These are a handoff, not authorization to begin a next task here.
