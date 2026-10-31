# Failed volume-only bulk relaxation attempt

## Status

One explicitly authorized Quantum ESPRESSO 7.5 invocation was attempted without retry.
QE rejected the native input during setup, before any SCF or structural-relaxation step
started:

```text
Error in routine cell_dofree (1):
Isotropic expansion is only allowed for ibrav=1; i.e. for simple cubic
```

The provider-neutral volume-only declaration rendered as `ibrav=0` with explicit FCC
primitive vectors and `cell_dofree='volume'`. QE 7.5 does not admit that combination.
There is no relaxed structure, energy trajectory, force observation, pressure
observation, or scientific result from this occurrence.

The external evidence root is:

```text
/Users/eugene/projects/ksdft2effmass/
  si-bulk-vc-relax-gamma-k10-c42-20261031T055443Z/
```

[`external-artifact-inventory.json`](external-artifact-inventory.json) authenticates
all retained external files. The compact repository copy includes the declaration,
rendered input, native output, crash record, execution record, and failure disposition.

## Bound attempted input

- right-handed primitive Si structure;
- Gamma-centered K10;
- 42/336 Ry wavefunction/density cutoffs;
- volume-only BFGS cell dynamics;
- target pressure 0 kbar and pressure tolerance 0.5 kbar;
- force tolerance 0.01 eV/Å;
- ionic energy tolerance `1e-4 eV`;
- electronic tolerance `1e-6 Ry`; and
- maximum 200 ionic steps.

## Required correction

The reusable QE integration cannot represent strict isotropic FCC relaxation by pairing
explicit `ibrav=0` vectors with QE's `cell_dofree='volume'`. A corrected route must be
reviewed before another calculator invocation. Defensible routes are:

1. add a verified FCC-native `ibrav` mapping and use QE's Bravais-preserving cell
dynamics, with explicit direct-, fractional-, and reciprocal-coordinate transforms; or
2. preserve `ibrav=0` and implement a calculator-neutral scalar-volume optimization or
finite-volume equation-of-state route from fixed-cell calculations.

Changing to unconstrained `cell_dofree='all'` is not an equivalent correction because it
would expand the declared cell degrees of freedom. No retry is authorized by this
record.
