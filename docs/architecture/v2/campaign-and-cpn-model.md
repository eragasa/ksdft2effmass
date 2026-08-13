# Campaign and CPN model

## Campaign definition

A `Campaign` is the calculator-independent definition of a scientific workflow.
It owns:

- campaign identity;
- `CpnDefinition`;
- initial `CpnMarking`; and
- references to immutable `Simulation` objects.

The CPN is the campaign dependency and lifecycle model. No parallel campaign
DAG, shell-loop language, prerequisite engine, or hidden scheduler state is
permitted.

## CampaignRun

`CampaignRun` is one immutable represented execution state. It owns:

- campaign identity;
- current `CpnMarking`;
- correlated `SimulationExecutionResult` references;
- run and attempt identities; and
- artifact-lineage references.

A state transition returns a new `CampaignRun`. Persistence is independent of
`HarnessTask` and `DevelopmentTaskSelection`.

## CPN semantics

`CpnDefinition` represents colors, places, transitions, arcs, input and output
inscriptions, token patterns, and pure guards. `CpnMarking` is a multiset of
colored tokens by place.

A transition is enabled only when input multisets satisfy inscriptions and its
pure guard accepts the immutable binding. Firing consumes and reads tokens as
declared, produces output tokens deterministically, and returns the successor
marking plus structured findings.

Guards perform no external I/O, calculator execution, artifact transfer,
dynamic capability probing, or scientific analysis.

## Simulation tokens

Campaign colors may represent:

- simulation references;
- authorization;
- execution requests;
- in-progress attempts;
- execution results;
- artifact availability;
- scientific-analysis readiness;
- required success or failure; and
- campaign terminal state.

They contain generic identities and statuses, not calculator namelist fields,
cutoffs, k-point coordinates, executable paths, or native output structures.

## External action protocol

```text
authorized CPN marking
→ fire deterministic request transition
→ resolve Simulation
→ SimulationExecutor external boundary
→ SimulationExecutionResult
→ introduce correlated result token
→ fire success or failure transition
→ successor CampaignRun
```

The same executor contract serves direct and CPN-controlled use. CPN control may
add ordering, authorization, synchronization, failure propagation, stop-on-first-
required-failure, retry, recovery, and terminal-state semantics; it must not
alter calculator behavior.

## Terminal and failure semantics

Attempt, branch, and campaign scopes are explicit. A failed attempt remains
retained even if a separately authorized retry creates a new attempt. Required
failure may inhibit further dispatch and enable campaign failure. Campaign
completion requires the declared accepted terminal marking, not merely an empty
queue or a successful process.

## Portability

`projectkoios.workflows` is the target owner for the generic CPN and campaign
contracts. Ksdft2effmass campaign definitions remain project-specific and may use
generic contracts without making the generic package depend on semiconductor or
Quantum ESPRESSO semantics.
