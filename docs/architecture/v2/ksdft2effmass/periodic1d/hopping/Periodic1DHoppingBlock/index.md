# `Periodic1DHoppingBlock`

## Purpose and status

`Periodic1DHoppingBlock` is implemented supporting representation data for one directed
hopping coefficient `H_R` at an integer cell displacement `R`. It is not independently
a scientific model or represented operator.

## Public contract

Supported import: `from ksdft2effmass.periodic1d import Periodic1DHoppingBlock`.

- `displacement_cells` is an exact built-in integer.
- `matrix` is a NumPy integer, floating, or complex array copied into non-writeable,
  C-contiguous `complex128` storage.
- `orbital_count` returns the common square dimension of this block.

## Invariants and failure behavior

Boolean, string, byte, and object matrices raise `TypeError`. Empty, nonsquare,
nonfinite, or non-`complex128`-representable values raise `ValueError`. Pairwise
Hermiticity is not intrinsic to one directed block; it belongs to the containing
`Periodic1DFiniteHoppingToyModel`.

## Code, tests, and Sphinx

| Kind | Path or node | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/hopping.py:Periodic1DHoppingBlock` | Immutable block and scalar boundary |
| Test | `TestPeriodic1DFiniteHoppingToyModel::test_construction__blocks__owns_ordered_nonwriteable_complex_matrices` | Canonical immutable storage |
| Test | `TestPeriodic1DFiniteHoppingToyModel::test_construction__matrix__rejects_coercible_nonscientific_scalars` | Boolean/string rejection |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/hopping.rst` | Public API and `H_R` interpretation |

The test nodes reside in
`python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DFiniteHoppingToyModel.py`.

## Dependencies, provenance, and evidence

The block depends only on NumPy storage. The configured model composes it; numerical
constructors consume it without changing ownership. Original local work under the
repository license. Tests establish software behavior only. No standalone numerical
verification, scientific validation, uncertainty quantification, or acceptance is
claimed.

## Limitations

The block stores no energy unit, basis identity, parent model, gauge, or provenance;
those meanings belong to its containing scientific or represented object.
