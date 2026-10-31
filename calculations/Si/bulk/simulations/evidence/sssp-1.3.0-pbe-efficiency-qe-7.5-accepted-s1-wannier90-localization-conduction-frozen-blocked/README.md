# Blocked conduction-frozen localization occurrence

This directory retains the single authorized conduction-frozen Wannier90 3.1.0
localization occurrence. The executable returned zero and printed its native completion
message. ProjectKoios nevertheless classified the outputs as ineligible because
Wannierisation did not print its convergence-criteria-satisfied message.

## Exact scientific change

Relative to the conditioned and damped blocked occurrence, the only scientific input
change was the frozen interval `[6.00, 19.02] eV`. The authenticated EIG table confirms
that this interval contains exactly all eight conduction bands and no valence bands at
every one of the 64 sampled k points. The remaining two dimensions of the rank-10
subspace were selected from four valence bands.

The 12-band outer window, projections, NNKP/AMN/MMN/EIG bytes, conditioning, damping,
iteration budgets, and both convergence thresholds were unchanged. In particular,
`dis_conv_tol = 1.0e-10` is a dimensionless fractional threshold, whereas
`conv_tol = 1.0e-10 angstrom^2` is the absolute Wannierisation spread-change threshold.

## Convergence disposition

- Disentanglement **converged** at iteration 531.
- Its final dimensionless fractional delta was `9.017e-11`, below `1.0e-10`.
- Wannierisation reached iteration 500 without its required convergence message.
- The final total spread was `39.776686650 angstrom^2`.
- The occurrence is therefore blocked despite native return code zero and
  `All done: wannier90 exiting`.

The late Wannierisation trajectory remained irregular, including sizable excursions,
so the final Hamiltonian is diagnostic output rather than an accepted operator.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, with maximum unitarity residual
  `1.6778840045852018e-10`;
- 64 `12 x 10` disentanglement matrices, with maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

These properties establish structural consistency only. They do not override the failed
Wannierisation gate or establish interpolation or effective-mass accuracy.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-20261031T084540Z
```

`external-artifact-inventory.json` authenticates 36 files totaling 13,091,354 bytes.
The retained `campaign-result.json` SHA-256 is
`f23bb43b486a14c674a4d5ecd8d0f24f3dac2186363d1e43f30ff096299df7bb`.

The authorization is consumed. No retry is authorized.
