# Aluminum smearing-convergence tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.smearing-convergence-aluminum`
- **Status:** `blocked`
- **Status detail:** Planned learning-only candidate split from the aluminum page; blocked pending aluminum baseline, PWTK decision, exact sweep inventory, resource estimate, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the aluminum PWTK k-mesh, smearing-function, and degauss convergence workflow as a distinct learning disposition from the baseline aluminum calculation.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.aluminum-metal`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `pwtk_tool_selection_and_authorization`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

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

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
