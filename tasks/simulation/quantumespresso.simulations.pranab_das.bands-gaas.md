# GaAs bandstructure tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.bands-gaas`
- **Status:** `completed`
- **Status detail:** Human response `A` resolved checkpoint QE-GAAS-BANDS-RUN-HC01 before execution. One exact local one-process QE 7.5 attempt completed without retry: SCF returned zero, contained JOB DONE., reported convergence in 27 iterations, and produced admitted QEXSD 25.05.21 state. A content-identical native-state copy entered the bands stage, which generated 91 path points but returned 1 after nine c_bands eigenvalue-nonconvergence diagnostics and the fatal message `too many bands are not converged`; it did not produce an admitted bands result. The dependent bands.x stage was explicitly unattempted. The attempted stages stayed within the resource envelopes. This is a completed failure disposition and learning-only Workflow observation, not GaAs convergence, scientific validation, or an aligned SOC comparator; no retry or setting change is authorized.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the GaAs relaxation, SCF, optional NSCF, bands, and bands.x tutorial workflow as compound-semiconductor learning evidence.

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

- Recover and pin every GaAs input and both pseudopotential identities.
- Run only authorized pw.x relaxation/SCF/NSCF/bands and bands.x stages.
- Capture per-stage snapshots, separate streams, exits, runtime, and artifacts.

## Completion criteria

- Version-sensitive convergence behavior and all exact inputs are recorded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records software lessons without adding GaAs to project scope.

## Exclusions

- GaAs does not become a supported project material.
- No tutorial bandstructure is a scientific oracle.
- The separate SOC and phonon branches are owned by their own Tasks.

## Authority references

- `.pi/checkpoints/qe-gaas-bands-execution.json`
- `docs/computational/gaas-bands-preflight.md`
- `docs/computational/quantumespresso.simulations.pranab_das.md`
- `examples/tutorials/gaas-bands/README.md`
