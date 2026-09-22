# Copper Fermi-surface tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.fermi-surface-copper`
- **Status:** `blocked`
- **Status detail:** Planned learning-only candidate; blocked pending ONCV pseudopotential, dense-grid resource estimate, fs.x availability, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the copper SCF, 30-cubed uniform bands, and fs.x Fermi-surface tutorial as learning-only behavior.

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

- Preflight the copper ONCV pseudopotential, smearing, dense mesh, storage, and fs.x output.
- Run only authorized pw.x SCF/bands and fs.x stages.
- Capture snapshots, separate streams, exits, runtime, and BXSF artifacts.

## Completion criteria

- Dense-grid runtime, memory, and disk estimates precede activation.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable artifact behavior or deliberate deferral.

## Exclusions

- Copper does not become a supported project material.
- XCrySDen GUI execution is excluded.
- No Fermi-surface topology is scientifically validated.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
