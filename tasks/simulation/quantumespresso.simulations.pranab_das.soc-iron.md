# Iron spin-orbit-coupling tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.soc-iron`
- **Status:** `blocked`
- **Status detail:** Planned learning-only candidate; blocked pending fully relativistic pseudopotential, inputs, resource estimate, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the noncollinear fully relativistic Fe SCF/bands/bands.x tutorial workflow.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.magnetism-iron`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Preflight relativistic representation, noncollinear settings, high cutoffs, dense mesh, and eight-rank resource request.
- Run only authorized pw.x SCF/bands and bands.x stages.
- Capture snapshots, separate streams, exits, runtime, spin-expectation artifacts, and convergence behavior.

## Completion criteria

- Relativistic pseudopotential and spin conventions are provenance-complete.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable behavior or a resource/scientific-scope deferral.

## Exclusions

- Iron SOC does not enter supported project scope.
- No tutorial spin texture or band result is scientifically validated.
- No pseudopotential substitution is made for convenience.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
