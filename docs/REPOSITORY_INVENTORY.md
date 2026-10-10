# PACT Security — M0-01 Repository Inventory and Documentation Reconciliation

> **Observed date:** 2026-10-10 (Asia/Jakarta)
> **Owner/session:** Codex / M0-01 inventory session
> **Scope:** P0 documentation intake only; PRD §§0, 14, 17; Architecture §7, M0-01.
> **Authority:** Observations and pending decisions, not architecture acceptance, contract approval, execution permission or product security evidence.

## 1. Task intake and completion criteria

The owner authorized only M0-01: inventory actual files, reconcile references, investigate the schema filename, identify gaps, and record evidence in the tracker. M0-01 has no WBS dependencies. The intake documents are accessible. No accepted ADR is required to describe current filesystem facts.

Allowed project edits are this new document and [todo.md](../todo.md). The other ten original files are preserved byte-for-byte. No source, package scaffolding, database, ADR, target scope, dependencies or Git repository is created. No local application, live security test, external model call, remote write or product MCP tool is executed.

Measurable completion criteria:

- All actual files and directories, including hidden entries, are accounted for.
- Git state and absence of implementation artifacts are established by local inspection.
- Existing documents are distinguished from proposed or missing paths; schema content and canonical-path claims are reconciled without inventing approval.
- Discrepancies, pending decisions, dependencies and next eligible tasks are recorded with source references.
- Safe checks validate paths, relative Markdown links, WBS/ledger counts, tracker totals and preservation of unrelated files/history.
- The tracker contains truthful status transitions, evidence, milestone totals and an appended session journal.

This is a documentation-only task. Runtime AC-001–017, security controls and release gates are not exercised or satisfied by this inventory. Required later design approvals remain pending; this task does not change policy or trust semantics.

## 2. Exact filesystem and Git observations

Workspace root: `D:\Dev\PACT`.

Before editing: **11 files and six directories**, excluding the workspace root. All files are Markdown. After this task adds this inventory: **12 files and the same six directories**.

```text
D:\Dev\PACT\
├── .agents\
│   └── skills\
│       ├── pact-refactor\
│       │   └── SKILL.md
│       ├── pact-security-review\
│       │   └── SKILL.md
│       └── pact-testing\
│           └── SKILL.md
├── docs\
│   ├── ARCHITECTURE.md
│   ├── REPOSITORY_INVENTORY.md    # added by M0-01
│   ├── schema.md
│   └── SECURITY.md
├── AGENTS.md
├── PRD.MD
├── skill.md
├── todo.md
└── workflow.md
```

`git rev-parse --is-inside-work-tree` and `git status --short --branch` both reported: `fatal: not a git repository (or any of the parent directories): .git`. A hidden-entry inventory also found no `.git` file/directory. **Git is not initialized**, and the workspace is not inside a parent Git repository. Branch, commit, remotes, tracked/untracked state and Git diff are unavailable. Git initialization or committing is a separate owner decision, not an implied M0-01 action.

No source packages, application tests, demo app, migrations, build/dependency configuration, CI workflows, executable PACT service or PACT MCP implementation is present in this tree. This is a filesystem observation; it does not assert that unrelated services elsewhere on the computer do not exist.

## 3. Existing documents and actual roles

| Actual path | Version / recorded maturity | Interpretation |
|---|---|---|
| [PRD.MD](../PRD.MD) | 1.0.0 / DRAFT | Normative product requirements; proposed details still require decisions. |
| [AGENTS.md](../AGENTS.md) | 1.0.2 / implementation guidance | Standing engineering invariants. |
| [workflow.md](../workflow.md) | 1.0.0 / proposed operating policy | Engineering action levels, state transitions and gates; no runtime authorization. |
| [skill.md](../skill.md) | 1.0.0 / workflow specification | Root reusable workflow library; not an executable PACT integration. |
| [todo.md](../todo.md) | 1.0.0 / operational ledger | Canonical task status, decisions and evidence; initialization history is preserved. |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 1.0.0 / DRAFT, NOT YET APPROVED | Proposed stack and 71-item WBS; no accepted ADRs. |
| [SECURITY.md](./SECURITY.md) | 1.0.0 / DRAFT, REVIEW REQUIRED | Existing threat-model input for M0-02; no reviewer sign-off or implemented controls. |
| [schema.md](./schema.md) | 1.0.0 / DRAFT, NOT DEPLOYED | Database/storage specification; declares `docs/DATA_MODEL.md` canonical, but that path is absent. |
| [.agents/skills/pact-testing/SKILL.md](../.agents/skills/pact-testing/SKILL.md) | Native engineering skill manifest | Workflow A adapter to root `skill.md`; not a test suite. |
| [.agents/skills/pact-security-review/SKILL.md](../.agents/skills/pact-security-review/SKILL.md) | Native engineering skill manifest | Workflow B adapter; not an approved security review. |
| [.agents/skills/pact-refactor/SKILL.md](../.agents/skills/pact-refactor/SKILL.md) | Native engineering skill manifest | Workflow C adapter; not an implementation. |

The actual workflow filename is `workflow.md`; the escaped `workflow\.md` spelling in task text does not identify a separate file or directory. Root `skill.md` versus native `SKILL.md` is an intentional distinction documented by `skill.md` §0.

## 4. Referenced missing artifacts

Absent proposed layouts are backlog gaps, not evidence of broken implemented features. No empty folders or placeholders were created to imitate them.

| Missing path(s) | Reference / task association | Current disposition |
|---|---|---|
| `docs/DATA_MODEL.md` | PRD §13/14; AGENTS §12; M0-09 | Existing database draft is at `docs/schema.md`; investigate canonicalization below. |
| `docs/API_SPEC.md` | PRD §9/14; M0-09 | No frozen CLI/MCP/REST specification. |
| `docs/TEST_PLAN.md` | PRD §11/14; M0-08 | No canonical test-plan artifact; embedded planned matrices are not executable tests. |
| `docs/ROADMAP.md` | PRD §14; architecture §7 | Optional summary only under current AGENTS/tracker rules; do not establish a competing ledger. |
| `docs/DECISIONS.md`, `docs/adr/` | PRD §17; AGENTS §12 | Registers describe planned decisions; no ADR files or acceptance evidence exist. |
| `docs/contracts/`, `docs/contracts/schema-v1.json` | PRD §7.3/14; M0-03 and M1-02 | No machine-readable contract schema, parser or validation tests. |
| `README.md`, `.env.example` | PRD §14; M3-08 | No installation/demo instructions or configuration example artifact. |
| `LICENSE` | PRD §14; OQ-15 | License/distribution undecided. |
| `.gitignore`, `pyproject.toml`, `uv.lock`, `.github/workflows/` | Architecture §5/8; M0-06/07 | Tooling is proposed, not configured or installed. |
| `packages/pact-core/`, `packages/pact-cli/`, `packages/pact-mcp/`, `packages/pact-api/` and their tests | PRD §14; M1/M3/M5 | No source packages or package test directories. |
| `apps/demo-marketplace/`, `apps/web/` | PRD §14; M1-04/M5 | No seeded target or web app. |
| `integrations/codex-skill/SKILL.md`, `integrations/github/` | PRD §14; M3-05/M5 | Existing engineering skills do not supply these product integrations. |
| `fixtures/authorization-benchmark/`, `infra/docker/`, `infra/migrations/`, `scripts/`, root `tests/` | Proposed PRD/architecture/schema layouts | No fixtures, runner configuration, migrations, scripts or test harness. |

The short companion names in the PRD header are clarified by its §14 layout: architecture/security belong under `docs/`, where their canonical copies already exist. No separate root `architecture.md` or `security.md` delivery copy is present or required for this inventory.

## 5. Schema investigation

`docs/schema.md` is a substantial database specification titled **Database Schema, ERD, RLS & Migration Specification**. Its header and §0.6 explicitly nominate `docs/DATA_MODEL.md` as the single canonical destination. Its own relative links resolve from the current `docs/` location. The expected canonical file is absent, so the statement that `schema.md` is an "identical delivery copy" cannot be verified against another local file.

Content covers P0 SQLite/local persistence and P1 hosted PostgreSQL, RLS, composite foreign keys, migrations, approval transactions, evidence lineage and future tests. It expressly says tables, policies and migrations are not implemented. It also introduces storage-specific `CONVERTED` draft status and proposes ADR-0010; these are design inputs requiring review, not accepted domain behavior or an existing ADR.

For current intake, **read `docs/schema.md` as the available database draft**, while retaining `docs/DATA_MODEL.md` as its declared but missing canonical destination. It does not replace `docs/contracts/schema-v1.json`: a database specification and a contract DSL schema serve different purposes.

Recommended later reconciliation: move the preserved draft to `docs/DATA_MODEL.md`, adjust its delivery-copy wording, and update references after the owner chooses the canonical path. Alternatively, an owner may choose `docs/schema.md` and reconcile the expected paths explicitly. **M0-01 performs neither a move nor a duplicate copy**, preserves the original bytes, and does not mark M0-09 complete.

## 6. Discrepancy register

| ID | Observation / source | Disposition and impact |
|---|---|---|
| `ISS-0001` | `docs/schema.md` header/§0 declare absent `docs/DATA_MODEL.md`. | DOCS / LOW; canonical-path decision pending. Actual available draft identified in §5; no duplicate source of truth created. |
| `ISS-0002` | Architecture header calls itself an `architecture.md` delivery copy and cites AGENTS v1.0.0; actual canonical file is `docs/ARCHITECTURE.md` and AGENTS is v1.0.2. | DOCS / LOW; editorial metadata correction remains pending; current files take precedence over stale metadata. |
| `ISS-0003` | Architecture §7 points status to `docs/ROADMAP.md` or an issue tracker; AGENTS §12 and todo §9 establish root `todo.md` as canonical. | DOCS / LOW; use `todo.md` under existing precedence; later align architecture wording without creating another status ledger. |
| `ISS-0004` | Architecture §2.4 identifies `TB-08` as Human → Approval; Security §3.3 identifies it as Browser → Hosted API. | DOCS / MEDIUM; owner/reviewer must reconcile boundary identity before relying on shared traceability; neither boundary is implemented. |
| `ISS-0005` | Security §15 includes mismatched AC mappings: SEC-T008 (DENY 500/timeout) → AC-016 (safe 404); SEC-T010 (safe denial) → AC-005 (patched app); SEC-T012 (budgets) → AC-015 (redirect); SEC-T025 (repeatability) → AC-017 (ALLOW 500). | DOCS / MEDIUM; review exact mappings during M0-02/M0-08 without rewriting PRD acceptance criteria. No tests or security verdicts are asserted. |
| Snapshot correction | Original todo §1/footer said filesystem NOT INSPECTED and listed only preparation documents. | Resolved within M0-01 tracker update; original initialization journal remains intact. |
| Interpretation clarification | Root `skill.md`, three engineering manifests and planned product `integrations/codex-skill/SKILL.md` are distinct. | No rename needed; existing text skills do not establish product MCP tools, tests or runtime approval authority. |

The first five issues record newly observed documentation inconsistencies, not duplicate implementation tasks. Their presence does not prevent M0-01 from satisfying its own DoD, which requires recording discrepancies rather than settling later design decisions. Existing architecture/security/schema documents remain unchanged.

## 7. Pending decision register and dependencies

All decisions below remain **pending**. No reviewer identity, acceptance, runtime approval or target authorization has been fabricated. The operational ADR register remains [todo.md §4](../todo.md#4-approval-and-architecture-decision-register).

| Decision | Current evidence / affected stage | Required owner action |
|---|---|---|
| Canonical database document path | Only `docs/schema.md` exists; M0-09 depends on M0-03/05. | Choose preserved move to `docs/DATA_MODEL.md` or explicit reference revision. |
| Workflow governance / named owners | Workflow adoption checklist and PRD §22 owner/reviewer roles remain unfilled. | Identify product/engineering/security reviewers and review process for later gated work. Direct M0-01 authorization is already supplied. |
| Git baseline | No Git initialization, branch or commit. | Authorize initialization/branch/commit policy separately; version-control evidence remains unavailable. |
| ADR-0001 / OQ-02 | No file; M0-03, then domain/schema work. | Review exact restricted DSL, canonical serialization/hash and DENY semantics. |
| ADR-0002 / OQ-03,06 | No file; M0-04, then fixtures/runner. | Review synthetic authentication, authorized target, isolation, budgets, redirects and no-disclosure/404 assertions. |
| ADR-0003 / OQ-04,14 | No file; M0-05, then trusted approval. | Review real human identity, digest/version/scope receipt binding, replay controls and immutable history. |
| ADR-0004 / PRD §8.3 | No file; M0-06/07. | Decide package layout, dependency/tooling versions, locking, licensing and OS support before build setup. |
| ADR-0005 / OQ-05 | No file; M3 integration. | Review MCP/host boundary and nonprivileged product tool surface. |
| ADR-0006 / OQ-10 | No file; M2 provider work. | Review provider/model configuration, consented data classes, egress and no-second-provider mode. |
| ADR-0007 / OQ-08,13; OQ-09 | No file; M5 hosted work. | Decide private-runner/control-plane trust, queue/storage and geography/compliance based on need. |
| ADR-0008 / OQ-11 | No file; CI integration. | Review signed events/audit and optional merge enforcement. |
| ADR-0009 / OQ-12 | No file; M6 evaluation. | Approve independent methodology and measured claims. |
| Proposed ADR-0010 | Mentioned only in schema §1/11; no file or canonical WBS task added. | Decide whether to track a hosted RLS proposal in later approved work; do not treat it as accepted or renumber ADR-0001–0009. |
| OQ-01,07,15 | Brand, reviewed policy/test migration and license remain open. | Resolve at the relevant policy-change/publication stage; not blockers for inventory. |

No pending design decision blocks local inventory. Git absence is a recorded provenance limitation, not an invented dependency for M0-01. No runtime grant exists or is needed for document checks.

After verified M0-01 completion, **M0-02, M0-03 and M0-06 are dependency-ready**. Recommended next task is **M0-02**, reviewing the existing security draft rather than assuming it is approved. M0-04 waits for M0-02; M0-05 waits for M0-02/03; M0-07 waits for M0-06; M0-08 waits for M0-03/04/05; M0-09 waits for M0-03/05. No other task was started.

## 8. Verification and evidence

Evidence entry: `EV-0001` in `todo.md`. Local check transcripts and the original manifest/diff are retained outside the project at:

```text
C:\Users\user\AppData\Local\Temp\PACT-M0-01-05ddfba0a36646219e21bd7ca1ab3cb2\
```

Temporary artifacts are local session evidence, not committed or durable release evidence. The substantive inventory, conclusions and results are recorded in project documentation. Repository-history diff/commit/PR evidence is unavailable because Git is not initialized; a local no-index comparison against the saved tracker provides a reviewable document diff.

Executed discovery commands:

```powershell
Get-ChildItem -LiteralPath . -Force -Recurse | Select-Object FullName, PSIsContainer, Length
git rev-parse --is-inside-work-tree
git status --short --branch
```

The verification script checks hidden-entry inventory, expected present/absent paths, relative Markdown file targets, 71 unique canonical tasks matching architecture IDs, exact milestone counts, original task/DoD and ADR rows, preservation of the initialization journal, unchanged original file hashes except `todo.md`, and absence of unauthorized extra files/directories. It exercises its path/link failure detection on nonexistent synthetic paths without creating files or making network requests.

Executed document-check and review commands (the evidence directory contains the temporary script and baseline):

```powershell
& 'C:\Users\user\AppData\Local\Temp\PACT-M0-01-05ddfba0a36646219e21bd7ca1ab3cb2\verify.ps1' -ProjectRoot 'D:\Dev\PACT' -EvidenceDirectory 'C:\Users\user\AppData\Local\Temp\PACT-M0-01-05ddfba0a36646219e21bd7ca1ab3cb2' -ExpectedStatus IN_REVIEW
git diff --no-index -- 'C:\Users\user\AppData\Local\Temp\PACT-M0-01-05ddfba0a36646219e21bd7ca1ab3cb2\todo.before.md' 'D:\Dev\PACT\todo.md'
& 'C:\Users\user\AppData\Local\Temp\PACT-M0-01-05ddfba0a36646219e21bd7ca1ab3cb2\verify.ps1' -ProjectRoot 'D:\Dev\PACT' -EvidenceDirectory 'C:\Users\user\AppData\Local\Temp\PACT-M0-01-05ddfba0a36646219e21bd7ca1ab3cb2' -ExpectedStatus DONE
```

| Check | Actual result |
|---|---|
| Initial inventory / Git probes | 11 original Markdown files, six directories; Git probes both report not a repository. No Git initialization performed. |
| First temporary checker attempt | Failed converting the existing bold `**71**` TOTAL cell to integer. This was a checker parser error, not a product test result. Corrected only the temporary parser to strip numeric Markdown emphasis. |
| Checker rerun, `IN_REVIEW` | PASS: 12 files/six directories; exact allowed file set; all ten untouched originals match their SHA-256 baseline; 23 expected missing paths absent. |
| References / negative cases | PASS: 25 local Markdown file links resolve; nonexistent synthetic and missing canonical link targets correctly detected, with no files created or network requests. Prose/backtick planned paths are reported gaps rather than live links. |
| Tracker consistency | PASS: 71 unique task IDs match the architecture WBS; 70 NOT_STARTED plus M0-01 IN_REVIEW; all board totals/progress match; other task rows and original M0-01 scope/DoD unchanged. |
| History / authority | PASS: initialization journal and nine unapproved ADR rows preserved; five discrepancy IDs and one EV-0001 evidence row recorded. |
| Local document review | Codex reviewed the inventory and no-index tracker diff. Git's difference exit status is expected for changed files; this is not a repository commit, human approval or ADR acceptance. |
| Final `DONE` verification | PASS: all file/path/link/negative/preservation checks repeated successfully; M0-01 DONE and 70 other tasks NOT_STARTED; M0 1/9 (11.1%) and total 1/71 (1.4%) agree with ledger. |

Transcripts: `checks-in_review.txt` and `checks-done.txt` in the evidence directory. The saved before/after tracker comparison is `todo.diff`; the initial file hashes are `before.json`. These are temporary local evidence, with substantive results preserved here and in EV-0001. Final checks were rerun after recording these results.

Application tests, schema validation tests, linters, type checks and security tests are **NOT RUN**: this task changes documentation only and the project has no configured implementation/test toolchain. No dependencies were installed to manufacture such checks. No runtime verdict or release gate is claimed. M0-01's task-specific DoD requires checked paths, recorded discrepancies and truthful claims; it prescribes no additional ADR acceptance or independent human security sign-off for this inventory. No missing approval blocks this documentation task.
