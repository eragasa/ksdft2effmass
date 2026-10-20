# `SymmetricGramOrthonormalizationRequest`

## Purpose and status

`SymmetricGramOrthonormalizationRequest` is a prospective immutable ActionRequest that
binds one validated sampled trial frame to one orthonormalization action instance.

## Public contract

```python
from ksdft2effmass.spaces.subspaces.trial import (
    SymmetricGramOrthonormalizationRequest,
)
```

```python
request = SymmetricGramOrthonormalizationRequest(sampled_frame=frame)
```

The sole field is:

```python
sampled_frame: SampledTrialFrame
```

## Invariants and failure behavior

The field must have the exact nominal `SampledTrialFrame` type. Wrong type raises
`TypeError`. Shape, units, and finite-storage invariants are already owned by the
sampled frame and are not duplicated in this request.

## Action correlation

`SymmetricGramOrthonormalizer(request)` retains this exact immutable request.
`orthonormalize()` accepts no arguments, and
`SymmetricGramOrthonormalizationResult.request` retains the same request for audit and
correlation.

## Boundary

The request contains no factorization tolerance, regularization policy, rank-selection
policy, path, schema, provenance, or model identity.

## Mapping and evidence

- Target source: `python/src/ksdft2effmass/spaces/subspaces/trial.py`
- Target tests: `python/tests/ksdft2effmass/spaces/subspaces/test__SymmetricGramOrthonormalizationRequest.py`
- Target Sphinx page: `doc/sphinx/api/ksdft2effmass/spaces/subspaces/trial.rst`

All mappings are prospective. No implementation or verification evidence exists yet.
