# Literature-informed conduction-frozen long-CG preflight

This directory retains the exact preflight for the authorized recommendation. No
calculator process has started because invocation authorization remains a separate
bounded action.

Starting from the unguided conduction-frozen 1000-iteration native-line-search input,
the only native change is:

```text
num_cg_steps = 200
```

The authenticated Wannier90 3.1.0 source and predecessor WOUT verify that the previous
omitted value used the native default 5. The commit-pinned AiiDA Wannier90 workflow
protocol observation records that its current moderate and precise protocols use 200.
This is a literature-informed diagnostic, not a universal literature standard.

The candidate retains the existing strict convergence tolerances and 1000-iteration
budgets rather than also adopting the AiiDA protocol's per-atom tolerances and larger
budgets. It retains the native parabolic line search, default dimensionless
`trial_step = 2.0`, current preconditioner, physical settings, target-space windows,
projections, and authenticated interface bytes.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory.

Status: **authorization consumed by one occurrence; no retry authorized**.

The occurrence reproduced disentanglement convergence at iteration 531 but exhausted
1000 Wannierisation iterations without that stage's convergence message. The longer CG
cadence reduced the final spread relative to the default-CG comparator, but its best
three-iteration spread-change window remained above both the campaign gate and the
literature-associated moderate two-atom threshold. Blocked evidence is retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-blocked/).

Campaign-preflight SHA-256:
`af7f9991f6834143665a7475366288af6b532e2bdd844660e7577c82ccac4e6d`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation with
> `num_cg_steps = 200` described in `campaign-preflight.json`, with zero retries and
> stop on failure.

This does not authorize a retry or scientific acceptance of the resulting operator.
