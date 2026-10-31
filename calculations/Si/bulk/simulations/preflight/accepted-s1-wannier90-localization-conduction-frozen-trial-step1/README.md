# Conduction-frozen trial-step preflight

This directory retains the exact preflight for the next documented optimizer control.
No successor process has been started.

Starting from the unguided 1000-iteration input, the only native change is:

```text
trial_step = 1.0
```

Wannier90 3.1.0 defaults this dimensionless parabolic line-search trial step to `2.0`
and explicitly recommends reducing it when spread minimization does not converge. It
scales an algorithmic search direction and has no energy or length unit. The failed
`guiding_centres` branch is not combined with this change. All windows, projections,
interface bytes, preconditioning, iteration budgets, mixing, and convergence thresholds
are unchanged. No `fixed_step` or convergence-noise control is added.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory.

Status: **authorization consumed by one occurrence; no retry authorized**.

The occurrence reproduced disentanglement convergence at iteration 531 but exhausted
1000 Wannierisation iterations without that stage's convergence message. Its final
spread was higher than the native-default-step comparator. Blocked evidence is retained
at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-trial-step1-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-trial-step1-blocked/).

Campaign-preflight SHA-256:
`1ce428cc8de7d1b7dfd377034280d0d35c4c827d5a3f9e9ff913f164456db3f5`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation with
> `trial_step = 1.0` described in `campaign-preflight.json`, with zero retries and stop
> on failure.

This does not authorize a retry or acceptance of the resulting operator.
