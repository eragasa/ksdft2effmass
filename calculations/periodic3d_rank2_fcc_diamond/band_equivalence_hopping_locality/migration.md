# FCC/diamond context migration checklist

## Current owner

`calculations/periodic3d_rank2_fcc_diamond/` owns the nonorthogonal periodic-3D rank-two
FCC-Bravais/diamond-basis context and its matched controls. Its
`band_equivalence_hopping_locality/` aggregate owns actions, protocol, report, and
replaceable output contracts. Gauge alignment, frame transport, band equivalence,
hopping locality, and support truncation remain distinct operation directories.

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
  `calculations/periodic3d/rank2/nonorthogonal/band-equivalence-locality/`;
- protocol donor:
  `experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`.

The donor calculation path is retired. The donor experiment path is an identity-
preserving forward pointer only. Protocol TeX and bibliography bytes were moved into
`protocol/` without content changes before internal path repair. Their pre-move SHA-256
values were `cb9a26fce5729e6922c034e7673a1426b4d9cd086abcd4d7a92ce3088f880ad1`
and `1a0efc2a4348d002485e1bd9533f22222aaebdbefb6030e37db0746896335353`,
respectively. The TeX now differs only where its parity-contract path targets the
calculation-owned shared document; the bibliography hash remains unchanged.

## Required consistency

1. All references use the context-first owner path.
2. Output paths use `analysis/replaceable/` and `simulations/replaceable/`.
3. FCC geometry, diamond basis, matched controls, and frame diagnostics retain their
   context-specific definitions.
4. The synthetic diamond-basis case is never described as silicon, material validation,
   or effective-mass evidence.
5. Refinement is not described as retained convergence evidence, and the downstream
   dimensional comparison inherits no identity, thresholds, or evidence status.
