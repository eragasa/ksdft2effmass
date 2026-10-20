# `OrthogonalSubspaceComparisonResult`

## Purpose and status

Prospective immutable ResultObject retaining:

```python
request: OrthogonalSubspaceComparisonRequest
candidate_projector: MatrixQuantity
reference_projector: MatrixQuantity
projector_difference: MatrixQuantity
```

All matrices are unitless and have the common full-space shape. The fixed sign is
`candidate_projector - reference_projector`.

The result contains no scalar distance, principal-angle classification, tolerance, or
disposition. No package-level serializer is selected.

Target source: `python/src/ksdft2effmass/analysis/subspaces/comparison.py`.
Target tests: `python/tests/ksdft2effmass/analysis/subspaces/test__OrthogonalSubspaceComparisonResult.py`.
All mappings are prospective.
