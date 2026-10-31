# Blocked conduction-frozen fixed-step-1 occurrence

This directory retains the single authorized occurrence that replaced Wannier90's
parabolic line search with dimensionless `fixed_step = 1.0`. The executable returned
zero and printed its native completion message, but ProjectKoios classified the output
as ineligible because Wannierisation again lacked its convergence-criteria-satisfied
message.

## Convergence disposition

- Disentanglement reproduced convergence at iteration 531.
- Its final dimensionless fractional delta was `9.017e-11`, below `1.0e-10`.
- Wannierisation reached 1000 iterations without convergence.
- Its final spread change was `-2.95e-2 angstrom^2`, versus the absolute
  `1.0e-10 angstrom^2` threshold.
- The final total spread was `50.615119724 angstrom^2`, higher than the native
  parabolic-line-search comparator's `37.128984231 angstrom^2`.
- Large excursions persisted. The fixed-step policy did not resolve this
  conduction-frozen localization problem.

The generated Hamiltonian remains diagnostic output and is not accepted.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.7229406790164603e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-fixed-step1-20261031T091916Z
```

`external-artifact-inventory.json` authenticates 36 files totaling 13,700,066 bytes.
The retained `campaign-result.json` SHA-256 is
`7acfb6e1cf033d5e9ab415d4cfb01d0b29caf91c754dc0a1dd3bb9b63a619a1f`.

The authorization is consumed. No retry is authorized.
