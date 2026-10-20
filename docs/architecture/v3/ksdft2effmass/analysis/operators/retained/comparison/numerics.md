# Numerical contract

For same-coordinate candidate `A` and reference `B`, the comparator constructs

$$
\Delta=A-B,
$$

$$
\Delta^{\mathrm{diag}}
=\operatorname{diag}(\operatorname{diag}(\Delta)),
\qquad
\Delta^{\mathrm{off}}=\Delta-\Delta^{\mathrm{diag}}.
$$

All matrices have one common `K`-by-`K` shape and unit. The action uses
`numpy.float64` arithmetic and introduces no tolerance.

The diagonal/off-diagonal split is basis dependent. It is meaningful only under the
request's explicit common coordinate identity.

The result contains no Frobenius norm. An experiment may separately apply
`RepresentedMatrixNormAnalyzer` to `difference`, `diagonal_difference`, or
`off_diagonal_difference` and must declare any normalization.
