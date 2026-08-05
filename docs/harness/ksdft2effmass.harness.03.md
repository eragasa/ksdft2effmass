# PI Harness Python Implementation Boundary

## Implemented H2 boundary

Active H2 is the in-progress implementation of the accepted version-1 generic
contract at `python/src/ksdft2effmass/harness/pi/`. Resolved `H2-HC01` Option A
is a bounded version-1 pre-acceptance correction: it changes invariant ownership
for resource manifest candidates without adding an interface, issue code, schema
version, or overlay capability. This page states the corrected required public
behavior; it does not claim that every implementation gate already passes. The
corrected H2 boundary remains provisional pending the required review and human
acceptance. The supported public import path during incubation is:

```python
import ksdft2effmass.harness.pi as pi_harness
```

The package contains immutable records and results plus concrete stateless
actions. It is not a workflow engine and does not discover project state. H4
owns all future project-local Python integration under
`python/src/ksdft2effmass/harness/pi/local/`; H2 creates no local adapter or
cutover behavior.

## Exact public surface

The generic public contract has exactly **36 interfaces**. The package also
exports five semantic primitives, giving 41 names in `__all__`. The 36
interfaces are the following.

### DataObjects (14)

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

### ResultObjects (8)

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

### Public support interfaces (3)

```text
WireRecordKind
HarnessWireRecord
HarnessInternalError
```

`WireRecordKind` is the closed enum of the 16 public-JSON record class names.
`HarnessWireRecord` is the corresponding closed typing union and adds no wire
discriminator. `HarnessInternalError` is a nonserialized `RuntimeError` for
unexpected programming or post-selection runtime failure; its immutable public
attributes are `operation` and `detail`.

### ActionObjects (11)

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

The five additional exported semantic primitives are `Identifier`,
`ResourcePath`, `OwnershipScopePath`, `DiagnosticPath`, and `Version`. They are
immutable built-in `str` or `int` values in Python, not additional DataObjects,
ResultObjects, or ActionObjects. The intended Rust boundary uses validated
newtypes for all five.

Users import every public name from the package boundary, not from implementation
modules. For example:

```python
from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    ResolveResource,
    ValidationResult,
    WireRecordKind,
)
```

No abstract DataObject, ResultObject, ActionObject, or Workflow base class is
public or required.

## DataObject, ResultObject, and ActionObject rules

All DataObjects and ResultObjects are operationally immutable, have no dynamic
attributes, retain tuples rather than mutable sequences, and compare by exact
field values in declared field order. The sole exception to public result
equality is the workstation-specific `resolved_path` in
`ResourceResolutionResult`. Runtime `pathlib.Path` values occur only as explicit
action inputs or as that nonserialized result field.

Direct Python construction is strict: the wrong semantic type raises
`TypeError`, while a value of the right semantic type that violates an intrinsic
invariant raises `ValueError`. Boolean values are rejected where an integer is
required; numeric strings are not accepted as numbers. `Version` values are
integers from 1 through $2^{53}-1$, excluding `bool`. Identifiers are nonempty,
case-sensitive ASCII strings with the accepted character grammar and are not
normalized or interpreted as hierarchies.

Every ActionObject is a concrete, fieldless class with an `execute` method. An
action retains no root, profile, cache, repository, client, or mutable state.
Expected malformed external input is represented by deterministic issues in a
result, normally with `FAIL` and no partially trusted primary value. Wrong
direct argument types may raise `TypeError`; impossible internal states and
post-selection I/O races remain exceptions rather than being converted into a
misleading validation result.

## Candidate-record construction and strict wire contract

Construction owns intrinsic validity, not validity of relations among manifest
entries or layers. In particular:

- `ResourceReference` construction checks exact field types, identifier syntax,
  the closed resource-kind value, version bounds, lexical `ResourcePath`, content
  identity, immutable tuple storage, and dependency-ID uniqueness and canonical
  ordering. A dependency equal to the reference's own `resource_id` is retained
  as a representable self-edge.
- `ResourceManifest` construction checks exact field types, manifest identity and
  version, the `generic`/`local` layer, the structural relationship between layer
  and `extends_manifest_id`, a nonempty immutable tuple of
  `ResourceReference`s, and deterministic ordering by the complete represented
  resource key `(resource_id, path, resource_kind, format_version,
  content_identity.algorithm, content_identity.digest, dependency_ids)`.
  Ordering does not deduplicate: repeated IDs, repeated paths, and even exact
  duplicate entries remain present for relational validation.

Consequently, a constructed candidate is intrinsically well formed but is not
thereby an accepted, authorized, resolvable, or capability-valid manifest.

The 16 public-JSON records are the 14 DataObjects plus `ValidationIssue` and
`ValidationResult`. Each is one strict UTF-8 RFC 8259 JSON object with
`schema_version` first in the Python field contract and equal to integer `1`.
Field names, types, nullability, and construction order are fixed. Input rejects:

- invalid UTF-8, a BOM, invalid JSON, unpaired surrogates, and duplicate keys;
- unknown or omitted fields and undeclared `null` values;
- Boolean integer values, numeric strings, nonfinite numbers, and out-of-range
  integers; and
- unsupported versions or violated intrinsic record invariants.

`DeserializeJsonRecord` applies those wire and intrinsic checks and returns no
partial record on their failure. It does not perform manifest-relational
validation. Structurally valid candidates containing a reference self-edge or
duplicate manifest entry IDs/paths therefore deserialize successfully and
preserve those defects for `ValidateResourceManifest`.

Optional fields are present and use JSON `null`; they are never omitted. JSON
member order has no input meaning. Canonical output is RFC 8785 JSON
Canonicalization Scheme bytes, encoded as UTF-8 without a BOM and followed by
exactly one LF byte. Arrays preserve their declared semantic order, while
canonical-set fields are sorted before serialization. There are no floating
point fields. `SerializeJsonRecord` uses the closed union without reflection or
a registry; `DeserializeJsonRecord` requires an explicit `WireRecordKind` and
never infers a kind, discovers a schema, or returns a partial record.

`ArtifactIdentity` supports only SHA-256 with a 64-character lowercase
hexadecimal digest. It states exact byte identity only, not provenance, semantic
equivalence, correctness, or acceptance.

## Three serialized path meanings

`ResourcePath`, `OwnershipScopePath`, and `DiagnosticPath` share strict,
case-sensitive lexical syntax: nonempty NFC Unicode, root-relative POSIX
segments, and no absolute form, empty/`.`/`..` segment, repeated or trailing
separator, backslash, control character, malformed surrogate, or Windows
drive/device/UNC spelling. Invalid input is rejected rather than normalized.
Their meanings remain distinct:

- `ResourcePath` identifies a manifest-root-relative regular-file resource.
- `OwnershipScopePath` identifies a repository-relative file or
  directory-tree declaration whose `OwnershipScope.scope_kind` supplies exact
  containment semantics.
- `DiagnosticPath` is the neutral lexical location in
  `ValidationIssue.path`. It may denote a file, directory, or ownership-scope
  prefix and makes no existence, regular-file, or containment claim.

A validator may preserve the lexical spelling of a valid specialized path in a
diagnostic, but this does not weaken the source type. In particular, a
directory-tree ownership finding is not mislabeled as a resource file.

## Deterministic validation

The version-1 `PIH.<AREA>.<CONDITION>` issue registry is closed. Generic results
cannot contain project-local issue codes. Every registered issue is `ERROR`
except `PIH.EVIDENCE.PROTECTED_GAP`, which is the sole `WARNING`; version 1 has
no registered `INFO` code. Local policy cannot downgrade severity.

The machine duplicate key is `(severity, code, subject_id, path, related_ids)`.
Exact duplicates are coalesced, and issues sort by severity rank, code, optional
subject, optional diagnostic path, related IDs, then message. Sorting is
independent of traversal order, mapping insertion order, hash iteration, locale,
current directory, and host case behavior. Empty or all-info results are
`PASS`; warnings without errors are `WARN`; any error is `FAIL`. Message prose is
explanatory rather than machine protocol.

## Explicit-root manifests and resources

`LoadProjectProfile` consumes supplied bytes, optional expected byte identity,
and explicit supported schema and public-contract version tuples. It performs no
path or environment lookup.

`ResolveResource` receives a resource ID, an explicit absolute generic root,
generic manifest and canonical-byte identity, optional corresponding local
inputs, and a validated project profile. Roots are never serialized. Resolution
validates manifest/profile identity and version compatibility before selection,
then enforces lexical path validity, exact component case, absence of symlink
components, resolved confinement beneath the canonical root, regular-file type,
and exact SHA-256 content identity. Missing, ambiguous, escaped, symlinked,
non-file, case-mismatched, or hash-mismatched resources return no selected path
or reference.

The only version-1 overlay policy is `extend_only`:

```text
local Python -> generic Python
generic Python -/-> local Python
local resources -> generic resource contracts
generic resources -/-> project-local identities
runtime .pi state -/-> generic package contents
```

A local manifest may add identities and depend on its named generic base. It may
not replace or reuse a generic resource ID or path, even when bytes match. A
generic resource may not depend on a local resource. There is no precedence
winner, fallback root, network fetch, installation, current-directory search,
Git-root search, `.pi` discovery, environment expansion, package-resource
fallback, or ambient global skill inheritance.

## Structural actions and their limits

- `ValidateResourceManifest` is the sole owner of relational manifest validity.
  It checks, in accepted stage precedence, manifest/profile identity, canonical
  manifest-byte identity, generic/local presence and base binding; duplicate IDs
  and paths within each manifest; forbidden local reuse of a generic ID or path;
  supported resource kind/format pairs; missing dependencies;
  generic-to-local edges; and dependency cycles, including self-edges. Invalid
  missing or generic-to-local edges are not traversed for a dependent cycle
  finding. Findings use the existing codes
  `PIH.RESOURCE.MANIFEST_MISMATCH`, `DUPLICATE_ID`, `DUPLICATE_PATH`,
  `OVERLAY_REPLACEMENT`, `KIND_UNSUPPORTED`, `VERSION_INCOMPATIBLE`,
  `MISSING_DEPENDENCY`, `GENERIC_TO_LOCAL_DEPENDENCY`, and
  `DEPENDENCY_CYCLE`. Within the intrinsically valid closed resource-kind enum,
  a kind absent from every profile-supported pair is `KIND_UNSUPPORTED`; a kind
  present in the profile at other versions but not at the supplied version is
  `VERSION_INCOMPATIBLE`. A self-edge is `DEPENDENCY_CYCLE`, not a new code,
  and a within-manifest duplicate is capability-specific rather than
  `PIH.ID.DUPLICATE`. Independent findings are collected and then use the
  contract-wide deterministic issue ordering and duplicate coalescing. The
  action neither resolves bytes nor authorizes a resource.
- `ValidateOwnershipManifest` checks the normalized version-2 view against an
  explicit chain, agent views, and profile: task/agent/role agreement,
  nonoverlapping scopes, reviewer independence, completion binding, and profile
  support. H4, not the generic action, owns parsing current agent files and
  legacy P1 compatibility.
- `ValidateCheckpointSet` checks duplicate identities, task links, lifecycle
  vocabulary, unresolved/resolved field combinations, and duplicate normalized
  decisions. It never chooses or normalizes a decision, infers approval from
  silence, writes a checkpoint, resumes work, or activates a successor.
- `EvaluateChainState` derives identifier-sorted active, blocked, and
  structurally ready task facts from an explicit chain, checkpoints, complete
  known external prerequisites, their satisfied subset, and profile vocabulary.
  A failed validation returns empty fact tuples. Readiness is not authorization;
  the action does not dispatch, mutate state or Git, or interpret scientific
  meaning.
- `ValidateChecksumManifest` compares a nonempty, path-sorted manifest with
  regular files confined below an explicit root. Checksums establish byte
  identity only; the action does not repair, delete, attest provenance, or claim
  semantic or scientific correctness.
- `AuditEvidenceIdentifiers` parses only supplied `(ResourcePath, bytes)` Python
  modules. It applies explicit profile marker, namespace/range, scope, and exact
  protected-gap facts and returns occurrences sorted by ID, path, and one-based
  line. It performs no filesystem discovery, test execution, AST mutation,
  filename-policy interpretation, evidence writing, or VVUQ judgment.
- `ValidateSkillResources` first calls `ValidateResourceManifest`. On manifest
  `FAIL` it returns that complete validation result unchanged and performs no
  descriptor or skill-closure interpretation. Only a valid manifest pair reaches
  descriptor uniqueness, closure, entry-kind, behavior-version, and policy
  checks. A `SkillDescriptor` describes triggers, required resources,
  side-effect class, authorization policy, retry policy, and termination policy;
  it neither dispatches an agent nor grants authorization.

`ResolveResource` has the same manifest gate: on manifest `FAIL`, it returns no
`reference` or `resolved_path`, propagates the complete manifest-validation
result, and performs no resource selection or filesystem interpretation. Thus a
relationally invalid candidate cannot reach `NOT_FOUND`, ambiguous-selection,
path, or content-hash processing.

The generic primary evidence kinds remain exactly `class_owned` and
`artifact_owned`. Agreement and direction are artifact relation metadata, not a
third ownership kind. Legacy `boundary_owned` is project-local compatibility
input only.

## H3 resource inputs and vectors

H2 consumes the H3 trees under `harness/pi/` and `harness/local/` read-only.
The corrected resource inputs for resolved `H2-HC01` Option A encode duplicate
ID, duplicate path, and self-dependency cases as successful deserialization
followed by, respectively, `PIH.RESOURCE.DUPLICATE_ID`,
`PIH.RESOURCE.DUPLICATE_PATH`, and `PIH.RESOURCE.DEPENDENCY_CYCLE` from
manifest validation. Their downstream oracle is manifest-failure propagation
without selection. These inputs provide the generic and extension manifests,
strict Draft 2020-12 schemas, project-profile instance, valid/invalid fixtures,
resource-resolution and semantic-invariant oracles, the generic evidence skill
and references, and the H3 completion validator. The local tree is explicit
project configuration; it is not imported into generic Python or embedded as a
generic default.

`harness/pi/fixtures/canonical/canonical-json-vectors.json` contains 17 accepted
RFC-8785-plus-LF vectors: one for each of the 16 public-JSON record kinds and one
additional `DiagnosticPath` NFC-spelling case. The diagnostic-path oracle
contains four valid and nineteen invalid cases. These resources fix textual
software-verification inputs and expected result partitions. They are not
generated truth from the H2 implementation, and passing against them does not
establish intended Rust conformance. H2 does not modify H3 schemas, manifests,
fixtures, profiles, skills, or handoff records.

## Import and dependency discipline

Internal generic imports remain relative. Generic modules do not import the
project-local layer, `ksdft2effmass.workflows.cpn`, electronic-structure domain
objects, QE or Wannier adapters, SNAKES, repository-specific task definitions,
or H3 resources as executable Python. Public records contain no credentials,
open files, sockets, mutable mappings or sequences, closures, subprocess or
scheduler handles, Git clients, mutable service clients, or imported scientific
objects.

## Claim boundary and exclusions

H2 evidence is **software verification only**. A `PASS` means that supplied
inputs satisfy the documented structural contract. It does not establish human
acceptance, task authorization, successor activation, command correctness,
numerical verification, scientific validation, uncertainty quantification,
physical correctness, package readiness, release status, or publication
permission. No actual numerical algorithm is implemented here, so numerical
verification is not applicable; scientific validation and uncertainty
quantification are also not applicable.

The following remain outside H2:

- H4 local integration, compatibility adapters, shadow replay, parity,
  rollback, retirement, and cutover;
- H5 distribution naming, extraction, compatibility facade, packaging,
  publication, or release readiness;
- P2 and all scientific or protected execution, including QE and Wannier90;
- SQLite or any mutable repository;
- workflow engines, dispatch, runners, command execution, Git mutation,
  subprocesses, schedulers, plugins, registries, service locators, and dynamic
  imports;
- command specification/result wire records, universal filename policy,
  Graphify integration, and scientific validation/UQ result types.

The intended later extraction may move the generic implementation to an
independent namespace, while H4's project adapter remains local. The final
standalone import and distribution names are an H5 decision. No compatibility
facade or second implementation exists in H2.

## Navigation

- [Previous: Contract and versioning](./ksdft2effmass.harness.02.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Skills and textual resources](./ksdft2effmass.harness.04.md)
