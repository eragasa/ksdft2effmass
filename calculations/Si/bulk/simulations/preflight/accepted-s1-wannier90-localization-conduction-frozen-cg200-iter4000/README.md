# Conduction-frozen long-CG 4000-iteration preflight

This directory retains the exact final iteration-budget diagnostic preflight. No
calculator process has started because invocation authorization remains a separate
bounded action.

Starting from the blocked `num_cg_steps = 200` candidate, the only native input change
is:

```text
num_iter = 4000
```

The candidate starts fresh and does not consume the blocked checkpoint. It retains
`num_cg_steps = 200`, strict campaign tolerances, three-iteration windows, target-space
windows, projections, preconditioner, mixing, native parabolic line search, default
`trial_step = 2.0`, and authenticated interface bytes.

The commit-pinned AiiDA moderate protocol uses both `num_cg_steps = 200` and
`num_iter = 4000`. Its per-atom convergence tolerances and other settings are not
adopted. This is one bounded protocol-matched iteration diagnostic, not adoption of that
entire workflow or a universal recommended parameter set.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory. If Wannierisation exhausts
4000 iterations, iteration-only and optimizer-combination studies stop.

Status: **authorization consumed by one blocked occurrence; no retry authorized**.

The occurrence exhausted 4000 Wannierisation iterations. It retrospectively contained
five three-iteration windows below the comparison AiiDA moderate two-atom threshold,
but none below the comparison precise threshold and none below the declared campaign
threshold. Large late excursions continued through iteration 3934. Evidence is retained
at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-iter4000-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-iter4000-blocked/).

Campaign-preflight SHA-256:
`bda73a7c42d04e1f17e734a5a5bed9d04d446c6472c812f7f73c19db7d329ed2`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation with
> `num_cg_steps = 200` and `num_iter = 4000` described in `campaign-preflight.json`,
> with zero retries and stop on failure.

This does not authorize a retry or scientific acceptance of the resulting operator.
