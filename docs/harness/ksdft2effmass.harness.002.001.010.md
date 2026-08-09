---
document_id: ksdft2effmass.harness.002.001.010
task_id: harness.simplification.docs-json.task-document-migration
parent: ksdft2effmass.harness.002.001.000
status: frozen-contract-awaiting-human-acceptance
sphinx: excluded
---

# Human review: HarnessTask contract and serial document migration

> **Revised proposal; no Task is active.** This page presents the complete
> two-stage architecture for renewed human review. It does not accept the
> proposed information model, activate either stage, implement a public object,
> prepare a file packet, migrate a file, or authorize selection-state work.

## Why the proposal was divided

The initial proposal combined information-model discovery, public implementation,
six human-mediated migrations, graph validation, and selection-state shadowing.
The human selected Option B at the activation checkpoint and required two
separately authorized stages:

1. `harness.simplification.docs-json.task-model-contract` freezes the complete
   field, wire, rendering-input, mapping, comparison, review-packet, public-API,
   and verification contract. It replaces no source authority and performs no
   implementation or migration.
2. `harness.simplification.docs-json.task-document-migration` remains blocked
   until Stage 1 is completed and explicitly human-accepted. It then implements
   the accepted contract and migrates one file at a time without changing the
   contract.

Candidate selection-state implementation is deferred to a later separately
authorized Task. The current chain remains operational authority throughout both
proposed stages. No chain cutover or deletion is authorized.

## Existing authority-merge inputs

The accepted attempt-1 inventories remain immutable. They established complete
path coverage for their revision but only seven partial mappings, zero fully
mapped paths, and residuals containing all 222 documentation paths and all 23
control paths. The one-Task JSON pilot demonstrated mechanics but did not complete
the parent migration.

Stage 1 creates a new current-revision inventory for exactly these six source
Task documents and completes all six mappings before proposing final
`HarnessTask` fields:

1. `.pi/tasks/harness.simplification.docs-json.md`
2. `.pi/tasks/harness.simplification.docs-json.publication.md`
3. `.pi/tasks/harness.simplification.docs-json.publication.triage.md`
4. `.pi/tasks/harness.simplification.docs-json.publication.hierarchy.md`
5. `.pi/tasks/harness.simplification.docs-json.authority-catalog.md`
6. `.pi/tasks/harness.simplification.docs-json.documentation-correction.md`

No exact `HarnessTask` field list is accepted or implemented before complete
source-span mappings for all six files and renewed human review.

## Explicit rendering boundary

Complete Markdown rendering has only explicit inputs:

```text
HarnessTask
+ HarnessTaskDocumentationContent
+ HarnessTaskProjectionProfile
→ HarnessTaskDocumentationRenderer
→ HarnessTaskDocumentation
```

`HarnessTask` contains canonical Task information established by the mappings.
`HarnessTaskDocumentationContent` contains documentation-owned narrative and
opaque content with exact source identity and bytes.
`HarnessTaskProjectionProfile` contains explicit rendering configuration and
exact template identity or bytes. The renderer may not use filesystem discovery,
the current working directory, repository-root discovery, hidden global
templates, or unrecorded parser state.

Maintained narrative does not move into canonical Task JSON merely to simplify
rendering. LaTeX, Mermaid, code fences, directives, tables, links, and other
opaque project content remain exact documentation-content inputs unless the
human accepts a transformation for the exact file.

## Existing objects reused

| Existing object | Reuse decision |
|---|---|
| `ArtifactIdentity` | Reused for exact SHA-256 identity of source, JSON, documentation-content, and rendered bytes |
| `HumanReviewTarget` | Reused to bind one review identity, revision, paths, evidence class, and contract references |
| `HumanReviewObservation` | Reused for explicit deterministic packet observations |
| `HumanReviewFinding` | Reused for candidate human-review issues |
| `HumanReviewPacket` | Reused as the canonical generic observations/findings/limitations component inside a migration packet |
| `HumanReviewDecision` | Reused to preserve exact human response and generic normalized review disposition |
| `HumanReviewPreparer` | Reused to canonicalize the generic review component |
| `HumanReviewDecisionRecorder` | Reused to record the generic human decision component |
| `ValidationResult` | Reused as the graph-validator structural result |
| `TaskRecordAdapter` | Retained as a temporary mixed Markdown/JSON compatibility adapter; not the canonical model |
| `TaskStateInspector` | Retained as the explicit-input consumer of mixed-format compatibility views; never Task authority |

`HumanReviewPacket` does not bind candidate Task JSON, source mappings,
documentation-content bytes, rendering profile, rendered output, or exact
comparison. `HumanReviewDecision` also lacks the migration-specific closed
file-disposition vocabulary. The proposed migration packet and file disposition
therefore compose the existing human-review objects rather than aliasing or
replacing them.

## Complete proposed information model

| Proposed class | Stereotype | Ownership |
|---|---|---|
| `HarnessTask` | DataObject | Canonical Task information in the frozen 16-field proposal derived from complete six-file mappings |
| `HarnessTaskSerializer` | ActionObject | Canonical versioned JSON from one accepted `HarnessTask` |
| `HarnessTaskDeserializer` | ActionObject | Strict canonical JSON to `HarnessTask` |
| `HarnessTaskGraphValidator` | ActionObject | Parent, prerequisite, identity, and cross-Task compatibility |
| `HarnessTaskDocumentSource` | DataObject | Exact source path, revision or Git identity, bytes, byte count, and `ArtifactIdentity` |
| `HarnessTaskSourceDisposition` | enumeration | Canonical Task field, documentation-owned content, historical evidence, or proposed removal |
| `HarnessTaskSourceMapping` | DataObject | Exact byte span and identity, source identity, disposition, nonempty target-reference tuple, transformation, and rationale |
| `HarnessTaskDocumentationContent` | DataObject | Explicit documentation-owned narrative and opaque bytes plus accepted mappings |
| `HarnessTaskProjectionProfile` | DataObject | Explicit rendering configuration, ordering, and exact template identity or bytes |
| `HarnessTaskDocumentation` | DataObject | Complete rendered Markdown bytes and `ArtifactIdentity` |
| `HarnessTaskDocumentationRenderer` | ActionObject | Pure explicit-input rendering to `HarnessTaskDocumentation` |
| `HarnessTaskDocumentationComparator` | ActionObject | Exact source/rendered comparison and mapping-coverage analysis |
| `HarnessTaskDocumentationComparisonResult` | ResultObject | Status, structured findings, exact differences, and unmapped spans |
| `HarnessTaskMigrationReviewPacketRequest` | immutable DataObject | Complete explicit runtime input boundary for preparing one packet; owns intrinsic type, immutability, tuple, nonempty, and lexical invariants but no cross-object validation |
| `HarnessTaskMigrationReviewPacketPreparer` | stateless ActionObject | Validates all cross-object identities and compatibility in one explicit request, reuses generic human-review behavior where appropriate, and deterministically produces one immutable packet |
| `HarnessTaskMigrationReviewPacket` | ResultObject | Immutable validated result produced by `HarnessTaskMigrationReviewPacketPreparer`; binds the exact request values without interpreting a human response or performing authority-changing work |
| `HarnessTaskMigrationDisposition` | enumeration | Accept file, revise contract or mapping, retain documentation ownership, or defer file |
| `HarnessTaskMigrationFileDisposition` | ResultObject | Exact migration packet, existing `HumanReviewDecision`, and migration-specific disposition |
| `HarnessTaskMigrationFileDispositionRecorder` | ActionObject | Validates packet/decision identity and records one explicit file disposition without persistence or activation |

The complete six-file mappings now derive exact names, types, ordering,
invariants, wire behavior, public imports, resource locations, and verification
obligations for all 19 interfaces. The frozen proposal is
[`harness-task-contract.md`](../../.pi/evidence/docs-json/task-model-contract/harness-task-contract.md).
The immutable source inventory is
[`source-inventory.json`](../../.pi/evidence/docs-json/task-model-contract/source-inventory.json),
and the 118 complete byte-span mappings are
[`source-mappings.json`](../../.pi/evidence/docs-json/task-model-contract/source-mappings.json).
These records do not replace Markdown source authority or create Stage-2 files.

The exact `HarnessTask` field order is:

| Order | Field | Type |
|---:|---|---|
| 1 | `schema_version` | built-in `int`, exactly 2 |
| 2 | `task_id` | `Identifier` |
| 3 | `title` | built-in `str` |
| 4 | `status` | `Identifier` |
| 5 | `status_detail` | built-in `str` or `None` |
| 6 | `parent_task_id` | `Identifier` or `None` |
| 7 | `task_prerequisite_ids` | tuple of `Identifier` |
| 8 | `external_prerequisite_ids` | tuple of `Identifier` |
| 9 | `explicit_activation_required` | built-in `bool` |
| 10 | `objective` | built-in `str` |
| 11 | `authority_reference_paths` | tuple of `ResourcePath` |
| 12 | `authorized_scope` | tuple of built-in `str` |
| 13 | `completion_criteria` | tuple of built-in `str` |
| 14 | `exclusions` | tuple of built-in `str` |
| 15 | `intake_path` | `ResourcePath` |
| 16 | `documentation_path` | `ResourcePath` |

`status_detail` preserves detail previously embedded after the lifecycle token.
`documentation_path` binds the required maintained review document. Child lists,
selection state, active-Task facts, successor state, timestamps, event logs, and
computed completion remain outside `HarnessTask`.

`HarnessTaskMigrationReviewPacketRequest` is runtime-only; the mappings establish
no wire or persistence need for it. Its existence does not expand the
serialized-record set. Its constructor owns only intrinsic type, immutability,
tuple, nonempty, and lexical invariants. Cross-object identity and compatibility
belong to `HarnessTaskMigrationReviewPacketPreparer`.

## Overview class diagram

```mermaid
classDiagram
    class HarnessTask {
        <<DataObject>>
        +schema_version
        +task_id
        +title
        +status
        +status_detail
        +parent_task_id
        +task_prerequisite_ids
        +external_prerequisite_ids
        +explicit_activation_required
        +objective
        +authority_reference_paths
        +authorized_scope
        +completion_criteria
        +exclusions
        +intake_path
        +documentation_path
    }
    class HarnessTaskSerializer {
        <<ActionObject>>
    }
    class HarnessTaskDeserializer {
        <<ActionObject>>
    }
    class HarnessTaskGraphValidator {
        <<ActionObject>>
    }
    class HarnessTaskDocumentSource {
        <<DataObject>>
    }
    class HarnessTaskSourceDisposition {
        <<enumeration>>
    }
    class HarnessTaskSourceMapping {
        <<DataObject>>
    }
    class HarnessTaskDocumentationContent {
        <<DataObject>>
    }
    class HarnessTaskProjectionProfile {
        <<DataObject>>
    }
    class HarnessTaskDocumentation {
        <<DataObject>>
    }
    class HarnessTaskDocumentationRenderer {
        <<ActionObject>>
    }
    class HarnessTaskDocumentationComparator {
        <<ActionObject>>
    }
    class HarnessTaskDocumentationComparisonResult {
        <<ResultObject>>
    }
    class HarnessTaskMigrationReviewPacketRequest {
        <<immutable DataObject>>
    }
    class HarnessTaskMigrationReviewPacketPreparer {
        <<stateless ActionObject>>
    }
    class HarnessTaskMigrationReviewPacket {
        <<ResultObject>>
    }
    class HarnessTaskMigrationDisposition {
        <<enumeration>>
    }
    class HarnessTaskMigrationFileDisposition {
        <<ResultObject>>
    }
    class HarnessTaskMigrationFileDispositionRecorder {
        <<ActionObject>>
    }
    class ArtifactIdentity {
        <<DataObject>>
    }
    class HumanReviewPacket {
        <<ResultObject>>
    }
    class HumanReviewDecision {
        <<ResultObject>>
    }
    class ValidationResult {
        <<ResultObject>>
    }
    class TaskRecordAdapter {
        <<adapter>>
    }
    class TaskStateInspector {
        <<ActionObject>>
    }

    HarnessTaskSerializer ..> HarnessTask : input
    HarnessTaskDeserializer ..> HarnessTask : output
    HarnessTaskGraphValidator ..> HarnessTask : input graph
    HarnessTaskGraphValidator ..> ValidationResult : output
    HarnessTaskDocumentSource *-- ArtifactIdentity : exact bytes
    HarnessTaskSourceMapping --> HarnessTaskSourceDisposition : classifies span
    HarnessTaskDocumentationContent *-- HarnessTaskDocumentSource : source
    HarnessTaskDocumentationContent *-- HarnessTaskSourceMapping : accepted spans
    HarnessTaskDocumentation *-- ArtifactIdentity : rendered bytes
    HarnessTaskDocumentationRenderer ..> HarnessTask : explicit input
    HarnessTaskDocumentationRenderer ..> HarnessTaskDocumentationContent : explicit input
    HarnessTaskDocumentationRenderer ..> HarnessTaskProjectionProfile : explicit input
    HarnessTaskDocumentationRenderer ..> HarnessTaskDocumentation : output
    HarnessTaskDocumentationComparator ..> HarnessTaskDocumentSource : source input
    HarnessTaskDocumentationComparator ..> HarnessTaskDocumentation : rendered input
    HarnessTaskDocumentationComparator ..> HarnessTaskSourceMapping : coverage input
    HarnessTaskDocumentationComparator ..> HarnessTaskDocumentationComparisonResult : output
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentSource : exact source
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskSourceMapping : complete ordered mappings
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTask : candidate
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentationContent : explicit narrative
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskProjectionProfile : explicit profile
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentation : rendered output
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentationComparisonResult : comparison
    HarnessTaskMigrationReviewPacketRequest *-- HumanReviewPacket : generic review component
    HarnessTaskMigrationReviewPacketPreparer ..> HarnessTaskMigrationReviewPacketRequest : explicit input
    HarnessTaskMigrationReviewPacketPreparer ..> HarnessTaskMigrationReviewPacket : immutable output
    HarnessTaskMigrationReviewPacket *-- HarnessTaskMigrationReviewPacketRequest : validated exact values
    HarnessTaskMigrationFileDisposition *-- HarnessTaskMigrationReviewPacket : exact packet
    HarnessTaskMigrationFileDisposition *-- HumanReviewDecision : exact human response
    HarnessTaskMigrationFileDisposition --> HarnessTaskMigrationDisposition : file outcome
    HarnessTaskMigrationFileDispositionRecorder ..> HarnessTaskMigrationReviewPacket : input
    HarnessTaskMigrationFileDispositionRecorder ..> HumanReviewDecision : input
    HarnessTaskMigrationFileDispositionRecorder ..> HarnessTaskMigrationFileDisposition : output
    TaskRecordAdapter ..> HarnessTask : temporary compatibility view
    TaskStateInspector ..> TaskRecordAdapter : mixed Markdown JSON inspection
```

## Focused class diagrams

### `HarnessTask`

```mermaid
classDiagram
    class HarnessTask {
        <<DataObject>>
        +int schema_version
        +Identifier task_id
        +str title
        +Identifier status
        +str_or_none status_detail
        +Identifier_or_none parent_task_id
        +tuple task_prerequisite_ids
        +tuple external_prerequisite_ids
        +bool explicit_activation_required
        +str objective
        +tuple authority_reference_paths
        +tuple authorized_scope
        +tuple completion_criteria
        +tuple exclusions
        +ResourcePath intake_path
        +ResourcePath documentation_path
    }
```

### `HarnessTaskSerializer`

```mermaid
classDiagram
    class HarnessTaskSerializer {
        <<ActionObject>>
        +execute(task) bytes
    }
    class HarnessTask {
        <<DataObject>>
    }
    HarnessTaskSerializer ..> HarnessTask : explicit input
```

### `HarnessTaskDeserializer`

```mermaid
classDiagram
    class HarnessTaskDeserializer {
        <<ActionObject>>
        +execute(json_bytes) HarnessTask
    }
    class HarnessTask {
        <<DataObject>>
    }
    HarnessTaskDeserializer ..> HarnessTask : strict output
```

### `HarnessTaskGraphValidator`

```mermaid
classDiagram
    class HarnessTaskGraphValidator {
        <<ActionObject>>
        +execute(tasks) ValidationResult
    }
    class HarnessTask {
        <<DataObject>>
    }
    class ValidationResult {
        <<ResultObject>>
    }
    HarnessTaskGraphValidator ..> HarnessTask : explicit graph input
    HarnessTaskGraphValidator ..> ValidationResult : structural output
```

### `HarnessTaskDocumentSource`

```mermaid
classDiagram
    class HarnessTaskDocumentSource {
        <<DataObject>>
        +path
        +revision or Git object identity
        +exact bytes
        +byte count
        +ArtifactIdentity content identity
    }
    class ArtifactIdentity {
        <<DataObject>>
    }
    HarnessTaskDocumentSource *-- ArtifactIdentity : exact bytes
```

### `HarnessTaskSourceDisposition`

```mermaid
classDiagram
    class HarnessTaskSourceDisposition {
        <<enumeration>>
        CANONICAL_TASK_INFORMATION
        DOCUMENTATION_OWNED_CONTENT
        HISTORICAL_EVIDENCE
        PROPOSED_REMOVAL
    }
```

### `HarnessTaskSourceMapping`

```mermaid
classDiagram
    class HarnessTaskSourceMapping {
        <<DataObject>>
        +mapping identity
        +source identity
        +start and end byte offsets
        +HarnessTaskSourceDisposition disposition
        +tuple target_references
        +transformation
        +rationale
    }
    class HarnessTaskSourceDisposition {
        <<enumeration>>
    }
    HarnessTaskSourceMapping --> HarnessTaskSourceDisposition : one disposition
```

### `HarnessTaskDocumentationContent`

```mermaid
classDiagram
    class HarnessTaskDocumentationContent {
        <<DataObject>>
        +HarnessTaskDocumentSource source
        +ordered accepted documentation spans
        +exact narrative and opaque bytes
        +ordered source mapping identities
    }
    class HarnessTaskDocumentSource {
        <<DataObject>>
    }
    class HarnessTaskSourceMapping {
        <<DataObject>>
    }
    HarnessTaskDocumentationContent *-- HarnessTaskDocumentSource : exact source
    HarnessTaskDocumentationContent *-- HarnessTaskSourceMapping : owned spans
```

### `HarnessTaskProjectionProfile`

```mermaid
classDiagram
    class HarnessTaskProjectionProfile {
        <<DataObject>>
        +profile identity and version
        +section and field ordering
        +format rules
        +exact template identity or bytes
        +final newline policy
    }
```

### `HarnessTaskDocumentation`

```mermaid
classDiagram
    class HarnessTaskDocumentation {
        <<DataObject>>
        +path
        +complete Markdown bytes
        +ArtifactIdentity content identity
    }
    class ArtifactIdentity {
        <<DataObject>>
    }
    HarnessTaskDocumentation *-- ArtifactIdentity : rendered bytes
```

### `HarnessTaskDocumentationRenderer`

```mermaid
classDiagram
    class HarnessTaskDocumentationRenderer {
        <<ActionObject>>
        +execute(task, content, profile) HarnessTaskDocumentation
    }
    class HarnessTask {
        <<DataObject>>
    }
    class HarnessTaskDocumentationContent {
        <<DataObject>>
    }
    class HarnessTaskProjectionProfile {
        <<DataObject>>
    }
    class HarnessTaskDocumentation {
        <<DataObject>>
    }
    HarnessTaskDocumentationRenderer ..> HarnessTask : explicit input
    HarnessTaskDocumentationRenderer ..> HarnessTaskDocumentationContent : explicit input
    HarnessTaskDocumentationRenderer ..> HarnessTaskProjectionProfile : explicit input
    HarnessTaskDocumentationRenderer ..> HarnessTaskDocumentation : output
```

### `HarnessTaskDocumentationComparator`

```mermaid
classDiagram
    class HarnessTaskDocumentationComparator {
        <<ActionObject>>
        +execute(source, rendered, mappings) HarnessTaskDocumentationComparisonResult
    }
    class HarnessTaskDocumentSource {
        <<DataObject>>
    }
    class HarnessTaskDocumentation {
        <<DataObject>>
    }
    class HarnessTaskSourceMapping {
        <<DataObject>>
    }
    class HarnessTaskDocumentationComparisonResult {
        <<ResultObject>>
    }
    HarnessTaskDocumentationComparator ..> HarnessTaskDocumentSource : source
    HarnessTaskDocumentationComparator ..> HarnessTaskDocumentation : rendered
    HarnessTaskDocumentationComparator ..> HarnessTaskSourceMapping : coverage
    HarnessTaskDocumentationComparator ..> HarnessTaskDocumentationComparisonResult : output
```

### `HarnessTaskDocumentationComparisonResult`

```mermaid
classDiagram
    class HarnessTaskDocumentationComparisonResult {
        <<ResultObject>>
        +comparison status
        +source and rendered identities
        +exact differences
        +structured findings
        +unmapped source spans
        +limitations
    }
```

### `HarnessTaskMigrationReviewPacketRequest`

```mermaid
classDiagram
    class HarnessTaskMigrationReviewPacketRequest {
        <<immutable DataObject>>
        +HarnessTaskDocumentSource source
        +tuple~HarnessTaskSourceMapping~ mappings
        +HarnessTask candidate_task
        +bytes canonical_task_json
        +HarnessTaskDocumentationContent documentation_content
        +HarnessTaskProjectionProfile projection_profile
        +HarnessTaskDocumentation rendered_documentation
        +HarnessTaskDocumentationComparisonResult comparison
        +HumanReviewPacket human_review_packet
    }
    class HarnessTaskDocumentSource {
        <<DataObject>>
    }
    class HarnessTaskSourceMapping {
        <<DataObject>>
    }
    class HarnessTask {
        <<DataObject>>
    }
    class HarnessTaskDocumentationContent {
        <<DataObject>>
    }
    class HarnessTaskProjectionProfile {
        <<DataObject>>
    }
    class HarnessTaskDocumentation {
        <<DataObject>>
    }
    class HarnessTaskDocumentationComparisonResult {
        <<ResultObject>>
    }
    class HumanReviewPacket {
        <<ResultObject>>
    }
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentSource : exact source
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskSourceMapping : complete ordered tuple
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTask : candidate
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentationContent : narrative and opaque bytes
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskProjectionProfile : rendering configuration
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentation : rendered output
    HarnessTaskMigrationReviewPacketRequest *-- HarnessTaskDocumentationComparisonResult : comparison
    HarnessTaskMigrationReviewPacketRequest *-- HumanReviewPacket : generic review component
```

The request validates only intrinsic type, immutability, tuple, nonempty, and
lexical invariants. It does not validate compatibility among its objects. It is
runtime-only unless the frozen Stage-1 contract later justifies a wire or
persistence requirement.

### `HarnessTaskMigrationReviewPacketPreparer`

```mermaid
classDiagram
    class HarnessTaskMigrationReviewPacketPreparer {
        <<stateless ActionObject>>
        +execute(request) HarnessTaskMigrationReviewPacket
    }
    class HarnessTaskMigrationReviewPacketRequest {
        <<immutable DataObject>>
    }
    class HarnessTaskMigrationReviewPacket {
        <<ResultObject>>
    }
    class HumanReviewPreparer {
        <<ActionObject>>
    }
    HarnessTaskMigrationReviewPacketPreparer ..> HarnessTaskMigrationReviewPacketRequest : explicit input
    HarnessTaskMigrationReviewPacketPreparer ..> HumanReviewPreparer : may reuse generic behavior
    HarnessTaskMigrationReviewPacketPreparer ..> HarnessTaskMigrationReviewPacket : deterministic output
```

Its exact proposed action boundary is:

```text
HarnessTaskMigrationReviewPacketPreparer.execute(
    request: HarnessTaskMigrationReviewPacketRequest,
) -> HarnessTaskMigrationReviewPacket
```

The preparer owns source-identity agreement; complete, ordered, nonoverlapping
mapping coverage; mapping references to the exact source; candidate Task and
canonical JSON agreement; documentation-content and source-span agreement;
projection-profile and rendered-document agreement; rendered/source comparison
identity; consistency of comparison status, differences, findings, and unmapped
spans; generic `HumanReviewPacket` target and revision agreement; and
deterministic construction of the immutable migration packet.

It may reuse `HumanReviewPreparer` behavior but does not duplicate or replace
generic human-review semantics. It performs no filesystem or repository
discovery, current-directory or Git-root inference, Git access, persistence,
human-response interpretation, human acceptance, source replacement, Task
migration, checkpoint mutation, Task activation, or successor activation.

### `HarnessTaskMigrationReviewPacket`

```mermaid
classDiagram
    class HarnessTaskMigrationReviewPacket {
        <<ResultObject>>
        +HarnessTaskMigrationReviewPacketRequest request
    }
    class HarnessTaskMigrationReviewPacketRequest {
        <<immutable DataObject>>
    }
    class HarnessTaskMigrationReviewPacketPreparer {
        <<stateless ActionObject>>
    }
    HarnessTaskMigrationReviewPacketPreparer ..> HarnessTaskMigrationReviewPacketRequest : validates
    HarnessTaskMigrationReviewPacketPreparer ..> HarnessTaskMigrationReviewPacket : produces
    HarnessTaskMigrationReviewPacket *-- HarnessTaskMigrationReviewPacketRequest : binds exact values
```

### `HarnessTaskMigrationDisposition`

```mermaid
classDiagram
    class HarnessTaskMigrationDisposition {
        <<enumeration>>
        ACCEPT_FILE_MIGRATION
        REVISE_CONTRACT_OR_MAPPING
        RETAIN_DOCUMENTATION_OWNERSHIP
        DEFER_FILE
    }
```

### `HarnessTaskMigrationFileDisposition`

```mermaid
classDiagram
    class HarnessTaskMigrationFileDisposition {
        <<ResultObject>>
        +HarnessTaskMigrationReviewPacket packet
        +HumanReviewDecision human decision
        +HarnessTaskMigrationDisposition migration disposition
    }
    class HarnessTaskMigrationReviewPacket {
        <<ResultObject>>
    }
    class HumanReviewDecision {
        <<ResultObject>>
    }
    class HarnessTaskMigrationDisposition {
        <<enumeration>>
    }
    HarnessTaskMigrationFileDisposition *-- HarnessTaskMigrationReviewPacket : exact packet
    HarnessTaskMigrationFileDisposition *-- HumanReviewDecision : verbatim response
    HarnessTaskMigrationFileDisposition --> HarnessTaskMigrationDisposition : exact outcome
```

### `HarnessTaskMigrationFileDispositionRecorder`

```mermaid
classDiagram
    class HarnessTaskMigrationFileDispositionRecorder {
        <<ActionObject>>
        +execute(packet, human_decision, migration_disposition) HarnessTaskMigrationFileDisposition
    }
    class HarnessTaskMigrationReviewPacket {
        <<ResultObject>>
    }
    class HumanReviewDecision {
        <<ResultObject>>
    }
    class HarnessTaskMigrationDisposition {
        <<enumeration>>
    }
    class HarnessTaskMigrationFileDisposition {
        <<ResultObject>>
    }
    HarnessTaskMigrationFileDispositionRecorder ..> HarnessTaskMigrationReviewPacket : input
    HarnessTaskMigrationFileDispositionRecorder ..> HumanReviewDecision : input
    HarnessTaskMigrationFileDispositionRecorder ..> HarnessTaskMigrationDisposition : input
    HarnessTaskMigrationFileDispositionRecorder ..> HarnessTaskMigrationFileDisposition : output
```

## Public-interface accounting

The proposal contains exactly 19 new project-local interfaces: 10 DataObject or
ResultObject interfaces, seven ActionObjects, and two enumerations. They are
proposed for `ksdft2effmass.harness.pi.local`; Task vocabulary and schemas do not
move into the generic harness surface. The two newly explicit
interfaces are the runtime-only immutable
`HarnessTaskMigrationReviewPacketRequest` and the stateless
`HarnessTaskMigrationReviewPacketPreparer`. Reused classes in the earlier table
do not count as newly proposed interfaces.

The request does not become a serialized record. Only project-local
`HarnessTask` schema version 2 has a proposed wire, owned by
`harness/local/schemas/task-record-v2.schema.json`; the version-1 pilot schema
remains supported and no generic `HarnessWireRecord` member is added. No
implementation or serialized record is added by this contract stage.

`HarnessTaskMigrationReviewPacket` remains the immutable ResultObject produced
by the preparer. `HumanReviewDecisionRecorder` remains the sole owner of the
generic human decision. `HarnessTaskMigrationFileDispositionRecorder` remains
the migration-domain action that validates the exact packet/decision
relationship and produces `HarnessTaskMigrationFileDisposition`. Neither action
moves human interpretation or authority into packet preparation or disposition
recording.

## Proposed verification obligations

Stage 1 must specify software-verification evidence for these boundaries without
implementing tests during the contract stage:

- request construction accepts only the exact field types and enforces
  immutability, tuple, nonempty, and lexical invariants;
- request construction does not perform cross-object identity or compatibility
  validation;
- the preparer rejects every listed source, mapping, Task/JSON, documentation,
  projection, rendering, comparison, and generic-review incompatibility;
- equivalent explicit requests produce equal immutable packet values
  deterministically;
- the preparer performs no discovery, Git access, persistence, human-response
  interpretation, authority change, mutation, migration, activation, or
  successor activation;
- any reuse of `HumanReviewPreparer` preserves generic human-review semantics;
- `HumanReviewDecisionRecorder` retains generic decision ownership; and
- `HarnessTaskMigrationFileDispositionRecorder` requires the exact packet and
  decision relationship and cannot interpret or accept a human response.

No request serialization round-trip obligation exists unless Stage 1 separately
justifies and proposes a wire contract for human acceptance.

## Stage 1: Task-model contract

Stage 1 performs current-revision inventory, complete six-file source-span
mapping, field and rendering-contract derivation, canonical schema and fixture
design, public-API accounting for all 19 proposed interfaces, verification-
obligation design for the request/preparer and remaining boundaries, and renewed
human review. It does not replace source authority, implement a class, generate
a file packet, or migrate a file.

The maintained Stage-1 Task page is
[harness.002.001.011](ksdft2effmass.harness.002.001.011.md).

## Stage 2: serial per-file migration

Stage 2 remains inactive and blocked until Stage 1 is completed and its frozen
contract is explicitly human-accepted. Stage 2 then implements exactly that
contract and processes the six files serially.

One immutable file packet is prepared, then work stops for one human disposition:

1. accept this file migration;
2. revise the contract or mapping;
3. retain documentation ownership; or
4. defer the file.

A required contract change stops Stage 2. It cannot be applied inside a file
packet and must return to a separately reviewed contract-revision decision.

## Review semantics

Both stages use the bounded rule:

```text
one independent review is completed
→ every material finding receives an explicit disposition
→ every correction receives deterministic verification
→ no material finding remains unresolved
```

The retained Stage-1 [independent review](../../.pi/evidence/docs-json/task-model-contract/integration-review.md)
failed with seven material findings. The single bounded
[correction disposition](../../.pi/evidence/docs-json/task-model-contract/review-correction.md)
corrected all seven and deterministically verified the resulting contract. The
initial failed review remains failed; no second review rewrote it, and no material
contract finding remains unresolved. The bounded version-1 generated-projection
drift and its pending disposition are reported in the
[validation record](../../.pi/evidence/docs-json/task-model-contract/validation.md).

## Selection-state boundary

Selection-state implementation is outside both proposed stages. The accepted
architecture still requires future selection state to remain separate from Task
data, but its DataObject, fields, validation, comparison, diagrams, implementation,
and cutover require a later separately authorized Task. The current chain remains
operational authority and may not be deleted or cut over here.

## Explicit exclusions

Neither proposed stage authorizes implementation or migration before its own
activation. Neither stage authorizes batch review, ambient discovery, hidden
renderer inputs, schema expansion during Stage 2, selection-state implementation,
chain cutover or deletion, SQLite, telemetry, dependencies, scientific work,
publication, external execution, protected work, release action, or automatic
successor activation.

## Renewed human review question

Should the frozen 19-interface contract, complete 118-span mapping set, six
proposed documentation destinations, and verified correction dispositions be
accepted as the Stage-2 implementation contract? Acceptance completes Stage 1
but does not activate Stage 2 or accept any file migration.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Incremental migration plan](ksdft2effmass.harness.002.001.009.md)
- **Next:** [HarnessTask model-contract stage](ksdft2effmass.harness.002.001.011.md)
