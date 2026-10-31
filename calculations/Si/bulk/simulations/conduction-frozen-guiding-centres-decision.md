# Conduction-frozen guiding-centres decision

## Purpose

The conduction-frozen 1000-iteration occurrence converged disentanglement but retained
large, intermittent Wannierisation spread excursions and did not satisfy its absolute
spread-change criterion. An execution-free comparison showed that the resulting 500-
and 1000-iteration finite interpolants differ substantially away from the source mesh.
The operator authorized the recommended optimizer-control study.

## One-variable revision

The successor candidate changes only:

```text
guiding_centres = .true.
```

Wannier90 3.1.0 documents this control as a means to avoid local minima and inconsistent
logarithm branch choices during spread minimization, recommends it where explicit
projections are present, and defaults it to false. The existing `Si:sp3` and
`Si:l=0:r=2` projection block supplies the required guide centers.

The candidate retains:

- the rank-10 construction from 12 parent bands;
- outer window `[-5.85, 19.02] eV`;
- conduction-frozen window `[6.00, 19.02] eV`;
- exact NNKP/AMN/MMN/EIG bytes and trial projections;
- `precond = .true.`;
- `num_iter = 1000`;
- absolute Wannierisation `conv_tol = 1.0e-10 angstrom^2`, window 3;
- `dis_num_iter = 1000`, `dis_mix_ratio = 0.2`; and
- dimensionless fractional `dis_conv_tol = 1.0e-10`, window 3.

No `trial_step`, `fixed_step`, or convergence-noise control is added. This isolates the
guiding-centres control. The occurrence starts fresh and does not consume a blocked
checkpoint.

## Acceptance boundary

Eligibility still requires both native convergence messages plus the existing shape,
ordering, isometry, and Hermiticity checks. A successful localization occurrence would
remain a candidate requiring interpolation, valley, curvature, and locality validation.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.
