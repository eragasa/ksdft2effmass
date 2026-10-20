# `OrthogonalSubspaceComparator`

## Purpose and status

Prospective immutable request-bound ActionObject comparing exactly two compatible
orthogonal subspaces.

```python
result = OrthogonalSubspaceComparator(request).compare()
```

The constructor accepts only `OrthogonalSubspaceComparisonRequest`. `compare()` accepts
no arguments and returns a result retaining the same request.

The comparator materializes and subtracts projectors. It does not compare individual
columns, calculate norms, choose thresholds, or orchestrate diagnostics.

Target source: `python/src/ksdft2effmass/analysis/subspaces/comparison.py`.
Target tests: `python/tests/ksdft2effmass/analysis/subspaces/test__OrthogonalSubspaceComparator.py`.
All mappings are prospective.
