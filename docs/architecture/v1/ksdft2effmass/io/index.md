# `ksdft2effmass.io` package in v1

The I/O package owns concrete external-format parsing and translation. It does
not own backend-neutral scientific meaning.

```mermaid
flowchart LR
    io["ksdft2effmass.io"] --> qe["io.quantum_espresso"]
    qe --> qexsd["io.quantum_espresso.qexsd"]
    qexsd --> periodic["periodic"]
    qexsd --> ksdft["ksdft and ksdft.pw"]
    qexsd --> provenance["provenance"]
```

- [Quantum ESPRESSO integration](quantum_espresso/index.md)
