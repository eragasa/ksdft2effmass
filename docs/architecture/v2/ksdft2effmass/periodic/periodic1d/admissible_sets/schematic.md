# M3 calculation schematic

```mermaid
flowchart TD
    D[Periodic1DConstrainedAdmissibleSetCalculationDefinition]
    B[Compose exact M2 definition]
    M[Execute M2 baseline]
    C[Construct continuous shift/splitting candidate family]
    A[Apply nine global-rotation alignment channels]
    T[Training spectral and operator-loss quadratics]
    E[Staggered evaluation losses]
    Q[Analytic squared-loss quadratics]
    K[Compatible-case common witness]
    S[Separated-case splitting-axis certificate]
    L[Range-one locality summary]
    R[Periodic1DConstrainedAdmissibleSetCalculationResult]
    J[Schema-v1 serializer]
    V[Independent verifier]

    D --> B --> M --> C --> A
    A --> T
    A --> E
    T --> Q
    Q --> K
    Q --> S
    M --> L
    K --> R
    S --> R
    E --> R
    L --> R
    R --> J
    R --> V
```

## Information-flow restrictions

- M2 training data determines the reference and attacked represented operators.
- M3 training formulas determine exact quadratics over the continuous parameter
  rectangle; thresholds then determine witnesses and separation certificates.
- M3 evaluation coordinates are disjoint and diagnostic only.
- Evaluation data cannot change any threshold, quadratic, witness, certificate,
  parameter range, or disposition.
- The post-hoc sensitivity package consumes sealed M3 evidence but is not an input to
  the confirmatory package.

## Disposition logic

```mermaid
flowchart LR
    A[Evaluate quadratic sublevel geometry] --> B{Prospective common witness feasible?}
    B -- yes --> C[compatible-witness]
    B -- no --> D{Analytic lower bound > resolution?}
    D -- yes --> E[certified-separated]
    D -- no --> F[unresolved]
```

Failure of the prospective witness alone cannot prove separation. The result follows
the `unresolved` branch unless the independent splitting-axis lower bound closes the
gap above the frozen resolution.
