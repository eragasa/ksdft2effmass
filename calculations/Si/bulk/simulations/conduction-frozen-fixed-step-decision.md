# Conduction-frozen fixed-step decision

## Purpose

The native-default parabolic line search, `guiding_centres = .true.`, and a halved
parabolic `trial_step = 1.0` all failed to converge Wannierisation for the
conduction-frozen target. The trial-step occurrence also produced a larger final spread
than the native-default comparator. The next documented optimizer control replaces the
parabolic line search with a fixed step.

## One-variable optimizer-policy revision

Starting from the unguided 1000-iteration input, the successor candidate adds:

```text
fixed_step = 1.0
```

and leaves `trial_step` omitted. Wannier90 3.1.0 documents `fixed_step` as a
line-search replacement that can be useful when line-search minimization fails to
converge; `fixed_step` and `trial_step` may not be specified together. The value is a
dimensionless algorithmic step length. `1.0` is a diagnostic coordinate on the same
step scale already tested for the parabolic trial, not a literature or acceptance
value prescribed by Wannier90.

The candidate retains:

- rank 10 from 12 parent bands;
- outer window `[-5.85, 19.02] eV`;
- conduction-frozen window `[6.00, 19.02] eV`;
- exact NNKP/AMN/MMN/EIG bytes and trial projections;
- `precond = .true.`;
- `guiding_centres = .false.` by omission;
- `num_iter = 1000`;
- absolute Wannierisation `conv_tol = 1.0e-10 angstrom^2`, window 3;
- `dis_num_iter = 1000`, `dis_mix_ratio = 0.2`; and
- dimensionless fractional `dis_conv_tol = 1.0e-10`, window 3.

The occurrence starts fresh and does not consume a blocked checkpoint.

## Acceptance boundary

Eligibility still requires both native convergence messages and all existing shape,
ordering, isometry, and Hermiticity checks. Successful internal convergence would not
by itself establish interpolation or effective-mass accuracy.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.
