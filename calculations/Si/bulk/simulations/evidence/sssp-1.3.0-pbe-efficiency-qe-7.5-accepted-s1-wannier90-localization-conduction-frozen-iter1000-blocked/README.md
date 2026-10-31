# Blocked conduction-frozen 1000-iteration localization occurrence

This directory retains the single authorized one-variable successor that increased only
Wannierisation `num_iter` from 500 to 1000. The executable returned zero and printed its
native completion message, but ProjectKoios classified the output as ineligible because
Wannierisation again lacked its convergence-criteria-satisfied message.

## Convergence disposition

- Disentanglement reproduced convergence at iteration 531.
- Its final dimensionless fractional delta was `9.017e-11`, below `1.0e-10`.
- Wannierisation reached the enlarged 1000-iteration budget without convergence.
- Its last reported spread change was `-1.30e-3 angstrom^2`, far above the absolute
  `1.0e-10 angstrom^2` criterion.
- The final total spread was `37.128984231 angstrom^2`, compared with
  `39.776686650 angstrom^2` after 500 iterations.
- Large late excursions remained, including increases near iterations 962, 971, and
  980; the trajectory does not support a simple iteration-limit remedy.

The generated Hamiltonian remains diagnostic output and is not accepted.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.7607570956812424e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

These structural properties do not override failed Wannierisation convergence.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-iter1000-20261031T085113Z
```

`external-artifact-inventory.json` authenticates 36 files totaling 13,699,461 bytes.
The retained `campaign-result.json` SHA-256 is
`3e766ff2641648b186e4f1110c962013a70e2d1a84dea2c27b5e41cff63f3cf6`.

The authorization is consumed. No retry is authorized.
