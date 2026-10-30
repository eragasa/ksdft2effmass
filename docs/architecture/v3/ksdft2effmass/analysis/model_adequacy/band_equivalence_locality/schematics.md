# Schematics

## Typed nominal lifecycle

```mermaid
flowchart LR
    C[Python-authored typed request] --> A[bound analyzer]
    A --> S[plain immutable scientific analysis]
    S --> P[analysis recorder]
    P --> R[passive retained result]
    R --> B[exact canonical result bytes]
    B --> V[byte-owning result verifier]
    I[constructor-bound diagnostic analyzers] --> V
    V --> Q[typed verification]
    V --> D[authenticated visualization projection]
    Q --> G{verification passes}
    D --> G
    G -- no --> X[stop before rendering]
    G -- yes --> Z[family visualizer]
    Z --> P[closed baseline PNG]
```

The recorder projects a completed analysis without invoking the analyzer again. The
verifier does not invoke the production analyzer, and the visualizer does not invoke
either scientific calculation route.

## Finite scientific composition

```mermaid
flowchart TD
    P[four-state Hermitian parent field] --> E[ordered eigensystem]
    E --> S[lowest rank-two projector and frame]
    S --> T[closed frame transport]
    T --> H[reference represented Hamiltonian]
    T --> U[declared smooth SO2 gauge]
    U --> C[comparison represented Hamiltonian]
    H --> F[complete multidimensional Fourier transform]
    C --> F
    F --> N[Nyquist and ordinary-lattice channels]
    N --> M[complete physical-metric shells]
    M --> R[interpolation truncation and total diagnostics]
```

Spatial dimension, parent-fiber dimension, and retained rank are separate contracts.

## Ownership layers

```mermaid
flowchart TD
    O[Optimization finite-periodic meshes transforms evaluation and diagnostics]
    P[PhysKit direct-lattice metric]
    O --> K[KSD band-equivalence locality calculation]
    P --> K
    K --> R[KSD typed request scientific analysis retained result and verification]
    R --> S[calculation-owned direct stage scripts]
    S --> F[local unsealed execution files and PNG]
```

No dependency points from installed source into a calculation or experiment directory.

## Error-channel separation

```mermaid
flowchart LR
    D[direct represented field] --> I[complete finite interpolation]
    I --> C[ordinary-lattice conversion]
    C --> T[metric-shell truncation]
    D --> E[total comparison]
    I --> E
    T --> E
```

Interpolation, conversion, truncation, and total comparisons are reported separately.
The diagram shows composition, not permission to add separately maximized norms.

## Direct family stages

```mermaid
flowchart LR
    S[Square triangular-honeycomb simple-cubic or FCC-diamond typed request] --> C[run_01_calculation.py]
    C --> E[execution.json request bytes result bytes]
    E --> V[run_02_verification.py]
    V --> Q[verification.json plus typed projection]
    Q --> R[run_03_render.py]
    R --> F[band-equivalence-locality-requirements.png]
```

The periodic-2D square, periodic-2D triangular/honeycomb, periodic-3D simple-cubic, and
periodic-3D FCC/diamond calculation roots own independent instances of these stages and
distinct execution identities. Every stage refuses overwrite, writes behind an
incomplete directory, and exposes a complete directory by rename. No stage seals or
publishes evidence.
