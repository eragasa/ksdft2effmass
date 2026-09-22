# Separation of harness and workflow

The development component is defined by the [harness architecture](ksdft2effmass/harness/index.md), and the scientific component is defined by the [workflow architecture](ksdft2effmass/workflows/index.md). This page focuses on their authority and lifecycle separation. The cross-cutting [human-decision contract](human-decisions.md) defines two domain-separated systems without a common nominal checkpoint base, shared aggregate, or shared repository.

The normative boundary is:

> The development harness governs changes to the scientific workflow. The
> scientific workflow governs Workflow and Task execution. Development Tasks,
> scientific Workflows, WorkflowRuns, TaskActivations, ResultObjects, and analyses
> have separate authorities and lifecycles. Human-reviewed scientific conclusions
> remain research records rather than workflow state.

```mermaid
flowchart TB
    HUMAN["Human operator"]

    subgraph BOOTSTRAP["Development harness — ksdft2effmass.harness"]
        DTASK["HarnessTask"]
        IMPLEMENT["Software implementation"]
        VERIFY["Software verification"]
        REVIEW["Development review"]

        DTASK --> IMPLEMENT
        IMPLEMENT --> VERIFY
        VERIFY --> REVIEW
    end

    subgraph WORKFLOWS["Scientific workflow — ksdft2effmass.workflows"]
        SERVICE["Scientific service"]
        WORKFLOW["Workflow + Task instances<br/>start-gate policy"]
        RUN["WorkflowRun<br/>generic marking"]
        ACTIVATION["TaskActivation<br/>bound ResultObjects + explicit context"]
        EXEC_AUTH["Exact one-dispatch execution grant"]
        RESULT["New immutable ResultObject"]
        ANALYSIS["Scientific analysis"]
        RESEARCH["Human-reviewed research record"]

        SERVICE --> WORKFLOW
        WORKFLOW --> RUN
        RUN --> ACTIVATION
        EXEC_AUTH --> ACTIVATION
        RESULT --> RUN
        RUN --> ANALYSIS
        ANALYSIS --> RESEARCH
    end

    subgraph CALCULATORS["External calculators"]
        EXECUTOR["Calculator-specific executor"]
        PROGRAM["External executable"]

        EXECUTOR --> PROGRAM
        PROGRAM --> EXECUTOR
    end

    HUMAN --> DTASK
    HUMAN --> SERVICE
    REVIEW --> WORKFLOW
    ACTIVATION --> EXECUTOR
    EXECUTOR --> RESULT
```

`ScientificService` is the scientific entry point. It selects or constructs a `Workflow`, creates a replayable `WorkflowRun`, requires workflow-owned `WorkflowRunReplayer` to return `equal` for the exact loaded or proposed successor revision and explicitly supplied `WorkflowRuntimeBundle`, applies immutable `TaskStartGateSet` policy or direct invocation, binds ResultObjects into discriminated `TaskActivation`, and composes generic selection/firing, workflow-owned generic invocation outcomes, distinct correlated child WorkflowRuns for nested Workflows, the effect-free Workflow adapter, `SimulationDispatchAdapter`, dispatch authorization/reconciliation, Task invocation, `TaskResultIngester`, explicit native-output extraction and parsing, normalization and analysis ActionObjects. Workflow control obtains one exact `authorized` `SimulationExecutionAuthorizationResult` for the unused grant, verified authority snapshot, and proposed immutable dispatch inputs before the preparer builds one atomic unit containing request creation, attempt creation, the request-transition successor, exact grant reservation, and dispatch obligation. The workflow service supplies that complete candidate unit; `WorkflowRunAtomicRepository` validates and binds the same candidate to its serialized bytes before opaque store commit. `SimulationDispatchAdapter` consumes the committed obligation and explicit request/context, the executor boundary independently obtains an exact `authorized` result for the same reserved grant and inputs, and one expected-revision compare-and-swap claim must change `reserved` to `claimed` immediately before invoking the selected calculator process effect; reconciliation returns a confirmed, rejected, or indeterminate `SimulationDispatchOutcome` envelope without inventing observations. Confirmed contains the concrete returned ResultObject; `TaskResultIngester` alone validates/correlates the envelope and admits that object plus exact native-output manifest references into one atomic result-state successor. Calculator-produced files remain in their exact execution workspace or configured external location and are read only by explicit extraction. After that ingress unit commits, QE normalization alone follows admitted calculator-owned `QuantumEspressoOutput` → integration-owned native artifact resolver → integration-owned `QuantumEspressoOutputParser` and/or `QuantumEspressoXsdDocumentParser` → integration-owned `QuantumEspressoObservationAdapter` → workflow-owned `NormalizedObservationSet` → `ScientificAnalyzer`. Workflow services construct candidate successor meaning; the domain repository invokes its bound validator and serializer on the exact candidate and rejects validation or identity-binding failure without an opaque store commit. The scientific service does not mutate repository-derived `HarnessState` or protected `DevelopmentAuthorityLedger`.

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
        CD["Workflow definition"]
        CR["WorkflowRun"]
        EO["External operations"]
        NO["Normalized observations"]
        SA["Scientific analysis"]
        HR["Human-reviewed research conclusion"]

        SI --> CD --> CR --> EO --> NO --> SA --> HR
    end
```

Within the development lifecycle, `DevelopmentTaskSelection` is repository-derived requested/selected state, not authority or permission. Repository sources compile independently of authority. `DevelopmentAuthorityContextResolver` reconstructs and verifies the candidate-independent `DevelopmentAuthorityContext`, and `DevelopmentOperationAuthorizer` returns an affirmative result only for a matching ledger `TaskAuthorization` covering the exact selection and Task revisions, starting and candidate revisions, operation, and permitted paths. Target development operations verify that result's identity bindings without reinterpreting policy; neither a Task, selection, validation result, nor candidate decision can authorize itself.

Human decisions are explicit external inputs to both control planes and their processing is deterministic. Development uses the one `DevelopmentDecision` model inside `HarnessState`; scientific workflow uses `ScientificDecisionRequest`, `ScientificDecisionResolution`, and `ScientificDecisionRecorder` inside the `WorkflowRun` boundary. Scientific decision ingress is a request-identified no-Task transition invoked through an application-owned trusted boundary: the recorder receives the verbatim response with direct source and authority-context identities, constructs the resolution with closed no-Task ingress provenance, uses the effect-free adapter and pure firer, constructs the complete scientific-decision-origin transition/successor, and returns the resolution only after atomic commit. Correction atomically replaces the exact effective token while retaining earlier records and reads as immutable history. No Task, TaskActivation, attempt, standalone response snapshot, or verifier subsystem exists for that transition. Neither decision family authorizes or mutates the other. A pending record blocks only its declared development transition/scope or affected scientific branch. Decision records grant no authority; separate development and execution grants remain required.

The two lifecycles may reference each other's immutable identities when required, but neither stores the other's state. Their domain repositories may compose the same domain-neutral `AtomicRevisionStore` capability, but separate `SQLiteAtomicRevisionStore` instances and separate databases are the default. Distinct parent and nested child WorkflowRuns likewise have separate single-stream revision histories: the parent records exact child correlation and admits only explicit exports from a replay-equal terminal child revision, without claiming cross-run atomicity. Shared implementation does not merge aggregates, authority, physical storage, or transaction boundaries; cross-stream atomicity and co-location require a later explicit decision. Development completion may make a scientific service available; it does not create or advance a `WorkflowRun`. Scientific completion may provide evidence for later development; it does not close a `HarnessTask`.

## Deferred implementation details

- Exact immutable implementation identity referenced by a `WorkflowRun`.
- How a scientific finding creates a new development intent without activating a Task automatically.
- Cross-component access-control rules for restricted artifacts and evidence.
- Whether one application process may host both components or they require separate services.
- Shared observability vocabulary that does not merge state authority.
- Whether later demonstrated need warrants co-location or cross-stream transactions; neither is part of the initial persistence architecture.

## Reconciled authority boundaries

Repository sources are authoritative for the complete normalized `HarnessState`; lossless harness persistence stores the same aggregate through a domain-owned repository. Scientific persistence stores one complete `WorkflowRun` aggregate revision through its separate domain-owned repository. Both may compose the shared opaque single-stream store, whose initial realization uses standard-library SQLite, without sharing domain meaning. Candidate-independent protected development authority remains in a separate `DevelopmentAuthorityLedger`. A `ScientificExecutionAuthoritySnapshot` identifies its trusted source and issuer, trust configuration, content and authentication verification, predecessor/revocation closure, validity and freshness bounds, and resolver version; verification failure yields no usable authorization context. One immutable `ScientificExecutionAuthorityGrant`, verified against an exact `ScientificExecutionAuthoritySnapshot`, covers one exact dispatch and cannot be delegated. `SimulationExecutionAuthorizer` returns a closed `SimulationExecutionAuthorizationResult` for the exact grant, snapshot, Task instance, activation, request, attempt, executor, immutable inputs, destinations, and resource ceiling. The request transaction atomically reserves that grant to one dispatch obligation. Immediately before the effect, one compare-and-swap claim changes the same reservation from `reserved` to `claimed`; only the successful claimant may proceed, and `claimed` is consumed for authorization purposes even if the later external outcome is indeterminate. Every retry or new attempt requires a new grant. Reconciliation retains the original grant, request, attempt, claim, and obligation and never authorizes automatic redispatch. Execution authority does not imply scientific acceptance. Scientific conclusions remain human-reviewed research records and are not inferred from development state, colored-Petri-net selection, analysis, or execution authority.
