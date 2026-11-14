# Hopping-locality schematics

## Installed nominal hierarchy

```mermaid
flowchart TD
    H[HoppingLocality] --> P[PeriodicHoppingLocality]
    P --> D1[Periodic1DHoppingLocality]
    P --> D2[Periodic2DHoppingLocality]
    P --> D3[Periodic3DHoppingLocality]
    D1 --> R11[Periodic1D rank one]
    D1 --> R12[Periodic1D rank two]
    D1 --> R1N[Periodic1D rank N]
    D2 --> R22[Periodic2D rank two]
    D2 --> R2N[Periodic2D rank N]
    D3 --> R32[Periodic3D rank two]
    D3 --> R3N[Periodic3D rank N]
```

Requests, analyses, and analyzers follow the same domain-to-periodic-to-dimension-to-rank
ownership chain. Rank two and rank $N$ are sibling capabilities.

## Installed numerical routes

```mermaid
flowchart TD
    S1[Retained scalar Fourier diagnostics] --> A1[Periodic1D rank-one adapter]
    B1[Unchanged 1D block Fourier coefficients] --> A2[Periodic1D rank-two or rank-N tail analyzer]
    M23[Exact 2D or 3D rank-two KSD model] --> P23[PhysKit raw block-power analyzer]
    F23[2D or 3D rank-N Fourier series] --> R23[Representation projection]
    R23 --> P23
    P23 --> K[KSD retained-rank normalization and metric-shell aggregation]
    A1 --> T1[Scalar coefficient tails]
    A2 --> T2[Block tails and applicable monotonicity]
    K --> S23[Cell-block powers by displacement and shell]
```

The rank-$N$ periodic-2D/3D route remains representation level. Only the installed
rank-two dimensional route starts from an exact KSD block-hopping scientific model.

## Peer locality resolutions

```mermaid
flowchart TD
    M[Exact periodic block-hopping model] --> C[Cell-block locality analyzer]
    M --> O[Orbital-resolved locality analyzer]
    M --> W[MLWF-resolved locality analyzer]
    E[Ordered periodic basis embedding] --> O
    E --> W
    P[MLWF localization and gauge provenance] --> W
    C --> CR[Block powers and shell aggregates]
    O --> OR[Directed basis-pair powers and physical displacements]
    W --> WR[Center-attributed MLWF-pair powers and physical displacements]
```

The analyzers are peers. MLWF-resolved locality does not invoke orbital-resolved or
cell-block locality as an implementation step, although independent verification may
check that element powers sum to the block power.

## Geometry and basis correlation

```mermaid
flowchart LR
    G[Periodic lattice geometry A] --> D[Physical element displacement]
    N[Integer displacement n] --> D
    S[Source center s alpha] --> D
    T[Target center s beta] --> D
    D --> F[d alpha beta n equals A times n plus s beta minus s alpha]
    H[Coefficient T alpha beta of n] --> P[Element power absolute T squared]
    F --> R[Resolved locality result]
    P --> R
```

Geometry supplies the primitive lattice. The embedding supplies the ordered internal
centers. Neither owner alone can infer the physical element displacement.

## MLWF provenance boundary

```mermaid
flowchart TD
    W90[Wannier90 localization owner] --> A[Authenticated localization artifacts]
    A --> P[Project Koios reusable parsing and provenance mechanics]
    P --> E[KSD ordered MLWF embedding and correlation]
    H[Correlated hopping coefficient artifact] --> E
    G[KSD periodic scientific model identity] --> E
    E --> L[KSD MLWF-resolved locality analysis]
    L --> C[Calculation-owned interpretation thresholds and retained evidence]
```

The locality owner consumes a correlated localization result. It does not execute
Wannier90, infer missing provenance, or promote an artifact into a validated material
model.

## Separation from truncation

```mermaid
flowchart LR
    H[Unchanged hopping coefficients] --> L[Locality analysis]
    H --> T[Explicit support-truncation operation]
    L --> D[Diagnostic result]
    T --> O[Truncated represented operator]
    O --> E[Operator and band consequences]
```

Locality diagnoses unchanged coefficients. Removing coefficients and evaluating the
resulting operator remain separate operations.
