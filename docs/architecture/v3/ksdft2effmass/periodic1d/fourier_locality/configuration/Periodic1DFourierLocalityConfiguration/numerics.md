# `Periodic1DFourierLocalityConfiguration` numerics

The constructor first validates the parent identity and each parent matrix as a four-row
tuple of four built-in integer entries. It requires exact symmetry of the onsite
numerator and a positive common denominator, then exact-compares the identity, both
matrices, and denominator with the controlled-parent constants. Floating-point matrix
materialization is deliberately deferred to the analyzer.

At least two construction extents must be positive, even, unique, and increasing. The production
extent equals the final entry. Support radii must be nonnegative, unique, and increasing,
with

\[
2R_{\max}+1 < N_{\min}
\]

so no ordinary support reaches a cyclic Nyquist point.

For evaluation size \(M\) and exact shift \(a/b\), reduced momenta are

\[
-\frac12+\frac{i+a/b}{M}, \qquad i=0,\ldots,M-1.
\]

The constructor compares the translation-equivalent exact `Fraction` values
`(i+a/b)/M` against every construction fraction `j/N`. No tolerance can admit an
overlapping point. `evaluation_reduced_momenta()` performs the displayed exact rational
arithmetic for each index before converting once to binary64.

Every threshold and consistency term is a built-in finite nonnegative `float`.
Serialization lists the seventeen fields explicitly; deserialization performs exact
container checks and reconstructs through the public constructor.
