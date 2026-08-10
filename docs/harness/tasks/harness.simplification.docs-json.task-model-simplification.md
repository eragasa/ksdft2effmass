<!-- Generated from SQLite control state; do not edit. -->
# Simplify the durable HarnessTask architecture

[Task index](index.md) · [Previous](./harness.simplification.docs-json.task-model-contract.md) · [Next](./harness.simplification.evidence.naming.md)

## Status

`completed`

## Objective

Retain the minimum durable HarnessTask model and compatibility boundaries while removing the unaccepted Stage-2A migration framework.

## Parent and prerequisites

- Parent: `harness.simplification.docs-json`
- Depends on: `harness.simplification.docs-json.task-model-contract`

## Authority references

- .pi/checkpoints/harness.simplification.docs-json.task-implementation-hardening.human-review-boundary-acceptance.json
- AGENTS.md
- harness/archive/task-control-v1/intake/harness.simplification.docs-json.task-model-simplification.intake.md

## Authorized scope

- Retain HarnessTask, HarnessTaskSerializer, HarnessTaskDeserializer, HarnessTaskGraphValidator, version-2 schema and focused fixtures, mixed Markdown/version-1/version-2 TaskRecordAdapter behavior, and TaskStateInspector compatibility.
- Remove the unaccepted migration-framework public interfaces, commands, project-local skill and descriptor routing, projection profile, packet fixtures, disposition machinery, source-span comparison tests, and documentation that presents them as current architecture.
- Resolve Stage 2A as deferred without architecture acceptance, supersede its implementation Task, keep Stage 2B deferred inactive, preserve historical evidence, and keep all six authoritative Markdown Task files byte-identical.

## Completion criteria

- Only the four retained Task-model classes are publicly defined and exported; retained focused tests and validation pass.
- The migration commands, skill routes, projection profile, packet fixtures, and unaccepted interface tests are absent.
- The six Markdown Task identities are unchanged, Stage 2B is inactive, automatic successor activation is false, dependencies and lockfile are unchanged, and the simplification is committed and pushed to dev.

## Exclusions

- Do not migrate a real Task, generate Markdown from JSON, activate Stage 2B or another successor, add dependencies, change the lockfile, or perform protected scientific, release, or publication execution.

## Historical source

No archived source.
