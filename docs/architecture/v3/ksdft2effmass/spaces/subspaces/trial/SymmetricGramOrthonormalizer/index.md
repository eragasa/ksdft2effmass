# `SymmetricGramOrthonormalizer`

## Purpose and status

`SymmetricGramOrthonormalizer` is a prospective immutable request-bound ActionObject
implementing one symmetric Gram orthonormalization. It is not an eigensolver, subspace
selector, regularizer, or experiment orchestrator.

## Public contract

```python
from ksdft2effmass.spaces.subspaces.trial import (
    SymmetricGramOrthonormalizer,
)
```

```python
result = SymmetricGramOrthonormalizer(request).orthonormalize()
```

Constructor domain: `SymmetricGramOrthonormalizationRequest`.
Terminal method codomain: `SymmetricGramOrthonormalizationResult`.
The zero-argument `orthonormalize()` method acts only on the immutable bound request.

## Algorithm and failure behavior

For frame matrix `S`, the action constructs

$$
G=S^{\mathsf T}S,
\qquad
J=SG^{-1/2}.
$$

It rejects a non-positive-definite `G`. It does not clip eigenvalues, choose a lower
rank, form a pseudoinverse, or accept a caller tolerance. The resulting `J` must pass
`OrthogonalTrialSubspace` validation.

A wrong constructor request type raises `TypeError`; invalid Gram or output invariants
raise `ValueError`.

## Collaborators and dependency direction

The action consumes and returns only types from its defining module plus operator
quantity records. Model systems construct the sampled frame. Analyses consume the
result. Neither dependency may be reversed.

## Scientific boundary

Success proves only that one finite sampled frame admitted the declared binary64
orthonormalization. It does not prove continuum orthogonality, basis completeness,
Hamiltonian invariance, or convergence.

## Mapping and evidence

- Target source: `python/src/ksdft2effmass/spaces/subspaces/trial.py`
- Target tests: `python/tests/ksdft2effmass/spaces/subspaces/test__SymmetricGramOrthonormalizer.py`
- Target Sphinx page: `doc/sphinx/api/ksdft2effmass/spaces/subspaces/trial.rst`

All mappings are prospective. No implementation or verification evidence exists yet.
