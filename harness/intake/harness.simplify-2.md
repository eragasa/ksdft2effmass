# Harness simplification round two intake

**Status:** Coordinating parent deferred to active R2.5 after R2.4 completed. R2.1–R2.4 are completed. R2.6 and R2.7 are inactive with `explicit_activation_required: false`, and automatic successor activation remains disabled.

**Task ID:** `harness.simplify-2`

## Goal

Make the harness simpler by consolidating authority, removing synchronization and replay machinery, and decomposing harness monoliths along cohesive contracts. The success metric is not total lines removed:

> Can a maintainer change one policy—Task persistence, evidence naming, resource resolution, or wire serialization—without editing an orchestration monolith or synchronizing unrelated representations?

This is a harness-only program. It does not include production refactors of operators, CPN execution, provenance serialization, or other scientific/package-source modules.

## Baseline already established

The completed SQLite-hybrid cutover established:

```text
harness/state/harness-control.sqlite3
harness/state/harness-control.sql
harness/state/projection-manifest.json
```

SQLite owns structured control state. JSON and Markdown are deterministic projections. Source code, tests, skills, agent prose, and narrative documentation remain ordinary files. Historical evidence identifiers remain aliases of semantic canonical identifiers. Runtime observations and telemetry remain outside the tracked control database.

Round two must preserve that accepted baseline rather than create another shadow model.

## Ordered Task decomposition

The active parent authorizes serial deterministic progression through the seven
child Tasks. During the hybrid migration, the existing harness-simplification
chain retains compatible selection state while SQLite owns the new structured
control state.

| Order | Task | Work package | Status |
| ---: | --- | --- | --- |
| 1 | `harness.simplify-2.control-decomposition` | R2.1 — control decomposition | completed |
| 2 | `harness.simplify-2.adapter-retirement` | R2.2 — adapter retirement | completed |
| 3 | `harness.simplify-2.python-conformance-decomposition` | R2.3 — Python conformance decomposition | completed; HC01 resolved |
| 4 | `harness.simplify-2.resource-decomposition` | R2.4 — resource and routing decomposition | completed |
| 5 | `harness.simplify-2.wire-validation-decomposition` | R2.5 — wire validation decomposition | active |
| 6 | `harness.simplify-2.cli-consolidation` | R2.6 — maintained CLI consolidation under `python/src/cli/` | inactive |
| 7 | `harness.simplify-2.validation-retirement` | R2.7 — validation consolidation and replay retirement | inactive |

R2.3–R2.7 have `explicit_activation_required: false`. After the preceding
prerequisite is completed, the parent agent may explicitly transition to the
next child when no unresolved checkpoint, human-owned material choice, protected
action, or unresolved material finding exists. Only one child may be active at a time.
Background activation is prohibited, and
`automatic_successor_activation` remains `false`. Actual ambiguity or a
human-owned or protected boundary stops progression for human disposition.
Final parent acceptance remains a human decision.

Each child performs a complete vertical cutover of its owned subsystem: accepted
end-state contract, implementation in isolation, complete affected-data
migration, controlled parity, one cutover, and removal of the obsolete live path.
Old and new operational authorities do not remain live after cutover; temporary
compatibility is retained only when an accepted public contract requires it.

## Highest-leverage outcomes

| Priority | Candidate | Concrete outcome |
| ---: | --- | --- |
| 1 | SQLite-hybrid control plane | Preserve one authority for Tasks, graph state, evidence identities, test ownership, agents, skills, resources, and projections. |
| 2 | Evidence and test identity model | Preserve semantic evidence IDs, historical aliases, and consistent test modules, functions, and parameter IDs. |
| 3 | Maintained command surface | Replace generated Bash/Python fragments with a few stable commands backed by maintained ActionObjects. |
| 4 | Duplicated control records | Stop reproducing manually synchronized inventories, completion files, ownership envelopes, and generated state copies. |
| 5 | Legacy `.pi` runtime authority | Preserve `.pi` history while moving remaining live structured control under `harness/`. |
| 6 | Oversized harness modules | Split by cohesive contracts rather than arbitrary line counts. |
| 7 | Agent and skill routing | Use fewer durable roles, shared policy, and task-selected skills without duplicated prompt fragments. |
| 8 | Replay and H3 validation | Replace nested replay routes with one composable validation Action returning structured results. |
| 9 | Control versus observations | Keep tracked control SQLite separate from ignored observations SQLite. |
| 10 | Python environment | Use `python/.venv/bin/python` for maintained commands. |

## Maintained control generation

Maintained synchronization and verification use the same control-generation
logic:

```text
authoritative repository inputs
→ one private control-generation builder
→ complete candidate SQLite, SQL, manifest, and projection artifacts
```

This is a private build/publish separation inside the existing control subsystem,
not a framework or new public interface. `HarnessControlMigrator` uses the
builder, validates the candidate, and remains the sole publisher.
`HarnessControlVerifier` uses the same builder, compares the candidate with
maintained artifacts, reports differences, and performs no maintained writes.
Verification therefore detects authoritative-source drift even when maintained
SQLite and maintained SQL agree with each other. Temporary verification artifacts
are removed after success or failure. There is no migrator check mode, second
construction algorithm, public builder Action, incremental updater, watcher,
daemon, event-log authority, or second database writer. Existing public imports
and execute signatures remain unchanged.

R2.3 establishes canonical evidence inputs, R2.4 establishes canonical resource
inputs, and existing canonical Task and graph inputs remain part of maintained
control construction. R2.6's synchronization command supplies those canonical
maintained inputs. R2.7 makes the verifier derive the same canonical input set
from repository-owned configuration. The verifier's source-aware guarantee is
limited to maintained canonical control state; it does not promise reproduction
of arbitrary noncanonical migration requests or alternate output locations.
Existing bounded compatibility for nondefault `HarnessControlMigrationRequest`
inputs remains unchanged unless separately authorized.

## Maintained command surface

The target command vocabulary is approximately:

```text
harness inspect
harness validate
harness project
harness task
harness evidence
```

Every maintained live CLI script and entry point belongs directly under
`python/src/cli/`; exact filenames and command grammar remain owned by R2.6.
Representative invocation has the form:

```bash
python/.venv/bin/python python/src/cli/<command>.py <explicit arguments>
```

Each command calls maintained ActionObjects under `python/src/ksdft2effmass/`. Routine inspection must not require agents to assemble inline Python or generated shell fragments.

## Process-record retirement

Preserve current records as history, but do not reproduce per-Task copies of:

- ownership JSON;
- completion JSON;
- parent-verification Markdown;
- test-evidence inventory JSON;
- node-migration JSON;
- review Markdown;
- command transcripts; or
- repeated chain synchronization records.

A Task, graph relationships, lifecycle events, and referenced evidence should ordinarily be sufficient.

## Legacy authority cutover

After the SQLite cutover:

- preserve historical `.pi/tasks`, chains, checkpoints, decisions, and evidence;
- stop treating legacy projections as live operational authority;
- keep maintained structured runtime state under `harness/`;
- retain exact human decisions where required; and
- delete compatibility readers only after proving that no live consumer remains.

This must be a bounded cutover, not an indefinitely maintained shadow system.

## Harness module priorities

The two maintained `pi` trees have distinct ownership. `harness/pi/` contains
manifest-addressed resources, schemas, fixtures, validation scripts, skills, and
documentation. Importable Python implementation is under
`python/src/ksdft2effmass/harness/pi/`. Paths below identify the owning tree
explicitly; neither tree replaces the other.

| Priority | Module | Disposition |
| ---: | --- | --- |
| 1 | `python/src/ksdft2effmass/harness/pi/local/control.py` | Completed R2.1 decomposition into cohesive control owners. |
| 2 | `python/src/ksdft2effmass/harness/pi/local/adapters.py` | Completed R2.2 audit and relocation of all nine adapters into five contract-specific modules. |
| 3 | `python/src/ksdft2effmass/harness/pi/evidence/python_conformance.py` | Decompose around one parsed test-module model. |
| 4 | `python/src/ksdft2effmass/harness/pi/resources.py` | Separate records, manifests, resolution, refresh, and skill closure. |
| 5 | `python/src/ksdft2effmass/harness/pi/validation.py` | Replace centralized wire dispatch with domain codecs. |
| Later | `python/src/ksdft2effmass/operators/serialization.py` | Separate production refactor. |
| Later | `python/src/ksdft2effmass/workflows/cpn/execution.py` | Separate CPN contract audit. |
| Later | `python/src/ksdft2effmass/provenance/serialization.py` | Separate provenance codec audit. |

### R2.1 — Control decomposition

R2.1 is completed. Its resulting internal ownership separates project-neutral
read-only SQLite Task-state inspection from repository-specific control
construction:

```text
python/src/ksdft2effmass/harness/pi/dbcontrol/
├── __init__.py
├── database.py
├── documents.py
├── files.py
└── inspection.py

python/src/ksdft2effmass/harness/pi/local/dbcontrol/
├── __init__.py
├── constants.py
├── database.py
├── encoding.py
├── ingestion.py
├── migration.py
├── projections.py
├── records.py
├── schema.py
└── verification.py
```

| Owner | Responsibility |
| --- | --- |
| Generic `dbcontrol/database.py` | Project-neutral, read-only SQLite Task lifecycle queries. |
| Generic `dbcontrol/documents.py`, `files.py`, and `inspection.py` | Private bounded Task-state document parsing, file inspection, and reconciliation moved from the superseded holder modules. |
| `task_state.py` | Retained public `TaskStateInspector` identity and execute signature, with private delegation to generic `dbcontrol`; no new public API. |
| Local `dbcontrol/records.py` and `schema.py` | Immutable migration and verification records plus the project-local SQLite DDL and schema version. |
| Local `dbcontrol/database.py` and `encoding.py` | Project-local connection, reconstruction, semantic-identity, deterministic SQL, hashing, and encoding mechanics. |
| Local `dbcontrol/ingestion.py` | Repository-specific Task, evidence, test, agent, skill, resource, and decision import. |
| Local `dbcontrol/projections.py` | Repository-specific JSON, graph, manifest, inventory, and Markdown projections. |
| Local `dbcontrol/verification.py` and `migration.py` | Thin verification and migration orchestration over the project-local owners. |

The required dependency direction is `local.dbcontrol` to generic `dbcontrol`
and `task_state` to generic `dbcontrol`. Generic `dbcontrol` must not depend on
`local.dbcontrol`, and `task_state` must not depend on `local.dbcontrol`.

Keep the public migration surface small:

```python
HarnessControlMigrationRequest
HarnessControlMigrationResult
HarnessControlMigrator
```

Also preserve the existing public verification exports
`HarnessControlVerificationResult` and `HarnessControlVerifier`. The three-item
migration surface does not authorize removing or privatizing those verification
contracts. Do not turn every internal step into a public ActionObject.

### R2.2 — Adapter audit and decomposition

R2.2 is completed. It audited all nine public adapters, relocated all nine
implementations into five contract-specific modules, retained the compatibility
facade, and preserved all nine public imports and execute signatures. It removed
no adapter and introduced no generic adapter framework.

### R2.3 — Python conformance decomposition

Parse each Python source once into one immutable internal representation:

```text
Python source
→ AST parse once
→ PythonTestModuleModel
→ independent rule evaluators
→ ordered findings
→ PythonConformanceResult
```

Target internal ownership:

```text
python/src/ksdft2effmass/harness/pi/evidence/python_conformance/
├── __init__.py
├── model.py
├── parser.py
├── naming.py
├── documentation.py
├── parameterization.py
├── ownership.py
├── migration.py
└── validation.py
```

Rule evaluators should remain close to pure functions:

```python
validate_naming(module)
validate_documentation(module)
validate_parameterization(module)
validate_ownership(module, ownership)
validate_migration(module, migration_map)
```

### R2.4 — Resource decomposition

Target internal ownership:

```text
python/src/ksdft2effmass/harness/pi/resources/
├── __init__.py
├── records.py
├── manifests.py
├── resolution.py
├── refresh.py
└── skill_closure.py
```

Dependency direction:

```text
records
   ↑
manifests
   ↑
resolution / refresh / skill_closure
```

Records must not import operational Actions. Existing public Actions remain stable.

### R2.5 — Wire validation decomposition

Prefer explicit domain codecs over a magical registry:

```text
python/src/ksdft2effmass/harness/pi/wire/
├── records.py
├── canonical_json.py
├── checkpoints.py
├── tasks.py
├── resources.py
├── human_review.py
└── dispatch.py
```

Dispatch routes by wire kind. Domain codecs own their field mappings. The registry must not accumulate domain construction logic or expose every codec publicly.

### R2.6 — Maintained CLI consolidation

Inventory every maintained live Python CLI under `python/src/ksdft2effmass/`,
`harness/`, and `.pi/`. Move the final thin scripts and entry points directly
under `python/src/cli/`, keep reusable behavior with its ActionObject owners under
`python/src/ksdft2effmass/`, migrate every live consumer, and retire obsolete
wrappers only after command/API agreement. Retain historical evidence scripts
unchanged, and do not add installed console-script entry points or change package
discovery.

### R2.7 — Replay and H3 retirement

Extract the narrow private control-generation builder described above, make the
verifier derive the canonical maintained inputs from repository-owned
configuration, and retire `replay_current_validators.py`, H3-era resource gates,
and nested validation routes where live-consumer analysis proves them obsolete.
Replace the repository-wide validation surface with:

```python
ValidateHarness.execute(request) -> HarnessValidationResult
```

The result contains named checks, statuses, findings, and durations. One CLI renders it. No validator invokes another CLI and parses its output.

## Agent and skill routing

The durable harness roles should converge toward:

- implementation;
- verification;
- documentation; and
- read-only integration review.

Architecture is ordinarily a task-selected skill rather than a permanently invoked role. Shared rules live once in root or scoped instructions or a reusable skill. Agent records contain only role, authority boundary, write boundary, essential responsibilities, stop conditions, and output contract.

Each Task dispatch selects only the skills needed for that assignment and names
the exact repository paths, workspace and baseline, required checks, preserved
contracts, review boundary, and handoff fields. Routine reconnaissance uses at
most one bounded scout followed by one focused reviewer when independent review
is materially useful; do not launch parallel deep reviews for ordinary path or
state inspection.

## Control and observation storage

Keep the stores explicit:

```text
harness/state/harness-control.sqlite3
.pi/cache/harness-observations.sqlite3
```

The tracked database contains definitions and accepted state. The ignored database may later contain validation runs, test results, tool calls, durations, retries, token or cost measurements, and telemetry events—but not under this Task.

## Python environment

Every maintained command uses the repository interpreter and a script under the
single CLI root:

```text
python/.venv/bin/python python/src/cli/<command>.py
```

The environment must support package imports, pytest, Ruff, mypy, Sphinx, wheel tests, and maintained harness CLIs without assuming that a root virtual environment, system Python, or ad hoc shell is interchangeable.

## Explicit exclusions

Do not include `operators`, `workflows/cpn`, `provenance`, or other production/scientific module decomposition. Do not implement telemetry. Do not add dependencies or change the lockfile. Do not perform scientific or external execution, protected actions, package publication, releases, scientific validation, or uncertainty quantification. Do not delete or rewrite retained historical control and evidence records.
