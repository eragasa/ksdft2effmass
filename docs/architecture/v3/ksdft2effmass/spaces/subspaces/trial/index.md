# `ksdft2effmass.spaces.subspaces.trial`

## Purpose and status

This prospective module owns typed sampled trial frames, orthogonal trial subspaces,
and one symmetric Gram orthonormalization action. It supplies reusable finite-matrix
operands without selecting a physical model or a diagnostic suite.

Target source:

`python/src/ksdft2effmass/spaces/subspaces/trial.py`

No source module, supported import, or public export exists yet.

## Contract inventory

| Symbol | Role | Status |
|---|---|---|
| [`SampledTrialFrame`](SampledTrialFrame/index.md) | Immutable unitless sampled `N`-by-`K` frame | Prospective |
| [`OrthogonalTrialSubspace`](OrthogonalTrialSubspace/index.md) | Immutable orthonormal trial-space injection | Prospective |
| [`SymmetricGramOrthonormalizationRequest`](SymmetricGramOrthonormalizationRequest/index.md) | Immutable request binding one sampled frame | Prospective |
| [`SymmetricGramOrthonormalizationResult`](SymmetricGramOrthonormalizationResult/index.md) | Immutable factorization and output record | Prospective |
| [`SymmetricGramOrthonormalizer`](SymmetricGramOrthonormalizer/index.md) | Request-bound symmetric Gram orthonormalization action | Prospective |

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Ownership boundary

The module owns semantic type enforcement and the map

$$
G=S^{\mathsf T}S,
\qquad
J=SG^{-1/2}.
$$

It does not own sampled sine or Hermite construction, spectral eigensolution,
Hamiltonian reduction, matrix norms, study aggregation, serialization, provenance, or
acceptance policy.

## Failure behavior

Wrong nominal types raise `TypeError`. Invalid shapes, non-unitless vectors,
non-positive-definite Gram matrices, or failed orthonormality conditions raise
`ValueError`. No rank truncation, pseudoinverse, or regularization is selected
implicitly.

## Code, tests, and Sphinx mapping

| Surface | Target mapping | Current status |
|---|---|---|
| Source | `python/src/ksdft2effmass/spaces/subspaces/trial.py` | Absent |
| Tests | `python/tests/ksdft2effmass/spaces/subspaces/test__SampledTrialFrame.py` and class peers | Absent |
| Sphinx | `doc/sphinx/api/ksdft2effmass/spaces/subspaces/trial.rst` | Absent |

## Provenance and evidence

Original local design under the repository license. The equations are elementary
finite-dimensional linear algebra. Software and numerical verification are not yet
evaluated; scientific validation, uncertainty quantification, and human acceptance are
not established by this prospective architecture.
