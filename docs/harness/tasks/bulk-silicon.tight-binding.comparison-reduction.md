<!-- Generated from SQLite control state; do not edit. -->
# Tight-binding comparison and reduction

[Task index](index.md) · [Previous](./bulk-silicon.simulation.qe.reference.md) · [Next](./bulk-silicon.tight-binding.direct-spectral.fitting.md)

## Status

`blocked`: Blocked by both direct-spectral fitting and Wannier Hamiltonian extraction.

## Objective

Compare the direct-spectral and Wannier-mediated tight-binding models and evaluate explicitly declared reductions.

## Parent and prerequisites

- Depends on: `bulk-silicon.tight-binding.direct-spectral.fitting`
- Depends on: `bulk-silicon.tight-binding.wannier.extraction`
- External prerequisite: `tight_binding_comparison_contract`

## Authority references

- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Compare common spectral observables.
- Compare represented operators only after compatibility and alignment prerequisites succeed.
- Evaluate accepted range, shell, orbital, or block reductions.
- Report parent-model, fitting, Wannierization, numerical, and reduction errors separately.

## Completion criteria

- Every comparison identifies its state spaces, bases, geometry, units, energy references, parent identities, and truncation state.
- Compatibility failures are explicit.
- Observable and represented-operator comparisons remain distinct.
- Accepted metrics and reduction tolerances are evaluated.

## Exclusions

- Unidentified or unaligned operators are not subtracted.
- Metadata similarity alone does not establish physical equivalence.
- Incompatible error definitions are not combined.
- No scientific validation or impurity interpretation is inferred.

## Historical source

No archived source.
