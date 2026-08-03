# Operator-Record Architecture

## Resolved paths and authority

The authoritative Python source root is `python/src/`, established by `python/pyproject.toml` package discovery and `docs/conf.py`. The operator package is `python/src/ksdft2effmass/operators/`; the Python test root is `python/tests/`.

The focused operator-record VVUQ migration is complete. Maintained
software-verification object tests live under:

```text
python/tests/software_verification/ksdft2effmass/<package>/test__<ObjectName>__<facet>.py
```

Maintained numerical-verification cases use the corresponding
`numerical_verification/` hierarchy. Operator-record object tests use the
`operators/` subtree, the concrete comparison Workflow uses `workflows/`, and
technical integration evidence uses `integration/`. Transitional unsuffixed
paths under `python/tests/ksdft2effmass/operators/` remain historical evidence,
not active owners.

The operator-record validation-correction task closed with human final acceptance
on 2026-08-03. No operator-record corrective task or successor task is active.
Human approval is required before any future implementation. The human PI is final authority for scientific meaning, mathematical conventions, public API decisions, serialization compatibility, architectural boundaries, backward compatibility, project scope, unresolved validation failures, and final acceptance. Record corrective decisions in `.pi/tasks/operator-record-validation-correction.md`; preserve historical refactor evidence.

The operator package structure is:

```text
python/src/ksdft2effmass/operators/
├── __init__.py
├── records.py
├── compatibility.py
├── difference.py
├── residuals.py
├── comparison.py
├── hermiticity.py
└── serialization.py
```

The dependency direction for comparison-related modules is `records.py` ->
`compatibility.py` -> `difference.py` -> `residuals.py` -> `comparison.py`.
Earlier layers must not import later layers. `comparison.py` owns only the
concrete `OperatorRecordComparator` Workflow composition.

## Object responsibilities

| Object | Category | Responsibility |
| --- | --- | --- |
| `StateSpace` | DataObject | Finite state-space metadata and state-space validation |
| `Basis` | DataObject | Ordered basis metadata |
| `Geometry` | DataObject | Cell and boundary metadata and geometry validation |
| `EnergyReference` | DataObject | Exact textual energy-zero-convention and energy-unit metadata |
| `OperatorRecord` | DataObject | Matrix and comparison-critical metadata only |
| `HermiticityResult` | ResultObject | Immutable Hermiticity result |
| `HermiticityAnalyzer` | ActionObject | Hermiticity analysis and enforcement; owns tolerance |
| `OperatorRecordJsonSerializer` | ActionObject | Versioned JSON text serialization; owns schema-version and complex-matrix mechanics |
| `OperatorRecordCompatibilityIssue` | ResultObject component | Authoritative compatibility mismatch code with canonical derived description |
| `OperatorRecordCompatibilityResult` | ResultObject | Tuple-only compatibility issues, derived rule sequence, and derived compatibility status |
| `OperatorRecordCompatibilityAnalyzer` | ActionObject | Exact compatibility analysis for already-represented records |
| `OperatorRecordDifferenceResult` | ResultObject | Immutable represented difference `candidate - reference` after compatibility succeeds |
| `OperatorRecordDifferencer` | ActionObject | Compatibility enforcement, sign convention, subtraction, nonfinite-difference detection, and difference-result construction |
| `OperatorRecordComparisonResult` | ResultObject | Immutable structural residual metrics for a represented difference |
| `OperatorRecordResidualAnalyzer` | ActionObject | Scale-safe residual norms, residual numerical errors, and metric-order roundoff policy |
| `OperatorRecordComparator` | Workflow ActionObject | Concrete composition of differencer followed by residual analyzer |

## Required software-verification test modules

Create one principal module per public object, except approved VVUQ-migrated objects may be split by facet:

- `test__StateSpace__construction.py`, `test__StateSpace__invariants.py`, and `test__StateSpace__value_semantics.py` under the target software-verification hierarchy
- `test__Basis__construction.py`, `test__Basis__invariants.py`, and `test__Basis__value_semantics.py` under the target software-verification hierarchy
- `test__Geometry__construction.py`, `test__Geometry__invariants.py`, and `test__Geometry__value_semantics.py` under the target software-verification hierarchy, plus `test__Geometry__linear_independence.py` under the target numerical-verification hierarchy
- `test__EnergyReference__construction.py`, `test__EnergyReference__invariants.py`, and `test__EnergyReference__value_semantics.py` under the target software-verification hierarchy
- `test__OperatorRecord__construction.py`, `test__OperatorRecord__matrix_invariants.py`, `test__OperatorRecord__metadata_invariants.py`, `test__OperatorRecord__ownership.py`, and `test__OperatorRecord__value_semantics.py` under the target software-verification hierarchy
- `test__HermiticityResult__construction.py`, `test__HermiticityResult__invariants.py`, and `test__HermiticityResult__value_semantics.py` under the target software-verification hierarchy
- `test__HermiticityAnalyzer__configuration.py` and `test__HermiticityAnalyzer__contract.py` under the target software-verification hierarchy, plus `test__HermiticityAnalyzer__analytical_residuals.py` under the target numerical-verification hierarchy
- `test__OperatorRecordJsonSerializer__contract.py`, `test__OperatorRecordJsonSerializer__serialization.py`, `test__OperatorRecordJsonSerializer__deserialization_structure.py`, `test__OperatorRecordJsonSerializer__deserialization_values.py`, and `test__OperatorRecordJsonSerializer__round_trip.py` under the target software-verification hierarchy, plus `test__OperatorRecordJsonSchema.py` and `test__OperatorRecordJsonFixtures.py` under its `integration/` subtree

Each module primarily tests the public contract of the object named in the filename. `OperatorRecordDifferenceResult` is migrated to `test__OperatorRecordDifferenceResult__construction.py`, `test__OperatorRecordDifferenceResult__invariants.py`, and `test__OperatorRecordDifferenceResult__value_semantics.py` under `python/tests/software_verification/ksdft2effmass/operators/`. `OperatorRecordCompatibilityAnalyzer` is migrated to cohesive `test__OperatorRecordCompatibilityAnalyzer__contract.py` and `test__OperatorRecordCompatibilityAnalyzer__rules.py` facets under the same target hierarchy. Package dependency-direction evidence belongs to the narrowly scoped integration module `python/tests/software_verification/ksdft2effmass/integration/test__OperatorComparisonDependencyDirection.py`, not to an Analyzer object test. Place cross-object behavior with the ActionObject that owns the operation: Hermiticity configuration and execution/enforcement software evidence in the two target `test__HermiticityAnalyzer__configuration.py` and `test__HermiticityAnalyzer__contract.py` facets, and independent residual oracles in the target numerical `test__HermiticityAnalyzer__analytical_residuals.py` facet; runtime JSON behavior in the five target serializer facets, with public schema and golden-fixture interoperability in their two narrow integration owners; matrix construction, intrinsic invariants, ownership, operational immutability, and exact value semantics in the five target `test__OperatorRecord__<facet>.py` modules.

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
- Static constructor declarations may expose already admitted input families while stored field annotations retain canonical built-in types. Such `TYPE_CHECKING`-only declarations preserve generated dataclass runtime behavior. This includes admitted numeric scalar families and the approved ordered-sequence input for `Basis.ordering`; Boolean rejection and bare-string rejection remain documented runtime semantic refinements where broad static protocols cannot express them precisely.
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

## Compatible-record comparison decomposition

Current comparison is limited to already-compatible finite ``OperatorRecord``
representations. It performs no basis alignment, gauge alignment, energy-zero
alignment, unit conversion, geometry transformation, approximate metadata
matching, physical-equivalence determination, impurity-operator interpretation,
or scientific validation.

The approved public decomposition is ``compatibility -> represented difference
-> residual analysis -> comparison Workflow``. For compatible records,
``OperatorRecordDifferencer`` forms the represented operator difference
``Delta H = H_candidate - H_reference`` in the common representation. This
public immutable ResultObject is independently executable and validatable, but
is not a complete serializable ``OperatorRecord`` and is not automatically an
impurity operator. ``OperatorRecordResidualAnalyzer`` accepts only that
represented difference, computes maximum absolute entry, Frobenius norm, and
spectral norm in the common energy unit, and owns dimensionless machine-epsilon
roundoff policy scaled by matrix dimension and common metric scale; it
canonicalizes within-allowance values upward before ResultObject construction
and rejects larger order defects with enum-backed structured numerical errors.
``OperatorRecordComparisonResult`` remains a structural ResultObject and must
not own machine-epsilon policy, roundoff canonicalization, or maximum-dimension
policy. ``OperatorRecordComparator`` is a concrete Workflow ActionObject whose
execution is equivalent to differencer execution followed by residual-analyzer
execution.

Implementations must use scale-safe algorithms and raise enum-backed structured
numerical errors with ownership separated between nonfinite represented
difference and residual metric/linear-algebra failures.

Every public mismatch code must be reachable by comparing independently valid
records. Because version-1 records require an orthonormal basis, no
orthonormality-convention mismatch code is public.
