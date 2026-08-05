# H3 bounded correction under H2-HC01 Option A

Status: implemented; focused H3 validation PASS

Resolved `H2-HC01` Option A authorizes this pre-H2-acceptance version-1
contract/resource reconciliation. It changes no public interface, issue code,
integer version, or extension-only generic/local policy.

## Corrected boundary

- `ResourceReference` retains intrinsic field, identifier, kind/version, path,
  content-identity, tuple, dependency uniqueness, and dependency ordering checks.
  Self-dependency is representable.
- `ResourceManifest` retains intrinsic identity/version/layer/base shape,
  nonempty immutable resources, and complete-key canonical ordering. Ordering
  preserves duplicate IDs, paths, and exact entries.
- `DeserializeJsonRecord` succeeds for these structurally valid relationally
  invalid candidates.
- `ValidateResourceManifest` owns duplicate IDs/paths, self/cycles, missing and
  generic-to-local dependencies, kind/format compatibility, manifest mismatch,
  and forbidden local replacement, using only existing `PIH.RESOURCE.*` codes.
- Resolution and skill-resource validation must propagate manifest failure and
  short-circuit.

## Reconciled resources

The two affected record-schema descriptions and manifest array shape now expose
the candidate boundary. The semantic oracle maps self-dependency from successful
deserialization to `PIH.RESOURCE.DEPENDENCY_CYCLE`. Resource-resolution cases
and their independent index state successful deserialization for duplicate ID,
duplicate path, and self-dependency before capability validation fails. The H3
validator checks these stage boundaries, complete-key ordering, duplicate
preservation, and local-layer duplicates. Generic manifest byte identities,
handoff identities, and checksum evidence are refreshed after stabilization.

This evidence is software verification only. It establishes no scientific or
numerical result, package release, successor activation, or human final H2
acceptance.
