back_to: [[ksdft2Effmass.computational.03]]
# Task 03.01.03: Approve retained bands, projections, windows, and the uniform grid

## Status

`Blocked`

## Objective

Freeze the Wannier-interface scientific specification before the uniform-grid NSCF child is run. The task produces the retained-band, projection, outer/inner-window, and uniform-grid contract required by the downstream static prerequisite projection and CPN transition contracts.

## Prerequisites

[[ksdft2Effmass.computational.03.01.01|03.01.01]], [[ksdft2Effmass.computational.03.01.02|03.01.02]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- `BulkSiReference-v1`;
- Wannier90 and interface inputs;
- the target-subspace and validation specifications;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Define the retained band count and its relationship to the accepted G02 bulk spectrum.
2. Record the trial projections and their scientific meaning.
3. Define candidate and acceptance policies for outer and inner windows without treating a plotting energy shift as an aligned physical zero.
4. Define the uniform reciprocal-space grid, ordering, spin convention, and required bridge artifacts.
5. Freeze the accepted interface specification before Task `03.01.04` executes its NSCF child.

## Outputs

Primary output:

Wannier-interface specification

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the retained bands, projections, windows, and uniform grid are explicit and versioned;
- k-point ordering, spin, units, energy reference, and required interface files are explicit;
- no unknown G02 Wannier grid is inferred or retroactively frozen;
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

- [[ksdft2Effmass.computational.03.01.04|03.01.04]]

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
