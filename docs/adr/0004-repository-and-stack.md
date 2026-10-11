# ADR-0004 — Repository tooling and dependency boundaries

> **Status:** PROPOSED — awaiting developer review
> **Version / date:** 0.2 / 2026-10-11 (P0 foundation reconciliation)
> **Task / trace:** M0-06; NFR-MAINT-001; PRD §§8.3, 14; Architecture §§1.1–1.2
> **Reviewer:** Developer / repository owner; acceptance NOT RECEIVED
> **Scope:** P0 tooling proposal. No installation, workspace scaffolding, CI activation, publishing, target execution or provider access is authorized by this document.

## 1. Context and observed prerequisites

[PRD.MD](../../PRD.MD), [AGENTS.md](../../AGENTS.md), [workflow.md](../../workflow.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [SECURITY.md](../SECURITY.md) and [todo.md](../../todo.md) govern this proposal. M0-01/03 are DONE; M0-02/04/05 remain IN_REVIEW. [ADR-0001](0001-contract-dsl.md) has accepted specified DSL choices; [ADR-0002 v0.3](0002-fixture-runner.md) and [ADR-0003 v0.3](0003-human-approval.md) remain PROPOSED. Tool selection cannot settle their policy, approval or isolation choices.

**Historical M0-06 intake (2026-10-10):** 17 project documentation/example files, eight directories, main tracking origin/main at ddf945dad8e7aaab0b052a22f37f57d3e0373295. No packages, application code, demo, project tests, pyproject.toml, uv.lock, CI or PACT MCP implementation exist. Existing SECURITY/todo changes and untracked ADRs must be preserved. Creating this ADR adds one document; M0-07 implementation is outside this task.

| Local observation | Exact version / availability | Interpretation |
|---|---|---|
| Windows / shell | Windows 11 AMD64, build 26300; PowerShell 7.6.5 | Observed host, not a verified support matrix |
| Default Python | C:/Program Files/Python314/python.exe, CPython 3.14.4 | Used for safe standard-library document checks |
| Launcher alternatives | Python312/python.exe 3.12.1 and Python311/python.exe 3.11.7 under the user's Local/Programs/Python directory | Old installations; no PACT environment or compatibility evidence |
| uv / Ruff | User Python314/Scripts contains uv 0.11.7 and Ruff 0.16.8 under AppData/Roaming; neither uv nor Docker was found on PATH | uv is installed outside PATH; Docker's machine-wide absence was not established |
| Libraries visible to default Python | Pydantic 2.13.5, pydantic-core 2.46.5, FastAPI 0.141.1, Starlette 1.0.0, pytest 9.1.1, HTTPX 0.28.1 | Metadata observed, no project lock or integration tests |
| Not visible to that interpreter | Hatchling, mypy, Typer, MCP SDK, OpenAI SDK | Not installed in this interpreter; no claim about other environments |
| Git | 2.53.0.windows.3 | Read-only status/hash discovery; no commit or push |


**Current reconciliation (2026-10-11):** domain/normalizer/untrusted approval-model/provisional parser/fake-provider code and unit fixtures exist. No pyproject.toml, uv.lock, build constraints or CI exists. This document remains a tooling proposal; no new package, lock, install or SDK is introduced. The owner chooses the Windows + Linux support-matrix direction; all six OS/minor cells remain required before claiming the proposed full range, and none is certified here.

**Version/provenance verification status:** the observation table above and candidate table below preserve historical EV-0008 observations/proposals, not current installed-project evidence. A fresh `python -X utf8 -I -B` metadata-only check of CPython 3.14.4 found none of the listed third-party distributions visible to that isolated interpreter. This does not prove machine-wide absence or contradict earlier user-site observations. Exact direct/transitive versions, maintained Python patches, publisher/artifact checksums, bundled license/NOTICE completeness, vulnerabilities and wheel/matrix compatibility must be reverified before resolving/freezing a lock or acquisition scope. No public index/release verification or dependency download occurs in this reconciliation.

The [foundation review package](../P0_FOUNDATION_REVIEW.md) and EV-0065 record current scopes/digests; EV-0008 retains the original v0.1 history. License/distribution choice remains pending before publication; private local development does not require inventing a product license.

## 2. Proposed runtime and OS matrix

Use standard, GIL-enabled CPython with `requires-python = ">=3.12,<3.15"`. Propose **3.14.8** as the primary bootstrap patch, recorded later in .python-version and CI; it is a historical candidate pin/reference and is not installed, retested or reverified against current official release/artifact data in this reconciliation. This is a compatibility range, not permission to use stale patches. Before bootstrap, review current security fixes and artifact provenance; any different patch is an explicit recorded revision. The installed 3.12.1/3.14.4 versions are discovery evidence only. [Python 3.14.8 release](https://www.python.org/downloads/release/python-3148/).

| OS / architecture | Python matrix | Proposed gate / current evidence |
|---|---|---|
| Windows 11 x86-64 | 3.12, 3.13, 3.14; primary exact 3.14.8 | Required core/import/CLI/build suite; only document checks on 3.14.4 ran |
| Linux Ubuntu 24.04 x86-64, glibc | 3.12, 3.13, 3.14 | Required CI matrix, offline core tests and wheel install; NOT RUN |
| macOS 14+ arm64 | 3.14 initially | Optional until owner selects support and a real host passes checks; NOT RUN |
| Python 3.11, 3.15+, PyPy, free-threaded builds; Windows ARM64, musl | Excluded initially | Separate dependency/wheel/type compatibility review before expanding support |

Choose maintained patch versions for the 3.12/3.13 matrix before activating it; exact patches and CI image digests are open. All six required OS/minor cells must pass before claiming that support range. Core portability does not prove runner containment: native Windows versus Linux container behavior remains ADR-0002/M0-02 review work, and Docker is not a mandatory core dependency.

## 3. Proposed dependency baseline and licensing

Use **uv 0.11.7**, one workspace and committed uv.lock; **Hatchling 1.32.4** as the PEP 517 backend; Pydantic v2 at validation boundaries, bare FastAPI for the synthetic demo, HTTPX for its bounded transport, pytest/Ruff/mypy as development tools. Exact initial candidates below are review inputs, not a resolved/tested lock. Prefer installed candidate versions for the first compatibility experiment, without inheriting global packages into PACT's environment. Newer versions are not automatically adopted.

| Component / candidate pin | Future permitted ownership / bound for upgrades | Declared license / Python minimum / primary metadata |
|---|---|---|
| CPython 3.14.8 | Toolchain; support >=3.12,<3.15, exact patch per job | PSF-2.0 plus bundled license notices; [Python licenses](https://docs.python.org/3.14/license.html) |
| uv==0.11.7 | Bootstrap tool outside application dependencies; review every tool upgrade | MIT OR Apache-2.0; package >=3.8; [version metadata](https://pypi.org/project/uv/0.11.7/) |
| hatchling==1.32.4 | Each package build backend; exact pin, upgrades within <2 by review | MIT; >=3.10; [metadata](https://pypi.org/project/hatchling/1.32.4/) |
| pydantic==2.13.5 | Core boundary DTO/schema module; >=2.13.5,<3 after compatibility review | MIT; >=3.9; [metadata](https://pypi.org/project/pydantic/2.13.5/) |
| fastapi==0.141.1 | Demo app only at P0; >=0.141.1,<0.142 for proposed update window | MIT; >=3.10; [metadata](https://pypi.org/project/fastapi/0.141.1/) |
| httpx==0.28.1 | Core execution infrastructure adapter and demo test client; >=0.28.1,<0.29 | BSD-3-Clause; >=3.8; [metadata](https://pypi.org/project/httpx/0.28.1/) |
| pytest==9.1.1 | Root dev group; >=9.1.1,<10 by review | MIT; >=3.10; [metadata](https://pypi.org/project/pytest/9.1.1/) |
| ruff==0.16.8 | Root dev group; >=0.16.8,<0.17 by review | MIT; >=3.7; [metadata](https://pypi.org/project/ruff/0.16.8/) |
| mypy==2.4.0 | Root dev group; >=2.4.0,<3 by review | MIT; >=3.10; [metadata](https://pypi.org/project/mypy/2.4.0/) |
| typer==0.27.3 | Deferred M3 CLI adapter only; >=0.27.3,<0.28 | MIT; >=3.10; [metadata](https://pypi.org/project/typer/0.27.3/) |
| mcp==2.3.0 | Deferred M3 MCP adapter only; >=2.3.0,<3, ADR-0005 still absent | MIT; >=3.10; [metadata](https://pypi.org/project/mcp/2.3.0/) |
| openai==3.28.0 | Deferred M2 opt-in provider extra only; >=3.28.0,<4, ADR-0006 still absent | Apache-2.0; >=3.10; [metadata](https://pypi.org/project/openai/3.28.0/) |

Upper bounds delimit review windows; they do not authorize upgrades or replace exact pins. SDK major versions and APIs must be tested independently, not assumed compatible with older examples. Do not add Typer/MCP/OpenAI to the initial bootstrap merely because their candidate metadata is recorded here. Historical EV-0008 metadata recorded Pydantic 2.13.5 as distinct from a 2.14.0 release then observed in [current metadata](https://pypi.org/project/pydantic/); any change requires a new compatibility record.

Historical EV-0008 local metadata reported pydantic-core==2.46.5 (MIT), Starlette 1.0.0 (BSD-3-Clause), and FastAPI constraints starlette>=0.46.0 and pydantic>=2.9.0. Those recorded constraints allowed the then-observed versions but are not evidence that all candidates resolve together. Resolve/pin every transitive dependency and review its wheel availability, license notices and known vulnerabilities before installing. Retain installed-distribution LICENSE/NOTICE and provenance in later build evidence; an SPDX label alone is not a legal or supply-chain clearance. EV-0008 recorded bundled Click in the Typer candidate's packaging; reverify that before acquisition, so inspect bundled notices too. Product license OQ-15 remains the owner's decision; do not create a LICENSE or publish packages in this task.

Exclude FastAPI `standard`/`all` and MCP `cli` extras by default; the first unnecessarily broadens the CLI/cloud/server dependency set. Add an ASGI server only when a separately authorized demo task needs a listening process, after an exact version/license review. No Docker client library, provider fallback gateway, telemetry SDK, hosted database, Redis, queue, cloud service, PyYAML, pytest plugins, Hypothesis or ORM is needed for the tooling bootstrap. ADR-0001 already accepts the restricted JSON-compatible YAML text subset. Full YAML decoding is outside that accepted design; it would require a new scoped decision and tests, not a silent parser/dependency expansion. Add test plugins only for a concrete coverage need with recorded pins; asynchronous tests can initially use standard-library asyncio.

## 4. Package ownership and import direction

Create actual members only when their work package needs them; no placeholder directories now. A non-published workspace root owns dev tools/config/lock, not product behavior. Reuse PRD's layout and names:

| Planned member / module | Owner of behavior | Permitted dependencies / forbidden coupling |
|---|---|---|
| packages/pact-core/pact_core/domain | Typed relations/entities, immutable policy and verdict semantics | Standard-library dataclasses/enums/typing; no FastAPI/Pydantic/HTTPX/SDK/ORM imports in pure domain |
| pact_core application services and ports | Orchestration and interfaces, shared by CLI/MCP | Domain; ports for storage/runner/clock/provider; no concrete adapter imports |
| pact_core boundary schemas | Strict external DTO/JSON Schema validation | Pydantic v2; explicit conversion to domain; no policy changes from coercion/schema generation |
| pact_core execution/persistence/providers infrastructure | Approved transport, storage and optional draft-provider adapters | HTTPX only in transport; stdlib SQLite initially; OpenAI isolated to optional provider module; never import provider SDK into verdict path |
| packages/pact-cli / pact-mcp | CLI/MCP input validation and shared service calls | pact-core plus Typer or MCP SDK respectively; no duplicated approval/verdict logic or AI-callable approval shortcut |
| apps/demo-marketplace | Disposable untrusted synthetic target | Bare FastAPI; no importing PACT to enforce or invent its authorization policy |
| packages/pact-api, apps/web, integrations/github | P1 adapters, not initial workspace members | Deferred; no speculative web/hosted/CI services |
| Root dev group / package test directories | Tooling and future tests | pytest, Ruff, mypy, Hatchling; offline fakes, explicit integration grants; dev deps absent from runtime wheels |

Every local dependency is declared in the consuming member. uv workspace sources bind `pact-core` locally for CLI/MCP, without publishing/index lookup. No demo -> core or core -> demo dependency. Import and AST-boundary tests must cover forbidden imports before implementation claims. Library metadata may eventually use reviewed compatibility ranges for consumers; P0 application/workspace direct pins remain exact until that publishing decision.

## 5. Lock, installation and build strategy

uv workspaces provide a shared lock/environment, with package dependencies still declared per member. Use a root virtual workspace, exact direct pins, explicit member paths and one uv.lock containing transitive versions, sources, environment markers and distribution hashes. Commit the lock only under separately delegated Git authority. .python-version, CI's uv binary version/checksum and matrix patches must agree with the recorded build inputs. [uv workspace documentation](https://docs.astral.sh/uv/concepts/projects/workspaces/).

The following is **illustrative root TOML data**, not a created pyproject.toml. Only pact-core is an initial M0-07 candidate; its manifest/build metadata/import smoke test must be created by that task. Demo, CLI and MCP members are added by their own tasks, not created by this example.

```toml
[project]
name = "pact-workspace"
version = "0.0.0"
requires-python = ">=3.12,<3.15"
dependencies = []

[tool.uv]
package = false

[tool.uv.workspace]
members = ["packages/pact-core"]

[dependency-groups]
dev = ["pytest==9.1.1", "ruff==0.16.8", "mypy==2.4.0", "hatchling==1.32.4"]
```

Each buildable member proposes `[build-system] requires = ["hatchling==1.32.4"]` and `build-backend = "hatchling.build"`, with explicit include/exclude lists. Do not assume uv.lock covers isolated build requirements. Maintain a separate reviewed build-constraints.txt with exact versions and SHA-256 hashes for Hatchling **and all its build transitives**, generated from real resolution, not invented values. Use isolated builds with explicit constraints/hashes. Installed uv 0.11.7 has `--build-constraints` and `--require-hashes`; current documentation also describes newer build-hash settings unavailable in this local help, so do not copy those settings into the baseline. Validate enforcement with missing/wrong/transitive-hash negatives before claiming hermetic builds. [uv build documentation](https://docs.astral.sh/uv/concepts/projects/build/).

Two phases require distinct authorization:

1. **Bootstrap preparation:** owner approves the tool/version/index/artifact scope and acquisition before any dependency download. Default approved source proposal is PyPI HTTPS plus its files.pythonhosted.org artifact host; Python artifacts from python.org; uv release binary source/checksum separately reviewed. No extra indexes, Git URLs, editable external sources, unauthenticated mirrors, insecure-host flags or credential-bearing lock URLs. Populate a project-specific verified cache/wheelhouse, exact Python patch and build dependencies using that authorized scope. Reject third-party sdists requiring unreviewed build hooks; prefer reviewed wheels for every matrix cell. A cache and hash check do not establish publisher trust or freshness.
2. **Offline installation / verification:** fresh project .venv, no global/system-site-package reuse. `--locked` checks manifest/lock agreement; `--offline` and `--no-python-downloads` prevent silent downloads. Offline cache misses, unsupported interpreter/wheel and stale locks must fail visibly, never trigger online fallback or skip a mandatory test. `--frozen` alone skips freshness checking and is unsuitable for the main gate. [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

Lock updates are explicit, reviewed changes: explain dependency/license/security/API effects, resolve exact transitive pins and hashes, rerun all required cells, build and wheel-install checks, record diff and rollback to the prior lock/toolchain. No scheduled/silent upgrades or model-selected dependency installs. Keep .venv/cache/dist and secret files ignored later; build from tracked allowlisted package files, never include .env, evidence, approval records or host data. Bootstrap/package-index egress is distinct from provider inference egress; neither enables the other.

## 6. Proposed future verification commands and failure cases

These commands are **NOT RUN**, require future manifests/lock/tests/cache/build-constraints, and are not PACT commands today. `uv` here means the verified pinned executable; today it is outside PATH. Select an explicitly installed matrix interpreter, never the WindowsApps alias. uv 0.11.7 help confirms these options; execution semantics still require M0-07 checks.

```text
uv lock --check --offline --no-python-downloads
uv sync --locked --offline --no-python-downloads --python 3.14.8 --all-packages --group dev
uv run --no-sync --offline --no-python-downloads python -m pytest
uv run --no-sync --offline --no-python-downloads ruff check .
uv run --no-sync --offline --no-python-downloads ruff format --check .
uv run --no-sync --offline --no-python-downloads mypy packages/pact-core/pact_core
uv build --all-packages --offline --no-python-downloads --python 3.14.8 --build-constraints build-constraints.txt --require-hashes
```

Initial editable sync must use the same reviewed build constraints/hashes through a supported configuration or environment setting; otherwise perform a constrained wheel build and install the reviewed wheel offline. Exact uv 0.11.7 sync build-hash enforcement remains an acceptance test, not an assumption. Do not weaken it with `--no-verify-hashes` or unreviewed build isolation bypasses. For each 3.12/3.13 cell substitute the selected exact patch. No suite may make real target/provider requests by default. pytest should disable uncontrolled plugin autoload; import tests assert no filesystem/network/provider side effects. Configure Ruff target-version py312 and strict mypy for pure domain/ports; record third-party stub exceptions individually, never blanket-ignore missing imports. These settings await M0-07.

| Future case | Positive or negative evidence required | Current status |
|---|---|---|
| TL-01 clean checkout | Every required OS/minor cell installs from unchanged reviewed lock/cache, executes real import smoke and quality checks | NOT RUN; no project configuration |
| TL-02 stale/missing lock | Alter direct pin or remove lock in disposable copy; locked/check gate fails without mutating baseline | NOT RUN |
| TL-03 cache/hash integrity | Empty cache and tampered wheel/build artifact fail offline; missing build-transitive pin/hash fails before hook execution | NOT RUN |
| TL-04 dependency boundary | Domain cannot import framework/SDK; provider-disabled base core and CLI/MCP service equivalence later | NOT RUN for this future locked-workspace gate; existing stdlib source/component evidence is separate |
| TL-05 metadata/matrix | Excluded Python rejected; native wheels for supported cells; build requirements constrained and licensed | NOT RUN |
| TL-06 isolation from host | Global package contamination, arbitrary pytest plugin and import-time egress absent; no secrets in lock/wheel/logs | NOT RUN |
| TL-07 distribution | Build wheel from sdist, install into separate fresh offline venv, import without workspace paths; inspect license/file list | NOT RUN |
| TL-08 reproducibility | Same inputs recorded: source, Python/uv/backend versions, lock/hash/OS; compare two build file lists and checksums | NOT RUN; byte-for-byte reproducibility not claimed |

## 7. Alternatives, trade-offs and reversible decisions

| Area | Recommended proposal | Alternatives / trade-off / open risk |
|---|---|---|
| Packaging | uv virtual workspace + one lock | pip/venv + hashed pip-tools constraints are standards-friendly but add separate lock workflow; Poetry has another tool/config model. uv single environment exposes dev/SDK packages, so import boundaries and isolated base-wheel tests are necessary |
| Backend | Exact Hatchling, isolated constrained build | uv_build avoids a separate backend supply chain but couples backend upgrades to uv; setuptools for legacy extensions adds more configuration. Exact hashes/transitives remain to be resolved |
| Python baseline | >=3.12,<3.15, primary 3.14.8 | 3.12-only minimizes newer-minor issues; 3.14-only reduces CI cells but narrows proposed portability. Three minors need real maintenance capacity/wheels |
| Validation / HTTP / testing | Pydantic v2 DTOs, bare FastAPI demo, HTTPX adapter, pytest | stdlib JSON/dataclasses alone need manual schema boundaries; Starlette-only adds schema integration work; unittest is viable but differs from project proposal. Strict schema behavior still belongs to accepted ADR-0001 |
| Types / format | mypy strict core + Ruff | Pyright is viable but introduces a different runtime/toolchain; Black+separate linter increases tools. mypy 2.4.0 has no local test evidence |
| Storage | stdlib SQLite ports first | Architecture proposes SQLAlchemy/Alembic once schema stabilizes; defer until persistence task/owner decision, no change to contract immutability/atomic audit requirements |
| SDKs | Deferred isolated Typer/MCP/OpenAI adapters | argparse CLI or Codex-host drafts may avoid SDK dependencies; SDK versions can require different transitive HTTP stacks. Egress/transport/approval choices need separate ADRs and tests |

Tool versions, formatter/type configuration and internal directory layout are reversible through reviewed lock/config changes before publication. Public package names/import paths become compatibility obligations once released. Product license, dependency acquisition scope, publishing, hosted services, provider egress, runner privileges, accepted policy/approval semantics and CI merge enforcement require explicit owner/security decisions; this ADR grants none.

## 8. Review request and acceptance evidence

Developer review is requested for the exact v0.2 bytes and remaining tooling design in §§2–7: workspace/backend/build-hash strategy, dependency ownership/deferred SDKs, SQLite deferral and license-review approach. The Windows/Linux matrix direction is already selected and is not requested again unchanged. Accept, request changes or defer the design while explicitly excluding final candidate pins and acquisition: maintained exact Python patches, package/transitive versions and notices, binary provenance/index grant, build-transitive hashes, clean bootstrap support and product publication license remain unresolved. Candidate metadata must be reverified before freeze. Acceptance does not report these tested or authorize a download, target, contract, provider call, privileged runner or CI policy change.

M0-06 documentation coverage is present when this ADR and the current safe reconciliation checks are recorded in EV-0065; EV-0008 remains historical v0.1 evidence. Keep M0-06 IN_REVIEW until genuine required owner review is recorded; no self-acceptance. Architecture §1.2's clean-checkout/dependency evidence before freezing implementation remains NOT RUN and must be supplied by separately authorized M0-07, with any incompatible findings returned as a revision. No M0-07 or next task starts in this session.

- **Owner decision:** PENDING; no approval recorded.
- **Local evidence:** todo.md EV-0065 current metadata/reconciliation checks; EV-0008 historical version/help/metadata observations. No locked project or runtime compatibility evidence.
- **Runtime/build/security evidence:** NOT RUN as listed in §6; no implemented PACT feature or universal security guarantee implied.
