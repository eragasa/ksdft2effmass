# Separation of harness and workflow in v1

## Implemented boundary

V1 has an operational development harness and an implemented CPN workflow foundation, but scientific calculations are coordinated by development Tasks and direct runners rather than persisted CPN runs.

```mermaid
flowchart TB
    subgraph harness["Operational development harness"]
        task["HarnessTask"] --> preflight["Calculation preflight"]
        preflight --> authority["Human execution authority"]
        authority --> runner["Direct runner"]
        observation["Execution observations"] --> review["Task-specific review"]
        review --> taskstate["HarnessTask transition"]
    end

    subgraph workflow["Implemented workflow foundation"]
        definition["CpnNetDefinition"]
        marking["CpnMarking"]
        enablement["TransitionEnabler"]
        firing["TransitionFirer"]
        definition --> enablement
        marking --> enablement
        enablement --> firing
    end

    runner --> calculator["External calculator"]
    calculator --> observation
    workflow -. not wired to scientific execution .-> runner
```

## Lifecycle coupling

```mermaid
flowchart LR
    select["Select calculation"] --> active["HarnessTask active"]
    active --> prepare["Scientific preparation"]
    prepare --> execute["Protected execution"]
    execute --> observe["Process and artifacts"]
    observe --> analyze["Task-specific analysis"]
    analyze --> transition["HarnessTask status transition"]
```

The same development lifecycle carries software scope, protected execution preparation, and scientific review language. V1 has no independent `CampaignRun` state between execution authority and calculator dispatch.

## Cross-component references

The CPN package can represent ordering, guards, token flow, outcomes, retries, and terminality. It contains no external executor, scientific payload, persistence repository, or concrete campaign. Consequently, V1 direct scientific records do not reference an authoritative CPN marking.

## Authority consequence

Development completion does not scientifically validate a result. Calculator success does not close a Task automatically. Human execution authority and human acceptance remain explicit even though their records are distributed across Task, chain, calculation, and documentation surfaces.
