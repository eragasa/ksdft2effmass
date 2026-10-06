# `Periodic1DRetainedOperatorReciprocalRepresentation`

## Purpose and status

This implemented row-024/026 DataObject binds a complete ordered reciprocal-matrix
family to one exact retained operator in one declared basis and gauge.

## Contract and invariants

The record requires stable nonempty representation, map, gauge, and provenance
identities; a one-dimensional `PeriodicRetainedOperator`; a complete
`CenteredUniformReciprocalMesh1D`; role-neutral `ReciprocalOperatorSamples1D`; an
orthonormal `Basis` ordered exactly like the retained labels; an exact matching
`EnergyReference`; and a lowercase SHA-256 over contiguous little-endian complex128
matrix bytes.

Matrix rank must equal retained rank. Sample and mesh reciprocal periods and every
ordered coordinate must agree after explicit unit conversion. Sample energy units must
match the represented energy reference. Type errors and semantic contradictions fail
rather than triggering inference, reordering, alignment, or conversion of operator
meaning.

## Scientific boundary

The binding supplies retained-operator interpretation that the sample container lacks.
It does not construct the retained space, choose or reconstruct a frame, infer a gauge
from dimensions, perform a Fourier transform, or assess scientific adequacy.

## Evidence map

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/representations.py:Periodic1DRetainedOperatorReciprocalRepresentation` | Representation metadata, compatibility, and content authentication |
| Test | `TestPeriodic1DCompositeScientificAdoption::test_method__execute__separates_exact_operator_from_gauge_forms` | One exact operator with explicit smooth reciprocal form |
| Tests | `...authenticates_preserved_array_identities`, `...rejects_incomplete_or_ambiguous_representation_metadata`, `...rejects_basis_and_energy_metadata_contradictions` | Digest, gauge, ordering, energy, and unit failures |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/representations.rst` | Public contract |

## Provenance and limitations

The digest establishes observed-content identity for canonical matrix bytes. It is not
independent historical provenance and excludes unavailable frame/projector bytes.
Passing tests do not establish gauge smoothness, convergence, validation, UQ, or
acceptance.
