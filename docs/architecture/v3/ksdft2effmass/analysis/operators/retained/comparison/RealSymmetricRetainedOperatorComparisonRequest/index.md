# `RealSymmetricRetainedOperatorComparisonRequest`

## Purpose and status

Prospective immutable ActionRequest binding one candidate and one reference in a
caller-declared common retained coordinate system.

```python
request = RealSymmetricRetainedOperatorComparisonRequest(
    candidate=candidate,
    reference=reference,
    coordinate_identity=coordinate_identity,
)
```

Both operands are exact `MatrixQuantity` values, exactly real symmetric, square, and
identical in shape and unit. `coordinate_identity` is an exact nonempty built-in
string. Wrong nominal types raise `TypeError`; incompatible values raise `ValueError`.

The identity records the caller's explicit declaration; the request cannot infer or
prove physical alignment from matrix entries.

Target source:
`python/src/ksdft2effmass/analysis/operators/retained/comparison.py`.
Target tests:
`python/tests/ksdft2effmass/analysis/operators/retained/test__RealSymmetricRetainedOperatorComparisonRequest.py`.
All mappings are prospective.
