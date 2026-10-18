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
represented plane-wave and finite-difference models, reciprocal meshes, finite-basis
sewing, common-space transport, encoded campaign records, and additional topological
and Wannier90 studies.

The package also exposes non-executable calculation scaffolds for represented-parent
comparison and shell/gauge locality. Both consume the nominal `Periodic2DModel`
branch, and the locality scaffold composes its represented-parent baseline rather than
inheriting from it. The scaffolds define dependency boundaries only; they do not close
the periodic2d parity gate, provide missing producer Actions, or establish calculated
results. Their eventual calculation definitions must retain the full nonorthogonal
primitive lattice, inverse metric, and reduced-coordinate convention. Two-dimensional
periodicity uses an intrinsic nonorthogonal two-vector basis. PhysKit's explicit
embedded-plane adapter preserves a full-column-rank $3\times2$ ambient basis, its
in-plane frame, projector, and dual basis while routing its induced metric to the
intrinsic $2\times2$ contract. That flat embedded plane remains distinct from a fully
periodic $3\times3$ slab or supercell.

The pinned PhysKit version `0.1.3.dev0` at exact accepted migration revision
`d81febb811fbc4feb014530fcae6cf6d9ad9ead5` provides the reusable nonorthogonal
Bloch-periodic scalar Laplacian under
`projectkoios.physkit.periodic.finite_difference`. Its dimension-bounded 2D/3D
implementation uses the full inverse metric, mixed centered derivatives, and
reduced-twist seam phases. The same version provides the explicit $3\times2$
embedded-plane adapter and strict defining-geometry JSON codec under
`projectkoios.physkit.periodic.lattice.embedding`. Dependency availability and the
consumer smoke test do not by themselves close the periodic2d parity gate, supply
kinetic-energy or effective-mass scaling, or establish material validation.

The [periodic2d capability-parity gate](../../periodic2d-capability-parity.md) remains
in force. No new two-dimensional defect campaign should proceed until the applicable
parent capabilities, typed results, verification, and documentation pass that gate.

## Prospective outward adequacy consumer

The draft
[HSH-1 architecture](../../analysis/model_adequacy/hopping_shell_hierarchy/index.md)
composes the retained scalar periodic2d parent to define one synthetic nested
hopping-support analysis. HSH-1 belongs to `analysis.model_adequacy`, not this parent
package: periodic2d owns the source model; PhysKit owns reusable lattice symmetry,
orbit, hopping-shell, projection, and physical hopping geometry; HSH owns the selected
hierarchy, weights, normalization, thresholds, witnesses, certificate meaning, and
bounded dispositions. No HSH implementation, result, or evidence claim exists.

After the isotropic three-dimensional stage, a distinct anisotropic two-dimensional
family will remove axis-permutation equivalence while retaining explicit
sign symmetries:

```text
ksdft2effmass.campaign.model-adequacy.periodic2d.anisotropic-hopping-support-hierarchy
```

That family has no opened development task, exact protocol, implementation, or result.
It must not be represented as another threshold case or version of HSH-1. Only after
the concrete isotropic/anisotropic sequence closes may reusable behavior be considered
for the
[general-lattice-vector extension](../../analysis/model_adequacy/general-lattice-vector-extension.md).
The two-dimensional target must preserve a full-rank intrinsic or reviewed
embedded-plane basis and its induced metric; it must not reinterpret a `3 x 2` plane as
a three-dimensional periodic cell.

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
