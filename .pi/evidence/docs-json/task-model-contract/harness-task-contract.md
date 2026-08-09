# Frozen HarnessTask model contract proposal

Status: Proposed contract for human acceptance; no interface is implemented.

Task: `harness.simplification.docs-json.task-model-contract`

Source revision: `dd50c74513f6c51e2a1c823a60b3111738082b3c`

Inventory: `source-inventory.json`

Mappings: `source-mappings.json`

## Contract boundary

This proposal is derived from complete byte-span mappings of the six selected Markdown Task sources. Markdown remains source authority. The proposed Stage-2 documentation destinations are review targets only and do not yet exist. No packet, migrated Task JSON, public class, schema, fixture, test, or selection-state implementation is created by this contract record.

The public model contains exactly 19 proposed interfaces. Concrete immutable records use composition and do not inherit from nominal DataObject or ActionObject bases. Wrong semantic types raise `TypeError`; correctly typed values that violate intrinsic invariants raise `ValueError`. Booleans are rejected where integers are required. Public tuples are exact tuples and nested state is immutable.

## Shared lexical types

`Identifier` uses `^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$`.

`ResourcePath` is relative, uses `/`, contains no empty, `.` or `..` segment, backslash, control character, or platform device name, and never derives authority from the current directory.

`ArtifactIdentity` is the existing schema-version-1 SHA-256 identity with algorithm `sha256` and a 64-character lowercase hexadecimal digest.

Text fields are exact nonempty built-in strings unless explicitly optional. Identifier and path tuples are lexically sorted and unique. Narrative tuples preserve declared order, are nonempty, and contain no duplicate exact values.

## 1. HarnessTask

Stereotype: immutable DataObject.

Exact field order and types:

| Field | Type | Intrinsic contract |
|---|---|---|
| `schema_version` | built-in `int` | exactly `2`; Boolean rejected |
| `task_id` | `Identifier` | nonempty lexical identity |
| `title` | built-in `str` | nonempty |
| `status` | `Identifier` | lifecycle fact; no status meaning inferred from identifier hierarchy |
| `status_detail` | built-in `str` or `None` | optional exact human-readable detail; not an activation source |
| `parent_task_id` | `Identifier` or `None` | may not equal `task_id` intrinsically |
| `task_prerequisite_ids` | tuple of `Identifier` | sorted, unique; excludes `task_id` |
| `external_prerequisite_ids` | tuple of `Identifier` | sorted, unique; excludes `task_id`; disjoint from Task prerequisites |
| `explicit_activation_required` | built-in `bool` | exact Boolean |
| `objective` | built-in `str` | nonempty |
| `authority_reference_paths` | tuple of `ResourcePath` | nonempty, sorted, unique |
| `authorized_scope` | tuple of built-in `str` | nonempty, ordered, unique |
| `completion_criteria` | tuple of built-in `str` | nonempty, ordered, unique |
| `exclusions` | tuple of built-in `str` | nonempty, ordered, unique |
| `intake_path` | `ResourcePath` | separate non-executable human intake |
| `documentation_path` | `ResourcePath` | maintained human-review document; not an activation or completion source |

The constructor owns only these intrinsic invariants. It does not check whether referenced Tasks or files exist, whether a prerequisite is completed, whether the documentation agrees, whether activation is authorized, or whether the Task graph is acyclic.

The six mappings require the two additions to the pilot shape: `status_detail` preserves operational detail previously embedded after the lifecycle token, and `documentation_path` binds the required maintained review document. Schema version 2 distinguishes this closed contract from the existing version-1 pilot, which remains exactly supported during serial migration. No `child_task_ids` field is added because parent relations on children define hierarchy without duplicated graph authority. No selection-state, active-task, successor, timestamp, database, event-log, review-decision, or computed-completion field belongs to `HarnessTask`.

## 2. HarnessTaskSerializer

Stereotype: stateless ActionObject.

Boundary: `execute(task: HarnessTask) -> bytes`.

It emits UTF-8 JSON with no BOM, the exact field order above, two-space indentation, JSON arrays for tuples, JSON null for optional absence, no trailing spaces, and exactly one final LF. `ensure_ascii` is false. Object keys and values are never discovered from files or globals. It serializes only `HarnessTask`; supporting runtime objects are not wire records.

## 3. HarnessTaskDeserializer

Stereotype: stateless ActionObject.

Boundary: `execute(payload: bytes) -> HarnessTask`.

It accepts exact built-in bytes containing one UTF-8 JSON object, rejects a BOM, invalid UTF-8, duplicate keys, unknown keys, missing keys, wrong JSON types, invalid lexical values, and unsupported schema versions, and returns the exact immutable `HarnessTask`. It performs no file I/O and no graph, authority, documentation, or activation validation.

## Canonical HarnessTask wire

The only new serialized public record is project-local `HarnessTask`. Its closed JSON object has exactly the 16 fields listed above and schema version 2. Arrays preserve the tuple ordering contract. Canonical serializer bytes are the equality oracle. Deserialization may accept semantically valid noncanonical whitespace and object-key order, but reserialization produces canonical bytes. Numeric overflow is not applicable beyond requiring a built-in Python integer equal to schema version 2.

Proposed owning schema: `harness/local/schemas/task-record-v2.schema.json`, with resource ID `ksdft2effmass.local.task-record.v2`.

The existing project-local `harness/local/schemas/task-record.schema.json` remains the version-1 pilot schema. It is neither replaced nor delegated to a generic schema during this six-file migration. `HarnessTaskSerializer` and `HarnessTaskDeserializer` are dedicated project-local actions and do not add `HarnessTask` to generic `WireRecordKind` or `HarnessWireRecord`. The request, source, mapping, documentation, profile, comparison, packet, and disposition objects remain runtime-only.

## 4. HarnessTaskGraphValidator

Stereotype: stateless ActionObject.

Boundary: `execute(tasks: tuple[HarnessTask, ...]) -> ValidationResult`.

It requires an exact nonempty tuple and validates unique Task identities; resolvable parents and Task prerequisites; no self-parent or self-prerequisite; disjoint Task and external prerequisites; acyclic parent and prerequisite graphs; unique intake and documentation paths; and consistency of every parent and prerequisite reference with the supplied graph. It treats `status` as opaque project-local lifecycle text and applies no completed-prerequisite or active-status policy. Existing explicit Task/chain relation validation owns lifecycle compatibility. It does not infer parentage from dot prefixes, infer ordering from file names, select an active Task, activate a successor, read a chain, or access files. Findings use stable identifiers and deterministic order by finding identifier, subject, and related identity.

## 5. HarnessTaskDocumentSource

Stereotype: immutable DataObject.

Fields, in order: `path: ResourcePath`, `revision: Identifier`, `git_object: str | None`, `content: bytes`, `byte_count: int`, and `artifact_identity: ArtifactIdentity`.

Intrinsic invariants require exact built-in bytes, nonnegative built-in integer byte count equal to `len(content)`, optional Git object text matching 40 lowercase hexadecimal characters, and artifact identity equal to SHA-256 of `content`. Revision/path compatibility and repository existence are not constructor concerns.

## 6. HarnessTaskSourceDisposition

Stereotype: enumeration.

Closed values: `CANONICAL_TASK_INFORMATION`, `DOCUMENTATION_OWNED_CONTENT`, `HISTORICAL_EVIDENCE`, and `PROPOSED_REMOVAL`. Proposed removal never authorizes removal.

## 7. HarnessTaskSourceMapping

Stereotype: immutable DataObject.

Fields, in order: `mapping_id: Identifier`, `source_identity: ArtifactIdentity`, `start_byte: int`, `end_byte: int`, `span_identity: ArtifactIdentity`, `disposition: HarnessTaskSourceDisposition`, `target_references: tuple[str, ...]`, `transformation: str`, and `rationale: str`.

Intrinsic invariants require built-in nonnegative offsets with `end_byte > start_byte`, nonempty unique lexical target references, and nonempty transformation and rationale. The constructor does not check source bounds, span bytes, global coverage, ordering, overlap, target existence, or cross-object compatibility.

## 8. HarnessTaskDocumentationContent

Stereotype: immutable DataObject.

Fields, in order: `source_identity: ArtifactIdentity`, `documentation_path: ResourcePath`, `content_mapping_ids: tuple[Identifier, ...]`, and `content_blocks: tuple[bytes, ...]`.

The two tuples are exact, nonempty, equal length, and preserve source order; mapping IDs are unique; content blocks are nonempty exact bytes. Cross-checking IDs, source spans, and target paths belongs to an ActionObject.

## 9. HarnessTaskProjectionProfile

Stereotype: immutable DataObject.

Fields, in order: `schema_version: int`, `profile_id: Identifier`, `template_bytes: bytes`, `template_identity: ArtifactIdentity`, `layout_tokens: tuple[str, ...]`, and `final_lf: bool`.

Schema version is 1. Template identity intrinsically matches exact template bytes. `layout_tokens` is an exact nonempty tuple. Tokens use the closed prefixes `literal:`, `task:`, and `content:` followed by a nonempty lexical reference. `task:` and `content:` references are each unique; every content mapping ID occurs exactly once as a `content:` token; `literal:` tokens may repeat. The profile contains every template and ordering input; it never discovers a template or parser state.

## 10. HarnessTaskDocumentation

Stereotype: immutable DataObject.

Fields, in order: `path: ResourcePath`, `content: bytes`, and `artifact_identity: ArtifactIdentity`. The identity intrinsically equals SHA-256 of the exact content.

## 11. HarnessTaskDocumentationRenderer

Stereotype: stateless ActionObject.

Boundary: `execute(task: HarnessTask, content: HarnessTaskDocumentationContent, profile: HarnessTaskProjectionProfile) -> HarnessTaskDocumentation`.

It validates explicit Task/content/profile compatibility, resolves every layout token exactly once as required by the profile, preserves each documentation-owned byte block exactly, formats canonical Task values by the profile, enforces the declared final-LF rule, and returns complete Markdown bytes. It performs no filesystem, current-directory, repository-root, Git, global-template, persistence, activation, acceptance, or migration behavior.

## 12. HarnessTaskDocumentationComparator

Stereotype: stateless ActionObject.

Boundary: `execute(source: HarnessTaskDocumentSource, rendered: HarnessTaskDocumentation, mappings: tuple[HarnessTaskSourceMapping, ...]) -> HarnessTaskDocumentationComparisonResult`.

It validates ordered contiguous source coverage, compares exact bytes, attributes every difference to accepted canonical rendering or an exact documentation block, and reports any unmapped or incompatible difference. It does not decide whether a migration is acceptable.

## 13. HarnessTaskDocumentationComparisonResult

Stereotype: immutable ResultObject.

Fields, in order: `status: Identifier`, `source_identity: ArtifactIdentity`, `rendered_identity: ArtifactIdentity`, `differences: tuple[str, ...]`, `findings: tuple[HumanReviewFinding, ...]`, `unmapped_spans: tuple[tuple[int, int], ...]`, and `limitations: tuple[str, ...]`.

Closed statuses are `EXACT`, `MAPPED_DIFFERENCES`, and `UNMAPPED_DIFFERENCES`. Difference, finding, span, and limitation tuples are immutable and deterministically ordered. Intrinsic range validity belongs to the result; agreement with actual source bytes belongs to the comparator and packet preparer.

## 14. HarnessTaskMigrationReviewPacketRequest

Stereotype: immutable runtime-only DataObject.

Fields, in order: `source: HarnessTaskDocumentSource`, `mappings: tuple[HarnessTaskSourceMapping, ...]`, `candidate_task: HarnessTask`, `canonical_task_json: bytes`, `documentation_content: HarnessTaskDocumentationContent`, `projection_profile: HarnessTaskProjectionProfile`, `rendered_documentation: HarnessTaskDocumentation`, `comparison: HarnessTaskDocumentationComparisonResult`, and `human_review_packet: HumanReviewPacket`.

It requires exact field types, a nonempty exact mappings tuple, and immutable nested values. It owns no cross-object identity or compatibility validation and has no wire or persistence contract.

## 15. HarnessTaskMigrationReviewPacketPreparer

Stereotype: stateless ActionObject.

Boundary: `execute(request: HarnessTaskMigrationReviewPacketRequest) -> HarnessTaskMigrationReviewPacket`.

It validates source identity agreement; complete ordered nonoverlapping mapping coverage; exact-source mapping references and span identities; candidate Task and canonical serializer-byte agreement; documentation content, mapping, and source-span agreement; projection profile, rendered path, and rendered bytes agreement; comparison source/render identities and consistency of status, differences, findings, and unmapped spans; generic `HumanReviewPacket` target and revision agreement; and deterministic packet construction. It may invoke `HumanReviewPreparer` through its public behavior but does not duplicate generic review semantics.

It performs no discovery, current-directory or Git-root inference, Git access, persistence, human-response interpretation, human acceptance, source replacement, Task migration, checkpoint mutation, Task activation, or successor activation.

## 16. HarnessTaskMigrationReviewPacket

Stereotype: immutable ResultObject.

Sole field: `request: HarnessTaskMigrationReviewPacketRequest`. The packet is the validated exact request bundle produced only by the preparer contract. Removing a separately generated packet identifier makes equal explicit requests produce equal packet values without an unstated identity algorithm. Its constructor owns the exact request type invariant only and does not rerun cross-object preparation logic.

## 17. HarnessTaskMigrationDisposition

Stereotype: enumeration.

Closed values: `ACCEPT_FILE_MIGRATION`, `REVISE_CONTRACT_OR_MAPPING`, `RETAIN_DOCUMENTATION_OWNERSHIP`, and `DEFER_FILE`.

## 18. HarnessTaskMigrationFileDisposition

Stereotype: immutable ResultObject.

Fields, in order: `packet: HarnessTaskMigrationReviewPacket`, `human_decision: HumanReviewDecision`, and `migration_disposition: HarnessTaskMigrationDisposition`. It records an outcome and owns no interpretation or mutation behavior.

## 19. HarnessTaskMigrationFileDispositionRecorder

Stereotype: stateless ActionObject.

Boundary: `execute(packet: HarnessTaskMigrationReviewPacket, human_decision: HumanReviewDecision, migration_disposition: HarnessTaskMigrationDisposition) -> HarnessTaskMigrationFileDisposition`.

It requires `human_decision.packet == packet.request.human_review_packet`, which binds the exact generic target and revision already validated by the preparer. It applies this closed compatibility table:

| `HumanReviewDecision.disposition` | `HarnessTaskMigrationDisposition` |
|---|---|
| `accepted` | `ACCEPT_FILE_MIGRATION` |
| `bounded_correction` | `REVISE_CONTRACT_OR_MAPPING` |
| `rejected` | `RETAIN_DOCUMENTATION_OWNERSHIP` |
| `deferred` | `DEFER_FILE` |

No other pair is valid. `HumanReviewDecisionRecorder` remains the sole owner of generic human-response recording, including the requirement that `bounded_correction` alone carries nonempty authorized scope. Interpretation remains outside both recorders. This action performs no persistence, checkpoint mutation, source replacement, migration, activation, or successor selection.

## Public import accounting

All 19 proposed names are exported from the project-local `ksdft2effmass.harness.pi.local` surface and owned in a focused Task-domain module or subpackage. Existing `ArtifactIdentity`, `ValidationResult`, human-review classes, `TaskRecordAdapter`, and `TaskStateInspector` are reused and do not count toward 19. No nominal base class, Workflow, selection-state class, or new free-function API is proposed.

## Proposed resources and compatibility

The accepted implementation stage may add only these project-local resource families:

- schema `harness/local/schemas/task-record-v2.schema.json`, resource ID `ksdft2effmass.local.task-record.v2`;
- projection profile `harness/local/projections/harness-task-documentation-v2.json`, resource ID `ksdft2effmass.local.harness-task-documentation.v2`;
- fixture index `harness/local/fixtures/task-record-v2/fixture-index.json`, resource ID `ksdft2effmass.local.task-record-v2.fixture-index`;
- canonical valid fixtures `harness/local/fixtures/task-record-v2/valid/minimal.json` and `complete.json`, resource IDs `ksdft2effmass.local.task-record-v2.valid.minimal` and `ksdft2effmass.local.task-record-v2.valid.complete`;
- invalid fixtures under `harness/local/fixtures/task-record-v2/invalid/`: `missing-<field>.json` and `wrong-type-<field>.json` for each of the 16 exact wire fields, plus `unknown-field.json`, `boolean-schema-version.json`, `unsupported-version.json`, `duplicate-key.json`, `invalid-identifier.json`, `invalid-path.json`, `unsorted-identifiers.json`, `duplicate-identifiers.json`, `unsorted-paths.json`, `duplicate-paths.json`, `duplicate-narrative.json`, `empty-required-text.json`, and `empty-required-tuple.json`; each resource ID is `ksdft2effmass.local.task-record-v2.invalid.<filename-stem>`;
- explicit entries and dependencies in `harness/local/resource-manifest.json` and `harness/local/fixtures/oracle-index.json`.

The schema has no resource dependency. The projection profile depends on the v2 schema. Every valid or invalid fixture depends on the v2 schema. The fixture index depends on the schema and every indexed fixture. The oracle-index entry depends on the fixture index. Each manifest entry binds the exact resource ID, relative path, SHA-256 identity calculated from implementation bytes, kind, and these explicit dependencies; no identity is fabricated before those bytes exist. No generic `harness/pi` resource or manifest changes are proposed. The v2 schema and canonical fixtures define serializer/deserializer agreement; the projection profile depends on the v2 schema and contains only explicit rendering inputs.

Compatibility covers the existing version-1 JSON pilot plus all six Markdown records before migration. After each accepted serial migration it covers the pilot, the increasing set of version-2 JSON records, and the decreasing six-to-zero Markdown set. `TaskRecordAdapter` remains the temporary mixed-format compatibility boundary and delegates version-2 canonical JSON semantics to the project-local deserializer rather than becoming the model.

Proposed Stage-2 destinations:

| Source Task | Maintained documentation | Non-executable intake |
|---|---|---|
| `.pi/tasks/harness.simplification.docs-json.md` | `docs/harness/ksdft2effmass.harness.002.001.012.md` | `.pi/tasks/harness.simplification.docs-json.intake.md` |
| `.pi/tasks/harness.simplification.docs-json.publication.md` | `docs/harness/ksdft2effmass.harness.002.001.013.md` | `.pi/tasks/harness.simplification.docs-json.publication.intake.md` |
| `.pi/tasks/harness.simplification.docs-json.publication.triage.md` | `docs/harness/ksdft2effmass.harness.002.001.014.md` | `.pi/tasks/harness.simplification.docs-json.publication.triage.intake.md` |
| `.pi/tasks/harness.simplification.docs-json.publication.hierarchy.md` | `docs/harness/ksdft2effmass.harness.002.001.015.md` | `.pi/tasks/harness.simplification.docs-json.publication.hierarchy.intake.md` |
| `.pi/tasks/harness.simplification.docs-json.authority-catalog.md` | `docs/harness/ksdft2effmass.harness.002.001.016.md` | `.pi/tasks/harness.simplification.docs-json.authority-catalog.intake.md` |
| `.pi/tasks/harness.simplification.docs-json.documentation-correction.md` | `docs/harness/ksdft2effmass.harness.002.001.017.md` | `.pi/tasks/harness.simplification.docs-json.documentation-correction.intake.md` |

These are proposed destinations, not created files. Each Stage-2 file packet must bind exact candidate bytes and receive one explicit human disposition.

## Proposed verification obligations

Implementation evidence must cover every public class in a class-owned `test__<PublicClass>.py` module, plus genuine artifact-owned schema and canonical-byte fixtures. Required evidence includes intrinsic type/value boundaries; Boolean rejection for integer fields; nested immutability; serializer canonical bytes; strict duplicate/unknown/missing-key rejection; deserializer round trip; graph cycles and missing references; explicit-input rendering and opaque-byte preservation; exact difference attribution; request/preparer responsibility separation; every preparer incompatibility; deterministic packet equality; generic decision ownership; exact packet/decision recording; absence of discovery, I/O, persistence, activation, and successor behavior; existing pilot compatibility; and mixed Markdown/JSON `TaskStateInspector` behavior after each serial migration.

Passing structural evidence establishes only software-contract conformance. It does not establish scientific validity, publication acceptance, or human acceptance.

## Human decision boundary

Acceptance freezes this contract for Stage 2. A material field, wire, ownership, rendering, packet, or verification change discovered during migration stops Stage 2 and requires a separately reviewed contract revision. Acceptance does not activate Stage 2, accept any file packet, migrate any source, or authorize selection-state work.
