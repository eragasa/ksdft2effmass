# M2 calculation schematic

```mermaid
flowchart TD
    D[Periodic1DMultibandAlignmentCalculationDefinition]
    H[Parent block-Hamiltonian samples]
    E[Retained eigensystem]
    P[Polar frame transport]
    A[Periodic gauge attack]
    Q[Pointwise Procrustes alignment]
    G[One global-unitary alignment]
    O[Projected represented operators]
    F[Complete Fourier transforms]
    R[Gauge-resolved range study]
    W[Staggered evaluation diagnostics]
    X[Periodic1DMultibandAlignmentCalculationResult]
    S[Schema-v1 serializer]
    V[Independent verifier]

    D --> H --> E --> P
    P --> A
    P --> Q
    A --> Q
    P --> G
    A --> G
    P --> O
    A --> O
    Q --> O
    O --> F --> R
    D --> W
    R --> X
    W --> X
    P --> X
    A --> X
    Q --> X
    G --> X
    X --> S
    X --> V
```

## Channel identities

| Channel | Frame | Invariance status | Locality role |
|---|---|---|---|
| Reference | transported $F(k)$ | baseline | baseline hopping decay |
| Attacked | $F(k)A(k)$ | same subspace and spectrum | demonstrates gauge-sensitive blocks |
| Pointwise aligned | attacked frame with $U(k)$ | constructed recovery | tests exact pointwise recovery |
| Globally constrained | attacked frame with one $U_0$ | finite constrained family | diagnostics only; not Fourier transformed as the primary recovered channel |

Training determines all frame and hopping objects. Evaluation coordinates only test the
already frozen objects.
