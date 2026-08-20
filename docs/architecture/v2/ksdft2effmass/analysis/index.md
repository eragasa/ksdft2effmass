# `ksdft2effmass.analysis` package

## Responsibility

`ksdft2effmass.analysis` owns deterministic interpretation of normalized observations. It owns algorithms, units, tolerances, numerical policy, findings, analysis versions, and explicit claim boundaries. It does not execute calculators or decide scientific acceptance.

```mermaid
flowchart LR
    observations["NormalizedObservationSet"] --> request["ScientificAnalysisRequest"]
    request --> analyzer["ScientificAnalyzer"]
    analyzer --> analysis["ScientificAnalysis<br/>findings + limitations + claim boundary"]
```

## Pages

- [Scientific analysis](analysis.md)

`NormalizedObservationSet` is calculator-independent and workflow-owned. Analysis implementations may import workflows, periodic, Kohn–Sham, and represented-operator contracts, but never calculator packages. The retained `ksdft2effmass.operators` owner supplies records and narrowly fixed-representation operations; analysis owns alignment selection, model fitting, continuum reduction, structured learning, evidence-bearing findings, and other higher-level scientific policy without redefining that inward kernel. Human-reviewed conclusions remain in research records citing exact analysis identities and provenance; Architecture v2 defines no software disposition or acceptance subsystem.

## Deferred implementation details

- Analysis package subdivision by scientific domain.
- Shared numerical-policy representation across analyzers.
- Whether analyzers operate on immutable in-memory records, artifact references, or both.
- Public registration and composition mechanism; mutable registries remain forbidden.
