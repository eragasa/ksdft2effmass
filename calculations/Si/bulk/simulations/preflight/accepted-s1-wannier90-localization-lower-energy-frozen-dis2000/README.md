# Lower-energy frozen-window disentanglement-extension preflight

This directory retains the exact one-variable successor to the blocked lower-energy
frozen-window occurrence. The operator authorized the recommendation to prepare this
successor. No calculator process has started because execution remains a separate action
tied to this resulting preflight.

The only native input change is:

```text
dis_num_iter = 2000
```

All target-space, projection, rank, mesh, interface, optimizer, and convergence settings
remain unchanged. In particular, the candidate retains dimensionless
`dis_conv_tol = 1.0e-10`, the `[-5.85, 8.00] eV` frozen window, and the accepted
Wannierisation policy `2.0e-9 angstrom^2`, window 6. It starts fresh and consumes no
blocked checkpoint.

The predecessor's final 200 absolute disentanglement deltas decreased monotonically,
ending at `2.091e-9`. Late log-linear fits cross the threshold near iterations
1274--1285; these are extrapolations rather than calculated results. The 2000-step bound
provides margin while remaining below the AiiDA moderate workflow's 4000-step budget.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory. Failure ends this rank-10
window/projection candidate.

Status: **authorization consumed by one provider-eligible occurrence; no retry authorized**.

Disentanglement converged at iteration 1290 and Wannierisation converged at iteration
189. Provider-eligible evidence is retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-dis2000-eligible/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-dis2000-eligible/).
Scientific acceptance tests remain pending.

Campaign-preflight SHA-256:
`41360d7a6759568baafdec8c3a63c94b263c250a48fa62ca876227f87159bd6c`.

Consumed authorization wording:

> Authorize exactly one lower-energy frozen-window Wannier90 localization invocation
> with `dis_num_iter = 2000` described in `campaign-preflight.json`, with zero retries
> and stop on failure.

This does not authorize a retry or scientific acceptance of the resulting operator.
