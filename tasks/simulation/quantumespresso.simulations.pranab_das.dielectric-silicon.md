# Silicon dielectric-function tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.dielectric-silicon`
- **Status:** `blocked`
- **Status detail:** Planned candidate; blocked pending norm-conserving pseudopotential, exact full-grid inputs, epsilon.x availability, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the silicon full-k-grid SCF and epsilon.x dielectric-function tutorial workflow.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.scf-silicon`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Preflight norm-conserving pseudopotential compatibility, no-symmetry grid, band count, broadening, and energy grid.
- Run only authorized pw.x SCF/optional NSCF and epsilon.x dielectric stages.
- Capture snapshots, separate streams, exits, runtime, and epsilon data artifacts.

## Completion criteria

- The exact grid, symmetry, band, broadening, and pseudopotential conditions are recorded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition labels results unconverged tutorial behavior.

## Exclusions

- No ultrasoft pseudopotential is substituted into epsilon.x.
- No dielectric spectrum is scientifically validated or treated as converged.
- No source-code recompilation to raise k-point limits is authorized.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
