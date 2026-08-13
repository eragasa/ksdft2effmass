# Architecture v2

Architecture v2 is the normative target architecture for deterministic scientific
operations and their supporting software-development lifecycle.

The governing model is:

```text
Development harness
    ProjectKoios Bootstrap model
    governs software development

Scientific execution harness
    ProjectKoios Workflows model
    governs deterministic scientific operations

External calculators
    perform bounded numerical side effects

Scientific analyzers
    deterministically interpret normalized observations
```

The development harness governs changes to the scientific harness. The
scientific harness governs scientific `Campaign` objects. `HarnessTask`,
`DevelopmentTaskSelection`, `Campaign`, `CampaignRun`, `Simulation`,
`SimulationExecutionResult`, `ScientificAnalysis`, and `ScientificDisposition`
have separate authorities and lifecycles.

## Normative pages

- [Principles](principles.md)
- [Separation of harnesses](separation-of-harnesses.md)
- [Development harness](development-harness.md)
- [Scientific execution harness](scientific-execution-harness.md)
- [Simulation model](simulation-model.md)
- [Campaign and CPN model](campaign-and-cpn-model.md)
- [Artifact and provenance model](artifact-and-provenance-model.md)
- [Control plane](control-plane.md)
- [Compiler architecture](compiler-architecture.md)
- [Persistence and projections](persistence-and-projections.md)
- [Repository layout](repository-layout.md)

These pages define target responsibilities. Exact stable import paths remain
open until tutorial-driven implementation demonstrates a cohesive public
contract. Cross-version status and cutover conditions are intentionally excluded
and are maintained only in the [migration crosswalk](../migration-v1-to-v2.md).
