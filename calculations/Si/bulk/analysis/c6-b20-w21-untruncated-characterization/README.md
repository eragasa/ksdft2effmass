# `C6-B20-W21` full untruncated operator characterization

## Purpose

This separately authorized S30 no-calculator analysis characterizes the full
provider-eligible `C6-B20-W21` Wannier operator before the revealed-408 development
comparison. It applies no spatial truncation and performs no Slater--Koster reduction.
The frozen 402-point confirmation values remain unobserved.

## Bound inputs

The analysis authenticates exact bytes before parsing:

- accepted relaxed right-handed S1 structure;
- the 216-point, 20-band EIG table;
- provider-eligible rank-10 HR, `u`, and `u_dis` outputs; and
- the corresponding `_wsvec.dat` required by `use_ws_distance = .true.`.

The larger localization artifacts remain outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1/run`.
Maintained ProjectKoios parsers decode EIG, HR, `u`, and `u_dis`; the retained
calculation-local WS-vector parser reconstructs element-resolved shifts. PhysKit owns
direct and reciprocal lattice geometry. KSD's `TypedJsonMappingSerializer` produces the
result bytes.

## Initial controls and serialization-bound correction

The initial analysis reused the previously declared structural reconstruction tolerances:

- `2e-5 eV` maximum matrix-element discrepancy;
- `5e-5 eV` maximum per-point matrix Frobenius discrepancy;
- `2e-5 eV` maximum ordered-spectrum discrepancy; and
- `2e-5 eV` maximum matched frozen-state discrepancy.

The first result is retained unchanged as
`characterization-result-initial-fixed-gate.json`. Those fixed C4-era tolerances did not
account for this native HR file's six-decimal matrix serialization and are preserved as
diagnostics rather than weakened to the observed discrepancies.

The corrected structural gate is a worst-case bound derived from authenticated native
precision before rereading the result: six HR decimals, ten `u`/`u_dis` decimals,
twelve EIG decimals, exact HR degeneracy weights, rank and parent dimensions, and the
authenticated energy scale. It propagates componentwise half-unit rounding through the
finite transform and applies Weyl's bound to spectra. The derivation is recorded in the
result. This is a format-aware verifier correction, not an empirical tolerance fitted to
the observed errors.

The analysis also verifies pair closure and real-space Hermiticity within `1e-8 eV`.
Descriptive controls are:

- Gamma-origin `41 x 41 x 41` spectral and valley grid;
- `0.5 eV` conduction-edge reporting window;
- Cartesian Hessian steps `0.001`, `0.002`, `0.005`, and `0.010 inverse angstrom`; and
- Gamma-origin `21 x 21 x 21` locality grid with all represented physical-radius
  shells retained.

Only format-aware representation reconstruction, frozen-state reproduction, and
Hermiticity are structural pass/fail gates. The initial fixed checks remain visible.
Valleys, masses, dense spectra, and locality are candidate predictions for S40; they do
not establish parent agreement or scientific acceptance.

## Implementation status

`run_analysis.py` is a calculation-local object-oriented prototype derived from the
prior provider-eligible characterization surface. Reusable domain objects must migrate
to their maintained owner before merge. This stage invokes no Quantum ESPRESSO or
Wannier90 executable.

## Run

From the repository root:

```text
PYTHONPATH=python/src:/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1/src/python \
  python/.venv/bin/python \
  calculations/Si/bulk/analysis/c6-b20-w21-untruncated-characterization/run_analysis.py
```

The script writes `characterization-result.json` and stops if an identity or structural
reconstruction gate fails.

## Retained observations

S30 completed with no calculator invocation:

- 279 native HR representatives expand to 383 element-resolved WS representatives;
- all negative representatives are present and the pair-Hermiticity residual is
  `0.0 eV`;
- maximum source matrix-element discrepancy is `2.1558486139506847e-5 eV`;
- maximum source ordered-spectrum discrepancy is `2.893173461693266e-5 eV`;
- maximum frozen-state error across 954 matched states is
  `1.2852634512228178e-9 eV`;
- all six Delta-family optimizers succeeded and preserved their declared identities;
- predicted valley-energy spread is `1.12372349392853 meV`;
- maximum mass variation across the four stencils is `0.171819%`, with all principal
  curvatures positive; and
- the full finite representation is recovered to floating-point precision at the final
  `16.857151341 angstrom` shell.

At the last shell not exceeding two relaxed conventional lattice parameters
(`10.938364187 angstrom`), the descriptive maximum truncation sensitivities are
`354.119969 meV` over all bands and `208.641336 meV` for the lowest conduction band.
These are not spatial-truncation acceptance results; no truncation was applied.

The operator is **provider eligible, structurally reconstructed, fully characterized,
and scientifically unassessed by S30 alone**. It is eligible as the fixed source for a
controlled reduction. The later S40 revealed-408 comparison failed parent-fidelity gap
and effective-mass criteria, but those oracle labels limit physical claims rather than
controlled-reduction eligibility; see
[`../c6-b20-w21-revealed-408-development/`](../c6-b20-w21-revealed-408-development/).

| Artifact | SHA-256 |
|---|---|
| analysis implementation | `985dcc7e000fdd0aea76e046f8cfbf8cf12b73990decdc2808be517fd50a538e` |
| initial fixed-gate result | `f038459542ab2d7801ce83630274fd27db60275c6694b53fbcb904980a22ef89` |
| serialization-bound correction | `680cf0aeaa25c85915e8315ce06d1a821c9172333b43e5046dc8f75ba06a3ef9` |
| final characterization result | `37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18` |
