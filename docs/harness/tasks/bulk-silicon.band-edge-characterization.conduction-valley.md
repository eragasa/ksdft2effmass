<!-- Generated from SQLite control state; do not edit. -->
# Local Δ-valley production sampling

[Task index](index.md) · [Previous](./bulk-silicon.band-edge-characterization.md) · [Next](./bulk-silicon.band-edge-characterization.effective-mass-analysis.md)

## Status

`blocked`: Essential calculation for the non-SOC electron pilot; blocked by the production SCF parent and an initial valley estimate from accepted dispersion evidence.

## Objective

Locate each symmetry-equivalent conduction minimum and retain local three-dimensional samples sufficient for the inverse-mass tensor and nonparabolicity diagnostics.

## Parent and prerequisites

- Parent: `bulk-silicon.band-edge-characterization`
- Depends on: `bulk-silicon.production-reference.scf`
- External prerequisite: `initial_valley_location_evidence`
- External prerequisite: `production_execution_authorization`
- External prerequisite: `valley_sampling_design_approval`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the SCF parent, initial valley coordinates, coordinate basis, sampling geometry/radius/spacing, retained bands, tracking rule, fit order/window, symmetry constraints, and withheld points.
- Retain ordered local energies, valley identities, fit/withheld partitions, symmetry mappings, line and surface cuts, and convergence/sensitivity records.
- The human owns sampling geometry, radius, spacing, polynomial model, fitting window, symmetry constraints, nonparabolic extension, and acceptance rules.

## Completion criteria

- Valley location and local Hessian are stable under accepted radius/spacing/model sensitivity checks.
- Longitudinal/transverse axes and symmetry-equivalent valleys agree within declared numerical rules or discrepancies are resolved.
- Withheld samples remain unused in fitting and residuals are retained.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- A one-dimensional path cut does not by itself establish the full tensor.

## Historical source

No archived source.
