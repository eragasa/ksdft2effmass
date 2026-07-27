back_to: [[ksdft2Effmass.computational.06]]
# Task 06.03.01: Align bulk and P:Si operators

## Status

`Blocked`

## Objective

Align bulk and P:Si operators. The task produces the artifact Aligned operator pairs required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.06.02.02|06.02.02]], `G05`.

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- the phosphorus physical specification;
- the validated bulk Wannier and alignment protocols;
- the phosphorus supercell sequence and run manifests;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Generate the required P:Si structure, first-principles, or Wannier inputs.
2. Execute the supercell or representation calculation with complete provenance.
3. Validate the doped target subspace before applying the bulk--dopant alignment.
4. Extract or analyze the phosphorus impurity operator on the common space.
5. Evaluate finite-size, gauge, localization, and alignment sensitivity as applicable.

## Outputs

Primary output:

Aligned operator pairs

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the doped calculation and target subspace pass the same documented validation framework as the bulk reference;
- the extracted phosphorus operator is represented on an explicit common space;
- finite-size, gauge, energy-alignment, and periodic-image effects are quantified;
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

- [[ksdft2Effmass.computational.06.03.02|06.03.02]]

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
