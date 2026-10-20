# `RealSymmetricReferenceResidualAnalyzer`

## Purpose and status

Prospective immutable request-bound ActionObject evaluating one analytical-reference
action residual.

```python
result = RealSymmetricReferenceResidualAnalyzer(request).analyze()
```

The constructor accepts only `RealSymmetricReferenceResidualRequest`. `analyze()` takes
no arguments and returns a result retaining the same request.

The analyzer does not reduce the operator, calculate Galerkin leakage, compare
retained matrices, choose a norm, or orchestrate diagnostics.

Target source: `python/src/ksdft2effmass/analysis/operators/residuals/reference.py`.
Target tests: `python/tests/ksdft2effmass/analysis/operators/residuals/test__RealSymmetricReferenceResidualAnalyzer.py`.
All mappings are prospective.
