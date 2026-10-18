# HSH-1 numerical contract

## Scalar and collection types

Public numeric inputs must be exact built-in `float` or `int` values as declared.
Booleans, numeric strings, NumPy scalar impostors, NaNs, and infinities are rejected.
Maintained HSH collections use immutable tuples. External quadratic adapters may use
private NumPy arrays or private SciPy CSR storage; their public dense matrix is a tuple
and their public sparse matrix is a defensive CSR copy.

## Ordering and finite geometry

The source mesh size is odd. Centered representatives are ordered lexicographically
after generating $[-n,\ldots,n]^2$. Each PhysKit-provided $D_4$ orbit has one canonical integer representative. HSH selects
and verifies ordering by squared radius and then representative. Every shell mask is a
prefix in that orbit ordering and contains complete orbits.

The maximal coefficient box uses the exact-pinned
`projectkoios.optimization.ParameterSpace` contract. Its ordered unique names must equal
the canonical orbit identities. The common box has strict bounds around zero; a derived
shell slice retains those bounds for active coordinates and uses equal bounds `[0, 0]`
for every inactive coordinate. Inclusive membership is exact at the stored binary64
bounds. A solver tolerance diagnoses a candidate before exact projection and never
widens a fixed bound.

The target package must reconstruct rather than trust:

- orbit closure, disjointness, and complete coverage of the finite domain;
- multiplicity sum equal to the block count;
- nested shell masks and the full final shell;
- real projected target and one common energy zero; and
- exact zero inactive coefficients in every embedded point; and
- exact correlation among orbit order, `ParameterSpace` names, common bounds, and every
  derived fixed-coordinate shell slice.

“Exact real projected target” means that every retained orbit value is one built-in
float, has no stored imaginary component, and is copied identically to every block in
that orbit. It does not mean exact real arithmetic. The input builder must freeze its
canonical member order and finite summation rule; producer and verifier independently
reconstruct the resulting binary64 values and projection defects.

## Quadratic representation

Each channel loss restricted to active coordinates is retained as

$$
q(z)=(z-c)^TQ(z-c)+m.
$$

The exact-pinned Optimization-owned
`projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss` owns the finite
unit-free center, symmetric positive-definite matrix, nonnegative finite minimum squared
loss, Optimization scalar validation, backend selection, `matrix` property,
`squared_loss(coordinates)`, and `root_loss(coordinates)`. HSH supplies only explicitly
normalized unit-free canonical coordinates and retains whether `sparse=False` NumPy
dense or `sparse=True` SciPy CSR behavior was selected.

The HSH-local `Periodic2DHoppingShellQuadraticLoss` owns the energy unit and scale
$E_G$, shell identity, channel, strictly increasing active maximal-space indices, exact
inactive-zero rule, and nonnegative reconstruction/correlation defects. Solver
feasibility defects are retained separately and cannot relax class membership. Its
`squared_loss(maximal_coefficients)` validates the energy-coefficient embedding,
forms the ordered ratios $z=c_{\mathrm{active}}/E_G$, and delegates those ratios to the
shared facade. The dense adapter requires successful NumPy Cholesky acceptance; the
sparse adapter requires a finite strictly positive smallest algebraic eigenvalue from
SciPy ARPACK and fails closed on nonconvergence. HSH additionally requires that an
independently reconstructed curvature lower bound exceed a prospectively frozen margin;
the HSH margin does not weaken the adapter invariant or turn backend acceptance into an
exact certificate.

A channel is nonempty only if its quadratic sublevel intersects the active slice of the
coefficient box. Unconstrained minimum feasibility is insufficient when the center lies
outside the box. The producer may use a deterministic bounded convex solver. The
verifier must independently enclose the box-constrained minimum: an outward lower bound
above threshold proves emptiness, while an explicit point at or below threshold proves
nonemptiness. If neither proof closes within the frozen arithmetic policy, the class is
`invalid-premise` rather than guessed empty or nonempty.

## Metric and dual norm

All classes use the same diagonal metric
$M_{oo}=m_o/(E_G^2|\mathcal R_{\max}|)$. Because this metric carries inverse-energy
squared dimensions before coefficient contraction and has hopping/Frobenius meaning,
its reusable typed representation belongs to PhysKit. HSH selects $E_G$, the comparison
domain, and the scientific role; unit-free optimization receives only the resulting
nondimensionalized coordinates and metric values. No class-dependent normalization is
allowed.
A support-certificate direction must be nonzero, finite, and dimensionless in the
maximal coefficient ordering. Its dual norm $\sqrt{u^TM^{-1}u}$ has the coefficient
energy unit, as do directional support endpoints and gaps. Directions may be normalized
for storage, but the verifier must reconstruct scale invariance.

## Lower and upper bounds

A constructive upper bound is rounded upward after both feasible points are verified.
A support lower bound uses outward-rounded conservative support endpoints and is rounded
downward. Required inequalities are

$$
0\le\underline\delta_k\le\delta_k^*\le\overline\delta_k.
$$

A recorded binary64 value near zero does not prove compatibility. Only a common point
whose reconstructed channel losses satisfy both thresholds under the frozen outward
tolerance can establish the compatible disposition.

The exact directed-rounding implementation remains a pre-freeze decision. Candidate
implementations must state arithmetic precision, rounding mode, transcendental/square-
root treatment, serialization conversion, and platform assumptions. Plain binary64
re-evaluation without a conservative error envelope is not a certificate.

## Training and withheld roles

The $15\times15$ source mesh alone defines loss quadratics and decisions. The disjoint
$31\times31$ direct-parent mesh supplies diagnostic maximum and RMS spectral errors.
Evaluation records carry an exact role and source identity. They cannot feed producer
branching before the class dispositions are fixed.

## Tolerances

All tolerances are finite, strictly positive built-in floats unless a field is explicitly
a nonnegative resolution. Separate controls are required for source projection,
quadratic reconstruction, feasibility, certificate rounding, verification, and withheld
correlation. Reusing one tolerance for unrelated scales requires explicit justification.
Thresholds and the distance resolution are benchmark controls, not error bars.

## Determinism and resource behavior

Orbit generation, matrix assembly, class order, and canonical JSON ordering are
deterministic. The largest dense objects are bounded by the number of $D_4$ orbits and
225 source samples; no large external-calculator artifacts are needed. Convex-solver
output is evidence only after deterministic reconstruction and certificate checks.

## Numerical limitations

Producer and verifier may share NumPy/SciPy, BLAS/LAPACK, binary64 behavior, and the
same Fourier conventions. Independent code paths reduce but do not eliminate common-
mode numerical errors. Withheld source-projection and finite-mesh interpolation errors
are separate from model-class incompatibility and should be separated from each other
when the retained comparisons permit it.
