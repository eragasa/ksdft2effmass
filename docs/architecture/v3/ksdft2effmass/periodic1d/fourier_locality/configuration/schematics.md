# Configuration schematics

## Direct-record boundary

```mermaid
flowchart LR
    P[Exact parent identity, numerators, and denominator] --> C[Periodic1DFourierLocalityConfiguration]
    M[Construction extents and evaluation stagger] --> C
    S[Support radii] --> C
    T[Thresholds and consistency terms] --> C
    C --> Q[Exact-rational-derived coordinate tuples]
    C --> A[Periodic1DFourierLocalityAnalyzer]
    C --> V[Independent verifier]
```

The configuration follows the direct PIAB1D pattern: it is a typed input record, not a
model factory or protocol registry.

## Runtime ownership

```mermaid
flowchart TB
    C[Configuration values]
    C --> A[Analyzer]
    A --> Q[Reduced-momentum quantities]
    A --> H[HermitianHamiltonian fibers]
    A --> O[Reciprocal operator samples]
    A --> B[Block hopping models]
```

Runtime Hamiltonians and operators are constructed by the action that uses them. They
are not hidden properties of the wire record.

## Decode path

```mermaid
flowchart LR
    J[Typed JSON mapping] --> F[Exact field and container checks]
    F --> C[Configuration constructor]
    C --> I[Parent, inventory, threshold, and disjointness invariants]
```
