# Conduction-frozen CG-reset preflight

This directory retains the exact preflight for the remaining narrowly scoped optimizer
control. No process has started.

Starting from the unguided 1000-iteration native-line-search input, the only native
change is:

```text
num_cg_steps = 1
```

The authenticated source and predecessor WOUT verify that the prior omitted value used
the Wannier90 3.1.0 default `5`. The new value resets the Fletcher--Reeves conjugate
direction more frequently while retaining the native parabolic line search and default
dimensionless `trial_step = 2.0`. The always-steepest-descent value `0` is not selected.

The user guide has no dedicated explanatory subsection for this source-exposed control,
so `1` is a bounded diagnostic coordinate rather than a documented recommended value.
All physical settings, windows, projections, interface bytes, preconditioning, iteration
budgets, mixing, and convergence thresholds are unchanged.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory.

Status: **authorization consumed by one occurrence; no retry authorized**.

The occurrence reproduced disentanglement convergence at iteration 531 but exhausted
1000 Wannierisation iterations without that stage's convergence message. Its final
spread substantially exceeded the native-default-CG comparator. Blocked evidence is
retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg-reset1-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg-reset1-blocked/).

Campaign-preflight SHA-256:
`fccd4dc8e3dedc9ec0f45badd513e3056d8c6b670b2a1d239fe33fc0f83ba137`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation with
> `num_cg_steps = 1` described in `campaign-preflight.json`, with zero retries and stop
> on failure.

This does not authorize a retry or acceptance of the resulting operator.
