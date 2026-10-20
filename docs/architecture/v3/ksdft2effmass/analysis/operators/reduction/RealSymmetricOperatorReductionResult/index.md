# `RealSymmetricOperatorReductionResult`

## Purpose and status

Prospective immutable ResultObject retaining one reduction request and its coordinate,
projector, embedded-operator, and invariance-residual matrices.

The result retains:

```python
request: RealSymmetricOperatorReductionRequest
coordinates: MatrixQuantity
projector: MatrixQuantity
embedded: MatrixQuantity
invariance_residual: MatrixQuantity
```

Shapes and units follow [`../numerics.md`](../numerics.md). The result contains no scalar
norm or acceptance classification. It retains the exact request for correlation.

No package-level serializer is selected.

Target source: `python/src/ksdft2effmass/analysis/operators/reduction.py`.
Target tests: `python/tests/ksdft2effmass/analysis/operators/test__RealSymmetricOperatorReductionResult.py`.
All mappings are prospective.
