# Periodic2d architecture delta

## Role in the general framework

Periodic2d extends the controlled periodic program to two reciprocal directions,
anisotropic represented spaces, two-dimensional defects, and topology. Graphene is the
target two-dimensional material-reference family.

Shared hierarchy, campaign, catalog, and comparison rules are owned by the parent
[general periodic architecture](../index.md). This page records only two-dimensional
differences.

## Current evidence and source boundary

The canonical current package is `ksdft2effmass.periodic2d`. Existing work provides
the nominal cosine-potential toy parent and scalar-hopping finite-extent defect model,
represented plane-wave and finite-difference operators, reciprocal meshes, finite-basis
sewing, common-space transport, a parent-qualified selected-band retention definition,
encoded campaign records, and additional topological and Wannier90 studies. The
selection definition does not yet supply a retained subspace or operator because the
preserved result documents do not authenticate frame or projector coordinates.

The [periodic2d capability-parity gate](../../periodic2d-capability-parity.md) remains
in force. No new two-dimensional defect campaign should proceed until the applicable
parent capabilities, typed results, verification, and documentation pass that gate.

## Target hierarchy

- Every supported two-dimensional scientific model inherits the nominal
  `Periodic2DModel` branch.
- Every two-dimensional defect model inherits `Periodic2DDefectModel` and preserves
  its exact parent-model and alignment prerequisites.
- Existing cosine and other controlled models enter the toy-model catalog only after
  their scientific-model ownership is separated from campaign provenance.
- Selected-band and composite-subspace studies expose retained spaces and operators as
  scientific objects distinct from encoded campaign documents and finite matrices.
- `GrapheneReferenceModel` identifies a specified graphene parent model; it does not
  itself own DFT execution, Wannier localization, campaign acceptance, or validation.
- Future graphene defect models retain the exact graphene parent identity and explicit
  geometry, basis, gauge, energy-reference, and unit alignment.

## Scientific boundary

Graphene is a two-dimensional periodic material-reference target, not a claim that all
of its embedding, electrostatic, spin, substrate, or many-body physics can be omitted.
Those modeling choices require authoritative scientific assumptions and versioned
specifications before implementation or calculation.
