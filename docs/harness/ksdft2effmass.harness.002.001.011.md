---
document_id: ksdft2effmass.harness.002.001.011
task_id: harness.simplification.docs-json.task-model-contract
parent: ksdft2effmass.harness.002.001.000
status: frozen-contract-awaiting-human-acceptance
sphinx: excluded
---

# Human review: HarnessTask model-contract stage

> **Stage 1 is active and its corrected frozen contract awaits human acceptance.**
> This page does not activate implementation, replace Markdown source authority,
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
10. an immutable runtime-only `HarnessTaskMigrationReviewPacketRequest` contract
    containing every explicit packet-preparation input, intrinsic invariants, and
    no constructor-owned cross-object validation;
11. a stateless `HarnessTaskMigrationReviewPacketPreparer` contract with the
    exact request-to-packet action boundary, complete cross-object validation,
    deterministic construction, and explicit side-effect exclusions;
12. immutable migration packet and exact file-disposition contracts that retain
    generic decision ownership in `HumanReviewDecisionRecorder`;
13. reuse decisions for existing human-review and identity objects;
14. mixed Markdown/JSON `TaskRecordAdapter` and `TaskStateInspector` obligations;
15. exact public-interface accounting for 19 proposed interfaces and exactly 20
    Mermaid class diagrams;
16. proposed public imports, schemas, fixtures, software-verification
    obligations, and maintained docs, without adding request serialization
    unless a wire requirement is separately justified; and
17. one frozen-contract human-review packet.

The full proposed class inventory, explicit rendering equation, public-interface
accounting, verification obligations, overview diagram, and focused diagram for
every proposed class are maintained in
[harness.002.001.010](ksdft2effmass.harness.002.001.010.md).

## Prepared review package

- [Immutable six-source inventory](../../.pi/evidence/docs-json/task-model-contract/source-inventory.json)
- [Complete 118-span mapping set](../../.pi/evidence/docs-json/task-model-contract/source-mappings.json)
- [Frozen 19-interface contract](../../.pi/evidence/docs-json/task-model-contract/harness-task-contract.md)
- [Human-directed documentation progression correction](../../.pi/evidence/docs-json/task-model-contract/documentation-destination-correction.md)
- [Deterministic validation and bounded limitation](../../.pi/evidence/docs-json/task-model-contract/validation.md)

The inventory binds six Git blobs and 20,074 bytes at revision
`dd50c74513f6c51e2a1c823a60b3111738082b3c`. The mapping set covers every byte
with contiguous, ordered, nonoverlapping half-open spans. It proposes these
Stage-2 documentation destinations without creating them:

| Source | Proposed maintained `docs/` target |
|---|---|
| `.pi/tasks/harness.simplification.docs-json.md` | `docs/harness/ksdft2effmass.harness.002.002.000.md` |
| `.pi/tasks/harness.simplification.docs-json.publication.md` | `docs/harness/ksdft2effmass.harness.002.002.001.md` |
| `.pi/tasks/harness.simplification.docs-json.publication.triage.md` | `docs/harness/ksdft2effmass.harness.002.002.002.md` |
| `.pi/tasks/harness.simplification.docs-json.publication.hierarchy.md` | `docs/harness/ksdft2effmass.harness.002.002.003.md` |
| `.pi/tasks/harness.simplification.docs-json.authority-catalog.md` | `docs/harness/ksdft2effmass.harness.002.002.004.md` |
| `.pi/tasks/harness.simplification.docs-json.documentation-correction.md` | `docs/harness/ksdft2effmass.harness.002.002.005.md` |

The human replaced the earlier `002.001.012` through `002.001.017` proposal with
this coherent `002.002.000` through `002.002.005` progression. These corrected
targets remain proposed until the contract is accepted. Stage 2 still requires
one immutable packet and one explicit human disposition per file.

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

The retained [independent review](../../.pi/evidence/docs-json/task-model-contract/integration-review.md)
failed with seven material findings. The one permitted
[correction pass](../../.pi/evidence/docs-json/task-model-contract/review-correction.md)
corrected and deterministically verified all seven: project-local ownership,
three documentation-byte dispositions, packet identity, disposition compatibility,
resource/wire integration, graph lifecycle policy, and six-record compatibility.
The original failed result remains unchanged, no material contract finding
remains unresolved, and no repeated review was performed.

The existing version-1 projection validator reports
`TASK_RENDER_EXPECTED_DRIFT` and `TASK_RENDER_LIVE_DRIFT` because Stage-1
activation changed the chain-owned active Task while the completed pilot's
non-authoritative generated page and expected fixture retain the earlier null
value. Stage 1 excludes generated-page and fixture synchronization. Option A asks
the human to accept this bounded limitation for later separately authorized
synchronization; the stale page is not authority.

Stage 1 completes only after the human explicitly accepts the frozen field and
rendering contract. Stage 2 remains blocked until that acceptance is durable.

## Exclusions

Stage 1 performs no public implementation, schema or fixture creation, tests,
source replacement, generated-document cutover, file migration, selection-state
implementation, chain cutover or deletion, dependency change, SQLite, telemetry,
scientific work, publication, external execution, protected work, release action,
or automatic successor activation.

## Human review question

After independent review and disposition of its findings, should the frozen
19-interface contract, complete six-file mappings, and proposed documentation
destinations be accepted for later Stage-2 implementation? Acceptance will not
activate Stage 2 or accept any individual migration packet.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [HarnessTask contract and serial migration](ksdft2effmass.harness.002.001.010.md)
