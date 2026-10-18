# Simple-cubic band equivalence versus hopping locality

## Identity

- Family: `ksdft2effmass.campaign.model-adequacy.periodic3d.band-equivalence-versus-hopping-locality`.
- Source: `experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`.
- Status: substantive protocol with bounded `8 x 8 x 8`, `16 x 16 x 16`, and
  `32 x 32 x 32` Monkhorst--Pack local actions and independently verified replaceable
  records; no immutable version, qualified convergence disposition, or retained evidence.

## Scientific role

This family introduces a third exchange-equivalent periodic coordinate by mirroring the
1-D directed-hopping parent and sine rotation along all axes. It constructs the finite
parent with Kronecker lattice translations and converts it exactly among cell--orbital,
Bloch, retained-frame, and Wannier/TB representations before any aligned Hamiltonian
subtraction. The fields preserve axis permutations and global inversion covariance;
truncation supports use complete cubic signed-permutation shells without assuming
coefficient equality on those shells. The experiment compares gauge-related rank-two
representations at equal sampled band accuracy.

## Architecture bundle

- [Science](science.md)
- [Numerics](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

The scalar isotropic 3-D hopping-support hierarchy is a separate family. No silicon or
other material interpretation is inherited.
