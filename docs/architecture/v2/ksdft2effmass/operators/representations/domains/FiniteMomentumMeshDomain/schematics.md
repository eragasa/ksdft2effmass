# Schematics

```mermaid
flowchart TD
    id["identifier"] --> domain["FiniteMomentumMeshDomain"]
    mesh["CenteredUniformMesh"] --> domain
    convention["coordinate_convention_id"] --> domain
    role["MomentumSampleRole"] --> domain
    domain --> cardinality["cardinality = mesh.point_count"]
    domain --> dimension["dimension = mesh.dimension"]
```

```mermaid
classDiagram
    FiniteDomainABC <|-- FiniteMomentumMeshDomain
    FiniteMomentumMeshDomain *-- CenteredUniformMesh
    FiniteMomentumMeshDomain *-- MomentumSampleRole
```
