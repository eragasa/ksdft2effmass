back_to: [[ksdft2Effmass.computational.04]]
# Task 04.04.01: Apply common bulk validation metrics

## Status

`Blocked`

## Objective

Apply common bulk validation metrics after a provenance-compatible CPN join. The task produces the comparative validation record required by the downstream static prerequisite projection and CPN transition contracts.

## Prerequisites

[[ksdft2Effmass.computational.04.02.02|04.02.02]], [[ksdft2Effmass.computational.04.03.02|04.03.02]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- the accepted bulk `PeriodicElectronicStructureDataset` and source manifest shared by both branches;
- the validated Wannier child and its parent-manifest lineage for the operator-mediated branch;
- direct and Wannier-derived TB result tokens with physical, numerical, pseudopotential, workflow, representation, energy, artifact, and validation metadata;
- the prescribed $sp^3s^*$ tight-binding model class;
- the frozen training and validation definitions;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Bind both branch results to the same accepted periodic electronic-structure parent dataset and source manifest.
2. Verify compatible physical, numerical, pseudopotential-set, workflow-schema, energy, representation, artifact, and branch-validation metadata.
3. Reject the join if parentage or required metadata is missing or incompatible; two completion states alone are insufficient.
4. Evaluate only metrics whose state-space and representation requirements are explicit.
5. Store the joined parentage, compatibility evidence, parameters, objectives, residuals, and acceptance decision.

## Outputs

Primary output:

Comparative validation record

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- training and withheld validation data remain disjoint;
- both result tokens identify the same accepted periodic electronic-structure parent and source manifest;
- physical, numerical, pseudopotential, workflow, energy, representation, artifact, and validation metadata required by each metric are compatible and verified;
- the fitted operator satisfies Hermiticity and the prescribed symmetries;
- operator, spectral, observable, and model-complexity results are reported together;
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

- [[ksdft2Effmass.computational.04.04.02|04.04.02]]

## Failure Conditions

The task fails if parentage is different or unverified, required specification or representation metadata is incompatible, its primary artifact cannot be reproduced, its required comparison space is undefined, validation depends only on visual agreement, or the reported result changes beyond tolerance under an unrecorded numerical choice.

## Computational Record

- run identifier:
- code version:
- software environment:
- input manifest:
- output manifest:
- validation record:
- completion date:
