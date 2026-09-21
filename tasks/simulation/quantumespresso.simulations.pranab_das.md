# Pranab Das Quantum ESPRESSO hands-on simulation campaign

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.pranab_das`
- **Status:** `inactive`
- **Status detail:** Human-requested Pranab Das hands-on tutorial campaign remains inactive. Six tutorial Tasks have retained completed calculated observations, two are deliberately deferred, and the remaining tutorial Tasks require their own preflight, activation, and protected-execution authorization. No tutorial execution is activated by this campaign record.
- **Parent Task:** `quantumespresso.simulations`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Coordinate bounded, isolated reproductions or explicit deferrals of every workflow in the selected Quantum ESPRESSO hands-on tutorial category and synthesize what they reveal about execution, artifacts, extraction, and scope.

## Relationships

### Task prerequisites

- `P2`

### External prerequisites

- None.

### Superseded by

- None.

## Authorized scope

- Prepare source, input, executable, pseudopotential, resource, and retention preflights for each child simulation.
- Activate at most one child simulation at a time after its exact protected-execution authorization.
- Map each child to the QE backend of one concept-first paired project tutorial under examples/tutorials/<tutorial-id>/qe/.
- Require isolated ignored backend-local run trees and separate standard-output and standard-error files.
- Promote only portable input, useful scripts, instructions, and small test-consumed fixtures under the tutorial-example commit boundary.
- Record an executed, failed, or deliberately deferred learning disposition for every child.
- Ground every tutorial-derived architecture or workflow claim about calculator, stage, continuation, native-output, diagnostic, or failure behavior in identified outputs from an actual explicitly authorized scientific-executable invocation with exact input, executable, pseudopotential, attempt, streams, native outputs, and postprocessing provenance.

## Completion criteria

- Every child simulation has a durable disposition supported by its preflight and, when run, its execution record.
- Every materialized project tutorial contains explicit QE and ABINIT backend status directories without implying numerical equivalence.
- The campaign review distinguishes reusable silicon/QE/Wannier behavior from learning-only or deferred examples.
- No tutorial observation is presented as production, convergence, scientific-validation, uncertainty-quantification, or human-acceptance evidence.
- Synthetic fixtures and fake executors may support isolated software or numerical verification but do not satisfy a tutorial-derived claim about observed calculator behavior.

## Exclusions

- This coordinating Task does not itself authorize any executable invocation.
- Automatic successor activation, concurrent simulation execution, remote execution, and production execution are prohibited.
- Routine stdout/stderr, generated XML, large native outputs, restart data, wavefunctions, charge densities, and dense matrices are not committed to Git.
- Tutorial settings do not override accepted project scientific specifications.
- Do not infer or fabricate tutorial-calculator behavior when identified calculated outputs are unavailable; record it as proposed or unobserved instead.

## Authority references

- `docs/architecture/v2/tutorial-examples.md`
- `docs/computational/quantumespresso.simulations.pranab_das.md`
