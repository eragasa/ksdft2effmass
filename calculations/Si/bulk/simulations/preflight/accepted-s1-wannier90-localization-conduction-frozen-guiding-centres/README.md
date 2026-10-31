# Conduction-frozen guiding-centres preflight

This directory retains the exact one-variable preflight authorized after the blocked
1000-iteration result and its execution-free sensitivity analysis. No successor process
has been started.

The only changed native setting is:

```text
guiding_centres = .true.
```

Wannier90 3.1.0 documents this control as a way to avoid local minima and inconsistent
logarithm branch choices during spread minimization and recommends it when explicit
projections are available. The outer/frozen windows, rank, projections, interface
bytes, preconditioning, iteration budgets, mixing, and convergence thresholds are
unchanged. No `trial_step`, `fixed_step`, or convergence-noise control is added.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory.

Status: **authorization consumed by one occurrence; no retry authorized**.

The occurrence reproduced disentanglement convergence at iteration 531 but exhausted
1000 Wannierisation iterations without that stage's convergence message. Its final
spread was higher than the unguided comparator. Blocked evidence is retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-guiding-centres-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-guiding-centres-blocked/).

Campaign-preflight SHA-256:
`5e855723303cf3ddbe4eac6fdeb3a759381c812515d06b9549bb4dc366a1622a`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation with
> `guiding_centres = .true.` described in `campaign-preflight.json`, with zero retries
> and stop on failure.

This does not authorize a retry or acceptance of the resulting operator.
