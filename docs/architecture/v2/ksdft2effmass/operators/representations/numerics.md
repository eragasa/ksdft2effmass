# Numerics

## Scope

Phase 1 performs representation validation and immutable storage construction. It does
not perform projection, eigensolution, alignment, Fourier transformation, truncation,
reconstruction, error analysis, convergence analysis, or threshold decisions.

## Finite domains

### Momentum domains

`FiniteMomentumMeshDomain` composes Numerics'
`CenteredUniformMesh(dimension, size, offsets)`. The mesh owner defines the reduced axis
coordinates

\[
q_{a,i}=-\frac12+\frac{i+\delta_a}{N},
\qquad i=0,\ldots,N-1,
\]

and tensor-product point count

\[
|K|=N^d.
\]

The representation domain stores no second coordinate array. Construction and evaluation
are explicit roles of the same mesh type, so shifted evaluation changes `offsets` and
identity rather than changing mesh class.

### Translation domains

A translation domain is an ordered unique finite tuple

\[
T=(R_0,\ldots,R_{m-1}),\qquad R_j\in\mathbb Z^d.
\]

Every vector has one common positive dimension. Phase 1 applies no metric, modulo map,
inversion closure, shell completion, support radius, or hopping-range interpretation.
Python integers are not narrowed to a fixed-width representation.

## Matrix-field representation

All concrete field leaves store an array

\[
A\in\mathbb C^{m\times n_{\mathrm{target}}\times n_{\mathrm{source}}}
\]

as exact finite NumPy `complex128` values. The first axis is correlated positionally with
the declared domain order. Matrix rows are target coordinates and columns are source
coordinates.

Square fields require

\[
n_{\mathrm{target}}=n_{\mathrm{source}}>0.
\]

Frame fields admit unequal dimensions. For a frame array, columns are source coordinates
in the retained space and rows are target coordinates in the ambient space.

## Storage normalization

The Numerics immutable-array owner:

1. requires an exact NumPy array;
2. requires exact `complex128` dtype;
3. rejects nonfinite real or imaginary components;
4. copies values in C order into immutable bytes; and
5. returns a read-only view backed by those bytes.

This is a storage canonicalization, not a mathematical projection or precision
certificate. Input dtype is not promoted or coerced. Binary64/complex128 overflow or
nonfinite values fail rather than being retained.

## Equality

Concrete fields compare exactly only when both operands have the same concrete role,
equal domain metadata, and `numpy.array_equal` values. Equality has no tolerance and does
not establish physical equivalence, basis equivalence, gauge equivalence, or approximate
agreement.

## Numerical failure behavior

| Condition | Failure |
|---|---|
| wrong array container or dtype | `TypeError` |
| wrong domain leaf | `TypeError` |
| wrong number of axes | `ValueError` |
| first-axis/domain mismatch | `ValueError` |
| zero matrix dimension | `ValueError` |
| nonsquare square-role field | `ValueError` |
| nonfinite entry | `ValueError` |
| duplicate or inconsistent translation | `ValueError` |

No tolerance is applied in Phase 1.

## Numerical exclusions

The role names do not numerically establish:

- Hermiticity of an operator field;
- idempotency or self-adjointness of a projector field;
- orthogonality, unitarity, realness, or determinant class of a gauge field;
- rank, isometry, periodicity, or sewing of a frame field; or
- pairing, support completeness, Parseval equality, or reconstruction for Fourier
  blocks.

Those require later evidence records and separately owned analyzers.
