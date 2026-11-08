# `Periodic1DRank2BlockHoppingModel` schematic

```mermaid
flowchart LR
    N[Periodic1DRankNModel] --> Q[Periodic1DRank2Model]
    Q --> M[Periodic1DRank2BlockHoppingModel]
    H0[PeriodicBlockHoppingModel] --> M
    I[model identity] --> M
    R[PeriodicModelRole] --> M
    B[Periodic1DBasisIdentity: two ordered coordinates] --> M
    G[Periodic1DLatticeGeometry] --> M
    G --> L[PhysKit DirectLattice1D]
    H[PhysKit dense or sparse rank-two hopping model] --> M
    M --> A[exact dimension, basis-rank, shape, support, and Hermiticity admission]
```

The KSD value retains physical period and unit ownership. PhysKit owns the reconstructed
direct-lattice primitive and block-hopping representation. Neither provider value is a
KSD superclass.

## Study-by-study legacy migration

```mermaid
flowchart LR
    F[finite Fourier transform] --> B[existing BlockHoppingModel1D]
    B --> C[existing cyclic-to-ordinary conversion result]
    C --> E[ordinary source and removed-Nyquist evidence remain distinct]
    E --> S[existing study composition root supplies identity, role, geometry, basis, and energy reference]
    S --> P[PhysKit dense block-hopping representation]
    P --> M[existing Periodic1DRank2BlockHoppingModel]
    M --> V[parity, replay, and provenance gates]
    V --> N[new study analysis consumes the scientific model]
    C --> H[historical study contract remains active until its migration passes]
```

The diagram adds no class to the approved inheritance hierarchy. The study composition
root is the existing calculation or analyzer assembly boundary being migrated; it is not
a proposed reusable base, adapter, manager, or admission class.
