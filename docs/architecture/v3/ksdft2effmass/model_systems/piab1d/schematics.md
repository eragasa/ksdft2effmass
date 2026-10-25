# Schematics

## Ownership and execution

```mermaid
flowchart LR
    P[PhysKit PIAB1D model and solver] --> C[run_01_calculation.py]
    K[KSD reduction and analyses] --> C
    C --> R[Piab1dCalculationResult]
    R --> V[run_02_verification.py]
    I[Independent reference analyzers] --> V
    V --> Q[Piab1dVerification]
    Q --> D[Authenticated Piab1dVisualizationData]
    D --> Z[run_03_render.py]
    Z --> F[13 immutable PNG figures]
```

## Typed result composition

```mermaid
classDiagram
    class Piab1dCalculationResult
    class Piab1dConfiguration
    class HamiltonianResultSection
    class EigensystemResultSection
    class SpectralReductionResultSection
    class QuadratureResultSection
    class AnalyticalSamplingResultSection
    class Piab1dDiagnostics
    class Piab1dGridSweepAnalysis
    class KineticPotentialDecompositionResult

    Piab1dCalculationResult *-- Piab1dConfiguration
    Piab1dCalculationResult *-- HamiltonianResultSection
    Piab1dCalculationResult *-- EigensystemResultSection
    Piab1dCalculationResult *-- SpectralReductionResultSection
    Piab1dCalculationResult *-- QuadratureResultSection
    Piab1dCalculationResult *-- AnalyticalSamplingResultSection
    Piab1dCalculationResult *-- Piab1dDiagnostics
    Piab1dCalculationResult *-- Piab1dGridSweepAnalysis
    Piab1dCalculationResult *-- KineticPotentialDecompositionResult
```

## Verification composition

```mermaid
flowchart TD
    R[Typed calculation result] --> A[derive visualization projection]
    A --> H[SHA-256 digest]
    R --> C[core reconstruction]
    R --> E[eigenpair sweep reconstruction]
    R --> N[residual norm reconstruction]
    R --> G[finite algebraic reconstruction]
    R --> K[decomposition reconstruction]
    C --> V[operation-named verification components]
    E --> V
    N --> V
    G --> V
    K --> V
    H --> V
    V --> Q{all 79 comparisons pass?}
    Q -- no --> S[stop before rendering]
    Q -- yes --> Z[render closed 13-plot inventory]
```

The arrows identify data dependencies. They do not represent a generic Workflow
framework or publication lifecycle.
