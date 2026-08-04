# Proposed minimum H1 contract

## Contract rule

H1 should specify only interfaces demonstrated by current consumers. Existing scripts are requirement evidence, not automatically the API. All records are immutable, versioned, deterministic to serialize, translatable to concrete Rust structs, and reject unknown fields according to an explicit compatibility policy. Actions are stateless and accept every root, profile and record explicitly.

## Recommended records

| Interface | Demonstrated need and current consumers | Proposed owner | Data/action separation | Versioning | Structured failure | Portability | Explicit exclusions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ArtifactIdentity` | Checksums, skill hashes, mutation audits, resource identity; all validators and reviews | generic Python | DataObject containing algorithm, digest and optional media/type identity; hashing is an ActionObject | public contract and serialization | malformed algorithm/digest issue | fixed strings/enums | no claim of semantic equality or historical attestation |
| `ResourceReference` | Skills, references, schemas, templates, profiles and manifests | generic Python | DataObject with stable ID, kind, format version, explicit root-relative path and content identity | public contract | invalid kind/path/version issue | concrete enum/struct | filesystem path is not durable identity; no implicit discovery |
| `ResourceManifest` | Skill closure is currently incomplete; H3 needs deterministic resources | generic resources plus generic Python record | DataObject lists references and declared dependencies; validator ActionObject checks closure | resource-manifest version independent of package version | missing, duplicate, incompatible or hash issue | deterministic arrays/tuples | no installation, dispatch or code execution |
| `ProjectProfile` | Current scripts hard-code roots, prefixes, markers, formats and local extensions | generic Python record, instantiated under local resources | DataObject supplies roots, policy IDs and extension references only | profile-schema version | unknown/malformed/unsupported profile issue | no closures or dynamic objects | no credentials, clients, handles, subprocesses, scientific results or implicit `.pi` search |
| `SkillDescriptor` | Six current skills, global/repository precedence, incomplete resource hashing | generic resources | DataObject names entry resource, trigger/capability IDs, required resource closure, side-effect class, authorization, result/failure schema and termination/retry policy | skill behavior version | invalid descriptor/dependency/overlay issue | textual/versioned fields | no ambient skill inheritance or automatic global fallback |
| `ValidationIssue` | Every current validator emits unstructured assertion/prose failures | generic Python | ResultObject component with stable code, severity, subject/path, related identities and message | issue-code namespace tied to public contract | it is the structured invalidity | concrete enum/string fields | message is not the machine protocol |
| `ValidationResult` | Ownership, checkpoint, skill, evidence, checksum and H0 gates | generic Python | ResultObject with status and deterministically ordered issue tuple | public contract | internal programming defect remains exception | fixed status and tuple fields | `PASS` grants no task, scientific or human acceptance |
| `OwnershipManifestView` | v2 ownership preflight is established; v1 must remain compatible locally | generic Python | immutable normalized role/path/completion view; loading and validation are actions | ownership contract version | path, role, overlap, reviewer, completion and profile issues | path strings and role records | no dispatch, no execution, no P1 object inventory in generic fields |
| `CheckpointRecord` | Eleven durable decisions and one resolver skill | generic Python plus local extension | immutable decision content; validation/resolution comparison are actions | checkpoint schema version | identity/status/schema/replay conflict issues | concrete option/status records | no automatic decision, resumption, Git operation or acceptance inference |
| `TaskReference` and `ChainView` | Ownership lookup and active/prerequisite/P2 assertions currently parse heterogeneous chains | generic Python narrow views | immutable IDs, record references, prerequisites and explicit activation facts; evaluator is an action | chain-view version | missing/duplicate/cycle/contradictory-state issues | graph as explicit arrays | no scientific CPN semantics, task prose schema, dispatch or auto-activation |
| `ChecksumEntry` and `ChecksumManifest` | Five fragmented SHA-256 catalogs | generic Python | immutable root/version/entry records; hashing and comparison are actions | checksum-manifest version | missing, changed, duplicate, traversal or algorithm issue | algorithm enum and path/digest strings | checksum pass is identity evidence only |
| `DeterministicCommandSpec` and `DeterministicToolResult` | Command manifests and evidence authority require argv/environment/input/output identity | generic Python records | records only; an external caller executes, result validator checks shape | command/result contract version | malformed result, missing identity, nonzero exit represented structurally | argv tuple, mappings, artifact references | no subprocess runner, shell interpolation, scheduler or remote execution in H1 |
| `DecisionBoundaryResult` | Pending/resolution commits and pushes are mandatory but absent from checkpoint schema | generic record with local Git policy extension | immutable task/checkpoint, commit, branch, remote, push status and partial-effect references; Git operation remains external | result contract version | failed/partial durability issue | strings/enums | no Git client, force push, reset, merge, tag or release operation |

## Recommended ActionObjects

| Action | Current need | Inputs | Output | Local policy supplied explicitly |
| --- | --- | --- | --- | --- |
| `LoadProjectProfile` | replace hard-coded repository globals | profile bytes/reference and schema | profile result | allowed schema versions and local resource reference |
| `ResolveResource` | skills/schemas currently rely on paths and precedence | resource root and reference | resolved resource result | explicit generic/local roots and overlay relation |
| `ValidateResourceManifest` | complete resource identity is missing | manifest and supplied root | `ValidationResult` | permitted kinds/versions/extensions |
| `ValidateOwnershipManifest` | established v2 launch preflight | manifest view, chain view, agent descriptors, profile | `ValidationResult` | agent format, local roots, v1 compatibility adapter |
| `ValidateCheckpointSet` | schema, identity, unresolved and replay consistency | checkpoint records and policy | `ValidationResult` | statuses, linked-record requirements and decision vocabulary |
| `EvaluateChainState` | active/blocked status is manually duplicated | task references, chain view, checkpoints, explicit activations | structured state result | local lifecycle vocabulary and protected activation requirements |
| `AuditEvidenceIdentifiers` | current AST audit is profile-coupled | module references and evidence profile | `ValidationResult` plus owner inventory | roots, markers, prefixes, filename policy and migration states |
| `ValidateChecksumManifest` | fragmented shell catalogs | explicit root and checksum manifest | `ValidationResult` | permitted algorithms and excluded generated paths |
| `ValidateSkillResources` | current skill validator hashes only entry files | resource manifest, descriptors and explicit roots | `ValidationResult` | dispatch precedence and allowed local overlays |

## Version layers

H1 must keep these independent:

1. public Python contract;
2. serialized record contract;
3. project-profile schema;
4. resource-manifest schema;
5. skill behavioral identity;
6. local compatibility-adapter version;
7. future package implementation/release version.

Changing a project profile or local compatibility adapter does not automatically change the public Python contract.

## Generic/local boundary

Generic code owns structural integrity: deterministic ordering, unknown-field policy, path confinement, symlink-escape rejection, unique identities, writer non-overlap, reviewer independence, acyclic prerequisites, explicit completion binding, resource closure, and structured results.

Local configuration owns `.pi` layout, task/checkpoint identities, agent frontmatter, Git branch/remote policy, evidence prefixes and markers, exact test-module rules, CPN/operator inventories, SNAKES/QE/Wannier semantics, scientific acceptance and compatibility with historical P1 records.

## Interfaces H1 should not include

- a universal workflow engine or generic scientific CPN;
- a subprocess, scheduler, Git-mutation, package-installation or publication service;
- QE, Wannier90, SNAKES or operator-record interfaces;
- a CLI unless an existing current consumer is demonstrated beyond development wrappers;
- a new `write-research-evidence-tests` skill identity;
- `boundary_owned` as a third generic primary evidence kind or a new mandatory `boundary` test-function surface;
- a universal test filename convention;
- Graphify integration in the minimum contract;
- automatic current-directory, Git-root, `.pi`, global-skill or repository-resource discovery;
- migration/retirement of historical records;
- scientific-validation or UQ result types without an authorized actual protocol;
- numerical-verification interfaces because no harness numerical algorithm was discovered;
- project-local Python adapters in H2 unless H1 assigns exact files that do not belong to H4.
