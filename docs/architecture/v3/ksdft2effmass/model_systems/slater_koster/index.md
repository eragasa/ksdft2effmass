# `ksdft2effmass.model_systems.slater_koster`

## Purpose

This package owns the reusable Level 1 Slater--Koster foundation required by the
bulk-silicon post-S110 protocol. It implements a spinless, orthogonal, homopolar
first/second-neighbor diamond $sp^3s^*$ model. It does not fit parameters, read campaign
evidence, select a reduction, or establish semiconductor-model adequacy.

The public model fixes:

- the ten-orbital order
  `(A:s,px,py,pz,s*, B:s,px,py,pz,s*)`;
- conventional Cartesian $p$ axes;
- the right-handed two-site diamond primitive cell;
- reciprocal-fractional k-point coordinates;
- full-center Bloch phases that include $R+\tau$;
- the 15 real eV parameters declared for S110 M2;
- four unique A-to-B first-neighbor bonds and the complete 12-vector
  same-sublattice second shell; and
- canonical typed-JSON serialization of the model definition.

See [numerics](numerics.md) for the matrix and phase conventions and
[implementation](implementation.md) for ownership and verification boundaries.

## Public owners

- `DiamondSp3sStarGeometry` owns lattice scale, handedness, site positions, and
  neighbor maps.
- `DiamondSp3sStarParameters` owns the stable 15-entry real parameter order.
- `DiamondSp3sStarModel` constructs an exact-Hermitian 10-by-10 Hamiltonian in eV.
- `DiamondSp3sStarModelJsonSerializer` records the definition deterministically through
  the repository typed-JSON serializer.

## Scientific boundary

Synthetic software tests establish implementation behavior only. No retained Wannier
operator, 408-point development oracle, 402-point confirmation oracle, or calculator
output is consumed by this package. Level 2 spectral feasibility and all later
post-S110 continuation levels remain separately authorized work.
