<!-- Generated from SQLite control state; do not edit. -->
# Water molecular-dynamics tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.magnetism-iron.md) · [Next](./quantumespresso.simulations.pdos-aluminum.md)

## Status

`blocked`: Planned learning-only candidate outside project scope; blocked pending prerequisite relaxation, mixed pseudopotentials, 100-step resource estimate, and execution authorization.

## Objective

Preflight and either explicitly defer or reproduce the relaxed-water 100-step pw.x molecular-dynamics tutorial as execution-state learning evidence.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `molecular_dynamics_scope_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Recover and authorize the omitted prerequisite relaxation and exact H/O pseudopotentials.
- Run only separately authorized relaxation and 100-step pw.x MD stages.
- Capture snapshots, separate streams, exits, runtime, trajectory, force, stress, and restart artifacts.

## Completion criteria

- The prerequisite relaxed structure and MD integration settings are provenance-complete.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The Task records a learning or deferral disposition without molecular-dynamics validation claims.

## Exclusions

- Molecular dynamics and water remain outside project scientific scope.
- The page's displayed relaxed structure is not silently accepted as an independently produced prerequisite.
- No trajectory is interpreted as equilibrated or physically validated.

## Historical source

No archived source.
