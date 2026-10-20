# Implementation

## Target module

```text
python/src/ksdft2effmass/spaces/subspaces/trial.py
```

The target module contains five public top-level classes and no private orchestration
framework:

```text
SampledTrialFrame                         DataObject
OrthogonalTrialSubspace                   DataObject
SymmetricGramOrthonormalizationRequest    ActionRequest
SymmetricGramOrthonormalizationResult     ResultObject
SymmetricGramOrthonormalizer              Request-bound ActionObject
```

All objects are frozen, slotted records. The request binds one sampled frame. The
action retains exactly one request and exposes no method for replacing it.

## Action flow

`SymmetricGramOrthonormalizer(request).orthonormalize()` performs:

1. exact nominal validation of `SymmetricGramOrthonormalizationRequest` at action
   construction;
2. extraction of the request's validated `SampledTrialFrame`;
3. construction of `G = S.T @ S`;
4. real-symmetric eigendecomposition of `G`;
5. rejection unless every eigenvalue is strictly positive;
6. construction of `G^{-1/2}` from the retained eigensystem;
7. construction of `J = S @ G^{-1/2}`;
8. construction and validation of `OrthogonalTrialSubspace(J)`; and
9. return of one immutable result retaining the exact request, `G`, `G^{-1/2}`, and
   the orthogonal trial subspace.

The module must not silently call a pseudoinverse, discard a direction, change retained
dimension, or apply a regularization threshold.

## Dependencies

Permitted direct dependencies are:

- `numpy`;
- `ksdft2effmass.operators.quantities.MatrixQuantity`; and
- `ksdft2effmass.operators.quantities.Unitless`.

Forbidden direct dependencies include `analysis`, `model_systems`, `experiments`,
`calculations`, `campaigns`, serializers, provenance, plotting, and filesystem APIs.

## Public export boundary

The defining module is the first target import route. A package-root re-export is not
selected by this document. Any later export requires synchronized source, Sphinx, and
package-export tests.

## Test strategy

Direct tests must cover shape validation, Boolean and wrong nominal rejection where
applicable, unit rejection, positive-definite Gram construction, exact rejection of a
rank-deficient frame, result immutability, and the orthonormality of `J` under the
explicit tolerance documented in [numerics](numerics.md).
