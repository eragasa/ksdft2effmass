# Conduction-frozen fixed-step preflight

This directory retains the exact preflight for replacing the failed parabolic line
search with Wannier90's documented fixed-step optimizer mode. No process has started.

Starting from the unguided 1000-iteration input, the line-search policy changes from
the native parabolic search with default dimensionless `trial_step = 2.0` to:

```text
fixed_step = 1.0
```

`trial_step` remains omitted because Wannier90 forbids specifying it together with
`fixed_step`. The value `1.0` is a diagnostic coordinate on the tested algorithmic step
scale, not a Wannier90-prescribed acceptance value. All physical settings, windows,
projections, interface bytes, preconditioning, iteration budgets, mixing, and
convergence thresholds are unchanged.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory.

Status: **authorization consumed by one occurrence; no retry authorized**.

The occurrence reproduced disentanglement convergence at iteration 531 but exhausted
1000 Wannierisation iterations without that stage's convergence message. Its final
spread exceeded the native parabolic-line-search comparator. Blocked evidence is
retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-fixed-step1-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-fixed-step1-blocked/).

Campaign-preflight SHA-256:
`f9bc4abec4f63772163b0a4020f82ff4b700e57f23e1e855d612760c9dce0b80`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation with
> dimensionless `fixed_step = 1.0` described in `campaign-preflight.json`, with zero
> retries and stop on failure.

This does not authorize a retry or acceptance of the resulting operator.
