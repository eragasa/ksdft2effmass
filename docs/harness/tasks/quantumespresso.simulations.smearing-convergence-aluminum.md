<!-- Generated from SQLite control state; do not edit. -->
# Aluminum smearing-convergence tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.scf-silicon.md) · [Next](./quantumespresso.simulations.soc-gaas.md)

## Status

`blocked`: Planned learning-only candidate split from the aluminum page; blocked pending aluminum baseline, PWTK decision, exact sweep inventory, resource estimate, and execution authorization.

## Objective

Reproduce or explicitly defer the aluminum PWTK k-mesh, smearing-function, and degauss convergence workflow as a distinct learning disposition from the baseline aluminum calculation.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.aluminum-metal`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `pwtk_tool_selection_and_authorization`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Recover and pin the complete PWTK sweep definition, every mesh, smearing function, degauss value, and expected stage count.
- Estimate cumulative CPU, memory, disk, and runtime before authorizing any sweep point.
- Run only explicitly authorized PWTK and pw.x stages in isolated per-point workspaces with independent attempts.
- Capture per-point snapshots, separate streams, terminal records, runtimes, failures, and compact energy observations.

## Completion criteria

- Every planned sweep point is enumerated and receives an executed, failed, or deliberate-deferral disposition.
- Every attempted point has separate stdout/stderr, available before/after manifests, and a terminal process record.
- Partial completion and failed points remain visible rather than being omitted from the reported trend.
- The disposition states that this tutorial sweep is not accepted production convergence evidence.

## Exclusions

- PWTK is not installed, added, or invoked without separate tool and dependency/licensing authorization.
- Aluminum does not become a supported project material.
- No production smearing, mesh, cutoff, or convergence policy is selected.
- Expected values, omitted points, and plotting choices are not changed to obtain a preferred trend.

## Historical source

No archived source.
