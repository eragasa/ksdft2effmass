# Band-frame ownership

## Status

**Safe to defer for selection-definition work; blocking before new periodic2d
retained-space or retained-operator adoption.** The current 2D slice declares which
bands are selected and does not require frame coordinates. A later claim that a
preserved result identifies a retained mathematical space requires this debt to be
resolved or explicitly superseded.

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

## Target direction

Keep represented band-frame coordinates in a cohesive band-frame owner and keep
scientific retention meaning in the dimensional retention owner:

```text
ksdft2effmass.solid_state.band_frames
    ReciprocalBandFramePath1D
    ReciprocalBandFrameMesh2D        # proposed, not implemented

ksdft2effmass.periodic1d.retention
    Periodic1DBandFrameRetainedSubspace

ksdft2effmass.periodic2d.retention
    Periodic2DBandFrameRetainedSubspace  # proposed, not implemented
```

`ReciprocalBandFrameMesh2D` would own ordered mesh coordinates, frame matrices,
directional sewing data, ambient dimension, retained rank, units, and numerical
orthonormality policy. `Periodic2DBandFrameRetainedSubspace` would bind that represented
record to a parent-qualified scientific retained space and require exact parent,
domain, rank, ambient-space, basis-order, and authenticated-content agreement.

Campaign or replay code would authenticate an artifact and construct the reusable
frame record. It would not own band-frame mathematics. The generic retained-space
record would not infer a frame or projector from energies, equal rank, topology
summaries, route names, or matrix shape.

The existing module `ksdft2effmass.solid_state.band_frames` remains the canonical local
owner. Do not introduce a competing top-level `band/frames` source tree. A later split
into a `solid_state.band_frames` package requires a separately reviewed migration and
must preserve supported imports deliberately.

## Required architecture decision

Before implementation, choose one explicit generic boundary:

1. **Preferred:** remove the compound witness identity from
   `PeriodicRetainedSubspace`; let typed projector/frame representation bindings own
   numerical witness identities and content digests.
2. Alternatively, replace it with a closed typed witness reference that distinguishes
   projector, frame, and frame-family semantics and declares content-identity scope.

Do not retain an untyped `str` field whose name contains “or,” and do not add parallel
optional projector and frame strings. Either decision must explain how the mathematical
retained-space identity remains stable under gauge changes while represented witnesses
remain separately authenticated.

## Deferred migration

1. Inventory every source, test, Sphinx, and architecture use of
   `projector_or_frame_record_id`.
2. Decide whether the generic retained-space object owns no numerical witness or one
   closed typed witness reference.
3. Migrate 1D isolated and composite adoption without changing authenticated frame or
   projector digest values.
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

- the generic retained-subspace witness boundary has one unambiguous reviewed design;
- all 1D uses preserve their exact authenticated frame/projector identities;
- represented projector and frame owners expose explicit domain, basis, gauge, sewing,
  units, provenance, and content-identity semantics;
- a 2D frame-mesh binding can be introduced without an “or” field or inferred metadata;
- affected tests, typing, Ruff, formatting, Sphinx, local links, and checksum checks
  pass; and
- no software result is promoted to scientific validation or uncertainty
  quantification.
