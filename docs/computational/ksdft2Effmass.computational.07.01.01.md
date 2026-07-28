back_to: [[ksdft2Effmass.computational.07]]
# Task 07.01.01: Construct the B:Si specialization gate

## Status

`Blocked`

## Objective

Construct the B:Si specialization gate from `PhysicalSpecification-v1`. The task records the B-specific charge state, pseudopotential, geometry, relaxation, spin, spin--orbit, and branch conventions required before downstream boron production tasks proceed.

## Prerequisites

`G01`.

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- `PhysicalSpecification-v1`;
- the boron physical specification decisions frozen there;
- the validated bulk Wannier and alignment protocols;
- the boron supercell sequence and multiband validation definitions;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Record the PseudoDojo PBE standard-table B pseudopotential metadata selected by `01.01.02`.
2. Record the primary neutral B$_\mathrm{Si}^0$ fully relativistic, noncollinear spinor SOC branch for final acceptor and continuum claims.
3. Record the scalar-relativistic non-SOC B:Si calculation as an early method-development branch only.
4. Record the deferral of charged B$_\mathrm{Si}^{-}$ to a controlled branch.
5. Record the fixed-lattice internal-relaxation convention and required links to the Stage `05` energy-alignment estimator.
6. Produce the B:Si specialization gate artifact consumed by downstream boron tasks.

## Outputs

Primary output:

B:Si specialization gate

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the primary B:Si physical branch is explicit and consistent with `PhysicalSpecification-v1`;
- exact B pseudopotential metadata and valence configuration are recorded or linked from `01.01.02`;
- final SOC and non-primary method-development branches are explicitly separated;
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

- [[ksdft2Effmass.computational.07.01.02|07.01.02]]

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
