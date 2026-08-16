<!-- Generated from SQLite control state; do not edit. -->
# Aluminum metal tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.md) · [Next](./quantumespresso.simulations.bands-gaas.md)

## Status

`blocked`: Planned learning candidate; blocked pending exact multi-stage inputs, pseudopotential, dense-grid resource estimate, and execution authorization.

## Objective

Reproduce or explicitly defer the aluminum VC-relax, metallic SCF/NSCF, DOS, and bands tutorial as learning-only behavior outside the project's material scope.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight the Al pseudopotential, smearing settings, 40-cubed NSCF mesh, and all postprocessing stages.
- Run only approved pw.x, dos.x, and bands.x stages in an isolated workspace.
- Capture per-stage snapshots, separate streams, exits, runtime, and artifact transitions.

## Completion criteria

- Resource estimates explicitly cover the dense NSCF stage.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable workflow lessons without extending scientific scope.

## Exclusions

- Aluminum is learning-only and does not become a supported project material.
- PWTK smearing sweeps are excluded unless separately authorized.
- No tutorial lattice or electronic result is scientifically accepted.

## Historical source

No archived source.
