# Band-frame and retained-subspace witness ownership decision

## Status

**Accepted target architecture; implementation pending.** This decision resolves the
generic `projector_or_frame_record_id` boundary and reciprocal-mesh ownership needed
before periodic2d frame or retained-operator adoption. It does not itself change source,
replay artifacts, payloads, digests, or public imports.

## Context

`PeriodicRetainedSubspace` identifies one retained mathematical space. Its current
`projector_or_frame_record_id: str` may name a projector, one frame, or a frame family.
Those are different represented objects:

- a projector is gauge invariant but basis represented;
- a frame is a gauge-dependent isometry into an ambient represented space; and
- a reciprocal-domain frame family additionally has point ordering, boundary sewing,
  and closure conventions.

One nonempty string cannot intrinsically state which object is referenced, its domain,
basis, gauge, sewing, units, provenance, or content-identity scope. The field also
duplicates the role of specialized bindings such as
`Periodic1DBandFrameRetainedSubspace`.

The current 1D adoptions remain internally correlated. The isolated route places the
authenticated frame-content SHA-256 identity in the compound field, and the composite
route places the authenticated smooth-projector SHA-256 identity there. This decision
preserves both exact digest values while correcting ownership: the isolated frame
digest moves to its frame binding, while the composite projector digest remains in its
source result and is no longer duplicated in the retained-space object.

Periodic2d introduces a second ownership question. `CenteredUniformReciprocalMesh2D`
currently owns reduced coordinates and deterministic first-outer, second-inner ordering
inside `analysis.model_systems.periodic2d.reciprocal_mesh`. A future represented frame
mesh must compose those semantics rather than copy them. Placing the frame owner in
`solid_state.band_frames` must not create a reverse `solid_state -> analysis`
dependency.

## Decision

### 1. The mathematical retained space owns no numerical-witness union

Remove `projector_or_frame_record_id` from `PeriodicRetainedSubspace` and from
`PeriodicRetainedSubspaceConstructor` in a forward source migration. Do not retain an
alias and do not replace it with parallel optional projector/frame strings.

`PeriodicRetainedSubspace` continues to own:

- its parent-qualified `PeriodicRetentionDefinition`;
- ambient state-space identity and represented ambient dimension;
- retained-space identity and rank through the definition;
- spin and internal-degree conventions;
- reciprocal-boundary convention; and
- retained-space construction provenance.

`PeriodicRetentionDefinition.construction_record_id` continues to identify the closed
method-specific selection or construction definition. It does not become a numerical
projector/frame content digest.

This keeps the mathematical retained-space identity stable under a unitary frame
change. A represented witness can change gauge or encoding without silently creating a
new mathematical space.

### 2. Evidence ownership follows the available represented payload

The target does not create one replacement witness union. It gives represented content
identity to a typed binding only when the corresponding represented payload exists. No
generic witness registry, factory, structural fallback, or virtual registration is
introduced.

The forward target is:

- `Periodic1DBandFrameRetainedSubspace` owns its represented frame path and the exact
  authenticated `frame_content_sha256` value used by isolated adoption because the
  frame coordinates are retained;
- `Periodic1DCompositeBandGroupResult.identities` remains the owner of
  `smooth_projector_sha256` as authenticated campaign evidence because no composite
  projector coordinates are retained;
- `Periodic1DCompositeOperatorGroupAdoption` keeps the exact source result and selected
  group correlated without copying the projector digest into the mathematical retained
  space or claiming a represented projector family; and
- future `Periodic2DBandFrameRetainedSubspace` binds one represented 2D frame mesh to a
  parent-qualified scientific retained space only after authenticated frame coordinates
  exist.

The existing 1D values are content digests, not stable logical record identifiers. The
isolated frame digest is SHA-256 over the frame array canonicalized as little-endian
complex128 in C order and serialized with C-order bytes. The composite smooth-projector
digest declares the same canonical byte scope over the ordered projector-family array,
but the current retained repository evidence does not include that array for direct
reverification. If future evidence supplies projector coordinates or a stable record
identity, each receives a separate field and must not be derived from the digest alone.

A represented projector-family binding is deferred until authenticated projector bytes
and their domain, ambient basis, reciprocal ordering, units, and construction semantics
exist. A digest-only object must not masquerade as the unavailable represented
projector. Campaign adoption code retains evidence correlation without owning
band-frame or projector mathematics.

### 3. Dimension-specific reciprocal meshes move to a lower-level solid-state owner

Create a cohesive `ksdft2effmass.solid_state.reciprocal_meshes` module in the later
source migration and move the immutable mesh DataObjects there:

- `CenteredUniformReciprocalMesh1D` from `solid_state.reciprocal_paths`; and
- `CenteredUniformReciprocalMesh2D` from
  `analysis.model_systems.periodic2d.reciprocal_mesh`.

The move preserves point counts, half-open domains, coordinate values, units,
identifiers, representative ordering, and exact public validation behavior. Existing
consumer imports are updated in one forward migration; the old defining modules do not
retain compatibility aliases.

Numerical neighbor, sewing, transport, and Hamiltonian Actions stay with their current
algorithmic owners and import the mesh DataObjects from `solid_state.reciprocal_meshes`.
`solid_state` therefore does not depend on `analysis`.

`electronic_structure.KPointSampling` remains separate. It represents weighted,
physically scaled Cartesian three-vector calculation sampling. The band-frame meshes
are dimension-specific, unweighted, half-open periodic meshes: the 1D mesh retains an
explicit reciprocal-coordinate unit, while the current 2D mesh uses reduced
coordinates. Their boundary sewing is represented separately. Neither object is
inferred from the other.

### 4. Band-frame coordinates remain in the established band-frame owner

`ksdft2effmass.solid_state.band_frames` remains the cohesive owner of represented band
frames. A future `ReciprocalBandFrameMesh2D` composes, rather than duplicates, an exact
`CenteredUniformReciprocalMesh2D` from `solid_state.reciprocal_meshes`.

The 2D frame object must declare at least:

- the exact reduced reciprocal mesh and flattened point ordering;
- one immutable frame matrix per mesh point;
- ambient represented state-space and ordered-basis identity;
- retained rank and frame units;
- gauge identity;
- both primitive reciprocal-boundary sewing directions;
- orthonormality policy and bounded numerical evidence;
- frame content identity with an explicit digest algorithm and canonical byte scope;
  and
- provenance plus any independently supplied stable record identity as a separate
  field.

The detailed sewing representation remains an implementation design task. It must be
closed and typed before source implementation; it cannot be inferred from matrix shape,
mesh periodicity, or the existing topology summaries.

A later module-to-package split of `solid_state.band_frames` is not required by this
decision. Do not create a competing top-level `band/frames` source tree. If the module
becomes too large, a separate reviewed source migration may replace it with a package
while deliberately updating supported imports.

## Dependency direction

The accepted dependency direction is:

```text
operators quantities
        ^
        |
solid_state.reciprocal_meshes
        ^
        |
solid_state.band_frames
        ^
        |
periodic1d.retention / periodic2d.retention
        ^
        |
campaign adoption and authenticated replay correlation
```

Algorithmic analysis modules may depend on the solid-state DataObjects. Solid-state
DataObjects do not depend on campaign, replay, or analysis modules. PhysKit continues
to own reusable lattice primitives; this decision adds no dependency and does not
migrate any class to PhysKit.

## Consequences

### Benefits

- The mathematical retained-space object no longer contains a projector/frame union.
- Gauge-dependent frame identity is separated from gauge-independent retained-space
  identity.
- The isolated frame digest is owned with its retained frame payload, while the
  composite projector digest remains evidence in the campaign result that actually
  contains it.
- 1D and 2D frame records can share one lower-level reciprocal-mesh boundary without
  copying coordinate or ordering semantics.
- Existing 1D authenticated digest values can be preserved exactly during migration.

### Costs

- The later source migration changes constructors and every current use of
  `projector_or_frame_record_id`.
- 1D isolated adoption requires a frame-binding migration, while composite adoption
  must stop treating digest-only campaign evidence as retained-space identity.
- Moving reciprocal meshes requires coordinated import, test, Sphinx, and canonical
  architecture updates.
- No 2D retained space can be adopted until the frame-mesh artifact contract and
  authenticated source are available.

## Rejected alternatives

### Keep `projector_or_frame_record_id`

Rejected because one string cannot enforce represented witness kind or its domain,
basis, gauge, sewing, provenance, and content-identity scope.

### Add optional projector and frame strings to `PeriodicRetainedSubspace`

Rejected because it preserves ambiguity, permits contradictory combinations, and keeps
representation details inside the mathematical retained-space owner.

### Add a generic witness enum and registry

Rejected because a closed label still does not provide the distinct typed state needed
for represented frames or future projector families, while a registry or discovery
mechanism would introduce unnecessary dynamic indirection.

### Add a digest-only represented projector-family binding

Rejected because the composite evidence retains no projector coordinate array to bind
or reauthenticate. Its digest remains meaningful authenticated campaign evidence, but
it does not by itself provide the domain, basis, ordering, units, or construction state
of a represented projector family.

### Copy mesh coordinates into `ReciprocalBandFrameMesh2D`

Rejected because `CenteredUniformReciprocalMesh2D` already owns exact coordinates and
ordering. Duplicate arrays or tuples could disagree while appearing shape compatible.

### Let `solid_state.band_frames` import from `analysis`

Rejected because it reverses the intended dependency direction and makes reusable
represented data depend on a higher-level algorithm namespace.

### Reuse `electronic_structure.KPointSampling`

Rejected because its weighted, physically scaled Cartesian three-vector contract is
not a dimension-specific, unweighted, half-open periodic mesh contract. The 1D mesh may
carry a physical reciprocal-coordinate unit; the 2D mesh currently uses reduced
coordinates. Neither mesh carries `KPointSampling` weights or scaling metadata.

## Forward migration sequence

1. Move 1D and 2D reciprocal mesh DataObjects to
   `solid_state.reciprocal_meshes`, update all consumers, and retain no old-module
   aliases.
2. In one atomic witness-correction stage:
   1. extend the existing 1D band-frame binding with the exact historical
      `frame_content_sha256` value and migrate isolated adoption to that field;
   2. update composite adoption to preserve
      `source_result.identities.smooth_projector_sha256` as digest-only campaign
      evidence without copying it into the mathematical retained space or creating a
      represented projector binding; and
   3. remove `projector_or_frame_record_id` from the generic retained-space source and
      constructor only after both adoption routes have moved.
3. In that same witness-correction stage, update source docstrings, class-owned tests,
   Sphinx concepts/API pages, canonical architecture mappings, crosswalk dispositions,
   and retained checksum verification.
4. Design and implement `ReciprocalBandFrameMesh2D` and
   `Periodic2DBandFrameRetainedSubspace` only after an authenticated 2D artifact schema
   is accepted.
5. Treat repository-local replay or sidecar creation as a separate protected operation;
   this decision supplies no execution authority.

The mesh-owner move and witness correction are independently reviewable migration
units. The three witness-correction substeps are indivisible: no intermediate reviewed
state may remove the compound field before the isolated frame binding and both adoption
correlations are complete.

## Scientific and evidence boundaries

A frame or projector can represent a retained subspace without becoming the subspace
itself. Gauge transport and basis transformation can change frame coordinates without
changing the underlying projector. Projection, disentanglement, basis transformation,
localization, truncation, and effective-model fitting remain separate operations.

Software and numerical checks of mesh ordering, orthonormality, sewing, content digest,
or adoption correlation do not establish physical adequacy, scientific validation, or
uncertainty quantification. Parent-model, numerical or discretization, and
model-reduction errors remain separate.

## Completion gate

This decision is implemented only when:

- no maintained source or test uses `projector_or_frame_record_id`;
- the exact historical 1D frame digest remains preserved with the frame binding, and
  the exact composite projector digest remains preserved with its source campaign
  evidence;
- reciprocal mesh DataObjects have one lower-level owner with unchanged coordinates and
  ordering;
- no represented projector binding is claimed from digest-only evidence;
- no old-module aliases, registries, factories, or inferred metadata are introduced;
- source, tests, Sphinx, canonical architecture, crosswalks, and technical-debt records
  agree; and
- Ruff, formatting, typing, affected tests, strict Sphinx, local links, retained
  checksums, and diff checks pass.

No completion claim authorizes 2D artifact replay, external computation, scientific
validation, release, publication, or cleanup.
