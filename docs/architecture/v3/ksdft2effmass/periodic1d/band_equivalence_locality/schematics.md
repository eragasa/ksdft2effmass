# Schematics

## Flat-parent calculation and retained projection

```mermaid
flowchart TD
    R[Exact flat-parent request]
    R --> CM[Centered construction mesh]
    R --> EM[Disjoint shifted evaluation mesh]
    R --> GD[Sinusoidal GaugeRotation definitions]
    R --> TR[Ordinary truncation ranges]
    CM --> A[Generic GaugeAttack]
    GD --> A
    A --> H[Attacked 2 by 2 matrix field]
    H --> B[Pointwise sorted bands]
    H --> A[Restricted global alignment]
    H --> F[Finite cyclic Fourier blocks]
    F --> N[Remove negative-Nyquist representative]
    N --> I[Complete ordinary interpolation]
    N --> T[Deliberate ordinary truncations]
    EM --> I
    EM --> T
    I --> E[Separate Hamiltonian and sorted-band consequences]
    T --> E
    B --> S[Serialization-free flat analysis]
    A --> S
    E --> S
    S --> P[Canonical retained bytes]
```

## Independent flat verification

```mermaid
flowchart TD
    B[Canonical flat result bytes] --> A[Strict typed readmission]
    B --> H[SHA-256 subject identity]
    A --> R[Admitted request]
    R --> I[Explicit finite sums and independent Bessel series]
    A --> C[Observed scalar hopping and range channels]
    I --> C
    C --> V[Typed composite verification]
    H --> V
    V --> P[Authenticated typed visualization projection]
    P --> G[Closed three-PNG inventory]
```

## Embedded-subspace/rank2 scientific core

```mermaid
flowchart TD
    R[Exact embedded-subspace rank-two request] --> P[Fixed 4 by 4 finite-range parent on centered mesh]
    P --> G{Sampled external-gap gate passes?}
    G -- no --> GF[External-gap-failure result]
    G -- yes --> F[Lowest-two-state raw frame and identity endpoint sewing]
    F --> T[PhysKit closed-loop polar transport]
    T --> B{Band-transport outcome}
    B -- backend failure --> BF[Typed backend-failure result]
    B -- numerical rank failure --> NF[Typed numerically-unresolved result]
    B -- below scientific singular-value gate --> TF[Typed threshold-failure result]
    B -- qualified --> Q[Qualified transported rank-two representation]
    Q --> GR[Sinusoidal GaugeRotation definition]
    GR --> GA[Generic GaugeAttack on the retained representation]
    GA --> O[Retained-space sinusoidal gauge orbit]
    Q --> A[Restricted harmonic alignment]
    Q --> C[Complete cyclic hopping powers and Parseval channels]
    O --> S[Serialization-free embedded analysis]
    A --> S
    C --> S
    S --> CB[Canonical embedded aggregate bytes]
    CB --> CA[Exact-byte readmission and SHA-256 identity]
    CB --> IR[Independent parent Gram-polar and direct-sum reconstruction]
    CA --> V[Typed qualification transport closure harmonic point and hopping checks]
    IR --> V
    V --> VP[Authenticated embedded visualization projection]
    VP --> VI[Closed band alignment locality and numerical-residual PNG inventory]
```

## Bounded parent-hopping family

```mermaid
flowchart TD
    FR[Family request with ordered scales from zero through one] --> MR[Exact member requests with all other controls unchanged]
    MR --> PA[Production single-member analyzer at each scale]
    PA --> FA[Correlated serialization-free family analysis]
    FA --> FB[Canonical family aggregate bytes]
    FB --> FD[Exact-byte admission and family SHA-256 identity]
    MR --> IA[Independent direct-formula member reconstruction at each scale]
    IA --> IC[Per-member qualification transport closure harmonic point and hopping comparisons]
    FD --> IC
    IC --> FV[Typed parent-family verification]
    FV --> FP[Authenticated fully qualified family projection]
    FP --> FI[Closed alignment locality and qualification PNG inventory]
```

## Embedded rank-two ordinary truncation

```mermaid
flowchart TD
    R[Truncation request with fixed embedded template] --> P[One qualified parent preparation]
    P --> Q{Parent and transport qualified?}
    Q -- no --> QS[Closed qualification-stopped outcome]
    Q -- yes --> F[Finite cyclic hopping blocks]
    F --> N[Remove only negative-Nyquist representative]
    N --> C[Conversion power and complete ordinary blocks]
    C --> I[Reference and attacked ordinary interpolation on disjoint mesh]
    C --> T[Conjugate-closed ordinary cutoff inventory]
    T --> E[Truncation-only and total Hamiltonian and spectral channels]
    I --> E
    R --> IR[Independent Gram-polar parent and direct finite sums]
    QS --> V[In-memory composite verification]
    E --> V
    IR --> V
    V --> OW[Canonical aggregate boundary remains open]
```

## Nested momentum refinement

```mermaid
flowchart TD
    RR[Refinement request with exact doubling meshes] --> MA[Complete single-mesh analysis at every size]
    MA --> Q{Every mesh qualified?}
    Q -- no --> QS[Qualification-stopped outcome with all mesh results]
    Q -- yes --> AP[Adjacent nested-mesh comparisons]
    AP --> PC[Parent diagnostic and shared-projector changes]
    AP --> LC[Correlation threshold hopping and angle changes]
    AP --> RC[Fine-mesh band reconstruction and Parseval residuals]
    PC --> D{Required final refinements pass every threshold?}
    LC --> D
    RC --> D
    D -- yes --> C[Converged finite-refinement outcome]
    D -- no --> U[Unresolved finite-refinement outcome]
    RR --> IR[Independent primitive-field mesh construction]
    IR --> IS[Independent single-mesh and shared-parent reconstruction]
    QS --> IV[Existing in-memory composite verification]
    C --> IV
    U --> IV
    IS --> IV
    IV --> OW[Canonical refinement artifact boundary remains open]
```

## Adaptive amplitude refinement

```mermaid
flowchart TD
    AR[Adaptive request on one fixed momentum mesh] --> M[Direct midpoint inventory]
    M --> Q{Parent and transport qualified?}
    Q -- no --> QS[Qualification-stopped outcome]
    Q -- yes --> D[Five separate interpolation-defect channels]
    D --> MP{Every midpoint check passes?}
    MP -- no --> RN[Add only failing midpoints as next nodes]
    MP -- yes --> V[Direct disjoint quarter-point validation]
    V --> VP{Every validation point passes?}
    VP -- yes --> C[Converged finite adaptive outcome]
    VP -- no --> RV[Add only failing quarter points as next nodes]
    RN --> CAP{Declared cap available?}
    RV --> CAP
    CAP -- level cap reached --> LE[Levels-exhausted outcome]
    CAP -- sample cap reached --> SE[Evaluations-exhausted outcome]
    CAP -- continue --> M
    AR --> IR[Independent primitive-field requests and direct formulas]
    QS --> IV[In-memory composite verification]
    C --> IV
    LE --> IV
    SE --> IV
    IR --> IV
    IV --> OW[Canonical refinement artifact boundary remains open]
```
