<!-- Generated from SQLite control state; do not edit. -->
# Silicon joint-density-of-states tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.integration.md) · [Next](./quantumespresso.simulations.kresolved-dos-silicon.md)

## Status

`blocked`: Planned candidate after dielectric preflight; blocked pending exact NSCF/JDOS inputs, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the silicon SCF/NSCF-to-epsilon.x JDOS branch separately from the dielectric-function workflow.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.dielectric-silicon`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Recover and preflight the page's referenced NSCF input and 16-rank example resource needs.
- Run only authorized pw.x SCF/NSCF and epsilon.x JDOS stages.
- Capture snapshots, separate streams, exits, runtime, and JDOS data artifacts.

## Completion criteria

- The relationship to dielectric inputs and all intentional differences are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition labels the JDOS output tutorial software behavior.

## Exclusions

- The 16-rank example is not itself resource authorization.
- No JDOS spectrum is scientifically validated or treated as converged.
- No implicit reuse of mutable dielectric workspace state is permitted.

## Historical source

No archived source.
