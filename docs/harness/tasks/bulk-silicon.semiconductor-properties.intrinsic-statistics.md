<!-- Generated from SQLite control state; do not edit. -->
# Intrinsic carrier statistics

[Task index](index.md) · [Previous](./bulk-silicon.semiconductor-properties.dielectric-screening.md) · [Next](./bulk-silicon.simulation.qe.band-reference.md)

## Status

`blocked`: Conditional deterministic analysis Task; blocked by accepted band edges, electron and applicable hole DOS information, and a declared temperature/statistical model.

## Objective

Compute intrinsic chemical potential and carrier concentration versus temperature and compare Boltzmann/effective-DOS approximations with full Fermi–Dirac integration.

## Parent and prerequisites

- Parent: `bulk-silicon.semiconductor-properties`
- Depends on: `bulk-silicon.band-edge-characterization.effective-mass-analysis`
- Depends on: `bulk-silicon.band-edge-characterization.valence-edge`
- Depends on: `bulk-silicon.semiconductor-properties.density-of-states`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: analysis.
- Inputs are accepted E_c/E_v references, valley/band degeneracies, effective or numerical DOS, temperature grid, constants, and occupation model.
- Deterministic outputs are N_c(T), N_v(T), μ_i(T), n_i(T), full-integration comparisons, approximation residuals, and validity-range figures.
- The human owns temperature range, statistics, degeneracy conventions, hole-model adequacy, and physical-validation references.

## Completion criteria

- Energy references and the chemical-potential model are explicit.
- Boltzmann and full Fermi–Dirac results are compared over the declared range.
- Approximation, numerical-integration, parent-band, and external-reference discrepancies remain separate.

## Exclusions

- The VBM or midgap is not called the Fermi level without the applicable equilibrium statistical model.
- No doped-carrier, incomplete-ionization, band-gap-renormalization, or transport claim is inferred.

## Historical source

No archived source.
