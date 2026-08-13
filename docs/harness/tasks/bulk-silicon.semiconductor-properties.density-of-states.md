<!-- Generated from SQLite control state; do not edit. -->
# Production density of states and effective DOS

[Task index](index.md) · [Previous](./bulk-silicon.semiconductor-properties.deformation-potentials.md) · [Next](./bulk-silicon.semiconductor-properties.dielectric-screening.md)

## Status

`blocked`: Conditional-to-essential calculation/analysis Task: required for numerical DOS and intrinsic statistics, but not for the shortest electron-mass reference path.

## Objective

Produce converged total and band-edge DOS records and determine whether the Wannier NSCF grid can be reused or a distinct denser QE NSCF mesh is required.

## Parent and prerequisites

- Parent: `bulk-silicon.semiconductor-properties`
- Depends on: `bulk-silicon.production-reference.scf`
- External prerequisite: `production_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the SCF parent, candidate uniform meshes, retained bands, tetrahedron/smearing/interpolation method, energy grid, broadening, and state-count convention.
- Retain NSCF/DOS manifests, compact energy-DOS arrays, integrated state counts, mesh/broadening sensitivity, band-edge DOS, effective N_c(T)/N_v(T) inputs, and total-DOS figures; projected DOS requires separate projection authority.
- The human owns mesh reuse versus distinct mesh, integration method, broadening/energy grid, band coverage, and acceptance rules.

## Completion criteria

- DOS and integrated state count converge under accepted mesh/method sensitivity checks.
- Band-edge DOS and parabolic approximations use explicit degeneracy/mass conventions.
- Any reuse of the Wannier mesh is justified by DOS-specific evidence.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- No PDOS is reported without projection authority, and broadening is not hidden as physical linewidth.

## Historical source

No archived source.
