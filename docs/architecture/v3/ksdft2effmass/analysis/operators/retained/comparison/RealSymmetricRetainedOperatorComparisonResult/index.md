# `RealSymmetricRetainedOperatorComparisonResult`

## Purpose and status

Prospective immutable ResultObject retaining the request and three signed matrices:

```python
request: RealSymmetricRetainedOperatorComparisonRequest
difference: MatrixQuantity
diagonal_difference: MatrixQuantity
off_diagonal_difference: MatrixQuantity
```

The matrices share the request's shape and unit and satisfy
`difference == diagonal_difference + off_diagonal_difference` up to the exact
binary64 construction performed by the comparator.

No norm, normalized score, threshold, or disposition is retained. No package-level
serializer is selected.

Target source:
`python/src/ksdft2effmass/analysis/operators/retained/comparison.py`.
Target tests:
`python/tests/ksdft2effmass/analysis/operators/retained/test__RealSymmetricRetainedOperatorComparisonResult.py`.
All mappings are prospective.
