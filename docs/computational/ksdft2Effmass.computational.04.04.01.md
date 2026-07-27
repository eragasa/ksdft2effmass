back_to: [[ksdft2Effmass.computational.04]]
# Task 04.04.01: Apply common bulk validation metrics

## Status

`Blocked`

## Objective

Apply common bulk validation metrics. The task produces the artifact Comparative validation record required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.04.02.02|04.02.02]], [[ksdft2Effmass.computational.04.03.02|04.03.02]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- the accepted bulk first-principles or Wannier reference;
- the prescribed $sp^3s^*$ tight-binding model class;
- the frozen training and validation definitions;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Construct the prescribed tight-binding operator and parameter constraints.
2. Fit or project using only the frozen training data.
3. Evaluate the Hamiltonian on the withheld validation data.
4. Measure operator, spectral, band-edge, and complexity quantities where defined.
5. Store parameters, objectives, residuals, and the pass/fail decision.

## Outputs

Primary output:

Comparative validation record

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- training and withheld validation data remain disjoint;
- the fitted operator satisfies Hermiticity and the prescribed symmetries;
- operator, spectral, observable, and model-complexity results are reported together;
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

- [[ksdft2Effmass.computational.04.04.02|04.04.02]]

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
