# Superseded combined silicon tutorial convergence sweeps

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.convergence-silicon`
- **Status:** `superseded`
- **Status detail:** Superseded by the human-selected separation into independent wavefunction-cutoff and reciprocal-cell-volume-normalized k-point convergence Tasks. No calculation executed under the combined Task.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Retain the superseded combined convergence scope and route any future work to its two explicitly separated successor Tasks.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.scf-silicon`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `pwtk_tool_selection_and_authorization`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- `quantumespresso.simulations.pranab_das.convergence-silicon-cutoff`
- `quantumespresso.simulations.pranab_das.convergence-silicon-kpoint-density`

## Authorized scope

- Preserve the historical combined scope without executing it.
- Route wavefunction-cutoff and reciprocal-cell-volume-normalized k-point work to the two successor Tasks and their separate tutorial directories.

## Completion criteria

- The two successor Tasks and separate tutorial directory identities are explicit.
- No execution or result is attributed to this superseded combined Task.

## Exclusions

- No scientific executable, PWTK tool, combined sweep, or lattice-parameter scan is authorized by this superseded Task.
- No production cutoff, mesh, lattice, or convergence setting is selected by this Task.

## Authority references

- `docs/computational/quantumespresso.simulations.pranab_das.md`
