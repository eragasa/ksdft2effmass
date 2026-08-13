<!-- Generated from SQLite control state; do not edit. -->
# Conditional dielectric-screening reference

[Task index](index.md) · [Previous](./bulk-silicon.semiconductor-properties.density-of-states.md) · [Next](./bulk-silicon.semiconductor-properties.intrinsic-statistics.md)

## Status

`blocked`: Conditional DFPT/physical-validation Task; justified only by impurity EMT screening or another approved response-property claim.

## Objective

Obtain or adopt separately authoritative electronic and static dielectric tensors and map them to explicitly declared EMT screening constants.

## Parent and prerequisites

- Parent: `bulk-silicon.semiconductor-properties`
- Depends on: `bulk-silicon.production-reference.scf`
- External prerequisite: `dfpt_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: physical validation.
- Inputs may be an authorized compatible DFPT calculation, identified experiment, or another accepted source; distinguish ε_infinity, ε_0, tensor/scalar conventions, temperature, and frequency.
- Retain DFPT requests/artifacts when executed, compact tensors, convergence records, literature/experimental identities, comparisons, and model-screening disposition.
- The human owns calculation versus literature authority, ionic contribution, scalar reduction, validation reference, and EMT screening convention.

## Completion criteria

- Electronic, ionic/static, and model dielectric quantities are never conflated.
- Any calculated tensor has separate basis, k/q mesh, cutoff, response convergence, units, and physical-validation evidence.
- The selected EMT constant has an explicit provenance and domain.

## Exclusions

- No DFPT or response executable is authorized by this plan.
- Ordinary SCF/band data do not supply ε_infinity or ε_0.

## Historical source

No archived source.
