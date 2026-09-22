# Water molecular-dynamics tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.molecular-dynamics-water`
- **Status:** `blocked`
- **Status detail:** Planned learning-only candidate outside project scope; blocked pending prerequisite relaxation, mixed pseudopotentials, 100-step resource estimate, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Preflight and either explicitly defer or reproduce the relaxed-water 100-step pw.x molecular-dynamics tutorial as execution-state learning evidence.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`

### External prerequisites

- `local_execution_resource_authorization`
- `molecular_dynamics_scope_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Recover and authorize the omitted prerequisite relaxation and exact H/O pseudopotentials.
- Run only separately authorized relaxation and 100-step pw.x MD stages.
- Capture snapshots, separate streams, exits, runtime, trajectory, force, stress, and restart artifacts.

## Completion criteria

- The prerequisite relaxed structure and MD integration settings are provenance-complete.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The Task records a learning or deferral disposition without molecular-dynamics validation claims.

## Exclusions

- Molecular dynamics and water remain outside project scientific scope.
- The page's displayed relaxed structure is not silently accepted as an independently produced prerequisite.
- No trajectory is interpreted as equilibrated or physically validated.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
