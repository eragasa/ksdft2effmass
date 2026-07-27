back_to: [[ksdft2Effmass.computational.09]]
# Task 09.01.04: Implement screened Coulomb and central-cell model families

## Status

`Blocked`

## Objective

Implement screened Coulomb and central-cell model families. The task produces the artifact Continuum impurity library required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.09.01.02|09.01.02]], [[ksdft2Effmass.computational.09.01.03|09.01.03]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- validated host-band, impurity, or synthetic continuum data;
- the continuum discretization and boundary-condition specification;
- the atomistic and continuum validation metrics;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Construct the requested continuum operator, solver component, or embedding.
2. Specify the continuum domain, basis or mesh, and boundary conditions.
3. Verify discretization convergence using analytic or synthetic benchmarks.
4. Compare the continuum and atomistic operators or states on the declared common domain.
5. Store spatial error curves, observables, tolerances, and the crossover decision where applicable.

## Outputs

Primary output:

Continuum impurity library

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the solver is converged with respect to its continuum discretization and domain;
- the atomistic--continuum comparison uses a documented embedding and common region;
- the reported crossover or failure to find one follows the stated exterior and cross-coupling tolerances;
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

- [[ksdft2Effmass.computational.09.03.01|09.03.01]]
- [[ksdft2Effmass.computational.09.04.01|09.04.01]]

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
