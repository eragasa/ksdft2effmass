# Conduction-frozen long-CG decision

## Purpose

A literature and workflow-protocol review found that the current AiiDA Wannier90
high-throughput moderate and precise protocols explicitly use `num_cg_steps = 200`,
whereas Wannier90 3.1.0 defaults to 5. The earlier conclusion that the bounded optimizer
ladder was exhausted was therefore too strong.

The workflow protocol is associated with the automated high-throughput Wannierisation
literature, but `200` is not a universal literature standard. It is treated here as one
bounded literature-informed diagnostic coordinate.

## One-variable revision

Starting from the unguided conduction-frozen 1000-iteration native-line-search input,
the candidate adds only:

```text
num_cg_steps = 200
```

All physical settings, target-space windows, projections, interface bytes,
preconditioning, mixing, iteration budgets, convergence windows, and strict convergence
thresholds remain unchanged. `guiding_centres`, `trial_step`, and `fixed_step` remain
omitted, retaining native `trial_step = 2.0` and the parabolic line search.

The test therefore asks only whether allowing a longer Fletcher--Reeves conjugate
sequence before a scheduled steepest-descent reset materially changes the irregular
Wannierisation trajectory. Wannier90 may still reset an excessive conjugate-gradient
coefficient internally.

The AiiDA moderate protocol's looser per-atom tolerances and 4000-iteration budget are
not adopted. The best three-iteration window in the existing default-CG 1000-iteration
trajectory remained above even its two-atom moderate threshold, so a tolerance-only
change would not establish convergence.

## Acceptance boundary

Both existing native convergence messages remain mandatory. Structural validity,
unitarity, isometry, Hermiticity, a native zero return code, or a lower final spread do
not replace those messages. Any converged candidate would remain subject to the
prospective interpolation, valley, curvature, effective-mass, and locality tests.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.

## Sources

- Wannier90 3.1.0 source and user-guide defaults.
- Current `aiidateam/aiida-wannier90-workflows` base Wannier90 protocol.
- Vitale et al., *Automated high-throughput Wannierisation*, npj Computational
  Materials 6, 66 (2020), DOI `10.1038/s41524-020-0312-y`.
