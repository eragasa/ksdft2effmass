# H1 proposed public contract surface

## Boundary and authority

This document proposes the smallest generic surface demonstrated by current
repository consumers. It is a contract artifact for `H1-HC01`, not an
implementation, schema, fixture, package, or authorization to execute work.
Existing scripts remain requirement evidence and current authority until H4
shadow parity and human cutover.

The proposed Python public contract version is `1`. The incubation import path
for a later H2 implementation is `ksdft2effmass.harness.pi`; H1 creates no such
path. The future standalone import and distribution names are deferred to
optional H5.

## Exact proposed public API

### DataObjects

```text
ArtifactIdentity
ResourceReference
ResourceManifest
ProjectProfile
SkillDescriptor
OwnershipScope
AgentDescriptorView
EvidenceIdentifierOccurrence
OwnershipManifestView
CheckpointRecord
TaskReference
ChainView
ChecksumEntry
ChecksumManifest
```

### ResultObjects

```text
ValidationIssue
ValidationResult
ProjectProfileLoadResult
ResourceResolutionResult
ChainEvaluationResult
EvidenceAuditResult
JsonSerializationResult
JsonDeserializationResult
```

### Public support types and error

```text
WireRecordKind              closed enum of every public-JSON record class name
HarnessWireRecord           closed typing union of those record classes
HarnessInternalError        nonserialized internal/programming-failure error
```

### Stateless ActionObjects

```text
SerializeJsonRecord
DeserializeJsonRecord
LoadProjectProfile
ResolveResource
ValidateResourceManifest
ValidateOwnershipManifest
ValidateCheckpointSet
EvaluateChainState
AuditEvidenceIdentifiers
ValidateChecksumManifest
ValidateSkillResources
```

There are no abstract DataObject, ResultObject, ActionObject, or Workflow base
classes. Every action is a fieldless/stateless concrete class with an `execute`
method and may retain no root, profile, cache, client, or mutable state. Exact
record fields, field order, invariants, JSON behavior, equality, and Rust mapping
are in [field-and-wire-contract.md](field-and-wire-contract.md).

## Action contracts

Expected invalidity always returns a `ValidationResult`; it does not raise a
catch-all validation exception. Wrong direct Python argument types may raise
`TypeError`. A violated internal assertion, impossible state produced by the
implementation itself, I/O race after validated selection, or other programming
failure may raise a documented implementation exception and is not converted to
`PASS`, `WARN`, or a misleading input issue.

| Action and exact `execute` input | Exact output | Expected invalidity | Side effects | Ordering and local policy | Explicit exclusions |
| --- | --- | --- | --- | --- | --- |
| `SerializeJsonRecord.execute(record: HarnessWireRecord)` | `JsonSerializationResult` | A value outside the closed union is the wrong Python semantic type and raises `TypeError`; a valid record returns `PASS`, bytes, and identity; impossible bypassed internal invalidity raises `HarnessInternalError`. | In-memory encoding and hashing only. | Exhaustive closed record union; RFC 8785 plus LF. | No reflection, registry, plugin, file I/O, or semantic attestation. |
| `DeserializeJsonRecord.execute(record_kind: WireRecordKind, payload: bytes)` | `JsonDeserializationResult` | UTF-8/JSON/duplicate-key/field/type/invariant/version failure returns `FAIL` and no record. | In-memory parsing only. | Explicit closed record kind selects one exact constructor. | No inferred kind, dynamic import, schema discovery, partial object, or hidden migration. |
| `LoadProjectProfile.execute(profile_bytes: bytes, expected_identity: ArtifactIdentity | None, supported_schema_versions: tuple[Version, ...], supported_contract_versions: tuple[Version, ...])` | `ProjectProfileLoadResult` | Invalid UTF-8/JSON, duplicate or unknown fields, identity mismatch, malformed values, or unsupported versions return a result with `profile = None` and `FAIL`. | None; no file I/O. | Issues use common order. Caller supplies allowed versions and optional expected bytes identity. | No path, environment, package-resource, `.pi`, Git-root, or current-directory discovery. |
| `ResolveResource.execute(resource_id: Identifier, generic_root: pathlib.Path, generic_manifest: ResourceManifest, generic_manifest_identity: ArtifactIdentity, local_root: pathlib.Path | None, local_manifest: ResourceManifest | None, local_manifest_identity: ArtifactIdentity | None, profile: ProjectProfile)` | `ResourceResolutionResult`; its `Path` is runtime-only and not serialized. | Unknown/duplicate ID, manifest mismatch, incompatible version, path invalidity, missing/non-file resource, symlink, or hash mismatch returns no selected path/reference and `FAIL`. | Read-only filesystem metadata and file-byte hashing below explicit roots. | Generic and local manifests are validated first. Local is extension-only; no replacement or fallback. | No ambient global fallback, network, installation, dispatch, execution, writes, or directory resource. |
| `ValidateResourceManifest.execute(generic_manifest: ResourceManifest, generic_manifest_identity: ArtifactIdentity, local_manifest: ResourceManifest | None, local_manifest_identity: ArtifactIdentity | None, profile: ProjectProfile)` | `ValidationResult` | Reports malformed structure, duplicate identity/path, dependency absence/cycle, generic-to-local dependency, wrong base, forbidden replacement, or unsupported kind/version. | None. | Resource IDs, paths, then dependency edges. Profile supplies supported extensions and policy references. | Does not resolve files or authorize resources. |
| `ValidateOwnershipManifest.execute(manifest: OwnershipManifestView, chain: ChainView, agents: tuple[AgentDescriptorView, ...], profile: ProjectProfile)` | `ValidationResult` | Reports identity mismatch, missing/duplicate normalized agent, role mismatch, scope invalidity/overlap, non-independent reviewer, invalid completion binding, and unsupported profile. | None. | Agents and scopes sort exactly. A local adapter parses project agent format and v1 compatibility before this generic call. | No raw frontmatter parsing, `.pi` lookup, dispatch, command execution, P1 inventory, test filename rule, acceptance, or repair. |
| `ValidateCheckpointSet.execute(checkpoints: tuple[CheckpointRecord, ...], task_ids: tuple[Identifier, ...], profile: ProjectProfile)` | `ValidationResult` | Reports duplicate IDs, invalid status/value combinations, unknown linked task IDs, contradictory resolution fields, and duplicate normalized decisions for one checkpoint identity. | None. | Checkpoints sorted by ID; profile supplies lifecycle vocabulary. | Does not choose/normalize a decision, infer silence, write records, resume tasks, mutate Git, or activate successors. |
| `EvaluateChainState.execute(chain: ChainView, checkpoints: tuple[CheckpointRecord, ...], known_external_prerequisite_ids: tuple[Identifier, ...], satisfied_external_prerequisite_ids: tuple[Identifier, ...], profile: ProjectProfile)` | `ChainEvaluationResult` representing active, blocked, and structurally ready task IDs. | Cycles, duplicates, missing prerequisites, active-task contradictions, unauthorized explicit-activation facts, or inconsistent status vocabulary return empty fact tuples and `FAIL`. | None. | Each output tuple is identifier-sorted. Profile supplies lifecycle vocabulary; task and external prerequisite fields are distinct; caller supplies the complete known external-condition set and its satisfied subset. | Does not activate, dispatch, resume, mutate state/Git, choose a human decision, or interpret scientific task meaning. “Ready” is a structural fact, not authorization. |
| `AuditEvidenceIdentifiers.execute(modules: tuple[tuple[ResourcePath, bytes], ...], profile: ProjectProfile)` | `EvidenceAuditResult` containing occurrences with ID, path, and one-based line. | Invalid Python source, undeclared marker, identifier outside explicit namespace/range rules, duplicate/range conflict, or protected-gap mismatch yields deterministic findings. Exact protected IDs are profile data and cannot be silently weakened. | None; parses supplied bytes only. | Occurrences sort by ID, path, line. Profile supplies complete module-scope-to-marker/namespace rules and exact protected `(module_path, test_function)` gaps. | No filesystem discovery, filename-policy interpretation, test execution, AST mutation, scientific/VVUQ judgment, or automatic migration; filename checks remain local. |
| `ValidateChecksumManifest.execute(root: pathlib.Path, manifest: ChecksumManifest)` | `ValidationResult` | Invalid root/path, duplicate, missing/non-file, symlink, algorithm/digest error, or byte mismatch yields `FAIL`. | Read-only filesystem metadata and hashing below explicit root. | Entries and issues sort by canonical path. | No deletion, repair, provenance attestation, semantic correctness, or scientific claim. |
| `ValidateSkillResources.execute(descriptors: tuple[SkillDescriptor, ...], generic_manifest: ResourceManifest, generic_manifest_identity: ArtifactIdentity, local_manifest: ResourceManifest | None, local_manifest_identity: ArtifactIdentity | None, profile: ProjectProfile)` | `ValidationResult` | Duplicate skill, missing entry/closure, undeclared dependency, wrong resource kind, incompatible behavior/policy, or forbidden overlay yields findings. | None after caller supplies records; resource byte checking is owned by `ResolveResource`/checksum validation. | Skills sort by ID and closure resource ID. Profile supplies allowed local extensions and policy identities. | No dispatch, inheritance, automatic global fallback, agent mutation, retry, or authorization grant. |

Clean-revision validation and optional local pre-commit worktree checking are
separate invocations with separately recorded explicit roots and identities. A
pre-commit result cannot replace the clean-revision result and cannot consume
personal or concurrently edited working notes.

## Demonstrated-consumer rule

`interface-decision-matrix.json` names at least one current consumer for every
included interface. The supporting `OwnershipScope`, `AgentDescriptorView`,
`EvidenceIdentifierOccurrence`, and operation-specific ResultObjects are included
only where current ownership, JSON, chain, resource, or evidence-audit consumers
demonstrate them. `field_and_argument_consumer_evidence` in the matrix traces the
mandatory field/argument groups. New convenience aliases, open generic result
wrappers, registries, factories, repositories, services, protocols, plugins,
dispatchers, runners, and workflow engines are deferred or rejected.

## Generic/local capability ownership

Exactly one cell marked **PRIMARY** owns each accepted capability. Other cells
show adapters, instances, runtime input, explanation, or retained history.

| Capability | Generic Python | Local Python | Generic resource | Local resource | Runtime `.pi` state | Maintained docs | Historical evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Artifact/resource identity records | **PRIMARY** | adapter only | accepted schema later | profile extension | instance/evidence input | explanation | retained catalogs |
| Resource manifest and extension-only resolution rules | **PRIMARY** | root composition later | accepted manifest/schema instances later | local extension manifest later | no package contents | explanation | H0 requirement evidence |
| Project profile record contract | **PRIMARY** | construction/loading adapter later | profile schema later | **instance only** | explicit caller input only | explanation | hard-coded validator evidence |
| Skill descriptor record contract | **PRIMARY** | routing adapter later | **accepted descriptor instances** | local descriptor extensions | current skill/agent state remains local | explanation | current skill inventory |
| Validation issue/result model and ordering | **PRIMARY** | separate local diagnostic types only | issue-code policy reference later | no generic local-code extension in v1 | retained results | explanation | validator prose/results |
| Ownership v2 structural validation | **PRIMARY** | v1/P1 and agent-format compatibility | generic schema later | project ownership profile later | manifests remain instantiated state | explanation | current validator and fixtures |
| Checkpoint structural validation | **PRIMARY** | lifecycle/durability/resumption policy | generic record schema later | local vocabulary later | checkpoint decisions **remain authoritative here** | explanation | validator/fixtures |
| Task/chain structural evaluation | **PRIMARY** | local chain adapters | generic view schema later | local lifecycle vocabulary | task/chain activation **remains authoritative here** | explanation | H0 assertions |
| Evidence-ID AST mechanics | **PRIMARY** | local protected/migration adapter | generic grammar reference later | prefixes/markers/filename rules | task evidence | accepted grammar explanation | current auditor/P1 replay |
| Checksum structural validation | **PRIMARY** | local root selection/exclusions | generic checksum schema later | local catalogs/policy | task catalogs/evidence | explanation | historical catalogs |
| Decision-boundary durability and Git facts | no owner | **PRIMARY** | none | Git policy/procedure | decision evidence and checkpoints | explanation | prior resolution records |
| Command specification/result records | deferred | current task-local only | none | none | current task evidence | explain deferral | heterogeneous manifests/results |
| Evidence-writing grammar | no duplicate implementation | local/domain extensions only | **PRIMARY** accepted resource derived from `document-research-python` in H3 | marker/namespace/domain extension | no generic package contents | maintained explanation | existing accepted skill remains authority until cutover |
| `class_owned`/`artifact_owned` primary evidence kinds | structural support later | legacy compatibility only | **PRIMARY** grammar contract | local filename/surface policy | manifests/evidence | maintained explanation | P1 `boundary_owned` retained unchanged |

Dependency direction is normative:

```text
local Python -> generic Python
local resources -> generic resource contracts
generic Python -/-> local Python
generic resources -/-> project-local identifiers
runtime .pi state -/-> generic package contents
```

## Evidence ownership

The generic primary kinds are exactly `class_owned` and `artifact_owned`.
Technical agreement or direction is one artifact-owned relation with metadata:

```text
relation_kind
left_side_id
right_side_id
direction
```

For version 1, `relation_kind` is one of `intrinsic`, `agreement`,
`directional_mapping`, or `package_surface`; `direction` is `none`,
`left_to_right`, or `right_to_left`. `intrinsic` and `package_surface` require
`direction = none`; `agreement` requires two named sides and `none`;
`directional_mapping` requires two named sides and a non-`none` direction.
These are artifact relation metadata, not a third ownership kind or a mandatory
Python class. Legacy P1 `boundary_owned` remains local compatibility input and
its historical files and test names are unchanged.

## Rejected and excluded surfaces

H1 rejects a generic Workflow engine, subprocess or Git mutation service,
plugin/registry/service-locator/dispatch framework, Graphify integration, a
third `boundary_owned` primary kind, and a duplicate evidence-writing grammar.
It also excludes package/CLI identity, QE, Wannier90, SNAKES, operator records,
scientific validation/UQ result types, package installation/publication, and
universal filename rules.
