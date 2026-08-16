<!-- Generated from SQLite control state; do not edit. -->
# Silicon tutorial convergence sweeps

[Task index](index.md) · [Previous](./quantumespresso.simulations.bi2se3.md) · [Next](./quantumespresso.simulations.dftu-feo.md)

## Status

`blocked`: Planned candidate after baseline SCF; blocked pending tool, source, input, pseudopotential, resource, and execution authorization.

## Objective

Reproduce or explicitly defer the tutorial cutoff, k-mesh, and lattice-parameter SCF sweeps while keeping tutorial observations separate from project convergence evidence.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- Depends on: `quantumespresso.simulations.scf-silicon`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `pwtk_tool_selection_and_authorization`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight every sweep point and the PWTK or explicit-command orchestration choice.
- Run only approved repeated pw.x SCF stages in isolated per-point workspaces.
- Capture snapshots, streams, exits, runtimes, and the resulting compact energy tables.

## Completion criteria

- Every attempted sweep point has exact provenance and separate stream files.
- Failed, missing, and completed points remain visible in the artifact inventory.
- The disposition states that tutorial sweeps are not accepted production convergence evidence.

## Exclusions

- No PWTK installation or use occurs without separate dependency/tool authorization.
- No expected values or tolerances are changed to obtain a preferred trend.
- No production cutoff, mesh, lattice, or convergence setting is selected by this Task.

## Historical source

No archived source.
