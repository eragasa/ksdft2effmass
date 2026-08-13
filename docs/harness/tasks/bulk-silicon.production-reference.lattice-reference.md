<!-- Generated from SQLite control state; do not edit. -->
# Production lattice reference and equation of state

[Task index](index.md) · [Previous](./bulk-silicon.production-reference.convergence.md) · [Next](./bulk-silicon.production-reference.scf.md)

## Status

`blocked`: Essential calculation and analysis Task; blocked by converged basis and SCF-mesh settings. Iteration back to convergence is permitted when geometry changes invalidate prior evidence.

## Objective

Determine the zero-pressure PBE equilibrium lattice reference and retain an experimental-lattice comparison as a distinct physical-validation branch when authorized.

## Parent and prerequisites

- Parent: `bulk-silicon.production-reference`
- Depends on: `bulk-silicon.production-reference.convergence`
- External prerequisite: `production_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the accepted production branch, convergence records, diamond primitive-cell convention, EOS protocol, and identified experimental reference if used.
- Principal controls are lattice/volume grid, fit family and window, included/withheld points, fixed symmetry, stress convention, and optional constrained variable-cell verification.
- Retain energy/stress records, EOS fit, covariance or fit uncertainty, residuals, refinement history, selected geometry manifest, and EOS visualization.
- The human owns any choice beyond the frozen zero-pressure PBE-relaxed primary branch and the disposition of experimental comparison evidence.

## Completion criteria

- The fitted minimum is stable under the accepted grid refinement and independently checked as required by NumericalSpecification-v1.
- Numerical fit uncertainty and disagreement with experiment are separate.
- The resulting geometry is frozen only after confirming that cutoff and mesh evidence remains applicable or repeating affected convergence.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- An experimental lattice constant is not silently substituted for the frozen primary relaxed-lattice convention.

## Historical source

No archived source.
