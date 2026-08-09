---
document_id: ksdft2effmass.harness.002.001.012
task_id: harness.simplification.docs-json.task-implementation-hardening
parent: ksdft2effmass.harness.002.001.000
status: active-implementation-hardening
sphinx: excluded
---

# Human review: HarnessTask implementation and hardening

> **Stage 2A is active and not yet implementation-accepted.** The activation
> checkpoint authorized implementation and hardening only. This page does not
> accept the resulting implementation, prepare a real migration packet, migrate
> a source file, activate Stage 2B, or modify the accepted Stage-1 contract.

## Purpose

Implement and harden the accepted Stage-1 contract as project-local public
software while all six Markdown Tasks remain authoritative and byte-unchanged.
Stage 2A separates authorization to implement from later human acceptance of the
resulting implementation.

## Accepted contract input

- [Frozen HarnessTask contract](../../.pi/evidence/docs-json/task-model-contract/harness-task-contract.md)
- [Final contract clarification](../../.pi/evidence/docs-json/task-model-contract/final-contract-clarification.md)
- [Human-accepted Stage-1 checkpoint](../../.pi/checkpoints/harness.simplification.docs-json.task-model-contract.clarified-final-acceptance.json)
- [Six-source inventory](../../.pi/evidence/docs-json/task-model-contract/source-inventory.json)
- [Complete mappings](../../.pi/evidence/docs-json/task-model-contract/source-mappings.json)

Stage 2A cannot silently change accepted fields, signatures, ownership boundaries,
wire behavior, documentation destinations, mapping semantics, or review behavior.
A material required change stops and returns for explicit contract review.

## Authorized implementation scope

Stage 2A implements:

- the 19 project-local public interfaces and 16-field schema-version-2
  `HarnessTask`;
- project-local schema, fixtures, profile, resource-manifest relationships, and
  canonical serializer/deserializer behavior;
- `LocalValidationResult` graph diagnostics, including exact `PIHL.TASK.*` codes
  and precedence;
- authoritative-template parsing, explicit rendering, exact byte-structural
  comparison, packet preparation, and migration-disposition behavior;
- accepted `ResourcePath` rejection coverage and focused hardening tests;
- mixed version-1 JSON, version-2 JSON, and Markdown `TaskRecordAdapter` and
  `TaskStateInspector` compatibility; and
- focused tests and maintained public documentation.

The implementation may use one representative illustrative or synthetic example
with a manually supplied `HarnessTask`, canonical JSON, rendered Markdown, and exact
source comparison. It must not describe that example as Markdown-to-JSON extraction
or use it as a real file-migration packet or modification of any selected source.

## Independent review

One independent review is completed after implementation. Every material finding
receives an explicit disposition and every correction receives deterministic
verification. The original review result remains unchanged; no repeated-review
loop is authorized.

## Concise implementation-acceptance packet

Stage 2A must stop at a human checkpoint with one concise packet containing:

1. exact production files added or changed;
2. final public API table;
3. every difference from the accepted Stage-1 contract;
4. one representative manually supplied `HarnessTask` → canonical JSON and
   `HarnessTask` + documentation content + projection profile → rendered Markdown
   example, explicitly labeled as not demonstrating Markdown-to-JSON extraction;
5. exact source/rendered diff for that example;
6. focused test and validation results;
7. independent-review findings and dispositions;
8. known limitations;
9. confirmation that all six Markdown Tasks remain authoritative and unchanged;
10. proposed Stage-2B activation boundary.

The packet links to detailed evidence but does not require reading mappings,
command transcripts, or every test to understand the acceptance decision.
Human implementation acceptance cannot be inferred from tests or review.

## Exclusions

Stage 2A creates no real migration packet and migrates no source. It does not
activate Stage 2B, repair the accepted legacy projection drift without separate
authority, implement selection state, cut over the chain, add dependencies,
change lockfiles, or perform SQLite, telemetry, scientific, publication,
external, protected, release, or unrelated work.

## Activation question

Should Stage 2A be activated exactly within this implementation-only boundary?

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Accepted HarnessTask model contract](ksdft2effmass.harness.002.001.011.md)
- **Next:** [Serial six-file migration](ksdft2effmass.harness.002.001.013.md)
