# Silicon bandstructure tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.bands-silicon`
- **Status:** `deferred`
- **Status detail:** Checkpoint PAIRED-SILICON-BANDS-RUN-HC01 authorized the exact staged QE 7.5 SCF, bands, and bands.x sequence. All three processes completed once with exit 0; 72 path points with eight bands, raw symmetry-representation indices, IEEE diagnostics, and bands-mode QEXSD semantics were processed as a tutorial observation. Only workflow-level pre/post inventories were captured, not the required before/after snapshot for every stage. The human-selected disposition is deliberate no-rerun deferral rather than completion. The calculated observation remains usable only within its recorded claim boundary; this disposition does not satisfy the snapshot criterion or establish software verification, numerical verification, scientific validation, uncertainty quantification, or scientific acceptance. Any repeat requires separate protected-execution authorization.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the silicon pw.x SCF and line-mode bands workflow with bands.x postprocessing.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.scf-silicon`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Preflight the tutorial's distinct SCF settings and L-Gamma-X-Gamma path, including its explicit zero-length path discontinuity between (0,1,0) and (1,1,0) in Cartesian 2*pi/alat coordinates.
- Run only authorized pw.x SCF, pw.x bands, and bands.x stages.
- Capture per-stage snapshots, separate streams, exits, runtime, and represented band-data artifacts.

## Completion criteria

- The path convention, energy reference, exact inputs, and cross-stage dependencies are explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Band outputs are labeled tutorial software behavior, not an accepted spectral reference.

## Exclusions

- Interactive plotband.x execution is excluded.
- Kohn-Sham eigenvalues are not identified with a complete excitation spectrum.
- No tutorial band gap is used as a validation oracle.

## Authority references

- `docs/computational/paired-silicon-scf-bands-preflight.md`
- `docs/computational/quantumespresso.simulations.pranab_das.md`
