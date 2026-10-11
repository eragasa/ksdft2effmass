# Finite hopping symmetry and geometry candidate

## Status and destination

This directory is a non-runtime export candidate for
`projectkoios-physkit`. The implementation was prepared against exact clean owner commit
`d6333208a1ff723682a557afd593a5c932058cb7` and KSD donor base
`08a3211f0748bdbb1d45bfc12f2ca8f8205007d3`.

The flattened export paths map to these intended owner destinations:

| Export file | Intended owner path |
|---|---|
| `symmetry_orbits.py` | `src/python/projectkoios/physkit/periodic/lattice/symmetry_orbits.py` |
| `hopping_symmetry.py` | `src/python/projectkoios/physkit/periodic/lattice/hopping_symmetry.py` |
| `hopping_geometry.py` | `src/python/projectkoios/physkit/periodic/lattice/hopping_geometry.py` |

Mapped tests remain under `exports/physkit/tests/projectkoios/physkit/periodic/lattice/`.
Exact relative-source, destination, and SHA-256 mappings are recorded in
[`transfer.toml`](transfer.toml). The owner repository remains authoritative for naming,
integration, supported imports, documentation placement, review, versioning, and
release.

## Candidate contracts

`SquareLatticeD4OperationSetConstructor` composes the existing
`IntegralLatticeOperation` contract into the exact eight square-lattice operations.
`LatticeDisplacementOrbitPartitioner` requires an explicitly supplied finite inventory
that is closed under a nonempty set of unique signed-axis operations. Its result
reconstructs dimensional agreement, coverage, disjointness, operation invariance,
canonical member order, canonical representative choice, and ordering by integer
squared radius.

`LatticeDisplacementShellInventoryConstructor` groups complete orbits by exact integer
squared radius. It does not select a campaign shell-radius sequence or determine which
shell is scientifically adequate.

`ScalarHoppingSymmetryDefectAnalyzer` reports independent maximum absolute
Hermiticity, imaginary-part, and orbit-constancy defects in the source energy unit.
`ScalarHoppingRealOrbitProjector` averages real parts in canonical orbit-member order
with finite scale normalization, sets projected imaginary parts to exact zero, preserves
basis/unit/energy-reference
metadata, and records the maximum coefficient change. Neither action chooses or applies
a tolerance.

`ScalarHoppingFrobeniusDistanceAnalyzer` compares two compatible complete hopping
families over the declared displacement inventory. It reports the unnormalized
full-block squared and root Frobenius distances with explicit units. Repeated orbit
coefficients therefore contribute according to their represented multiplicities.
Scientific normalization by an energy scale or block count remains caller-owned.

## Bounded HSH combinatorics

Composing the candidate with the existing PhysKit displacement and operation primitives
reconstructs the centered $15\times15$ HSH inventory as 36 complete $D_4$ orbits whose
multiplicities sum to 225. Inclusive shell radii
`(0, 1, 2, 4, 8, 18, 50, 98)` produce orbit counts
`(1, 2, 3, 4, 6, 12, 27, 36)` and represented-block counts
`(1, 5, 9, 13, 25, 61, 161, 225)`. These are combinatorial implementation checks, not
HSH calculation outcomes.

## Candidate validation

In a disposable overlay of the exact owner base, 16 focused candidate tests and all
1,188 non-slow overlay tests plus 20 subtests pass. Scoped Ruff check/format, strict mypy
over the three candidate modules, sdist/wheel builds, wheel-content inspection, and
wheel imports pass. A repository-wide Ruff run also reports 260 pre-existing findings
outside the mapped candidate paths; those unrelated findings were not modified. These
checks establish staged software behavior only, not owner acceptance or scientific
validation.

## Exclusions

This candidate does not own reciprocal-sample generation, source identity, spectral
weights, HSH energy-zero selection, coefficient bounds, loss normalization, thresholds,
witnesses, certificates, dispositions, retained schemas, scientific claims, or
calculation execution. It does not establish scientific validation or owner acceptance.
