<!-- Generated from SQLite control state; do not edit. -->
# Silicon bandstructure tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.bands-gaas.md) · [Next](./quantumespresso.simulations.bi2se3.md)

## Status

`blocked`: Planned candidate; blocked pending exact SCF/bands inputs, pseudopotential, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the silicon pw.x SCF and line-mode bands workflow with bands.x postprocessing.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- Depends on: `quantumespresso.simulations.scf-silicon`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight the tutorial's distinct SCF settings and L-Gamma-X-U-Gamma path.
- Run only authorized pw.x SCF, pw.x bands, and bands.x stages.
- Capture per-stage snapshots, separate streams, exits, runtime, and represented band-data artifacts.

## Completion criteria

- The path convention, energy reference, exact inputs, and cross-stage dependencies are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Band outputs are labeled tutorial software behavior, not an accepted spectral reference.

## Exclusions

- Interactive plotband.x execution is excluded.
- Kohn-Sham eigenvalues are not identified with a complete excitation spectrum.
- No tutorial band gap is used as a validation oracle.

## Historical source

No archived source.
