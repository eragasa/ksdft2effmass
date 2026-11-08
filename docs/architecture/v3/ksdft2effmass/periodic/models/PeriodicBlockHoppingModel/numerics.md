# `PeriodicBlockHoppingModel` numerics

## Coefficient domain

For a retained dimension \(N\) and integer lattice displacement
\(\mathbf n\in\mathbb Z^d\), the provider representation stores a complex binary64
matrix

\[
T(\mathbf n)\in\mathbb C^{N\times N}.
\]

PhysKit represents \(\mathbf n\) with `LatticeDisplacement`. It is a dimensionless
kernel index, not the physical direct-lattice translation
\(\mathbf R_{\mathbf n}=A\mathbf n\).

Retained rank means the primitive-cell state-space dimension and equals the structured
basis coordinate count. It does not mean algebraic matrix rank, parent-state count,
mesh size, spatial dimension, or hopping-support cardinality.

## Exact invariants

Construction checks:

1. `band_subspace_rank` is a positive built-in integer;
2. the basis value has the exact dimensional identity type required by the concrete
   child;
3. the basis coordinate count equals `band_subspace_rank`;
4. provider displacement dimension equals the dimensional child;
5. provider block size equals `band_subspace_rank`;
6. every displacement has its additive inverse; and
7. each inverse coefficient is elementwise exactly the conjugate transpose.

For the maintained rank-two children, inherited rank refinement fixes \(N=2\). The
shared block-hopping validator does not contain a rank-two special case.

Sparse provider coefficients are materialized only at this explicit scientific-model
admission boundary. The stored provider value remains sparse and immutable.

## Direct-lattice geometry

Every dimensional child composes one immutable, unit-bearing lattice geometry and
reconstructs its exact PhysKit direct lattice from that value. The one-dimensional
geometry stores a physical period and length unit. The two- and three-dimensional
geometries store the numerical rows of the ordered primitive-basis matrix, whose
primitive vectors are its columns, together with the physical length unit. They derive
`DirectLatticeMetric` rather than treating the metric as complete geometry.

Geometry may derive \(\mathbf R_{\mathbf n}=A\mathbf n\), but coefficient lookup remains
indexed by \(\mathbf n\). The model does not calculate shell labels, distances, powers,
or truncation errors.

For a separately established intracell embedding, an external locality analyzer may
derive the element displacement
\(A(\mathbf n+\mathbf s_\beta-\mathbf s_\alpha)\). The model does not infer the centers
\(\mathbf s_\alpha\) from structured basis labels or provider metadata.

## Overflow and tolerance

Model admission performs no Fourier summation and introduces no numerical tolerance. It
therefore has no additional overflow policy beyond the already admitted provider
values. Approximate Hermiticity belongs to a numerical-error or model-construction
policy, not this exact identity contract.
