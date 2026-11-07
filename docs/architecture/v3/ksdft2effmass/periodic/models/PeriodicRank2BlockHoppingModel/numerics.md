# `PeriodicRank2BlockHoppingModel` numerics

## Coefficient domain

For each integer lattice displacement \(\mathbf n\in\mathbb Z^d\), the provider
representation stores a complex binary64 matrix

\[
T(\mathbf n)\in\mathbb C^{2\times2}.
\]

PhysKit currently represents \(\mathbf n\) with `LatticeDisplacement`. It is a
dimensionless kernel index, not the physical direct-lattice displacement
\(\mathbf R_{\mathbf n}=A\mathbf n\).

Rank means the retained primitive-cell state-space dimension. It does not mean matrix
algebraic rank, parent-state count, mesh size, or hopping-support cardinality.

## Exact invariants

Construction checks:

1. provider dimension equals the dimensional child;
2. every block has basis size two;
3. every displacement has its additive inverse; and
4. each inverse coefficient is elementwise exactly the conjugate transpose.

Sparse provider coefficients are materialized only at this explicit scientific-model
admission boundary. The stored provider value remains sparse and immutable.

## Direct-lattice geometry

Every dimensional child composes one immutable, unit-bearing lattice geometry and
reconstructs its exact PhysKit direct lattice from that value. The one-dimensional
geometry stores a physical period and length unit. The two- and three-dimensional
geometries store the numerical rows of the ordered primitive-basis matrix, whose
primitive vectors are its columns, together with the physical length unit. They derive
`DirectLatticeMetric` rather than treating the metric as the complete geometry.
Geometry may derive
\(\mathbf R_{\mathbf n}=A\mathbf n\) as a `DirectLatticeDisplacement`, but the model
continues to index coefficients by \(\mathbf n\). The model does not calculate shell
labels, distances, powers, or truncation errors.

For an explicitly embedded ordered basis, an external locality analyzer may instead
derive the element displacement
\(A(\mathbf n+\mathbf s_\beta-\mathbf s_\alpha)\). The model does not store or infer
the centers \(\mathbf s_\alpha\) and does not decide whether matrix indices denote
generic retained states, orbitals, or MLWFs.

## Overflow and tolerance

Model admission performs no summation and introduces no numerical tolerance. It
therefore has no overflow policy beyond the already admitted provider values. Approximate
Hermiticity belongs to a numerical-error or model-construction policy, not this identity
contract.
