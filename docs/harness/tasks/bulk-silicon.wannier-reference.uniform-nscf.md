<!-- Generated from SQLite control state; do not edit. -->
# Production uniform NSCF mesh for Wannier90

[Task index](index.md) · [Previous](./bulk-silicon.wannier-reference.localization.md) · [Next](./bulk-silicon.workflow.extracted-model-verification.md)

## Status

`blocked`: Essential protected calculation; blocked by the accepted production SCF parent and human-approved target subspace, bands, grid, projections, and window design.

## Objective

Generate the regular reciprocal-space QE state set required for production Wannierization with complete wavefunction lineage.

## Parent and prerequisites

- Parent: `bulk-silicon.wannier-reference`
- Depends on: `bulk-silicon.production-reference.scf`
- External prerequisite: `production_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the SCF parent, mesh topology, retained occupied/unoccupied bands, spin treatment, target subspace, prospective windows/projections, executable/environment, and external storage plan.
- Retain NSCF input/output manifests, QEXSD, wavefunction and restart identities, mesh and band records, resource/timing data, streams, inventory, and compatibility metadata for pw2wannier90.x.
- The human owns mesh topology/density, band count, target subspace, wavefunction retention, and disentanglement necessity.

## Completion criteria

- Grid closure and QE/Wannier neighbor-list compatibility are verified.
- Band count and mesh adequacy are tested against later interpolation targets without borrowing SCF or path convergence.
- Large wavefunctions remain external with complete checksummed inventory.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- Projections and energy windows are not selected by this planning record.

## Historical source

No archived source.
