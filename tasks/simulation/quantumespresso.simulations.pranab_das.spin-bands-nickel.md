# Spin-polarized nickel bands tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.spin-bands-nickel`
- **Status:** `completed`
- **Status detail:** Human response `A` resolved checkpoint QE-NICKEL-SPIN-BANDS-RUN-HC01 before execution. One exact local one-process QE 7.5 Workflow then attempted SCF, bands, spin-component 1 bands.x, and spin-component 2 bands.x once each. All returned zero, contained JOB DONE., stayed within the authorized envelopes, and used content-identical admitted native-state copies. The retained calculated tutorial observation records 71 path points, 10 bands per collinear component, and agreement of both bands.x outputs with the corresponding QEXSD eigenvalues within 0.001-eV printed precision. This is learning-only Workflow evidence, not nickel scientific validation or convergence.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the nickel spin-polarized SCF/bands workflow and separate spin-component bands.x postprocessing.

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

- Recover and pin all Ni inputs and pseudopotential identity.
- Run only authorized pw.x SCF/bands and spin-component bands.x stages.
- Capture snapshots, separate streams, exits, runtime, and spin-resolved band artifacts.

## Completion criteria

- Spin conventions, components, inputs, and executable version are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records parser/interface lessons or deliberate deferral.

## Exclusions

- Nickel does not become a supported project material.
- Spin-resolved bands are not scientifically validated.
- The tutorial's eight-rank command is not authority for a resource request.

## Authority references

- `.pi/checkpoints/qe-nickel-spin-bands-execution.json`
- `docs/computational/nickel-spin-bands-preflight.md`
- `docs/computational/quantumespresso.simulations.pranab_das.md`
- `examples/tutorials/nickel-spin-bands/README.md`
