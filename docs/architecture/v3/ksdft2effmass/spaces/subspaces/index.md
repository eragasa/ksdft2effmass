# `ksdft2effmass.spaces.subspaces`

## Purpose and status

This prospective subpackage owns typed finite subspaces and their intrinsic
construction operations.

## Child map

- [`trial`](trial/index.md) — sampled trial frames, orthogonal trial subspaces, and
  symmetric Gram orthonormalization.

Existing `operators.subspaces.OrthogonalSpectralSubspace` remains an implemented
legacy owner until a separately reviewed migration places spectral subspaces here.
This tranche does not add a compatibility facade or move that existing class.

## Ownership boundary

The subpackage does not own operators, eigensolution, operator reduction, comparison,
experiments, or calculation evidence.

## Evidence

The `trial` module is prospective. No source or supported export exists yet.
