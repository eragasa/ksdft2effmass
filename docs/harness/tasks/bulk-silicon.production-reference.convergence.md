<!-- Generated from SQLite control state; do not edit. -->
# Plane-wave and Brillouin-zone convergence

[Task index](index.md) · [Previous](./bulk-silicon.production-reference.md) · [Next](./bulk-silicon.production-reference.lattice-reference.md)

## Status

`blocked`: Essential calculation series; blocked by the production pseudopotential decision and protected-execution authorization.

## Objective

Converge wavefunction and applicable charge-density cutoffs and the SCF Monkhorst–Pack mesh against every retained parent and band-edge observable.

## Parent and prerequisites

- Parent: `bulk-silicon.production-reference`
- Depends on: `bulk-silicon.production-reference.pseudopotential-selection`
- External prerequisite: `production_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the accepted physical branch, exact pseudopotential identity, trial geometry, frozen numerical protocol, execution environment, and declared acceptance metrics.
- Principal axes are E_cut^psi, applicable E_cut^rho/E_cut^psi, mesh size and offset; monitor total energy/atom, stress, lattice response, indirect gap, valley position, selected edge eigenvalues, and electron masses where the protocol requires them.
- Retain sanitized inputs, run manifests, compact QEXSD/output records, convergence tables, rejected settings, guard calculations, residuals, and figures; large restart data remain external.
- The human owns any revision of the frozen protocol/tolerances and the final setting disposition.

## Completion criteria

- Each study changes one controlled variable at a time or documents an explicit coupled iteration.
- Observable-specific convergence is evaluated using the accepted numerical rules, including at least one finer guard where required.
- Cutoff, SCF-mesh, and downstream sampling adequacy remain separately represented.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- A symmetry path, Wannier mesh, DOS mesh, or local valley stencil is not accepted as an SCF integration mesh.

## Historical source

No archived source.
