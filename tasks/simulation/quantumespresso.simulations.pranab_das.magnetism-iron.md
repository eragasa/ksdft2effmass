# Magnetic iron tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.magnetism-iron`
- **Status:** `blocked`
- **Status detail:** Planned learning-only candidate; blocked pending FM/AFM inputs, ultrasoft pseudopotential, optional PWTK decision, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the FM/AFM iron, optional cutoff-dual sweeps, DOS, and projected-DOS tutorial as magnetic-workflow learning evidence.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`

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

- Preflight distinct FM/AFM structures, starting magnetizations, ultrasoft cutoff ratios, and sweep cost.
- Run only separately approved pw.x, dos.x, projwfc.x, and optional PWTK stages.
- Capture snapshots, separate streams, exits, runtimes, and magnetic/DOS artifacts.

## Completion criteria

- Every magnetic initial condition and attempted sweep point is explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The costly sweep receives an execute or defer disposition before launch.

## Exclusions

- Iron does not become a supported project material.
- PWTK use is separately authorized and may be deferred.
- Ground-state or magnetic-order claims are not scientifically validated.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
