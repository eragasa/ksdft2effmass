# `OrthogonalSubspaceComparisonRequest`

## Purpose and status

Prospective immutable ActionRequest binding candidate and reference orthogonal
subspaces.

```python
request = OrthogonalSubspaceComparisonRequest(
    candidate=candidate,
    reference=reference,
)
```

Each field accepts the explicit union
`OrthogonalTrialSubspace | OrthogonalSpectralSubspace`. Both must have the same full
and retained dimensions. Wrong nominal types raise `TypeError`; dimension disagreement
raises `ValueError`.

The request does not infer correspondence for unequal dimensions and carries no norm,
tolerance, or threshold.

Target source: `python/src/ksdft2effmass/analysis/subspaces/comparison.py`.
Target tests: `python/tests/ksdft2effmass/analysis/subspaces/test__OrthogonalSubspaceComparisonRequest.py`.
All mappings are prospective.
