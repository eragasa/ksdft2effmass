# `ksdft2effmass` package schematics

## Architecture v3 source ownership

```mermaid
flowchart TB
    K[ksdft2effmass]
    K --> M[model_systems]
    K --> P[periodic1d]
    K --> A[analysis]
    K --> H[hamiltonian]
    K --> O[operators]
    K --> S[spaces]
    K --> J[serialization]
    P --> F[periodic1d.fourier_locality]
    M --> PI[piab1d]
    M --> Q[qho1d]
    M --> MA[mathieu1d]
```

Only documented maintained or prospective contracts are shown; this is not an exhaustive
import graph.

## Scientific data direction

```mermaid
flowchart LR
    C[Typed configuration] --> A[Domain analysis]
    A --> R[Immutable typed result]
    R --> V[Byte-owning independent verification]
    V --> D[Authenticated visualization projection]
    D --> G[Closed rendering]
```

Filesystem effects and evidence policy remain outside reusable scientific objects.

## Dependency direction

```mermaid
flowchart LR
    K[ksdft2effmass] --> P[projectkoios.physkit]
    K --> O[projectkoios-optimization]
    P --> O
```

PhysKit must not depend on `ksdft2effmass`.
