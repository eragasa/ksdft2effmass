# Repository-level calculations in v1

## Implemented status

Architecture v1 has no `ksdft2effmass.calculators` package and no reusable
calculator executor protocol. Direct calculation behavior is owned by compact
inputs, preflight records, and operation-specific runners under `calculations/`.
Quantum ESPRESSO is the only calculator with retained direct-execution evidence.

```mermaid
flowchart LR
    input["Native QE input"] --> runner["Calculation-specific runner"]
    runner --> pw["pw.x"]
    pw --> native["Native output and .save data"]
    native --> qexsd["io.quantum_espresso.qexsd"]
    qexsd --> semantic["Neutral domain records"]
```

| Surface | Capability |
|---|---|
| `calculations/` runners | Invoke `pw.x` under calculation-specific preflight and retention contracts |
| `ksdft2effmass.io.quantum_espresso.qexsd` | Parse supported QEXSD and construct periodic, Kohn--Sham, plane-wave, and provenance records |

Input generation and process execution are not public Python object models in
v1. QEXSD parsing and semantic construction are implemented Python boundaries.

## Pages

- [Direct simulation model](simulation-model.md)
- [`ksdft2effmass.io.quantum_espresso.qexsd`](../ksdft2effmass/io/quantum_espresso/qexsd/index.md)
