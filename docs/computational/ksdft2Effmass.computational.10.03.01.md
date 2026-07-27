back_to: [[ksdft2Effmass.computational.10]]
# Task 10.03.01: Measure error amplification under successive reductions

## Status

`Blocked`

## Objective

Measure error amplification under successive reductions. The task produces the artifact Composition dataset required by the downstream dependency graph.

## Prerequisites

`G08-P` and `G09-P`, or `G08-B` and `G09-B`.

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- the completed outputs of every reduction path being compared;
- explicit common-space alignment maps;
- the norm, tolerance, and validity domain for the comparison;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Execute both computational paths from their frozen input artifacts.
2. Transport the resulting operators or transformations to a common comparison space.
3. Compute the prescribed defect using the stated norm and validation domain.
4. Repeat under controlled numerical or gauge perturbations.
5. Attribute the measured discrepancy to representation, fitting, truncation, or physical-model effects.

## Outputs

Primary output:

Composition dataset

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- both compared paths begin from versioned and compatible input artifacts;
- the outputs are aligned before their defect is computed;
- the norm, tolerance, sensitivity, and validity domain accompany the reported defect;
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

- [[ksdft2Effmass.computational.10.03.02|10.03.02]]

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
