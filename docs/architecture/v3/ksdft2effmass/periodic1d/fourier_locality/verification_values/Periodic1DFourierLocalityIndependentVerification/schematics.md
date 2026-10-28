# `Periodic1DFourierLocalityIndependentVerification` schematics

```mermaid
classDiagram
    class Periodic1DFourierLocalityIndependentVerification {
        +comparisons
    }
    class MaximumAbsoluteErrorComparison
    Periodic1DFourierLocalityIndependentVerification *-- MaximumAbsoluteErrorComparison
```

```mermaid
flowchart LR
    R[Admitted calculation result] --> I[Independent verifier]
    P[Verifier-owned projection] --> I
    I --> S[Scientific reference comparisons]
    I --> V[Projection-to-result comparisons]
    S --> X[IndependentVerification comparison mapping]
    V --> X
```
