<!-- Generated from SQLite control state; do not edit. -->
# Bulk-silicon semiconductor-property program

[Task index](index.md) · [Previous](./bulk-silicon.records.periodic.extraction.md) · [Next](./bulk-silicon.semiconductor-properties.deformation-potentials.md)

## Status

`inactive`: Planning-only property and acceptance boundary. Immediate deterministic properties branch from accepted band-edge/DOS data; dielectric and strain properties are conditional.

## Objective

Coordinate band-edge-level semiconductor properties, carrier statistics, conditional screening and deformation-potential branches, visualizations, numerical verification, and bounded physical validation for later EMT use.

## Parent and prerequisites

None.

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: physical validation.
- Separate properties obtainable from pristine band energies from those requiring DOS integration, SOC/multiband fits, DFPT, strain calculations, experiment, doped systems, or scattering models.
- Retain definitions, units, temperature/domain assumptions, numerical residuals, external reference identities, and EMT relevance.
- Require human acceptance for each claim family; the parent performs no scientific executable.

## Completion criteria

- Every reported property names its minimum data, mathematical extraction, numerical-verification evidence, physical-validation evidence when claimed, and domain of validity.
- Immediate, conditional, and deferred properties remain distinct.
- EMT inputs identify pristine-bulk versus doped/experimental provenance.

## Exclusions

- No mobility, conductivity, scattering, impurity binding, dielectric, SOC, or many-body claim is inferred from ordinary SCF/path data alone.
- Parent-model, numerical, reduction, statistical-approximation, and experimental discrepancies are not combined.

## Historical source

No archived source.
