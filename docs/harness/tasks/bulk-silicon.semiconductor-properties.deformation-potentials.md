<!-- Generated from SQLite control state; do not edit. -->
# Conditional silicon deformation potentials

[Task index](index.md) · [Previous](./bulk-silicon.semiconductor-properties.md) · [Next](./bulk-silicon.semiconductor-properties.density-of-states.md)

## Status

`blocked`: Conditional strained-calculation and analysis Task; justified only by approved strain, phonon-coupling, or impurity-EMT claims.

## Objective

Determine hydrostatic and shear band-edge deformation potentials from controlled strained-cell branches with compatible numerical settings.

## Parent and prerequisites

- Parent: `bulk-silicon.semiconductor-properties`
- Depends on: `bulk-silicon.production-reference.convergence`
- Depends on: `bulk-silicon.production-reference.lattice-reference`
- Depends on: `bulk-silicon.production-reference.scf`
- External prerequisite: `strained_production_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the accepted unstrained parent, strain tensor families/amplitudes, internal-relaxation convention, compatible SCF and band-edge sampling, fit forms, and withheld strains.
- Retain strained structures, run manifests, aligned band edges, stress/energy records, linear/nonlinear fits, residuals, strain-range sensitivity, and deformation-potential figures.
- The human owns strain modes/range, relaxation convention, band-edge alignment, fit order, symmetry constraints, and validation comparator.

## Completion criteria

- Positive/negative strains, linear regime, symmetry relations, and withheld checks are explicit.
- Numerical convergence is demonstrated under strain and separated from fit/model and physical-validation errors.
- Hydrostatic and shear constants are reported with exact conventions.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- No phonon, electron–phonon, mobility, or piezoresistive claim follows automatically.

## Historical source

No archived source.
