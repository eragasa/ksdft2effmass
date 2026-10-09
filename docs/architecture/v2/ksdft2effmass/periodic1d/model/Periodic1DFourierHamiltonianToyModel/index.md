# `Periodic1DFourierHamiltonianToyModel`

## Purpose and status

`Periodic1DFourierHamiltonianToyModel` is the implemented row-017 complete untruncated
quadratic-kinetic periodic Fourier toy parent.

## Public contract

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DFourierHamiltonianToyModel`.

The constructor binds exact nonempty model, Bloch state-space, and primitive reciprocal-
domain identities; a `PeriodicFourierPotential1D`; and a positive recoil-energy scale
compatible with the potential energy unit. The model has nominal 1D membership and exact
`PeriodicModelRole.TOY`.

## Mathematics and state-space convention

For reduced momentum `k` in the primitive interval `[-0.5, 0.5]`,

$$
H_{nm}(k)=E_G(k+n)^2\delta_{nm}+V_{n-m}.
$$

This law defines the untruncated parent. It does not select a finite reciprocal cutoff,
mesh, retained bands, gauge, or effective hopping range.

## Invariants and failure behavior

Wrong exact identity/component types raise `TypeError`; empty identities, nonpositive
recoil energy, or incompatible potential/kinetic units raise `ValueError`. A short
`__post_init__` delegates parent-identity and component/unit invariant families.

## Scientific boundary

Nominal membership identifies a controlled toy parent, not a material Hamiltonian.
Finite plane-wave representations have separate basis, map, state-space, and provenance
identities. Their numerical discretization error is not merged with later retention or
model-reduction error.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/model.py:Periodic1DFourierHamiltonianToyModel` | Complete parent law and identities |
| Test | `TestPeriodic1DFourierHamiltonianToyModel::test_construction__parent__binds_complete_nominal_toy_identity` | Identity, role, domain, potential, scale, catalog membership |
| Test | `TestPeriodic1DFourierHamiltonianToyModel::test_construction__identity__rejects_empty_parent_identity` | Stable identity requirement |
| Test | `TestPeriodic1DFourierHamiltonianToyModel::test_construction__recoil_energy__rejects_nonpositive_scale` | Positive kinetic law |
| Test | `TestPeriodic1DFourierHamiltonianToyModel::test_construction__units__rejects_incompatible_kinetic_and_potential_energy` | Energy-unit compatibility |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/model.rst` | Equation and parent/representation boundary |

## Provenance and evidence

Original local work under the repository license. Synthetic tests establish software
behavior. No infinite-basis convergence, material validation, uncertainty
quantification, or acceptance is established.

## Limitations

The parent is spinless and uses a quadratic kinetic law plus finite Fourier potential
component. It is not a production electronic-structure model.
