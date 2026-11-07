# `FourierSeriesBlockHoppingRepresentation` numerics

For a finite Fourier matrix series indexed by integer lattice displacements,

\[
H(\mathbf q)
=\sum_{\mathbf n}T(\mathbf n)e^{2\pi i\mathbf q\cdot\mathbf n}.
\]

Equivalently, after a geometry supplies
\(\mathbf R_{\mathbf n}=A\mathbf n\) and
\(\mathbf k_{\mathbf q}=B\mathbf q\),

\[
H(\mathbf k_{\mathbf q})
=\sum_{\mathbf n}T(\mathbf n)
 e^{i\mathbf k_{\mathbf q}\cdot\mathbf R_{\mathbf n}}.
\]

`integer_modes` supplies \(\mathbf n\), and `matrix_coefficients` supplies
\(T(\mathbf n)\). The operation performs no Fourier transform; it projects an already
constructed series into PhysKit's integer-displacement-indexed value types. It does not
construct or require physical direct-lattice displacements.

Each coefficient is copied into complex128 storage and wrapped in a unitless
`ComplexMatrixQuantity`. No cast to real values, tolerance comparison, normalization, or
energy conversion is applied.

Terms are sorted lexicographically by displacement. Shell inventories must therefore be
correlated by displacement identity when their source enumeration differs.

The operation supports dimensions two and three. Other dimensions are rejected before
constructing provider displacements.
