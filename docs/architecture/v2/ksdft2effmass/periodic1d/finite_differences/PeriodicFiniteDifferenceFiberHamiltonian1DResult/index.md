# `PeriodicFiniteDifferenceFiberHamiltonian1DResult`

**Defined in:** `ksdft2effmass.periodic1d.finite_differences`

## Role

Immutable correlation of the exact parent-qualified request, half-open grid,
construction tolerance, and sparse represented energy matrix.

## Intrinsic invariants

The sparse matrix shape equals the grid point count and its unit equals the qualified
parent recoil-energy unit. Result validation does not replay the Action or establish
seam provenance, convergence, physical adequacy, validation, or uncertainty
quantification.

## Evidence

`test__PeriodicFiniteDifferenceFiberHamiltonian1DResult.py` independently checks shape
correlation.
