back_to: [[ksdft2Effmass.computational.02]]
# Task 02.02.01: Run the production SCF parent and bulk-validation NSCF calculations

## Status

`Blocked`

## Objective

Run the production SCF parent and only the path, valley, effective-mass, or other diagnostic NSCF calculations required for G02 bulk validation. The task produces the accepted SCF parent and validation spectra required by the downstream static prerequisite projection and CPN transition contracts.

## Prerequisites

[[ksdft2Effmass.computational.02.01.04|02.01.04]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- `PhysicalSpecification-v1` and `NumericalSpecification-v1`;
- Quantum ESPRESSO input templates and pseudopotentials;
- the common convergence and validation metrics;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Construct the required Quantum ESPRESSO inputs from the frozen specifications.
2. Run the SCF parent until the code-specific self-consistency criterion is satisfied, then test the accepted parent density, total energy, and required parent quantities against the separately declared cutoff, mesh, geometry, and reproducibility tolerances.
3. Freeze the SCF parent manifest, including density/potential lineage, pseudopotential, exchange-correlation approximation, geometry, cutoffs, wavevector mesh, occupations, software identity, and convergence settings.
4. Construct separate NSCF or band children that reference the frozen parent: a symmetry path for dispersion, targeted valley sampling for extrema and curvature, and only the additional meshes required by the G02 observables.
5. Select and converge each child's wavevectors and retained bands for its stated observable; do not infer adequacy from SCF convergence or reuse a path calculation as a Brillouin-zone integration dataset.
6. Extract total-energy, band-edge, valley, and effective-mass quantities where applicable.
7. Evaluate every result against the stated software, numerical, and scientific acceptance rule without combining those evidence classes.
8. Store inputs, outputs, parent--child manifests, and the validation decision.

## Outputs

Primary output:

Accepted SCF parent and bulk-validation spectra

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- all calculations are reproducible from stored manifests;
- the SCF parent satisfies both the recorded code-specific iterative criterion and the declared discretization/convergence protocol;
- each NSCF or band child records its purpose, parent identity, wavevector sampling, band count, and observable-specific convergence evidence;
- the relevant bulk observables satisfy their convergence tolerances;
- the accepted parameters do not depend on an undocumented software default;
- the declared output exists and can be reconstructed from the stored inputs;
- all task-specific numerical tolerances are recorded with a pass/fail result;
- unresolved failures are not propagated as accepted downstream inputs.

## Validation Record

Record:

$$
\text{reference},
\qquad
\text{candidate},
\qquad
\text{metric},
\qquad
\text{tolerance},
\qquad
\text{result}.
$$

## Unlocks

- [[ksdft2Effmass.computational.02.02.02|02.02.02]]
- the Stage 03 target-subspace design after G02 passes; the Wannier-compatible uniform-grid NSCF child is not an output of this task

## Failure Conditions

The task fails if its primary artifact cannot be reproduced, if its required comparison space is undefined, if validation depends only on visual agreement, or if the reported result changes beyond tolerance under an unrecorded numerical choice.

## Computational Record

- run identifier:
- code version:
- software environment:
- input manifest:
- output manifest:
- validation record:
- completion date:
