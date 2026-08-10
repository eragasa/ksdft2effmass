<!-- Generated from SQLite control state; do not edit. -->
# Deferred CPN workflow persistence

[Task index](index.md) · [Previous](./cpn-skill-capability-audit.md) · [Next](./deferred-harness-current-phase-history.md)

## Status

`deferred_inactive`: Deferred until artifact, record, model, and comparison contracts are stable and the Task is separately activated.

## Objective

Implement the SNAKES adapter and durable project-owned workflow-marking persistence after the simulation-first contracts stabilize.

## Parent and prerequisites

- Depends on: `P1`
- Depends on: `P2`
- Depends on: `bulk-silicon.records.periodic.extraction`
- Depends on: `bulk-silicon.tight-binding.comparison-reduction`

## Authority references

- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Represent typed token payloads for accepted artifact, record, model, request, result, and failure identities.
- Persist project-owned markings, lineage, correlations, retry history, and terminal failure history.
- Support deterministic restart from persisted project state.

## Completion criteria

- Durable marking round trips are deterministic.
- Typed tokens preserve accepted identities and immutable payloads.
- Retry and restart behavior have focused software-verification evidence.
- Independent review and human acceptance occur when separately activated.

## Exclusions

- This deferred Task does not block the simulation-first path.
- No live-net or arbitrary-object pickle, serialized lambda, credential, open file, process handle, scheduler handle, or mutable client is stored.
- No unverified hierarchical SNAKES API is assumed.
- No work is activated by this Task record.

## Historical source

No archived source.
