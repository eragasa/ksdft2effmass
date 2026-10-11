# Project Koios PhysKit export candidates

## Status

This is a non-runtime staging boundary for reusable dimensionful quantities, physical
metrics, physics, and physically interpreted mathematical behavior whose intended owner
is
[`projectkoios-physkit`](https://github.com/eragasa/projectkoios-physkit). No PhysKit
source candidate is implemented in this bundle yet.

Target base inspected during preparation:
`d6333208a1ff723682a557afd593a5c932058cb7` (`projectkoios-physkit` 0.1.2).
Donor worktree base:
`39d36f9a51e13a83f62557854095ae1180d5193f`.

## Existing target capabilities to reuse

HSH design must first compose maintained PhysKit contracts rather than export copies:

- `LatticeDisplacement` and `LatticeDimension`;
- `IntegralLatticeOperation` and `LatticeDisplacementTransformer`;
- `FinitePeriodicDomain` and its coordinate/index actions;
- `ScalarHoppingTerm` and `ScalarHoppingModel`; and
- sparse represented-operator construction and compatibility behavior.

## Prospective export candidates

Only genuinely missing, reusable behavior belongs here after its contract is reviewed:

- finite integral-operation group/orbit construction built on PhysKit lattice types;
- deterministic square-lattice $D_4$ displacement-orbit enumeration;
- reusable hopping-support shell construction when it is independent of HSH thresholds
  and hierarchy dispositions;
- projection of scalar hopping inventories onto a declared finite symmetry action; and
- physically interpreted hopping-coefficient and normalized Frobenius metric geometry.

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
