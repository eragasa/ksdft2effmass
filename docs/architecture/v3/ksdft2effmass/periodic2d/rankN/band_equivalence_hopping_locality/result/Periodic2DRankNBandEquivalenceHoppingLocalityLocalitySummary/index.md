# `Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary`

## Status and responsibility

Implemented immutable result object in
`ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.result`.
It retains built-in finite nonnegative normalized total, onsite, and non-onsite hopping
powers and requires their scalar partition to agree within the installed absolute
`1.0e-12` check.

## Deferred numerical limitation

The object validates supplied scalars but does not own or reconstruct the underlying
hopping inventory. Its current producer derives non-onsite power by subtracting
separately rounded total and onsite sums and clipping at zero. Consequently, a stored
zero is not an exact certificate that all nonzero-displacement blocks vanish.

This limitation is tracked as
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).

## Mapping and evidence

- Source: `python/src/ksdft2effmass/periodic2d/rankN/band_equivalence_hopping_locality/result.py`
- Producer test: `python/tests/ksdft2effmass/periodic2d/rankN/test__Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer.py`
- Sphinx: `doc/sphinx/api/band-equivalence-hopping-locality.rst`
- Serialization preserves the scalar value; it does not upgrade zero to an exact
  scientific statement.

## Related pages

- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematic](schematics.md)
