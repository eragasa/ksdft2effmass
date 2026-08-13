<!-- Generated from SQLite control state; do not edit. -->
# Bulk-silicon production Wannier reference

[Task index](index.md) · [Previous](./bulk-silicon.tight-binding.wannier.extraction.md) · [Next](./bulk-silicon.wannier-reference.interface.md)

## Status

`inactive`: Planning-only G03 acceptance boundary. All children are blocked by G02 and human-owned subspace/window/projection decisions; no Wannier execution is authorized.

## Objective

Coordinate the production uniform NSCF child, QE–Wannier90 interface, Wannier construction, localization assessment, and independent interpolation verification.

## Parent and prerequisites

None.

## Authority references

- docs/computational/bulk-silicon-production-program.md
- docs/computational/ksdft2Effmass.computational.03.md
- docs/publications/papers/ksdft2effmass.P91/manuscript.tex
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: numerical verification.
- Bind the Wannier branch to the accepted production SCF parent and explicit target subspace.
- Separate interface generation, localization/disentanglement, convergence/sensitivity, interpolation verification, and final operator acceptance.
- Require a human acceptance decision before freezing BulkSiWannier-v1.

## Completion criteria

- Uniform-grid, interface, localization, and interpolation-verification records are complete and mutually compatible.
- Centers, spreads, hopping decay, band-edge interpolation, and withheld-grid residuals pass accepted rules.
- Gauge, windows, projections, truncation, parent lineage, and limitations are explicit.

## Exclusions

- A successful interface or low spread alone does not validate interpolation or scientific suitability.
- Wannierization is not described as a low-rank approximation and does not automatically define the final TB model.

## Historical source

No archived source.
