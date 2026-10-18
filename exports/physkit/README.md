# Project Koios PhysKit export candidates

## Status

This is a non-runtime staging boundary for reusable dimensionful quantities, physical
metrics, physics, and physically interpreted mathematical behavior whose intended owner
is
[`projectkoios-physkit`](https://github.com/eragasa/projectkoios-physkit). An active
finite hopping symmetry/geometry candidate is staged under
[`periodic/lattice/`](periodic/lattice/README.md).

Target base inspected during preparation:
`d6333208a1ff723682a557afd593a5c932058cb7` (`projectkoios-physkit` 0.1.2).
Current donor worktree base:
`08a3211f0748bdbb1d45bfc12f2ca8f8205007d3`.

## Existing target capabilities to reuse

HSH design must first compose maintained PhysKit contracts rather than export copies:

- `LatticeDisplacement` and `LatticeDimension`;
- `IntegralLatticeOperation` and `LatticeDisplacementTransformer`;
- `FinitePeriodicDomain` and its coordinate/index actions;
- `ScalarHoppingTerm` and `ScalarHoppingModel`; and
- sparse represented-operator construction and compatibility behavior.

## Active export candidate

The staged candidate supplies:

- finite signed-axis-operation orbit construction built on PhysKit lattice types;
- deterministic square-lattice $D_4$ operation and displacement-orbit enumeration;
- reusable exact integer squared-radius hopping shells independent of HSH thresholds;
- scalar-hopping defect analysis and exact-real orbit projection; and
- dimensionful full-block hopping/Frobenius geometry.

The candidate remains donor-side transfer material. It is not an accepted PhysKit API
until separately reviewed and integrated by the owner.

Unit-free parameter-space metrics, distances, dual norms, and support optimization
belong to Optimization, with future transfer work recorded under
`exports/optimization`. Anything requiring physical dimensions, units,
dimensional conversion, or lattice/hopping interpretation belongs here. The owner is
selected by dimensional and physical semantics, not by counting consumers.

## Exclusions

HSH source identities, coefficient-bound selection, spectral weights, thresholds,
training/withheld roles, witness and certificate policy, outward-rounding policy, class
and hierarchy dispositions, retained schemas, workflow routing, and scientific claims
remain owned by `ksdft2effmass`.
