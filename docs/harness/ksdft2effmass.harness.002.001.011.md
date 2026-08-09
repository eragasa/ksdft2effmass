---
document_id: ksdft2effmass.harness.002.001.011
task_id: harness.simplification.docs-json.task-model-contract
parent: ksdft2effmass.harness.002.001.000
status: proposed-awaiting-renewed-human-review
sphinx: excluded
---

# Human review: HarnessTask model-contract stage

> **Proposed Stage 1; inactive.** This page reviews only the contract-freeze
> stage. It does not activate implementation, replace Markdown source authority,
> create a migration packet, migrate a file, define selection state, or authorize
> Stage 2.

## Objective

Complete current-revision source-span mappings for all six selected docs/JSON
Task files before finalizing any `HarnessTask` field. Derive one coherent proposed
field, wire, documentation-content, explicit-renderer-input, comparison,
review-packet, public-API, and software-verification contract, then return that
frozen contract for explicit human acceptance.

## Inputs

- the six exact source Task files listed in
  [harness.002.001.010](ksdft2effmass.harness.002.001.010.md);
- accepted attempt-1 documentation/control inventories and mappings;
- current exact source identities and bytes;
- the Task-graph and separate-selection-state architecture decision;
- the per-file human-mediation decision; and
- existing `ArtifactIdentity`, human-review, projection, compatibility-adapter,
  and Task-inspection contracts.

## Required output contract

Stage 1 must return, without implementation:

1. complete source-span coverage for all six files;
2. one exact proposed `HarnessTask` field and invariant table;
3. one canonical versioned JSON wire-field table;
4. strict serializer and deserializer behavior;
5. Task-graph validation rules;
6. explicit `HarnessTaskDocumentationContent` ownership of documentation-owned
   narrative and opaque bytes;
7. explicit `HarnessTaskProjectionProfile` configuration and template inputs;
8. renderer and comparator contracts;
9. comparison finding and unmapped-span representation;
10. immutable migration packet and exact file-disposition contracts;
11. reuse decisions for existing human-review and identity objects;
12. mixed Markdown/JSON `TaskRecordAdapter` and `TaskStateInspector` obligations;
13. proposed public imports, schemas, fixtures, tests, and maintained docs; and
14. one frozen-contract human-review packet.

The full proposed class inventory, explicit rendering equation, overview diagram,
and focused diagram for every proposed class are maintained in
[harness.002.001.010](ksdft2effmass.harness.002.001.010.md).

## Source authority

Markdown remains source authority throughout Stage 1. Inventories, mappings,
schema tables, diagrams, and candidate JSON are review aids only. No Task JSON
replaces a source file, no maintained review document is generated over source,
and no per-file migration packet is prepared.

Every selected byte belongs to exactly one reviewed span disposition: canonical
Task information, documentation-owned content, historical evidence, or proposed
removal. Proposed removal remains human-owned and does not remove bytes in Stage
1.

## Explicit renderer boundary

The accepted proposal must define:

```text
HarnessTask
+ HarnessTaskDocumentationContent
+ HarnessTaskProjectionProfile
→ HarnessTaskDocumentationRenderer
→ HarnessTaskDocumentation
```

All bytes and configuration are explicit. Filesystem discovery, current working
directory, repository-root discovery, hidden templates, and unrecorded parser
state are prohibited.

## Review and completion

One independent review is completed. Every material finding receives an explicit
disposition, every correction receives deterministic verification, and no
material finding remains unresolved. The review result itself is retained
truthfully and is not rewritten after correction.

Stage 1 completes only after the human explicitly accepts the frozen field and
rendering contract. Stage 2 remains blocked until that acceptance is durable.

## Exclusions

Stage 1 performs no public implementation, schema or fixture creation, tests,
source replacement, generated-document cutover, file migration, selection-state
implementation, chain cutover or deletion, dependency change, SQLite, telemetry,
scientific work, publication, external execution, protected work, release action,
or automatic successor activation.

## Human review question

Should `harness.simplification.docs-json.task-model-contract` be activated with
this exact contract-only scope and return for another explicit human decision
before implementation or migration?

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [HarnessTask contract and serial migration](ksdft2effmass.harness.002.001.010.md)
