<!-- Generated from SQLite control state; do not edit. -->
# Silicon density-of-states tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.dielectric-silicon.md) · [Next](./quantumespresso.simulations.fermi-surface-copper.md)

## Status

`blocked`: Planned candidate; blocked pending exact SCF/NSCF/DOS inputs, pseudopotential, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the silicon SCF-to-NSCF-to-dos.x tutorial workflow and inventory its cross-stage artifacts.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- Depends on: `quantumespresso.simulations.structure-optimization-silicon`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight compatible prefix/outdir, tetrahedron occupation, dense mesh, and band-count inputs.
- Run only authorized pw.x SCF, pw.x NSCF, and dos.x stages.
- Capture per-stage snapshots, separate streams, exits, runtime, and DOS data artifacts.

## Completion criteria

- Cross-stage artifact dependencies and exact inputs are recorded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The final disposition identifies useful parser behavior without convergence or validation claims.

## Exclusions

- No DOS curve is accepted as a project reference.
- No shared mutable prefix or outdir is used across Tasks.
- No interactive plotting program is required.

## Historical source

No archived source.
