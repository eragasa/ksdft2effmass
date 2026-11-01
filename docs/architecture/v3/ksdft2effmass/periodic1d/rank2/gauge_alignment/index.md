# Rank-two gauge alignment

`ksdft2effmass.periodic1d.rank2.gauge_alignment` owns the reusable periodic-1D
rank-two right-unitary alignment capability. It receives already identified reference
and attacked orthonormal frame paths, selects pointwise and one aggregate Procrustes
right actions, and returns the aligned paths, selected matrices, singular-value evidence,
and applied rank cutoffs.

The capability implements the periodic-1D specializations of the shared
`GaugeAlignmentAnalysisRequest`, `GaugeAlignmentAnalysis`, and
`GaugeAlignmentAnalyzer` role contracts. Every role exposes the same validated
`GaugeAlignmentAnalysisIdentity` with rank two, `U(2)`, right action, and the
Euclidean-orthonormal inner product through the standard action triad:

- `Periodic1DRank2GaugeAlignmentAnalysisRequest` binds two rank-two frame paths on
  one reciprocal mesh and ambient state-space dimension, together with the Procrustes
  tolerances;
- `Periodic1DRank2GaugeAlignmentAnalyzer` selects the right actions; and
- `Periodic1DRank2GaugeAlignmentAnalysis` retains correlated rank-two aligned paths,
  one pointwise transformation per reciprocal sample, the global transformation, and
  selection diagnostics.

The capability does not own the four-state parent, attack construction, hopping
transforms, support truncation, aggregate result wire, verification, or rendering. The
rank-two composite band-alignment study consumes it from
`rank2.band_alignment.composite`; the gauge-alignment capability does not import the
composite study.

- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
