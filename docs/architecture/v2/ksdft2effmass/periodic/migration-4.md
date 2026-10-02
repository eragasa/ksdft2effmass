# Migration phase 4: scientific-retention owners

## Status

**Proposed.** The target concepts are documented but no shared retained-space/operator
API is implemented.

## Purpose

Introduce the typed scientific objects required by the manuscript without treating an
operator, matrix, or preserved document as a `PeriodicModel`.

## Required owners

Phase 4 introduces composition-based owners for:

1. **Retention construction or selection.** Identifies parent model and operator,
   construction kind, selected band or spectral content, reciprocal domain, and
   applicable assumptions.
2. **Retained-space identity.** Identifies parentage, ambient and retained spaces,
   rank, projector or frame data, and construction provenance.
3. **Exact retained operator.** Identifies domain and codomain as the retained space and
   links the exact restriction to its parent operator.
4. **Represented retained operator.** Combines the retained operator with an applicable
   `OperatorRecord` or specialized represented-operator record, basis, gauge, geometry,
   unit, energy reference, and provenance.
5. **Construction Actions and Results.** Perform selection, restriction, and
   representation explicitly rather than through DataObject constructors or private
   cross-object methods.

A retention-kind enum may classify spectral restriction, selected-band retention, or
disentanglement, but it cannot replace parent identity, projector or frame, retained
space, rank, domain/codomain, and operator data.

## Existing mechanics to compose

Applicable existing mechanics include:

- `ContiguousBandSelection`;
- `OrthogonalSpectralSubspace`;
- `ReciprocalBandFramePath1D`;
- `ReciprocalOperatorSamples1D`;
- `OperatorRecord`; and
- `ScalarFiniteLatticeOperator` where the finite-periodic scalar contract applies.

These types remain numerical or represented data. Composition with a new scientific
owner must not silently widen their existing public contracts.

## Required separations

- Retained-space identity is distinct from its gauge-dependent frame representation.
- The exact retained operator is distinct from every finite matrix representation.
- Complete Fourier transformation is distinct from truncation or fitting.
- An effective model is distinct from the exact retained operator it approximates.
- Alignment diagnostics are distinct from the transport map used for comparison.
- Scalar energy alignment is distinct from unitary or partial-isometry transport.

## Excluded work

Phase 4 does not yet migrate concrete 1D or 2D models, populate the toy catalog, execute
campaigns, define material-reference physics, or authorize defect subtraction.

## Completion gate

- Public contracts document parentage, domain/codomain, rank, construction, units,
  gauge, energy reference, geometry, and provenance where applicable.
- Runtime validation rejects wrong semantic types and incompatible dimensions.
- DataObjects remain immutable and Actions own reusable cross-object behavior.
- Tests establish construction, invalid-input rejection, identity propagation, and
  represented-dimension agreement without claiming scientific validation.
- Exports and Sphinx documentation expose only deliberately supported routes.
- Source and targeted tests pass Ruff, formatting, mypy, pytest, Sphinx
  warnings-as-errors, links, and `git diff --check`.
