# Aluminum metal tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.aluminum-metal`
- **Status:** `blocked`
- **Status detail:** Planned learning candidate; blocked pending exact multi-stage inputs, pseudopotential, dense-grid resource estimate, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the aluminum VC-relax, metallic SCF/NSCF, DOS, and bands tutorial as learning-only behavior outside the project's material scope.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Preflight the Al pseudopotential, smearing settings, 40-cubed NSCF mesh, and all postprocessing stages.
- Run only approved pw.x, dos.x, and bands.x stages in an isolated workspace.
- Capture per-stage snapshots, separate streams, exits, runtime, and artifact transitions.

## Completion criteria

- Resource estimates explicitly cover the dense NSCF stage.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable workflow lessons without extending scientific scope.

## Exclusions

- Aluminum is learning-only and does not become a supported project material.
- PWTK smearing sweeps are excluded unless separately authorized.
- No tutorial lattice or electronic result is scientifically accepted.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
