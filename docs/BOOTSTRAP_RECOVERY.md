# M0-07 quarantine completion and proposed local workspace scope

> **Version / date:** 0.1 / 2026-10-12 Asia/Jakarta
> **Result:** ACQUISITION COMPLETE — 36/36; execution/installation NOT AUTHORIZED.
> **Task/trace:** M0-07; FR-PLT-001, NFR-MAINT-001. No successor task.

## 1. Genuine renewal authority

The owner answered **“Izinkan satu upaya karantina baru”** to [inspection v0.1 §6](BOOTSTRAP_INSPECTION.md), local commit `bba5f64887462247e654ccdae4e0074c85e2fad7`, SHA-256 `A4500C6B840DE9C84F3A5E98A92D0401D2A7B01B967241C536E2A26701C35E7A`. That reviewed file remains unchanged. Authority covered one new attempt for the same Windows CPython 3.14.8 URL/hash, maximum three approved redirects, 64 MiB transfer/additional storage, ten minutes, zero paid cost, no automatic retry and no execution/installation. Historical failed receipts and the old fragment were preserved.

## 2. Measured result

| Field | Actual result |
|---|---|
| File | `cpython-3.14.8+20261009-x86_64-pc-windows-msvc-install_only_stripped.tar.gz` |
| HTTPS source | Exact unchanged URL in [EV-0068 manifest](bootstrap-artifacts.json), build 20261009 |
| Redirect destinations | `github.com` → `release-assets.githubusercontent.com`; one redirect, no signed query logged |
| Body bytes | **23,228,299**, exact reviewed size; HTTP/TLS overhead not metered |
| Full SHA-256 | **`5B6FA7DDEABE23AE83D7B54E5043EB4FA1CCB10A73FA4C6B0F541DEA8160D505`**, matches expected |
| Download + static inspection | **3.198 seconds**, monotonic measurement; command exit 0 |
| Additional local storage | **23,418,321 bytes**, new archive and sanitized evidence; below 64 MiB |
| Static contents | **2,190 members**, 61,641,623 expanded bytes inventoried, **44 notice files**, no links |
| Existing data | Original 16-MiB fragment and all prior quarantine files/receipts unchanged by SHA-256 |
| Execution / extraction / install | **NOT RUN**; only stdlib tar/text reads using preexisting Python 3.14.4 |

Every full artifact was then hashed independently against the original manifest: **36/36 match**, totaling **314,881,608 bytes**. Previous static results cover 30 wheels and five archives; this attempt supplies the sixth archive result. This proves acquired bytes and bounded static checks, not installed compatibility or executable safety. It does not erase EV-0069's interrupted acquisition or claim its missing counters were recovered.

The new archive contains CPython and pip/vendor notice texts. Like the other stripped runtimes, it does not contain `PYTHON.json`. The component/license mapping gaps in inspection §4 remain open; no full native SBOM, binary attestation, broader advisory audit or publication-license clearance is claimed. This report introduces no new package or license obligation beyond the owner-reviewed artifact set.

## 3. Preserved local evidence

- `renewal-receipt.json`: SHA-256 `3ACBEC8B05B616FB69E8A5C3FBD973CF06008F224AF090CC215A2C08D01A96F1`; actual download progress, sanitized redirect hosts, final hash/length, timestamps/bounds and static notice inventory.
- `quarantine-complete.json`: SHA-256 `08382851AE78FB642337DC646D2E6DD5C20C60EF7FC2EDED928ECBD32ED4FFE6`; independent 36-file hash/size comparison, exact manifest digest, preserved old evidence and NOT RUN states.
- Both files reside in ignored `D:/Dev/PACT/.bootstrap/quarantine/EV-0068-d6e690c/`. Acquired artifacts are never staged or committed. Earlier receipt digests remain unchanged, including the failed attempt.

## 4. Exact commands and remaining DoD

`& 'C:/Program Files/Python314/python.exe' -X utf8 -I -B 'C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/renew_quarantine.py'` → **exit 0**, one attempt, 23,228,299 body bytes, 3.198 seconds, matching hash, bounded static inspection and preserved fragment. The local script saves progress before completion and does not import acquired code. It reuses a separately copied locally authored inspector with the correct intake HEAD; the old script and reviewed artifact bytes are preserved.

`& 'C:/Program Files/Python314/python.exe' -X utf8 -I -B 'C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/write_recovery_review.py'` → report generation plus independent hash/size preservation assertions; actual final command/preservation/Git results are recorded in todo EV-0070 before local commit.

**NOT RUN:** downloaded interpreter/tool/package execution, dependency resolver/install/build, project pytest/Ruff/mypy, clean-checkout smoke, six-cell runtime matrix, remote CI, OS isolation/human approval, target/provider/hosted/benchmark tests. M0-07 stays open: its exact architecture DoD requires clean checkout installation from lock, smoke locally **and in actual CI**, import with no side effects, and no committed .env secret. No package manager, lock or CI skeleton exists yet.

## 5. Concrete next proposal — offline Windows workspace only

This section is **PROPOSED, NOT AUTHORIZED**. It makes the next decision reviewable; it does not infer installation permission from either quarantine reply. Tooling architecture and artifact identity are already accepted for their recorded scopes and are not reopened.

| Boundary | Proposed authorized work if accepted |
|---|---|
| Environment | This Windows x86-64 machine, normal current user, project-local tools/interpreters/venvs. CPython 3.12.15/3.13.16/3.14.8 Windows archives and uv 0.13.0 Windows wheel only. Linux artifacts remain data-only pending a separately reviewed execution environment |
| Dependencies | Exact manifest pins below; applicable Windows/universal wheels only. uv is a separate bootstrap executable; no provider/CLI/MCP/Pydantic/FastAPI/HTTPX or new dependency. Existing bundled pip is not used for downloads |
| Network/data | **No network request, new acquisition, telemetry, source upload, service/listener or external target/provider call.** Offline/no-index/no-source-build fallback; local wheel files only. These installer settings are not proof of OS-wide network containment |
| Paths | New project-local `.bootstrap/tools/`, `.bootstrap/runtimes/`, `.bootstrap/workspace-checks/`, `.venv/` and bounded per-version test environments; reviewed quarantine remains immutable. Tracked M0-07 files: root pyproject.toml/uv.lock/.python-version/.gitignore, pact-core package manifest, necessary smoke/config/docs and basic CI YAML skeleton, todo evidence. Preserve domain semantics, reviewed ADRs, existing historical tests/fixtures and unrelated files |
| Tools to execute | Verified Windows CPython and uv for version/help/venv/lock/install/build; installed pinned pytest/Ruff/mypy/Hatchling for focused quality checks. Validate actual CLI options first; unsupported offline/build-hash behavior stops the affected action, never switches online or weakens hashes |
| Lock/build | One uv workspace/lock, existing pact-core only, app runtime dependencies initially empty. Exact hashes for wheel installation plus separately constrained/hashed six-package Hatchling build closure. Reject missing/wrong hash, unavailable wheel/cache, stale lock; no global package reliance or sdist download/build. Test portable clean-environment behavior rather than assume local paths in a generated lock are portable |
| Checks | Existing core tests and minimal import smoke; relevant lint/type/build checks; isolated Windows three-minor checks where feasible; meaningful missing-cache/hash/stale-lock failures. Disable third-party pytest plugin autoload. Any meaningful failure is reported and repaired only within M0-07 or separately scoped; no policy behavior change to make quality pass |
| Limits | Additional storage **2 GiB**, executable verification **60 minutes** per bounded run, concurrency 1, service cost zero. Stop on exhausted limit/unexpected subprocess/network request. Clean only newly created scratch/venv directories after verifying absolute paths; retain quarantine, receipts and failed-test evidence |
| Git/CI | Existing codex branch, local checkpoint commit after checks; **no push, remote CI execution, branch protection or publication**. CI skeleton can be authored; no remote pass claimed. Task stays IN_REVIEW/BLOCKED while actual CI/six-cell proof is absent |
| Known limitations | Static notices are present but complete native component mapping/advisory/SBOM/attestation remains unproven. Private local tooling use only; preserve notices and record this limitation. If these gaps must be resolved before any local execution, keep candidates inactive and continue primary-source/static provenance work. No silent risk acceptance or publication follows |

Exact dependency set proposed for this scope:

| Name | Version | Use |
|---|---|---|
| uv | 0.13.0 | bootstrap-tool |
| hatchling | 1.32.4 | direct-dev; build closure |
| pytest | 9.1.1 | direct-dev |
| ruff | 0.16.8 | direct-dev |
| mypy | 2.4.0 | direct-dev |
| packaging | 26.3 | transitive-dev; build closure |
| pathspec | 1.1.1 | transitive-dev; build closure |
| pluggy | 1.6.0 | transitive-dev; build closure |
| trove-classifiers | 2026.9.21.13 | transitive-dev; build closure |
| iniconfig | 2.3.1 | transitive-dev |
| pygments | 2.21.0 | transitive-dev |
| colorama | 0.4.6 | transitive-dev |
| mypy-extensions | 1.1.0 | transitive-dev |
| typing-extensions | 4.16.0 | transitive-dev |
| librt | 0.16.0 | transitive-dev |
| tomlkit | 0.15.1 | transitive-dev; build closure |
| ast-serialize | 0.12.1 | transitive-dev |

Manifest digest stays `8FEDFF4BE21ABAC355B8B9251D55608F75C7E2864BB6E7676C53C00CF32DEEFE`; that immutable file supplies exact selected filenames, URLs, hashes, licenses, dependency markers and six-cell mappings. The proposal selects the Windows subset, not fresh versions or online resolution. Full installed compatibility remains a test obligation.

**One genuine decision needed:** permit this bounded offline local execution/installation and M0-07 workspace work, with the visible private-use provenance limitations, **or** keep executables inactive pending further static provenance review. This does not accept full ADR-0003, approve contracts/targets, activate a broker/runner, permit provider egress, enable staging/corpus, authorize admin setup/remote CI/push, or close M0-07. Existing accepted design and disabled-profile decisions are unchanged.
