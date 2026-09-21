# Bi2Se3 bulk, SOC, slab, and DOS tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.bi2se3`
- **Status:** `blocked`
- **Status detail:** Planned high-cost learning candidate; blocked pending complete inputs, relativistic pseudopotentials, 24-rank resource review, and execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the Bi2Se3 bulk, SOC, slab, dense-DOS, and postprocessed-bands tutorial branches as high-cost learning evidence.

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

- Preflight each branch independently, including slab size, vacuum, odd dense DOS mesh, disk, memory, and 24-rank commands.
- Run only separately approved pw.x, bands.x, and dos.x stages.
- Capture branch- and stage-level snapshots, separate streams, exits, runtimes, and artifacts.

## Completion criteria

- Bulk, SOC, slab, and DOS branches each receive an explicit execute or defer disposition.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Known tutorial caveats about finite size and Fermi energy remain visible.

## Exclusions

- Bi2Se3 does not enter supported project scope.
- The 24-rank example is not itself resource authorization.
- No topological, surface-state, or finite-size scientific claim is validated.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
