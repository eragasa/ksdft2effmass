# `ksdft2effmass.periodic1d.admissible_sets.results`

## Purpose and status

Implemented immutable proof and result objects for M3.

## Public contract

- [`Periodic1DAdmissibleSetDisposition`](Periodic1DAdmissibleSetDisposition/index.md)
- [`Periodic1DQuadraticLoss`](Periodic1DQuadraticLoss/index.md)
- [`Periodic1DAdmissibleSetLocalityResult`](Periodic1DAdmissibleSetLocalityResult/index.md)
- [`Periodic1DAdmissibleSetParameterEvaluation`](Periodic1DAdmissibleSetParameterEvaluation/index.md)
- [`Periodic1DAdmissibleSetCaseResult`](Periodic1DAdmissibleSetCaseResult/index.md)
- [`Periodic1DConstrainedAdmissibleSetCalculationResult`](Periodic1DConstrainedAdmissibleSetCalculationResult/index.md)

## Ownership and invariants

The records enforce quadratic symmetry/curvature, role identity, finite losses,
witness/certificate/disposition consistency, locality correlation, domain membership,
and agreement between quadratics and sampled training losses.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/admissible_sets/results.py`.
Direct tests mutate quadratics, locality inventory, roles, thresholds, and Boolean
numeric fields.

## Limitations

A `certified-separated` enum value is meaningful only with its correlated lower bound,
resolution, continuous bounded domain, and verified unclipped-set premises.
