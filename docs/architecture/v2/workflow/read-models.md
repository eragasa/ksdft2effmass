# Scientific workflow read models

## Purpose

Scientific read models are deterministic derived views of workflow persistence. They support inspection and analysis without replacing `CampaignRun` authority.

## Read models

| Read model | Content |
|---|---|
| `CampaignRunSummary` | Run identity, campaign, revision, status, and terminality |
| `CampaignMarkingHistory` | Ordered marking and transition identities |
| `SimulationCorrelationView` | Attempt, request, simulation, result, and executor identities |
| `ArtifactLineageView` | Producer, consumer, parent, role, and content identities |
| `CampaignFailureView` | Failures grouped by phase, attempt, and transition |
| `ScientificAnalysisView` | Analysis identities, analyzers, inputs, findings, and versions |
| `ScientificDispositionView` | Intended use, cited analyses, authority, and conclusion |

## Projection rules

A read model declares its source run revision, view schema, generating action, and content identity. Equivalent source state and view version produce equivalent semantic content.

Read models cannot:

- advance a CPN marking;
- authorize or dispatch a calculator;
- accept a result;
- create analysis or disposition;
- mutate artifact lineage; or
- close development work.

Dashboards and visualizations consume read models. Their presentation is not scientific evidence or authority.

## Unresolved issues

- Which read models are persisted versus generated on demand.
- Query and pagination contracts for large run histories.
- Canonical ordering for lineage and failure views.
- Whether read models have stable public wire formats.
- Retention and access policy for views referencing restricted artifacts.
