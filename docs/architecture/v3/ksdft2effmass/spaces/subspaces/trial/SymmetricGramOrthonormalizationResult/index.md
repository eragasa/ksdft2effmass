# `SymmetricGramOrthonormalizationResult`

## Purpose and status

`SymmetricGramOrthonormalizationResult` is a prospective immutable ResultObject that
retains the input frame, Gram matrix, symmetric inverse square root, and validated
orthogonal trial subspace from one orthonormalization action.

## Public contract

```python
from ksdft2effmass.spaces.subspaces.trial import (
    SymmetricGramOrthonormalizationResult,
)
```

The constructor is owned by the result invariant and normally called by
`SymmetricGramOrthonormalizer`.

## State and invariants

The result retains:

- `request: SymmetricGramOrthonormalizationRequest`;
- `gram_matrix: MatrixQuantity` with shape `K` by `K` and `Unitless`;
- `gram_inverse_square_root: MatrixQuantity` with shape `K` by `K` and `Unitless`; and
- `trial_subspace: OrthogonalTrialSubspace` with shape `N` by `K`.

The sampled frame is reached through `request.sampled_frame`. All dimensions must
correlate. The record does not retain a scalar condition number,
norm, threshold, or acceptance disposition; outward analyses may derive those from the
retained matrices.

## Serialization and boundary

No wire format or serializer is selected. Calculation owners may serialize the fields
they explicitly adopt without making that shape a package-level schema.

## Mapping and evidence

- Target source: `python/src/ksdft2effmass/spaces/subspaces/trial.py`
- Target tests: `python/tests/ksdft2effmass/spaces/subspaces/test__SymmetricGramOrthonormalizationResult.py`
- Target Sphinx page: `doc/sphinx/api/ksdft2effmass/spaces/subspaces/trial.rst`

All mappings are prospective. No implementation or verification evidence exists yet.
