# `PlaneWaveFiberHamiltonian1DResult`

**Defined in:** `ksdft2effmass.periodic1d.plane_waves`

## Role

Immutable correlation of the exact parent-qualified request, ordered finite plane-wave
basis, construction tolerance, and represented energy matrix.

## Intrinsic invariants

The matrix is square with basis dimension and uses the qualified parent's recoil-energy
unit. Result validation does not replay the Action or prove provenance, Hermiticity,
convergence, physical adequacy, validation, or uncertainty quantification.

## Evidence

`test__PlaneWaveFiberHamiltonian1DResult.py` checks shape correlation independently of
the construction Action.
