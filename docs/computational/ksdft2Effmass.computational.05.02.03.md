back_to: [[ksdft2Effmass.computational.05]]
# Task 05.02.03: Quantify sensitivity to windows, projections, and localization

## Status

`Blocked`

## Objective

Quantify sensitivity to windows, projections, and localization. The task produces the artifact Alignment-sensitivity record required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.05.02.02|05.02.02]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- operator and subspace records on documented bases;
- overlap, singular-value, and polar-decomposition routines;
- synthetic or first-principles reference transformations;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Construct the overlap matrix between the two documented comparison spaces.
2. Evaluate ranks, singular values, and principal angles before forming an identification map.
3. Construct the polar or Procrustes alignment and transport one operator into the other space.
4. Repeat the comparison under controlled gauge and construction changes.
5. Store the alignment map, diagnostics, sensitivities, and validity domain.

## Outputs

Primary output:

Alignment-sensitivity record

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- rank compatibility and principal-angle diagnostics are reported before subtraction;
- the identification map is reproducible from stored inputs;
- gauge and construction sensitivity remain within the declared tolerance or are reported as a limitation;
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

- [[ksdft2Effmass.computational.05.02.04|05.02.04]]

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
