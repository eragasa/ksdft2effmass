back_to: [[ksdft2Effmass.computational.02]]
# Task 02.02.02: Extract band edges, valley positions, and effective masses

## Status

`Blocked`

## Objective

Extract band edges, valley positions, and effective masses. The task produces the artifact Bulk validation record required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.02.02.01|02.02.01]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- `PhysicalSpecification-v1`, `NumericalSpecification-v1`, and
  [`SiliconEffectiveMassValidationSpecification-v1`](../../specification/ksdft2Effmass.silicon-effective-mass-validation.v1.md);
- the inactive exact
  [QE 7.5 simulation requirements](bulk-silicon-effective-mass-simulation-requirements.md);
- Quantum ESPRESSO input templates and pseudopotentials;
- the common convergence and validation metrics;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Construct the required Quantum ESPRESSO inputs from the frozen specifications.
2. Declare the explicit $\Delta$-valley targets, Cartesian axes, state-identity rule,
   local fit/stencil family, and training and withheld point sets before fitting.
3. Execute the calculation or convergence series with one controlled variable changed
   at a time.
4. Locate each target minimum, verify the full Cartesian stationary-point and
   nondegeneracy conditions, and extract the Hessian and longitudinal and transverse
   masses with explicit $\hbar^2$ and unit conventions.
5. Evaluate parent numerical, local-derivative, guard, and withheld-point evidence
   against the frozen tolerances while retaining interpolation and reduction errors as
   separate routes.
6. Store inputs, outputs, manifests, rejected points, error components, and the
   scientific acceptance decision.

## Outputs

Primary output:

Bulk validation record

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- all calculations are reproducible from stored manifests;
- the target is an identity-tracked, nondegenerate Cartesian stationary minimum with
  positive principal curvatures at the declared numerical resolution;
- longitudinal and transverse masses satisfy their frozen convergence tolerances and
  the local extraction is stable under the required guard comparison;
- the relevant bulk observables satisfy their convergence tolerances;
- the accepted parameters do not depend on an undocumented software default;
- the declared output exists and can be reconstructed from the stored inputs;
- all task-specific numerical tolerances are recorded with a pass/fail result;
- parent, local-derivative, Wannier-interpolation, reduction, and external-comparison
  discrepancies are retained separately;
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

- [[ksdft2Effmass.computational.02.02.03|02.02.03]]

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
