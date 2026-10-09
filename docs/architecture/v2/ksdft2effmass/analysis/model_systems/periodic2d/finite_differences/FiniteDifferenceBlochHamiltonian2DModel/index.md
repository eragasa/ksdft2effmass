# `FiniteDifferenceBlochHamiltonian2DModel`

## Purpose and public contract

This implemented row-035 DataObject is the complete reusable input definition for one
finite dimensionless centered-difference representation. It is supported from
`ksdft2effmass.analysis.model_systems` and is not a nominal scientific
`PeriodicModel` parent.

The record binds an exact coordinate basis, immutable real potential samples, positive
kinetic scale, common energy unit, and explicit source, operator, state-space,
energy-reference, and provenance identities. Fixed properties declare spinless-scalar
content and the centered-second-order stencil.

## Numeric and semantic invariants

- Potential shape is exactly `(N, N)` in `x_outer_y_inner` order.
- Potential and kinetic scale have exactly equal units.
- `c = E_K / h**2` follows the established binary64 evaluation route.
- Squared-spacing underflow/overflow, coefficient underflow/overflow, kinetic-diagonal
  overflow, and nonfinite `4*c + V[i,j]` raise `OverflowError` during construction.
- Identifiers are nonempty strings and are not reconstructed from arrays.

Potential samples are data rather than an arbitrary callable. Construction establishes
representability, not continuum convergence or scientific validity.

## Code, Sphinx, and tests

| Surface | Mapping |
|---|---|
| Class | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.py::FiniteDifferenceBlochHamiltonian2DModel` |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.rst` |
| Canonical test source | [`tests.py`](tests.py) |

| Pytest node | Evidence established |
|---|---|
| `TestFiniteDifferenceBlochHamiltonian2DModelConstruction::test_construction_retains_complete_finite_representation_metadata` | Complete metadata, fixed conventions, unit correlation, and immutability |
| `...::test_construction_rejects_potential_shape_and_unit_contradictions` | Shape and unit failures |
| `...::test_construction_rejects_unrepresentable_kinetic_stencils` | Squared-spacing, coefficient, and kinetic-diagonal range failures |
| `...::test_construction_rejects_overflow_from_kinetic_and_potential_sum` | Composed diagonal overflow failure |

`tests.py` is a relative symlink to the single runnable software-verification module;
there is no second architecture-only test implementation.

## Evidence and limitations

Tests use synthetic values at binary64 range boundaries. They do not establish
convergence, physical adequacy, scientific validation, uncertainty quantification, or
acceptance. Original local work under the repository license.
