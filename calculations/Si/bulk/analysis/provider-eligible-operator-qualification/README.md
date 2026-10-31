# Provider-eligible operator characterization

## Purpose

This calculation-local, object-oriented analysis characterizes the provider-eligible
lower-energy-frozen Wannier operator before withheld parent validation. The code is
intentionally retained under `calculations/` for campaign use and must be migrated to
its reusable domain owner before merge.

No Quantum ESPRESSO or Wannier90 process is invoked. The analysis verifies structural
reconstruction, then records interpolation, valley, curvature, and locality properties.
It does **not** assign scientific pass/fail status to those candidate predictions. They
are what the finite operator predicts and become targets for later parent comparison.

## Bound inputs

The analysis authenticates, before parsing:

- the accepted relaxed structure;
- the retained 12-band EIG interface table;
- `_hr.dat`, `_u.mat`, and `_u_dis.mat` from the blocked 1000-step predecessor;
- the corresponding three artifacts from the provider-eligible 1290-step occurrence;
  and
- each occurrence's external `_wsvec.dat`, whose exact identity is already bound by
  the retained external-artifact inventory.

The two `_wsvec.dat` files remain outside Git at the inventory-declared external roots.
The script reads them in place and checks byte count and SHA-256. It does not acquire,
copy, or alter them. Their use is required because both native occurrences used
`use_ws_distance = .true.`; dense interpolation without the element-resolved WS shifts
would not reproduce the native Wannier90 interpolant.

Maintained ProjectKoios parsers decode EIG, HR, U, and U-dis. The calculation-local WS
parser is part of the prototype migration surface. PhysKit `DirectLattice3D` and
`ReciprocalLattice3D` own the lattice geometry. Result bytes are produced by KSD's
generic `TypedJsonMappingSerializer`, not by a calculation-specific JSON codec.

## Analysis objects

`ProviderEligibleOperatorQualification` composes immutable declarations and focused
action objects:

1. `ArtifactAuthenticator` verifies exact source identities.
2. `CandidateOperatorLoader` constructs native-gauge and WS-corrected finite
   Hamiltonians.
3. `SourceReconstructionAnalyzer` compares the HR reconstruction with
   \(U^\dagger U_{\mathrm{dis}}^\dagger E U_{\mathrm{dis}} U\) at all 64 source
   points and checks all 304 frozen states.
4. `SpectralStabilityAnalyzer` compares the unaligned 1000- and 1290-step candidates
   only through ordered spectra on source and `41 x 41 x 41` grids.
5. `ValleyFamilyAnalyzer` locates the six Cartesian Delta-valley candidates from
   independently classified dense-grid starts.
6. `EffectiveMassAnalyzer` computes descriptive Cartesian Hessians at four stencil
   scales.
7. `LocalityAnalyzer` resolves element-shifted physical-radius shells and evaluates
   finite-cutoff spectral sensitivity on a `21 x 21 x 21` grid.

## Declared controls

Only source reconstruction has a pass/fail role because it checks whether two
representations of the same constructed operator agree within native decimal
serialization precision:

- `2e-5 eV` maximum matrix-element discrepancy;
- `5e-5 eV` maximum per-point matrix Frobenius discrepancy;
- `2e-5 eV` maximum spectral discrepancy; and
- `2e-5 eV` maximum matched frozen-state discrepancy.

The remaining settings define observations rather than acceptance gates:

- Gamma-origin `41 x 41 x 41` spectral and valley grid;
- a `0.5 eV` edge-reporting window;
- Hessian steps `0.001`, `0.002`, `0.005`, and `0.010 inverse angstrom`; and
- shell truncation on a Gamma-origin `21 x 21 x 21` grid, with the shell at or below
  two relaxed conventional lattice parameters reported explicitly.

No candidate-only valley-energy, mass, or locality threshold can establish agreement
with the parent operator. Those tolerances must be defined for a separately declared
withheld QE comparison before that comparison is executed.

## Run

From the repository root, with the retained ProjectKoios tranche available:

```text
PYTHONPATH=python/src:/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1/src/python \
  python/.venv/bin/python \
  calculations/Si/bulk/analysis/provider-eligible-operator-qualification/run_analysis.py
```

The script writes `qualification-result.json` through the generic typed serializer.

## Observations

Structural reconstruction is verified:

- maximum HR/native-gauge spectral discrepancy: `1.1859e-5 eV`;
- maximum matched frozen-state discrepancy across 304 states: `1.1785e-9 eV`.

The final disentanglement extension has a small spectral effect:

- maximum 1290-step versus 1000-step dense spectral difference: `1.7180e-4 eV`;
- maximum corresponding lowest-conduction difference: `7.7774e-5 eV`.

The candidate's descriptive predictions are:

- six located Delta-family minima spanning `65.507 meV` in the candidate interpolant;
- positive principal curvatures and a maximum cross-stencil principal-mass variation
  of `5.55e-4`;
- at the shell at two relaxed lattice parameters, `26.904 meV` maximum all-band
  truncation sensitivity and `19.463 meV` maximum lowest-conduction sensitivity; and
- exact finite-representation recovery after the final represented shell at
  `11.6019 angstrom`.

These are not failures by themselves. The valley spread is a quantity for withheld
parent comparison, and the locality curve constrains any later short-range reduction;
neither invalidates the full finite Wannier operator without an intended-use tolerance.
The operator therefore remains **provider-eligible, characterized, and scientifically
unassessed** pending separately authorized withheld parent validation.

Result SHA-256:
`e82995489fd5e5084008c0a7d8bf6bc42c6c219838b073f0b0d9a56d24e04c53`.
