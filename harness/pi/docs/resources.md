# Generic textual resources

## Scope and identity

`harness/pi/` is the generic textual-resource root. A caller supplies this root explicitly together with `harness/pi/resource-manifest.json`; neither the current directory, Git, caller-supplied runtime-state records, environment variables, parent-directory search, nor package fallback selects it. An optional project-local root and manifest are separate explicit inputs.

The generic manifest has stable identity `pih.generic.resources`, manifest version `1`, and layer `generic`. Each resource entry is identified by its opaque, stable `resource_id`, not by its path. An entry also records its `resource_kind`, `format_version`, manifest-root-relative `ResourcePath`, exact SHA-256 `content_identity`, and complete, sorted `dependency_ids`. The manifest therefore distinguishes:

- stable logical identity (`resource_id` or `manifest_id`);
- contract revision (`format_version` or `manifest_version`);
- exact byte identity (`ArtifactIdentity`); and
- location below a caller-supplied root (`ResourcePath`).

Matching hashes establish byte equality only. They do not establish equal kind, behavior, semantic meaning, provenance, acceptance, or scientific correctness. A resource-byte change requires a new content identity and manifest revision; a behavior change also requires the applicable behavior/format version change. The profile and manifest bind exact supported integer versions. Unsupported versions and unknown fields are rejected rather than inferred, upgraded, or partially consumed.

## Accepted-contract generic identities

The generic manifest is the authoritative inventory. In this page, “accepted-contract” identifies the accepted contract task governing the resource-task surface; it does not claim final resource-task human acceptance, which remains a separate gate. Its version-1 families are:

- `pih.skill.document-research-python.v1`, its descriptor `pih.manifest.skill-descriptor.document-research-python.v1`, and its directly referenced grammar `pih.reference.test-evidence-documentation.v1`;
- record schemas under the `pih.schema.record-*.v1` identities;
- reusable schema entry points `pih.schema.project-profile.v1`, `pih.schema.resource-manifest.v1`, and `pih.schema.skill-descriptor.v1`; and
- `pih.schema.common-wire-definitions.v1` for shared wire definitions.

The skill descriptor names its entry and complete required-resource closure. Construction and deserialization retain intrinsic validation but produce only candidate records: a resource self-edge and duplicate manifest entries remain representable. Manifest resources use deterministic complete-key canonical ordering and preserve duplicates. `ValidateResourceManifest` then owns duplicate IDs/paths, self/cycles, missing or generic-to-local dependencies, compatibility/mismatch, and forbidden replacement. `ResolveResource` and skill validation propagate its failure and short-circuit without selecting or interpreting resources. A successful structural check does not authorize invocation of a skill; authorization, side-effect, retry, and termination policies remain separate facts.

The documentation in `harness/pi/docs/` explains the accepted resources but is not a second manifest, skill descriptor, schema, or procedure. Where an identity or hash differs from prose, the selected manifest and exact resource bytes govern.

## Generic and local composition

Version 1 uses `extend_only`. A local manifest names the generic base in `extends_manifest_id`; it may introduce new local IDs and paths and may depend on generic resources. It may not reuse or replace any generic resource ID or serialized path, even when bytes match. Generic resources may never depend on project-local resources or contain project identifiers, evidence prefixes, repository-specific paths, or scientific policy.

The dependency direction is normative:

```text
project-local resources -> generic resources
generic resources -/-> project-local resources
```

“Generic before local” is validation and dependency order, not overwrite precedence. There is no shadow winner, ambient fallback, network fetch, or implicit installation.

## Path types and confinement

Three serialized lexical path meanings remain distinct:

- `ResourcePath` identifies one regular-file resource relative to an explicit resource root. Resolution additionally requires existence, exact component case, no symlink component, containment below the canonical root, regular-file kind, and matching bytes.
- `OwnershipScopePath` identifies a repository ownership declaration paired with `scope_kind = file | directory_tree`. A directory-tree scope contains its named path and descendants beginning with `path + "/"`; it is not a manifest resource identity.
- `DiagnosticPath` is a neutral lexical location for `ValidationIssue.path`. It may spell a regular file, directory, or ownership-scope prefix and asserts neither existence, file kind, nor containment semantics. `null` means no location applies.

All three reject absolute paths, empty or `.`/`..` segments, repeated or trailing separators, non-NFC input, controls, backslashes, and Windows drive/device/UNC syntax. They compare by exact case-sensitive spelling. Runtime roots and resolved `pathlib.Path` values are never serialized identities.

## Fixtures and canonical vectors

`harness/pi/fixtures/fixture-index.json` indexes public-record schema fixtures, DiagnosticPath cases, resource-resolution cases, and canonical JSON vectors. The resolution oracle covers valid generic and local selection as well as successful deserialization followed by capability-specific failure for duplicate ID/path and self-dependency, plus missing dependency, cycle, incompatible version, generic-to-local dependency, forbidden replacement, absent file, and absent resource failures. DiagnosticPath fixtures include regular-file, directory-tree, `null`, and NFC spellings plus malformed platform-independent cases.

`harness/pi/fixtures/canonical/canonical-json-vectors.json` supplies the canonical record vectors: RFC 8785 JSON encoded as UTF-8 followed by exactly one LF, with an expected SHA-256. These vectors preserve exact DiagnosticPath spelling and are the shared input for later Python-consumer encoding/decoding and intended Rust agreement. They are contract fixtures, not execution results.

## Resource-to-Python-consumer handoff

After separate human acceptance of the resource task, the later Python consumer task may consume the accepted generic manifest, local manifest, project profile, schemas, skill resources, fixtures, canonical vectors, and resource-task completion-validator identity as read-only inputs. That consumer is expected to implement the accepted generic Python contract against those exact identities and to test explicit-root resolution, closure, canonical bytes, dependency direction, and path semantics.

This handoff does not activate the later Python consumer task. It remains blocked until the resource task is human-accepted, receives separate explicit human authorization, and passes its own ownership preflight. Resource-task documentation neither creates Python production code nor authorizes a local integration task, another successor task, skill cutover, publication, or external or scientific execution.
