# Scientific workflow persistence

## Purpose

Workflow persistence stores `ScientificWorkflow`, `ScientificWorkflowRun`, simulation correlations, artifact lineage, analyses, and dispositions independently of development state. It owns revision consistency and recovery, not workflow meaning or authority.

## Aggregate boundary

The authoritative aggregate is defined by [ScientificWorkflowRun](scientific/scientific-workflow-run.md). Persistence stores its immutable revisions and referenced records.

| Object | Purpose |
|---|---|
| `ScientificWorkflowRunIdentity` | Stable logical run identity |
| `ScientificWorkflowRunRevision` | Immutable revision and predecessor identity |
| `ScientificWorkflowRunSnapshot` | Consistent selected run revision |
| `ScientificWorkflowRunTransaction` | Expected revision plus complete appended records |
| `ScientificWorkflowRunPersistenceConflict` | Expected-versus-observed revision mismatch |
| `ScientificWorkflowRunWriteResult` | Created revision and resulting snapshot identity |
| `ScientificWorkflowRunMigrationResult` | Versioned migration identities and findings |

## Repository boundary

```text
load explicit run and revision → ScientificWorkflowRunSnapshot
commit validated append transaction → ScientificWorkflowRunWriteResult
```

`ScientificWorkflowRunRepository` does not enable or fire transitions, execute simulations, interpret observations, resolve conflicts silently, or create dispositions.

## Transaction boundaries

The following operations have explicit atomic persistence boundaries:

- reserve an attempt and record its request identity;
- accept one correlated result for one request;
- append artifact publication identities;
- record a CPN transition and successor marking;
- append an analysis reference; and
- append a separately authorized disposition reference.

An external calculator process is not enclosed in a database transaction. The run persists requested/in-progress state before dispatch and correlates the returned result idempotently afterward.

## Integrity

Integrity verification covers run and revision identities, predecessor closure, marking/transition consistency, request/result uniqueness, artifact references, analysis and disposition references, schema versions, and implementation identities required for replay.

## Unresolved issues

- Concrete repository and storage technology.
- Optimistic versus serialized writer coordination.
- Crash recovery between external process completion and result persistence.
- Idempotency-key representation and retention period.
- Transaction grouping for artifact publication and result correlation.
- Migration support policy for persisted CPN expressions and token payloads.
