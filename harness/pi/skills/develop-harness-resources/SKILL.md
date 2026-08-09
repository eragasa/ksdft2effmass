---
name: develop-harness-resources
description: Designs, versions, reviews, relocates, and synchronizes generic or project-local harness textual resources, manifests, profiles, descriptors, schemas, fixtures, policy references, and documentation without duplicating deterministic resource actions.
---

# Develop harness resources

## Purpose and trigger

Use this skill when work creates, changes, versions, reviews, or relocates a
resource manifest or reference, project profile, local extension manifest, skill
descriptor, textual schema, canonical fixture, policy reference, resource
documentation, or extractable harness resource.

Do not use it for ordinary Python implementation, routine test writing, task or
chain status, route selection, parity execution, Git operations, checkpoint
resolution, scientific datasets, numerical results, or generated Sphinx output.
Task authority and permitted paths remain external to this skill.

Read [the resource conventions](references/harness-resource-conventions.md)
before making a resource-design decision.

## Ownership judgment

Classify every resource as generic or project-local before assigning identity or
path. Generic resources must remain project-independent, use explicit identities,
depend only on generic resources, accept explicit project profiles, and avoid CWD
or Git-root discovery. Project-local resources may represent project policies,
markers, prefixes, paths, and compatibility rules and may extend or depend on
generic resources.

Local resources must not replace a generic ID or path, redefine generic behavior,
or make a generic resource depend on local state. The permitted dependency
direction is that local resources may depend on generic resources.

## Compact procedure

1. Identify the represented capability.
2. Classify it as generic or project-local.
3. Identify its authoritative schema or textual contract.
4. Assign stable resource and format or behavior version identities.
5. Declare exact dependencies.
6. Add positive and focused negative fixtures when the contract requires them.
7. Add or update explicit manifest entries.
8. Refresh explicitly selected content identities.
9. Validate closure, overlay direction, paths, profiles, and descriptors.
10. Synchronize maintained documentation and canonical/live copies.
11. Report structural limitations and excluded claims.
12. Stop without activating unrelated work.

Do not embed historical task paths, counts, hashes, phase gates, agent authority,
assignments, checkpoints, retries, or handoff procedure.

## Deterministic owners

| Operation | Existing owner |
|---|---|
| Manifest structure and overlay validation | `ResourceManifestValidator` |
| Explicit selected identity refresh | `ResourceManifestRefresher` |
| Root-confined selection and hashing | `ResourceResolver` |
| Skill descriptor closure | `SkillResourceValidator` |
| Canonical JSON | `JsonRecordSerializer` and `JsonRecordDeserializer` |
| Checksum validation | `ChecksumManifestValidator` |
| Project profile loading | `ProjectProfileLoader` |
| Local composition | Existing project-local context ActionObject |

This skill decides what resources should represent. It never duplicates those
algorithms or treats their structural results as authorization.

## Manifest maintenance

Require explicit resource IDs. For an existing selected entry whose bytes
changed, use the read-only proposal command:

```bash
python/.venv/bin/python -m \
  ksdft2effmass.harness.pi.local.refresh_resource_manifest \
  --root <explicit-resource-root> \
  --manifest <explicit-manifest-path> \
  --resource-id <resource-id>
```

Do not calculate applicable digests with ad hoc shell or inline Python, scan a
repository for resources, or treat refresh as resource discovery. New entries
require explicit authoring and review; refresh changes identities, not logical
resource membership.

## Routing and claim boundary

Route maintained pytest meaning to `develop-python-test-evidence`, public Python
documentation to `document-python-research-software`, object ownership to
`design-data-action-objects`, and material architecture alternatives to
`develop-architecture-decision`.

A structurally passing resource set establishes only documented resource-contract
conformance. It does not establish implementation correctness, numerical
verification, scientific validation, uncertainty quantification, physical
correctness, external execution validity, or human acceptance.

## Stop conditions

Stop and report when generic/local ownership is materially ambiguous, a change
would replace a generic identity or reverse dependency direction, schema and
runtime behavior conflict, a behavior change lacks an authorized versioning
decision, a required profile or manifest is missing, maintained actions cannot
represent the operation, or generic resources would acquire scientific meaning.
Do not activate successors or unrelated work.
