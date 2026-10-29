# Higher-rank frame alignment in periodic one-dimensional models

This package supports the rank-$r$ frame-alignment study for periodic one-dimensional
Hamiltonians. The study compares four alignment strategies over retained subspaces with
$r\in\{3,4,8,16\}$ and circuit depths $L\in\{1,2,4,8\}$.

## Physical and numerical scope

The calculation separates three questions:

1. Can neighboring retained frames be transported around the reciprocal-space period
   without a rank-deficient overlap?
2. Can the endpoint mismatch be distributed smoothly so that the transported frame is
   periodic?
3. How do identity, global-unitary, pointwise-unitary, and known-inverse alignment
   strategies affect operator locality and reconstruction error?

The short labels `A0`--`A3` remain only as stable identifiers inherited from the frozen
experimental protocol. Public Python names use the scientific descriptions of the
channels and transformations.

## Available implementation

The current package provides:

- the fixed rank, depth, construction-mesh, global-unitary-selection-mesh,
  evaluation-mesh, channel, phase-branch, and tolerance choices;
- explicit outcomes for successful alignment, rank deficiency, numerical failure, and
  downstream inapplicability;
- an immutable transport request that fixes one case, unshifted construction mesh,
  ambient basis, retained frame, and endpoint sewing;
- neighbor-link singular values, numerical-rank margins, and backend validation
  residuals; and
- immutable results for the three right-unitary transformations required to close a
  transported frame around the reciprocal-space period.

The higher-rank Hamiltonian producer, independent recalculation, complete result
verification, figures, and calculation scripts have not yet been implemented. No
higher-rank case has been executed or scientifically validated through this package.

## Numerical responsibilities

- Project Koios Optimization evaluates polar-Procrustes transport, numerical rank, and
  the distributed matrix root.
- PhysKit supplies the physical meaning of frames, ambient bases, reciprocal-space
  routes, and endpoint sewing.
- `ksdft2effmass` defines the study parameters, scientific diagnostics, alignment
  outcomes, verification requirements, and eventual claims.

The calculation-local `workflow/` directory under the historical rank-$N$ calculation is
retained only for provenance. The maintained package neither imports nor adapts it.

## Further details

- [Software realization](implementation.md)
- [Numerical formulation](numerics.md)
- [Physical interpretation](scientifics.md)
- [Calculation flow](schematics.md)
