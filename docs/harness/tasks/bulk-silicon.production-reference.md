<!-- Generated from SQLite control state; do not edit. -->
# Bulk-silicon production reference program

[Task index](index.md) · [Previous](./bulk-silicon.band-edge-characterization.valence-edge.md) · [Next](./bulk-silicon.production-reference.convergence.md)

## Status

`inactive`: Planning-only G02 acceptance boundary. Essential children are defined but inactive; no production execution or automatic successor activation is authorized.

## Objective

Coordinate the accepted physical branch, numerical convergence, equilibrium geometry, production SCF parent, compact records, numerical verification, and separately declared physical validation needed to replace the tutorial SCF parent.

## Parent and prerequisites

None.

## Authority references

- docs/computational/bulk-silicon-production-program.md
- docs/computational/ksdft2Effmass.computational.02.md
- docs/publications/papers/ksdft2effmass.P91/manuscript.tex
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: physical validation.
- Bind the production pseudopotential authority, convergence, lattice-reference, and SCF children to one compatible physical and numerical specification.
- Retain parent-model, numerical/discretization, and validation errors separately and publish the stage visualizations as child deliverables.
- Require a human acceptance decision before freezing BulkSiReference-v1; the parent itself performs no scientific executable.

## Completion criteria

- Every essential child has an accepted manifest and its declared numerical-verification evidence.
- The accepted SCF state identifies density/potential lineage, geometry, pseudopotential, cutoffs, mesh, occupations, code, resources, restart state, and compact artifact inventory.
- Physical comparisons are labeled separately from convergence, limitations are explicit, and a human accepts or rejects the bounded G02 claim.

## Exclusions

- This Task does not execute calculations, choose unresolved alternatives, combine error classes, or imply experimental agreement.
- Closing the parent does not activate band-edge, Wannier, tight-binding, impurity, publication, or release work.

## Historical source

No archived source.
