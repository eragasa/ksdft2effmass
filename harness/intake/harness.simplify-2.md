# Harness simplification round two intake

**Status:** Active coordinating parent. Six ordered work packages are decomposed and inactive; implementation has not started and automatic successor activation remains disabled.

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

The active parent coordinates six separately activated child Tasks. During the
hybrid migration, the existing harness-simplification chain retains compatible
selection state while SQLite owns the new structured control state. Decomposition
does not activate the first child, and child completion does not activate its
successor automatically.

| Order | Task | Work package |
| ---: | --- | --- |
| 1 | `harness.simplify-2.control-decomposition` | R2.1 — control decomposition |
| 2 | `harness.simplify-2.adapter-retirement` | R2.2 — adapter retirement |
| 3 | `harness.simplify-2.python-conformance-decomposition` | R2.3 — Python conformance decomposition |
| 4 | `harness.simplify-2.resource-decomposition` | R2.4 — resource and routing decomposition |
| 5 | `harness.simplify-2.wire-validation-decomposition` | R2.5 — wire validation decomposition |
| 6 | `harness.simplify-2.validation-retirement` | R2.6 — validation consolidation and replay retirement |

Each child has `explicit_activation_required: true`. The parent retains shared
contract-preservation requirements, exclusions, final integration review, and
explicit human acceptance; the children own only their bounded implementation
packages.

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

## Maintained command surface

The target command vocabulary is approximately:

```text
harness inspect
harness validate
harness project
harness task
harness evidence
```

Representative invocation:

```bash
python/.venv/bin/python -m ksdft2effmass.harness inspect
python/.venv/bin/python -m ksdft2effmass.harness validate
python/.venv/bin/python -m ksdft2effmass.harness project
```

Each command calls maintained ActionObjects. Routine inspection must not require agents to assemble inline Python or generated shell fragments.

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
| 1 | `python/src/ksdft2effmass/harness/pi/local/control.py` | Decompose immediately. |
| 2 | `python/src/ksdft2effmass/harness/pi/local/adapters.py` | Retire unused adapters, then split survivors. |
| 3 | `python/src/ksdft2effmass/harness/pi/evidence/python_conformance.py` | Decompose around one parsed test-module model. |
| 4 | `python/src/ksdft2effmass/harness/pi/resources.py` | Separate records, manifests, resolution, refresh, and skill closure. |
| 5 | `python/src/ksdft2effmass/harness/pi/validation.py` | Replace centralized wire dispatch with domain codecs. |
| Later | `python/src/ksdft2effmass/operators/serialization.py` | Separate production refactor. |
| Later | `python/src/ksdft2effmass/workflows/cpn/execution.py` | Separate CPN contract audit. |
| Later | `python/src/ksdft2effmass/provenance/serialization.py` | Separate provenance codec audit. |

### R2.1 — Control decomposition

Target internal ownership:

```text
python/src/ksdft2effmass/harness/pi/local/control/
├── __init__.py
├── records.py
├── schema.py
├── ingestion.py
├── projections.py
├── sql_export.py
├── verification.py
└── migration.py
```

| Module | Responsibility |
| --- | --- |
| `records.py` | Immutable request, result, and configuration DataObjects. |
| `schema.py` | SQLite DDL, schema version, and connection initialization. |
| `ingestion.py` | Task, evidence, test, agent, skill, resource, and decision import. |
| `projections.py` | JSON, graph, manifest, inventory, and Markdown projections. |
| `sql_export.py` | Deterministic SQL recovery export. |
| `verification.py` | Integrity, foreign keys, semantic digest, and reconstruction agreement. |
| `migration.py` | Thin orchestration only. |

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

### R2.2 — Adapter retirement

Before moving code, identify live consumers. Retire adapters that:

- have no live consumer;
- translate only between two generated projections; or
- preserve compatibility no archived input still needs.

Potential survivor ownership:

```text
python/src/ksdft2effmass/harness/pi/local/adapters/
├── __init__.py
├── tasks.py
├── ownership.py
├── resources.py
└── legacy_markdown.py
```

Deletion has priority over rearrangement. Do not introduce a generic adapter framework.

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

### R2.6 — Replay and H3 retirement

Retire `replay_current_validators.py`, H3-era resource gates, and nested validation routes where live-consumer analysis proves them obsolete. Replace them with:

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

Every maintained command uses:

```text
python/.venv/bin/python
```

The environment must support package imports, pytest, Ruff, mypy, Sphinx, wheel tests, and maintained harness CLIs without assuming that a root virtual environment, system Python, or ad hoc shell is interchangeable.

## Explicit exclusions

Do not include `operators`, `workflows/cpn`, `provenance`, or other production/scientific module decomposition. Do not implement telemetry. Do not add dependencies or change the lockfile. Do not perform scientific or external execution, protected actions, package publication, releases, scientific validation, or uncertainty quantification. Do not delete or rewrite retained historical control and evidence records.
