# `RealSymmetricReferenceResidualRequest`

## Purpose and status

Prospective immutable ActionRequest binding one finite real-symmetric operator, one
orthogonal trial subspace, and one retained real-symmetric reference.

```python
request = RealSymmetricReferenceResidualRequest(
    operator=operator,
    trial_subspace=trial_subspace,
    reference=reference,
)
```

The operator has shape `N` by `N`; the trial injection has shape `N` by `K`; the
reference has shape `K` by `K`. Operator and reference units agree. Operator and
reference are exactly real symmetric. Wrong nominal types raise `TypeError`; shape,
unit, or symmetry disagreement raises `ValueError`.

Target source: `python/src/ksdft2effmass/analysis/operators/residuals/reference.py`.
Target tests: `python/tests/ksdft2effmass/analysis/operators/residuals/test__RealSymmetricReferenceResidualRequest.py`.
All mappings are prospective.
