# Conduction-frozen CG-reset decision

## Purpose

The tested parabolic-line-search, guiding-centres, reduced-trial-step, and fixed-step
variants all failed Wannierisation. The remaining narrowly scoped optimizer control is
the Fletcher--Reeves conjugate-gradient reset cadence exposed by Wannier90 3.1.0 as
`num_cg_steps`.

## One-variable revision

Starting from the unguided 1000-iteration native-line-search input, the successor
candidate adds only:

```text
num_cg_steps = 1
```

Wannier90 source defaults this integer control to 5 and the predecessor WOUT reports
that effective value. The source resets the conjugate-gradient coefficient to steepest
descent when the configured count is reached. Setting 1 therefore resets the conjugate
direction more frequently while retaining the native parabolic line search and default
dimensionless `trial_step = 2.0`.

The 3.1.0 user guide does not provide a dedicated explanatory subsection for
`num_cg_steps`; this is a bounded source-informed diagnostic, not a documented
recommended value. The more aggressive `num_cg_steps = 0` always-steepest-descent case
is not selected.

The candidate retains every physical setting, window, projection, interface artifact,
preconditioner setting, iteration budget, mixing ratio, and convergence threshold. It
keeps `guiding_centres`, `trial_step`, and `fixed_step` omitted. The occurrence starts
fresh and does not consume a blocked checkpoint.

## Acceptance boundary

Eligibility still requires both native convergence messages and all existing shape,
ordering, isometry, and Hermiticity checks. Successful internal convergence would not
by itself establish interpolation or effective-mass accuracy.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.
