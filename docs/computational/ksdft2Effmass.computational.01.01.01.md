back_to: [[ksdft2Effmass.computational.01]]
# Task 01.01.01: Freeze the Physical Reference Specification

## Status

`Passed`

## Objective

Define the physical content of the bulk-silicon, phosphorus-doped, and boron-doped first-principles systems before numerical convergence parameters are selected.

## Prerequisites

None.

## Inputs

- the current mathematical and computational research-plan definitions;
- the intended bulk-silicon, P:Si, and B:Si physical systems;
- candidate exchange-correlation, pseudopotential, spin, charge-state, and geometry conventions.

## Required Decisions

- exchange-correlation approximation;
- pseudopotential family and valence configurations;
- scalar-relativistic or fully relativistic treatment;
- inclusion or exclusion of spin--orbit coupling;
- spin-polarized or non-spin-polarized treatment;
- primitive and supercell crystal conventions;
- experimental or relaxed bulk lattice constant;
- substitutional dopant sites;
- neutral or charged defect calculations;
- atomic relaxation protocol;
- boundary conditions and periodic-image interpretation;
- physical observables retained for convergence.

## Procedure

1. Write one explicit physical specification for bulk silicon.
2. Write separate extensions for P:Si and B:Si.
3. Identify which choices must be identical across bulk and doped calculations.
4. Identify controlled branches, such as scalar-relativistic versus spin--orbit calculations.
5. Mark all unresolved choices as blocking decisions rather than allowing software defaults.

## Outputs

```text
PhysicalSpecification-v1
```

The artifact must distinguish physical assumptions from numerical approximations.

## Acceptance Criteria

- every required decision has an explicit value or a documented controlled branch;
- bulk and doped specifications identify all shared settings;
- no downstream calculation depends on an undocumented default;
- the specification identifies the band-edge, subspace, and impurity observables used for convergence.

## Validation Record

Record:

$$
\text{decision},
\qquad
\text{physical justification},
\qquad
\text{computational consequence},
\qquad
\text{affected downstream tasks}.
$$

## Unlocks

- [[ksdft2Effmass.computational.01.01.02|01.01.02]]: freeze numerical conventions;
- [[ksdft2Effmass.computational.01.02.01|01.02.01]]: implement the operator-record schema;
- [[ksdft2Effmass.computational.06.01.01|06.01.01]]: construct the P:Si specialization gate;
- [[ksdft2Effmass.computational.07.01.01|07.01.01]]: construct the B:Si specialization gate.

## Failure Conditions

The task remains incomplete if the charge state, spin--orbit treatment, relaxation protocol, pseudopotential compatibility, or energy-reference convention remains implicit.

## Computational Record

- specification version: `PhysicalSpecification-v1`
- author or reviewer: PI decisions applied to AI-assisted draft
- software constraints: no execution software selected in this task; numerical software stack deferred to `01.01.02`
- pseudopotential source and hashes: PseudoDojo PBE standard-table ONCV UPF family frozen; exact release, filenames, versions, SHA-256 hashes, suggested cutoffs, converged cutoffs, and Quantum ESPRESSO compatibility deferred to `01.01.02`
- unresolved controlled branches: no unresolved decision blocks `01.01.02` or `01.02.01`; charged P$_\mathrm{Si}^{+}$ and B$_\mathrm{Si}^{-}$ branches are deferred; scalar-relativistic non-SOC B:Si is method-development only; Stage `05` selects the operational energy-alignment estimator
- validation record: `specification/ksdft2Effmass.physical-specification.v1.md`
- completion date: 2026-07-27
