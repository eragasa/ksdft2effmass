# Operator-Record DataObject/ActionObject Refactor Task

## Status

Closed and accepted. Human final acceptance was approved on 2026-07-30 after parent verification. Later operator-record corrections are recorded prospectively in `.pi/tasks/operator-record-validation-correction.md`, accepted on 2026-08-03; they do not erase this task's original chronology or accepted historical evidence. Scientific validation has not been performed and remains outside both tasks.

## Resolved repository roots

Repository evidence identifies exactly one authoritative Python source root:

- `python/pyproject.toml`: `[tool.setuptools] package-dir = { "" = "src" }`.
- `python/pyproject.toml`: `[tool.setuptools.packages.find] where = ["src"]`, `include = ["ksdft2effmass*"]`.
- `python/pyproject.toml`: pytest `testpaths = ["tests"]`.
- `python/pyproject.toml`: Ruff `src = ["src", "tests"]`.
- `python/pyproject.toml`: mypy `files = ["src", "tests"]`.
- `docs/conf.py`: prepends `../python/src` to `sys.path` for autodoc.
- Repository layout: package files exist under `python/src/ksdft2effmass/`; tests exist under `python/tests/`.
- Current imports use `ksdft2effmass` as the public package, supplied by `python/src`.

Therefore:

- Python project root for commands: `python/`.
- Python source root: `python/src/`.
- Operator package path: `python/src/ksdft2effmass/operators/`.
- Python test root: `python/tests/`.
- Object-test convention: `python/tests/ksdft2effmass/<package>/test__<ObjectName>.py`.
- Operator-record object-test hierarchy: `python/tests/ksdft2effmass/operators/`.
- Genuine production Workflow test convention: `python/tests/ksdft2effmass/workflows/test__<WorkflowName>.py`.
- Technical integration-test convention: `python/tests/ksdft2effmass/integration/test__<IntegrationName>.py`.
- Pytest discovery uses configured `testpaths = ["tests"]` and does not override `python_files`, so pytest's default `test_*.py` pattern discovers these filenames beneath `python/tests/`.

If future evidence conflicts with this, pause and request a human decision instead of choosing a root silently.

## Objective

Refactor finite operator records so represented data, Hermiticity analysis, and serialization follow the repository DataObject/ActionObject architecture without unrelated cleanup.

## Accepted architecture source

The root `AGENTS.md` is authoritative for global architectural policy. Focused references are:

- `.pi/skills/design-data-action-objects/references/data-action-architecture.md`
- `.pi/skills/develop-operator-records/references/operator-record-architecture.md`

The human-approved architecture decision must be recorded in the Decision records section before implementation starts.

## Proposed architecture to present at Checkpoint 1

Target package structure:

```text
python/src/ksdft2effmass/operators/
├── __init__.py
├── records.py
├── hermiticity.py
└── serialization.py
```

Object contract:

| Object | Category | Responsibility |
| --- | --- | --- |
| `StateSpace` | DataObject | Finite state-space metadata |
| `Basis` | DataObject | Ordered basis metadata |
| `Geometry` | DataObject | Cell and boundary metadata |
| `EnergyReference` | DataObject | Energy-zero metadata |
| `OperatorRecord` | DataObject | Matrix and comparison-critical metadata |
| `HermiticityResult` | ResultObject | Immutable Hermiticity result |
| `HermiticityAnalyzer` | ActionObject | Hermiticity analysis and enforcement |
| `OperatorRecordJsonSerializer` | ActionObject | Versioned JSON-compatible serialization |

Architectural decisions requiring human approval:

- `OperatorRecord` contains represented data only.
- Hermiticity tolerance belongs to `HermiticityAnalyzer`.
- Hermiticity results are returned as `HermiticityResult`.
- Serialization belongs to `OperatorRecordJsonSerializer`.
- Schema-version and complex-matrix mechanics belong to the serializer.
- Geometry validation belongs to `Geometry`.
- State-space validation belongs to `StateSpace`.
- Exact equality belongs to the DataObject.
- Approximate or physically aligned comparison is a separate future ActionObject.
- The public API is exported from `ksdft2effmass.operators`.
- Sphinx documentation and tests are required parts of completion.

Hermiticity criterion:

$$
\varepsilon_{\mathrm H}
=
\max_{i,j}
\left|
H_{ij}-H_{ji}^{*}
\right|,
$$

accepted when $\varepsilon_{\mathrm H}\leq\tau$ for analyzer tolerance $\tau$.

## Public API replacement

These former `OperatorRecord` methods are replaced:

```python
record.hermiticity_residual()
record.is_hermitian()
record.require_hermitian()
record.to_dict()
OperatorRecord.from_dict(...)
```

with:

```python
analyzer = HermiticityAnalyzer(tolerance=...)
result = analyzer.execute(record)
analyzer.require(record)

serializer = OperatorRecordJsonSerializer()
text = serializer.serialize(record)
restored = serializer.deserialize(text)
```

## Dependency graph

```text
Architecture analysis
    ↓
Human architecture approval
    ↓
Implementation
    ↓
Tests ∥ Sphinx documentation
    ↓
Integration review
    ↓
Human resolution of material findings, if any
    ↓
Parent verification
    ↓
Human final acceptance
```

Implementation, tests, and documentation must not all begin simultaneously in a shared worktree. Tests and documentation may be designed from the approved public contract, but they must not run validation against partially written production modules.

## Subagent routing and ownership

1. Architecture: `ksdft2effmass.ksdft2effmass-architecture`
   - read-only;
   - establishes DataObject boundaries, ActionObject boundaries, ResultObject boundaries, package structure, public API, validation invariants, serialization schema, compatibility policy, Rust-compatibility implications, and unresolved decisions.
2. Human approval gate
   - parent pi presents the architecture analysis to the human PI;
   - implementation cannot begin until approval or correction is recorded in this task file;
   - timeout, unavailable human, or absent response leaves the chain blocked.
3. Implementation: `ksdft2effmass.ksdft2effmass-implementation`
   - owns `python/src/ksdft2effmass/operators/`;
   - owns all source-code documentation in those Python modules, including module docstrings, class docstrings, method docstrings, field and invariant documentation, exception documentation, and examples embedded in source docstrings;
   - loads `design-data-action-objects` and `develop-operator-records`.
4. Tests: `ksdft2effmass.ksdft2effmass-tests`
   - owns `python/tests/ksdft2effmass/operators/` for operator-record object tests beneath the configured test root `python/tests/`;
   - tests only the approved public contract and documented invariants;
   - must not depend unnecessarily on private implementation details;
   - does not own `python/tests/ksdft2effmass/workflows/` or `python/tests/ksdft2effmass/integration/` unless parent pi explicitly assigns those non-overlapping files;
   - must not add `__init__.py` files to test directories unless established pytest import mode requires them; unresolved uncertainty escalates to the human PI.
5. Documentation: `ksdft2effmass.ksdft2effmass-documentation`
   - owns `docs/`;
   - responsible for conceptual Sphinx documentation, generated API pages, serialization specification, DataObject/ActionObject explanation, mathematical and scientific conventions, examples, toctree integration, and warning-as-error Sphinx builds;
   - must not edit Python source docstrings unless pi explicitly transfers ownership after implementation.
6. Integration review: `ksdft2effmass.ksdft2effmass-integration-reviewer`
   - read-only;
   - reports findings with exact file and line references;
   - does not silently repair findings.
7. Parent pi
   - owns final integration, combined verification, uncertainty routing, and presentation to the human PI;
   - no subagent may declare the overall task complete.

## Nested test organization

Object tests must mirror the public package hierarchy beneath the configured test root:

```text
python/tests/ksdft2effmass/<package>/test__<ObjectName>.py
```

Operator-record object tests use:

```text
python/tests/ksdft2effmass/operators/test__<ObjectName>.py
```

Create one principal test module for each public object:

```text
python/tests/ksdft2effmass/operators/test__StateSpace.py
python/tests/ksdft2effmass/operators/test__Basis.py
python/tests/ksdft2effmass/operators/test__Geometry.py
python/tests/ksdft2effmass/operators/test__EnergyReference.py
python/tests/ksdft2effmass/operators/test__OperatorRecord.py
python/tests/ksdft2effmass/operators/test__HermiticityResult.py
python/tests/ksdft2effmass/operators/test__HermiticityAnalyzer.py
python/tests/ksdft2effmass/operators/test__OperatorRecordJsonSerializer.py
```

Each module must primarily test the public contract of the object named in the filename. Place cross-object behavior with the ActionObject that owns the operation:

- Hermiticity execution and enforcement belong in `test__HermiticityAnalyzer.py`.
- JSON serialization, deserialization, malformed payloads, schema validation, and round trips belong in `test__OperatorRecordJsonSerializer.py`.
- Matrix ownership, provenance immutability, exact equality, and intrinsic record invariants belong in `test__OperatorRecord.py`.

Do not create broad dumping-ground modules such as `test_records.py`, `test_operators.py`, `test_utils.py`, or `test_misc.py`.

Workflow tests are reserved for genuine concrete production Workflow objects:

```text
python/tests/ksdft2effmass/workflows/test__<WorkflowName>.py
```

Technical integrations that are not domain workflows use:

```text
python/tests/ksdft2effmass/integration/test__<IntegrationName>.py
```

Examples of technical integrations include public package imports, JSON interoperability, filesystem boundaries, command-line behavior, Sphinx autodoc imports, and future Python/Rust schema compatibility. Technical integration tests do not require production Workflow objects.

For the current operator-record refactor, do not create an `OperatorRecordWorkflow` for:

```text
construct -> Hermiticity analysis -> serialize -> deserialize
```

These operations remain owned by `OperatorRecord`, `HermiticityAnalyzer`, and `OperatorRecordJsonSerializer`. A complete technical smoke test, if genuinely needed and explicitly assigned, belongs under `python/tests/ksdft2effmass/integration/test__<IntegrationName>.py` and must not duplicate object-level tests.

Do not silently move the repository's global test root. If pytest configuration later excludes `test__<ObjectName>.py` or the integration/workflow routing convention, pause for human intervention before changing global collection settings.

## Human authority

The human PI is the final authority for scientific meaning, mathematical conventions, public API decisions, serialization compatibility, architectural boundaries, backward compatibility, project scope, acceptance of unresolved validation failures, and final acceptance of the refactor.

No subagent may silently infer or make these decisions. Subagents may resolve routine implementation details only when the approved architecture and authoritative repository conventions determine the answer unambiguously.

## Required human checkpoints

### Checkpoint 1: Architecture approval

After architecture analysis, pause and present proposed DataObjects, ActionObjects, ResultObjects, package structure, public API, matrix convention, geometry convention, energy-reference semantics, serialization schema, backward-compatibility plan, Rust-compatibility implications, and unresolved questions.

Do not begin implementation until the human explicitly approves or corrects the proposal. A timeout, unavailable human, or absent response leaves the chain blocked.

### Checkpoint 2: Material uncertainty during execution

Immediately pause the affected branch when an agent encounters uncertainty that could materially change scientific semantics, architecture, public API, serialized data, compatibility, validation behavior, file ownership, or project scope. Independent branches may continue only if the pending decision cannot invalidate their work.

### Checkpoint 3: Integration findings

Pause after integration review if it finds an architectural deviation, public API incompatibility, scientific-convention mismatch, inconsistent schema, incomplete research documentation, failed completion gate, unexpected compatibility issue, conflict with existing user work, or required scope expansion. Present findings before assigning corrective work.

### Checkpoint 4: Final acceptance

After parent verification, present the complete implementation report to the human. Passing automated checks does not constitute human acceptance.

## Conditions requiring human intervention

Pause and request a decision if more than one plausible Python source root exists; more than one test root remains plausible; package configuration and repository layout disagree; pytest configuration excludes `test__<ObjectName>.py`; workflow-vs-integration routing conflicts with an existing control-plane rule, skill, agent responsibility, file-ownership boundary, chain dependency, test convention, or package layout; adding `__init__.py` files to test directories appears necessary but is not established by repository import mode; an established public import may break; preservation of the old import path is uncertain; existing serialized records may require migration; a schema-version decision is ambiguous; row-vector versus column-vector cell convention is not established; geometry or energy units are ambiguous; a validation rule may reject previously accepted research data; a DataObject/ActionObject boundary has multiple scientifically meaningful interpretations; Rust compatibility conflicts with established Python behavior; an agent needs to modify a file owned by another active agent; uncommitted user changes overlap the assigned work; a historical passed task conflicts with the new active task; a validation failure appears unrelated to this refactor; fixing a failure requires unrelated refactoring; removal of the old module could break compatibility; documentation and implementation express different conventions; a subagent wants to change the approved architecture; or a destructive or difficult-to-reverse action is proposed.

## Routine decisions

Agents may follow established repository conventions for formatting, import ordering, local variable naming, test parametrization, private-method placement within an approved owner, mechanical import updates under an approved compatibility plan, and docstring wording that does not alter scientific meaning. If evidence is incomplete or conflicting, the issue becomes material uncertainty.

## Uncertainty report format

For architectural or routing conflicts, including Workflow-vs-integration routing, use this format:

```markdown
## Decision required: <short conflict>

### Exact conflict

<the exact conflict>

### Files inspected

- `<file or source>`: <relevant fact>
- `<file or source>`: <relevant fact>

### Conflicting instructions

- `<instruction source>`: <instruction>
- `<instruction source>`: <instruction>

### Options

1. **<option>**
   - Consequence: <effect>

2. **<option>**
   - Consequence: <effect>

### Recommendation

<recommended option and concrete reason>

### Work status

- Safe to continue: <work>
- Blocked: <work>
```

For ordinary material uncertainties without conflicting instructions, use the same headings and state "No conflicting instruction found" under Conflicting instructions. Ask one coherent question at a time unless multiple decisions are inseparable. A missing human response leaves the affected work blocked.

## Decision records

Record every human decision in this section. Do not create a competing decision-log system unless the repository later adopts one.

Each decision must contain:

```text
Decision
Context
Options considered
Human resolution
Consequences
Affected files or agents
Date
```

Dependent agents must receive recorded decisions as authoritative context. They must not reopen an accepted decision unless new evidence creates a genuine conflict.

### Recorded decisions

#### Human checkpoint resolution: revision requested, implementation blocked

Decision
: Keep implementation blocked and return to read-only architecture analysis. This is not architecture approval.

Context
: The first architecture analysis completed, and the approval gate correctly blocked because no human architecture approval was recorded. The human PI accepted the previous proposal only in principle and required revisions before approval.

Options considered
: Option 1 — keep implementation blocked and revise the architecture proposal; Option 2 — proceed without recorded approval.

Human resolution
: Option 1. Prepare a revised architecture proposal addressing coherent `EnergyReference` semantics, explicit `Geometry.length_unit`, precise meaning or removal of `StateSpace.domain` and `StateSpace.codomain`, uniqueness requirements for `Basis.ordering`, owned C-contiguous row-major matrix storage, accurate API-level immutability claims, explicit numerical criterion for cell-rank validation, schema-version-1 field table, final canonical public API, and remaining human decisions. Incorporate compatibility directions: `ksdft2effmass.operators` is canonical; do not preserve top-level operator re-exports solely for hypothetical compatibility; do not add deprecated wrappers; treat schema version `1` as the first supported format; do not migrate hypothetical earlier payloads; escalate if actual released users, published examples, or persisted payloads are discovered.

Consequences
: Production implementation, test changes, Sphinx or research-documentation changes, public API changes, and serialization changes remain blocked. Read-only repository inspection, revised architecture analysis, presentation of options/recommendations, and control-plane state updates representing revision requested are allowed.

Affected files or agents
: `ksdft2effmass.ksdft2effmass-architecture` may run read-only analysis. `ksdft2effmass.ksdft2effmass-implementation`, `ksdft2effmass.ksdft2effmass-tests`, `ksdft2effmass.ksdft2effmass-documentation`, and `ksdft2effmass.ksdft2effmass-integration-reviewer` remain blocked until explicit approval of the revised proposal.

Date
: 2026-07-30

#### Human checkpoint outcome: final revisions required before approval

Decision
: Keep implementation blocked and prepare a final revised read-only architecture proposal. This is not architecture approval.

Context
: The revised architecture proposal was reviewed. The human PI accepted removal of `StateSpace.domain` and `StateSpace.codomain`, required `Geometry.length_unit`, unique basis labels, owned C-contiguous row-major `np.complex128` matrices, API-level immutability language, scale-invariant singular-value cell criterion, canonical `ksdft2effmass.operators` public API, removal of hypothetical top-level compatibility re-exports, no deprecated method wrappers, schema version `1` as the first supported wire format, no hypothetical migration support, and the proposed Workflow/test-routing policies. Two architectural corrections and strict schema behavior remain before approval.

Options considered
: Option 1 — approve the revised proposal as-is; Option 2 — require final revisions before approval.

Human resolution
: Option 2. Final proposal must simplify `EnergyReference` to `zero: str` and `unit: str` only; remove `value` from public constructor, schema version `1`, equality, codec payloads, documentation, and tests; use normalized-matrix convention with $E_{\mathrm{zero}}=0$ in the stored matrix coordinate system. For schema version `1`, require `OperatorRecord` to use an orthonormal basis by validating `basis.orthonormal is True`; nonorthogonal representations require a future overlap/metric design and generalized eigenproblems are outside this refactor. Place the cell-rank tolerance on `Geometry` as `LINEAR_INDEPENDENCE_RTOL: ClassVar[float] = 1.0e-12`, and reject zero or insufficiently independent cells using $\sigma_{\min} > r_{\mathrm{cell}}\sigma_{\max}$. Codec behavior for schema version `1` must be strict: require all fields, reject unknown fields at every level, reject booleans where integers or real numbers are required, reject nonfinite values, reject duplicate basis labels, reject `orthonormal=false` through `OperatorRecord`, and reject `energy_reference.value` as an unknown field.

Consequences
: Production implementation, test changes, Sphinx or research-documentation changes, public API changes, serialization changes, and architecture approval remain blocked. Only read-only repository inspection, final architecture proposal, presentation of options/recommendations, and control-plane state updates representing final revisions required are allowed.

Affected files or agents
: `ksdft2effmass.ksdft2effmass-architecture` may run read-only analysis. `ksdft2effmass.ksdft2effmass-implementation`, `ksdft2effmass.ksdft2effmass-tests`, `ksdft2effmass.ksdft2effmass-documentation`, and `ksdft2effmass.ksdft2effmass-integration-reviewer` remain blocked until explicit human approval of the final revised proposal.

Date
: 2026-07-30

#### Human architecture approval: final Checkpoint 1 proposal approved for implementation

Decision
: Approve the Final Checkpoint 1 Architecture Proposal for the operator-record refactor, subject to the binding clarifications in this decision. Implementation, test restructuring, and Sphinx documentation may proceed under this approved architecture.

Context
: The approved design establishes DataObjects for represented scientific data, ActionObjects for analysis and serialization, ResultObjects for action results, a strict schema-version-1 wire format, an orthonormal-basis restriction, explicit geometry and energy units, deterministic owned matrix storage, the canonical `ksdft2effmass.operators` public API, no artificial `OperatorRecordWorkflow`, mirrored object-level test organization, and explicit technical-integration routing. The architecture has undergone read-only review and two revision cycles.

Options considered
: Preserve behavior on `OperatorRecord`; separate represented data from analysis and serialization; preserve hypothetical compatibility wrappers and top-level exports; establish a clean canonical API without hypothetical compatibility; allow ambiguous energy offsets; require a normalized energy-zero convention; allow nonorthogonal bases without an overlap matrix; restrict schema version 1 to orthonormal bases; allow permissive payload decoding; require strict versioned payload validation.

Human resolution
: Approve the architecture with these binding clarifications. Use `StateSpace(identifier: str, kind: str, dimension: int)` with no `domain` or `codomain`. Use `Basis(identifier: str, kind: str, ordering: tuple[str, ...], orthonormal: bool)` with string, nonempty, unique labels and exact Boolean validation; schema version 1 `OperatorRecord` requires `basis.orthonormal is True`. Use `Geometry(system, cell, boundary_conditions, coordinate_convention, length_unit)` with row-vector cell convention, every component in `length_unit`, and `LINEAR_INDEPENDENCE_RTOL: ClassVar[float] = 1.0e-12`; accept only when `sigma_max > 0` and `sigma_min > LINEAR_INDEPENDENCE_RTOL * sigma_max`. Use `EnergyReference(zero: str, unit: str)` only; the named reference has numerical value zero in the stored matrix coordinate system, and no value or unapplied offset is stored. Use owned, copied, finite, square, C-contiguous row-major `np.complex128` matrices, marked non-writeable through the public API; describe this as API-level immutability and make `OperatorRecord` explicitly unhashable. Use `HermiticityResult(residual: float, tolerance: float)` with `is_hermitian` as a derived property, not an independently supplied field. Use the Hermiticity criterion `epsilon_H = max_ij |H_ij - conj(H_ji)|` with acceptance `epsilon_H <= tau`; `HermiticityAnalyzer` owns `tau`. Schema version `1` is the first supported format; the codec must require every declared field, reject unknown fields at every level, reject booleans where integer or real values are required, reject nonfinite numeric values, reject malformed or ragged matrices, reject duplicate basis labels, reject `basis.orthonormal=false`, reject `energy_reference.value`, encode complex values as `[real, imaginary]`, and emit deterministic JSON-compatible objects. The canonical public path is `ksdft2effmass.operators`; do not preserve top-level `ksdft2effmass` operator re-exports solely for hypothetical compatibility; do not add wrappers for removed `OperatorRecord` methods. If actual released users, published examples, or persisted payloads are discovered, pause and request human direction. Do not create `OperatorRecordWorkflow` for construct -> Hermiticity analysis -> serialize -> deserialize. Use `python/tests/ksdft2effmass/operators/test__<ObjectName>.py` for object tests, `python/tests/ksdft2effmass/workflows/test__<WorkflowName>.py` only for genuine production Workflow objects, and `python/tests/ksdft2effmass/integration/test__<IntegrationName>.py` for technical integration tests.

Consequences
: Current `StateSpace.domain` and `StateSpace.codomain` are removed. `Geometry.length_unit` becomes required. `EnergyReference.value` is removed. Nonorthogonal `OperatorRecord` instances are rejected. Existing broad tests must be split into object-owned modules. Serialization becomes strict and versioned. Top-level operator re-exports may be removed. Earlier ad hoc payloads are not automatically migrated. Approximate comparison, unit conversion, basis alignment, nonorthogonal metrics, and general rectangular maps remain future ActionObjects or data models.

Affected files or agents
: Expected implementation scope includes `python/src/ksdft2effmass/operators/` and directly affected source exports such as `python/src/ksdft2effmass/__init__.py`. Test scope includes `python/tests/ksdft2effmass/operators/` and explicitly assigned technical integration tests under `python/tests/ksdft2effmass/integration/`. Documentation scope includes `docs/`. Affected agents are implementation, tests, documentation, integration reviewer, and parent pi.

Date
: 2026-07-30

Approval status
: Approved for implementation. Continue through implementation -> tests and documentation -> integration review -> parent verification -> human final acceptance. Pause again if implementation evidence contradicts any approved assumption or reveals actual compatibility obligations.

#### Human resolution: Checkpoint 3 targeted corrective work approved

Decision
: Approve targeted corrective work for the three Checkpoint 3 findings.

Context
: Integration review found an obsolete broad test module, permissive numeric-string decoding, and a stale control-plane validation example.

Options considered
: Leave findings unresolved; approve targeted correction; reopen architecture.

Human resolution
: Approve targeted correction. The approved architecture remains unchanged.

Consequences
: Obsolete tests may be removed after coverage mapping, codec decoding becomes schema-strict, and the task validation example is updated.

Affected files or agents
: Implementation owner, test owner, parent pi, integration reviewer.

Date
: 2026-07-30

## Validation commands

Commands are discovered from `python/pyproject.toml` and `docs/conf.py`.

Run from `python/`:

```bash
python3 -m ruff format --check .
python3 -m ruff check .
python3 -m mypy src tests
python3 -m pytest --collect-only tests/ksdft2effmass/operators
python3 -m pytest tests
PYTHONPATH=src python3 - <<'PY'
from ksdft2effmass.operators import HermiticityAnalyzer, OperatorRecordJsonSerializer
print(HermiticityAnalyzer, OperatorRecordJsonSerializer)
PY
PYTHONPATH=src python3 - <<'PY'
import numpy as np
from ksdft2effmass.operators import Basis, EnergyReference, Geometry, OperatorRecord, OperatorRecordJsonSerializer, StateSpace
record = OperatorRecord(
    identifier='smoke',
    operator_kind='finite_test_hamiltonian',
    matrix=np.eye(1),
    state_space=StateSpace(identifier='s', kind='finite', dimension=1),
    basis=Basis(identifier='b', kind='canonical', ordering=('0',), orthonormal=True),
    geometry=Geometry(
        system='toy',
        cell=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        boundary_conditions='finite',
        coordinate_convention='dimensionless row vectors',
        length_unit='dimensionless',
    ),
    energy_reference=EnergyReference(zero='zero', unit='eV'),
    provenance={'source': 'smoke'},
)
serializer = OperatorRecordJsonSerializer()
text = serializer.serialize(record)
restored = serializer.deserialize(text)
assert restored == record
PY
```

Run from repository root for documentation:

```bash
PYTHONPATH=python/src python3 -m sphinx -W -b html docs docs/_build/html
```

## Completion gates

The parent pi must independently run the combined unit tests, Ruff formatter check, Ruff lint check, mypy check, Sphinx build with warnings treated as errors, public-import smoke test, JSON round-trip test, architecture-conformance review, obsolete-import scan, and dangling-helper scan.

A failing gate leaves the task incomplete unless the human explicitly accepts the unresolved failure after receiving its cause and consequences.

## Required final report

Pi's final report must include files changed, commands run, subagent outputs summarized, unresolved limitations, assumptions, expensive scientific validations not performed, parent verification results, material findings and human resolutions, and confirmation that passing automated checks is not human final acceptance.

## Human-approved corrective contract recorded 2026-07-30

The active approved correction is final for this targeted refactor and must not
be reopened for unrelated architecture.

### JSON serialization object

`OperatorRecordJsonSerializer` replaces `OperatorRecordJsonCodec`. The public
contract is actual JSON text:

```python
serializer = OperatorRecordJsonSerializer()
text = serializer.serialize(record)
restored = serializer.deserialize(text)
assert restored == record
```

No compatibility alias or wrapper for `OperatorRecordJsonCodec`, `encode()`, or
`decode()` may be added unless actual released users or persisted artifacts are
discovered. Such evidence blocks the task and requires human direction.

### Scientific validation policy

Every scientific invariant, convention, transformation, approximation, and
wire-format decision must have a public specification and an independently
executable validation surface. Private methods are allowed only when they belong
exclusively to one DataObject or ActionObject, mechanically implement an already
public and documented rule, are fully observable through public inputs and
outputs, are not called by other classes, and contain no hidden scientific
convention or transformation. Tests validate public behavior rather than private
method names. No class may call another class's private method.

Module-private functions are permitted only within their module, for shared
mechanical invariants, with no hidden scientific semantics, with behavior
validated through public DataObjects or ActionObjects, and with documentation
when nontrivial. Do not create `utils.py`, `helpers.py`, `common.py`, or
`misc.py`. Dangling-helper policy means every function has a clear module or
object owner, not that every mechanical operation must be wrapped in a class.

### Required stage order

```text
control-plane contract
    ↓
public schema and validation fixtures
    ↓
production implementation
    ↓
tests
    ↓
documentation
    ↓
read-only integration review
    ↓
parent verification
    ↓
human final acceptance
```

Implementation, tests, and documentation must not run concurrently when any
stage depends on incomplete outputs from another. Completion gates include the
public schema, valid and invalid golden fixtures, deterministic JSON text
serialization, strict deserialization, source documentation, Sphinx
documentation, stale-API scans, dangling-helper and cross-private-call audits,
integration review after combined-tree validation, and parent verification.

## Human final acceptance recorded 2026-07-30

### Decision

Accept the operator-record refactor as complete and close this task.

### Accepted scope

This acceptance covers:

- DataObject/ActionObject/ResultObject architecture;
- finite operator-record invariants;
- orthonormal-basis restriction;
- geometry and energy-reference conventions;
- Hermiticity analysis;
- strict schema-version-1 specification;
- deterministic JSON text serialization;
- valid and invalid conformance fixtures;
- object-scoped tests;
- public API;
- Sphinx and source documentation;
- control-plane policies and completion gates;
- Python/Rust-compatible wire-format preparation.

### Accepted public API

```python
from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    HermiticityAnalyzer,
    HermiticityResult,
    OperatorRecord,
    OperatorRecordJsonSerializer,
    StateSpace,
)
```

Canonical serialization use:

```python
serializer = OperatorRecordJsonSerializer()

text = serializer.serialize(record)
restored = serializer.deserialize(text)

assert restored == record
```

### Accepted validation evidence

- 153 tests passed;
- Ruff formatting passed;
- Ruff linting passed;
- mypy passed;
- Sphinx warning-as-error build passed;
- valid schema fixtures passed;
- invalid schema fixtures were rejected;
- public-import validation passed;
- deterministic serialization passed;
- JSON round-trip validation passed;
- obsolete API scan passed;
- dangling-helper scan passed;
- cross-private-call audit passed;
- read-only integration review passed;
- parent verification passed.

### Scientific limitation

This acceptance validates software behavior, mathematical data invariants,
schema semantics, serialization reproducibility, API organization, and
documentation consistency. It does not validate the physical correctness of a
represented Hamiltonian, basis alignment between calculations, energy-reference
alignment between calculations, Wannier reconstruction accuracy, tight-binding
reduction accuracy, impurity extraction, or comparison with first-principles
data. Those require separate scientific-validation ActionObjects, Workflows,
reference datasets, and acceptance criteria.

### Consequences

- Schema version `1` is now the first accepted operator-record wire format.
- `OperatorRecordJsonCodec`, `encode()`, and `decode()` are not supported public
  APIs.
- `OperatorRecord.to_dict()` and `OperatorRecord.from_dict()` are not supported.
- Nonorthogonal operator records are not supported by schema version `1`.
- Future Python and Rust implementations must conform to the public schema and
  golden fixtures.
- Changes to schema-version-1 semantics require explicit human review.

### Final status

```text
Implementation: accepted
Tests: accepted
Documentation: accepted
Control plane: accepted
Integration review: accepted
Parent verification: accepted
Human final acceptance: approved
Scientific validation: not yet performed
```

No Rust implementation, schema version `2`, or scientific-validation workflow is
started as part of closing this task.
