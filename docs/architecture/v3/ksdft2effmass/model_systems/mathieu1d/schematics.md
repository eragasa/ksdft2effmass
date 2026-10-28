# Schematics

## Direct lifecycle

```mermaid
flowchart LR
    C[Python-authored Mathieu1dConfiguration] --> A[Mathieu1dAnalyzer]
    P[Periodic parent constructors] --> A
    F[Fourier, truncation, fit, and diagnostics] --> A
    A --> R[Mathieu1dCalculationResult]
    R --> V[Mathieu1dVerifier]
    I[Independent dense, sparse, Fourier, and fit formulas] --> V
    V --> Q[Mathieu1dVerification: 873 comparisons]
    V --> D[Authenticated Mathieu1dVisualizationData]
    Q --> Z[Mathieu1dVisualizer]
    D --> Z
    Z --> G[Two validated PNG values]
```

The arrows are data dependencies, not a generic Workflow or execution graph.

## Typed result composition

```mermaid
classDiagram
    class Mathieu1dCalculationResult
    class Mathieu1dConfiguration
    class Mathieu1dRefinementResult
    class Mathieu1dBandSamplesResult
    class Mathieu1dTransformResult
    class Mathieu1dRangeResult

    Mathieu1dCalculationResult *-- Mathieu1dConfiguration
    Mathieu1dCalculationResult *-- Mathieu1dRefinementResult
    Mathieu1dCalculationResult *-- Mathieu1dBandSamplesResult
    Mathieu1dCalculationResult *-- Mathieu1dTransformResult
    Mathieu1dCalculationResult *-- "1..*" Mathieu1dRangeResult
```

## Representation and reduction boundaries

```text
finite plane-wave fibers ─────┐
                              ├── sampled ordered parent spectra
periodic finite-difference ───┘

selected training band
        │ complete finite Fourier transform
        ▼
all N hopping representatives
        │
        ├── symmetric truncation ──► mediated range model
        └── same range basis ──────► direct weighted fit
                                      │
                                      ▼
                         route and withheld-sample diagnostics
```

The two parent matrices inhabit different finite coordinate representations and are
compared only through ordered eigenvalues at common sampled momenta. Range routes are
compared only after they share the same representative inventory.

## Authentication boundary

```text
exact result.json bytes
        │ SHA-256 + typed reconstruction
        ▼
independent complete result ──► independent comparisons
        │
        └── visualization projection ──► projection SHA-256
                                             │
passing stored verification + fresh equality │
                         └─────────────────────┘
                                      ▼
                               atomic rendering
```

Neither digest identity nor successful rendering establishes scientific validation.
