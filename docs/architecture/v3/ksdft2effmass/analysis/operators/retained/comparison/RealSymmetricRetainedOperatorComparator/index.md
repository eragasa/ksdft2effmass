# `RealSymmetricRetainedOperatorComparator`

## Purpose and status

Prospective immutable request-bound ActionObject comparing exactly two compatible
retained operators.

```python
result = RealSymmetricRetainedOperatorComparator(request).compare()
```

The constructor accepts only `RealSymmetricRetainedOperatorComparisonRequest`.
`compare()` accepts no arguments and returns a result retaining the same request.
The fixed sign convention is `candidate - reference`.

The comparator does not align coordinates, choose a norm, calculate a residual against
an ambient operator, or orchestrate other diagnostics.

Target source:
`python/src/ksdft2effmass/analysis/operators/retained/comparison.py`.
Target tests:
`python/tests/ksdft2effmass/analysis/operators/retained/test__RealSymmetricRetainedOperatorComparator.py`.
All mappings are prospective.
