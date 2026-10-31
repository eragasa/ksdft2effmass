# Blocked conduction-frozen guiding-centres occurrence

This directory retains the single authorized one-variable occurrence that added only
`guiding_centres = .true.` to the blocked 1000-iteration input. The executable returned
zero and printed its native completion message, but ProjectKoios classified the output
as ineligible because Wannierisation again lacked its convergence-criteria-satisfied
message.

## Convergence disposition

- Disentanglement reproduced convergence at iteration 531.
- Its final dimensionless fractional delta was `9.017e-11`, below `1.0e-10`.
- Wannierisation reached 1000 iterations without convergence.
- Its final reported spread change was `-5.07e-3 angstrom^2`, versus the absolute
  `1.0e-10 angstrom^2` threshold.
- The final total spread was `52.632067930 angstrom^2`, higher than the unguided
  1000-iteration value `37.128984231 angstrom^2`.
- Late excursions and large gradient norms persisted. Guiding centres did not resolve
  this conduction-frozen localization problem under the declared controls.

The generated Hamiltonian remains diagnostic output and is not accepted.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.690586559632834e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

These structural properties do not override failed Wannierisation convergence.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-guiding-centres-20261031T090944Z
```

`external-artifact-inventory.json` authenticates 36 files totaling 13,700,087 bytes.
The retained `campaign-result.json` SHA-256 is
`e59f2ac5d0076e32dd90bdc3671df8a53016777636d54c9b515c66337cf93d40`.

The authorization is consumed. No retry is authorized.
