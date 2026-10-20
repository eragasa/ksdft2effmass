# `ksdft2effmass.analysis.operators.reduction`

## Purpose and status

This prospective module reduces one finite real-symmetric operator through one typed
orthogonal subspace. It owns the reduction and invariance-residual matrices, not their
norms or experimental interpretation.

Target source: `python/src/ksdft2effmass/analysis/operators/reduction.py`.
No implementation or supported import exists yet.

## Contract inventory

| Symbol | Role |
|---|---|
| [`RealSymmetricOperatorReductionRequest`](RealSymmetricOperatorReductionRequest/index.md) | Immutable operator/subspace ActionRequest |
| [`RealSymmetricOperatorReductionResult`](RealSymmetricOperatorReductionResult/index.md) | Immutable reduction ResultObject |
| [`RealSymmetricOperatorReducer`](RealSymmetricOperatorReducer/index.md) | Request-bound ActionObject with `reduce()` |

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Ownership boundary

The module accepts either an `OrthogonalTrialSubspace` or an
`OrthogonalSpectralSubspace`. It does not construct either subspace, solve eigenpairs,
select retained dimension, compare against a reference, choose a norm, or aggregate a
study.

## Existing-owner relationship

Existing `operators.subspaces.OperatorCompression` already owns spectral-subspace
compression. Implementation must resolve that overlap by reviewed generalization or
replacement; it must not leave two public implementations of the same spectral
compression behavior.

## Evidence

Prospective architecture only. Software verification, numerical verification,
scientific validation, uncertainty quantification, and human acceptance are not yet
established.
