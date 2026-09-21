# Silicon density-of-states tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.dos-silicon`
- **Status:** `completed`
- **Status detail:** Checkpoint QE-SILICON-DOS-RUN-HC01 Option A authorized Workflow qe-7.5-silicon-dos-20260903T102922Z. The independent SCF, NSCF, and DOS Task processes each exited 0 and printed `JOB DONE.`; distinct activations, attempts, consumed grants, process observations, result ingresses, and CPN firings are retained. Exact immutable state-copy identities were verified before both downstream Tasks. The admitted DOS artifact has SHA-256 b967ed73c7d2572123dbf0b928630e38868ad2f9afbb1b3e77f140ecd53bf6df and 2,501 finite data rows. No retry or repeat execution is authorized, and no project geometry, reference DOS, convergence study, numerical verification, scientific validation, or UQ claim is made.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Compose three independent reusable CPN Task instances for the silicon SCF, NSCF, and dos.x operations, then reproduce or explicitly defer the tutorial workflow and inventory its immutable cross-Task artifact handoffs.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`
- `quantumespresso.simulations.pranab_das.structure-optimization-silicon`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `simulation_input_selection`
- `tutorial_source_reuse_terms_resolved`

### Superseded by

- None.

## Authorized scope

- Preflight compatible prefix/outdir, tetrahedron occupation, dense mesh, and band-count inputs.
- Bind the retained calculated structure-optimization ResultObject and QEXSD-derived 10.207479550732002 Bohr tutorial geometry to the DOS Workflow, and construct exact adapted SCF and NSCF input identities without changing any other pinned scientific setting.
- Define and software-verify independent private reusable SCF, NSCF, and DOS CPN Task contracts and their effect-free composition without invoking a scientific executable.
- Run only separately dispatched and authorized pw.x SCF, pw.x NSCF, and dos.x Task instances.
- Capture per-Task snapshots, separate streams, exits, runtime, immutable predecessor-state handoffs, and DOS data artifacts.

## Completion criteria

- The reusable CPN composition contains distinct SCF, NSCF, and DOS Task instances with separate activations, attempts, grants, result ingresses, and failure boundaries.
- Cross-Task artifact dependencies, exact inputs, and identity-checked immutable native-state copies are recorded.
- Every attempted Task has a private workspace plus separate stdout/stderr and before/after snapshots.
- The final disposition identifies useful parser behavior without convergence or validation claims.

## Exclusions

- No monolithic SCF-to-DOS shell-sequence Task is permitted.
- No DOS curve is accepted as a project reference.
- No Task mutates another Task's workspace or shares a mutable prefix or outdir.
- No interactive plotting program is required.

## Authority references

- `.pi/checkpoints/qe-silicon-dos-geometry-selection.json`
- `.pi/checkpoints/qe-silicon-dos-input-selection.json`
- `.pi/checkpoints/qe-silicon-dos-workflow-execution.json`
- `docs/architecture/v2/ksdft2effmass/workflows/dft-simulation-cpn-service-decision.md`
- `docs/architecture/v2/ksdft2effmass/workflows/simulation-task-model.md`
- `docs/computational/quantumespresso.simulations.pranab_das.md`
- `docs/computational/silicon-scf-nscf-dos-preflight.md`
- `examples/tutorials/silicon-dos/qe/expected/qe75-calculated-observation.json`
