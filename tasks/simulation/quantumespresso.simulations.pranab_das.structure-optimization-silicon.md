# Silicon structure-optimization tutorial simulation

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das.structure-optimization-silicon`
- **Status:** `completed`
- **Status detail:** Checkpoint QE-SILICON-VCRELAX-RUN-HC01 Option A authorized one exact isolated QE 7.5 pw.x variable-cell-relaxation Task, which completed once without retry on 2026-09-03 with exit 0 and JOB DONE. QE reported BFGS convergence after 14 SCF cycles and 12 BFGS steps; the QEXSD final cell implies a 10.207479550732002 Bohr conventional cubic lattice constant. The distinct final SCF reported convergence, while intermediate stdout retained six BFGS curvature warnings and fourteen c_bands one-eigenvalue-not-converged messages; stderr retained IEEE floating-point exception flags. Compact provenance and observation are retained, with native state external. This calculated tutorial result is not production convergence, numerical verification, scientific validation, uncertainty quantification, or a project lattice reference. Checkpoint QE-SILICON-DOS-GEOMETRY-HC01 later selected the QEXSD-derived geometry only for the bounded tutorial DOS Workflow, which completed under separate checkpoint QE-SILICON-DOS-RUN-HC01.
- **Parent Task:** `quantumespresso.simulations.pranab_das`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Reproduce or explicitly defer the silicon pw.x variable-cell relaxation tutorial and observe its native structural outputs and failure boundaries.

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

- Preflight the fixed-position VC-relax input and cell_dofree convention.
- Represent VC-relax as one independent reusable CPN Task instance with its own activation, attempt, grant, workspace, process observation, result ingress, and failure boundary.
- Run only the separately authorized pw.x VC-relax Task.
- Capture final-coordinate artifacts, snapshots, streams, exit state, and runtime.

## Completion criteria

- Input and structure conventions are explicit and provenance-complete.
- Any attempted relaxation has one independently correlated CPN Task result, distinct stdout/stderr, and before/after snapshots.
- Observed final coordinates are labeled tutorial results rather than accepted geometry.
- Any downstream DOS use requires a separate human geometry decision; QE-SILICON-DOS-GEOMETRY-HC01 records the bounded tutorial selection.

## Exclusions

- No tutorial-relaxed geometry is promoted to a project structure.
- No convergence tolerance is changed without separate authority.
- No production or remote execution occurs.

## Authority references

- `.pi/checkpoints/qe-silicon-dos-geometry-selection.json`
- `.pi/checkpoints/qe-silicon-dos-input-selection.json`
- `.pi/checkpoints/qe-silicon-dos-workflow-execution.json`
- `.pi/checkpoints/qe-silicon-structure-optimization-execution.json`
- `docs/architecture/v2/ksdft2effmass/workflows/simulation-task-model.md`
- `docs/computational/quantumespresso.simulations.pranab_das.md`
- `docs/computational/silicon-structure-optimization-preflight.md`
- `examples/tutorials/silicon-structure-optimization/qe/expected/qe75-calculated-observation.json`
