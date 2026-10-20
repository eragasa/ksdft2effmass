# `RealSymmetricOperatorReducer`

## Purpose and status

Prospective immutable request-bound ActionObject for one orthogonal operator reduction.

```python
result = RealSymmetricOperatorReducer(request).reduce()
```

The constructor requires exactly `RealSymmetricOperatorReductionRequest`; wrong type
raises `TypeError`. `reduce()` accepts no arguments and returns
`RealSymmetricOperatorReductionResult` retaining the same request.

The reducer owns only the matrices in [`../numerics.md`](../numerics.md). It does not
choose a subspace, compare a reference, calculate norms, or orchestrate diagnostics.

Target source: `python/src/ksdft2effmass/analysis/operators/reduction.py`.
Target tests: `python/tests/ksdft2effmass/analysis/operators/test__RealSymmetricOperatorReducer.py`.
All mappings are prospective.
