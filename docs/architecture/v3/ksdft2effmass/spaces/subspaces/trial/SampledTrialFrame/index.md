# `SampledTrialFrame`

## Purpose and status

`SampledTrialFrame` is a prospective immutable DataObject for one caller-constructed,
unitless sampled frame before orthonormalization. It does not assert linear
independence, orthogonality, spectral provenance, or scientific adequacy.

## Public contract

Target defining route:

```python
from ksdft2effmass.spaces.subspaces.trial import SampledTrialFrame
```

Target constructor:

```python
SampledTrialFrame(vectors: MatrixQuantity)
```

Read-only derived properties expose full dimension `N` and retained dimension `K`.

## Invariants and failure behavior

- `vectors` is exactly `MatrixQuantity`;
- its unit is `Unitless`;
- its shape is `N` by `K` with `1 <= K <= N`;
- storage finiteness and immutability remain owned by `MatrixQuantity`.

Wrong nominal types raise `TypeError`; incompatible units or shapes raise `ValueError`.
Rank deficiency is not rejected here because it is established by the Gram
factorization action.

## Dependencies and boundary

The class depends only on operator quantity records. It owns no model identity,
coordinates, quadrature rule, Hamiltonian, norm, serializer, or provenance.

## Mapping and evidence

- Target source: `python/src/ksdft2effmass/spaces/subspaces/trial.py`
- Target tests: `python/tests/ksdft2effmass/spaces/subspaces/test__SampledTrialFrame.py`
- Target Sphinx page: `doc/sphinx/api/ksdft2effmass/spaces/subspaces/trial.rst`

All mappings are prospective. No implementation or verification evidence exists yet.
