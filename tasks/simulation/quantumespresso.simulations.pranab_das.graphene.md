# Graphene DOS and bands tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.graphene`
- **Status:** `blocked`
- **Status detail:** Planned learning-only candidate outside project material scope; blocked pending complete inputs, pseudopotential, resources, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the graphene SCF, NSCF, DOS, and bands tutorial solely to learn workflow and low-dimensional artifact behavior.

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

- Recover and pin the page's externally referenced graphene inputs.
- Run only authorized pw.x SCF/NSCF/bands, dos.x, and bands.x stages.
- Capture per-stage snapshots, separate streams, exits, runtime, and artifacts.

## Completion criteria

- Low-dimensional boundary settings and exact inputs are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable software behavior or an explicit deferral.

## Exclusions

- Graphene does not become a supported project material.
- No graphene physical claim or scientific validation is made.
- No tutorial input is silently repaired or completed.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
