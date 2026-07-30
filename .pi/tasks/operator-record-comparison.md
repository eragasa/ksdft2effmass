# Compatible OperatorRecord Comparison Task

## Status

Historical comparison task record created on 2026-07-30. It is preserved as
prospective historical evidence and is no longer the active authority for
operator-record corrections. The active corrective authority is
`.pi/tasks/operator-record-validation-correction.md`, which supersedes stale
statements in this file where explicitly noted, including removal of the
unreachable basis-orthonormal flag compatibility rule.

## Objective

Define and implement comparison of already-compatible finite `OperatorRecord`
representations.

This task establishes comparison semantics before basis alignment, energy
alignment, impurity extraction, DFT/Wannier import, or Rust implementation.

## Human scientific-software decision

The next task is:

```text
Define and implement comparison of already-compatible finite OperatorRecord representations.
```

The task must compare records by representation compatibility, not by equality
of every metadata object. Record identifiers, provenance, geometry system names,
operator identifiers, and physical-system labels are expected to differ between
records such as pristine and doped operators.

## Scope boundaries

In scope:

- public compatibility semantics for finite `OperatorRecord` representations;
- public compatibility ResultObject and ActionObject;
- public comparison ResultObject and ActionObject;
- absolute matrix residual metrics for compatible records;
- object-scoped tests under `python/tests/ksdft2effmass/operators/`;
- public mathematical definitions and Sphinx documentation;
- read-only integration review;
- parent verification and human final acceptance.

Out of scope:

- basis permutation;
- basis alignment;
- unit conversion;
- energy-zero shifting;
- geometry alignment;
- gauge alignment;
- Hermitian projection;
- relative or normalized residuals;
- JSON serialization formats for compatibility or comparison results;
- scientific pass/fail acceptance;
- impurity extraction;
- DFT/Wannier import;
- Rust implementation;
- schema version 2;
- scientific validation claims.

Comparison reports symmetric norm-valued numerical differences. It does not
determine whether those differences are scientifically acceptable. A future
signed operator-difference ResultObject and ActionObject belongs to impurity
extraction or another explicitly approved asymmetric operation.

## Representation compatibility

Two records are compatible for this first comparison operation when their matrix
representations use:

- the same matrix dimension;
- the same state-space kind;
- the same `operator_kind`;
- the same ordered basis labels;
- the same basis kind;
- the same lattice vectors;
- the same boundary conditions;
- the same coordinate convention;
- the same geometry length unit;
- the same energy unit;
- the same energy-zero convention.

Compatibility does not depend on any instance identity or provenance field.
Do not require equality of:

- `OperatorRecord.identifier`;
- `StateSpace.identifier`;
- `Basis.identifier`;
- `Geometry.system`;
- provenance;
- physical-system labels such as pristine and doped.

Compatibility is determined only by the explicitly listed representation fields.
These excluded fields identify represented physical objects or record instances
and are expected to differ.

For version 1, require exact equality of compatibility-critical metadata. Do not
introduce numerical geometry tolerances or alignment algorithms. Approximate
geometry compatibility belongs to a later explicitly approved policy.

## Compatibility result

Create a public, Rust-compatible enum:

```text
OperatorRecordCompatibilityMismatchCode
```

It must contain one stable member for every compatibility rule.

Create an immutable, Rust-compatible ResultObject:

```text
OperatorRecordCompatibilityIssue
```

It contains the authoritative mismatch `code`; the human-readable
`description` is now a canonical derived property, per the active corrective
task.

Create an immutable, Rust-compatible ResultObject:

```text
OperatorRecordCompatibilityResult
```

It must report:

- an immutable ordered collection of `OperatorRecordCompatibilityIssue` values;
- the identifiers of both records;
- the compatibility rules applied.

Its compatibility status must be determined consistently from whether the issue
collection is empty. Do not maintain independent mutable or potentially
contradictory compatibility state.

Mismatch ordering must be deterministic and documented.

Define a public compatibility ActionObject:

```text
OperatorRecordCompatibilityAnalyzer
```

Incompatibility must be inspectable and testable. Do not hide compatibility
logic inside private helper functions or exception strings.

## Stable mismatch-code policy

The implementation phase must define stable, public mismatch codes for every
compatibility rule. The required code set must include one code for each of:

- matrix dimension mismatch;
- state-space kind mismatch;
- `operator_kind` mismatch;
- ordered basis-label mismatch;
- basis-kind mismatch;
- lattice-vector mismatch;
- boundary-condition mismatch;
- coordinate-convention mismatch;
- geometry length-unit mismatch;
- energy-unit mismatch;
- energy-zero-convention mismatch.

The exact spelling of enum members may be proposed by the implementation plan,
but the members must be stable, machine-readable, and documented in source docs,
tests, and Sphinx documentation before final acceptance.

## Comparison metrics

For compatible records, the implementation may form an intermediate difference
matrix, but the public outputs are symmetric norms satisfying

$$
\left\|
\mathbf H_{\mathrm{candidate}}
-
\mathbf H_{\mathrm{reference}}
\right\|
=
\left\|
\mathbf H_{\mathrm{reference}}
-
\mathbf H_{\mathrm{candidate}}
\right\|.
$$

Do not claim that the sign of the intermediate difference is observable through
this comparison result. Retain reference/candidate identifiers for provenance and
future asymmetric operations, but do not expose the residual matrix in this task.

Create an immutable ResultObject:

```text
OperatorRecordComparisonResult
```

Let `Delta H` denote either intermediate difference
`candidate.matrix - reference.matrix` or its negative; the following norms are
unchanged by that sign choice. Report these absolute metrics:

1. Entrywise maximum residual

   $$
   \varepsilon_{\max}
   =
   \max_{i,j}
   \left|
   \Delta H_{ij}
   \right|.
   $$

2. Frobenius residual

   $$
   \varepsilon_{\mathrm F}
   =
   \left(
   \sum_{i,j}
   \left|
   \Delta H_{ij}
   \right|^2
   \right)^{1/2}.
   $$

3. Spectral or induced operator residual

   $$
   \varepsilon_2
   =
   \left\|
   \Delta\mathbf H
   \right\|_2,
   $$

   defined as the largest singular value of `Delta H`.

The result must identify the reference and candidate records, matrix dimension,
and energy unit.

Do not introduce relative or normalized residuals yet. Their denominator and
zero-reference policies require a separate scientific decision.

For this version, comparison and compatibility results must not receive a JSON
serialization format. Public serialization requires a separately approved schema
and interoperability decision. Do not modify `specification/operator-record/v1/`.

The scientific role of `spectral_residual` is to measure the largest change in the
operator's action on a normalized state. `maximum_absolute_residual` measures individual matrix
elements, and `frobenius_residual` measures aggregate matrix discrepancy. All three answer
different, valid questions.

## Comparison action

Create a public ActionObject:

```text
OperatorRecordComparator
```

Its execution must:

1. obtain a public compatibility result;
2. reject incompatible representations explicitly;
3. compute metrics only for compatible records;
4. return the immutable comparison result.

When compatibility analysis fails, `OperatorRecordComparator` must raise a public
exception:

```text
IncompatibleOperatorRecordsError
```

The exception must expose the complete public
`OperatorRecordCompatibilityResult` through a documented public attribute.
Compatibility information must not exist only in an exception message. This
Python exception corresponds conceptually to an error-valued result in a future
Rust implementation.

## Validation surfaces

The task must provide:

- public mathematical definitions;
- stable mismatch codes;
- schema or fixture coverage where appropriate;
- object-scoped tests under `python/tests/ksdft2effmass/operators/`;
- tests for every compatibility rule;
- analytically checkable matrices for every metric;
- symmetric-metric tests showing swapped inputs swap identifiers but preserve
  all three metrics;
- zero-residual tests;
- incompatible-record tests;
- complex-matrix tests;
- explicit tests/documentation that comparison and compatibility result JSON
  serialization is out of scope for this version;
- NumPy/SciPy-independent expected values for small validation fixtures;
- Sphinx API and concept documentation;
- separation between software-verification and scientific-validation claims;
- read-only integration review.

No dangling module-level helper functions and no cross-object private-method
calls are allowed.

## Affected files and ownership

Expected production-source ownership:

- `python/src/ksdft2effmass/operators/` — implementation agent owns new or
  changed operator comparison source files and public exports.
- If a new module is introduced, the preferred name is
  `python/src/ksdft2effmass/operators/comparison.py`, subject to architecture
  review before implementation.

Expected tests ownership:

- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityMismatchCode.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityIssue.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityResult.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityAnalyzer.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordComparisonResult.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordComparator.py`
- `python/tests/ksdft2effmass/operators/test__IncompatibleOperatorRecordsError.py`

Expected documentation ownership:

- `docs/concepts/operator-records.rst`
- `docs/api/operators.rst`
- repository-layout or development docs only if public navigation changes require
  them.

Expected specification/fixture ownership:

- Do not modify `specification/operator-record/v1/` for this task. Comparison
  and compatibility result serialization is out of scope for this version and
  requires a separately approved schema and interoperability decision.

Expected unaffected areas:

- DFT/Wannier import code;
- scientific specifications outside comparison fixtures or explanatory text;
- research results;
- Rust implementation;
- Graphify generated outputs;
- global agent configuration.

## Proposed implementation chain

Do not launch this chain until the task record and proposed chain have been
reported to the human.

```text
1. control-plane contract review
   -> read-only architecture agent verifies this task record and identifies any
      missing public decisions before implementation.
2. architecture/design pass
   -> define module placement, public object fields, public exception behavior,
      mismatch-code enum member spellings, deterministic mismatch ordering, and
      the explicit no-result-serialization boundary.
3. production implementation
   -> implement only the approved operator comparison source/API.
4. tests
   -> add object-scoped tests for compatibility and comparison public APIs.
5. documentation
   -> update Sphinx concept/API docs with definitions and software/scientific
      validation boundary.
6. initial parent verification
   -> run formatter, linter, type checker, unit tests, public-import smoke test,
      JSON checks if applicable, Sphinx -W, stale-reference scan, and
      obsolete-helper scan.
7. read-only integration review
   -> reviewer reports blocker/material/minor findings without editing.
8. deterministic corrections or genuine checkpoints
   -> parent applies deterministic corrections automatically; create a durable
      checkpoint only for genuine human decisions.
9. complete parent verification rerun
   -> any source, test, or documentation correction after integration review
      invalidates the earlier verification result until the applicable
      completion gates are rerun.
10. final human acceptance
   -> after verification passes, parent presents final report for acceptance.
```

## Completion gates

- The task record and proposed implementation chain are reported before any
  implementation begins.
- Public API exports are documented and smoke-tested.
- Compatibility logic is public, inspectable, and testable through
  `OperatorRecordCompatibilityMismatchCode`, `OperatorRecordCompatibilityIssue`,
  `OperatorRecordCompatibilityResult`, and
  `OperatorRecordCompatibilityAnalyzer`.
- Comparison metrics are returned through immutable `OperatorRecordComparisonResult`.
- `OperatorRecordComparator` uses compatibility analysis before metric
  computation and rejects incompatible records by raising
  `IncompatibleOperatorRecordsError` with a public compatibility-result
  attribute.
- Tests cover every compatibility rule and mismatch-code enum member.
- Tests verify deterministic mismatch ordering and that compatibility status is
  derived from the immutable ordered issue collection.
- Tests cover zero residual, symmetric swapping of reference/candidate inputs,
  complex matrices, and analytically checkable `maximum_absolute_residual`, `frobenius_residual`, and
  `spectral_residual` values.
- Tests verify `0 <= maximum_absolute_residual <= spectral_residual <= frobenius_residual` for selected
  validation matrices that avoid roundoff ambiguity.
- Expected values for small validation cases are independent of NumPy/SciPy.
- No relative or normalized residuals are introduced.
- No JSON serialization format is introduced for compatibility or comparison
  results, and `specification/operator-record/v1/` remains unchanged.
- No basis, energy, geometry, gauge, unit, or Hermitian alignment is performed.
- No scientific pass/fail acceptance policy is introduced.
- Formatter, linter, type checker, unit tests, public import smoke test, Sphinx
  warning-as-error build, stale-reference scan, and obsolete-helper scan pass.
- Read-only integration review reports no unresolved blocker/material findings.
- If integration-review corrections modify source, tests, or documentation,
  applicable completion gates are rerun before final human acceptance.
- Human final acceptance is recorded.

## Implementation and verification summary

Implementation status: complete after targeted symmetric-metric and compatibility-result invariant correction.
Verification status: passed after complete parent verification rerun.
Read-only integration review: passed with no blocker, material, or minor
findings after correction.
Human final acceptance: pending.
Scientific validation: not performed; not applicable to this software-comparison
implementation task by itself.

Implemented public API:

- `OperatorRecordCompatibilityMismatchCode`
- `OperatorRecordCompatibilityIssue`
- `OperatorRecordCompatibilityResult`
- `OperatorRecordCompatibilityAnalyzer`
- `OperatorRecordComparisonResult`
- `OperatorRecordComparator`
- `IncompatibleOperatorRecordsError`

Implemented files:

- `python/src/ksdft2effmass/operators/comparison.py`
- `python/src/ksdft2effmass/operators/__init__.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityMismatchCode.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityIssue.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityResult.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordCompatibilityAnalyzer.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordComparisonResult.py`
- `python/tests/ksdft2effmass/operators/test__OperatorRecordComparator.py`
- `python/tests/ksdft2effmass/operators/test__IncompatibleOperatorRecordsError.py`
- `docs/concepts/operator-records.rst`
- `docs/api/operators.rst`

Corrected invariants:

- Comparison is documented and tested as a symmetric norm operation; swapping
  reference and candidate swaps identifiers but preserves `maximum_absolute_residual`,
  `frobenius_residual`, and `spectral_residual`.
- A signed operator-difference ResultObject/ActionObject and residual-matrix
  exposure are explicitly deferred to a later impurity-extraction task.
- `OperatorRecordCompatibilityResult` independently rejects missing evaluated
  rules, duplicated evaluated rules, noncanonical rule ordering, duplicated
  issue codes, noncanonical issue ordering, and issue codes outside the
  evaluated rule set.
- `rules_applied` must equal `tuple(OperatorRecordCompatibilityMismatchCode)`.
- `OperatorRecordCompatibilityMismatchCode` uses `StrEnum` without Ruff
  suppression.
- Private validators use `object` for scalar validation and remain owned
  mechanical methods; no shared module-level helper functions remain.

Verification evidence:

- `python -m ruff format --check src tests` passed.
- `python -m ruff check src tests` passed.
- `python -m mypy` passed.
- `python -m pytest` passed with 222 tests.
- `python3 -m sphinx -W -b html docs docs/_build/html` passed.
- Public-import smoke test for new comparison API passed.
- `.pi/checkpoints/validate_checkpoints.py --include-fixtures --dry-run` passed.
- JSON validation for control-plane JSON files passed.
- `specification/operator-record/v1/` remained unchanged.
- No module-level helper functions remain in `comparison.py`.
- Initial integration review artifact:
  `.pi-subagents/artifacts/b8ca2905_ksdft2effmass.ksdft2effmass-integration-reviewer_0_output.md`.
- Post-correction integration review artifact:
  `.pi-subagents/artifacts/8af86686_ksdft2effmass.ksdft2effmass-integration-reviewer_0_output.md`.

No basis alignment, basis permutation, unit conversion, energy-zero shifting,
geometry alignment, gauge alignment, Hermitian projection, normalization,
relative residual, signed operator-difference result, residual-matrix exposure,
result serialization format, schema-version change, or scientific pass/fail
acceptance policy was introduced.

## Current action limit

Do not launch another task after completing this chain. After final human
acceptance, record acceptance, close this task, and stop.

## Repository-wide documentation and validation correction authorization

On 2026-07-30 the human PI explicitly authorized a repository-wide
research-software documentation and validation correction including the current
compatible `OperatorRecord` comparison implementation.  Approved scope includes:
Python 3.14 as the supported Python version; repository-local control-plane
updates enforcing complete source documentation; remediation of maintained
first-party Python source and tests; Sphinx/source synchronization; correction
of symmetric comparison semantics; independently validatable compatibility
ResultObject invariants; descriptive public comparison metric names; and
completion-gate updates.  The authorization explicitly excludes changes to
scientific meaning, numerical behavior, public schemas, and accepted public APIs
except for the comparison corrections named in the human prompt.

Deterministic corrections recorded under this authorization:

- Python metadata now requires Python 3.14 and Ruff targets Python 3.14.
- The repository-wide source-documentation standard is recorded in `AGENTS.md`
  and `docs/development/source-documentation.rst`.
- `OperatorRecordCompatibilityResult.rules_applied` is a public read-only
  canonical property derived from `tuple(OperatorRecordCompatibilityMismatchCode)`
  rather than an arbitrary constructor parameter.
- `OperatorRecordCompatibilityResult.is_compatible` remains derived solely from
  whether `issues` is empty.
- `OperatorRecordComparisonResult` public metric fields are
  `maximum_absolute_residual`, `frobenius_residual`, and `spectral_residual`,
  mapped respectively to $\varepsilon_{\max}$, $\varepsilon_{\mathrm F}$, and
  $\varepsilon_2$.  The unaccepted names `epsilon_max`, `epsilon_f`, and
  `epsilon_2` have no compatibility aliases.
- Comparison remains a symmetric norm-valued operation.  Exchanging reference
  and candidate swaps identifiers and preserves all metric values.  No signed
  residual matrix is exposed; signed operator-difference objects remain deferred
  to a future impurity-extraction task.

This correction is not a new scientific task and does not claim scientific
validation.
