# `Periodic3DRank2Study`

`Periodic3DRank2Study` is the immutable correlation of one nonempty study identity, one
exact `Periodic3DRank2BlockHoppingModel`, and its explicit `reference` or `candidate`
role. It inherits `Periodic3DStudy` and fixes retained rank two.

`Periodic3DRank2StudyOrchestrator` inherits `Periodic3DStudyOrchestrator`, accepts the
same explicit values, and constructs the study without branching on crystal structure.

FCC, BCT, diamond, and simple cubic therefore use this same concrete study type. Their
ordered lattice geometry, physical unit, basis identity, energy reference, and model
role remain data owned by the supplied scientific model; named calculation directories
own further analysis composition and evidence:

- `calculations/periodic3d_rank2_fcc/band_equivalence_hopping_locality/study.py`;
- `calculations/periodic3d_rank2_bct/band_equivalence_hopping_locality/study.py`;
- `calculations/periodic3d_rank2_dia/band_equivalence_hopping_locality/study.py`;
- `calculations/periodic3d_rank2_sc/band_equivalence_hopping_locality/study.py`.

Each calculation function combines the structure-agnostic correlation with the peer
hopping-locality analyzer using explicit calculation-owned shell labels. These modules
do not yet claim a band-equivalence result.
