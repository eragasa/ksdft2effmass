# Silicon tutorial wavefunction-cutoff convergence

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.convergence-silicon-cutoff`
- **Status:** `completed`
- **Status detail:** Human response `a authorized` resolved checkpoint QE-SILICON-CUTOFF-CONVERGENCE-RUN-HC01 as Option A. One exact local QE 7.5 attempt completed on 2026-09-08 without retry: all six independent ecutwfc points returned zero, contained JOB DONE., reported SCF convergence after four iterations, and produced identity-bound QEXSD 25.05.21 state. Total energies from 12 through 32 Ry are retained in the compact calculated observation. Every stderr stream retained the same uncharacterized 139-byte floating-point exception note. Peak resident memory was not measured. This tutorial curve neither selects a production cutoff nor establishes an infinite-basis limit, numerical verification, scientific validation, uncertainty quantification, or scientific acceptance.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Execute or explicitly defer the silicon tutorial wavefunction-cutoff SCF sequence and retain one compact energy-versus-cutoff table without selecting a production cutoff.

## Relationships

### Task prerequisites

- `P2`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Preflight the six tutorial ecutwfc candidates 12, 16, 20, 24, 28, and 32 Ry with every other represented scientific setting fixed.
- When separately authorized, attempt every independent pw.x SCF point once in its own isolated workspace even if another point fails.
- Retain exact input and dependency identities, separate streams, snapshots, exits, runtimes, calculator convergence facts, and one point-indexed energy table.

## Completion criteria

- Every attempted, failed, and systemically unattempted cutoff point remains explicit with exact provenance.
- The compact table records ecutwfc, total energy when available, process and calculator status, diagnostics, and runtime.
- The disposition states that the tutorial curve is not accepted production convergence evidence.

## Exclusions

- No PWTK installation or invocation is authorized.
- No k-mesh, lattice-parameter, structural-relaxation, spin, or SOC sweep belongs to this Task.
- No expected value or tolerance is changed to obtain a preferred trend, and no production cutoff is selected.

## Authority references

- `.pi/checkpoints/qe-silicon-cutoff-convergence-execution.json`
- `docs/architecture/v2/tutorial-examples.md`
- `docs/computational/quantumespresso.simulations.pranab_das.md`
- `docs/computational/silicon-wavefunction-cutoff-convergence-preflight.md`
- `examples/tutorials/silicon-wavefunction-cutoff-convergence/README.md`
- `examples/tutorials/silicon-wavefunction-cutoff-convergence/qe/expected/qe75-calculated-observation.json`
