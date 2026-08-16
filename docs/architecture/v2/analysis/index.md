# Scientific analysis architecture

## Responsibility

`ksdft2effmass.analysis` owns deterministic interpretation of normalized observations. It owns algorithms, units, tolerances, numerical policy, findings, and analysis versions. It does not execute calculators or authorize scientific conclusions.

```mermaid
flowchart LR
    observations["NormalizedObservationSet"] --> request["ScientificAnalysisRequest"]
    request --> analyzer["ScientificAnalyzer"]
    analyzer --> analysis["ScientificAnalysis"]
    analysis --> recorder["ScientificDispositionRecorder"]
    authority["Disposition grant + authority snapshot"] --> recorder
    recorder --> disposition["ScientificDisposition + validated recording transaction"]
```

## Pages

- [Analysis and disposition](analysis-and-disposition.md)

`NormalizedObservationSet` is calculator-independent and workflow-owned. Analysis implementations may import workflows, periodic, and Kohn–Sham contracts, but never calculator packages. Disposition creation is not analyzer behavior: the workflow-owned `ScientificDispositionRecorder` validates exact inputs and returns a closed recording result after repository commit.

## Unresolved issues

- Analysis package subdivision by scientific domain.
- Shared numerical-policy representation across analyzers.
- Whether analyzers operate on immutable in-memory records, artifact references, or both.
- Public registration and composition mechanism; mutable registries remain forbidden.
