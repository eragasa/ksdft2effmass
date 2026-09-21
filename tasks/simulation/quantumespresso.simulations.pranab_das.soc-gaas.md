# GaAs spin-orbit-coupling tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.soc-gaas`
- **Status:** `blocked`
- **Status detail:** Planned learning-only candidate; blocked pending complete SOC inputs, fully relativistic pseudopotentials, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the GaAs fully relativistic SCF/bands/bands.x tutorial branch.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.bands-gaas`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Recover and pin all GaAs SOC inputs and both relativistic pseudopotentials.
- Run only authorized pw.x SCF/bands and bands.x stages.
- Capture snapshots, separate streams, exits, runtime, and represented SOC band artifacts.

## Completion criteria

- The relationship to the non-SOC GaAs workflow is explicit and compatible comparisons are guarded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records workflow lessons without supporting a GaAs scientific claim.

## Exclusions

- GaAs SOC does not enter supported project scope.
- No comparison is made across unmatched pseudopotential or basis conventions.
- No tutorial band splitting is a validation oracle.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
