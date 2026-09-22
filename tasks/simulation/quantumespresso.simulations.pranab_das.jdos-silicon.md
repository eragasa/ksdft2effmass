# Silicon joint-density-of-states tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.jdos-silicon`
- **Status:** `blocked`
- **Status detail:** Planned candidate after dielectric preflight; blocked pending exact NSCF/JDOS inputs, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the silicon SCF/NSCF-to-epsilon.x JDOS branch separately from the dielectric-function workflow.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.dielectric-silicon`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Recover and preflight the page's referenced NSCF input and 16-rank example resource needs.
- Run only authorized pw.x SCF/NSCF and epsilon.x JDOS stages.
- Capture snapshots, separate streams, exits, runtime, and JDOS data artifacts.

## Completion criteria

- The relationship to dielectric inputs and all intentional differences are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition labels the JDOS output tutorial software behavior.

## Exclusions

- The 16-rank example is not itself resource authorization.
- No JDOS spectrum is scientifically validated or treated as converged.
- No implicit reuse of mutable dielectric workspace state is permitted.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
