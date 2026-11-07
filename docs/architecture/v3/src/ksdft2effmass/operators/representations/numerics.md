# Numerical representation

## Domains

`FiniteMomentumMeshDomain` composes the Numerics-owned `CenteredUniformMesh`. Mesh
dimension, axis size, offsets, coordinates, and tensor-product point count remain owned by
that dependency; KSD does not accept a parallel coordinate array.

`FiniteTranslationDomain` stores a nonempty ordered tuple of unique integer vectors with
one common positive dimension. Components are exact built-in integers. Boolean values and
numeric strings are rejected. No metric, modulo reduction, shell completion, or sorting
is applied.

## Matrix fields

Concrete field leaves require finite NumPy arrays with exact `complex128` dtype and shape

\[
(N,n_{\mathrm{target}},n_{\mathrm{source}}),
\]

where `N` equals the carrier-domain cardinality. Square roles require equal positive
matrix dimensions. Frame fields may be rectangular; rows are target coordinates and
columns are source coordinates.

Construction obtains owned immutable bytes-backed storage. Caller mutation cannot change
the stored field. Dimensions are derived from validated array shape rather than accepted
as independent constructor data.

## Typed exact comparison and tolerances

`MatrixFieldABC.is_exactly_equal_to(other: MatrixFieldABC, /)` requires the same concrete
leaf, equal domain metadata, and `numpy.array_equal` values. The explicit method avoids an
unspecified `object` equality boundary. No tolerance, gauge equivalence, basis conversion,
unit conversion, or energy-reference alignment is applied.

## Numerical limits

Translation integers retain Python integer range. Matrix storage uses binary64 complex
components. Nonfinite real or imaginary components are rejected; overflow that produces a
nonfinite value is not retained.
