# Numerical contract

## Shapes and arithmetic

For `S` with shape `N` by `K`, construction requires

$$
1 \le K \le N.
$$

All represented values use `numpy.float64`. `MatrixQuantity` supplies immutable finite
storage. The frame and resulting injection use `Unitless`; physical or quadrature units
must be removed by the model-specific producer before `SampledTrialFrame` construction.

## Gram factorization

The action computes

$$
G=S^{\mathsf T}S
$$

and uses a real-symmetric eigendecomposition

$$
G=V\operatorname{diag}(\gamma_1,\ldots,\gamma_K)V^{\mathsf T}.
$$

Every `gamma_i` must be strictly positive. The inverse square root is

$$
G^{-1/2}
=V\operatorname{diag}(\gamma_1^{-1/2},\ldots,\gamma_K^{-1/2})V^{\mathsf T},
$$

and

$$
J=SG^{-1/2}.
$$

No condition-number cutoff or eigenvalue clipping is selected. If later callers need
regularization, that is a separate numerical policy and action contract.

## Orthonormality validation

`OrthogonalTrialSubspace` should use the same explicit binary64 policy already used by
`OrthogonalSpectralSubspace` unless implementation evidence requires a separately
reviewed rule:

$$
\lVert J^{\mathsf T}J-I_K\rVert_{\max}
\le 128\,\epsilon_{64}\max(N,K).
$$

This tolerance validates a finite numerical invariant. It does not establish
conditioning, continuum orthogonality, quadrature convergence, or scientific adequacy.

## Conditioning

The result retains `G` and `G^{-1/2}` so outward experiments can calculate condition
numbers or correction sizes explicitly. This leaf action does not classify a frame as
scientifically acceptable from a condition number.

## Resource behavior

The Gram matrix and its factorization require `O(N K^2 + K^3)` arithmetic and `O(K^2)`
additional dense storage beyond the input and output frames. The action does not form
an `N`-by-`N` projector.
