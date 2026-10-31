# Conduction-frozen Wannierisation iteration-extension preflight

This directory retains the exact preflight requested after the conduction-frozen
occurrence converged disentanglement but did not converge Wannierisation within 500
iterations. No successor process has been started.

The only changed native setting is:

```text
num_iter = 500  ->  1000
```

The conduction-frozen window, outer window, rank, projections, interface bytes,
preconditioning, damping, disentanglement controls, and strict convergence thresholds
are unchanged. The occurrence starts fresh and does not consume the blocked checkpoint.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory.

Status: **authorization consumed by one occurrence; no retry authorized**.

The successor reproduced disentanglement convergence at iteration 531 but exhausted
the enlarged 1000-iteration Wannierisation budget without that stage's convergence
message. Blocked evidence is retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-iter1000-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-iter1000-blocked/).

Campaign-preflight SHA-256:
`fc2354cb1afa4f64738e9ae82bec35907d3e8f59fc7f7c598f4628fc1b5c1b44`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation with
> `num_iter = 1000` described in `campaign-preflight.json`, with zero retries and stop
> on failure.

This does not authorize a retry or acceptance of the resulting operator.
