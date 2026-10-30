# Calculation flow for higher-rank gauge alignment

## Scientific producer flow

```mermaid
flowchart TD
    Q[Immutable calculation request]
    P[Analytic parent spectrum and reference frame]
    G[Depth-dependent gauge attack]
    GS[Global-unitary selection once at M = 2049]
    M[Construction meshes M = 513, 1025, 2049]
    T[Common closed-loop transport of analytic reference frame]
    A{Prescribed gauge alignment}
    IDENTITY[identity]
    GLOBAL[global-unitary reused without refitting]
    POINTWISE[pointwise-unitary selected per construction mesh]
    ORACLE[known-inverse-oracle]
    F[Immutable gauge-aligned operator and frame fields]
    R[Recovery analysis]
    FT[PhysKit odd-mesh finite-periodic transform]
    E[Shifted 8191-point complete-series and direct evaluation]
    S[Nine frozen symmetric supports]
    D[Interpolation, truncation, total-error, tail, and bound diagnostics]
    O[Correlated immutable calculation result]

    Q --> P --> G
    G --> GS
    G --> M
    M --> T
    GS --> A
    M --> A
    A --> IDENTITY --> F
    A --> GLOBAL --> F
    A --> POINTWISE --> F
    A --> ORACLE --> F
    F --> R --> FT --> E
    FT --> S
    E --> D
    S --> D --> O
    T --> O
    GS --> O
```

Closed-loop transport is common evidence and does not define a fifth gauge alignment.
The four gauge alignments are also distinct from the interpolation, truncation, and total
error channels evaluated after Fourier transformation.

## Typed stage lifecycle

```mermaid
flowchart TD
    AR[Complete immutable gauge-alignment analysis request]
    C[fields.py: construct nominal aligned fields]
    R[recovery.py: frame and operator recovery]
    F[fourier.py: coefficients and structural evidence]
    I[interpolation.py: shifted immutable fields]
    L[locality.py: support and error-channel evidence]
    A[assembly.py: correlate stages and assemble result]
    B[Canonical typed bytes and SHA-256 identity]
    X[Typed unresolved status; downstream values absent]

    AR --> C --> R --> F --> I --> L --> A --> B
    AR -. rank, integrity, or backend failure .-> X
```

Each stage retains its exact source request. Assembly rejects evidence from an equal but
replacement request, unrelated same-shaped arrays, wrong gauge alignment, wrong mesh,
or inconsistent selection provenance. Serialization owns wire mechanics only and does
not recompute scientific quantities.

`Periodic1DHigherRankAlignmentAnalyzer` receives the complete request and concrete
Optimization, PhysKit, and KSD owners in its constructor. Its `execute()` method has no
arguments. It does not inspect registries, import the historical calculation-local
Workflow, or infer missing physical identities.

## Later authenticated lifecycle

```mermaid
flowchart LR
    C[Typed calculation bytes]
    I[Independent numerical recomputation]
    V[Byte-owning verification]
    D[Authenticated plotting data]
    G[Atomic figure publication]

    C --> V
    I --> V
    V --> D --> G
```

This lifecycle is not implemented for the higher-rank family. Independent recomputation
must bypass the production analyzer. Verification must own and hash the exact admitted
calculation bytes. Rendering must consume authenticated data and calculate no new
scientific values.

## Future dimensional and metric separation

```mermaid
flowchart TD
    FA[Fiberwise gauge-alignment equations]
    D1[Implemented periodic-1D orthonormal specialization]
    D2[Future reviewed 2-D mesh, Fourier-index, and support geometry]
    D3[Future reviewed 3-D mesh, Fourier-index, and support geometry]
    NM[Future reviewed metric-aware nonorthonormal formulation]

    FA --> D1
    FA -. no current implementation .-> D2
    FA -. no current implementation .-> D3
    FA -. distinct metric contract .-> NM
```

The dashed boxes describe architectural boundaries, not available classes, stubs, or
software capabilities. The present 1-D Fourier and locality owners remain dimension
specific, and the present Procrustes contract remains orthonormal and $U(r)$-valued.
