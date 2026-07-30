# Operator-Record Architecture

## Resolved paths and authority

The authoritative Python source root is `python/src/`, established by `python/pyproject.toml` package discovery and `docs/conf.py`. The operator package is `python/src/ksdft2effmass/operators/`; the Python test root is `python/tests/`.

Object tests must mirror the public package hierarchy below the configured test root:

```text
python/tests/ksdft2effmass/<package>/test__<ObjectName>.py
```

Operator-record object tests therefore live under:

```text
python/tests/ksdft2effmass/operators/test__<ObjectName>.py
```

Tests for genuine production Workflow objects use `python/tests/ksdft2effmass/workflows/test__<WorkflowName>.py`. Technical integration tests that are not domain workflows use `python/tests/ksdft2effmass/integration/test__<IntegrationName>.py`.

Human approval is required before implementation. The human PI is final authority for scientific meaning, mathematical conventions, public API decisions, serialization compatibility, architectural boundaries, backward compatibility, project scope, unresolved validation failures, and final acceptance. Record corrective decisions in `.pi/tasks/operator-record-validation-correction.md`; preserve historical refactor evidence.

## Object responsibilities

| Object | Category | Responsibility |
| --- | --- | --- |
| `StateSpace` | DataObject | Finite state-space metadata and state-space validation |
| `Basis` | DataObject | Ordered basis metadata |
| `Geometry` | DataObject | Cell and boundary metadata and geometry validation |
| `EnergyReference` | DataObject | Energy-zero metadata |
| `OperatorRecord` | DataObject | Matrix and comparison-critical metadata only |
| `HermiticityResult` | ResultObject | Immutable Hermiticity result |
| `HermiticityAnalyzer` | ActionObject | Hermiticity analysis and enforcement; owns tolerance |
| `OperatorRecordJsonSerializer` | ActionObject | Versioned JSON text serialization; owns schema-version and complex-matrix mechanics |
| `OperatorRecordCompatibilityIssue` | ResultObject component | Authoritative compatibility mismatch code with canonical derived description |
| `OperatorRecordCompatibilityResult` | ResultObject | Tuple-only compatibility issues, derived rule sequence, and derived compatibility status |
| `OperatorRecordCompatibilityAnalyzer` | ActionObject | Exact compatibility analysis for already-represented records |
| `OperatorRecordComparisonResult` | ResultObject | Immutable residual metrics for compatible records |
| `OperatorRecordComparator` | ActionObject | Scale-safe fixed-representation comparison after compatibility audit |

## Required test modules

Create one principal module per public object:

- `test__StateSpace.py`
- `test__Basis.py`
- `test__Geometry.py`
- `test__EnergyReference.py`
- `test__OperatorRecord.py`
- `test__HermiticityResult.py`
- `test__HermiticityAnalyzer.py`
- `test__OperatorRecordJsonSerializer.py`

Each module primarily tests the public contract of the object named in the filename. Place cross-object behavior with the ActionObject that owns the operation: Hermiticity execution/enforcement in `test__HermiticityAnalyzer.py`; JSON serialization, deserialization, malformed payloads, schema validation, and round trips in `test__OperatorRecordJsonSerializer.py`; matrix ownership, provenance immutability, exact equality, and intrinsic record invariants in `test__OperatorRecord.py`.

Do not create broad dumping-ground modules such as `test_records.py`, `test_operators.py`, `test_utils.py`, or `test_misc.py`. Technical integrations such as public package imports, JSON interoperability, filesystem boundaries, command-line behavior, Sphinx autodoc imports, and future Python/Rust schema compatibility belong under `python/tests/ksdft2effmass/integration/test__<IntegrationName>.py` unless they are object-owned behavior. Do not add `__init__.py` files to test directories unless required by established pytest import mode.

Do not create an `OperatorRecordWorkflow` for `construct -> Hermiticity analysis -> serialize -> deserialize`; those operations remain owned by `OperatorRecord`, `HermiticityAnalyzer`, and `OperatorRecordJsonSerializer`.

## Required decisions

- `OperatorRecord` contains represented data only.
- Hermiticity tolerance belongs to `HermiticityAnalyzer`.
- Hermiticity results are returned as `HermiticityResult`.
- Serialization belongs to `OperatorRecordJsonSerializer`.
- Schema-version and complex-matrix mechanics belong to the JSON serializer.
- Geometry validation belongs to `Geometry`.
- State-space validation belongs to `StateSpace`.
- Exact equality belongs to the DataObject.
- Approximate or physically aligned comparison is a separate future ActionObject.
- The public API is exported from `ksdft2effmass.operators`.
- Sphinx documentation and tests are required parts of completion.

## Mathematical Hermiticity criterion

Use the absolute entrywise maximum residual

$$
\varepsilon_{\mathrm H}
=
\max_{i,j}
\left|
H_{ij}-H_{ji}^{*}
\right|,
$$

with acceptance under analyzer tolerance $\tau$ when

$$
\varepsilon_{\mathrm H}\leq\tau.
$$

This is analyzer policy, not `OperatorRecord` state.

## Validation invariants

- Matrix is two-dimensional, square, finite, and `complex128` after canonicalization.
- Matrix dimension matches `StateSpace.dimension` and `len(Basis.ordering)`.
- Stored matrix is copied from the caller and made non-writeable.
- Provenance is copied and exposed read-only; provenance values are explicit strings.
- `Geometry.cell` is three finite, linearly independent three-component row lattice vectors.
- `EnergyReference` stores `zero` and `unit`; no numerical offset field is stored.
- DataObject equality is exact structural equality. Do not use tolerances for `__eq__`.

## Replaced API

Former data-object methods are not allowed:

```python
record.hermiticity_residual()
record.is_hermitian()
record.require_hermitian()
record.to_dict()
OperatorRecord.from_dict(...)
```

Use ActionObjects instead:

```python
analyzer = HermiticityAnalyzer(tolerance=..., energy_unit="eV")
result = analyzer.execute(record)
analyzer.require(record)

serializer = OperatorRecordJsonSerializer()
text = serializer.serialize(record)
restored = serializer.deserialize(text)
```

## Versioned serializer design

- `schema_version` is an explicit fixed field.
- Complex entries are encoded deterministically as `[real, imaginary]` pairs.
- Missing or unsupported schema versions are serializer errors.
- Round trips preserve exact DataObject equality for represented data.
- Wire-format field names are fixed for Rust compatibility.

## Public imports

`ksdft2effmass.operators` must export `StateSpace`, `Basis`, `Geometry`, `EnergyReference`, `OperatorRecord`, `HermiticityResult`, `HermiticityAnalyzer`, and `OperatorRecordJsonSerializer`.

## Corrective serialization and validation contract

The approved JSON ActionObject is `OperatorRecordJsonSerializer`, not
`OperatorRecordJsonCodec`. Its public methods are `serialize(record) -> str` and
`deserialize(text) -> OperatorRecord`; it operates on actual JSON text with
deterministic key ordering and compact separators. Do not add aliases for
`OperatorRecordJsonCodec`, `encode()`, or `decode()` unless actual released users
or persisted artifacts are discovered; such evidence requires human direction.

Schema-version-1 semantics must be public in
`specification/operator-record/v1/operator-record.schema.json` with valid and
invalid golden fixtures. Runtime validation must reject unknown fields, duplicate
JSON object keys, nonstandard constants, numeric strings, booleans-as-numbers,
malformed complex pairs, ragged/nonsquare matrices, dimension mismatches,
duplicate basis labels, nonorthogonal bases, singular cells, and forbidden
historical `energy_reference.value` fields.

No class may call another class's private method. Private serializer methods are
allowed only for owned mechanical steps that implement documented schema rules
and are exercised through `serialize()` and `deserialize()` tests. Source
docstrings are part of implementation; Sphinx documentation is part of
completion. Integration review occurs only after combined-tree validation.

## Compatible-record comparison

Current comparison is limited to already-compatible finite ``OperatorRecord``
representations. It performs no basis alignment, gauge alignment, energy-zero
alignment, unit conversion, geometry transformation, approximate metadata
matching, physical-equivalence determination, or scientific validation. For
compatible records, ``Delta H = H_candidate - H_reference`` and the public
metrics are maximum absolute entry, Frobenius norm, and spectral norm in the
common energy unit, satisfying ``0 <= maximum <= spectral <= Frobenius``.
Implementations must use scale-safe algorithms and raise structured numerical
errors for nonfinite subtraction, overflow, or linear-algebra failure.

Every public mismatch code must be reachable by comparing independently valid
records. Because version-1 records require an orthonormal basis, no
orthonormality-convention mismatch code is public.
