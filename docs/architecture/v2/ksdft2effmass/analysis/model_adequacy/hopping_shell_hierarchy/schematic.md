# HSH-1 calculation schematic

```mermaid
flowchart TD
    D[Periodic2DHoppingShellHierarchyDefinition]
    P[Compose exact retained scalar parent definition]
    S[Reconstruct source hopping family]
    Y[Check and project exact real D4 target]
    O[Construct canonical orbit inventory and shell masks]
    Q[Construct spectral and operator quadratics]
    N[Determine channel minima and nonemptiness]
    U[Construct feasible pairs and upper bounds]
    C[Construct outward-rounded support certificates]
    W[Verify common witnesses]
    H[Resolve hierarchy-level minimum-class claim]
    E[Evaluate fixed points on withheld 31x31 parent mesh]
    R[Periodic2DHoppingShellHierarchyResult]
    J[Schema-v1 serializer]
    V[Independent typed verifier]
    X[Standalone wire/source verifier]

    D --> P --> S --> Y --> O --> Q --> N
    N --> U
    N --> C
    N --> W
    U --> H
    C --> H
    W --> H
    H --> E --> R
    R --> J
    D --> V
    R --> V
    J --> X
```

## Information-flow restrictions

- Source bytes and the frozen definition determine the exact projected target.
- Training coordinates and weights determine quadratics, feasible sets, certificates,
  and dispositions.
- Withheld direct-parent values are opened only after all training proof objects are
  fixed.
- Withheld diagnostics cannot alter weights, thresholds, coefficient bounds, shell
  order, witnesses, certificate directions, distance bounds, or dispositions.
- Serialization transports already constructed objects; it does not infer scientific
  meaning or repair invalid results.
- The standalone verifier may consume files and manifests but must not import producer
  modules.

## Per-class disposition logic

```mermaid
flowchart TD
    A[Reconstruct both restricted quadratics] --> B{Premises valid?}
    B -- no --> Z[invalid-premise]
    B -- yes --> C{Spectral set nonempty?}
    C -- no --> D[spectral-set-empty]
    C -- yes --> E{Operator set nonempty?}
    E -- no --> F[operator-set-empty]
    E -- yes --> G{Verified common witness?}
    G -- yes --> H[compatible-common-witness]
    G -- no --> I{Certified lower bound > resolution?}
    I -- yes --> J[certified-separated]
    I -- no --> K[unresolved-nonempty]
```

## Hierarchy-level decision

The hierarchy result may emit `minimum-tested-compatible-class-certified` only if the
first compatible class has an explicit witness and every earlier class is either
channel-empty or certified separated. If no class is compatible or any smaller class is
unresolved, the result reports only bounded per-class dispositions and, when present,
the first class with a found witness without calling it minimal.
