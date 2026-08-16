# `ksdft2effmass.integration` package

The prospective `ksdft2effmass.integration` namespace contains concrete
anti-corruption adapters for explicitly selected external systems. Integrations
implement consumer-owned contracts and remain downstream of the packages whose
contracts they consume.

```mermaid
flowchart LR
    app["ksdft2effmass.application"] --> integration["ksdft2effmass.integration"]
    integration --> qe["quantumespresso"]
    qe --> calculators["ksdft2effmass.calculators"]
    qe --> workflows["ksdft2effmass.workflows"]
    qe --> periodic["ksdft2effmass.periodic"]
    qe --> ksdft["ksdft2effmass.ksdft"]
```

- [Quantum ESPRESSO integration](quantumespresso/index.md)

Additional integrations require demonstrated project need and separately
selected contracts. This namespace is not a runtime plugin registry.
