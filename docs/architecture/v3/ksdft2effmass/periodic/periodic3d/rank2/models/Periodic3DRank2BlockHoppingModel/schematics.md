# `Periodic3DRank2BlockHoppingModel` schematic

```mermaid
flowchart TD
    N[Periodic3DRankNModel] --> Q[Periodic3DRank2Model]
    Q --> M[Periodic3DRank2BlockHoppingModel]
    P[PeriodicBlockHoppingModel] --> M
    I[model identifier] --> M
    R[PeriodicModelRole] --> M
    B[Periodic3DBasisIdentity: two ordered coordinates] --> M
    G[Periodic3DLatticeGeometry: ordered basis A and length unit] --> M
    G --> D[derived DirectLattice3D and metric G = AᵀA]
    H[PhysKit dense or sparse 3D block representation] --> M
    M --> A[exact dimension, basis-rank, shape, support, and Hermiticity admission]
    M --> L[optional hopping-locality request]
    S[explicit shell labels] --> L
```

The locality request consumes the model as a peer operation. It is not inherited by or
stored inside the model.
