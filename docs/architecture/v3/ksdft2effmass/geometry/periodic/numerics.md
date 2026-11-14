# Periodic geometry numerics

## Basis convention

For dimension \(d\in\{1,2,3\}\), let the ordered direct primitive vectors be columns
of

\[
A\in\mathbb R^{d\times d}.
\]

The two-pi-dual reciprocal primitive basis is

\[
B=2\pi A^{-\mathsf T},
\qquad
A^{\mathsf T}B=2\pi I.
\]

Geometry construction requires finite built-in binary64-compatible components, an
invertible direct basis, and an explicit physical length unit. The reciprocal unit is
the corresponding inverse-length unit. Basis order is scientific metadata and is never
silently sorted or canonicalized.

## Integer lattice displacements

The scientific term `IntegerLatticeDisplacement` denotes integer basis coefficients
\(\mathbf n\in\mathbb Z^d\). The current provider representation is PhysKit
`LatticeDisplacement`. It is dimensionless and is not itself a physical direct- or
reciprocal-space vector.

Boolean, string, floating-point, NumPy-integer, and wrong-dimensional components are not
admitted. The exact provider value is composed rather than copied into a KSD replacement
class.

## Direct-lattice displacements

A `DirectLatticeDisplacement*d` binds one geometry to one integer displacement and
derives

\[
\mathbf R_{\mathbf n}=A\mathbf n.
\]

Its authoritative retained values are `geometry` and `integer_displacement`. Its derived
`physical_displacement` is:

- `ScalarQuantity` in one dimension; or
- `VectorQuantity` with shape `(2,)` or `(3,)` in two or three dimensions.

The quantity uses the geometry's physical length unit. It is not retained independently
and therefore cannot drift from the lattice and integer coefficients that define it.

## Reciprocal-lattice displacements

A `ReciprocalLatticeDisplacement*d` binds one geometry to one integer displacement and
derives the reciprocal-lattice vector

\[
\mathbf G_{\mathbf m}=B\mathbf m,
\qquad
\mathbf m\in\mathbb Z^d.
\]

Its `physical_displacement` has the geometry's inverse-length unit. This value represents
an integer reciprocal-lattice shift. It is not a general reciprocal-space vector and it
does not select a periodic fiber or Brillouin-zone representative.

## Reciprocal-lattice coordinates

A `ReciprocalLatticeCoordinate*d` stores finite built-in floats
\(\mathbf q\in\mathbb R^d\). The components are dimensionless coefficients in the
ordered reciprocal primitive basis. The value is not a Cartesian vector and is not a
state-space coordinate.

The coordinate contract does not impose a reciprocal-quotient interval. In particular,
\(\mathbf q\) and \(\mathbf q+\mathbf m\), with
\(\mathbf m\in\mathbb Z^d\), remain different stored coordinates. A centered,
unit-half-open, symmetry-reduced, path-bound, or mesh-bound representative requires a
separate explicit owner.

## Reciprocal-space vectors

A `ReciprocalSpaceVector*d` binds one geometry to a finite physical reciprocal-space
quantity \(\mathbf k\) with inverse-length units. For a reciprocal coordinate
\(\mathbf q\), geometry constructs

\[
\mathbf k_{\mathbf q}=B\mathbf q.
\]

The value retains `geometry` and `physical_vector`. Construction rejects wrong
dimension, nonfinite components, direct-length units, booleans, and numeric strings.

This neutral value does not by itself identify a reciprocal mesh, path label,
reciprocal-quotient representative, periodic fiber, band index, basis order, gauge,
energy, or wavefunction.

## Direct--reciprocal pairing

For correlated geometry, direct displacement, and reciprocal coordinate,

\[
\mathbf k_{\mathbf q}\mathbin{\cdot}\mathbf R_{\mathbf n}
=2\pi\,\mathbf q\mathbin{\cdot}\mathbf n.
\]

The left side pairs physical inverse-length and length quantities. The right side pairs
dimensionless reciprocal coefficients with integer lattice coordinates. Implementations
must not substitute elementwise products in unrelated coordinate systems.

Complex phases, Fourier kernels, and periodic represented operators are consumer-owned
operations outside this package.

## Reciprocal-coordinate recovery

Recovering reciprocal coordinates from a physical reciprocal-space vector solves

\[
B\widehat{\mathbf q}=\mathbf k.
\]

The exact dimensional geometry method requires a correlated
`ReciprocalSpaceVector*d` and returns `ReciprocalCoordinateRecoveryResult*d`. There is
no separate recovery-action class and no dimension-neutral result superclass.

The immutable result records:

1. `source_vector`;
2. `recovered_coordinate`;
3. `reconstructed_vector`, equal to \(B\widehat{\mathbf q}\) in represented
   arithmetic; and
4. `reconstruction_residual`,

\[
\delta_k
=\left\lVert B\widehat{\mathbf q}-\mathbf k\right\rVert_2.
\]

The residual is a `ScalarQuantity` in the geometry's reciprocal-length unit. The result
derives its geometry from `source_vector` and requires the reconstructed vector to bind
an equal immutable geometry value. Recovery does not accept a tolerance, report
pass/fail, or choose a reciprocal-quotient representative.

## Precision and failure behavior

Initial implementations use provider binary64 basis values and NumPy binary64 linear
algebra already admitted by PhysKit. Construction rejects nonfinite inputs and singular
geometry. Coordinate recovery reports a finite reconstruction residual and raises when
the solve fails or produces nonfinite output.

No implicit integer wrapping, modulo reduction, clipping, tolerance-based equality,
unit dropping, coordinate rounding, or overflow recovery is permitted. Large finite
inputs may overflow provider matrix multiplication or norm evaluation; such nonfinite
results are rejected rather than normalized silently.

## Metric ownership

Two- and three-dimensional geometry derive PhysKit `DirectLatticeMetric` from their
exact reconstructed direct lattice. One-dimensional geometry does not invent a local
metric replacement. Direct displacement, reciprocal displacement, and reciprocal-space
vector construction require only the direct and reciprocal primitive bases.

Metric-shell classification, reciprocal meshes, Fourier transforms, interpolation,
support truncation, kernel coefficients, and model-error tolerances remain outside this
package.
