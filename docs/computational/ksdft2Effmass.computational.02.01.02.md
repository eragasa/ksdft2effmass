back_to: [[ksdft2Effmass.computational.02]]
# Task 02.01.02: Converge kinetic-energy and charge-density cutoffs

## Status

`Blocked`

## Objective

Converge kinetic-energy and charge-density cutoffs. The task produces the artifact Cutoff convergence record required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.02.01.01|02.01.01]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- `PhysicalSpecification-v1` and `NumericalSpecification-v1`;
- Quantum ESPRESSO input templates and pseudopotentials;
- the common convergence and validation metrics;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Construct the required Quantum ESPRESSO inputs from the frozen specifications.
2. Execute the calculation or convergence series with one controlled variable changed at a time.
3. Extract total-energy, band-edge, valley, and effective-mass quantities where applicable.
4. Evaluate convergence against the stated tolerances.
5. Store inputs, outputs, manifests, and the validation decision.

## Outputs

Primary output:

Cutoff convergence record

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- all calculations are reproducible from stored manifests;
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

- [[ksdft2Effmass.computational.02.01.03|02.01.03]]

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
