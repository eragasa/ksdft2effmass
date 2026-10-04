# Band-frame ownership

## Status

**Generic retained-space witness and reciprocal-mesh ownership resolved; represented-
frame metadata remains open.** The current 2D definition declares which bands are
selected and does not require frame coordinates. Authenticated 2D frame evidence and
explicit represented-frame basis, gauge, units, and artifact provenance remain future
work outside the corrected generic retained-space API. The implemented ownership
decision is recorded in the
[band-frame ownership decision](../../architecture/v2/ksdft2effmass/periodic/band-frame-ownership-decision.md).

## Current ownership

The implemented 1D path separates three meanings:

1. [`ReciprocalBandFramePath1D`](../../../python/src/ksdft2effmass/solid_state/band_frames.py)
   stores ordered reciprocal points, frame coordinates, endpoint sewing, and an
   orthonormality tolerance.
2. [`Periodic1DBandFrameRetainedSubspace`](../../../python/src/ksdft2effmass/periodic1d/retention.py)
   binds that gauge-dependent represented frame path to the scientific
   `PeriodicRetainedSubspace` identity.
3. Campaign adoption authenticates replay artifacts and constructs the parent,
   selection, retained space, retained operator, represented operator, and effective
   models without collapsing them.

The general
[`PeriodicRetainedSubspace`](../../../python/src/ksdft2effmass/periodic/retention.py)
owns no projector/frame witness field. The 1D isolated binding owns and reauthenticates
its exact frame-content digest. The composite smooth-projector digest remains only in
the exact source campaign result because projector-coordinate bytes are unavailable.

No corresponding reciprocal-mesh frame or projector-coordinate record currently exists
for periodic2d. Preserved 2D results retain energies, hopping data, represented-space
metadata, and diagnostics, but not authenticated frame or projector coordinate bytes.

## Resolved debt

`projector_or_frame_record_id` was a compound, stringly typed boundary. A projector,
one frame, and a reciprocal-domain frame family are different represented objects even
when they identify the same mathematical subspace. The former field could not
intrinsically enforce:

- projector versus frame versus frame-family semantics;
- reciprocal path or mesh domain;
- ambient basis and ordering;
- gauge and sewing convention;
- coordinate content identity and digest scope; or
- the relationship between a numerical witness and the scientific retained-space
  identity.

The compound field also overlapped with dimension-specific binding records such as
`Periodic1DBandFrameRetainedSubspace`. Its removal prevents that ambiguity from
spreading into the future 2D API.

## Implemented direction

The [band-frame ownership decision](../../architecture/v2/ksdft2effmass/periodic/band-frame-ownership-decision.md)
implements one ownership design:

- excludes the former compound witness from the mathematical
  `PeriodicRetainedSubspace` owner;
- preserves the isolated represented-frame identity in its typed frame binding while
  leaving the digest-only composite projector identity with its source campaign result
  until projector coordinates exist;
- keep the unit-carrying 1D and reduced-coordinate 2D half-open reciprocal-mesh
  DataObjects together in `ksdft2effmass.solid_state.reciprocal_meshes` without
  changing coordinates or ordering; and
- keep represented frame coordinates in `ksdft2effmass.solid_state.band_frames`, where
  a future `ReciprocalBandFrameMesh2D` composes the lower-level 2D mesh rather than
  copying its coordinates.

The dimensional scientific frame bindings remain under `periodic1d.retention` and
`periodic2d.retention`. Campaign or replay code authenticates available frame artifacts
and constructs those bindings without owning band-frame mathematics. Digest-only
projector evidence remains campaign evidence and does not imply an available
represented projector.

Do not introduce a competing top-level `band/frames` source tree. A later split of the
existing `solid_state.band_frames` module into a package is not required by the
accepted decision and would need its own reviewed migration.

## Resolution and future work

The reciprocal-mesh owner move is complete: consumers use the lower-level module and
the old defining modules retain no compatibility aliases. The atomic witness correction
is also complete: the typed 1D frame binding owns the exact frame digest, isolated
adoption supplies it, composite adoption retains projector-digest evidence only through
its exact source result, and the compound generic field is removed. Both SHA-256 values
and their canonical little-endian complex128 C-order byte scope remain unchanged.

Future frame work must preserve the separation among selected-band definition,
mathematical retained space, represented frame or projector, exact retained operator,
and effective model. The existing 1D frame path and typed retained-space binding do not
supply a standalone explicit represented-frame basis identity, gauge identity, units
contract, or frame-artifact provenance field. Define the 2D reciprocal-mesh frame
contract only after those meanings, mesh ordering, both reciprocal-boundary sewing
directions, parent finite basis, and digest scope are explicit. Add class-owned software
and numerical verification for that represented frame contract without treating those
checks as scientific validation.

## Boundaries

This record does not authorize payload replay, sidecar creation, external execution,
PhysKit migration, compatibility aliases, or changes to historical digests. The
corrected 1D adoption aggregates and authenticated digests enforce their distinct
contracts. The removed generic witness field is not a foundation for new 2D frame
ownership.

Projector construction, frame construction, gauge transport, basis transformation,
disentanglement, hopping truncation, and effective-model fitting remain distinct
operations. Parent-model, numerical or discretization, and model-reduction errors
remain separate.

## Resolution and remaining closure criteria

The completed generic-witness correction requires:

- the compound generic retained-subspace witness field to be removed;
- the isolated frame digest to remain with its typed frame binding and the composite
  projector digest to remain with its source campaign evidence;
- affected tests, typing, Ruff, formatting, Sphinx, local links, and checksum checks to
  pass; and
- no software result to be promoted to scientific validation or uncertainty
  quantification.

The broader represented-frame metadata debt remains open until:

- represented frame owners expose explicit domain, basis, gauge, sewing, units,
  provenance, and content-identity semantics without inferring them from arrays or
  digests;
- a 2D frame-mesh binding can be introduced without an “or” field or inferred metadata;
  and
- no represented projector owner is introduced without authenticated projector
  coordinates and equivalent metadata.
