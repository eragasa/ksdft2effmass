# HSH-1 numerical contract

## Scalar and collection types

Public numeric inputs must be exact built-in `float` or `int` values as declared.
Booleans, numeric strings, NumPy scalar impostors, NaNs, and infinities are rejected.
Maintained collections use immutable tuples. Internal dense computation may use
`numpy.float64` and `numpy.ndarray`, but arrays cannot escape through maintained public
objects.

## Ordering and finite geometry

The source mesh size is odd. Centered representatives are ordered lexicographically
after generating $[-n,\ldots,n]^2$. Each $D_4$ orbit has one canonical integer
representative. Orbits are ordered by squared radius and then representative. Every
shell mask is a prefix in that orbit ordering and contains complete orbits.

The target package must reconstruct rather than trust:

- orbit closure, disjointness, and complete coverage of the finite domain;
- multiplicity sum equal to the block count;
- nested shell masks and the full final shell;
- real projected target and one common energy zero; and
- exact zero inactive coefficients in every embedded point.

## Quadratic representation

Each channel loss restricted to active coordinates is retained as

$$
q(z)=(z-c)^TQ(z-c)+m.
$$

`analysis.model_adequacy.losses.DimensionlessPositiveDefiniteQuadraticLoss` owns the
finite dimensionless center, symmetric positive-definite matrix, nonnegative finite
minimum squared loss, strict typing, immutable `quadratic_matrix` property,
`squared_loss(coordinates)`, and `rms_loss(coordinates)`. It accepts only explicitly
normalized dimensionless canonical coordinates.

The HSH-local `Periodic2DHoppingShellQuadraticLoss` owns the energy unit and scale
$E_G$, shell identity, channel, strictly increasing active maximal-space indices,
inactive-zero rule and tolerance, and nonnegative reconstruction/correlation defects.
Its `squared_loss(maximal_coefficients)` validates the energy-coefficient embedding,
forms the ordered ratios $z=c_{\mathrm{active}}/E_G$, and delegates those ratios to the
shared primitive. Positive definiteness is checked with a prospectively frozen absolute
tolerance and an independently reconstructed factorization or eigenvalue bound.

A channel is nonempty only if its quadratic sublevel intersects the active slice of the
coefficient box. Unconstrained minimum feasibility is insufficient when the center lies
outside the box. The producer may use a deterministic bounded convex solver. The
verifier must independently enclose the box-constrained minimum: an outward lower bound
above threshold proves emptiness, while an explicit point at or below threshold proves
nonemptiness. If neither proof closes within the frozen arithmetic policy, the class is
`invalid-premise` rather than guessed empty or nonempty.

## Metric and dual norm

All classes use the same diagonal metric
$M_{oo}=m_o/(E_G^2|\mathcal R_{\max}|)$. No class-dependent normalization is allowed.
A support-certificate direction must be nonzero and finite in the maximal coefficient
space. Its dual norm is $\sqrt{u^TM^{-1}u}$. Directions may be normalized for storage,
but the verifier must reconstruct scale invariance.

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
mode numerical errors. Withheld interpolation error is separate from model-class
incompatibility.
