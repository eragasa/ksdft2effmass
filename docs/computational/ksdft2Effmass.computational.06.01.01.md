back_to: [[ksdft2Effmass.computational.06]]
# Task 06.01.01: Construct the P:Si specialization gate

## Status

`Blocked`

## Objective

Construct the P:Si specialization gate from `PhysicalSpecification-v1`. The task records the P-specific charge state, pseudopotential, geometry, relaxation, spin, and branch conventions required before downstream phosphorus production tasks proceed.

## Prerequisites

`G01`.

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- `PhysicalSpecification-v1`;
- the phosphorus physical specification decisions frozen there;
- the validated bulk Wannier and alignment protocols;
- the phosphorus supercell sequence and run manifests;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Record the PseudoDojo PBE standard-table P pseudopotential metadata selected by `01.01.02`.
2. Record the primary neutral P$_\mathrm{Si}^0$ scalar-relativistic, collinear spin-polarized, non-SOC branch.
3. Record the deferral of charged P$_\mathrm{Si}^{+}$ and non-spin-polarized fractional-occupation calculations to controlled branches.
4. Record the fixed-lattice internal-relaxation convention and required links to the Stage `05` energy-alignment estimator.
5. Produce the P:Si specialization gate artifact consumed by downstream phosphorus tasks.

## Outputs

Primary output:

P:Si specialization gate

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the primary P:Si physical branch is explicit and consistent with `PhysicalSpecification-v1`;
- exact P pseudopotential metadata and valence configuration are recorded or linked from `01.01.02`;
- charged and non-primary method-development branches are explicitly separated from the primary branch;
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

- [[ksdft2Effmass.computational.06.01.02|06.01.02]]

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
