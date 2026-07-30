back_to: [[ksdft2Effmass.computational.01]]
# Task 01.02.02: Implement run manifests and provenance capture

## Status

`Ready`

## Objective

Implement run manifests and provenance capture. The task produces the artifact Tested `RunManifest required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.01.01.02|01.01.02]].

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

Tested `RunManifest`

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

- contributes to the completion gate for Computational Stage `01`

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
