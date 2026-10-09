# `UniformPeriodicCoordinateBasis2D`

## Purpose and public contract

This implemented row-035 DataObject defines one square half-open dimensionless grid
with coordinate period `L`, odd extent `N >= 5`, and a caller-owned basis identity. It
is supported from `ksdft2effmass.analysis.model_systems`.

Its finite state space has dimension `N**2`. Canonical site vectors are
Euclidean-orthonormal and ordered by `(x_index, y_index)` with `x_outer_y_inner`
flattening. Coordinates are `i*L/N`; the endpoint `L` is excluded.

## Invariants and failures

- `coordinate_period` is an exact finite positive built-in float.
- `points_per_direction` is an odd built-in integer of at least five; booleans are
  rejected.
- `basis_identifier` is a nonempty string and is never inferred from dimension.
- `coordinate_period / points_per_direction` must remain positive in binary64;
  spacing underflow raises `OverflowError` during construction.

This is a finite Euclidean coordinate-sample basis, not a continuum position basis or
an implicit quadrature-weighted basis.

## Code, Sphinx, and tests

| Surface | Mapping |
|---|---|
| Class | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.py::UniformPeriodicCoordinateBasis2D` |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.rst` |
| Canonical test source | [`tests.py`](tests.py) |

| Pytest node | Evidence established |
|---|---|
| `TestUniformPeriodicCoordinateBasis2DConstruction::test_construction_exposes_half_open_euclidean_site_basis` | Exact spacing, dimension, endpoint order, flattening, and normalization |
| `...::test_construction_rejects_non_float_coordinate_periods` | Boolean, integer, and numeric-string rejection |
| `...::test_construction_rejects_nonpositive_or_nonfinite_coordinate_periods` | Period value domain |
| `...::test_construction_rejects_non_integer_or_invalid_grid_extents` | Strict odd-grid extent domain |
| `...::test_construction_rejects_missing_or_mistyped_basis_identity` | Explicit identity boundary |
| `...::test_construction_rejects_binary64_spacing_underflow` | Fail-closed spacing representability |

`tests.py` is a relative symlink to the single runnable pytest owner under
`python/tests/software_verification`; the architecture tree does not duplicate test
assertions.

## Evidence and limitations

Software verification covers the listed synthetic inputs. Numerical verification,
scientific validation, uncertainty quantification, and human acceptance are not
established. Original local work under the repository license.
