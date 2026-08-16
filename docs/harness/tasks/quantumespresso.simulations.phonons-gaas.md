<!-- Generated from SQLite control state; do not edit. -->
# GaAs phonon tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.pdos-aluminum.md) · [Next](./quantumespresso.simulations.review.md)

## Status

`blocked`: Planned default-defer learning candidate; blocked pending mixed-pseudopotential review, day-scale resource authorization, and execution checkpoint.

## Objective

Preflight and either explicitly defer or reproduce the GaAs pw.x/ph.x/q2r.x/matdyn.x phonon-dispersion and DOS tutorial as out-of-scope learning evidence.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.bands-gaas`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `phonon_scope_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Review mixed pseudopotential representations, 6-cubed q mesh, restart policy, disk, and source-reported day-scale runtime.
- Run only separately authorized pw.x, ph.x, q2r.x, and matdyn.x stages.
- Capture snapshots, separate streams, exits, runtimes, restart state, dynamical matrices, force constants, and frequencies.

## Completion criteria

- A resource and scope disposition is recorded before any ph.x invocation.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Any frequencies remain tutorial observations without validation claims.

## Exclusions

- Phonons and electron-phonon behavior remain outside project scientific scope.
- Default disposition is deferral unless the exact day-scale run is separately authorized.
- No imaginary-frequency or convergence interpretation is scientifically accepted.

## Historical source

No archived source.
