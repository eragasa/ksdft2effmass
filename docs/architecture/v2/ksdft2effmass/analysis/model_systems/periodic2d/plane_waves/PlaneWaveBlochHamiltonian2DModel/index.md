# `PlaneWaveBlochHamiltonian2DModel`

## Purpose and status

`PlaneWaveBlochHamiltonian2DModel` is the implemented row-016 finite plane-wave
representation definition. Its established historical `Model` suffix does not classify
it as a nominal scientific `PeriodicModel`.

## Public contract

Supported import:
`from ksdft2effmass.analysis.model_systems import PlaneWaveBlochHamiltonian2DModel`.

The immutable record fixes PhysKit direct and reciprocal lattices, a nonnegative square
reciprocal cutoff, sorted unique conjugate-symmetric Fourier coefficients, positive
kinetic energy scale, represented state-space and basis identities, and energy-reference
identity.

## State, ordering, and invariants

The basis contains integer pairs `-M <= p,q <= M` in `p`-outer, `q`-inner order and has
dimension `(2M+1)^2`. The spin convention is exactly `spinless_scalar`. Missing Fourier
transfers return exact complex zero. Coefficient inventories satisfy
`V[-m] = conjugate(V[m])`; the record does not silently symmetrize them.

Wrong semantic types raise `TypeError`. Negative cutoff, noncanonical transfer inventory,
failed reality relation, nonpositive scale, or empty represented identities raise
`ValueError`. A short `__post_init__` delegates lattice, basis, Fourier, energy, and
identity invariant families.

## Scientific boundary

The record defines complete input for one finite matrix construction. It is neither the
untruncated continuum parent nor the represented result. Cutoff error, parent-model
adequacy, retained-space selection, and campaign acceptance remain separate.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/plane_waves.py:PlaneWaveBlochHamiltonian2DModel` | Finite representation definition |
| Test | `TestPlaneWaveBlochHamiltonian2DModel::test_properties__square_cutoff__exposes_declared_basis_identity` | Ordering, dimension, spin, coefficients, exact zero, non-membership in `PeriodicModel` |
| Test | `TestPlaneWaveBlochHamiltonian2DModel::test_construction__missing_conjugate_partner__raises_value_error` | Reality-condition rejection |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/plane_waves.rst` | Full mathematics, units, algorithm, and evidence |

Tests reside under
`python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/`.

## Provenance and evidence

Original local work under the repository license; scientific references for Bloch and
plane-wave conventions are recorded on the Sphinx page. Software tests establish the
finite definition; constructor numerical tests establish bounded analytic cases. No
continuum convergence, material validation, uncertainty quantification, or human
acceptance is established.

## Limitations

Only square reciprocal cutoffs, a scalar kinetic scale, and finite Fourier inventories
are supported. PhysKit lattice arrays do not themselves carry physical units, so the
caller must retain a consistent coordinate and kinetic-scale convention.
