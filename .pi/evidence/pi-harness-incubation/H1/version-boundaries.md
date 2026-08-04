# H1 independent version boundaries

Status: corrected under resolved `H1-HC01` Option B and pending final H1 human
acceptance.

## Independent version axes

| Axis | Version-1 owner | What it versions | Does not version |
| --- | --- | --- | --- |
| Python public contract | H1 contract; future H2 implementation | exported class names, action signatures, Python semantic types, invariants, result behavior | profile instances, skill prose, resource bytes, package release |
| Serialized record contract | H1 field/wire contract; future H3 schemas and H2 codecs | JSON field names/types/order, canonical bytes, record semantics | Python import namespace, project profile revision |
| Project-profile schema | H1 semantics; H3 generic schema and local instance | profile fields, local policy representation, compatibility declarations | Python API or package version |
| Resource-manifest schema | H1 semantics; H3 schema/resources | manifest/reference shape, dependency and overlay representation | skill behavior or Python API |
| Skill behavioral version | descriptor/resource owner in H3 | operational trigger/procedure/result/failure behavior of one skill | file path alone, profile revision, package release |
| Local compatibility-adapter version | project-local owner in H4 | mapping of current `.pi`, agent, Git, P1 v1, marker, prefix, and filename policy into the generic contract | generic Python API or accepted historical evidence |
| Future implementation/release version | future package/release authority, not H1 | distributable implementation identity and release metadata | acceptance of a profile/resource/skill contract by itself |

The version axes advance independently. In particular, changing a project
profile or local adapter does not change the Python API version; changing skill
prose behavior does not change a resource-manifest schema when the manifest
shape remains valid; and a package release number does not establish human
acceptance or scientific validity.

## Compatibility terms

- **Backward compatible:** a newer producer remains consumable by an older
  consumer under the older consumer's declared supported contract without loss
  or reinterpretation of represented meaning.
- **Forward compatible:** an older producer remains consumable by a newer
  consumer under the newer consumer's declared supported older version.
- **Rejected:** the consumer must return a structured unsupported-version or
  unknown-field result and produce no partially trusted record.
- **Migration-requiring:** represented meaning can be preserved only by an
  explicit versioned adapter or resource migration with retained old/new
  identities and validation.
- **Contract-breaking:** existing valid consumers or represented meanings would
  change without an explicit major-version boundary.

## Change classification

| Change | Classification |
| --- | --- |
| Clarify human message prose without changing machine fields/codes/semantics | backward and forward compatible |
| Add an `INFO` message using an existing registered code/condition | backward compatible if issue multiplicity and ordering contract remains unchanged; otherwise migration-requiring |
| Add a new issue code for a newly detected condition | version 1 is closed; requires a new integer public-contract version and explicit consumer migration |
| Change issue code meaning, severity, duplicate key, ordering, or an existing issue field's semantic path type after acceptance/implementation | contract-breaking new integer Python/record version |
| Add an optional JSON field to a v1 record | rejected by v1 unknown-field policy; requires a new integer serialized-record schema version and migration |
| Add a required JSON field, rename a field, change type/nullability, or reinterpret a field | contract-breaking serialized-record change |
| Expand an enum accepted by a record | version 1 is closed; requires a new integer schema/contract version and explicit compatibility decision |
| Relax identifier/path confinement, permit hidden discovery, or allow local replacement overlays | contract-breaking and requires human decision |
| Add SHA algorithm beyond SHA-256 | new artifact-identity schema/version and compatibility declaration; no silent acceptance |
| Change profile values while retaining schema and meaning | profile instance revision only; Python API unchanged |
| Add/remove/rename a profile field | new profile schema version; v1 rejects; migration required |
| Add a resource entry to a manifest | manifest content/version change; schema unchanged if shape/meaning remains v1 |
| Change a resource's bytes | new `ArtifactIdentity` and manifest content/version; skill behavior version also changes if behavior changes |
| Move a resource path with unchanged bytes | new manifest version and migration mapping; identity may remain only if resource identity is path-independent and all references update |
| Change skill trigger, authorization, side-effect, result/failure, retry, or termination behavior | skill behavioral version change; may also require descriptor resource identity change |
| Change local P1 v1 mapping or project Git/durability behavior | local compatibility-adapter version change; generic API unchanged unless generic meaning must change |
| Rename future distribution/import/CLI | future package/release or major API migration; H5 decision, not profile change |

## Version negotiation and rejection

Every version-sensitive loader/action receives supported closed integer versions
explicitly or obtains complete allowed resource/skill pairs from a validated
`ProjectProfile`. Version 1 performs exact integer matching and never guesses compatibility from package versions, file locations,
Git history, or unknown fields. Unsupported input returns the capability's
`VERSION_INCOMPATIBLE` or `PIH.WIRE.UNSUPPORTED_VERSION` issue and no partial
record.

A newer reader may support several older versions through explicit code paths.
An adapter records its own version and source/target versions; it must not mutate
or rewrite accepted historical evidence. A local compatibility adapter may map
legacy P1 `boundary_owned` into generic `artifact_owned` relation metadata for
comparison while preserving the original input string and historical tests.

## Pre-acceptance H1-HC01 Option-B correction

The accepted bounded correction changes the still-unimplemented proposal's
`ValidationIssue.path` semantic type from `ResourcePath | None` to
`DiagnosticPath | None`. It adds one common semantic primitive and the intended
validated Rust `DiagnosticPath(String)` newtype, but no DataObject, ResultObject,
ActionObject, candidate disposition, schema-version value, or interface-count
entry. Because no H2 implementation or H3 schema/fixture exists and final H1
acceptance remains pending, this correction establishes the proposed version-1
contract rather than migrating an accepted implementation. The same type change
after final acceptance or implementation would require the contract-breaking
version boundary stated above.

`ResourcePath` and `OwnershipScopePath` retain their specialized version-1
meanings. No serialization, integer, checksum, overlay, evidence-kind, or
generic/local decision is reopened.

## Initial values proposed at H1-HC01

```text
Python public contract integer version:   1
serialized-record schema version:         1 per included record
project-profile schema version:           1
resource-manifest schema version:         1
skill behavioral version:                 per SkillDescriptor, positive integer
local compatibility-adapter version:      project-owned, positive integer when present
future implementation/package version:    unset and deferred
```

These are contract proposal values, not implemented version numbers, package
metadata, a release, or publication authority.
