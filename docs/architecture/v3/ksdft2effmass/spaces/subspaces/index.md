# `ksdft2effmass.spaces.subspaces`

## Purpose and status

This prospective subpackage owns typed finite subspaces and their intrinsic
construction operations.

## Child map

- [`trial`](trial/index.md) — sampled trial frames, orthogonal trial subspaces, and
  symmetric Gram orthonormalization.

Hamiltonian spectral spaces remain with `ksdft2effmass.hamiltonian` because their
contract owns reduced-Hamiltonian coordinate reduction and embedding. A genuinely
generic mathematical subspace belongs to PhysKit rather than a KSD linear-algebra
compatibility package.

## Ownership boundary

The subpackage does not own operators, eigensolution, operator reduction, comparison,
experiments, or calculation evidence.

## Evidence

The `trial` module is prospective. No source or supported export exists yet.
