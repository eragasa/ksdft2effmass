# Blocked literature-informed long-CG occurrence

This directory retains the single authorized occurrence that changed only
`num_cg_steps` from the verified Wannier90 3.1.0 default 5 to the current AiiDA
high-throughput protocol value 200. The executable returned zero and printed its native
completion message, but ProjectKoios classified the output as ineligible because
Wannierisation lacked its convergence-criteria-satisfied message.

## Protocol scope

The candidate retained the campaign's strict tolerances and 1000-iteration budgets. It
did not adopt the AiiDA workflow's per-atom tolerances, 4000-iteration budgets, or other
settings. `literature-protocol-observation.json` binds the commit-pinned protocol
observation. The value 200 is a bounded literature-informed coordinate, not a universal
literature standard.

## Convergence disposition

- Disentanglement reproduced convergence at iteration 531.
- Its final dimensionless fractional delta was `9.017e-11`, below `1.0e-10`.
- Wannierisation reached 1000 iterations without convergence.
- Its final spread change was `-5.29e-5 angstrom^2`, versus the absolute
  `1.0e-10 angstrom^2` threshold.
- The best three-iteration maximum absolute change was `7.67e-6 angstrom^2`, beginning
  at iteration 609. This remains about 38 times the current AiiDA moderate two-atom
  threshold of `2.0e-7 angstrom^2`.
- The final total spread was `36.563494226 angstrom^2`, lower than the native-default-CG
  1000-iteration comparator's `37.128984231 angstrom^2` but still nonstationary.

The longer CG cadence improved some diagnostic spread measures but did not satisfy the
campaign gate or the literature-associated moderate gate. The generated Hamiltonian is
not accepted.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.8743717689062578e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-cg200-20261031T093233Z
```

`external-artifact-inventory.json` authenticates 38 files totaling 13,706,134 bytes.
The retained `campaign-result.json` SHA-256 is
`5f81a2ba6ed3118d4eb75fcba24059ca26af2de30cb73f559b204c56494b0255`.

The authorization is consumed. No retry is authorized.
