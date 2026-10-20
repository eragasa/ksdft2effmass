# Schematics

```mermaid
classDiagram
    FiniteDomainABC <|-- FiniteMomentumMeshDomain
    FiniteDomainABC <|-- FiniteTranslationDomain
    CenteredUniformMesh --> FiniteMomentumMeshDomain
    MomentumSampleRole --> FiniteMomentumMeshDomain
```
