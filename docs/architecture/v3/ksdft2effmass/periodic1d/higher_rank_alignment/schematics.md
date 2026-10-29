# Calculation flow for higher-rank frame alignment

## Transport data available now

```mermaid
flowchart LR
    C[Study parameters]
    Q[Selected case, mesh, basis, frame, and sewing]
    F[Frames on the construction mesh]
    T[Closed-loop polar transport]
    L[Neighbor-link singular values and rank]
    U[Periodic-closure unitaries and phases]
    S[Alignment-family outcome]

    C --> Q
    Q --> T
    F --> T
    T --> L
    T --> U
    C --> S
```

The implemented code stores the fixed study parameters, the exact selected transport
geometry and identities, link-by-link transport diagnostics, closure transformations,
and alignment outcomes. It does not yet construct the higher-rank Hamiltonian family.

## Complete calculation planned for a later phase

```mermaid
flowchart TD
    Q[Physical model and numerical parameters]
    P[Parent and attacked Hamiltonians]
    A[Four alignment families]
    T[Parallel transport and periodic closure]
    H[Real-space hopping representations]
    R[Independent numerical recalculation]
    V[Comparison and verification]
    D[Verified plotting data]
    G[Figures]

    Q --> P
    P --> A
    P --> T
    A --> H
    T --> H
    Q --> R
    H --> V
    R --> V
    V --> D --> G
```

The independent recalculation will evaluate the declared observables without calling the
production analysis path. Verification will compare both calculations and bind the plots
to the exact saved result. Figure construction will not calculate new scientific values.
