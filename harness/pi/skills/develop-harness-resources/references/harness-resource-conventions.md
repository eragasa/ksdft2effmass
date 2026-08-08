# Harness resource conventions

## Represented boundary

A harness textual resource is a versioned, manifest-addressed regular file whose
meaning is defined by an accepted schema or textual contract. Resource design
separates logical identity, represented version, explicit location, exact bytes,
manifest membership, and project profile selection.

| Identity | Meaning |
|---|---|
| Resource ID | Stable logical identity |
| Format version | Version of represented structure or behavior |
| Resource path | Explicit manifest-relative POSIX path |
| Content identity | SHA-256 identity of exact bytes |
| Manifest identity | Identity and version of one resource inventory |
| Profile binding | Project-selected generic and optional local manifests |

Exact byte identity does not imply semantic equivalence. Semantic equivalence
does not imply byte identity. Any byte change requires refreshed content identity.
A represented structure or behavior change may also require a new format,
behavior, or manifest version; a digest change alone must not conceal that choice.

## Generic ownership

Generic resources belong beneath the caller-selected generic harness resource
root. They must:

- avoid project task IDs, evidence markers, scientific semantics, and implicit
  repository paths;
- use explicit versioned logical identities and manifest-relative paths;
- depend only on generic resources;
- remain usable through explicit project-profile inputs; and
- avoid current-directory, parent-directory, Git-root, network, or package
  fallback discovery.

A generic schema or policy represents reusable harness structure or behavior. It
must not encode one project's scientific conventions, current workflow status,
or agent assignments.

## Project-local ownership

Project-local resources belong beneath the caller-selected local harness resource
root. They may identify project policies, evidence markers and prefixes, explicit
paths, compatibility rules, and local extension identities. They may depend on
accepted generic identities and add local resources.

They must not replace a generic ID, reuse a generic resource path, redefine
generic behavior, or require any generic resource to depend on local state. The
only permitted cross-layer dependency direction is that local resources may
depend on generic resources. Generic resources remain independent of the local
layer.

## Dependencies and closure

Declare every direct resource dependency explicitly and in canonical sorted
order. The manifest must contain the complete transitive closure selected by a
skill descriptor or profile. Dependency IDs express represented requirements,
not execution order, ownership assignment, or acceptance.

`ValidateResourceManifest` owns duplicate ID/path detection, extension-only
overlay enforcement, missing dependencies, dependency cycles, generic/local
direction, profile compatibility, and format support. `ValidateSkillResources`
owns entry kind, required-resource closure, authorization-policy inclusion, and
profile-supported skill behavior. Do not restate their algorithms in prose or
ad hoc scripts.

## Schemas and fixtures

Schemas define represented structure, closed fields, versions, and lexical
constraints; they do not establish semantic or scientific truth. Keep schema
validation distinct from runtime construction and adaptation.

Use positive fixtures for structurally accepted examples. Use negative fixtures
to isolate one intended defect where practical. Canonical vectors establish exact
serialization behavior only. Generic fixtures must contain no project-specific
data. Fixture completeness remains a human-reviewed contract judgment rather
than a conclusion inferred from passing counts.

When a schema, runtime DataObject, adapter, fixture, and documentation cover the
same represented contract, synchronize them. Stop on disagreement instead of
choosing whichever surface is easiest to update.

## Skill resource closure

A reusable skill resource family normally contains one concise `SKILL.md`, one
directly linked stable convention reference when needed, and one descriptor. The
descriptor must:

- name the exact entry resource;
- include the entry and every required reference in `required_resource_ids`;
- declare the authorization policy resource explicitly;
- use sorted unique capability and resource IDs;
- declare side-effect, retry, and termination policy; and
- use a behavior version supported by the selected project profile.

The descriptor itself is a manifest resource whose dependencies include its
entry, reference closure, and descriptor schema. Canonical and live skill and
reference bytes remain identical where the resource contract maintains both.
A skill must not contain task status, writer paths, agent authority, checkpoints,
retries, handoffs, or historical phase procedure.

## Manifest authoring and identity refresh

New logical resources require explicit authoring of resource ID, kind, format
version, path, dependencies, and initial content identity. Do not infer manifest
membership by scanning files.

For existing entries, `RefreshResourceManifest` observes only explicitly selected
manifest paths beneath one explicit root and proposes canonical updated content.
It does not write a manifest or discover resources. `ResolveResource` verifies
root-confined exact-case nonsymlink regular-file selection and an existing
identity. Canonical JSON remains owned by `SerializeJsonRecord` and
`DeserializeJsonRecord`.

After a resource family changes, validate the generic manifest, optional local
manifest, selected profile binding, descriptor closure, path confinement,
canonical/live identity, and documentation. A structural pass grants no task
activation, execution authority, or human acceptance.

## Reporting and stop boundary

Report the ownership classification, represented contract, logical and version
identities, dependencies, manifest/profile changes, deterministic checks, and
limitations. Keep structural conformance separate from implementation
correctness, numerical verification, scientific validation, uncertainty
quantification, physical correctness, external execution validity, and human
acceptance.

Stop on unresolved ownership, generic replacement, reversed dependency direction,
schema/runtime conflict, unauthorized behavior versioning, missing profile or
manifest, unsupported deterministic operation, or scientific meaning in a
generic resource. Do not expand the task to unrelated framework, route, agent,
or control-plane work.
