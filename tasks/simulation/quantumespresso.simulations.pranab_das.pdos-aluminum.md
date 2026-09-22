# Aluminum projected-DOS tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.pdos-aluminum`
- **Status:** `blocked`
- **Status detail:** Planned learning candidate after aluminum preflight; blocked pending inputs, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the aluminum SCF/NSCF-to-projwfc.x projected-DOS workflow and its artifact naming behavior.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.aluminum-metal`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Preflight reused or independently repeated aluminum state and projection inputs.
- Run only authorized pw.x SCF/NSCF, projwfc.x, and optional sumpdos.x stages.
- Capture snapshots, separate streams, exits, runtime, and orbital-projection artifacts.

## Completion criteria

- The pseudopotential-owned projection basis and file naming are recorded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition distinguishes parser behavior from physical interpretation.

## Exclusions

- Projected DOS is not treated as a basis-independent observable.
- Aluminum remains outside supported material scope.
- No plotting step is required for completion.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
