# Particle-in-a-box 2D/3D and non-orthonormal representation plan

## Status and boundary

This is **proposed KSD experiment work**, not completed PIAB2D or PIAB3D numerical
evidence. It extends the public one-dimensional particle-in-a-box ownership model
without changing retained Appendix D results. The pinned PhysKit revision already owns
rectangular PIAB2D and PIAB3D models, their analytical spectrum evaluators, and an
oblique PIAB2D finite-difference solver. Those reusable capabilities are not KSD
campaigns or retained KSD evidence. This plan does not authorize production
calculations, scientific validation, or uncertainty quantification.

“Non-orthonormal” can describe two mathematically different situations. This plan
keeps them separate:

1. a non-orthonormal **spatial coordinate frame**, whose axis vectors may be non-unit
   and non-orthogonal; and
2. a non-orthogonal **representation basis**, whose coefficient inner product is
   described by an overlap matrix $S$.

Neither situation may be treated by silently applying an orthonormal-coordinate or
ordinary eigenproblem formula.

## Existing reusable foundation

The normalized experiment hierarchy is
`experiments/model-systems/piab/{piab1d,piab2d,piab3d}/`. Actual retained runs use
matching `calculations/model-systems/piab/<dimension>/runs/<run-id>/` paths; absent
runs do not receive calculation placeholders.

The implemented one-dimensional KSD slice supplies:

- `DirichletInterval`;
- `UniformCartesianGrid1D`;
- `SecondOrderCentralDifferenceLaplacian1D`;
- `SchrodingerKineticEnergy1D`;
- `SampledPotential1D`;
- `FiniteDifferenceHamiltonian1D` with canonical CSR storage;
- `SparseMatrixQuantity` with immutable CSR components;
- `ParticleInBoxAnalytical`;
- `ParticleInBoxFiniteDifference`;
- `ParticleInBoxGridEvaluator`;
- `OrthogonalSpectralSubspace` and `OperatorCompression` for retained coordinates;
- `RepresentedMatrixNormAnalyzer` for explicit matrix metrics; and
- `RealSymmetricEigenpairSolver`, using tridiagonal diagonals for complete one-
  dimensional spectra and an iterative sparse solver for selected eigenpairs.

The solver does not materialize a sparse operator as dense before diagonalization. A
complete general non-tridiagonal sparse eigensystem is rejected; higher-dimensional
campaigns must request the scientifically identified subset required by their
contract. The retained particle-in-a-box campaign remains one-dimensional.
Higher-dimensional
contracts must be introduced through new public classes rather than changing the
meaning of these names.

## Orthonormal 2D and 3D domains

### Spatial records

Introduce model-independent domain DataObjects:

- `DirichletRectangle` composed from `UniformCartesianGrid2D` and declared boundary
  values on its four faces; and
- `DirichletRectangularBox` composed from `UniformCartesianGrid3D` and declared
  boundary values on its six faces.

The existing grids retain `ij` indexing and row-major (`C`) flattening. For shape
$(N_1,N_2)$, the flattened index is $iN_2+j$. For shape $(N_1,N_2,N_3)$, it is
$(iN_2+j)N_3+k$. Domain and operator records must state whether shapes include or
exclude boundary points.

Initial operator support remains restricted to homogeneous Dirichlet values. A
nonhomogeneous condition requires a separate affine forcing vector and must not be
represented as a matrix-only operator.

### Laplacians

For mutually orthonormal axes, construct Kronecker sums from independently represented
one-dimensional second derivatives:

$$
L_{2D}=L_1\otimes I_2 + I_1\otimes L_2,
$$

and

$$
L_{3D}=L_1\otimes I_2\otimes I_3
      +I_1\otimes L_2\otimes I_3
      +I_1\otimes I_2\otimes L_3.
$$

Proposed operator owners are:

- `SecondOrderCentralDifferenceLaplacian2D`; and
- `SecondOrderCentralDifferenceLaplacian3D`.

They must consume structural domain protocols from `ksdft2effmass.operators`, preserve
flattening order exactly, and return canonical CSR matrices with inverse-area units.
Sparse Kronecker construction must avoid dense identity factors and dense intermediate
operators. Kinetic-energy,
sampled-potential, and Hamiltonian composition then receive dimension-specific public
owners rather than dimension-erased containers.

### Analytical reference

For an orthogonal rectangular domain with side lengths $L_i$, the continuum energies
are separable:

$$
E_{n_1,\ldots,n_d}
=\frac{\hbar^2\pi^2}{2m}\sum_{i=1}^{d}\frac{n_i^2}{L_i^2},
\qquad n_i\ge 1.
$$

A public analytical result must retain each integer mode tuple because degeneracies
make a scalar ordinal index insufficient to identify a state. Sorting policy and
stable tie handling must be explicit.

## Non-orthonormal spatial frames

### Geometry

Represent an affine frame by an origin $x_0$ and invertible axis matrix $A$:

$$
x=x_0+A\xi.
$$

Use dedicated immutable records, provisionally `AffineCoordinateFrame2D` and
`AffineCoordinateFrame3D`. They must retain:

- axis-vector orientation and order;
- physical units;
- determinant sign and absolute volume factor;
- the covariant metric $G=A^T A$;
- the inverse metric $G^{-1}$; and
- a declared condition-number diagnostic.

“Non-orthonormal” includes scaled orthogonal axes and genuinely oblique axes. Singular
or numerically unresolved frames must be rejected; a tolerance policy requires
explicit numerical-verification evidence before becoming public.

Proposed grids are `UniformAffineGrid2D` and `UniformAffineGrid3D`. They use uniform
computational coordinates $\xi$ and preserve the same `ij`/row-major indexing contract
as Cartesian grids. They must not be named Cartesian grids because physical axes can
be oblique.

### Metric Laplacian

For a constant affine frame, the physical Laplacian is

$$
\nabla_x^2
=\sum_{i,j}(G^{-1})_{ij}\frac{\partial^2}{\partial\xi_i\partial\xi_j}.
$$

Off-diagonal inverse-metric entries generate mixed derivatives. Proposed owners are:

- `MetricFiniteDifferenceLaplacian2D`; and
- `MetricFiniteDifferenceLaplacian3D`.

The discrete construction must state the centered mixed-derivative stencil, boundary
closure, flattening order, and matrix symmetry. It must not approximate an oblique
frame by retaining only diagonal metric entries.

The physical integration measure is

$$
dx=|\det A|\,d\xi.
$$

Quadrature, normalization, and overlap calculations must carry this Jacobian. A
constant Jacobian can cancel from a standard nodal eigenproblem, but it cannot be
silently discarded from wavefunction normalization or comparisons across geometries.

A general oblique Dirichlet parallelogram or parallelepiped does not inherit the simple
product-sine eigenspectrum of an orthogonal box. The project must not claim a separable
analytical spectrum for that case.

## Non-orthogonal representation bases

A non-orthogonal basis produces the generalized eigenproblem

$$
Hc=ESc,
$$

where the overlap matrix $S$ identifies the coefficient-space inner product. This is
separate from an oblique spatial frame: either, both, or neither may be present.

Introduce explicit records only when a migrated calculation requires them:

- `OverlapMatrix`, including basis identity, units, Hermiticity, and positive-definite
  status;
- `GeneralizedHermitianEigenpairResult`; and
- `GeneralizedHermitianEigenpairSolver`.

The solver must use a declared positive-definite reduction, such as Cholesky or
symmetric orthonormalization, and report residuals in the original generalized
problem. `RealSymmetricEigenpairSolver` must reject this use rather than assuming
$S=I$.

Operator subtraction or pullback remains prohibited until state-space, basis,
geometry, unit, and energy-reference compatibility is established. Exact equality of
matrix shapes does not establish those prerequisites.

## Verification plan

### Software verification

For every new public class, verify:

- exact shape and flattening contracts;
- immutability and strict scalar admission;
- coordinate, energy, and inverse-area units;
- face ownership and homogeneous-boundary admission;
- Kronecker-factor placement;
- metric and Jacobian correlation; and
- rejection of incompatible domains, frames, potentials, or overlap matrices.

### Numerical verification

Use independent oracles appropriate to each case:

1. orthonormal rectangles and boxes: tensor-product discrete eigenvalues and continuum
   separable energies;
2. diagonal but non-unit frames: agreement between affine-metric and rescaled
   orthonormal constructions;
3. oblique frames: manufactured smooth functions, independently assembled mixed
   stencils, symmetry checks, and observed refinement under a fixed physical domain;
4. generalized eigenproblems: residuals $\|HC-SCE\|$, $S$-orthonormality
   $\|C^*SC-I\|$, and comparison with an independently transformed standard problem.

Parent-model error, spatial-discretization error, eigensolver error, and
model-reduction error remain separate. These checks do not constitute semiconductor
validation or uncertainty quantification.

## Staged implementation

1. **Completed:** migrate the one-dimensional residual, convergence, eigenpair, norm,
   and identifiability campaigns and preserve retained numerical artifacts.
2. **Completed by PhysKit:** own rectangular PIAB2D and PIAB3D models, analytical mode
   inventories, and the oblique PIAB2D finite-difference solver. This establishes
   reusable capability, not KSD experiment evidence.
3. Freeze the orthogonal PIAB2D KSD protocol, including the explicit decision whether
   the diagonal-basis use of PhysKit's oblique solver is admitted, then add KSD-owned
   schemas, thin adapters, and independent campaign verification.
4. Add or review a reusable sparse PIAB3D finite-difference owner in PhysKit before
   freezing the KSD PIAB3D numerical protocol. KSD must not fill this gap with a
   campaign-local reusable solver.
5. Introduce affine-frame and oblique-coordinate KSD experiments only after the
   orthogonal dimensional campaigns close their software-verification gates.
6. Introduce overlap-matrix and generalized-eigenproblem contracts only with a concrete
   non-orthogonal-basis consumer.

Each stage must preserve earlier public imports and retained artifacts or document an
explicitly authorized compatibility change.
