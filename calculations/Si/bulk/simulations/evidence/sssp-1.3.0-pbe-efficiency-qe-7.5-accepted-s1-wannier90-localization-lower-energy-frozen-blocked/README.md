# Blocked rank-10 lower-energy frozen-window occurrence

This directory retains the single authorized occurrence using the lower-energy frozen
window `[-5.85, 8.00] eV` and the accepted prospective Wannierisation policy. The
executable returned zero and printed its native completion message. ProjectKoios
correctly classified the output as ineligible because disentanglement exhausted its
budget without its convergence message.

## Convergence disposition

- Wannierisation converged at iteration 265 under
  `conv_tol = 2.0e-9 angstrom^2`, window 6.
- Final total spread was `19.532779948 angstrom^2`.
- Disentanglement exhausted 1000 iterations.
- Its final dimensionless fractional delta was `-2.091e-9`, about 20.9 times the
  declared `1.0e-10` threshold.
- Absolute disentanglement deltas decreased monotonically over iterations 801--1000,
  from `1.905e-8` to `2.091e-9`.
- Log-linear fits over the final 50, 100, and 200 iterations would cross `1.0e-10` near
  iterations 1285, 1283, and 1274, respectively. These are extrapolations, not calculated
  convergence results.

The scientific construction therefore resolved the previous Wannierisation failure but
did not complete disentanglement within the declared budget. The operator remains
blocked. Any iteration-budget revision requires a new decision, exact preflight, and
bounded authorization.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.8890222719392114e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.5475254411256856e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

These structural properties and successful Wannierisation do not override failed
disentanglement convergence.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-lower-energy-frozen-20261031T094734Z
```

`external-artifact-inventory.json` authenticates 39 files totaling 12,856,663 bytes.
The retained `campaign-result.json` SHA-256 is
`2767c9bcfd47b0ec06bd254f708dc77592eb746c2a1cec2947fdd446573c75c7`.

The authorization is consumed. No retry is authorized.
