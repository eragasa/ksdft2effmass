# `analysis.model_systems.periodic2d.plane_waves`

## Purpose and status

This implemented module constructs one finite spinless scalar plane-wave representation
of a two-dimensional periodic Bloch operator.

## Public inventory

| Symbol | Role |
|---|---|
| `PlaneWaveFourierCoefficient2D` | One reciprocal-transfer coefficient |
| `PlaneWaveBlochHamiltonian2DModel` | Complete finite representation definition; not a nominal scientific model |
| `PlaneWaveBlochHamiltonian2DRequest` | Reduced-momentum fiber and duality tolerance |
| `PlaneWaveBlochHamiltonian2DResult` | Represented matrix and correlated request/residual |
| `PlaneWaveBlochHamiltonian2DConstructor` | Matrix-construction Action |

## Mathematics and conventions

For column-basis lattices `A` and `B`, the Action checks `A^T B = 2*pi*I` to the
caller-owned absolute tolerance and constructs

$$
H_{n'n}(\kappa)=E_K\lVert B(\kappa+n)\rVert^2\delta_{n'n}+V_{n'-n}.
$$

Reduced momentum is expressed in the reciprocal primitive basis. The square cutoff uses
`p`-outer, `q`-inner ordering. Missing Fourier transfers are exact zero, and
`V[-m] = conjugate(V[m])` is required for a real scalar potential.

## Class navigation

- [`PlaneWaveBlochHamiltonian2DModel`](PlaneWaveBlochHamiltonian2DModel/index.md)
- [`PlaneWaveBlochHamiltonian2DRequest`](PlaneWaveBlochHamiltonian2DRequest/index.md)
- [`PlaneWaveBlochHamiltonian2DResult`](PlaneWaveBlochHamiltonian2DResult/index.md)
- [`PlaneWaveBlochHamiltonian2DConstructor`](PlaneWaveBlochHamiltonian2DConstructor/index.md)

`PlaneWaveFourierCoefficient2D` remains a small intrinsic coefficient DataObject fully
documented by the module Sphinx page.

## Code, tests, Sphinx, and provenance

| Kind | Path | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/plane_waves.py` | Representation definition and construction |
| Software tests | `python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/` | Types, ordering, correlation, units, immutability |
| Numerical test | `python/tests/numerical_verification/ksdft2effmass/analysis/model_systems/periodic2d/test__PlaneWaveBlochHamiltonian2DConstructor.py` | Analytic lattice and Fourier cases |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/plane_waves.rst` | Full equations, units, algorithm, evidence, and references |

Original local work under the repository license, with literature provenance recorded in
Sphinx. Tests do not establish continuum convergence or material validation.
