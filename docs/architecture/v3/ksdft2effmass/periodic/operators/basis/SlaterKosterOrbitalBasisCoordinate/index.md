# `SlaterKosterOrbitalBasisCoordinate`

## Contract and identity

Frozen coordinate keyed by exact primitive-cell `site_label`, `SlaterKosterOrbital`,
and optional explicit `spin_component`.

## Invariants

Site labels are nonempty and exact. The orbital is a concrete enum member. `None` means
spinless, not unknown spin. Conventional Cartesian orbital axes are fixed by contract.

## Dependencies and flow

The diamond `sp3s*` model constructs ten ordered coordinates, five on site `A` followed
by five on site `B`, and binds them through `PeriodicBasisIdentity`.

## Serialization

The record stores `kind = slater_koster_orbital`, `site_label`, `orbital`, and
`spin_component` through `BaseTypedRecord`.

## Scientific boundary

It does not own site embedding, lattice geometry, orbital gauge, hopping parameters,
energy reference, or adequacy claims.

## Mappings

Source: `python/src/ksdft2effmass/periodic/operators/basis.py`; direct tests are the periodic basis
and Slater--Koster model suites; Sphinx: `doc/sphinx/api/periodic-basis.rst`.

## Provenance and evidence

The key extends the selected basis recommendation with the existing diamond `sp3s*`
orbital inventory. Tests provide software-verification evidence only.

## Limitations

Spinor and higher-orbital models require explicit new labels and model contracts.

## Navigation

- [Module](../index.md)
- [Slater--Koster model architecture](../../../../model_systems/slater_koster/index.md)
