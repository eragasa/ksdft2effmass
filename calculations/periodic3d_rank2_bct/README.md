# Periodic-3D rank-two BCT study

**Status: executable in-memory locality composition; no retained result**

This calculation owner binds the body-centered-tetragonal study identity to the
structure-agnostic `Periodic3DRank2Study` hierarchy. The existing controlled Bain-path
context under `calculations/periodic3d_rank2_bain_path/` remains unchanged; this
scaffold does not classify that complete path as one static BCT result.

- [`band_equivalence_hopping_locality/study.py`](band_equivalence_hopping_locality/study.py)
  correlates an exact reference or candidate model and calculates unchanged hopping
  power for the supplied metric-shell labels.

Band-equivalence comparison is not yet implemented by this module. No numerical result
or scientific acceptance claim is retained here.
