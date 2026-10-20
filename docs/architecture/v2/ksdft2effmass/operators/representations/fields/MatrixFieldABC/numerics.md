# Numerical contract

Concrete NumPy implementations represent values with shape

\[
(m,n_{\mathrm{target}},n_{\mathrm{source}}),
\]

where `m` equals domain cardinality and both matrix dimensions are positive. The ABC does
not require NumPy, a dtype, contiguity, or a particular precision.

Equal shape or cardinality does not imply equal domain or represented coordinates.
