# Schematics

## Direct typed lifecycle

```mermaid
flowchart LR
    C[Periodic1DFourierLocalityConfiguration] --> A[Periodic1DFourierLocalityAnalyzer]
    P[Exact four-state parent] --> A
    O[Canonical transform, fit, and diagnostics] --> A
    A --> R[Periodic1DFourierLocalityCalculationResult]
    R --> V[Periodic1DFourierLocalityVerifier]
    I[Independent eigensystem, Fourier, fit, and decision formulas] --> V
    V --> Q[Periodic1DFourierLocalityVerification]
    V --> D[Authenticated visualization data]
    Q --> Z[Periodic1DFourierLocalityVisualizer]
    D --> Z
    Z --> G[Two validated PNG values]
```

The arrows are typed data dependencies, not a Workflow or registry. The complete
calculate, independently verify, and authenticated-render lifecycle is implemented.

## Module ownership

```mermaid
flowchart TB
    PKG[fourier_locality package]
    PKG --> CFG[configuration.py]
    PKG --> ANA[analysis.py]
    PKG --> RES[result.py]
    PKG --> IV[verification_values.py]
    PKG --> VER[verification.py]
    PKG --> VIS[visualizations/]

    CFG --> ANA
    ANA --> RES
    RES --> IV
    IV --> VER
    VER --> VIS
```

The result module owns values and admission correlation only. It does not import a
producer, verifier, renderer, or calculation script.

## Result composition

```mermaid
classDiagram
    class Periodic1DFourierLocalityCalculationResult
    class Periodic1DFourierLocalityConfiguration
    class Periodic1DFourierLocalityEvaluationResult
    class Periodic1DFourierLocalityMeshResult
    class Periodic1DFourierLocalityRangeResult

    Periodic1DFourierLocalityCalculationResult *-- Periodic1DFourierLocalityConfiguration
    Periodic1DFourierLocalityCalculationResult *-- Periodic1DFourierLocalityEvaluationResult
    Periodic1DFourierLocalityCalculationResult *-- Periodic1DFourierLocalityMeshResult
    Periodic1DFourierLocalityMeshResult *-- Periodic1DFourierLocalityRangeResult
```

## Authentication boundary

```mermaid
flowchart LR
    B[Exact result bytes] --> H[SHA-256 identity]
    B --> T[Strict typed reconstruction]
    T --> X[Independent complete reconstruction]
    X --> C[Named comparisons]
    X --> P[Visualization projection]
    P --> PH[Projection SHA-256]
    H --> V[Verification aggregate]
    C --> V
    PH --> V
    V --> R[Authenticated rendering]
```

Digest equality establishes byte identity only.
