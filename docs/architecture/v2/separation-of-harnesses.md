# Separation of harnesses

The normative boundary is:

> The development harness governs changes to the scientific harness. The
> scientific harness governs scientific Campaigns. Development Tasks,
> Campaigns, CampaignRuns, simulations, execution results, analyses, and
> scientific dispositions have separate authorities and lifecycles.

```mermaid
flowchart TB
    HUMAN["Human operator"]

    subgraph BOOTSTRAP["Development harness — ProjectKoios Bootstrap"]
        DTASK["HarnessTask"]
        IMPLEMENT["Software implementation"]
        VERIFY["Software verification"]
        REVIEW["Development review"]

        DTASK --> IMPLEMENT
        IMPLEMENT --> VERIFY
        VERIFY --> REVIEW
    end

    subgraph WORKFLOWS["Scientific execution harness — ProjectKoios Workflows"]
        SERVICE["Scientific service"]
        CAMPAIGN["Campaign<br/>CPN definition"]
        RUN["CampaignRun<br/>CPN marking"]
        REQUEST["Simulation request"]
        RESULT["Simulation execution result"]
        ANALYSIS["Scientific analysis"]
        DISPOSITION["Scientific disposition"]

        SERVICE --> CAMPAIGN
        CAMPAIGN --> RUN
        RUN --> REQUEST
        RESULT --> RUN
        RUN --> ANALYSIS
        ANALYSIS --> DISPOSITION
    end

    subgraph CALCULATORS["External calculators"]
        EXECUTOR["Calculator-specific executor"]
        PROGRAM["External executable"]

        EXECUTOR --> PROGRAM
        PROGRAM --> EXECUTOR
    end

    HUMAN --> DTASK
    HUMAN --> SERVICE
    REVIEW --> CAMPAIGN
    REQUEST --> EXECUTOR
    EXECUTOR --> RESULT
```

`ScientificService` is the authorized scientific entry point. It selects or
constructs a `Campaign`, creates a `CampaignRun`, resolves requested
`Simulation` objects, delegates bounded effects through `SimulationExecutor`,
and routes returned `SimulationExecutionResult` objects back into the CPN. It
does not mutate development state.

```mermaid
flowchart LR
    subgraph DEVELOPMENT["Development lifecycle"]
        DP["Planned"]
        DA["Active"]
        DI["Implementation"]
        DV["Software verification"]
        DR["Review"]
        DC["Completed"]

        DP --> DA --> DI --> DV --> DR --> DC
    end

    subgraph SCIENTIFIC["Scientific lifecycle"]
        SI["Scientific intent"]
        CD["Campaign definition"]
        CR["CampaignRun"]
        EO["External operations"]
        NO["Normalized observations"]
        SA["Scientific analysis"]
        SD["Scientific disposition"]

        SI --> CD --> CR --> EO --> NO --> SA --> SD
    end
```

The two lifecycles may reference each other's immutable identities when required,
but neither stores the other's state. Development completion may make a
scientific service available; it does not create or advance a `CampaignRun`.
Scientific completion may provide evidence for later development; it does not
close a `HarnessTask`.
