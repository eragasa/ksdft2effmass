# `Periodic1DRank2BlockHoppingModel` numerics

The model binds integer lattice displacements \(n\in\mathbb Z\) to complex `2 x 2`
coefficient blocks. Provider dimension must be `LatticeDimension.ONE`. The physical
primitive period is retained as a positive finite binary64 scalar together with an
explicit physical length unit. The physical direct-lattice displacement
\(R_n=an\) is a geometry-derived value rather than the coefficient index.

For every stored displacement, construction requires

\[
T(-n)=T(n)^\dagger
\]

by exact complex128 element comparison. The zero-displacement block must therefore be
exactly Hermitian.

The geometry reconstructs a fresh PhysKit `DirectLattice1D` for shared dimensional
admission. It does not compute shell labels, Fourier coefficients, powers, or truncation
errors.

No tolerance, mesh, transform, or energy conversion is part of construction.

## Existing representation and conversion values

For a legacy `BlockHoppingModel1D`, the integer representatives and dense coefficient
blocks remain representation data. Its `reciprocal_period` records the coordinate period
used by the originating transform; it is not automatically the physical reciprocal
primitive \(2\pi/a\). In particular, the established unitless period one convention is
a reduced-coordinate convention and does not determine a physical direct period by
itself.

`CenteredEvenMeshCyclicToOrdinaryResult1D` removes only the declared negative-Nyquist
representative and retains its normalized power separately. Model construction must
consume the resulting ordinary coefficient inventory without folding that conversion
loss into a geometry value or silently restoring the removed coefficient.

`BlockHoppingModel1D.to_physkit_ordinary_representation()` performs only the reusable
representation step. It maps every caller-declared ordinary integer representative to a
one-dimensional PhysKit `LatticeDisplacement`, copies every dense coefficient without
numerical repair, preserves arbitrary square block rank and the admitted physical or
unitless coefficient unit, and requires explicit provider representation, basis, and
energy-reference identities. It
does not consume or reinterpret `reciprocal_period` and must not be called on an
unconverted cyclic inventory.

A study-owned migration composition calls that method only after any required
cyclic-to-ordinary result exists, then supplies the existing scientific-model constructor
with explicit identity, role, and geometry. The resulting model constructor remains the
sole rank-two and exact-Hermiticity admission boundary. No additional inheritance layer
or admission class is approved.
