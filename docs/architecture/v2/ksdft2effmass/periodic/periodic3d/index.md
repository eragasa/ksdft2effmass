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

## Execution boundary

Quantum ESPRESSO remains responsible for electronic-structure calculations and
Wannier90 for localization. This architecture does not authorize production runs,
remote computation, pseudopotential or exchange-correlation choices, numerical-setting
changes, or access to external calculation archives. Those actions require their own
specifications, provenance, authorization, and retained evidence.
