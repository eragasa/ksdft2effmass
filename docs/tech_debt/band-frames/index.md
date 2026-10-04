# Band-frame ownership

## Status

**Architecture decision complete; source migration safe to defer for selection-only
work and blocking before new periodic2d retained-space or retained-operator adoption.**
The current 2D definition declares which bands are selected and does not require frame
coordinates. The accepted target is recorded in the
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
currently also contains `projector_or_frame_record_id: str`. The 1D isolated route
places a frame content digest in that field, while the composite route places a smooth
projector content digest there and checks it against retained campaign evidence.

No corresponding reciprocal-mesh frame or projector-coordinate record currently exists
for periodic2d. Preserved 2D results retain energies, hopping data, represented-space
metadata, and diagnostics, but not authenticated frame or projector coordinate bytes.

## Debt

`projector_or_frame_record_id` is a compound, stringly typed boundary. A projector, one
frame, and a reciprocal-domain frame family are different represented objects even when
they identify the same mathematical subspace. The field does not state which object is
referenced and cannot intrinsically enforce:

- projector versus frame versus frame-family semantics;
- reciprocal path or mesh domain;
- ambient basis and ordering;
- gauge and sewing convention;
- coordinate content identity and digest scope; or
- the relationship between a numerical witness and the scientific retained-space
  identity.

The compound field also overlaps with dimension-specific binding records such as
`Periodic1DBandFrameRetainedSubspace`. Adding a 2D frame class while preserving this
ambiguity would spread the debt into the new API.

## Accepted direction

The [band-frame ownership decision](../../architecture/v2/ksdft2effmass/periodic/band-frame-ownership-decision.md)
selects one forward design:

- remove `projector_or_frame_record_id` from the mathematical
  `PeriodicRetainedSubspace` owner;
- preserve the isolated represented-frame identity in its typed frame binding while
  leaving the digest-only composite projector identity with its source campaign result
  until projector coordinates exist;
- move the existing unit-carrying 1D and reduced-coordinate 2D half-open
  reciprocal-mesh DataObjects to `ksdft2effmass.solid_state.reciprocal_meshes` without
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

## Deferred migration

1. Inventory every source, test, Sphinx, and architecture use of
   `projector_or_frame_record_id`.
2. Move the unit-carrying 1D and reduced-coordinate 2D half-open reciprocal-mesh
   DataObjects to the accepted lower-level owner and update consumers without
   compatibility aliases.
3. In one atomic stage, add the typed 1D frame content-digest field and migrate isolated
   adoption; update composite adoption to retain the exact projector digest only
   through its source campaign result; and only then remove the compound field.
   Preserve both SHA-256 values and their canonical little-endian complex128 C-order
   byte scope without claiming unavailable projector coordinates.
4. Preserve the separation among selected-band definition, mathematical retained space,
   represented frame/projector, exact retained operator, and effective model.
5. Define the 2D reciprocal-mesh frame contract only after mesh ordering, both
   reciprocal-boundary sewing directions, parent finite basis, gauge identity, units,
   and digest scope are explicit.
6. Add class-owned software and numerical verification for the represented frame
   contract; do not treat those checks as scientific validation.
7. Update the
   [scientific-retention architecture](../../architecture/v2/ksdft2effmass/periodic/retained-spaces-and-operators.md),
   source docstrings, Sphinx concepts, canonical architecture pages, and affected
   adoption records together.

## Boundaries

This record does not authorize payload replay, sidecar creation, external execution,
PhysKit migration, compatibility aliases, or changes to historical digests. It does not
claim that existing 1D adoptions are invalid: their explicit adoption aggregates and
authenticated digests continue to enforce their current contracts. It records that the
generic witness field should not become the foundation for new 2D frame ownership.

Projector construction, frame construction, gauge transport, basis transformation,
disentanglement, hopping truncation, and effective-model fitting remain distinct
operations. Parent-model, numerical or discretization, and model-reduction errors
remain separate.

## Completion criteria

This debt is complete when:

- the compound generic retained-subspace witness field is removed;
- the isolated frame digest remains with its typed frame binding and the composite
  projector digest remains with its source campaign evidence;
- represented frame owners expose explicit domain, basis, gauge, sewing, units,
  provenance, and content-identity semantics, while no represented projector owner is
  introduced without projector coordinates and equivalent metadata;
- a 2D frame-mesh binding can be introduced without an “or” field or inferred metadata;
- affected tests, typing, Ruff, formatting, Sphinx, local links, and checksum checks
  pass; and
- no software result is promoted to scientific validation or uncertainty
  quantification.
