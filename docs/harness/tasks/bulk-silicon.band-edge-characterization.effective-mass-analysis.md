<!-- Generated from SQLite control state; do not edit. -->
# Electron effective-mass and nonparabolicity analysis

[Task index](index.md) · [Previous](./bulk-silicon.band-edge-characterization.conduction-valley.md) · [Next](./bulk-silicon.band-edge-characterization.symmetry-path.md)

## Status

`blocked`: Essential deterministic analysis and numerical-verification Task for the non-SOC electron pilot; performs no scientific executable.

## Objective

Extract the conduction inverse-mass tensor, longitudinal/transverse masses, derived conductivity and DOS masses, group velocities, and bounded nonparabolicity diagnostics from retained local data.

## Parent and prerequisites

- Parent: `bulk-silicon.band-edge-characterization`
- Depends on: `bulk-silicon.band-edge-characterization.conduction-valley`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: analysis.
- Inputs are verified local-valley records, physical reciprocal coordinates, band correspondence, fit/withheld partitions, hbar/unit conventions, and declared uncertainty method.
- Deterministic outputs include Hessians, eigenaxes, m_l*, m_t*, full tensor, documented six-valley conductivity/DOS combinations, finite-difference or fit velocities, residuals, and window/radius/spacing sensitivity figures.
- The human owns the estimator, model order, accepted window, symmetry pooling, uncertainty interpretation, and whether a Kane-type parameter is justified.

## Completion criteria

- Analytic units and tensor conventions are explicit and software checks reproduce controlled synthetic dispersions.
- Numerical results are stable under accepted stencil/window/model changes and pass withheld-point rules.
- Parabolic and nonparabolic domains are separately reported; Wannier derivatives, if later used, are independently verified against direct QE samples.

## Exclusions

- This Task runs no QE/Wannier program and does not infer mobility, scattering time, conductivity, quasiparticle masses, or experimental validation.
- Standard six-valley formulas are documented with their symmetry assumptions rather than silently assumed.

## Historical source

No archived source.
