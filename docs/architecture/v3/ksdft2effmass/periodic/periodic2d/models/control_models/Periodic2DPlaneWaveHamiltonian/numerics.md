# `Periodic2DPlaneWaveHamiltonian` numerics

## Model and basis

The dimensionless control Hamiltonian is

\[
H(\boldsymbol\kappa)
= \lVert \boldsymbol\kappa-i\nabla\rVert^2
+ \lambda_x\cos x
+ \lambda_y\cos y
+ \lambda_{xy}\cos x\cos y.
\]

The direct lattice is \(A=2\pi I\), the two-pi-dual reciprocal lattice is \(B=I\),
and the reduced momentum is
\(\boldsymbol\kappa=(\kappa_x,\kappa_y)\). The finite basis is

\[
\mathcal B_C=\{(p,q)\in\mathbb Z^2:-C\le p,q\le C\},
\]

with `p`-outer, `q`-inner order and represented dimension \((2C+1)^2\).

## Kinetic diagonal

For basis pair \((p,q)\), the kinetic diagonal is

\[
(\kappa_x+p)^2+(\kappa_y+q)^2.
\]

The kinetic scale is the exact dimensionless scalar one. No factor of one half, energy
shift, or implicit unit conversion is introduced.

## Potential Fourier coefficients

The nonzero Fourier coefficients are derived analytically:

\[
\cos x=\tfrac12(e^{ix}+e^{-ix}),\qquad
\cos y=\tfrac12(e^{iy}+e^{-iy}),
\]

and

\[
\cos x\cos y
=\tfrac14\sum_{s_x,s_y\in\{-1,1\}}e^{i(s_xx+s_yy)}.
\]

Therefore:

- displacements \((\pm1,0)\) carry \(\lambda_x/2\);
- displacements \((0,\pm1)\) carry \(\lambda_y/2\); and
- displacements \((\pm1,\pm1)\) carry \(\lambda_{xy}/4\).

No unlisted coefficient is inferred. Couplings that leave the finite square basis are
absent from that finite representation; the operation performs no subsequent support
truncation.

## Provider adaptation

The operation composes a `PlaneWaveBlochHamiltonian2DModel` with explicit identifiers:

- state space: `periodic2d.cosine.spinless_scalar`;
- basis: `periodic2d.cosine.p_outer_q_inner`; and
- energy reference: `periodic2d.cosine.model_zero`.

Project Koios constructs the matrix and evaluates the maximum component of the
`A^T B - 2*pi*I` duality residual. KSD copies only the represented matrix magnitude and
that residual into its correlated result.

## Numeric type and invariants

The represented matrix uses binary64 complex entries. The result requires:

- nonempty square shape;
- finite entries;
- exact binary-array Hermiticity;
- dimension equal to \((2C+1)^2\); and
- duality residual no larger than the request tolerance.

These checks establish finite-representation software behavior only.
