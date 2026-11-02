# Simple-cubic context migration checklist

## Current owner

`calculations/periodic3d_rank2_simple_cubic/` owns the orthogonal periodic-3D rank-two
context. Its `band_equivalence_hopping_locality/` aggregate owns the calculation actions,
protocol, report, and replaceable output contract. The context root keeps gauge
alignment, frame transport, band equivalence, hopping locality, and support truncation
as distinct operation directories.

## Installed actions

- `run_nominal_calculation.py`
- `run_refinement_01.py`
- `run_refinement_02.py`
- `render_nominal_analysis.py`

The bounded nominal writer belongs in routine CI. Full refinement writers remain
explicitly expensive. No retained execution, scientific output, or convergence claim is
created by this migration.

## Migrated donors

- calculation donor:
  `calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/`;
- protocol donor:
  `experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`.

The donor calculation path is retired. The donor experiment path is an identity-
preserving forward pointer only. Protocol TeX and bibliography bytes were moved into
`protocol/` without content changes before internal path repair. Their pre-move SHA-256
values were `2f730d6db77a0f7f4fe64e1b3c95c31a9aea8ed02fa1885f82660adc96f5f0c3`
and `1a0efc2a4348d002485e1bd9533f22222aaebdbefb6030e37db0746896335353`,
respectively. The TeX now differs only where its parity-contract path targets the
calculation-owned shared document; the bibliography hash remains unchanged.

## Required consistency

1. All calculation, comparison, architecture, and publication references use the
   context-first owner path.
2. Output paths use `analysis/replaceable/` and `simulations/replaceable/`.
3. Geometry, gauge, band, locality, and support outcomes are not conflated.
4. Refinement is not described as retained convergence evidence.
5. The downstream dimensional comparison does not inherit identity, thresholds, or
   evidence status.
