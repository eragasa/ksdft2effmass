back_to: [[ksdft2Effmass.computational.01]]
# Task 01.01.02: Freeze numerical conventions and software stack

## Status

`Passed`

## Objective

Freeze numerical conventions and software stack. The task produces the artifact NumericalSpecification-v1 required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.01.01.01|01.01.01]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- the current research-plan definitions;
- documented physical or numerical decisions;
- the shared repository and test environment;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Translate the relevant physical or mathematical definition into an explicit computational specification.
2. Implement the specification, schema, or metric without relying on undocumented defaults.
3. Construct a minimal controlled example with a known expected result.
4. Run validation and regression checks.
5. Store the accepted artifact and its provenance record.

## Outputs

Primary output:

[`NumericalSpecification-v1`](../../specification/ksdft2Effmass.numerical-specification.v1.md)

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the artifact is explicit, versioned, and machine-readable where applicable;
- a controlled regression example reproduces the expected result;
- physical assumptions and numerical approximations are distinguished;
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

- [[ksdft2Effmass.computational.01.02.02|01.02.02]]

## Failure Conditions

The task fails if its primary artifact cannot be reproduced, if its required comparison space is undefined, if validation depends only on visual agreement, or if the reported result changes beyond tolerance under an unrecorded numerical choice.

## Computational Record

- run identifier: local specification-edit session, 2026-07-28
- code version: `416ef8a` at task start
- software environment: Python `3.14.6`; `pw.x` and `wannier90.x` not found in `PATH`
- input manifest: `PhysicalSpecification-v1`; PseudoDojo `nc-sr-04_pbe_standard` metadata and UPF download for Si
- output manifest: `specification/ksdft2Effmass.numerical-specification.v1.md`
- validation record: SHA-256 reconstruction of downloaded and decompressed Si PseudoDojo UPF file passed; protocol-only acceptance confirmed by PI instruction; no DFT or Wannier validation performed
- completion date: 2026-07-28
