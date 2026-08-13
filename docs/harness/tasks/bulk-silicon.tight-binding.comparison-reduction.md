<!-- Generated from SQLite control state; do not edit. -->
# Tight-binding comparison and reduction

[Task index](index.md) · [Previous](./bulk-silicon.simulation.qe.reference.md) · [Next](./bulk-silicon.tight-binding.direct-spectral.fitting.md)

## Status

`blocked`: Blocked by the production direct-spectral fit and production Wannier interpolation verification. The final join also requires human-owned model, alignment, metric, truncation, and compatibility decisions.

## Objective

Compare the direct-spectral and Wannier-mediated tight-binding models and evaluate explicitly declared reductions.

## Parent and prerequisites

- Depends on: `bulk-silicon.tight-binding.direct-spectral.fitting`
- Depends on: `bulk-silicon.wannier-reference.interpolation-verification`
- External prerequisite: `tight_binding_comparison_contract`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- docs/computational/ksdft2Effmass.computational.04.md
- docs/publications/papers/ksdft2effmass.P91/manuscript.tex

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
