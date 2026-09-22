# `ksdft2effmass.workflows` namespace in v1

Architecture v1 implements calculator-independent Colored Petri Net semantics
under [`ksdft2effmass.workflows.cpn`](cpn/index.md). The parent namespace owns no
public `ScientificWorkflow`, `ScientificWorkflowRun`, simulation executor, or
scientific persistence service.

```mermaid
flowchart LR
    workflows["ksdft2effmass.workflows"] --> cpn["workflows.cpn"]
    cpn -. "no calculator import" .-> external["external calculators"]
```

The implemented CPN is a reusable semantic foundation. Accepted v1 calculator
executions used repository-level direct runners rather than CPN dispatch.
