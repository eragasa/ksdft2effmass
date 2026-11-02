# Bain-path context migration checklist

## Current owner

`calculations/periodic3d_rank2_bain_path/` owns the unit-volume periodic-3D rank-two Bain
context. Its `band_equivalence_hopping_locality/` aggregate owns the authoritative
protocol, M0/M1/M2 actions, sampled scan, report, and replaceable output contract. Gauge
alignment, frame transport, band equivalence, hopping locality, and support truncation
remain distinct operation directories.

## Installed actions

- `run_geometry_control.py` — M0 geometry/frozen-gauge channel;
- `run_response_controls.py` — separate M1 frozen and M2 prescribed radial response;
- `run_path_scan.py` — qualification, 201-point base scan, and declared transition
  refinement.

No retained execution, generated scientific output, accepted common path witness,
convergence claim, or material conclusion is created by this migration.

## Migrated donors

- calculation donor: `calculations/periodic3d/rank2/strain-locality/`;
- protocol donor and legacy identity:
  `experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`;
- shared protocol donor:
  `experiments/model-adequacy/gauge-locality-under-synthetic-strain.md`.

The calculation donor is retired. Both experiment surfaces are forward pointers. The
shared donor text is preserved under `calculations/periodic/multiband/`; this context's
`protocol.md` is the dimension-specific authority.

## Required consistency

1. M0, M1, and M2 remain separate scientific channels with separate outcomes.
2. The common FCC-to-Bain map, state spaces, gauges, energy reference, units, and metric
   conventions remain explicit before operator comparison.
3. Sampled maxima are not continuum suprema; pointwise optimized controls are not one
   common path witness.
4. Output paths use `analysis/replaceable/`.
5. The path is not described as elastic, phase-stability, martensitic-transition,
   silicon, or other material evidence.
