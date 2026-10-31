# Conduction-frozen localization preflight

This directory retains the exact preflight for the operator-selected
conduction-frozen rank-10 candidate. No process has been started.

The authenticated EIG table mechanically confirms that `[6.00, 19.02] eV` contains
exactly eight bands at each of the 64 k points, while exactly four bands lie below the
window. Thus all eight conduction bands are required in the rank-10 subspace and the
remaining two dimensions are selected from the four valence bands.

The outer 12-band window, interface artifacts, structure, grid, projections, strict
convergence criteria, conditioning, damping, and iteration budgets are unchanged. The
frozen window is the only new scientific variable. The occurrence is fresh and does
not consume either blocked checkpoint.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Eligibility still requires both native convergence messages and all existing
shape, ordering, isometry, and Hermiticity checks.

Status: **authorization consumed by one occurrence; no retry authorized**.

The occurrence returned zero and converged disentanglement at iteration 531, but it
exhausted 500 Wannierisation iterations without that stage's convergence message. The
blocked evidence is retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-blocked/).

Campaign-preflight SHA-256:
`788bb4c82cc4fd510a0e4cf4a7902e4627c36b547a2d6da0aa98ac052f06e1c1`.

Consumed authorization wording:

> Authorize exactly one conduction-frozen Wannier90 localization invocation described
> in `campaign-preflight.json`, with zero retries and stop on failure.

This does not authorize a retry or acceptance of a valence-complete operator.
