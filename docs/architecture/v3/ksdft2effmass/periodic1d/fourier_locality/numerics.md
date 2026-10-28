# Numerical contract

## Exact parent and units

The package composes the fixed parent

\[
K(q)=T_0+e^{2\pi iq}T_{+1}+e^{-2\pi iq}T_{+1}^{\dagger},
\qquad H(q)=\lambda_0(K(q)),
\]

with exact rational matrix coefficients, standard `C^4` basis, hopping scale one, and
energy reference `E_ref = 1`. Matrix entries are exact dimensionless ratios to
`E_ref`; represented energies have units `E_ref`.

## Frozen finite inventories

Construction meshes are `N=(32,64,128,256)` with production `N=256`. The common
1025-point Mathieu-scaled stagger is exactly disjoint from every construction mesh.
Complete cyclic representatives are `-N/2,...,N/2-1`; ordinary supports are
`S_R={-R,...,R}` for every `R=0,...,15`. The cyclic Nyquist representative is never
assigned ordinary hopping meaning.

## Transform and error channels

For complete interpolant `I_N` and transform-mediated truncation `T_(N,R)`, the package
retains maximum and root-mean-square forms of

\[
H-I_N,\qquad I_N-T_{N,R},\qquad H-T_{N,R}.
\]

These are interpolation, deliberate-truncation, and total channels. Their residuals
telescope pointwise, but their summarized norms are not added as identities. The
verifier reconstructs each channel and checks the applicable triangle inequality.

The equal-weight direct fit uses the same Hermitian support. Its total evaluation error
and transform/direct defects remain separate from the three transform-mediated channels.

## Gates and decisions

- sampled first-to-second gap on the declared production/evaluation union:
  `>= 0.25 E_ref`;
- producer/verifier mixed absolute-relative comparison: `1e-12` in declared units;
- final `N=128` to `N=256` stability: `1e-10` on named normalized operands;
- production application threshold: `1e-8 E_ref`;
- first passage: least support where both mediated and direct total maximum errors pass;
- sustained qualification: every later declared support also passes; and
- finite error--complexity objectives: `(2*R+1, mediated total evaluation error)`,
  evaluated separately for each construction mesh.

Unknown values, nonfinite values, threshold-side disagreement, incomplete inventories,
and failed correlations are fail-closed.

## Numerical claim boundary

All sampled eigenvalues, gaps, coefficients, errors, masks, and decisions are binary64
finite results. They are not exact reals, interval certificates, continuum errors, or
uncertainty estimates. Exact formulas and exact mesh definitions do not make their
runtime values mathematically exact.

The complete frozen values are recorded in the calculation's
[`numerical-control-decision.md`](../../../../../../calculations/periodic1d/rank1/fourier-locality/numerical-control-decision.md).
