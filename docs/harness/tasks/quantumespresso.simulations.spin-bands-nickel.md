<!-- Generated from SQLite control state; do not edit. -->
# Spin-polarized nickel bands tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.soc-iron.md) · [Next](./quantumespresso.simulations.structure-optimization-silicon.md)

## Status

`blocked`: Planned learning-only candidate; blocked pending complete inputs, pseudopotential, eight-rank resource review, and execution authorization.

## Objective

Reproduce or explicitly defer the nickel spin-polarized SCF/bands workflow and separate spin-component bands.x postprocessing.

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

- Recover and pin all Ni inputs and pseudopotential identity.
- Run only authorized pw.x SCF/bands and spin-component bands.x stages.
- Capture snapshots, separate streams, exits, runtime, and spin-resolved band artifacts.

## Completion criteria

- Spin conventions, components, inputs, and executable version are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records parser/interface lessons or deliberate deferral.

## Exclusions

- Nickel does not become a supported project material.
- Spin-resolved bands are not scientifically validated.
- The tutorial's eight-rank command is not authority for a resource request.

## Historical source

No archived source.
