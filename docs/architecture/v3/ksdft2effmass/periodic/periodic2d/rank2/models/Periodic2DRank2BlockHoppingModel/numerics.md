# `Periodic2DRank2BlockHoppingModel` numerics

The model binds integer lattice displacements
\(\mathbf n=(n_1,n_2)\in\mathbb Z^2\) to complex `2 x 2` coefficient blocks. Provider
dimension must be `LatticeDimension.TWO`. The model geometry stores the ordered
primitive-basis matrix and its physical length unit, reconstructs exactly
`DirectLattice2D`, and derives its metric. The physical direct-lattice displacement
\(\mathbf R_{\mathbf n}=A\mathbf n\) is a geometry-derived value rather than the
coefficient index.

For every stored displacement, construction requires

\[
T(-n_1,-n_2)=T(n_1,n_2)^\dagger
\]

by exact complex128 element comparison. The zero-displacement block must therefore be
exactly Hermitian.

The direct metric is derived as \(G=A^{\mathsf T}A\) without replacing the ordered
basis \(A\). The stored row tuples record the numerical matrix rows, while the primitive
vectors remain the columns of \(A\). A locality request supplies one nonnegative built-in
shell index per provider term. Normalized shell power is a later analysis result and is
not stored in the model.

No tolerance, mesh, Fourier transform, or energy conversion is part of construction.
