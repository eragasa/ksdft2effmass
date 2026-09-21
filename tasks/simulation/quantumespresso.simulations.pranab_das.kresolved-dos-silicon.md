# Silicon k-resolved DOS tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.kresolved-dos-silicon`
- **Status:** `blocked`
- **Status detail:** Planned candidate; blocked pending complete source inputs, pseudopotential, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the silicon bands-to-projwfc.x k-resolved DOS workflow and inventory its projection artifacts.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.bands-silicon`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Resolve the page's externally referenced SCF and doubled-path inputs before activation.
- Run only authorized pw.x SCF/bands and projwfc.x stages.
- Capture snapshots, separate streams, exits, runtime, and k-resolved projection outputs.

## Completion criteria

- All omitted inputs are recovered and pinned or the Task is explicitly deferred.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records projection and indexing conventions without scientific-validation claims.

## Exclusions

- No input is inferred silently from a different tutorial version.
- No orbital projection is treated as basis independent.
- No plotting output is required.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
