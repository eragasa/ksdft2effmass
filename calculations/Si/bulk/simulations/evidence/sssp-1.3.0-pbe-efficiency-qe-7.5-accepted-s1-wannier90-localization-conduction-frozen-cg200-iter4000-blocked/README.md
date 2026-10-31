# Blocked long-CG 4000-iteration occurrence

This directory retains the single authorized occurrence that changed only `num_iter`
from 1000 to 4000 relative to the `num_cg_steps = 200` predecessor. The executable
returned zero and printed its native completion message, but ProjectKoios classified the
output as ineligible because Wannierisation lacked the campaign's native strict
convergence message.

## Convergence disposition

- Disentanglement reproduced convergence at iteration 531 with final dimensionless
  fractional delta `9.017e-11`.
- Wannierisation exhausted 4000 iterations.
- The final spread change was `-2.48e-5 angstrom^2` versus the campaign's absolute
  `1.0e-10 angstrom^2` threshold.
- The final total spread was `36.557416368 angstrom^2`, only about
  `0.00608 angstrom^2` below the 1000-iteration predecessor.
- The best three-iteration window began at iteration 1413 and had maximum absolute
  change `5.02e-8 angstrom^2`: 502 times the campaign threshold and about 25 times the
  comparison AiiDA precise two-atom threshold `2.0e-9 angstrom^2`.
- Five three-iteration windows met the comparison AiiDA moderate two-atom threshold
  `2.0e-7 angstrom^2`; the first began at iteration 1411.
- No window met the comparison precise threshold.
- After iteration 1000, 277 iterations had absolute changes above
  `0.05 angstrom^2`; the last was iteration 3934.

Thus, a workflow using the comparison moderate tolerance would have stopped at a
transient plateau, but this occurrence did not satisfy the declared campaign gate or the
comparison precise gate and continued to show late excursions. This retrospective
comparison does not revise the campaign tolerance or establish operator acceptance.
`trajectory-analysis.json` retains the deterministic details.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.7662060702861027e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

These structural properties do not override failed localization convergence.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-cg200-iter4000-20261031T093641Z
```

`external-artifact-inventory.json` authenticates 40 files totaling 17,362,179 bytes.
The retained `campaign-result.json` SHA-256 is
`2ff5edd02fb25fe0dc0dab8c8ebbd7b6ce15e6b7e7a519d67a14b1e04f894caa`.

The authorization is consumed. No retry is authorized. Under the prospective stop rule,
iteration-only and optimizer-combination studies now stop; a successor requires a new
scientific construction or an explicitly reviewed convergence-policy revision.
