# Schematics

## Package composition

```mermaid
flowchart TB
    D[data.py: Qho1dVisualizationData]
    E[inventory.py: closed three-member enum]
    S[eigenstates.py]
    T[distortion.py]
    G[diagnostics.py]
    V[visualizer.py: Qho1dVisualizer]
    R[Root PNG renderer]

    D --> S
    D --> T
    D --> G
    E --> V
    S --> V
    T --> V
    G --> V
    V --> R
```

## Authenticated lifecycle

```mermaid
flowchart LR
    B[Exact QHO1D result bytes] --> Q[Qho1dVerifier]
    Q --> D[Authenticated projection]
    Q --> V[Passing verification]
    D --> A{Digest match?}
    V --> A
    A -- no --> F[Fail closed]
    A -- yes --> Z[Qho1dVisualizer]
    Z --> P[Exact three-PNG inventory]
```
