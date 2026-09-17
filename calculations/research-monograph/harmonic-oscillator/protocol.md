# Appendix E harmonic-oscillator comparison protocol

## Evidence status

This protocol governs a **calculated illustrative numerical experiment**. It
implements the comparison defined in Appendix E without replacing that
appendix's mathematical definitions. Passing the verifier is numerical
verification of the declared finite construction; it is not semiconductor
evidence, scientific validation, or uncertainty quantification.

## Models and state spaces

The exact reference is the real-line oscillator with
$\hbar=m=\omega=\ell=1$. For retained dimension $K$, its ordered comparison
space is

$$
\mathcal K_K=\operatorname{span}\{|0\rangle,\ldots,|K-1\rangle\},
$$

and its matrix in number-state order is

$$
H_{\mathrm{lad}}^{(K)}=\operatorname{diag}(1/2,3/2,\ldots,K-1/2).
$$

The finite-box continuum operator acts on $L^2((-X,X))$ with Dirichlet
boundary conditions. Its numerical representation uses $N$ uniformly spaced
interior points, spacing $\Delta x=2X/(N+1)$, a centered second-order kinetic
stencil, and the sampled potential $x^2/2$. The grid basis is ordered by
increasing coordinate. The finite grid matrix and exact retained ladder matrix
are not subtracted directly.

## Comparison map

For each $(b,\eta,K)$, where $b=X/\ell$ and $\eta=\Delta x/\ell$, the first $K$
real-line oscillator states are sampled and quadrature-scaled to form $S$. The
injection is

$$
J=S(S^TS)^{-1/2}.
$$

The retained result identifies every map through its exact reconstruction
inputs and algorithm, shape, canonical little-endian binary64 content SHA-256,
$G=S^TS$, and $G^{-1/2}$. This path-plus-content representation avoids retaining
a dense injection array in Git. The verifier independently constructs sampled
states with SciPy's physicists' Hermite polynomials, reconstructs $J$, and checks
its content identity. The map direction is from number-state coordinates to
grid coordinates, and $J^TJ=I_K$ is checked before interpreting a Frobenius
comparison.

The represented finite-box Hamiltonian is pulled back as

$$
A_{X,h}^{(K)}=J^T H_{X,h}J.
$$

Only $A_{X,h}^{(K)}$ and $H_{\mathrm{lad}}^{(K)}$, which share the same ordered
orthonormal coordinates, are subtracted.

## Controlled sweep

The retained Cartesian sweep is:

- box half-widths $b=4,6,8$;
- grid spacings $\eta=0.2,0.1,0.05$; and
- retained dimensions $K=2,4,6$.

This design separates three questions:

1. spatial refinement holds $b$ and $K$ fixed while reducing $\eta$;
2. box expansion holds $\eta$ and $K$ fixed while increasing $b$; and
3. retained-space sensitivity compares distinct declared values of $K$ without
   treating $K$ as an error bar.

Adjacent-grid pullbacks are compared only after both have been mapped to the
same $\mathcal K_K$. The retained JSON includes every map's reconstruction
contract and content identity together with its Gram matrices, compact
common-coordinate operators, residual decomposition, and dimensions.

## Diagnostics and independent verification

For every case, the result records

- $\|G-I\|_F$ and the two-norm condition number of $G$;
- $\|J^TJ-I\|_F$;
- absolute and reference-normalized Frobenius discrepancies;
- diagonal and off-diagonal discrepancy norms; and
- the full common-coordinate difference matrix.

The verifier independently checks the grid, analytic oscillator states, Gram
matrix, symmetric inverse square root, injection, finite-difference
Hamiltonian, exact ladder energies, pullback, Hermiticity, all reported norms,
the identity

$$
D_F^2=D_{\mathrm{diag}}^2+D_{\mathrm{off}}^2,
$$

and every adjacent-grid discrepancy. It also checks the retained input and
script SHA-256 identities.

## Acceptance and interpretation boundary

A passing verifier establishes agreement with the stated finite mathematics
within the documented binary64 tolerances. Spatial refinement, box expansion,
and retained-space sensitivity are reported separately. In particular, a
smaller total discrepancy can result from cancellation between boundary and
discretization effects; it must not be interpreted as independent convergence
of both effects.

The finite box is a different continuum realization from the real-line
oscillator, the finite-difference matrix is only its numerical representation,
and changing $K$ changes the comparison space. No result here validates a
semiconductor model or supports a claim about DFT, Wannier localization,
effective masses, or impurities.
