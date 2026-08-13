<!-- Generated from SQLite control state; do not edit. -->
# Direct spectral tight-binding fitting

[Task index](index.md) · [Previous](./bulk-silicon.tight-binding.comparison-reduction.md) · [Next](./bulk-silicon.tight-binding.wannier.bridge.md)

## Status

`blocked`: Blocked by the inactive production symmetry-path, local-valley, and effective-mass Tasks and by human-owned fitting-contract decisions. Tutorial path/extraction evidence is not a production fitting dataset.

## Objective

Construct pre-frozen production spectral training and withheld-validation targets and fit one declared direct tight-binding parameterization without data leakage.

## Parent and prerequisites

- Depends on: `bulk-silicon.band-edge-characterization.conduction-valley`
- Depends on: `bulk-silicon.band-edge-characterization.effective-mass-analysis`
- Depends on: `bulk-silicon.band-edge-characterization.symmetry-path`
- External prerequisite: `direct_tb_fitting_contract`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- docs/computational/ksdft2Effmass.computational.04.md
- docs/publications/papers/ksdft2effmass.P91/manuscript.tex

## Authorized scope

- Define training and withheld target partitions with parent identities.
- Fit only the accepted basis, parameterization, objective, weights, and constraints.
- Retain fitted parameters, model geometry, target identities, and residuals.

## Completion criteria

- The fit is reproducible from retained records and settings.
- Training and withheld results are separate.
- Accepted metrics and tolerances are evaluated.
- Spectral-fit limitations and error classes are explicit.

## Exclusions

- Spectral fitting is not claimed to reconstruct a unique operator.
- Withheld targets are not used during fitting.
- Fitting, parent-model, discretization, and reduction errors are not conflated.
- No scientific validation is claimed without independent reference evidence.

## Historical source

No archived source.
