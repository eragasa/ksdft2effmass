# `RealSymmetricOperatorReductionRequest`

## Purpose and status

Prospective immutable ActionRequest binding one finite real-symmetric operator and one
orthogonal subspace.

```python
request = RealSymmetricOperatorReductionRequest(
    operator=operator,
    subspace=subspace,
)
```

`operator` is `MatrixQuantity | SparseMatrixQuantity`. `subspace` is the explicit union
`OrthogonalTrialSubspace | OrthogonalSpectralSubspace`. The operator must be exactly
real symmetric, have shape `N` by `N`, and agree with the subspace full dimension.
Wrong nominal types raise `TypeError`; shape or symmetry failures raise `ValueError`.

The request contains no norm, threshold, path, schema, or scientific disposition.

Target source: `python/src/ksdft2effmass/analysis/operators/reduction.py`.
Target tests: `python/tests/ksdft2effmass/analysis/operators/test__RealSymmetricOperatorReductionRequest.py`.
All mappings are prospective.
