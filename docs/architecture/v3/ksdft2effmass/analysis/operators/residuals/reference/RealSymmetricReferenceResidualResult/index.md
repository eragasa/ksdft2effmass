# `RealSymmetricReferenceResidualResult`

## Purpose and status

Prospective immutable ResultObject retaining:

```python
request: RealSymmetricReferenceResidualRequest
residual: MatrixQuantity
```

The residual has shape `N` by `K` and the operator's unit. The result retains no scalar
norm, threshold, error attribution, or disposition. No package-level serializer is
selected.

Target source: `python/src/ksdft2effmass/analysis/operators/residuals/reference.py`.
Target tests: `python/tests/ksdft2effmass/analysis/operators/residuals/test__RealSymmetricReferenceResidualResult.py`.
All mappings are prospective.
