back_to: [[ksdft2Effmass.computational.07]]
# Task 07.02.02: Validate degeneracies, orbital content, and spin--orbit structure

## Status

`Blocked`

## Objective

Validate degeneracies, orbital content, and spin--orbit structure. The task produces the artifact Doped subspace validation required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.07.02.01|07.02.01]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- the boron physical specification;
- the validated bulk Wannier and alignment protocols;
- the boron supercell sequence and multiband validation definitions;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Generate the required B:Si structure, first-principles, or Wannier inputs.
2. Execute the calculation while retaining the required multiband and spin--orbit information.
3. Validate degeneracies, orbital character, and the doped target subspace.
4. Align and extract the boron impurity operator on the common space.
5. Evaluate finite-size, gauge, localization, and alignment sensitivity as applicable.

## Outputs

Primary output:

Doped subspace validation

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the retained subspace resolves the required valence, orbital, and spin--orbit structure;
- the extracted boron operator is represented on an explicit common space;
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

- [[ksdft2Effmass.computational.07.03.01|07.03.01]]

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
