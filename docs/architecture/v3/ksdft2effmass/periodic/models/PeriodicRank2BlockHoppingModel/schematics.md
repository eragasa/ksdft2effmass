# `PeriodicRank2BlockHoppingModel` schematic

```mermaid
flowchart TD
    M[Model identity] --> P[PeriodicModel]
    R[PeriodicModelRole] --> P
    P --> B[PeriodicBlockHoppingModel]
    B --> Q[PeriodicRank2BlockHoppingModel]
    Q --> D1[Periodic1DRank2BlockHoppingModel]
    Q --> D2[Periodic2DRank2BlockHoppingModel]
    Q --> D3[Periodic3DRank2BlockHoppingModel]
    G1[Periodic1DLatticeGeometry] --> D1
    G23[DirectLatticeMetric] --> D2
    G23 --> D3
    V[PhysKit dense or sparse block representation] --> D1
    V --> D2
    V --> D3
    D1 --> A[exact dimensional and Hermiticity admission]
    D2 --> A
    D3 --> A
```

PhysKit storage remains a composed value. The KSD hierarchy never subclasses the
provider representation classes. Each child exposes the exact PhysKit direct lattice
required by shared dimensional admission.
