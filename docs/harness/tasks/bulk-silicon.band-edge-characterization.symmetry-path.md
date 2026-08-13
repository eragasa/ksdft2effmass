<!-- Generated from SQLite control state; do not edit. -->
# Production silicon symmetry-path bands

[Task index](index.md) · [Previous](./bulk-silicon.band-edge-characterization.effective-mass-analysis.md) · [Next](./bulk-silicon.band-edge-characterization.valence-edge.md)

## Status

`blocked`: Essential calculation for dispersion inspection; blocked by an accepted production SCF parent and a human-approved sourced path specification.

## Objective

Evaluate production Kohn–Sham bands on a modern, explicitly sourced silicon high-symmetry path for dispersion and band-order inspection.

## Parent and prerequisites

- Parent: `bulk-silicon.band-edge-characterization`
- Depends on: `bulk-silicon.production-reference.scf`
- External prerequisite: `production_execution_authorization`
- External prerequisite: `symmetry_path_design_approval`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the accepted SCF parent, sourced path, reciprocal-coordinate convention, segment labels, interpolation density, retained band count, and VBM-reference rule.
- Retain input, parent identity, ordered k-point and eigenvalue record, path distances/labels, band correspondence metadata, streams, artifact inventory, direct/indirect gap observations, and publication band figure.
- The human owns the path source, density, band count, symmetry labeling, and any physical-validation comparator.

## Completion criteria

- The production and legacy tutorial paths are explicitly distinct.
- Every coordinate, label, energy, unit, reference, repeated endpoint, and band index is reproducible.
- Path-density and retained-band adequacy are numerically checked for the claimed dispersion only.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- This path is not used as the sole effective-mass fit, Wannier grid, DOS mesh, or complete TB training/validation set.

## Historical source

No archived source.
