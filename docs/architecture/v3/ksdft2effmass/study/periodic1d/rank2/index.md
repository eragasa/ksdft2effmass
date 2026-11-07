# `Periodic1DRank2Study`

`Periodic1DRank2Study` is the immutable correlation of one nonempty study identity, one
exact `Periodic1DRank2BlockHoppingModel`, and its explicit `reference` or `candidate`
role. It inherits `Periodic1DStudy` and fixes retained rank two.

`Periodic1DRank2StudyOrchestrator` inherits `Periodic1DStudyOrchestrator`, accepts the
same explicit values, and constructs the study without invoking the historical
`BlockHoppingModel1D` locality contract. The named composition is
`calculations/periodic1d_rank2/band_equivalence_hopping_locality/study.py`. No legacy
representation is inferred or migrated.
