# Conduction-frozen Wannierisation iteration-extension decision

## Purpose

The conduction-frozen occurrence converged disentanglement at iteration 531 but reached
its declared 500-iteration Wannierisation budget without the native convergence
message. The operator directed an increase in the iteration count.

## One-variable revision

The successor candidate changes only:

```text
num_iter = 500  ->  1000
```

It retains:

- the rank-10 construction from 12 parent bands;
- outer window `[-5.85, 19.02] eV`;
- conduction-frozen window `[6.00, 19.02] eV`;
- the exact NNKP/AMN/MMN/EIG bytes and trial projections;
- `precond = .true.`;
- absolute Wannierisation `conv_tol = 1.0e-10 angstrom^2`, window 3;
- `dis_num_iter = 1000`, `dis_mix_ratio = 0.2`; and
- dimensionless fractional `dis_conv_tol = 1.0e-10`, window 3.

The candidate starts from the same declared inputs rather than consuming the blocked
checkpoint. This preserves a single-attempt deterministic occurrence and makes the
larger Wannierisation budget the only changed variable.

## Acceptance boundary

A successful occurrence must still print both native convergence messages and satisfy
all existing shape, ordering, isometry, and Hermiticity checks. More iterations do not
weaken either convergence threshold or establish interpolation or effective-mass
accuracy.

This decision authorizes preflight preparation only. Calculator execution remains a
separate bounded action.
