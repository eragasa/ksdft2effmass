# FeO DFT+U tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.dftu-feo`
- **Status:** `blocked`
- **Status detail:** Planned high-risk learning candidate; blocked pending QE-version syntax, inputs, pseudopotentials, Hubbard policy, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the FeO DFT, DFT+U, projected-DOS, and optional hp.x self-consistent-Hubbard workflow as learning-only behavior.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`

### External prerequisites

- `dftu_hubbard_parameter_policy`
- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Resolve QE pre-7.1 versus 7.1-plus Hubbard syntax and exact FeO inputs.
- Run only individually approved pw.x, projwfc.x, and optional hp.x stages.
- Capture iteration-level snapshots, separate streams, exits, runtimes, Hubbard artifacts, and local-minimum observations.

## Completion criteria

- The baseline, DFT+U, and hp.x branches each receive an explicit run or defer disposition.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Reported Hubbard values remain tutorial outputs tied to exact pseudopotentials and manifolds.

## Exclusions

- The hp.x iteration is deferred by default pending a bounded stopping rule and resource estimate.
- FeO and DFT+U do not enter supported project scope.
- No Hubbard parameter or insulating-state claim is scientifically accepted.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
