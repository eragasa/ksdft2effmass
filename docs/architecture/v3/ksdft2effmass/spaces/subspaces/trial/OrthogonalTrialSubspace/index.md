# `OrthogonalTrialSubspace`

## Purpose and status

`OrthogonalTrialSubspace` is a prospective immutable DataObject for an orthonormal
column injection selected independently of eigensolution. Its distinct nominal type
prevents a prescribed analytical trial space from being mislabeled as an
`OrthogonalSpectralSubspace`.

## Public contract

```python
from ksdft2effmass.spaces.subspaces.trial import OrthogonalTrialSubspace
```

```python
OrthogonalTrialSubspace(basis_vectors: MatrixQuantity)
```

Planned read-only properties expose `full_dimension` and `retained_dimension`.
`projector()` materializes `J @ J.T` only at an explicit caller boundary.

## Invariants and failure behavior

- `basis_vectors` is an exact unitless `MatrixQuantity`;
- its shape is `N` by `K` with `1 <= K <= N`; and
- `basis_vectors.T @ basis_vectors` agrees with `I_K` under the explicit tolerance in
  [`../numerics.md`](../numerics.md).

Wrong nominal types raise `TypeError`; unit, shape, or orthonormality failures raise
`ValueError`.

## Scientific boundary

The type establishes a numerical orthogonal subspace and a coordinate injection. It
does not establish Hamiltonian invariance, spectral optimality, continuum convergence,
or physical identification.

## Mapping and evidence

- Target source: `python/src/ksdft2effmass/spaces/subspaces/trial.py`
- Target tests: `python/tests/ksdft2effmass/spaces/subspaces/test__OrthogonalTrialSubspace.py`
- Target Sphinx page: `doc/sphinx/api/ksdft2effmass/spaces/subspaces/trial.rst`

All mappings are prospective. No implementation or verification evidence exists yet.
