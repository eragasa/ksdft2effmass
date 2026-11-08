# `PeriodicBlockHoppingModel` schematic

```mermaid
flowchart TD
    PM[PeriodicModel] --> BH[PeriodicBlockHoppingModel]

    D1[Periodic1DRankNModel] --> R1[Periodic1DRank2Model]
    D2[Periodic2DRankNModel] --> R2[Periodic2DRank2Model]
    D3[Periodic3DRankNModel] --> R3[Periodic3DRank2Model]

    R1 --> M1[Periodic1DRank2BlockHoppingModel]
    R2 --> M2[Periodic2DRank2BlockHoppingModel]
    R3 --> M3[Periodic3DRank2BlockHoppingModel]

    BH --> M1
    BH --> M2
    BH --> M3

    B1[Periodic1DBasisIdentity] --> M1
    B2[Periodic2DBasisIdentity] --> M2
    B3[Periodic3DBasisIdentity] --> M3

    G1[Periodic1DLatticeGeometry] --> M1
    G2[Periodic2DLatticeGeometry] --> M2
    G3[Periodic3DLatticeGeometry] --> M3

    V[PhysKit dense or sparse block representation] --> M1
    V --> M2
    V --> M3

    M1 --> A[exact dimension, basis-rank, shape, and Hermiticity admission]
    M2 --> A
    M3 --> A
```

The rank branch and representation branch express independent facts. Fixed rank refines
the dimensional finite-rank scientific model; block-hopping behavior supplies composed
provider representation and shared admissibility. The concrete class is the correlation
boundary.

PhysKit storage remains a composed immutable value. KSD does not subclass provider
representation classes and does not project structured basis coordinates through the
provider's descriptive basis string.
