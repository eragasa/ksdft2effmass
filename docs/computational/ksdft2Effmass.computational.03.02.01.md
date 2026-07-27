back_to: [[ksdft2Effmass.computational.03]]
# Task 03.02.01: Construct candidate Wannier Hamiltonians

## Status

`Blocked`

## Objective

Construct candidate Wannier Hamiltonians. The task produces the artifact Candidate operator records required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.03.01.03|03.01.03]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- `BulkSiReference-v1`;
- Wannier90 and interface inputs;
- the target-subspace and validation specifications;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Construct the required projection, window, and Wannier90 inputs.
2. Run the candidate Wannier construction while recording all gauge and disentanglement choices.
3. Export reciprocal-space and real-space Hamiltonian representations.
4. Evaluate interpolation, center, spread, symmetry, and hopping-decay diagnostics.
5. Store the candidate or accepted operator with its validation record.

## Outputs

Primary output:

Candidate operator records

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the target subspace and all projection or window choices are recorded;
- interpolation and band-edge errors satisfy the accepted tolerances;
- centers, spreads, symmetries, and real-space decay show no unresolved pathology;
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

- [[ksdft2Effmass.computational.03.02.02|03.02.02]]

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
