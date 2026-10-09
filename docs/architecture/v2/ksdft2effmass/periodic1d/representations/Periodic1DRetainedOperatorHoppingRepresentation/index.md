# `Periodic1DRetainedOperatorHoppingRepresentation`

## Purpose and status

This implemented row-024 DataObject binds a complete centered finite-mesh hopping
family to one exact retained operator in one declared basis and gauge.

## Contract and invariants

The record carries explicit representation, representation-map, gauge, and provenance
identities; retained operator; reciprocal mesh; `BlockHoppingModel1D`; orthonormal
ordered basis; exact energy reference; and a SHA-256 over contiguous little-endian
complex128 block bytes. Its representatives must equal the complete centered cell
representatives of the mesh. Matrix rank, basis labels, reciprocal period, and energy
units must match the retained operator and mesh.

## Exact representation versus effective model

A complete finite-mesh coefficient family is another representation of the declared
finite retained operator. Dropping blocks or fitting a prescribed finite-range class
constructs an approximate effective model and is owned by separate result types. This
binding is also distinct from `Periodic1DCompleteHoppingRepresentationResult`, which
owns a performed Fourier construction and reconstruction evidence.

## Evidence map

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/representations.py:Periodic1DRetainedOperatorHoppingRepresentation` | Complete represented family and authenticated content |
| Test | `TestPeriodic1DCompositeScientificAdoption::test_method__execute__separates_exact_operator_from_gauge_forms` | Smooth and rough gauges bind one exact operator |
| Tests | `...authenticates_preserved_array_identities`, `...rejects_incomplete_or_ambiguous_representation_metadata`, `...rejects_basis_and_energy_metadata_contradictions` | Digest, completeness, gauge, ordering, energy, and unit failures |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/representations.rst` | Public contract and route distinction |

## Provenance and limitations

The retained composite smooth and rough block hashes authenticate canonical observed
bytes. Rough reciprocal matrices and both frame arrays are unavailable and are not
reconstructed. Passing tests do not establish locality, gauge quality, convergence,
scientific validation, UQ, or acceptance.
