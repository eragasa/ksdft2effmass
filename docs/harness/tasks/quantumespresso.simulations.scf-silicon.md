<!-- Generated from SQLite control state; do not edit. -->
# Silicon SCF tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.review.md) · [Next](./quantumespresso.simulations.smearing-convergence-aluminum.md)

## Status

`blocked`: Planned first low-cost candidate; blocked pending source-reuse, exact input, pseudopotential, executable/resource, and protected-execution authorization.

## Objective

Reproduce or explicitly defer the pinned two-atom diamond-silicon pw.x SCF tutorial as the campaign baseline.

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

- Preflight the pinned silicon SCF input and Si.pz-vbc.UPF identity.
- Run only the authorized pw.x SCF stage in an isolated workspace.
- Capture the required snapshots, streams, exit record, runtime, and native artifact inventory.

## Completion criteria

- The exact input, executable, pseudopotential, resources, and retention policy are recorded.
- Any attempted stage has separate stdout/stderr and before/after snapshots.
- The Task records an executed, failed, or deliberate-deferral disposition without scientific acceptance claims.

## Exclusions

- No execution occurs before the exact protected checkpoint.
- Tutorial energies and gaps are illustrative rather than acceptance oracles.
- No tutorial setting becomes a production silicon setting.

## Historical source

No archived source.
