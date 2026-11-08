# `Periodic2DFiniteDifferenceHamiltonian` schematic

```mermaid
flowchart LR
    M[Periodic2DCosinePotentialModel] --> R[exact finite-difference request]
    K[reduced momentum] --> R
    N[odd periodic grid] --> R
    R --> H[Periodic2DFiniteDifferenceHamiltonian]
    H --> X[x kinetic block with Bloch seam]
    H --> Y[y kinetic block with Bloch seam]
    X --> S[Kronecker sum]
    Y --> S
    M --> V[sampled diagonal cosine potential]
    R --> V
    S --> A[represented matrix]
    V --> A
    A --> O[Periodic2DFiniteDifferenceHamiltonianResult]
    R --> O
```

The result remains in its native coordinate state space. Comparison with a plane-wave
result requires a separately owned common-space transport.
