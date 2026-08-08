# Generic textual resources

## Scope and identity

`harness/pi/` is the generic textual-resource root. A caller supplies this root explicitly together with `harness/pi/resource-manifest.json`; neither the current directory, Git, caller-supplied runtime-state records, environment variables, parent-directory search, nor package fallback selects it. An optional project-local root and manifest are separate explicit inputs.

The generic manifest has stable identity `pih.generic.resources`, manifest version `3`, and layer `generic`. Each resource entry is identified by its opaque, stable `resource_id`, not by its path. An entry also records its `resource_kind`, `format_version`, manifest-root-relative `ResourcePath`, exact SHA-256 `content_identity`, and complete, sorted `dependency_ids`. The manifest therefore distinguishes:

- stable logical identity (`resource_id` or `manifest_id`);
- contract revision (`format_version` or `manifest_version`);
- exact byte identity (`ArtifactIdentity`); and
- location below a caller-supplied root (`ResourcePath`).

Matching hashes establish byte equality only. They do not establish equal kind, behavior, semantic meaning, provenance, acceptance, or scientific correctness. A resource-byte change requires a new content identity and manifest revision; a behavior change also requires the applicable behavior/format version change. The profile and manifest bind exact supported integer versions. Unsupported versions and unknown fields are rejected rather than inferred, upgraded, or partially consumed.

## Accepted-contract generic identities

JSON is the wire representation of `ResourceManifest`; `SerializeJsonRecord` and `DeserializeJsonRecord` own its canonical encoding and strict caller-selected decoding. The generic manifest is the authoritative inventory. In this page, “accepted-contract” identifies the accepted contract task governing the resource-task surface; it does not claim final resource-task human acceptance, which remains a separate gate. Its maintained families are:

- `pih.skill.document-python-research-software.v1` and its descriptor `pih.manifest.skill-descriptor.document-python-research-software.v1`;
- `pih.skill.develop-harness-resources.v1`, its descriptor `pih.manifest.skill-descriptor.develop-harness-resources.v1`, and `pih.reference.harness-resource-conventions.v1`;
- `pih.skill.develop-python-test-evidence.v1`, its descriptor `pih.manifest.skill-descriptor.develop-python-test-evidence.v1`, and `pih.reference.test-evidence-conventions.v1`;
- read-only `pih.skill.develop-architecture-decision.v1`, its descriptor `pih.manifest.skill-descriptor.develop-architecture-decision.v1`, and `pih.reference.architecture-decision-conventions.v1`;
- record schemas under the `pih.schema.record-*.v1` identities;
- reusable schema entry points `pih.schema.project-profile.v1`, `pih.schema.resource-manifest.v1`, and `pih.schema.skill-descriptor.v1`; and
- `pih.schema.common-wire-definitions.v1` for shared wire definitions.

The skill descriptor names its entry and complete required-resource closure. Construction and deserialization retain intrinsic validation but produce only candidate records: a resource self-edge and duplicate manifest entries remain representable. Manifest resources use deterministic complete-key canonical ordering and preserve duplicates. `ValidateResourceManifest` then owns duplicate IDs/paths, self/cycles, missing or generic-to-local dependencies, compatibility/mismatch, and forbidden replacement. `ResolveResource` and skill validation propagate its failure and short-circuit without selecting or interpreting resources. A successful structural check does not authorize invocation of a skill; authorization, side-effect, retry, and termination policies remain separate facts.

The documentation in `harness/pi/docs/` explains the accepted resources but is not a second manifest, skill descriptor, schema, or procedure. Where an identity or hash differs from prose, the selected manifest and exact resource bytes govern.

## Generic and local composition

Version 1 uses `extend_only`. A local manifest names the generic base in `extends_manifest_id`; it may introduce new local IDs and paths and may depend on generic resources. It may not reuse or replace any generic resource ID or serialized path, even when bytes match. Generic resources may never depend on project-local resources or contain project identifiers, evidence prefixes, repository-specific paths, or scientific policy.

The dependency direction is normative: project-local resources may depend on generic resources, while generic resources must remain independent of project-local resources.

“Generic before local” is validation and dependency order, not overwrite precedence. There is no shadow winner, ambient fallback, network fetch, or implicit installation.

## Path types and confinement

Three serialized lexical path meanings remain distinct:

- `ResourcePath` identifies one regular-file resource relative to an explicit resource root. Resolution additionally requires existence, exact component case, no symlink component, containment below the canonical root, regular-file kind, and matching bytes.
- `OwnershipScopePath` identifies a repository ownership declaration paired with `scope_kind = file | directory_tree`. A directory-tree scope contains its named path and descendants beginning with `path + "/"`; it is not a manifest resource identity.
- `DiagnosticPath` is a neutral lexical location for `ValidationIssue.path`. It may spell a regular file, directory, or ownership-scope prefix and asserts neither existence, file kind, nor containment semantics. `null` means no location applies.

All three reject absolute paths, empty or `.`/`..` segments, repeated or trailing separators, non-NFC input, controls, backslashes, and Windows drive/device/UNC syntax. They compare by exact case-sensitive spelling. Runtime roots and resolved `pathlib.Path` values are never serialized identities.

## Resource-design skill and deterministic owners

`develop-harness-resources` owns judgment about generic versus project-local ownership, stable identities and versions, dependency closure, extension-only overlays, schema/fixture agreement, skill descriptor closure, manifest synchronization, and structural claim limits. Its canonical entry, descriptor, and convention reference are generic resources; the live skill and reference remain byte-identical to their canonical counterparts.

The skill does not reproduce mechanics. `ValidateResourceManifest` owns manifest and overlay structure, `RefreshResourceManifest` owns explicit selected byte-identity proposals, `ResolveResource` owns root-confined selection and hash agreement, `ValidateSkillResources` owns descriptor closure, the JSON actions own canonical wire representation, `ValidateChecksumManifest` owns checksum agreement, `LoadProjectProfile` owns explicit profile loading, and the project-local context ActionObject owns local composition. Historical resource agents remain historical and disabled.

## Validation, resolution, and identity refresh

Intrinsic field invariants and canonical resource ordering belong to `ArtifactIdentity`, `ResourceReference`, and `ResourceManifest`. Cross-resource duplicate, dependency, overlay, and profile compatibility checks belong to `ValidateResourceManifest`. Exact selection with identity agreement belongs to `ResolveResource`.

`RefreshResourceManifest` owns a different deterministic operation: given one existing manifest, one explicit absolute root, and explicit manifest resource IDs, it reuses the maintained exact-case, nonsymlink, root-confined regular-file observation and computes SHA-256 from observed bytes. It returns a new immutable, canonically ordered manifest proposal and the sorted IDs whose identities changed. Every nonidentity resource field and every manifest field is preserved. Unknown IDs and filesystem failures are structured findings with no partial manifest.

Refresh does not scan a root, discover or add resources, remove resources, infer a repository, validate an unrelated generic/local profile relationship, mutate the input manifest, write JSON, or invoke Git. Filesystem persistence remains outside the generic ActionObject. Callers may serialize a successful proposal with `SerializeJsonRecord`; the thin read-only command is:

```text
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.refresh_resource_manifest \
  --root /absolute/path/to/resource/root \
  --manifest /absolute/path/to/resource-manifest.json \
  --resource-id pih.skill.example.v1
```

The command emits deterministic JSON and exits `0` for a proposal, `1` for structured validation failure, `2` for invalid explicit command inputs, and `3` for an unexpected command-boundary failure. It has no write mode. Matching or refreshed hashes establish exact byte identity only; they do not establish semantic correctness, provenance truth, scientific validity, uncertainty quantification, or human acceptance.

## Fixtures and canonical vectors

`harness/pi/fixtures/fixture-index.json` indexes public-record schema fixtures, DiagnosticPath cases, resource-resolution cases, and canonical JSON vectors. The resolution oracle covers valid generic and local selection as well as successful deserialization followed by capability-specific failure for duplicate ID/path and self-dependency, plus missing dependency, cycle, incompatible version, generic-to-local dependency, forbidden replacement, absent file, and absent resource failures. DiagnosticPath fixtures include regular-file, directory-tree, `null`, and NFC spellings plus malformed platform-independent cases.

`harness/pi/fixtures/canonical/canonical-json-vectors.json` supplies the canonical record vectors: RFC 8785 JSON encoded as UTF-8 followed by exactly one LF, with an expected SHA-256. These vectors preserve exact DiagnosticPath spelling and are the shared input for later Python-consumer encoding/decoding and intended Rust agreement. They are contract fixtures, not execution results.

## Resource-to-Python-consumer handoff

After separate human acceptance of the resource task, the later Python consumer task may consume the accepted generic manifest, local manifest, project profile, schemas, skill resources, fixtures, canonical vectors, and resource-task completion-validator identity as read-only inputs. That consumer is expected to implement the accepted generic Python contract against those exact identities and to test explicit-root resolution, closure, canonical bytes, dependency direction, and path semantics.

This handoff does not activate the later Python consumer task. It remains blocked until the resource task is human-accepted, receives separate explicit human authorization, and passes its own ownership preflight. Resource-task documentation neither creates Python production code nor authorizes a local integration task, another successor task, skill cutover, publication, or external or scientific execution.
