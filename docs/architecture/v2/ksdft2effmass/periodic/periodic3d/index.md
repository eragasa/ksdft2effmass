# Periodic3d architecture delta

## Role in the general framework

Periodic3d is the material-reference destination for bulk silicon and its initial
substitutional phosphorus and boron defect families. It must reuse accepted
lower-dimensional abstractions only when their mathematical domains and represented
contracts remain valid in three dimensions.

Shared hierarchy, campaign, catalog, and comparison rules are owned by the parent
[general periodic architecture](../index.md). This page records only three-dimensional
differences.

## Target hierarchy

- Every supported three-dimensional scientific model inherits the nominal
  `Periodic3DModel` branch.
- `SiliconReferenceModel` identifies the specified pristine bulk-silicon parent model.
- Every three-dimensional defect model inherits `Periodic3DDefectModel` and retains an
  exact parent-model identity.
- Initial material-reference defect targets are substitutional phosphorus and boron in
  silicon.
- Toy 3D models are introduced only when they establish a named mathematical,
  numerical, or software requirement; empty symmetry placeholders are prohibited.

## Representation and comparison boundary

A silicon physical model, its Kohn--Sham operator, a projected or Wannier operator, and
a finite matrix representation remain distinct objects. Pristine and doped operators
cannot be subtracted until basis, gauge, energy reference, units, geometry, and state
spaces are aligned.

Three-dimensional comparisons may reuse common scalar quantities from toy campaigns,
but tensor, valley, orbital, spin, and defect-locality results require explicit typed
contracts. Lower-dimensional agreement does not establish three-dimensional numerical
verification or silicon validation.

## Prospective admissible-set model adequacy

The shared
[admissible-set evidence semantics](../../analysis/model_adequacy/admissible-set-evidence-semantics.md)
are dimension-independent, but no three-dimensional scientific problem is implied by
that common vocabulary. The
[periodic-3D experiment architecture](../../../experiments/model-adequacy/periodic3d/index.md)
records the required parent, lattice, symmetry, representation, candidate-family,
channel, metric, certificate, role, and verification decisions before implementation.
The selected sequence introduces an isotropic simple-cubic scalar 3-D control first,
then returns to the preserved anisotropic orthorhombic 3-D proposal after an intervening
anisotropic 2-D stage. The two 3-D targets are distinct experiment families and neither
is a bulk-silicon surrogate. Development of the first is tracked under
`docs/tasks/dev/experiments/isotropic3d/`; the later exact proposal remains under
`experiments/model-adequacy/periodic3d/anisotropic-hopping-support-hierarchy/`.

No periodic-1D or periodic-2D certificate geometry, shell equivalence, alignment family,
threshold, or metric transfers automatically to three dimensions. The isotropic target
must define cubic signed-permutation orbits explicitly; the anisotropic target uses sign
orbits without axis permutations and named support groups rather than cubic shells.
Concrete composition and evidence remain experiment-owned until repeated implemented
behavior justifies a reusable analysis owner.

After the ordered concrete stages, the
[general-lattice-vector extension](../../analysis/model_adequacy/general-lattice-vector-extension.md)
may admit full-rank `3 x 3` direct bases with explicit dual, metric, orientation, units,
and conditioning policy. It must consume reviewed PhysKit lattice primitives and must
not infer model symmetry or hopping equivalence from lattice-vector lengths alone.

## Execution boundary

Quantum ESPRESSO remains responsible for electronic-structure calculations and
Wannier90 for localization. This architecture does not authorize production runs,
remote computation, pseudopotential or exchange-correlation choices, numerical-setting
changes, or access to external calculation archives. Those actions require their own
specifications, provenance, authorization, and retained evidence.
