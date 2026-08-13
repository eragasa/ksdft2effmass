# CampaignRun object model

## Aggregate

`CampaignRun` is the immutable aggregate for one represented campaign execution. It records attempts and state transitions without embedding runtime engines or mutable calculator clients.

```mermaid
classDiagram
    class CampaignRun
    class CampaignDefinitionReference
    class CampaignRunParentReference
    class CampaignAttempt
    class CampaignMarkingRecord
    class CampaignTransitionRecord
    class SimulationCorrelation
    class CampaignFailureRecord
    class ScientificAnalysisReference
    class ScientificDispositionReference

    CampaignRun --> CampaignDefinitionReference : executes
    CampaignRun --> CampaignRunParentReference : optionally derives from
    CampaignRun *-- CampaignAttempt : contains
    CampaignRun *-- CampaignMarkingRecord : records
    CampaignRun *-- CampaignTransitionRecord : records
    CampaignAttempt *-- SimulationCorrelation : performs
    CampaignAttempt *-- CampaignFailureRecord : may report
    CampaignRun --> ScientificAnalysisReference : analyzed by
    CampaignRun --> ScientificDispositionReference : disposed by
```

## Component objects

| Object | Responsibility |
|---|---|
| `CampaignDefinitionReference` | Exact campaign, CPN definition, and schema versions |
| `CampaignRunParentReference` | Optional parent-run and derivation relationship |
| `CampaignAttempt` | One bounded attempt with identity, authority, and status |
| `CampaignMarkingRecord` | Exact immutable CPN marking at one run revision |
| `CampaignTransitionRecord` | Fired transition, binding, predecessor, successor, and findings |
| `SimulationCorrelation` | Request, simulation, executor, result, and artifact identities |
| `CampaignFailureRecord` | Phase-specific failure associated with an attempt or transition |
| `ScientificAnalysisReference` | Reference to separately persisted deterministic analysis |
| `ScientificDispositionReference` | Reference to separately authorized disposition |

## Revision semantics

A state transition returns a new `CampaignRun` revision. Attempts, markings, transition records, correlations, failures, analyses, and dispositions are append-only within the represented history. Retry creates a new attempt and does not overwrite its predecessor.

Analysis and disposition are referenced rather than embedded as mutable execution fields. Execution records observations, analysis interprets them, and disposition records an authorized conclusion.

## Runtime exclusions

Persistence excludes runtime engines, arbitrary Python objects, closures, credentials, process handles, open files, scheduler clients, and calculator clients. Runtime behavior is reconstructed from versioned definitions, configuration, and implementation identities.

## Unresolved issues

- Snapshot-only versus snapshot-plus-transition-log canonical representation.
- Exact token payload wire format and canonical ordering.
- Whether a run may reference multiple dispositions for different intended uses.
- Parent-child semantics for retries, branches, and campaign derivation.
- Event compaction and long-run history retention.
