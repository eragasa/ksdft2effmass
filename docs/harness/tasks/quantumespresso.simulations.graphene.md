<!-- Generated from SQLite control state; do not edit. -->
# Graphene DOS and bands tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.fermi-surface-copper.md) · [Next](./quantumespresso.simulations.integration.md)

## Status

`blocked`: Planned learning-only candidate outside project material scope; blocked pending complete inputs, pseudopotential, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the graphene SCF, NSCF, DOS, and bands tutorial solely to learn workflow and low-dimensional artifact behavior.

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

- Recover and pin the page's externally referenced graphene inputs.
- Run only authorized pw.x SCF/NSCF/bands, dos.x, and bands.x stages.
- Capture per-stage snapshots, separate streams, exits, runtime, and artifacts.

## Completion criteria

- Low-dimensional boundary settings and exact inputs are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable software behavior or an explicit deferral.

## Exclusions

- Graphene does not become a supported project material.
- No graphene physical claim or scientific validation is made.
- No tutorial input is silently repaired or completed.

## Historical source

No archived source.
