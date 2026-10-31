# C6-T1 full-parent-band outer-window decision

## Evidence requiring a target-space review

The original `C6` construction held the numerical outer window fixed at
`[-5.85, 19.02] eV`. Over the authenticated 216-point EIG inventory, that window selects
all 12 parent bands at 142 points, 11 at 62 points, and only the rank-minimum ten at 12
points. Eighty-six high-energy states across 74 points lie above the fixed outer maximum.
The authenticated C6 eigenvalue range is
`[-5.8341319732, 20.8036050385] eV`.

Thus the fixed numerical window inherited from `C4` does not define a mesh-stable parent
band inventory at `C6`. This does not prove that the varying inventory caused either
optimizer failure, but it is sufficient to end pure mesh-only attribution and to define
a separate target-space candidate.

## C6-T1 target space

Candidate `C6-T1` changes only the outer-window envelope:

```text
dis_win_min = -6.0 eV
dis_win_max = 21.0 eV
```

The resulting outer subspace is the span of all 12 authenticated parent states at every
C6 construction point. The proposed bounds provide `0.1658680268 eV` below the observed
minimum and `0.1963949615 eV` above the observed maximum. These are declared finite
construction-mesh margins, not a bound on unseen bands or a claim about the entire
Brillouin zone.

Retain exactly:

- accepted structure, parent, Gamma-origin `6 x 6 x 6` mesh, source ordering, and energy
  reference;
- 12 parent bands, rank 10, and non-spinorial character;
- frozen window `[-5.85, 8.00] eV`;
- projections `Si:sp3` and `Si:l=0:r=2`;
- dimensionless `dis_conv_tol = 1.0e-10`, `dis_conv_window = 3`, and
  `dis_mix_ratio = 0.2`;
- `dis_num_iter = 4000`, `num_iter = 4000`, `conv_tol = 2.0e-9 angstrom^2`, and
  `conv_window = 6`;
- `precond = true`, `num_cg_steps = 200`, native-default dimensionless
  `trial_step = 2.0`, unset `fixed_step`, and disabled guiding centres;
- HR and unitary-matrix output; and
- the authenticated NNKP, EIG, AMN, and MMN bytes.

The windows affect localization, not the retained NNKP topology or QE-generated
AMN/MMN/EIG interface. Those authenticated artifacts may therefore be reused without a
new QE, preprocessing, or conversion occurrence. Start fresh and consume no checkpoint
or failed localization output.

## Interpretation and stop rules

`C6-T1` is a target-space candidate, not a continuation of the one-variable `C4` to
`C6` mesh test. Any difference from the original candidates combines the changed outer
subspace with the already changed mesh and cannot be attributed to mesh density alone.

Both native convergence messages and all existing provider gates remain mandatory. If
`C6-T1` fails optimizer eligibility, stop automatic optimizer tuning. Return rank,
parent-band inventory, frozen window, and projection family to separate review rather
than changing them together.

If `C6-T1` becomes provider-eligible, evaluate it against the revealed 408-point
development evidence under the unchanged gap, valley-position, and per-mass criteria.
Do not inspect the 402-point confirmation parent values unless the operator and its
predictions have first been frozen under the prospective confirmation contract.
Wannier90 local optimization does not certify a global minimum.

This decision authorizes preflight preparation only. It does not authorize
`wannier90.x`, any retry, `C8`, `C12`, direct-parent confirmation, component-operator
construction, or Slater-Koster reduction.
