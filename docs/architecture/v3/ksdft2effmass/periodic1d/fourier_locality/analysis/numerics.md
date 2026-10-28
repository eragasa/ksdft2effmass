# Analysis numerics

## Parent fibers and ordered spectra

For every declared reduced momentum, the analyzer assembles the fixed `4 x 4` complex
Hermitian fiber from exact parent coefficients represented in binary64. A canonical
Hermitian eigensystem owner returns ordered eigenvalues. The lowest two values are
retained; eigenvectors are not needed for scalar represented-operator locality.

## Complete transform and truncation

Each construction mesh uses all `N` centered cyclic representatives. Complete inverse
reconstruction is checked on the construction points. Ordinary truncation retains only
`S_R` and never converts the cyclic Nyquist coefficient into an ordinary hopping.

Evaluation uses explicit complex phase sums on the fixed 1025-point inventory. Maximum
and root-mean-square residuals are calculated directly from pointwise arrays.

## Direct route

The direct route uses the same Hermitian support and equal construction weights. Its
real-parameterized least-squares design must have full declared rank. Condition number,
training residuals, evaluation residuals, coefficient defects, and sampled route defects
are retained without replacing mediated values.

## Decisions

The analyzer calculates exact binary64 comparisons for gap and application thresholds.
It evaluates every earlier support before returning a first passage. The sustained flag
checks every later declared support. Per-mesh nondominance uses exact stored objective
values and the weak-all/strict-one rule; a separate near-tie flag does not alter the mask.

## Stability

Final refinement compares named normalized operands at `N=128` and `N=256` on the same
evaluation inventory. Earlier mesh pairs are diagnostic. No extrapolation, fitted rate,
or uncertainty is calculated.
