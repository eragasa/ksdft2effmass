# Calculation flow for higher-rank frame alignment

## Implemented calculation producer

```mermaid
flowchart TD
    Q[Immutable case request and physical identities]
    P[Analytic parent spectrum and retained frame]
    G[Depth-dependent gauge attack]
    GS[Global unitary selected once at M = 2049]
    M[Unshifted meshes M = 513, 1025, 2049]
    T[Common closed-loop reference-frame transport]
    A[Identity, global, pointwise, and known-inverse alignment]
    F[PhysKit odd-mesh matrix Fourier transform]
    E[Shifted 8191-point direct and Fourier evaluation]
    S[Nine symmetric supports]
    D[Separate interpolation, truncation, total, tail, and bound diagnostics]
    R[Immutable complete calculation result]

    Q --> P --> G
    G --> GS
    G --> M
    GS --> A
    M --> T
    M --> A
    A --> F --> E
    F --> S
    E --> D
    S --> D --> R
    T --> R
    GS --> R
```

`Periodic1DHigherRankAlignmentAnalyzer` receives the request and concrete Optimization
and PhysKit owners in its constructor. Its `execute()` method has no arguments. The
producer does not inspect registries, import the historical calculation-local Workflow,
or infer missing physical identities.

Transport acts on the analytic reference frame and remains separate from all four
alignment families. The global unitary is selected only at $M=2049$ and reused on both
coarser meshes and the shifted direct-evaluation mesh. Pointwise alignment is selected
independently on each construction mesh. The known-inverse channel applies the analytic
inverse directly.

## Later authenticated lifecycle

```mermaid
flowchart LR
    C[Typed calculation bytes]
    I[Independent numerical recalculation]
    V[Byte-owning verification]
    D[Authenticated plotting data]
    G[Atomic figure publication]

    C --> V
    I --> V
    V --> D --> G
```

This second flow is not implemented for the higher-rank family. Independent
recalculation must not call the production analyzer. Verification must own and hash the
exact admitted calculation bytes. Rendering must consume only authenticated data and
must not calculate new scientific values.
