# `SlaterKosterOrbital`

## Contract and identity

Closed `StrWireEnum` for the current spinless `sp3s*` Slater--Koster orbital vocabulary
in conventional Cartesian axes.

## Invariants

Exact members are `s`, `p_x`, `p_y`, `p_z`, and `s_star`. No alias or implicit axis
rotation exists.

## Dependencies and flow

The enum is consumed by `SlaterKosterOrbitalBasisCoordinate` and the diamond
`DiamondSp3sStarModel` basis declaration.

## Serialization

Owners explicitly map members through `to_wire()` and `from_wire()`.

## Scientific boundary

The enum labels orbitals only. It does not define hopping parameters, orbital centers,
Bloch phase, geometry, or model adequacy.

## Mappings

Source: `python/src/ksdft2effmass/periodic/operators/basis.py`; tests include the periodic basis
and Slater--Koster model suites; Sphinx: `doc/sphinx/api/periodic-basis.rst`.

## Provenance and evidence

The vocabulary matches the implemented diamond `sp3s*` model. Tests are software
verification, not semiconductor validation.

## Limitations

Higher-orbital Slater--Koster families require a separately reviewed vocabulary change.

## Navigation

- [Module](../index.md)
- [`SlaterKosterOrbitalBasisCoordinate`](../SlaterKosterOrbitalBasisCoordinate/index.md)
