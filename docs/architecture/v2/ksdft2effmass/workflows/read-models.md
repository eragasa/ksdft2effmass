# Scientific workflow read models

## Purpose

Scientific read models are deterministic derived views of workflow persistence. They support inspection and analysis without replacing `WorkflowRun` authority.

## Read models

| Read model | Content |
|---|---|
| `WorkflowRunSummary` | Workflow/run identity, revision, status, and terminality |
| `WorkflowMarkingHistory` | Initial/current marking identities and canonical ordered transition identities |
| `TaskDispatchCorrelationView` | Task instance, TaskActivation, attempt, request, executor, dispatch-envelope, and returned ResultObject identities |
| `ArtifactLineageView` | Producer, consumer, parent, role, and content identities |
| `WorkflowFailureView` | Failures grouped by phase, attempt, and transition |
| `ScientificAnalysisView` | Analysis identities, analyzers, inputs, findings, and versions |

## Projection rules

A read model declares its source run revision, view schema, generating action, and content identity. Equivalent source state and view version produce equivalent semantic content.

Read models cannot:

- advance a colored-Petri-net marking;
- authorize or dispatch a calculator;
- accept a result;
- create analysis or infer a scientific conclusion;
- mutate artifact lineage; or
- close development work.

Dashboards and visualizations consume read models. Their presentation is not scientific evidence or authority.

## Unresolved issues

- Which read models are persisted versus generated on demand.
- Query and pagination contracts for large run histories.
- Canonical ordering for lineage and failure views.
- Whether read models have stable public wire formats.
- Retention and access policy for views referencing restricted artifacts.
