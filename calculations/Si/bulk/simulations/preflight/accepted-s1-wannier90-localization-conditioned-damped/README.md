# Conditioned and damped localization revision preflight

This directory retains the recommended fresh convergence-control revision after the
first localization occurrence failed both optimization convergence gates. No revised
localization process has been started.

The exact interface bytes, structure, mesh, 12-band outer space, rank-10 projections,
energy window, absence of a frozen window, and `1.0e-10 angstrom^2` convergence
tolerances remain unchanged. The candidate changes only:

- `precond = .true.`;
- `num_iter = 500` rather than 100;
- `dis_mix_ratio = 0.2` rather than 0.5; and
- `dis_num_iter = 1000` rather than 200.

The occurrence is fresh and does not consume the blocked checkpoint. Preconditioning
addresses Wannier spread minimization; reduced mixing separately damps the observed
late-stage disentanglement reversal. The larger budgets test convergence without
weakening either tolerance.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Eligibility policy is unchanged.

Status: **authorization consumed; occurrence blocked without retry**.

Campaign-preflight SHA-256:
`0e88b28d743d0219b09c33212d35589cad12761778a5a6e048fb3dbc83e102f4`.

Exactly one invocation returned zero and native completion. Conditioning enabled
Wannierisation convergence at iteration 86, but disentanglement exhausted 1000
iterations with a final fractional delta of `3.815e-6` and explicit nonconvergence.
Provider disposition is `output-ineligible`. Evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conditioned-damped-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conditioned-damped-blocked/).

No retry or successor calculation is authorized.
