# M0-07 bootstrap acquisition review

> **Version / date:** 0.1 / 2026-10-12
> **Status:** PROPOSED — NOT AUTHORIZED; metadata review only.
> **Scope:** Wave 1 preparation of M0-07; FR-PLT-001, NFR-MAINT-001.
> **Binding:** Exact packet and [artifact review data](bootstrap-artifacts.json) digests in todo EV-0068.

## 1. Intake, authority and allowed changes

Intake HEAD is `a000fe5cd47284c81ccceb0b4f08c38ff45ac070`, clean tracked files on main, two preexisting untracked documents, 68 files excluding Git internals. Work now uses local branch `codex/m0-07-bootstrap-review`. M0-06 DONE is accepted tooling design via [DECISIONS](DECISIONS.md); exact reviewed ADR-0004 bytes remain unchanged. Final pins/licenses/artifacts/acquisition were explicitly withheld, so an implementation request does not authorize downloading distributions.

Allowed changes in this wave: this packet, IMPLEMENTATION_PLAN.md, bootstrap-artifacts.json, and todo.md. Preserve source/tests/ADRs and existing untracked docs. Public primary documentation and package/release JSON metadata were read; no distribution, interpreter, SDK or service was downloaded/installed. No private code was submitted in research requests.

M0-07 exact DoD remains: **Clean checkout installs from lock; one smoke test runs locally and in CI; import causes no side effects; no .env secret committed.** None of the lock/install/CI proof is established by this proposal. M0-07 must remain open until those checks actually run.

## 2. Proposed exact bootstrap versions and ownership

Only the existing pact-core package becomes a workspace member in the later workspace wave. Initial application runtime dependencies stay empty. These are exact review candidates, not an installed or resolved lock. No extras are requested. Each version's primary metadata URL, raw metadata digest, Requires-Python, dependency strings, declared notices, selected wheel filename/URL/size/hash and matrix mapping are in bootstrap-artifacts.json. [PyPI JSON API](https://docs.pypi.org/api/json/).

| Package | Exact candidate | Ownership | Declared license / review note |
|---|---|---|---|
| uv | 0.13.0 | External bootstrap executable, outside app runtime | MIT OR Apache-2.0; new pin vs historical 0.11.7 |
| hatchling | 1.32.4 | Build backend and dev tool | MIT |
| pytest | 9.1.1 | Dev test tool | MIT; no dev extras/plugins |
| ruff | 0.16.8 | Dev lint/format | MIT; retain reviewed candidate line instead of adopting current 0.17.0 automatically |
| mypy | 2.4.0 | Dev types | MIT; bundled typeshed notices require artifact inspection |
| packaging | 26.3 | Build + dev transitive | Apache-2.0 OR BSD-2-Clause |
| pathspec | 1.1.1 | Build + mypy transitive | **MPL-2.0**, explicit new license-review item |
| pluggy | 1.6.0 | Build + pytest transitive | MIT |
| trove-classifiers | 2026.9.21.13 | Build transitive | Apache-2.0 |
| tomlkit | 0.15.1 | Build transitive | MIT; present in current Hatchling requirements |
| iniconfig | 2.3.1 | pytest transitive | MIT |
| pygments | 2.21.0 | pytest transitive | BSD-2-Clause |
| colorama | 0.4.6 | pytest transitive, Windows only | BSD-3-Clause |
| typing-extensions | 4.16.0 | mypy transitive | PSF-2.0 |
| mypy-extensions | 1.1.0 | mypy transitive | MIT |
| librt | 0.16.0 | mypy native transitive | MIT |
| ast-serialize | 0.12.1 | mypy native transitive | MIT; current mypy requirement |

For licenses absent from SPDX fields, compare upstream pinned text/classifiers: [pathspec](https://github.com/cpburnz/python-pathspec/blob/v1.1.1/LICENSE), [mypy-extensions](https://github.com/python/mypy_extensions/blob/1.1.0/LICENSE), [Colorama](https://github.com/tartley/colorama/blob/0.4.6/LICENSE.txt), [Trove](https://github.com/pypa/trove-classifiers/blob/2026.9.21.13/LICENSE). These are metadata/text observations, not clearance of bundled/native component notices or a PACT publication license. Retain license/NOTICE files during later inspection; no publication or redistribution is requested now.

The observed no-extra metadata closure is 17 package identities including uv, with 30 distinct selected wheels. Hatchling's constrained build set is **hatchling, packaging, pathspec, pluggy, tomlkit, trove-classifiers**. pytest requires iniconfig/packaging/pluggy/pygments and Windows colorama; mypy requires typing-extensions/mypy-extensions/pathspec/librt/ast-serialize. Python <3.11 marker dependencies and optional extras are excluded for this matrix. This is reviewed metadata closure, not a solver run; wheel METADATA and actual resolution must later agree or stop for review. Native ABI3 cp39 ast-serialize wheels are tag candidates for the selected CPython minors, not runtime compatibility proof.

Defer Pydantic/FastAPI/HTTPX, their transitives, ASGI listener, provider SDKs, Typer/MCP, databases/cloud/container libraries, PyYAML/Hypothesis and plugins until the corresponding bounded tasks need them. Pydantic's deferred M1-02 adapter remains open. No dependency is added merely because it appears in ADR-0004's broader historical candidate table.

All 17 version-specific PyPI JSON responses report an empty vulnerabilities array at inspection. This means no advisory returned by that endpoint; it does **not** establish absence of vulnerabilities, native-bundle risk, or stale advisories. Broader advisory review and archive notice/content inspection remain NOT RUN. Recheck fixed candidates before executing any downloaded tool; adverse results stop the affected action.

## 3. Proposed CPython artifacts and six-cell matrix

Use standard GIL x86-64 CPython **3.12.15 / 3.13.16 / 3.14.8**, with 3.14.8 the initial default candidate. These releases were verified on Python.org; 3.12.15 is source-only and cannot supply an official current Windows installer. [3.12.15 release](https://www.python.org/downloads/release/python-31215/), [3.13.16 release](https://www.python.org/downloads/release/python-31316/), [3.14.8 release](https://www.python.org/downloads/release/python-3148/).

Propose a new, explicit binary source: **astral-sh/python-build-standalone build 20261009**, install-only stripped archives. uv 0.13.0's pinned download metadata at commit `4ecd0eff2a81e3ffdcd7cfee10d08936e4747c17` lists all six exact artifacts. Each SHA-256 was cross-checked against the release API's asset digest; the metadata source digest is `c68324c2a24a77ef0fa667b6bb6ba8312b90cc6ea0016424c1729574ea86a03d`. Both records are publisher metadata, not independent attestation or downloaded-byte verification. [Pinned metadata](https://github.com/astral-sh/uv/blob/4ecd0eff2a81e3ffdcd7cfee10d08936e4747c17/crates/uv-python-managed/download-metadata.json), [release](https://github.com/astral-sh/python-build-standalone/releases/tag/20261009).

Raw JSON digests bind observed snapshots, not permanent responses from mutable APIs. A second read of the GitHub release JSON changed `download_count`; all other fields of the six selected asset records, including identity, filename, source, size and digest, matched. The artifact hashes remain mandatory fixed values. Do not treat a counter-only metadata change as altered binary content, or replace an artifact hash when material fields differ. [GitHub asset metadata](https://docs.github.com/en/rest/releases/assets?apiVersion=2022-11-28).

| Proposed environment | Exact interpreter | Wheel metadata availability | Actual execution |
|---|---|---|---|
| Windows x86-64 | 3.12.15, 3.13.16, 3.14.8 | Selected win_amd64 / universal wheels for every applicable package | NOT RUN |
| Ubuntu 24.04 x86-64 glibc | 3.12.15, 3.13.16, 3.14.8 | Selected manylinux glibc-compatible / universal wheels for every applicable package; colorama omitted | NOT RUN |

Full support requires all six cells, including installed-wheel imports/build/quality checks. Tags and Requires-Python are preliminary screening only. ARM/musl/PyPy/free-threaded/3.11/3.15+ remain excluded. No Linux host, WSL distro or container is provisioned by this packet; future GitHub Actions upload/run is separately gated. It must disclose the real runner image, action commits, source upload, permissions, cache destinations/retention and cost before remote execution.

Alternatives: use Python.org Windows 3.13/3.14 installers plus a separately reviewed 3.12 build and Linux toolchain; or owner-provided maintained, provenance-verified runtimes. These add different artifacts/build chains and cannot silently substitute for this candidate list. Using installed 3.12.1/3.14.4 as the final maintained baseline is not recommended. Python-build-standalone has bundled component licenses, not PSF-only clearance; inspect the exact archive notices before any execution/installation. The upstream license compilation is guidance, not proof of contents of the selected build. [Licensing reference](https://github.com/astral-sh/python-build-standalone/blob/7d11c1071095ade89249b2b54642ab77ef61f8b1/python-licenses.rst).

## 4. Concrete next owner decision — quarantine only

Review this packet and its JSON digest together. The requested next decision covers **the exact proposed version/artifact set and new binary-source/declared-license inspection scope**, including MPL-2.0 pathspec. It does not re-request accepted tooling architecture. If accepted, permit the following bounded acquisition **for static inspection only**:

- Acquire exactly 30 listed PyPI wheels and 6 listed runtime archives into project-local ignored quarantine; current publisher sizes total **314,881,608 bytes (300.3 MiB)**. Cap cumulative transfer at **1 GiB**, total local acquisition storage at **2 GiB**, wall time at **30 minutes**, paid service cost at **zero**. No automatic replacement, upgrade or extra package.
- HTTPS GET for the exact files.pythonhosted.org wheel URLs and the exact GitHub release URLs in the JSON. Allow at most three redirects only to GitHub's release-assets.githubusercontent.com / objects.githubusercontent.com for those assets; deny other schemes/hosts/destinations. Do not retain/log signed redirect query strings. Fixed release metadata may be rechecked without uploading private data.
- Verify actual SHA-256 and length before inspection; preserve a sanitized per-file receipt and inspect archive entries/license/NOTICE/METADATA without importing or running content. Reject traversal, absolute paths, unsafe links, oversized entries/extraction and mismatched hashes; do not use broad extraction or source build hooks.
- No execution of downloaded binaries, dependency/interpreter installation, global Python/PATH/registry changes, accounts/keys/services, Linux provisioning, remote CI, provider/target requests, telemetry, push, deployment or publication. Transmission of repository source/contracts/evidence/credentials is NONE.

**Owner outcome:** PENDING. This file and its JSON cannot grant permission. A genuine decision is recorded with their exact digests in the next evidence entry. After authorized acquisition, present exact byte/license/provenance findings and a local-installation proposal. Unverified bundled notices or material vulnerability findings keep installation gated; accepting this inspection phase is not approval of unknown terms or code execution.

Rollback: retain recorded metadata/hashes and receipts; quarantine has no active interpreter/venv or executable authority. Cleanup operates only on verified project-local paths; no global package uninstall or history reset. A canceled/missing/mismatched download is a failed acquisition, not a passed workspace check.

## 5. Subsequent workspace implementation and hash enforcement

After the installation gate is separately resolved, create the minimal root/member manifests, single uv.lock, .python-version, ignore rules, exact build constraints/hashes, pytest/Ruff/mypy settings, import smoke and basic CI configuration. Dev dependencies stay out of core runtime wheels. Pure domain cannot import frameworks/providers; build file lists exclude .env, evidence and approval material. Do not install a demo or listening server in M0-07.

Propose uv 0.13.0 because its pinned source describes `--require-build-hashes` separately from runtime hash checking, including build constraints; do not silently reuse a historical `--require-hashes` example for all build dependencies. Current reference docs agree. The locally existing uv 0.11.7 help exposes `--require-hashes` for build constraints, but its sync help does not show the new build-hash flag. No executable uv 0.13.0 command has been run. [Pinned CLI source](https://github.com/astral-sh/uv/blob/4ecd0eff2a81e3ffdcd7cfee10d08936e4747c17/crates/uv-cli/src/lib.rs), [uv CLI reference](https://docs.astral.sh/uv/reference/cli/).

At installation time verify the **actual selected executable** help and behavior. Use reviewed build constraints/hash configuration and build isolation; no `--no-verify-hashes`, unreviewed plugin/build backend, global site-package reuse, unlocked resolver upgrade or online fallback. Missing build-transitive hashes must fail before hook execution. If the supported flags/config differ from the proposal, stop instead of weakening enforcement.

Proposed sequence, **NOT RUN**: explicitly acquire/verify known artifacts → establish project-only interpreter/tool directories → generate lock from reviewed offline artifacts/constraints → validate manifest/lock freshness → offline locked sync/build → fresh wheel installation in a distinct venv → import smoke/unit/lint/format/strict type checks → adverse copies → review and commit. Use explicit interpreter paths, `--offline`, `--no-python-downloads`, `--locked` and build-hash enforcement where actually supported; `--frozen` alone is not freshness proof. Disable uncontrolled pytest plugin autoload and provider egress. Exact executable commands will be recorded when the manifests and verified tools exist.

## 6. Positive, negative and completion evidence

| Check family | Exact expected evidence | Current result |
|---|---|---|
| BR-01 review structure | Unique exact pins/artifacts, fixed HTTPS sources, 64-hex SHA-256, six complete tag mappings, no extras/sdists or active authority flags | Offline review-data checks recorded in EV-0068 |
| BR-02 metadata agreement | Selected wheel hashes/sizes/Requires-Python/markers match saved primary metadata; each Python asset matches both metadata records | Metadata comparison only; byte verification NOT RUN |
| BR-03 adverse review data | Changed hash/source, unreviewed pin, missing/duplicate cell, sdist or activation flag is rejected in disposable in-memory copies | Offline negative checks recorded in EV-0068; not installer/transport tests |
| BR-04 preservation | 67 other original file hashes, 70 other WBS rows, all DoDs/dependencies, prior evidence/journal and reviewed snapshots unchanged | Recorded in EV-0068 |
| TL-01/04/05/06/07/08 | Clean lock/wheel install, side-effect-free imports, quality checks, six supported cells, host/plugin isolation, notice/file-list and repeat-build evidence | NOT RUN; workspace/tools not acquired |
| TL-02/03 | Disposable stale/missing lock, empty cache, wrong artifact/hash and omitted build-transitive pin/hash fail offline without baseline mutation | NOT RUN; review-data mutation tests are not these runtime tests |
| M0-07 CI clause | Actual local smoke and remotely executed authorized CI smoke with recorded run/image/action identity | NOT RUN; no upload/run authorized |

No install, unit/runtime/lint/type/build, Linux/OS isolation, human approval, target/provider, hosted or benchmark pass is claimed here. M0-07 remains BLOCKED at final artifact/acquisition review; roadmap wave 2 is conditional. M0-05's REGISTRY_DISABLED and all other external/security gates remain unchanged.
