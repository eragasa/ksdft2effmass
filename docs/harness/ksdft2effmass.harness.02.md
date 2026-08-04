# PI Harness Contract and Versioning

## Contract status

H1 is active after resolved `H1-HC01` Option B for exactly one bounded
`DiagnosticPath` contract correction and return to final human acceptance. The
detailed decision artifacts are retained under
`.pi/evidence/pi-harness-incubation/H1/`. This page is maintained explanation;
`.pi` task, chain, and checkpoint records remain the authority for execution
state.

The corrected contract is not implemented. H1 creates no Python namespace,
resource root, schema, fixture, package, runner, or dispatch mechanism. It awaits
a separate final H1 human-acceptance checkpoint, and acceptance would not
activate H3.

## Proposed version-1 public surface

The smallest demonstrated DataObject surface is:

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

The ResultObjects are:

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

The public support surface also includes the closed `WireRecordKind` enum,
closed `HarnessWireRecord` typing union and nonserialized
`HarnessInternalError` for unexpected internal/runtime failures. A private Rust
constructor-error mapping corresponds to Python `TypeError`/`ValueError`; it is
not an additional public interface.

The stateless ActionObjects are:

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

Existing validators, skills, schemas, fixtures, and state records demonstrate
requirements; they are not automatically this API. Every included interface has
a named current consumer, exact fields or arguments, structured failure
behavior, a version owner, a Rust representation, and an explicit exclusion
boundary in the retained H1 contract.

`DeterministicCommandSpecification` and `DeterministicCommandResult` are deferred
because current task artifacts do not demonstrate one stable cross-task wire
contract and H1 includes no runner. `DecisionBoundaryResult` remains local
compatibility because its demonstrated consumer is inseparable from project Git
durability policy. Generic workflow engines, subprocess/Git mutation services,
plugin or dispatch frameworks, Graphify integration, and a third evidence
ownership kind are rejected.

## Object and action separation

Records are immutable concrete DataObjects. Findings and aggregate outcomes are
immutable ResultObjects. Validation, loading, resource resolution, and auditing
are stateless concrete ActionObjects. There are no abstract base classes and no
production Workflow invented to own integration evidence.

For an action $V$ acting on explicit records $x$, profile $p$, and roots or
bytes $r$,

$$
V(x,p,r) \longrightarrow R,
$$

where $R$ contains structured deterministic findings. The action does not infer
state from the current directory, Git, `.pi`, environment defaults, or package
fallback.

## Identity and serialization

Version-1 opaque identifiers are nonempty case-sensitive ASCII strings. They are
not normalized and generic code infers no semantic hierarchy from them.
The three serialized path semantics are immutable built-in Python `str` values
with validated Rust newtypes. `ResourcePath` is an NFC Unicode, root-relative
POSIX regular-file resource path. `OwnershipScopePath` identifies a file or
directory-tree ownership scope. `DiagnosticPath` is the neutral lexical location
used only by diagnostics; it may identify a regular file, directory, or scope
prefix and makes no existence or regular-file claim. All reject empty/absolute
paths, `.`, `..`, empty segments, repeated separators, trailing slashes,
backslashes, Windows drive/device/UNC forms, controls, non-NFC input, and
platform-dependent case folding.

Every serialized record is strict UTF-8 JSON with fixed field names, required
fields, explicit `null` only for declared optional values, duplicate-key and
unknown-field rejection, Boolean exclusion from integer fields, deterministic
array rules, and RFC 8785 canonical output plus one LF. Named serializer and
deserializer ActionObjects own the wire operation; DataObjects do not serialize
themselves. H1 provides field tables and draft wire
rules; H3 owns accepted schemas and fixtures.

`ArtifactIdentity` accepts SHA-256 only in version 1 and requires lowercase
64-character hexadecimal digest text. It identifies exact bytes only. Equal
content digests do not claim semantic equivalence, scientific correctness,
provenance, or human acceptance.

## Resource resolution

A caller supplies one explicit generic root and manifest and, optionally, one
explicit local root and manifest. The profile names expected manifest identities
but contains no workstation root.

The sole proposed version-1 overlay policy is `extend_only`:

- local resources may extend generic resources;
- local resources may depend on generic resources;
- generic resources cannot depend on local resources;
- local resources cannot replace a generic identity or path;
- duplicates fail even when hashes match;
- no ambient global fallback exists.

Resolution checks lexical and resolved confinement, exact component case,
absence of symlinks, regular-file type, dependency/version compatibility, and
selected byte identity. A resolved `pathlib.Path` is runtime-only and never
serialized as durable identity.

## Project profile

The proposed profile is strict, data-only configuration. It binds generic/local
manifest IDs and versions; actions separately receive and verify canonical-JSON
SHA-256 identities to avoid a circular local-manifest/profile hash. It also
represents policy references, complete supported resource/skill version pairs, evidence
namespace/range generation plus module-scope marker/namespace rules and exact
protected unowned `(module_path, test_function)` gaps, pytest markers, a local-only
filename-policy identity, checkpoint/task lifecycle vocabularies,
compatibility-adapter version, and permitted local extension identities. It contains no credentials, closures,
clients, handles, executable services, local domain objects, or implicit `.pi`
path.

Project instances may name `ksdft2effmass` values. The generic contract and
generic resources may not embed the project name, local task IDs, CPN, SNAKES,
QE, Wannier90, operator, evidence-prefix, marker, filename, Git, or scientific
semantics.

## Structured validation

A `ValidationIssue` contains stable code, severity, subject identity, neutral
`DiagnosticPath | None`, related identities, and a human message. This permits
machine-readable findings for both regular-file resources and directory-tree
ownership scopes without weakening or mislabeling the specialized source path
types. The machine protocol is the code and structured fields, not message
prose. Severities are `ERROR`, `WARNING`, and
`INFO`; result states are `FAIL`, `WARN`, and `PASS`.

Issues sort by severity, code, subject, path, related identities, then message.
Exact duplicate machine findings are coalesced. Empty results and all-info
results are `PASS`; warnings without errors are `WARN`; any error is `FAIL`.
Expected invalid input produces structured failure and no partially trusted
primary result. Internal programming failures remain exceptions.

A validation `PASS` establishes structural software-contract conformance only.
It grants no human acceptance, task authorization, successor activation,
command correctness, numerical verification, scientific validation, uncertainty
quantification, package readiness, release, or publication.

## Evidence ownership

The generic primary evidence kinds are exactly:

```text
class_owned
artifact_owned
```

A technical agreement or direction remains `artifact_owned` and carries
relation metadata such as `relation_kind`, `left_side_id`, `right_side_id`, and
`direction`. Legacy P1 `boundary_owned` remains unchanged local compatibility
input. H1 creates no generic third kind, mandatory `test_boundary__...` surface,
or fake Workflow.

## Independent version boundaries

The contract keeps these axes independent:

1. Python public contract;
2. serialized record contract;
3. project-profile schema;
4. resource-manifest schema;
5. skill behavioral version;
6. local compatibility-adapter version;
7. future implementation/package release version.

Unknown fields and unsupported closed integer versions are rejected. Field addition/removal,
type/nullability change, issue-code meaning/order change, relaxed path safety,
hidden discovery, or replace-capable overlays require an explicit new contract
boundary. A profile revision is not a Python API or package version.

## Generic/local ownership

The dependency direction is:

```text
local Python -> generic Python
local resources -> generic resource contracts
generic Python -/-> local Python
generic resources -/-> project-local identifiers
runtime .pi state -/-> generic package contents
```

Generic Python owns structural records, stateless actions, path/resource safety,
and structured results. Local Python owns compatibility, composition, lifecycle
and Git policy. H3 generic resources own the accepted evidence grammar and wire
resources; local resources own project instances and extensions. `.pi` retains
instantiated tasks, chains, checkpoints, decisions, and evidence. Maintained docs
explain but do not activate.

## Successor ownership

The exact proposed successor order is H3, then H2, then H4. H3 alone creates
accepted textual resources under `harness/pi/` and `harness/local/`; it creates
no production Python. H2 alone implements generic Python under
`python/src/ksdft2effmass/harness/pi/` and class/artifact software evidence under
the accepted test root; it creates no `local/` Python. H4 owns all project-local
Python integration, shadow replay, parity comparison, cutover, rollback, and
retirement proposals.

Each successor requires a separate activation and validated version-2 ownership
manifest with nonoverlapping writers, a manifest-bound completion validator, and
independent read-only review. H1 creates none of those successor manifests or
agent records.

## Human decision

The human PI resolved `H1-HC01` as Option B: accept the H1 architecture subject
to correction of the diagnostic-path type. The correction changes only
`ValidationIssue.path: ResourcePath | None` to
`ValidationIssue.path: DiagnosticPath | None`, adds the neutral semantic
primitive and intended `DiagnosticPath(String)` Rust newtype, and leaves the
interface count and specialized `ResourcePath`/`OwnershipScopePath` meanings
unchanged. H1 remains active pending final human acceptance; H3 and every
successor remain blocked and inactive.

## Navigation

- [Previous: Architecture and ownership](./ksdft2effmass.harness.01.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Python implementation boundary](./ksdft2effmass.harness.03.md)
