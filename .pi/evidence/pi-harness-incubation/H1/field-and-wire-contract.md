# H1 field and wire contract

Status: corrected under resolved `H1-HC01` Option B and pending final H1 human
acceptance; no class, schema, fixture, or serializer is implemented by H1.

## Common semantic types

| Name | Exact Python semantic type | Version-1 rule | Rust mapping |
| --- | --- | --- | --- |
| `Identifier` | `str` | Nonempty ASCII; first character `[A-Za-z0-9]`; remaining characters `[A-Za-z0-9._:/-]`; case-sensitive; no normalization; opaque unless a field explicitly declares an enum. | `Identifier(String)` validated newtype |
| `ResourcePath` | `str` | Canonical root-relative POSIX regular-file resource path under the path contract below. | `ResourcePath(String)` validated newtype |
| `OwnershipScopePath` | `str` | Canonical repository-relative POSIX path paired with an explicit file/tree scope kind; no trailing slash. | `OwnershipScopePath(String)` validated newtype |
| `DiagnosticPath` | `str` | Immutable built-in string; nonempty NFC-normalized root-relative POSIX syntax; no absolute path, empty/`.`/`..` segment, repeated separator, trailing slash, control, backslash, Windows drive/device/UNC syntax, or case folding. Purely lexical on wire; may identify a regular file, directory, or ownership-scope prefix and makes no existence or regular-file claim. | `DiagnosticPath(String)` validated newtype |
| `Version` | `int` excluding `bool` | Range $1\ldots 2^{53}-1$; one closed integer contract version, not an implicit major/minor pair. The bound preserves exact RFC 8785/ECMAScript-number round trips. | `Version(u64)` with upper-bound validation |
| `SignedExitStatus` | `int` excluding `bool` | Range $0\ldots 2^{31}-1$; reserved for deferred command records only. | `u32` |
| immutable sequence | `tuple[T, ...]` | No mutable list is retained; ordering is field-specific. | `Vec<T>` retained behind immutable borrowing |
| optional value | `T | None` | Wire value is the member type or JSON `null`; the field itself is never omitted. | `Option<T>` |

Identifiers reject non-ASCII text in version 1 because all demonstrated current
identifiers are ASCII and no current consumer requires Unicode identifiers.
No semantic meaning, hierarchy, namespace ownership, or case folding is inferred
from an opaque identifier. Collision responsibility belongs to the producer or
the explicitly supplied project profile. Equality and sorting use exact ASCII
code-unit order.

## Common object and JSON rules

All included DataObjects and ResultObjects are operationally immutable, use exact
value equality over every declared field in field order, and have no dynamic
attributes. Intrinsic invalidity raises `TypeError` for the wrong Python semantic
type and `ValueError` for a violated intrinsic invariant when a caller constructs
a Python object directly. Actions convert expected malformed external input into
structured validation issues; unexpected programming defects remain exceptions.

Every record marked **public JSON: yes** uses one UTF-8 RFC 8259 JSON object.
The first field is `schema_version` and is integer `1`. The wire field names are
exactly the Python field names in the listed order. Unknown or omitted fields,
invalid UTF-8, a byte-order mark, unpaired surrogates, duplicate object keys,
nonfinite numbers, numeric strings, Boolean values in integer fields, and any
integer outside the field-specific bound (never above $2^{53}-1$) are rejected. Optional fields are present with `null`; other `null` values are
rejected. JSON object key order has no semantic meaning on input. Canonical output is the
RFC 8785 JSON Canonicalization Scheme applied recursively, encoded as UTF-8 with
no BOM, followed by one LF byte. The declared field order is Python/Rust object
construction order, not JSON key order; RFC 8785 lexicographic member ordering
owns canonical JSON object order and escaping. No included record contains a
floating-point field. Arrays preserve declared semantic order; fields declared
canonical sets are sorted before serialization. H1 creates no production schema or fixture; H3 owns those
accepted resources.

A malformed serialized record yields a `ValidationResult` containing an `ERROR`
issue owned by the relevant `PIH.WIRE.*`, `PIH.PATH.*`, or capability namespace.
It does not produce a partially trusted record. A structurally valid
`ResourceReference` or `ResourceManifest` candidate may contain relational
manifest defects and therefore deserialize successfully; callers must use
`ValidateResourceManifest` before resolution or skill validation. Serialization
attests represented bytes only; it does not establish provenance, manifest
validity, human acceptance, or semantic correctness.

## Included DataObjects

### `ArtifactIdentity`

Role: DataObject. Public JSON: yes.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | exactly `1` | `u64` |
| 2 | `algorithm` | `str` | yes | exactly `"sha256"` in version 1 | enum with `Sha256` |
| 3 | `digest` | `str` | yes | exactly 64 lowercase hexadecimal ASCII characters | `[u8; 32]`, lowercase hex on wire |

The version-1 default and only accepted algorithm is SHA-256. Uppercase digest
text is rejected rather than canonicalized. The digest claims byte-content
identity only. Equal algorithm and digest values mean the represented byte
sequences are asserted equal subject to SHA-256 collision responsibility; they
do not mean semantic equivalence. Version 1 carries no media/type field in `ArtifactIdentity` because no current
checksum consumer demonstrates one. Resource interpretation is represented
separately by `ResourceReference.resource_kind`; it does not participate in the
byte digest and does not make equal bytes semantically equivalent.

Exclusions: timestamps, filesystem paths, attestations, signatures, credentials,
open files, hash objects, and semantic-equivalence claims.

### `ResourceReference`

Role: DataObject. Public JSON: yes.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | `1` | `u64` |
| 2 | `resource_id` | `Identifier` | yes | stable opaque identity | `Identifier` |
| 3 | `resource_kind` | `str` | yes | one of `skill`, `reference`, `schema`, `template`, `profile`, `manifest`, `script`, `documentation` | `ResourceKind` enum |
| 4 | `format_version` | `Version` | yes | behavior/format version of this resource | `Version` |
| 5 | `path` | `ResourcePath` | yes | manifest-root-relative file path | `ResourcePath` |
| 6 | `content_identity` | `ArtifactIdentity` | yes | identity of exact file bytes | `ArtifactIdentity` |
| 7 | `dependency_ids` | `tuple[Identifier, ...]` | yes | unique and strictly identifier-sorted; a self-edge is structurally representable and is relationally invalid under `ValidateResourceManifest` | `Vec<Identifier>` |

Only regular files are resources in version 1. Directory resources, globs,
URLs, package names, ambient discovery, executable objects, and imported Python
objects are excluded.

### `ResourceManifest`

Role: DataObject. Public JSON: yes.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | `1` | `u64` |
| 2 | `manifest_id` | `Identifier` | yes | stable manifest identity | `Identifier` |
| 3 | `manifest_version` | `Version` | yes | resource-manifest content contract revision | `Version` |
| 4 | `layer` | `str` | yes | `generic` or `local` | `ManifestLayer` enum |
| 5 | `extends_manifest_id` | `Identifier | None` | yes | `null` for generic; required for local and names the generic manifest | `Option<Identifier>` |
| 6 | `resources` | `tuple[ResourceReference, ...]` | yes | nonempty; constructor canonicalizes to an immutable tuple ordered by the complete represented resource key while preserving duplicate IDs, duplicate paths, and exact duplicate entries for relational validation | `Vec<ResourceReference>` |

The complete represented resource ordering key is
`(resource_id, path, resource_kind, format_version, content_identity.algorithm,
content_identity.digest, dependency_ids)`; all version-1 schema-version fields
are fixed at `1`. Construction and deserialization establish only structural
candidate-manifest validity. They do not establish manifest acceptance,
authorization, resolvability, or capability validity. `ValidateResourceManifest` owns
cross-record relations: duplicate resource IDs and paths, self-edges, missing
dependencies, dependency cycles, generic-to-local dependencies, incompatible
kind/format, generic/local manifest mismatch, and forbidden local replacement.
Dependencies must resolve in the same manifest, or from a local manifest into
its named generic base. Generic resources cannot depend on local identities. A
local manifest is an explicit extension overlay; version 1 permits extension
only and forbids replacement of a generic `resource_id` or path, even when
hashes match.

### `ProjectProfile`

Role: DataObject. Public JSON: yes. Accepted instances are H3 local resources;
the generic class contains no project literal.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | profile schema version `1` | `u64` |
| 2 | `profile_id` | `Identifier` | yes | opaque profile identity | `Identifier` |
| 3 | `public_contract_version` | `Version` | yes | required closed Python contract integer version, initially `1` | `Version` |
| 4 | `generic_manifest_id` | `Identifier` | yes | required generic manifest identity | `Identifier` |
| 5 | `generic_manifest_version` | `Version` | yes | exact accepted generic manifest revision | `Version` |
| 6 | `local_manifest_id` | `Identifier | None` | yes | optional explicit local extension manifest | `Option<Identifier>` |
| 7 | `local_manifest_version` | `Version | None` | yes | required exactly when local manifest ID is present | `Option<Version>` |
| 8 | `overlay_policy` | `str` | yes | exactly `extend_only` in v1 | `OverlayPolicy` enum |
| 9 | `policy_reference_ids` | `tuple[Identifier, ...]` | yes | unique, strictly sorted provenance identities; actions never dereference them implicitly | `Vec<Identifier>` |
| 10 | `supported_resource_formats` | `tuple[tuple[Identifier, Version], ...]` | yes | unique strictly `(resource_kind, version)`-sorted accepted pairs | `Vec<(Identifier,Version)>` |
| 11 | `supported_skill_behaviors` | `tuple[tuple[Identifier, Version], ...]` | yes | unique strictly `(skill_id, version)`-sorted accepted pairs | `Vec<(Identifier,Version)>` |
| 12 | `evidence_namespace_rules` | `tuple[tuple[Identifier, int, int, int], ...]` | yes | `(namespace_prefix, minimum, maximum, decimal_width)` generates `prefix + "-" + zero_padded_number`; integers exclude bool, use $0\ldots2^{53}-1$, minimum $\le$ maximum, width $1\ldots15$; prefixes unique/sorted | `Vec<(Identifier,u64,u64,u8)>` |
| 13 | `evidence_scope_rules` | `tuple[tuple[OwnershipScope, Identifier, tuple[Identifier, ...]], ...]` | yes | `(module_scope, required_marker, allowed_namespace_prefixes)`; scopes nonoverlapping, namespace prefixes nonempty/sorted and declared above | `Vec<(OwnershipScope,Identifier,Vec<Identifier>)>` |
| 14 | `protected_unowned_functions` | `tuple[tuple[ResourcePath, Identifier], ...]` | yes | exact unique sorted `(module_path, test_function_name)` warnings for demonstrated migration debt | `Vec<(ResourcePath,Identifier)>` |
| 15 | `pytest_markers` | `tuple[Identifier, ...]` | yes | unique, strictly sorted marker inventory containing every scope-rule marker; may be empty only when scope rules are empty | `Vec<Identifier>` |
| 16 | `filename_policy_id` | `Identifier | None` | yes | provenance identity for local-only filename validation; generic evidence auditing does not interpret it | `Option<Identifier>` |
| 17 | `checkpoint_unresolved_statuses` | `tuple[Identifier, ...]` | yes | nonempty unique sorted local vocabulary | `Vec<Identifier>` |
| 18 | `checkpoint_resolved_statuses` | `tuple[Identifier, ...]` | yes | nonempty unique sorted and disjoint from unresolved statuses | `Vec<Identifier>` |
| 19 | `task_active_statuses` | `tuple[Identifier, ...]` | yes | nonempty unique sorted local vocabulary | `Vec<Identifier>` |
| 20 | `task_blocked_statuses` | `tuple[Identifier, ...]` | yes | nonempty unique sorted and disjoint from active statuses | `Vec<Identifier>` |
| 21 | `task_satisfied_statuses` | `tuple[Identifier, ...]` | yes | unique sorted; disjoint from active/blocked | `Vec<Identifier>` |
| 22 | `compatibility_adapter_version` | `Version | None` | yes | explicit local adapter revision, including P1 v1 support when selected | `Option<Version>` |
| 23 | `local_extension_ids` | `tuple[Identifier, ...]` | yes | unique sorted allowed local extensions | `Vec<Identifier>` |

The profile contains data only. Runtime roots are deliberately not serialized;
they are separate action arguments. Unknown fields and unsupported schema or
contract versions are errors. Profile compatibility requires an equal supported closed schema and public-contract integer versions; additive fields require a new profile
schema version because v1 rejects unknown fields. Closures, callables, code
strings, credentials, environment snapshots, mutable clients, Git clients,
subprocess/scheduler handles, task objects, CPN/SNAKES/QE/Wannier/operator
objects, and implicit `.pi` locations are prohibited.

### `SkillDescriptor`

Role: DataObject. Public JSON: yes.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | `1` | `u64` |
| 2 | `skill_id` | `Identifier` | yes | opaque skill identity | `Identifier` |
| 3 | `behavior_version` | `Version` | yes | skill behavioral version | `Version` |
| 4 | `entry_resource_id` | `Identifier` | yes | one manifest `skill` resource | `Identifier` |
| 5 | `trigger_capability_ids` | `tuple[Identifier, ...]` | yes | nonempty unique sorted capabilities | `Vec<Identifier>` |
| 6 | `required_resource_ids` | `tuple[Identifier, ...]` | yes | nonempty unique sorted closure including entry | `Vec<Identifier>` |
| 7 | `side_effect_class` | `str` | yes | `read_only`, `local_write`, or `external_effect` | `SideEffectClass` enum |
| 8 | `authorization_policy_id` | `Identifier` | yes | declared policy identity governing invocation; validated against manifest closure, never implicitly loaded | `Identifier` |
| 9 | `retry_policy` | `str` | yes | `none` or `explicit_authorization_only` | `SkillRetryPolicy` enum |
| 10 | `termination_policy` | `str` | yes | exactly `stop_after_result` in v1 | `SkillTerminationPolicy` enum |

A descriptor neither dispatches an agent nor grants authorization. Ambient skill
inheritance and global fallback are excluded unless a local profile names a
resource and policy explicitly.

### `OwnershipScope` and `AgentDescriptorView`

Both are DataObjects with public JSON and are included only because current
version-2 ownership manifests and agent records demonstrate their use.

`OwnershipScope` fields in order are `schema_version: int = 1`,
`path: OwnershipScopePath`, and `scope_kind: str`, where `scope_kind` is exactly
`file` or `directory_tree`. The path uses the serialized path character and
segment rules but may denote a file or directory prefix and never has a trailing
slash. A `file` scope contains exactly that path. A `directory_tree` scope
contains the named path and every path with the exact prefix `path + "/"`.
Two scopes overlap when either contains the other's path. Comparison is exact,
case-sensitive, lexical POSIX comparison followed by explicit-root symlink and
resolved-confinement validation when bound to a runtime root. Rust mapping is
`struct OwnershipScope { schema_version: u64, path: OwnershipScopePath,
scope_kind: OwnershipScopeKind }`.

`AgentDescriptorView` fields in order are `schema_version: int = 1`,
`agent_id: Identifier`, and `acceptance_role: str`, where the role is exactly
`writer` or `read_only`. It contains no frontmatter bytes, prompt, tools, skills,
paths, mutable client, or dispatch behavior. A project-local adapter owns parsing
current agent files into this normalized view. Rust mapping is
`struct AgentDescriptorView { schema_version: u64, agent_id: Identifier,
acceptance_role: AcceptanceRole }`.

### `OwnershipManifestView`

Role: DataObject. Public JSON: yes. It is the generic version-2 normalized view;
legacy version-1 P1 data is transformed only by a local compatibility adapter.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | `1` for this view | `u64` |
| 2 | `task_id` | `Identifier` | yes | task identity | `Identifier` |
| 3 | `task_record_path` | `ResourcePath` | yes | explicit task-record reference | `ResourcePath` |
| 4 | `writers` | `tuple[tuple[Identifier, Identifier, tuple[OwnershipScope, ...]], ...]` | yes | `(role, agent, owned_scopes)`; nonempty; role/agent unique; each scope set nonempty, sorted by path/kind, and internally nonoverlapping | `Vec<(Identifier,Identifier,Vec<OwnershipScope>)>` |
| 5 | `reviewers` | `tuple[tuple[Identifier, Identifier], ...]` | yes | `(role, agent)`; nonempty; roles and agents unique and disjoint from writers | `Vec<(String,String)>` |
| 6 | `completion_validator_path` | `ResourcePath` | yes | one writer-owned validator file | `ResourcePath` |
| 7 | `completion_command` | `tuple[str, ...]` | yes | nonempty argv; structural execution identity only | `Vec<String>` |
| 8 | `orchestration_profile_id` | `Identifier | None` | yes | optional declared local profile identity | `Option<Identifier>` |

Canonical writer/reviewer order is role then agent. Owned scopes are canonical
and pairwise nonoverlapping across writers. Agent frontmatter, `.pi` discovery,
P1 object kinds, exact test filenames, evidence branch authorization, command
execution, dispatch, and review acceptance are excluded from the generic view.

### `CheckpointRecord`

Role: DataObject. Public JSON: yes. It is a narrow view, not a replacement for
current project checkpoint files.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | generic view version `1` | `u64` |
| 2 | `checkpoint_id` | `Identifier` | yes | durable checkpoint identity | `Identifier` |
| 3 | `task_id` | `Identifier | None` | yes | linked task when present | `Option<Identifier>` |
| 4 | `episode_id` | `Identifier | None` | yes | linked episode when present | `Option<Identifier>` |
| 5 | `status` | `Identifier` | yes | opaque profile-interpreted lifecycle value | `Identifier` |
| 6 | `decision_class` | `Identifier | None` | yes | opaque profile-interpreted decision class | `Option<Identifier>` |
| 7 | `created_at` | `str | None` | yes | RFC 3339 UTC text when present; no implicit current time | `Option<String>` |
| 8 | `question` | `str | None` | yes | human-facing text | `Option<String>` |
| 9 | `options` | `tuple[tuple[Identifier, str, str | None], ...]` | yes | unique option IDs in declared presentation order | `Vec<(Identifier,String,Option<String>)>` |
| 10 | `human_response` | `str | None` | yes | immutable response text when supplied | `Option<String>` |
| 11 | `normalized_decision` | `str | None` | yes | recorded normalization, never inferred by generic code | `Option<String>` |
| 12 | `resolved_at` | `str | None` | yes | RFC 3339 UTC text when present | `Option<String>` |
| 13 | `authorized_scope` | `str | None` | yes | recorded project-local scope text | `Option<String>` |
| 14 | `record_paths` | `tuple[ResourcePath, ...]` | yes | unique sorted references | `Vec<ResourcePath>` |
| 15 | `resumption_status` | `Identifier | None` | yes | recorded fact, not an instruction | `Option<Identifier>` |

`ValidateCheckpointSet` applies this exact profile-relative state table:

| Status membership | Required non-null/nonempty fields | Required null fields |
| --- | --- | --- |
| `checkpoint_unresolved_statuses` | `question`; `options` has at least one unique option | `human_response`, `normalized_decision`, `resolved_at`, `authorized_scope` |
| `checkpoint_resolved_statuses` | `human_response`, `normalized_decision`, `resolved_at`, `authorized_scope` | none |
| neither or both sets | invalid status/state | not applicable |

`record_paths` may be empty while pending and is profile/project content rather
than a durability claim. `resumption_status` is never used to infer mutation.
RFC 3339 fields must use a `Z` UTC suffix and a syntactically valid calendar
time. Generic code cannot select an option, infer acceptance from silence, write
the human response, resume work, mutate Git, activate a successor, or interpret
scientific meaning.

### `TaskReference`

Role: DataObject. Public JSON: yes.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | `1` | `u64` |
| 2 | `task_id` | `Identifier` | yes | opaque task identity | `Identifier` |
| 3 | `record_path` | `ResourcePath` | yes | explicit task-record reference | `ResourcePath` |
| 4 | `task_prerequisite_ids` | `tuple[Identifier, ...]` | yes | unique sorted task IDs; no self-reference | `Vec<Identifier>` |
| 5 | `external_prerequisite_ids` | `tuple[Identifier, ...]` | yes | unique sorted opaque external-condition IDs, disjoint from task IDs | `Vec<Identifier>` |
| 6 | `status` | `Identifier` | yes | opaque profile-interpreted state | `Identifier` |
| 7 | `explicit_activation_required` | `bool` | yes | declared activation fact, never inferred from prose | `bool` |

### `ChainView`

Role: DataObject. Public JSON: yes.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | `1` | `u64` |
| 2 | `chain_id` | `Identifier` | yes | opaque chain identity | `Identifier` |
| 3 | `active_task_id` | `Identifier | None` | yes | declared active task, if any | `Option<Identifier>` |
| 4 | `tasks` | `tuple[TaskReference, ...]` | yes | nonempty, unique, strictly sorted by task ID | `Vec<TaskReference>` |
| 5 | `explicitly_activated_task_ids` | `tuple[Identifier, ...]` | yes | unique sorted IDs contained in `tasks` | `Vec<Identifier>` |
| 6 | `production_execution_authorized` | `bool` | yes | declared control-plane fact | `bool` |
| 7 | `package_publication_authorized` | `bool` | yes | declared control-plane fact | `bool` |

The view is not a CPN, workflow engine, task dispatcher, mutable repository, or
scientific state machine.

`EvaluateChainState` derives facts by this exact algorithm after checkpoint-set
and chain validation:

1. Every task prerequisite names a task in the view. Every external prerequisite
   appears in `known_external_prerequisite_ids`; the satisfied-external tuple is
   a subset of the known tuple. Unknown values fail before derivation.
2. A task prerequisite is satisfied exactly when the referenced task status is
   in `profile.task_satisfied_statuses`. An external prerequisite is satisfied
   exactly when it is in `satisfied_external_prerequisite_ids`.
3. `active_task_ids` is exactly the sorted tasks whose status is in
   `task_active_statuses`. It must contain zero or one ID and equal
   `ChainView.active_task_id` (`None` means empty), otherwise validation fails.
4. An unresolved checkpoint blocks only its non-null linked `task_id`. Resolved
   checkpoints do not independently satisfy prerequisites and generic code never
   interprets their decision prose.
5. A non-satisfied task is `ready` exactly when it is not active, has no
   unresolved linked checkpoint, every task/external prerequisite is satisfied,
   and either explicit activation is not required or its ID occurs in
   `explicitly_activated_task_ids`.
6. `blocked_task_ids` contains every non-satisfied task with an unresolved linked
   checkpoint or any unsatisfied prerequisite/required activation. An active task
   at a checkpoint may therefore appear in both active and blocked tuples. A
   declared blocked task whose conditions have all become satisfied appears in
   ready, not blocked.
7. An explicitly activated ID whose task does not declare
   `explicit_activation_required` is `PIH.CHAIN.ACTIVATION_UNEXPECTED`; a required
   activation absent from an otherwise prerequisite-ready task is represented as
   structurally blocked, not an invalid chain. `ACTIVATION_MISSING` is reserved
   for a chain/status declaration that claims the task active despite absent
   required activation.

All three fact tuples are identifier-sorted. A validation failure returns all
three empty.

### `ChecksumEntry` and `ChecksumManifest`

Both are DataObjects with public JSON.

`ChecksumEntry` field order is: `schema_version: int = 1`, `path: ResourcePath`,
`content_identity: ArtifactIdentity`. Paths are unique only in their enclosing
manifest. `ChecksumManifest` field order is only `schema_version: int = 1` and
`entries: tuple[ChecksumEntry, ...]`. Entries are nonempty, path-unique, and
strictly path-sorted. The explicit runtime root is an action argument, not a
serialized root-role or workstation identity. Version 1 adds no unattested
catalog ID/version fields. Checksums claim byte identity only. Root discovery,
scientific correctness, provenance attestation, signatures, and deletion are
excluded.

## Included ResultObjects

### `ValidationIssue`

Public JSON: yes.

| Order | Field | Exact Python type | Required | Invariant and meaning | Rust |
| ---: | --- | --- | --- | --- | --- |
| 1 | `schema_version` | `int` excluding `bool` | yes | `1` | `u64` |
| 2 | `code` | `Identifier` | yes | registered stable issue code | `String`/enum wrapper |
| 3 | `severity` | `str` | yes | `ERROR`, `WARNING`, or `INFO` | `ValidationSeverity` enum |
| 4 | `subject_id` | `Identifier | None` | yes | primary opaque subject | `Option<Identifier>` |
| 5 | `path` | `DiagnosticPath | None` | yes | neutral canonical lexical location when relevant; may denote a regular file, directory, or ownership-scope prefix and makes no existence/file-kind claim | `Option<DiagnosticPath>` |
| 6 | `related_ids` | `tuple[Identifier, ...]` | yes | unique strictly sorted related identities | `Vec<Identifier>` |
| 7 | `message` | `str` | yes | nonempty human-facing explanation; not machine protocol | `String` |

### `ValidationResult`

Public JSON: yes. Fields in order are `schema_version: int = 1`, `status: str`,
and `issues: tuple[ValidationIssue, ...]`. Status is `PASS`, `WARN`, or `FAIL`.
Issues are in the deterministic order defined in
`issue-code-and-ordering-contract.md`. Exact duplicate machine findings are
prohibited. Empty issues mean `PASS`; only `INFO` also means `PASS`; at least one
`WARNING` and no `ERROR` means `WARN`; at least one `ERROR` means `FAIL`.

`PASS` means only that the supplied input satisfies this structural contract. It
does not mean human acceptance, task authorization, numerical verification,
scientific validation, uncertainty quantification, package readiness, command
semantic correctness, or publication readiness.

### Operation-specific results

These concrete ResultObjects prevent unnamed tuple outputs. They are not public
JSON records because they may contain runtime bytes, filesystem paths, or an
exhaustive in-memory record union.

- `ProjectProfileLoadResult(profile: ProjectProfile | None, validation: ValidationResult)`.
- `ResourceResolutionResult(resolved_path: pathlib.Path | None, reference: ResourceReference | None, validation: ValidationResult)`. The path is runtime-only.
- `ChainEvaluationResult(active_task_ids: tuple[Identifier, ...], blocked_task_ids: tuple[Identifier, ...], ready_task_ids: tuple[Identifier, ...], validation: ValidationResult)`.
- `EvidenceIdentifierOccurrence(evidence_id: Identifier, path: ResourcePath, line: int)`, where `line` excludes `bool` and is $1\ldots2^{53}-1$. This is a DataObject with public JSON because its inventory is retained evidence.
- `EvidenceAuditResult(occurrences: tuple[EvidenceIdentifierOccurrence, ...], validation: ValidationResult)`.
- `JsonSerializationResult(payload: bytes | None, content_identity: ArtifactIdentity | None, validation: ValidationResult)`.
- `JsonDeserializationResult(record: HarnessWireRecord | None, validation: ValidationResult)`.

For every operation-specific result, a failed `validation` requires every primary
value to be `None` or the corresponding fact tuple to be empty. Exact equality
covers fields except `ResourceResolutionResult.resolved_path`, whose equality is
not public because it is workstation runtime state. All other results have exact
value equality. Rust uses same-named structs; runtime paths map to
`Option<std::path::PathBuf>`, bytes to `Option<Vec<u8>>`, and the record union to
`Option<HarnessWireRecord>`.

`WireRecordKind` is a public closed Python `Enum` and Rust enum whose string
values are exactly the public-JSON class names in this document.
`HarnessWireRecord` is a public closed Python typing union and Rust tagged
in-memory enum of exactly those record classes. It adds no wire
discriminator: `DeserializeJsonRecord` receives the expected `WireRecordKind`
explicitly. `WireRecordKind` is the closed enum of those exact class names.
Adding a kind requires a new closed integer contract version.

## Exact Rust action boundary

Every ActionObject maps to a zero-sized Rust struct with
`execute(&self, ...) -> Result<ConcreteResult, HarnessInternalError>`. Expected
input invalidity is inside the returned `ValidationResult`; only programming or
post-selection I/O failures use `HarnessInternalError`. Python exports
`HarnessInternalError(RuntimeError)` with immutable public attributes
`operation: Identifier` and `detail: str`; it is not serialized and its message
is not machine protocol. Rust uses
`struct HarnessInternalError { operation: Identifier, detail: String }` and
implements `std::error::Error`. Direct validated Rust constructors use a private nonserialized implementation
enum with `WrongType { field: Identifier }` and
`InvalidValue { field: Identifier, rule_code: Identifier }`, corresponding to
Python `TypeError` and `ValueError`. This private mapping demonstrates concrete
Rust implementability but is not an added public H1 interface.

`Identifier`, `ResourcePath`, `OwnershipScopePath`, `DiagnosticPath`, and
`Version` are validated Rust newtypes, not aliases. Table references to `String` for an opaque identifier
are superseded by this exact `Identifier` newtype; table references to `Path` for
a serialized path mean `ResourcePath`, never `std::path::Path`.
`ValidationIssue.code` is `Identifier`, not an enum;
the registry validates it. Filesystem roots are borrowed `&std::path::Path` and
returned runtime paths are owned `PathBuf`. Serialized bytes are `&[u8]` inputs
and `Vec<u8>` outputs. Immutable Python tuples map to ordered `Vec<T>` values
exposed only through immutable borrowing. `ChecksumEntry`, `ChecksumManifest`,
`ValidationResult`, and all other records map to same-named Rust structs with
fields in the declared order and validated constructors returning `Result<Self,
PrivateConstructorError>`, where that private implementation enum is exactly the
wrong-type/invalid-value mapping above and is not exported by the H1 public
surface.

Serialization uses a fixed exhaustive match over `HarnessWireRecord`; there is
no registry, reflection, plugin, dynamic attribute, or service locator. Both
languages must emit RFC 8785 bytes plus LF and reject duplicate keys before
object construction.

The exact Rust method shapes are:

```text
SerializeJsonRecord::execute(&self, &HarnessWireRecord)
  -> Result<JsonSerializationResult, HarnessInternalError>
DeserializeJsonRecord::execute(&self, WireRecordKind, &[u8])
  -> Result<JsonDeserializationResult, HarnessInternalError>
LoadProjectProfile::execute(&self, &[u8], Option<&ArtifactIdentity>, &[Version], &[Version])
  -> Result<ProjectProfileLoadResult, HarnessInternalError>
ResolveResource::execute(&self, &Identifier, &Path, &ResourceManifest,
  &ArtifactIdentity, Option<&Path>, Option<&ResourceManifest>,
  Option<&ArtifactIdentity>, &ProjectProfile)
  -> Result<ResourceResolutionResult, HarnessInternalError>
ValidateResourceManifest::execute(&self, &ResourceManifest, &ArtifactIdentity,
  Option<&ResourceManifest>, Option<&ArtifactIdentity>, &ProjectProfile)
  -> Result<ValidationResult, HarnessInternalError>
ValidateOwnershipManifest::execute(&self, &OwnershipManifestView, &ChainView,
  &[AgentDescriptorView], &ProjectProfile)
  -> Result<ValidationResult, HarnessInternalError>
ValidateCheckpointSet::execute(&self, &[CheckpointRecord], &[Identifier], &ProjectProfile)
  -> Result<ValidationResult, HarnessInternalError>
EvaluateChainState::execute(&self, &ChainView, &[CheckpointRecord],
  &[Identifier], &[Identifier], &ProjectProfile)
  -> Result<ChainEvaluationResult, HarnessInternalError>
AuditEvidenceIdentifiers::execute(&self, &[(ResourcePath, Vec<u8>)], &ProjectProfile)
  -> Result<EvidenceAuditResult, HarnessInternalError>
ValidateChecksumManifest::execute(&self, &Path, &ChecksumManifest)
  -> Result<ValidationResult, HarnessInternalError>
ValidateSkillResources::execute(&self, &[SkillDescriptor], &ResourceManifest,
  &ArtifactIdentity, Option<&ResourceManifest>, Option<&ArtifactIdentity>,
  &ProjectProfile)
  -> Result<ValidationResult, HarnessInternalError>
```

`Path` above is `std::path::Path`. The Python signatures in
`contract-surface.md` are normative for Python and correspond positionally to
these Rust shapes. Rust enums own every field declared as a closed string enum;
opaque machine identifiers use `Identifier`, human prose uses `String`, and
optional fields use `Option<T>`. There is no platform-dependent serialized path.

## Deferred and local-only records

`DeterministicCommandSpecification` and `DeterministicCommandResult` are deferred.
H1 freezes no command wire fields, runner, environment-capture format, or shell
semantics. Any future contract must use argv rather than trusted shell
interpolation, exclude credential-bearing environment entries, represent
nonzero exit status structurally, and state that command success is not semantic
correctness.

`DecisionBoundaryResult` is local compatibility only. A future local record must
separate immutable decision content, durability result, commit identity, branch
and remote identity, push status, and partial effects. It may not contain a Git
client or authorize mutation. H1 defines no generic fields or wire version for
it.

## Prohibited runtime contents

No included record or result may contain credentials, secret-bearing environment
values, open files, sockets, subprocess or scheduler handles, Git clients,
mutable service clients, closures, imported project-domain objects, live SNAKES
objects, or mutable mappings/sequences. Runtime `pathlib.Path` values occur only
as explicit action arguments or nonserialized resolution outputs; serialized
resource and ownership records retain `ResourcePath` and `OwnershipScopePath`
respectively, while `ValidationIssue.path` alone uses neutral `DiagnosticPath`.
