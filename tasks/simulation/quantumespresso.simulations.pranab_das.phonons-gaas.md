# GaAs phonon tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.phonons-gaas`
- **Status:** `blocked`
- **Status detail:** Planned default-defer learning candidate; blocked pending mixed-pseudopotential review, day-scale resource authorization, and execution checkpoint.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Preflight and either explicitly defer or reproduce the GaAs pw.x/ph.x/q2r.x/matdyn.x phonon-dispersion and DOS tutorial as out-of-scope learning evidence.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.bands-gaas`

### External prerequisites

- `local_execution_resource_authorization`
- `phonon_scope_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Review mixed pseudopotential representations, 6-cubed q mesh, restart policy, disk, and source-reported day-scale runtime.
- Run only separately authorized pw.x, ph.x, q2r.x, and matdyn.x stages.
- Capture snapshots, separate streams, exits, runtimes, restart state, dynamical matrices, force constants, and frequencies.

## Completion criteria

- A resource and scope disposition is recorded before any ph.x invocation.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Any frequencies remain tutorial observations without validation claims.

## Exclusions

- Phonons and electron-phonon behavior remain outside project scientific scope.
- Default disposition is deferral unless the exact day-scale run is separately authorized.
- No imaginary-frequency or convergence interpretation is scientifically accepted.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
