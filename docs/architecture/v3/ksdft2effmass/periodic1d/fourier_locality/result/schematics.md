# Result-module schematics

## Aggregate ownership

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

Refinement and sampled-gap values are direct fields of the calculation result. Complete
transform values are direct fields of the mesh result. This keeps four cohesive records
without empty section objects or universal result layouts.

## Admission sequence

```mermaid
flowchart LR
    L[Local typed admission] --> M[Mesh and support correlation]
    M --> C[Coefficient-to-candidate correlation]
    C --> D[Fail-closed decisive dispositions]
    D --> R[Immutable calculation result]
    R --> J[Canonical typed JSON]
    J --> V[Independent byte-owning verifier]
```

The result module does not calculate the parent spectrum and does not own verification,
rendering, file publication, or hashing.
