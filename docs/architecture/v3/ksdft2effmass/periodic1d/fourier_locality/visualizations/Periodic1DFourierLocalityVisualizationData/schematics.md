# `Periodic1DFourierLocalityVisualizationData` schematics

```mermaid
flowchart TB
    R[Independent CalculationResult]
    R --> P[Parent and gap projection]
    R --> C[Coefficient and omitted-norm projection]
    R --> E[Three-channel projection]
    R --> X[Error--complexity and passage projection]
    R --> D[Route-agreement projection]
    P --> V[VisualizationData]
    C --> V
    E --> V
    X --> V
    D --> V
```

```mermaid
classDiagram
    class Periodic1DFourierLocalityVisualizationData {
        +parent_gap_values
        +coefficient_values
        +error_channel_values
        +error_complexity_values
        +route_agreement_values
        +plot_inventory
    }
```

The verifier binds canonical projection bytes to the admitted subject through separate
subject and projection digests; the projection does not embed a duplicate subject digest.
