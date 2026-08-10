<!-- Generated from SQLite control state; do not edit. -->
# Compatible OperatorRecord Comparison Task

[Task index](index.md) · [Previous](./human-review-interface.review-packet-pilot.md) · [Next](./operator-record-refactor.md)

## Status

`legacy_recorded`: Closed as superseded historical evidence. This comparison task did not receive a
separate human final-acceptance decision. Its implemented work and later
corrections were incorporated into, verified under, and accepted through
`.pi/tasks/operator-record-validation-correction.md` on 2026-08-03. That accepted
record supersedes maintained-status and architecture statements here, including
the unreachable basis-orthonormal flag rule and the earlier deferral of a public
represented-difference object. This file preserves the original prospective
decision chronology and intermediate evidence; it is not an active task.

## Objective

Define and implement comparison of already-compatible finite `OperatorRecord`
representations.

This task establishes comparison semantics before basis alignment, energy
alignment, impurity extraction, DFT/Wannier import, or Rust implementation.

## Parent and prerequisites

None.

## Authority references

- harness/archive/task-control-v1/tasks/operator-record-comparison.md

## Authorized scope

- public compatibility semantics for finite `OperatorRecord` representations;
- public compatibility ResultObject and ActionObject;
- public comparison ResultObject and ActionObject;
- absolute matrix residual metrics for compatible records;
- object-scoped tests under `python/tests/ksdft2effmass/operators/`;
- public mathematical definitions and Sphinx documentation;
- read-only integration review;
- parent verification and human final acceptance.
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

## Completion criteria

- The task record and proposed implementation chain are reported before any
- Public API exports are documented and smoke-tested.
- Compatibility logic is public, inspectable, and testable through
- Comparison metrics are returned through immutable `OperatorRecordComparisonResult`.
- `OperatorRecordComparator` uses compatibility analysis before metric
- Tests cover every compatibility rule and mismatch-code enum member.
- Tests verify deterministic mismatch ordering and that compatibility status is
- Tests cover zero residual, symmetric swapping of reference/candidate inputs,
- Tests verify `0 <= maximum_absolute_residual <= spectral_residual <= frobenius_residual` for selected
- Expected values for small validation cases are independent of NumPy/SciPy.
- No relative or normalized residuals are introduced.
- No JSON serialization format is introduced for compatibility or comparison
- No basis, energy, geometry, gauge, unit, or Hermitian alignment is performed.
- No scientific pass/fail acceptance policy is introduced.
- Formatter, linter, type checker, unit tests, public import smoke test, Sphinx
- Read-only integration review reports no unresolved blocker/material findings.
- If integration-review corrections modify source, tests, or documentation,
- Human final acceptance is recorded.

## Exclusions

- public compatibility semantics for finite `OperatorRecord` representations;
- public compatibility ResultObject and ActionObject;
- public comparison ResultObject and ActionObject;
- absolute matrix residual metrics for compatible records;
- object-scoped tests under `python/tests/ksdft2effmass/operators/`;
- public mathematical definitions and Sphinx documentation;
- read-only integration review;
- parent verification and human final acceptance.
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

## Historical source

`harness/archive/task-control-v1/tasks/operator-record-comparison.md` (`sha256:179987712addb439d022abfd050b164d9c190952123760abaa7fd747dc77b177`)
