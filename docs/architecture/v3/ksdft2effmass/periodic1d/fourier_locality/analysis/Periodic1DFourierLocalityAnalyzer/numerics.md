# `Periodic1DFourierLocalityAnalyzer` numerics

The analyzer uses binary64 complex parent matrices and a Hermitian eigensolver. Ordered
lowest and adjacent eigenvalues are retained in units `E_ref`.

For each construction size it computes one complete transform, one complete interpolant,
and all sixteen symmetric truncations. Equal-weight direct fits use a Hermitian scalar
basis with `2*R+1` real degrees of freedom expressed through one real onsite coefficient
and conjugate pairs.

Maximum residuals use explicit absolute values. Root-mean-square residuals divide the
sum of squared absolute values by the exact inventory length before taking the square
root. Omitted coefficient norms and Parseval channels retain their own units and are not
normalized into application errors.

Threshold comparisons use the authored inclusive directions. Nondominance compares the
stored binary64 objective pair without a tolerance. The analyzer records near ties
separately and never changes a dominance result to force stability.

Any canonical numerical owner reporting an unexpected shape, ordering, unit, rank, or
nonfinite value causes calculation failure before root-result construction.
