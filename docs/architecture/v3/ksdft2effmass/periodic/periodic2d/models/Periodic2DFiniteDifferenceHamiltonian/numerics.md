# `Periodic2DFiniteDifferenceHamiltonian` numerics

## Grid and ordering

For odd grid size \(N\ge5\), the period is \(L=2\pi\), spacing is \(h=L/N\), and
sampled coordinates are

\[
x_j=jh,\qquad j=0,\ldots,N-1.
\]

The periodic endpoint is not duplicated. Two-dimensional sites use `x`-outer,
`y`-inner order, so the represented dimension is \(N^2\).

## One-dimensional kinetic block

For one reduced momentum component \(\kappa\), the centered representation of
\(-d^2/dx^2\) has

\[
K_{jj}=\frac{2}{h^2},\qquad
K_{j,j+1}=K_{j+1,j}=-\frac{1}{h^2}
\]

for interior neighbors. The periodic seam is

\[
K_{0,N-1}=-\frac{1}{h^2}e^{-i\kappa L},\qquad
K_{N-1,0}=-\frac{1}{h^2}e^{+i\kappa L}.
\]

The seam entries are conjugates for real finite \(\kappa\), preserving exact matrix
Hermiticity in the constructed binary64 array.

## Two-dimensional kinetic operator

With coordinate order fixed above, the kinetic matrix is the Kronecker sum

\[
K=K_x\otimes I_y+I_x\otimes K_y.
\]

No mixed kinetic derivative is introduced.

## Sampled potential

At grid point \((x_j,y_l)\), the diagonal potential is

\[
V_{jl}=\lambda_x\cos x_j+\lambda_y\cos y_l
+\lambda_{xy}\cos x_j\cos y_l.
\]

The sampled square array is flattened in C order, matching `x`-outer, `y`-inner site
enumeration, and inserted as a diagonal matrix.

## Numeric type and invariants

The represented matrix uses binary64 complex entries. The result requires:

- nonempty square shape;
- finite entries;
- exact binary-array Hermiticity; and
- shape exactly \(N^2\times N^2\).

The second-order stencil has discretization error. These invariants do not estimate that
error or establish grid convergence.
