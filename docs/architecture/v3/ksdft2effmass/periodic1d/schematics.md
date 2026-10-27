# Schematics

## Family-owned direct lifecycle

```mermaid
flowchart LR
    C[Python-authored family configuration] --> A[family analyzer]
    P[periodic parent and finite-representation owners] --> A
    S[solid-state transforms and alignment owners] --> A
    A --> R[family typed result]
    R --> B[result wire bytes]
    B --> V[byte-owning independent verifier]
    I[independent finite formulas] --> V
    V --> Q[family verification aggregate]
    V --> D[authenticated visualization projection]
    Q --> G{all required comparisons pass?}
    D --> G
    G -- no --> X[stop before rendering]
    G -- yes --> Z[family visualizer]
    Z --> F[closed immutable figure inventory]
```

The arrows are direct data dependencies. They do not define a Workflow framework,
registry, or publication lifecycle.

## Ownership layers

```text
PhysKit
  quantities, lattice primitives, represented linear algebra, matrix norms
                         │
                         ▼
model_systems.periodic_1d       solidstate              operators / analysis
finite parent fibers            paths, frames,           represented values and
and Fourier potentials          sewing, transforms       reusable diagnostics
             └──────────────────────┬──────────────────────────┘
                                    ▼
                         periodic1d family analyzer
                                    │
                   concrete typed result and verification
                                    │
                                    ▼
                  calculations/<periodic1d-family>/
                 protocol, stages, provenance, rendering
```

## Eight separate calculation studies

```mermaid
flowchart TD
    P[Periodic1D reusable behavior]
    P --> M[1 Mathieu1D single-band benchmark]
    P --> R1[2 compatible rank-one null control]
    P --> B2[3 rank-two band-equivalence locality]
    P --> C2[4 rank-two composite alignment locality]
    P --> AC[5 confirmatory constrained admissible sets]
    P --> AS[6 scalar direct admissible-set demonstration]
    P --> AT[7 post-hoc threshold sensitivity]
    P --> RN[8 higher-rank composite alignment]
```

No arrow between studies denotes version succession or evidence inheritance. Shared
mechanics do not merge their protocols, inputs, thresholds, result wires, evidence
status, or claims. The eight studies need not create eight reusable source children.

## Native and formal-certificate wires

```text
family analyzer ──> native typed binary64 result bytes ──> independent verifier
                              │                                  │
                              └── digest-bound outward export ──┘
                                             │
                                             ▼
                              proposition-specific certificate
                                             │
                                             ▼
                                 Formal checker result
```

Canonical native bytes remain numerical data. Only exact rational values or documented
outward rational intervals enter exact certificate fields.

## Common-coordinate rule

```text
parent space A ──map A──┐
                        ├── declared common retained coordinates ── comparison
parent space B ──map B──┘
```

Parent matrices are never subtracted directly when their finite spaces, bases, frames,
or coordinate orders differ.
