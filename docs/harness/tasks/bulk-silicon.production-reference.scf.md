<!-- Generated from SQLite control state; do not edit. -->
# Production bulk-silicon SCF parent

[Task index](index.md) · [Previous](./bulk-silicon.production-reference.pseudopotential-selection.md) · [Next](./bulk-silicon.records.periodic.extraction.md)

## Status

`blocked`: Essential protected calculation; blocked by accepted convergence and lattice-reference records plus exact execution authorization.

## Objective

Construct and freeze the converged production n_SCF(r), V_KS[n_SCF](r), and identity-verified restart state consumed by all production child calculations.

## Parent and prerequisites

- Parent: `bulk-silicon.production-reference`
- Depends on: `bulk-silicon.production-reference.convergence`
- Depends on: `bulk-silicon.production-reference.lattice-reference`
- External prerequisite: `production_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- docs/computational/ksdft2Effmass.computational.02.md
- docs/publications/papers/ksdft2effmass.P91/manuscript.tex
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are the accepted branch, exact geometry, cutoffs, SCF mesh, occupations, iterative settings, executable/environment identity, and external artifact root.
- Retain input/output manifests, QEXSD semantic record, code-reported SCF iteration history when available, restart-state manifest, before/after inventory, separate streams, timing, resources, warnings, and immutable parent identity.
- Deterministic outputs include SCF diagnostic series and tutorial-versus-production comparison under explicitly compatible quantities only.
- The human owns warning disposition and final acceptance of the production parent; no child may consume an unidentified or mutable parent.

## Completion criteria

- Code-specific iterative convergence and cutoff/mesh/geometry convergence all pass their distinct rules.
- The compact record and external restart manifest are complete and reproducible.
- All warnings, unavailable quantities, and tutorial incompatibilities are explicit.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- The SCF k mesh is not assumed adequate for paths, local curvature, DOS, Wannierization, or tight-binding datasets.

## Historical source

No archived source.
