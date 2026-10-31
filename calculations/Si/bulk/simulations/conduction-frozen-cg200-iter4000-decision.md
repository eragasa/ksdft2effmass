# Conduction-frozen long-CG 4000-iteration decision

## Purpose

The `num_cg_steps = 200` occurrence lowered the final spread relative to the native
CG-reset comparator but did not converge within 1000 iterations. Its trajectory
intermittently approached small spread changes and then underwent renewed excursions,
so convergence at a larger iteration count is possible but cannot be extrapolated.

The current AiiDA Wannier90 moderate protocol combines `num_cg_steps = 200` with
`num_iter = 4000`. This decision defines one bounded final iteration-budget diagnostic,
not an open-ended search.

## One-variable revision

Starting from the exact `num_cg_steps = 200` candidate, change only:

```text
num_iter = 4000
```

Retain the strict campaign convergence thresholds, three-iteration windows, physical
settings, target-space windows, projections, preconditioner, mixing, native parabolic
line search, default `trial_step = 2.0`, and authenticated interface bytes. Start fresh;
do not continue from or consume a blocked checkpoint.

The AiiDA protocol's looser per-atom tolerances and other workflow settings are not
adopted. The occurrence therefore tests iteration budget alone.

## Prospective stop rule

Both native convergence messages remain mandatory. A native zero return code, lower
spread, stable shapes, unitarity, isometry, or Hermiticity does not substitute for them.
If Wannierisation exhausts 4000 iterations or retains late excursions without its native
convergence message, iteration-only and optimizer-combination studies stop. The next
candidate must redesign the scientific target space or projections.

Even native convergence would only make the operator eligible for the already declared
interpolation, valley, curvature, effective-mass, and locality tests; it would not
establish scientific acceptance by itself.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.
