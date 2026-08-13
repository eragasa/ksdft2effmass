<!-- Generated from SQLite control state; do not edit. -->
# Bulk-silicon band-edge characterization

[Task index](index.md) · [Previous](./bulk-silicon.artifacts.qe.inventory.md) · [Next](./bulk-silicon.band-edge-characterization.conduction-valley.md)

## Status

`inactive`: Planning-only G02 band-edge acceptance boundary. The non-SOC electron pilot is essential; valence/SOC extensions remain conditional. No child is active.

## Objective

Coordinate purpose-specific production band sampling, deterministic edge analysis, effective-mass extraction, visualizations, numerical verification, and bounded physical comparisons.

## Parent and prerequisites

None.

## Authority references

- docs/computational/bulk-silicon-downstream-sampling-plan.md
- docs/computational/bulk-silicon-production-program.md
- docs/publications/papers/ksdft2effmass.P91/manuscript.tex
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: numerical verification.
- Bind every sampled child to the same accepted production SCF parent and explicit coordinate and energy-reference conventions.
- Keep symmetry-path inspection, local conduction-valley fitting, valence-manifold analysis, and withheld numerical verification as distinct datasets.
- Require human acceptance before freezing band-edge quantities; the parent performs no scientific executable.

## Completion criteria

- Essential non-SOC band-edge children pass accepted numerical rules and report indirect gap, valley position, m_l*, m_t*, tensor conventions, and withheld residuals.
- Conditional valence/SOC claims are absent or supported by their separately compatible branch.
- Figures, compact records, physical comparisons, and limitations are complete.

## Exclusions

- No path alone establishes a full mass tensor, Wannier mesh, DOS integration, or complete fitting dataset.
- No Kohn–Sham band result is represented as a many-body excitation spectrum.

## Historical source

No archived source.
