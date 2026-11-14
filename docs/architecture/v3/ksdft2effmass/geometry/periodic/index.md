# `ksdft2effmass.geometry.periodic`

## Status

Prospective architecture. The package, modules, and public imports described here are not
yet implemented. This documentation does not authorize compatibility aliases, migration
of retained evidence, deletion of active `ksdft2effmass.solidstate` lattice records, or
a provider rename in PhysKit.

## Responsibility

The package owns KSD scientific values that correlate periodic lattice geometry,
integer lattice displacements, physical direct- and reciprocal-lattice displacements,
dimensionless reciprocal-lattice coordinates, and physical reciprocal-space vectors.
It does not use Bloch-state terminology for geometry-only values.

PhysKit continues to own reusable direct and reciprocal lattice primitives, integer
lattice displacement records, physical quantities, unit conversion, and direct-lattice
metrics. KSD composes those provider values with explicit physical units and scientific
correlation.

## Canonical vocabulary

For ordered direct and reciprocal primitive-basis matrices

\[
A^{\mathsf T}B=2\pi I,
\]

the canonical names are

\[
\mathbf R_{\mathbf n}=A\mathbf n,
\qquad
\mathbf G_{\mathbf m}=B\mathbf m,
\qquad
\mathbf k_{\mathbf q}=B\mathbf q,
\]

where \(\mathbf n,\mathbf m\in\mathbb Z^d\) and
\(\mathbf q\in\mathbb R^d\).

| Scientific value | Meaning | Unit |
|---|---|---|
| `IntegerLatticeDisplacement` | integer basis coefficients \(\mathbf n\) or \(\mathbf m\) | dimensionless |
| `DirectLatticeDisplacement` | physical vector \(A\mathbf n\) | length |
| `ReciprocalLatticeDisplacement` | physical reciprocal-lattice vector \(B\mathbf m\) | inverse length |
| `ReciprocalLatticeCoordinate` | real coefficients \(\mathbf q\) in the ordered reciprocal basis | dimensionless |
| `ReciprocalSpaceVector` | physical reciprocal-space vector \(B\mathbf q\) | inverse length |

The canonical scientific term `IntegerLatticeDisplacement` currently maps to PhysKit's
`LatticeDisplacement` provider class. KSD uses that provider value under the field name
`integer_displacement`; it does not add an alias or duplicate class. Renaming the
provider class belongs to a separate PhysKit review.

`ReciprocalLatticeDisplacement` and `ReciprocalSpaceVector` are not synonyms. The former
requires integer coefficients and represents a reciprocal-lattice shift. The latter
admits real coefficients and may identify a periodic-fiber coordinate only when a
separate periodic-state owner supplies that interpretation.

## Proposed source layout

```text
ksdft2effmass/geometry/
└── periodic/
    ├── base.py
    ├── direct_displacement.py
    ├── reciprocal_displacement.py
    ├── reciprocal_coordinate.py
    ├── reciprocal_space.py
    ├── periodic1d/
    │   ├── geometry.py
    │   ├── direct_displacement.py
    │   ├── reciprocal_displacement.py
    │   ├── reciprocal_coordinate.py
    │   ├── reciprocal_space.py
    │   ├── physkit_projection.py
    │   └── legacy_projection.py
    ├── periodic2d/
    │   └── corresponding dimensional modules
    └── periodic3d/
        └── corresponding dimensional modules
```

Dimension-neutral modules own abstract scientific value contracts. Each dimensional
package owns final frozen, slotted, keyword-only values with exact numerical shapes.
Provider and legacy projections are explicit peer operations rather than superclasses or
aliases.

## Geometry hierarchy

```text
PeriodicLatticeGeometry
├── Periodic1DLatticeGeometry
├── Periodic2DLatticeGeometry
└── Periodic3DLatticeGeometry
```

A geometry value owns an immutable scalar snapshot of the ordered primitive basis and an
explicit physical length unit. It reconstructs exact PhysKit direct and reciprocal
lattices. Two- and three-dimensional geometry may derive `DirectLatticeMetric`; the
shared contract does not require it because the installed PhysKit metric owner does not
admit one dimension.

`PeriodicLatticeGeometry` owns only genuinely dimension-neutral behavior:

- the authoritative `lattice_unit` field;
- abstract `lattice_dimension`, `direct_lattice`, and `reciprocal_lattice`
  projections; and
- the final derived `reciprocal_lattice_unit` property.

Dimension-correlated construction methods remain on final dimensional geometries. This
avoids narrowing inherited parameter types in violation of ordinary Python override
substitutability.

## Semantic value hierarchies

```text
DirectLatticeDisplacement
├── DirectLatticeDisplacement1D
├── DirectLatticeDisplacement2D
└── DirectLatticeDisplacement3D

ReciprocalLatticeDisplacement
├── ReciprocalLatticeDisplacement1D
├── ReciprocalLatticeDisplacement2D
└── ReciprocalLatticeDisplacement3D

ReciprocalLatticeCoordinate
├── ReciprocalLatticeCoordinate1D
├── ReciprocalLatticeCoordinate2D
└── ReciprocalLatticeCoordinate3D

ReciprocalSpaceVector
├── ReciprocalSpaceVector1D
├── ReciprocalSpaceVector2D
└── ReciprocalSpaceVector3D
```

A direct- or reciprocal-lattice displacement retains one geometry and one exact provider
integer displacement. Its physical quantity is derived and cannot drift from those
inputs. A reciprocal coordinate stores finite dimensionless real coefficients in the
ordered reciprocal primitive basis. A reciprocal-space vector binds a finite physical
inverse-length quantity to one exact geometry.

None of these classes identifies a reciprocal mesh, Brillouin-zone representative,
finite basis, state space, gauge, Hamiltonian, band index, or scientific-model rank.
Those interpretations belong to periodic-fiber, real-space-kernel, or represented-model
owners.

## Base-class ownership

| Abstract base | Authoritative retained fields | Derived or abstract surface |
|---|---|---|
| `PeriodicLatticeGeometry` | `lattice_unit` | dimension, provider lattices, reciprocal unit |
| `DirectLatticeDisplacement` | `geometry`, `integer_displacement` | dimension and `physical_displacement` |
| `ReciprocalLatticeDisplacement` | `geometry`, `integer_displacement` | dimension and `physical_displacement` |
| `ReciprocalLatticeCoordinate` | `components` | exact dimension |
| `ReciprocalSpaceVector` | `geometry`, `physical_vector` | exact dimension |

Shared bases validate only invariants expressible without a dimension-dependent cast.
Dimensional leaves validate exact tuple lengths, exact geometry types, scalar-versus-
vector quantity shape, and exact provider lattice type. No base accepts `object`, `Any`,
an unknown-dimensional array, or an unknown-producer fallback.

Implementations must explicitly call shared post-construction validation before their
leaf-specific checks; Python dataclass inheritance does not automatically chain an
overridden `__post_init__`. Provider quantities are immutable, but `VectorQuantity`
deliberately has no value-based equality, so correlated validation compares units and
numerical components explicitly rather than relying on quantity `==`.

## Proposed dimensional API

For three dimensions, the geometry-facing API is:

```python
def direct_displacement(
    self,
    integer_displacement: LatticeDisplacement,
) -> DirectLatticeDisplacement3D: ...

def reciprocal_displacement(
    self,
    integer_displacement: LatticeDisplacement,
) -> ReciprocalLatticeDisplacement3D: ...

def reciprocal_space_vector(
    self,
    coordinate: ReciprocalLatticeCoordinate3D,
) -> ReciprocalSpaceVector3D: ...

def recover_reciprocal_coordinate(
    self,
    source_vector: ReciprocalSpaceVector3D,
) -> ReciprocalCoordinateRecoveryResult3D: ...
```

One- and two-dimensional APIs use their exact dimensional value types. Coordinate
recovery requires `source_vector.geometry == self`. The former raw
`VectorQuantity -> tuple[float, ...]` inverse is intentionally absent.

## Reciprocal-coordinate recovery

Coordinate recovery solves

\[
B\widehat{\mathbf q}=\mathbf k
\]

and returns one final dimension-owned result:

```text
ReciprocalCoordinateRecoveryResult*d
├── source_vector
├── recovered_coordinate
├── reconstructed_vector
└── reconstruction_residual
```

There is no abstract recovery-action hierarchy. The dimensional geometry owns the solve
and returns an immutable result. The result reports numerical reconstruction error
without choosing an acceptance tolerance or a canonical Brillouin-zone representative.
Its geometry is derived from `source_vector`, not stored redundantly.

## Consumer boundary

This package stops at periodic geometry and coordinate values. It does not own real-space
kernels, hopping terms, Fourier coefficients, Bloch fibers, band indices, energies, or
wavefunctions.

Real-space-kernel owners may consume `IntegerLatticeDisplacement` and derive
`DirectLatticeDisplacement` when physical separation is required. Periodic-fiber owners
may consume `ReciprocalLatticeCoordinate` and `ReciprocalSpaceVector`. Ordered
basis-embedding owners may correlate retained-state or MLWF centers with this geometry
to derive element displacements such as
\(A(\mathbf n+\mathbf s_\beta-\mathbf s_\alpha)\). The embedding and locality meanings
remain outside geometry. None of these consumers belongs to or is imported by
`ksdft2effmass.geometry.periodic`.

## Model composition

Periodic scientific models compose these geometry values:

```text
Periodic1DRank2BlockHoppingModel
├── geometry: Periodic1DLatticeGeometry
└── representation: PhysKit block-hopping model

Periodic2DRank2BlockHoppingModel
├── geometry: Periodic2DLatticeGeometry
└── representation: PhysKit block-hopping model

Periodic3DRank2BlockHoppingModel
├── geometry: Periodic3DLatticeGeometry
└── representation: PhysKit block-hopping model
```

Geometry remains independent of retained rank. Models and kernel representations do not
become geometry superclasses.

## Legacy boundary

The active KSD-local `ksdft2effmass.solidstate.DirectLattice*` records are migration
inputs only. Exact dimension-owned legacy projection operations may construct the new
geometry values while preserving units and basis orientation. Core geometry modules do
not import the legacy subsystem, and no new value retains both legacy and PhysKit
lattices as competing authorities.

The composed legacy `Lattice1D`, `Lattice2D`, and `Lattice3D` values additionally carry
correlated duality and Bravais-analysis results. Those results remain separate evidence;
projecting their direct basis does not silently transfer or discard their verification
status.

## Detailed documents

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
