# `FiniteDifferenceBlochHamiltonian2DResult`

## Purpose and public contract

This implemented row-035 ResultObject retains one immutable energy-valued finite-
difference matrix and its complete construction request. It is supported from
`ksdft2effmass.analysis.model_systems`.

The nested request preserves grid geometry, basis normalization/order, momentum and
seam convention, potential samples, source/operator/state-space identities, energy
reference, and provenance.

## Invariants and failures

- The request has the exact reusable request type.
- Matrix shape is exactly `(N**2, N**2)`.
- Matrix unit equals the model kinetic and potential unit.
- Values are finite by `ComplexMatrixQuantity` and exactly Hermitian by this result.
- Stored complex128 bytes are non-writeable.

This is represented-space output—not the continuum operator, a retained operator,
eigensystem, convergence result, or acceptance decision.

## Code, Sphinx, and tests

| Surface | Mapping |
|---|---|
| Class | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.py::FiniteDifferenceBlochHamiltonian2DResult` |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.rst` |
| Canonical test source | [`tests.py`](tests.py) |

| Pytest node | Evidence established |
|---|---|
| `TestFiniteDifferenceBlochHamiltonian2DResultConstruction::test_construction_retains_exact_request_and_immutable_matrix` | Request identity, declared shape, and immutable storage |
| `...::test_construction_rejects_wrong_dimension_unit_and_hermiticity` | Shape, unit, and exact-Hermiticity failures |

`tests.py` is a relative symlink to the single runnable software-verification module.

## Evidence and limitations

Synthetic software tests establish intrinsic result behavior only. No convergence,
scientific validation, UQ, or acceptance follows. Original local work under the
repository license.
