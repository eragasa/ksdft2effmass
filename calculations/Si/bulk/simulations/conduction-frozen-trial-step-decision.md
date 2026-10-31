# Conduction-frozen trial-step decision

## Purpose

The one-variable `guiding_centres = .true.` occurrence did not converge and produced a
larger final spread than the unguided 1000-iteration comparator. The operator directed
continuation to the next documented Wannier90 optimizer control.

## One-variable revision

Starting from the unguided 1000-iteration input, the successor candidate adds only:

```text
trial_step = 1.0
```

Wannier90 3.1.0 uses a default trial step of `2.0` for the parabolic line search and
explicitly recommends decreasing it when spread minimization does not converge. The
input is a dimensionless algorithmic line-search step: it scales the conjugate-gradient
search direction and is not an energy, length, or physical displacement. This candidate
halves that trial step. `guiding_centres` remains false/default, so the failed
guiding-centres branch is not compounded with the line-search change.

The candidate retains:

- rank 10 from 12 parent bands;
- outer window `[-5.85, 19.02] eV`;
- conduction-frozen window `[6.00, 19.02] eV`;
- exact NNKP/AMN/MMN/EIG bytes and trial projections;
- `precond = .true.`;
- `num_iter = 1000`;
- absolute Wannierisation `conv_tol = 1.0e-10 angstrom^2`, window 3;
- `dis_num_iter = 1000`, `dis_mix_ratio = 0.2`; and
- dimensionless fractional `dis_conv_tol = 1.0e-10`, window 3.

No `fixed_step` or convergence-noise control is added. The occurrence starts fresh and
does not consume a blocked checkpoint.

## Acceptance boundary

Eligibility still requires both native convergence messages and every existing shape,
ordering, isometry, and Hermiticity check. Successful internal convergence would not by
itself establish interpolation or effective-mass accuracy.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.
