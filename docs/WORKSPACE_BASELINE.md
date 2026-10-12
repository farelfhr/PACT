# M0-07 private offline Windows workspace baseline

> **Date/version:** 2026-10-12 / 0.1
> **Status:** Local implementation/checkpoint; M0-07 not DONE. Remote CI/Linux not run.
> **Requirements:** FR-PLT-001, NFR-MAINT-001.

The owner explicitly answered “Izinkan scope offline Windows tersebut” to
BOOTSTRAP_RECOVERY §5 at commit a17d2cf, EV-0070 digest
76109C4FDD638EBFA39CB8EDCEABADB49F2F51DA765882B6F54189DA5CD18A49.
This permits exact reviewed Windows tool/runtime execution and project-local
installation, 2 GiB additional storage, a bounded 60-minute serial run, zero
paid cost and no network/acquisition/upload/services/global/admin/target/provider
or remote CI/push. The review packet and all foundation/ADR bytes remain unchanged.

## Implemented scope

- One virtual uv workspace and local pact-core member, version 0.0.0, private
  classification, empty application runtime dependencies. No CLI/demo/runner,
  Pydantic/SDK/service or authenticated approval feature is added.
- Exact reviewed dependency pins in uv.lock, 28 local wheel hash/size bindings;
  separate six-package hashed Hatchling build constraints. uv 0.13.0 is outside
  application dependencies. Python 3.14.8 is the primary local interpreter;
  Windows 3.12.15/3.13.16 are isolated secondary environments.
- Project-local tools/runtime/venv/cache paths, explicit offline/no-index/no
  interpreter-download settings. `tools/workspace.py` checks every reviewed
  artifact, lock pin/source/hash and complete build closure before use, retains
  notices, rejects unsafe extraction paths and prepares Windows only. Other
  platforms and expanded dependencies need their own scope.
- Non-editable installation avoids Hatchling's additional `editables` requirement.
  No dependency was acquired to work around that initial failure. Only local
  pact-core is built; third-party source builds are disabled.
- Installed wheel includes py.typed and the two immutable JSON schemas; wheel
  and sdist exclude tests, bytecode and .env files. Synthetic canary exclusion
  was actually tested. No actual credentials or .env are committed.
- pytest configuration, strict mypy over all 17 core source files, Ruff lint over
  the repository and formatting checks for newly introduced tools/tests. Existing
  source formatting is preserved; a repository-wide formatter pass is not claimed.
  Two narrowly scoped E402 exceptions retain legacy unittest path bootstrap;
  no security assertion or validation check was removed.
- A disabled manual-only six-cell CI skeleton. It uses no implicitly approved
  checkout/setup action, deliberately fails if its disabled gate is casually
  removed, and has not run. Linux runner/bootstrap and source/artifact transfer
  need a concrete owner-approved CI profile.

## Typing integration and compatibility

The first actual quality check found 89 mypy errors in seven existing files and
six Ruff findings. The bounded changes add helper annotations, fix class-scope
shadowing of builtin object, and use no-op typing.cast after existing type/shape
guards (or before constructors whose existing validation still runs). No value
coercion, relation semantics, approval transition, scenario ordering, canonical
hash or schema artifact changes. Two unused test imports were removed. All
original test assertions, JSON fixtures and schema bytes are preserved.
The 77-test/2,730-subtest pre-change baseline is retained; the final suite includes
14 new workspace checks and still passes the same 2,730 characterization subtests.

## Actual Windows checks

| Interpreter | Locked offline installation | Installed import smoke | Unit suite | Strict mypy / lint / new-tool format |
|---|---|---|---|---|
| 3.12.15 | PASS | PASS | 91 tests + 2,730 subtests PASS | PASS |
| 3.13.16 | PASS | PASS | 91 tests + 2,730 subtests PASS | PASS |
| 3.14.8 | PASS | PASS | 91 tests + 2,730 subtests PASS | PASS |

All cells ran on the same local Windows x86-64 machine. This does not establish
Linux/remote CI or full application support. Imports are checked in a fresh
isolated interpreter against the installed site-packages wheel, with write,
socket/subprocess and other side-effect events guarded and schema resources
compared to their generators. Authenticated approval remains unavailable.
These audited import observations are not OS sandbox/containment guarantees.

Commands below were executed from D:/Dev/PACT using the extracted exact runtime
(the outer evidence wrapper additionally uses preexisting Python 3.14.4):

```powershell
& '.bootstrap/runtimes/cpython-3.12.15-windows-x64/python/python.exe' -I -B tools/workspace.py sync --python 3.12.15
& '.bootstrap/runtimes/cpython-3.12.15-windows-x64/python/python.exe' -I -B tools/workspace.py check --python 3.12.15
& '.bootstrap/runtimes/cpython-3.13.16-windows-x64/python/python.exe' -I -B tools/workspace.py sync --python 3.13.16
& '.bootstrap/runtimes/cpython-3.13.16-windows-x64/python/python.exe' -I -B tools/workspace.py check --python 3.13.16
& '.bootstrap/runtimes/cpython-3.14.8-windows-x64/python/python.exe' -I -B tools/workspace.py sync --python 3.14.8
& '.bootstrap/runtimes/cpython-3.14.8-windows-x64/python/python.exe' -I -B tools/workspace.py check --python 3.14.8
```

Prerequisites are the exact 36 previously acquired/verified files in ignored
.bootstrap/quarantine/EV-0068-d6e690c, a Python 3.12+ stdlib interpreter for initial
local preparation, and genuine permission to execute the Windows profile.
These scripts perform no acquisition. A missing/tampered artifact must fail;
do not remove offline/hash checks or add an online fallback.

uv's local flat-index resolver did not initially write wheel hashes. Actual
reviewed bytes were hashed and bound into the lock; the mandatory preflight
rejects missing/changed bindings. Direct lock regeneration can omit them and
must not be followed by bypassing preflight. Absolute find-links changed source
identity and initially failed lock freshness; relative locked paths are used
for relocation checks. `--require-build-hashes` is experimental in uv 0.13.0,
so enforcement is tested, not assumed from its flag name.

## Actual negative/build evidence

Native uv checks, always offline/no-index/no-cache against disposable data:

| Case | Actual outcome |
|---|---|
| Wrong build-transitive hash | Exit 2, rejected |
| Missing build-transitive hash | Exit 2, rejected |
| Tampered runtime wheel | Exit 1, rejected |
| Empty wheelhouse/cache | Exit 1, resolution fails, no online fallback |
| Positive wheel/sdist build | Exit 0; synthetic .env canary absent |
| Wheel rebuilt from own sdist | Exit 0 with explicit --wheel; payload/hash match |

The first sdist command omitted required --wheel and exited 2; the failure log
is preserved and the corrected invocation passes. An initial wildcard package
name was rejected (exit 2), the first editable sync was blocked by absent
editables, and premature quality probes found missing tools after that failure.
No failure was converted to PASS or resolved with unapproved packages.

Built wheel SHA-256: `395e484ce8807481c6d168d2bc6b6ee55ae5d639ac9888c60d08bd54f953ea61`; sdist-rebuilt wheel SHA-256: `395e484ce8807481c6d168d2bc6b6ee55ae5d639ac9888c60d08bd54f953ea61`. Byte equality was observed for these inputs only, not a universal build reproducibility promise.

Exact native argv, exit, stdout/stderr and durations reside under ignored
.bootstrap/workspace-checks/EV-0071/*.json and negative-builds/*.json. Evidence
summary/hashes are recorded in todo EV-0071; no raw environment secrets are logged.

## Supply-chain correction and remaining gates

The earlier EV-0069 notice-only inventory incorrectly said the uv wheel had no
dedicated native SBOM. This is corrected here without rewriting accepted bytes:
uv-0.13.0.dist-info/sboms/uv.cyclonedx.json is present, CycloneDX 1.5, 595 components,
SHA-256 B58D1D469C3556FEA3CEA35B30061DA909BEA545F305B3B4E6A28AF27A2E38AF.
It is retained in the project-local extracted tool tree. Presence alone does
not prove complete licensing/attestation/advisory coverage. Other private-use
native provenance limitations disclosed in EV-0070 remain visible.

Fresh Git-checkout relocation and stale/missing-lock verification are recorded
in the dated completion appendix after they actually run. Until then they are
NOT RUN; pre-commit copied package build is not a clean Git checkout.

Remote CI smoke and all Linux cells are NOT RUN. Broker/runner isolation, real
human approval, live target/provider calls, hosted/corpus/benchmarks and remote
Git writes remain outside scope. REGISTRY_DISABLED and disabled profiles stay
unchanged. M0-07 cannot be DONE until its exact DoD and actual CI evidence exist;
no other WBS ID is started or closed by this baseline.
