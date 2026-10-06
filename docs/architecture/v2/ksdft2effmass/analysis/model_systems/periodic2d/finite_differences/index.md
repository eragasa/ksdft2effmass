# `analysis.model_systems.periodic2d.finite_differences`

## Purpose and status

This implemented module owns the reusable row-035 finite representation of a spinless
scalar Bloch operator on a square dimensionless coordinate cell. It owns the half-open
grid and Euclidean site basis, immutable potential samples, centered second-order
stencil, directed Bloch seams, explicit energy metadata, represented identities, and
construction provenance.

It does not own the cosine scientific parent, continuum convergence, common-space
comparison, or campaign acceptance.

## Public inventory

- [`UniformPeriodicCoordinateBasis2D`](UniformPeriodicCoordinateBasis2D/index.md)
- [`FiniteDifferenceBlochHamiltonian2DModel`](FiniteDifferenceBlochHamiltonian2DModel/index.md)
- [`FiniteDifferenceBlochHamiltonian2DRequest`](FiniteDifferenceBlochHamiltonian2DRequest/index.md)
- [`FiniteDifferenceBlochHamiltonian2DResult`](FiniteDifferenceBlochHamiltonian2DResult/index.md)
- [`FiniteDifferenceBlochHamiltonian2DConstructor`](FiniteDifferenceBlochHamiltonian2DConstructor/index.md)

## Ownership and boundaries

The `Model` suffix denotes a complete finite representation input, not nominal
`PeriodicModel` membership. Potential samples are immutable data rather than an
arbitrary callable. The cosine constructor samples its exact parent and delegates the
only matrix assembly algorithm to this module.

The representation is dimensionless and square-cell-specific. Binary64 range failures
for spacing, squared spacing, stencil coefficients, represented diagonals, and seam
arguments are explicit `OverflowError` outcomes. Dense matrix storage scales as
`O(N**4)` and may raise `MemoryError`; no arbitrary grid cap is imposed. No result
establishes finite-difference convergence, continuum accuracy, physical adequacy,
scientific validation, uncertainty quantification, or acceptance.

## Code and evidence

| Kind | Path |
|---|---|
| Source | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.py` |
| Basis software tests | `python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/test__UniformPeriodicCoordinateBasis2D__construction.py` |
| Model software tests | `python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/test__FiniteDifferenceBlochHamiltonian2DModel__construction.py` |
| Request software tests | `python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/test__FiniteDifferenceBlochHamiltonian2DRequest__construction.py` |
| Result software tests | `python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/test__FiniteDifferenceBlochHamiltonian2DResult__construction.py` |
| Constructor numerical tests | `python/tests/numerical_verification/ksdft2effmass/analysis/model_systems/periodic2d/test__FiniteDifferenceBlochHamiltonian2DConstructor__execute.py` |
| Adapter | `python/src/ksdft2effmass/periodic2d/model/toy_models/cosine.py` |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.rst` |
