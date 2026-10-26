# Numerical contract

## Representations

The analytical subject is the real-line oscillator. The finite subject is an interior
matrix on a symmetric finite interval with homogeneous Dirichlet boundary data and
second-order centered differences. These are different operators and state spaces.

For realized spacing `h`, analytical samples are scaled by `sqrt(h)`. If `S` is the
sample matrix and `G = S.T @ S`, the injection is

\[
J = S G^{-1/2}.
\]

A non-positive Gram eigenvalue is rejected; no regularization policy is inferred.
The common-coordinate difference is

\[
\Delta_K = J^{\mathsf T}H_{b,h}J-D_K.
\]

All maintained successor calculations use binary64 arrays, row-major ordering,
increasing interior coordinates, and increasing number-state order. Production
Frobenius diagnostics are evaluated by
`projectkoios.physkit.linalg.matrix.norm.FrobeniusMatrixNorm`.

## Adjacent-grid diagnostic

For adjacent authored spacings whose realized values satisfy
`h_coarse > h_fine`, fixed box half-width `b`, and fixed retained dimension `K`, the
ported diagnostic is

\[
C_{b,K}(h_{\mathrm{coarse}},h_{\mathrm{fine}})
=
\left\|
J_{\mathrm{coarse}}^{\mathsf T}H_{b,h_{\mathrm{coarse}}}J_{\mathrm{coarse}}
-
J_{\mathrm{fine}}^{\mathsf T}H_{b,h_{\mathrm{fine}}}J_{\mathrm{fine}}
\right\|_{\mathrm F}.
\]

The two finite spatial matrices act in different grid spaces and are never subtracted
directly. Their pullbacks act in the same ordered retained number-state coordinates,
which makes the displayed subtraction well-defined. The norm is evaluated only by
`projectkoios.physkit.linalg.matrix.norm.FrobeniusMatrixNorm`.

This is an adjacent-representation change diagnostic. Without an extrapolation model,
regularity assumptions, or an independently justified asymptotic regime, it is not a
continuum error estimate, convergence rate, uncertainty, or acceptance criterion.

## Independent route

Production analytical states use the maintained three-term recurrence. Independent
verification evaluates `scipy.special.eval_hermite` with factorial normalization.
Production finite Hamiltonians compose operator owners; verification constructs their
tridiagonal entries directly and retains direct NumPy Frobenius reductions. Both routes
explicitly align finite-eigenvector signs to analytical samples before comparison.

The verification tolerances bound software-route differences. They are not continuum
error bars or physical uncertainty estimates.

## Serialization

Arrays and quantities are serialized only by the shared typed-value codec with dtype,
shape, unit, and representation metadata. Constructors re-establish local and
cross-record shape, ordering, unit, and sweep invariants after decoding.
