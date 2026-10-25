# `ksdft2effmass.spaces`

## Purpose and status

This prospective package owns finite state-space and subspace contracts independently
of the operators that act on them. It is documentation-first; no source package or
supported import exists yet.

## Child map

- [`subspaces`](subspaces/index.md) — typed finite subspaces and their construction.

## Ownership boundary

`spaces` owns identities, dimensions, injections, and intrinsic subspace invariants. It
does not own Hamiltonians, operator reduction, scientific model construction,
experiment composition, serialization, or acceptance policy.

## Dependency rules

The package may consume immutable quantity records from `ksdft2effmass.operators` until
a separately reviewed quantity owner exists. It must not depend on `analysis`, model
systems, experiments, or calculations. Analysis may consume spaces; the reverse
dependency is forbidden.

## Evidence and limitations

Prospective architecture only. No implementation, tests, API documentation, or
scientific evidence exists yet.
