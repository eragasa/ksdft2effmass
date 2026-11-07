# `Periodic2DRank2Study`

`Periodic2DRank2Study` is the immutable correlation of one nonempty study identity, one
exact `Periodic2DRank2BlockHoppingModel`, and its explicit `reference` or `candidate`
role. It inherits `Periodic2DStudy` and fixes retained rank two.

`Periodic2DRank2StudyOrchestrator` inherits `Periodic2DStudyOrchestrator`, accepts the
same explicit values, and constructs the study without selecting shell assignments,
thresholds, or persistence.

Named calculation compositions are separated by structure data:

- `calculations/periodic2d_rank2_sqr/band_equivalence_hopping_locality/study.py`;
- `calculations/periodic2d_rank2_hex/band_equivalence_hopping_locality/study.py`.

Both use the same concrete study and orchestrator classes. Each calculation function
combines that correlation with the peer hopping-locality analyzer using explicit
calculation-owned shell labels. Neither path introduces a square- or hexagonal-specific
subclass or claims a band-equivalence result.
