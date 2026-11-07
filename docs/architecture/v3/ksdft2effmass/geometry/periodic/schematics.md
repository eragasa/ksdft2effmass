# Periodic geometry schematics

## Complete class hierarchy

```mermaid
classDiagram
    direction LR

    class PeriodicLatticeGeometry {
        <<abstract frozen value>>
        +lattice_unit
        +lattice_dimension
        +reciprocal_lattice_unit
        +direct_lattice
        +reciprocal_lattice
    }
    class Periodic1DLatticeGeometry { <<final>> }
    class Periodic2DLatticeGeometry { <<final>> }
    class Periodic3DLatticeGeometry { <<final>> }

    class DirectLatticeDisplacement {
        <<abstract frozen value>>
        +geometry
        +integer_displacement
        +lattice_dimension
        +physical_displacement
    }
    class DirectLatticeDisplacement1D { <<final>> }
    class DirectLatticeDisplacement2D { <<final>> }
    class DirectLatticeDisplacement3D { <<final>> }

    class ReciprocalLatticeDisplacement {
        <<abstract frozen value>>
        +geometry
        +integer_displacement
        +lattice_dimension
        +physical_displacement
    }
    class ReciprocalLatticeDisplacement1D { <<final>> }
    class ReciprocalLatticeDisplacement2D { <<final>> }
    class ReciprocalLatticeDisplacement3D { <<final>> }

    class ReciprocalLatticeCoordinate {
        <<abstract frozen value>>
        +components
        +lattice_dimension
    }
    class ReciprocalLatticeCoordinate1D { <<final>> }
    class ReciprocalLatticeCoordinate2D { <<final>> }
    class ReciprocalLatticeCoordinate3D { <<final>> }

    class ReciprocalSpaceVector {
        <<abstract frozen value>>
        +geometry
        +physical_vector
        +lattice_dimension
    }
    class ReciprocalSpaceVector1D { <<final>> }
    class ReciprocalSpaceVector2D { <<final>> }
    class ReciprocalSpaceVector3D { <<final>> }

    class ReciprocalCoordinateRecoveryResult1D {
        <<final frozen result>>
        +source_vector
        +recovered_coordinate
        +reconstructed_vector
        +reconstruction_residual
    }
    class ReciprocalCoordinateRecoveryResult2D {
        <<final frozen result>>
        +source_vector
        +recovered_coordinate
        +reconstructed_vector
        +reconstruction_residual
    }
    class ReciprocalCoordinateRecoveryResult3D {
        <<final frozen result>>
        +source_vector
        +recovered_coordinate
        +reconstructed_vector
        +reconstruction_residual
    }

    class IntegerLatticeDisplacement {
        <<PhysKit provider: currently LatticeDisplacement>>
        +dimension
        +components
    }

    PeriodicLatticeGeometry <|-- Periodic1DLatticeGeometry
    PeriodicLatticeGeometry <|-- Periodic2DLatticeGeometry
    PeriodicLatticeGeometry <|-- Periodic3DLatticeGeometry
    DirectLatticeDisplacement <|-- DirectLatticeDisplacement1D
    DirectLatticeDisplacement <|-- DirectLatticeDisplacement2D
    DirectLatticeDisplacement <|-- DirectLatticeDisplacement3D
    ReciprocalLatticeDisplacement <|-- ReciprocalLatticeDisplacement1D
    ReciprocalLatticeDisplacement <|-- ReciprocalLatticeDisplacement2D
    ReciprocalLatticeDisplacement <|-- ReciprocalLatticeDisplacement3D
    ReciprocalLatticeCoordinate <|-- ReciprocalLatticeCoordinate1D
    ReciprocalLatticeCoordinate <|-- ReciprocalLatticeCoordinate2D
    ReciprocalLatticeCoordinate <|-- ReciprocalLatticeCoordinate3D
    ReciprocalSpaceVector <|-- ReciprocalSpaceVector1D
    ReciprocalSpaceVector <|-- ReciprocalSpaceVector2D
    ReciprocalSpaceVector <|-- ReciprocalSpaceVector3D

    DirectLatticeDisplacement1D *-- Periodic1DLatticeGeometry : geometry
    DirectLatticeDisplacement2D *-- Periodic2DLatticeGeometry : geometry
    DirectLatticeDisplacement3D *-- Periodic3DLatticeGeometry : geometry
    DirectLatticeDisplacement --> IntegerLatticeDisplacement : composes

    ReciprocalLatticeDisplacement1D *-- Periodic1DLatticeGeometry : geometry
    ReciprocalLatticeDisplacement2D *-- Periodic2DLatticeGeometry : geometry
    ReciprocalLatticeDisplacement3D *-- Periodic3DLatticeGeometry : geometry
    ReciprocalLatticeDisplacement --> IntegerLatticeDisplacement : composes

    ReciprocalSpaceVector1D *-- Periodic1DLatticeGeometry : geometry
    ReciprocalSpaceVector2D *-- Periodic2DLatticeGeometry : geometry
    ReciprocalSpaceVector3D *-- Periodic3DLatticeGeometry : geometry

    ReciprocalCoordinateRecoveryResult1D *-- "2" ReciprocalSpaceVector1D : source and reconstruction
    ReciprocalCoordinateRecoveryResult2D *-- "2" ReciprocalSpaceVector2D : source and reconstruction
    ReciprocalCoordinateRecoveryResult3D *-- "2" ReciprocalSpaceVector3D : source and reconstruction
    ReciprocalCoordinateRecoveryResult1D *-- ReciprocalLatticeCoordinate1D : recovered coordinate
    ReciprocalCoordinateRecoveryResult2D *-- ReciprocalLatticeCoordinate2D : recovered coordinate
    ReciprocalCoordinateRecoveryResult3D *-- ReciprocalLatticeCoordinate3D : recovered coordinate
```

Only the geometry and value classes belong to `ksdft2effmass.geometry.periodic`.
`IntegerLatticeDisplacement` is shown to make the composition explicit, but its current
implementation owner is PhysKit's `LatticeDisplacement`. Real-space kernels, hopping
terms, periodic fibers, and Bloch states are consumers outside this package.

## Direct and reciprocal construction

```mermaid
flowchart LR
    Geometry[Periodic3DLatticeGeometry] --> A[direct primitive basis A]
    Geometry --> B[reciprocal primitive basis B]

    N[integer displacement n] --> RD[DirectLatticeDisplacement3D]
    A --> RD
    RD --> R[physical displacement R = A n]

    M[integer displacement m] --> GD[ReciprocalLatticeDisplacement3D]
    B --> GD
    GD --> GV[physical reciprocal displacement G = B m]

    Q[ReciprocalLatticeCoordinate3D q] --> K[ReciprocalSpaceVector3D]
    B --> K
    K --> KV[physical reciprocal-space vector k = B q]

    A --> Dual[duality relation A transpose B = 2 pi I]
    B --> Dual
```

Integer direct and reciprocal displacements share the same provider coordinate shape but
acquire different physical meanings through the lattice that acts on them. A reciprocal-
space vector admits real coefficients and is not a reciprocal-lattice displacement.

## Reciprocal-coordinate recovery

```mermaid
flowchart TD
    K[source ReciprocalSpaceVector3D] --> Geometry[source vector geometry]
    Geometry --> Solve[solve B q = k in float64]
    K --> Solve
    Solve --> Q[recovered ReciprocalLatticeCoordinate3D]
    Q --> KR[reconstructed ReciprocalSpaceVector3D]
    K --> Error[reconstruction residual]
    KR --> Error
    K --> Result[ReciprocalCoordinateRecoveryResult3D]
    Q --> Result
    KR --> Result
    Error --> Result
```

The dimensional geometry owns the solve directly; there is no recovery-action class or
abstract result hierarchy. The result reports numerical reconstruction error. Tolerance
selection, pass/fail verification, reciprocal-quotient representative selection, and
periodic-state interpretation remain separate operations.

## Ownership and dependency direction

```mermaid
flowchart TD
    PK[PhysKit lattices, integer displacements, quantities, units, metrics]
    KG[KSD periodic geometry values]
    KV[KSD direct and reciprocal displacement and coordinate values]
    Models[KSD scientific models]
    Consumers[periodic fibers, kernels, calculators, and analyzers]

    PK --> KG
    PK --> KV
    KG --> KV
    KG --> Models
    KV --> Consumers
    Models --> Consumers

    Legacy[legacy ksdft2effmass.solidstate lattices]
    Projection[explicit dimension-owned legacy projection]
    Legacy --> Projection
    Projection --> KG
```

Core geometry has no dependency on scientific models, real-space kernels, periodic
fibers, calculations, campaigns, serialization, or the legacy lattice subsystem. Only
isolated migration projections import legacy records.
