# `Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer`

## Status and responsibility

Implemented request-bound action object in
`ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.analysis`.
It composes one exact periodic-2D analytic case, gauge-alignment routes, frame
transport, Fourier reconstruction, physical-metric shell powers, support decisions, and
immutable case analysis without filesystem effects. The case action receives an explicit
axis-ordered `ReciprocalEndpointSewingInventory`; rank-N frame transport validates two
axis maps and the ambient frame dimension rather than constructing identity internally.
The retained synthetic v1 case contract accepts only named ambient-space identity
sewing selected at the composition boundary, preserving its existing result envelope.
The lower-level rank-N transport request is independently swappable and may receive a
qualified nonidentity map while retaining that map with its transport result.

## Deferred numerical limitation

The locality summary currently derives normalized non-onsite power as
`max(0.0, total_power - onsite_power)` after total and onsite powers have been rounded
separately. Under the selected bounded baseline this can suppress only roundoff-scale
power and does not affect support selection, which uses direct shell sums. A reported
zero is therefore not proof that all nonzero-displacement hopping blocks vanish.

This limitation is tracked as
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).

## Mapping and evidence

- Source: `python/src/ksdft2effmass/periodic2d/rankN/band_equivalence_hopping_locality/analysis.py`
- Test: `python/tests/ksdft2effmass/periodic2d/rankN/test__Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer.py`
- Sphinx: `doc/sphinx/api/band-equivalence-hopping-locality.rst`
- Evidence status: bounded software and numerical verification only; no retained
  production execution or scientific validation is authorized.

## Related pages

- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematic](schematics.md)
