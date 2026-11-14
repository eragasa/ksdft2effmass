# `Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer`

## Status and responsibility

Implemented case-bound numerical reference action in
`ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.fourier_reference`.
It independently reconstructs finite Fourier fields, shell powers, truncation errors,
and support selections without calling the production Fourier transformer or support
selector.

## Deferred numerical limitation

For the locality summary's non-onsite scalar only, the reference currently repeats the
producer formula `max(0.0, total_power - onsite_power)`. It therefore shares the
subtraction-induced roundoff false-zero mechanism and is not independent for that one
scalar. Its direct shell-power and support comparisons are unaffected.

This limitation is tracked as
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).

## Mapping and evidence

- Source: `python/src/ksdft2effmass/periodic2d/rankN/band_equivalence_hopping_locality/fourier_reference.py`
- Test: `python/tests/ksdft2effmass/periodic2d/rankN/test__Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer.py`
- Sphinx: `doc/sphinx/api/band-equivalence-hopping-locality.rst`
- Evidence status: bounded numerical comparison, excluding independent confirmation of
  the non-onsite summary partition.

## Related pages

- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematic](schematics.md)
