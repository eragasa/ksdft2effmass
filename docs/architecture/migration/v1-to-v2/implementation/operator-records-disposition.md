# Operator-record retention and compatibility disposition

## Status and identity

**Human-accepted and administratively closed.** The human response
`accept and closeout` accepted the deterministic planning result for
`migration.v2.operators-ownership.records-disposition`. It applies the
human-authorized Option A ownership decision: the existing
`ksdft2effmass.operators` package remains the cohesive owner of finite represented
operator records, their schema-version-1 serializer, and exact represented-metadata
compatibility.

This is a provisional no-change migration baseline for the current accepted
contract, not a freeze of the final Architecture v2 scientific API. The controlled
research-monograph exercises are expected to reveal which state-space, projection,
embedding, comparison, and model-class information later APIs must preserve. Any
future public-contract change remains subject to separate human authorization,
compatibility analysis, and applicable migration evidence.

This disposition requires no source relocation, compatibility facade, public-import
change, wire conversion, fixture conversion, dependency change, or scientific
execution. It does not implement a new schema version, approve serialization for
comparison results or exceptions, or decide the separately owned disposition of
Hermiticity, differencing, residual, comparison, alignment, fitting, or reduction
algorithms.

## Source and object disposition

| Current source | Retained v2 role | Disposition |
|---|---|---|
| `python/src/ksdft2effmass/operators/records.py` | Represented-record DataObjects and intrinsic invariants | Retain in place as the canonical owner; do not introduce a v1 facade or duplicate record types. |
| `StateSpace` | Finite represented state-space metadata | Retain exact fields, positive-dimension invariant, canonical built-in integer storage, and exact value semantics. |
| `Basis` | Ordered basis metadata | Retain exact label ordering, uniqueness, defensive tuple storage, and the distinction between independently valid nonorthonormal basis metadata and the orthonormal schema-v1 record requirement. |
| `Geometry` | Cell and boundary metadata | Retain row-vector convention, finite built-in-float storage, exact metadata, and the public scale-relative linear-independence criterion. |
| `EnergyReference` | Textual energy-zero and unit metadata | Retain exact strings; add no numerical offset, unit registry, normalization, or conversion policy. |
| `OperatorRecord` | Finite matrix representation with interpreting metadata | Retain all eight fields, immutable owned `complex128` matrix, dimension coupling, orthonormal-record requirement, compact string provenance, and exact structural equality. |
| `python/src/ksdft2effmass/operators/serialization.py` | Schema-version-1 JSON serializer ActionObject | Retain in place with deterministic canonical text, strict decoding, duplicate-key rejection, finite-number enforcement, and DataObject reconstruction. |
| `python/src/ksdft2effmass/operators/compatibility.py` | Exact compatibility audit for independently valid records | Retain in place as an ActionObject/ResultObject boundary before arithmetic; do not merge compatibility into a DataObject or higher-level analysis. |

`OperatorRecord.provenance` remains the compact schema-version-1
string-to-string metadata field. It is not reinterpreted as a Workflow run, artifact
manifest, calculator observation, validation result, or proof that its strings are
true. Any future rich provenance relation must be composed explicitly and must not
silently replace or fabricate this retained wire field.

The DataObject/ActionObject split remains unchanged. Individual DataObjects own only
intrinsic field and cross-field invariants within one record. The serializer owns wire
mechanics. `OperatorRecordCompatibilityAnalyzer` owns relations between two valid
records. Alignment, conversion, physical equivalence, and scientific acceptance stay
outside all three owners.

## Current public Python compatibility baseline

For this no-change disposition, the supported import surface remains
`ksdft2effmass.operators`. The repository root package continues to re-export none of
these objects. The table records what this Task leaves unchanged; it does not declare
that the exercise program can never motivate a separately approved future contract.

| Public family | Current retained names | No-change rule for this Task |
|---|---|---|
| Record DataObjects | `StateSpace`, `Basis`, `Geometry`, `EnergyReference`, `OperatorRecord` | Preserve names, nominal type identities, constructor/runtime behavior, public attributes, exceptions, and exact equality semantics. |
| Record serializer | `OperatorRecordJsonSerializer` | Preserve `SCHEMA_VERSION == 1` and public `serialize(record) -> str` and `deserialize(text) -> OperatorRecord`. No public dictionary API is introduced. |
| Compatibility types | `OperatorRecordCompatibilityMismatchCode`, `OperatorRecordCompatibilityIssue`, `OperatorRecordCompatibilityResult`, `IncompatibleOperatorRecordsError`, `OperatorRecordCompatibilityAnalyzer` | Preserve names, structured fields, enum values/order, `execute()` and `require()` behavior, and the incompatible result carried by the exception. |

Direct imports from internal modules are not promoted into an additional public
contract by this plan. The package initializer remains the supported public route.
No alias package, renamed class, transitional adapter, or second nominal
`OperatorRecord` type is warranted because the accepted v2 owner and current owner are
the same.

## Exact compatibility disposition

Compatibility remains exact, deterministic represented-metadata auditing before direct
matrix subtraction. The canonical mismatch order remains:

1. `MATRIX_DIMENSION_MISMATCH`;
2. `STATE_SPACE_KIND_MISMATCH`;
3. `OPERATOR_KIND_MISMATCH`;
4. `ORDERED_BASIS_LABELS_MISMATCH`;
5. `BASIS_KIND_MISMATCH`;
6. `LATTICE_VECTORS_MISMATCH`;
7. `BOUNDARY_CONDITIONS_MISMATCH`;
8. `COORDINATE_CONVENTION_MISMATCH`;
9. `GEOMETRY_LENGTH_UNIT_MISMATCH`;
10. `ENERGY_UNIT_MISMATCH`; and
11. `ENERGY_ZERO_CONVENTION_MISMATCH`.

Record identifier, state-space identifier, basis identifier, geometry system label,
and provenance remain deliberately ignored by this represented-compatibility audit.
That exclusion permits a software subtraction only when every compatibility-critical
field agrees. It does not establish that the records represent the same physical
system or that subtraction is scientifically meaningful.

Compatibility performs no basis, gauge, geometry, spin, unit, or energy-zero alignment;
no conversion or tolerance is hidden in the audit. A future alignment operation must
produce or identify records satisfying this exact prerequisite before using guarded
fixed-representation arithmetic. It must not weaken this audit or reinterpret an
incompatible result as physical inequivalence.

## Schema-version-1 wire disposition

`specification/operator-record/v1/operator-record.schema.json` remains the public,
language-neutral Draft 2020-12 schema. `OperatorRecordJsonSerializer` remains its
Python runtime owner. The wire remains closed to unknown fields and retains exactly
these represented paths:

| Wire object | Exact retained fields and representation |
|---|---|
| Root | `schema_version`, `identifier`, `operator_kind`, `matrix`, `state_space`, `basis`, `geometry`, `energy_reference`, `provenance` |
| `matrix` | Nonempty row-major matrix of `[real, imaginary]` finite JSON-number pairs |
| `state_space` | `identifier`, `kind`, `dimension` |
| `basis` | `identifier`, `kind`, `ordering`, `orthonormal`; schema version 1 requires `orthonormal: true` |
| `geometry` | `system`, `cell`, `boundary_conditions`, `coordinate_convention`, `length_unit` |
| `energy_reference` | `zero`, `unit`; no `value`, offset, or inferred reference energy |
| `provenance` | Object with nonempty string keys and nonempty string values |

The runtime continues to enforce constraints not fully expressible in the schema:

- `N = state_space.dimension = len(basis.ordering)`;
- matrix shape is exactly `N x N`;
- matrix and cell components are finite;
- cell rows satisfy the documented `Geometry` linear-independence criterion;
- duplicate JSON object keys and nonstandard constants are rejected; and
- DataObject semantic-type and intrinsic invariants are reapplied during decoding.

No wire migration is required for Architecture v2. A future wire change requires a
new explicitly approved schema version, compatibility policy, fixtures, serializer
behavior, and consumer migration; it must not mutate version 1 in place. Comparison,
Hermiticity, difference, residual, exception, and compatibility-result objects retain
no approved wire merely because some error codes are `StrEnum` values.

## Fixture and evidence disposition

The complete golden corpus remains under `specification/operator-record/v1/` without
relocation or reclassification.

| Fixture class | Exact retained inventory | Required result |
|---|---|---|
| Valid | `minimal.json`, `complex-hermitian.json`, `complex-nonhermitian.json` | Public deserialization succeeds and deterministic reserialization preserves the represented JSON value. Hermiticity classification in the two named complex fixtures remains separate analyzer evidence. |
| Invalid structure/value | `dimension-mismatch.json`, `duplicate-basis-label.json`, `empty-string.json`, `energy-reference-value.json`, `missing-field.json`, `nonorthogonal-basis.json`, `nonsquare-matrix.json`, `ragged-matrix.json`, `singular-cell.json`, `unknown-field.json`, `unsupported-version.json` | Public deserialization rejects each through the documented value/invariant boundary. |
| Invalid semantic type | `boolean-as-number.json`, `numeric-string.json` | Public deserialization rejects each with `TypeError`; values are not coerced. |

The schema, fixtures, serializer tests, DataObject tests, compatibility tests, and
static dependency-direction test remain distinct software-verification owners. The
Geometry linear-independence and applicable algorithm tests retain their declared
numerical-verification status. Passing any of them does not establish provenance
truth, basis or gauge alignment, physical correctness, scientific validation,
uncertainty quantification, or cross-language conformance.

Historical case-study and computational pages remain records of their stated episodes
and tasks. They are not migration adapters, current public-contract owners, or reasons
to rewrite the version-1 artifacts.

## Dependencies, consumers, and cutover gates

The retained internal direction is
`records -> compatibility -> difference -> residuals -> comparison`; serialization
depends directly on records. Earlier layers must not import later layers. The sibling
analysis-disposition Task owns the exact future treatment of Hermiticity, difference,
residual, and comparison algorithms, but it may not replace record, serialization, or
exact-compatibility ownership decided here.

Because this Task performs retention rather than relocation, it has no transitional
cutover. A later implementation claiming backward compatibility with the current
version-1 boundary must satisfy these gates; a separately authorized breaking
contract must instead define its explicit version, compatibility policy, consumer
migration, and retained evidence:

1. account for the supported `ksdft2effmass.operators` record, serializer, and
   compatibility imports and their nominal identities;
2. leave version 1 unchanged or introduce a separately versioned wire with canonical
   behavior, fixtures, runtime invariants, and consumer migration;
3. preserve exact compatibility-before-arithmetic semantics unless an explicitly
   approved alignment contract supplies a stronger prerequisite;
4. preserve the inward dependency direction and prevent higher-level analysis from
   becoming a record or wire owner by convenience;
5. migrate every identified consumer before retiring any route, with no v2 domain code
   depending indefinitely on a transitional duplicate; and
6. classify software and numerical verification separately and make no unsupported
   scientific or cross-language claim.

Rollback for a later implementation is the last accepted revision applicable to that
implementation. This disposition creates no alternate legacy owner or facade.

## Deferred scope

No material human-owned choice remains for this bounded no-change disposition: Option
A and the currently accepted schema-version-1 contract determine provisional retention
uniquely. The following remain outside this Task rather than unresolved alternatives
within it:

- the sibling disposition of fixed-representation numerical algorithms;
- higher-level basis, gauge, geometry, unit, spin, and energy-reference alignment;
- model fitting, continuum reduction, structured learning, transferability analysis,
  and scientific interpretation;
- exercise-informed revision of the eventual scientific API and object boundaries;
- any schema version after version 1 or wire for non-record result objects;
- any authorized Rust component and associated cross-language conformance evidence;
- implementation, scientific or protected execution, publication, release, and
  automatic successor activation.
