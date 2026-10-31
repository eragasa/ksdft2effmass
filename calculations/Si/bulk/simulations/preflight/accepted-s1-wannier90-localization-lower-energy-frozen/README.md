# Rank-10 lower-energy frozen-window preflight

This directory retains the exact preflight for the first scientific-construction
successor to the blocked all-conduction-frozen branch. No calculator process has started
because invocation authorization remains a separate bounded action.

## Construction revision

The rank, parent bands, outer window, mesh, projections, and interface bytes remain
unchanged. The frozen interval changes from `[6.00, 19.02] eV` to
`[-5.85, 8.00] eV` in the native QE energy reference.

The authenticated EIG inventory verifies that the new interval freezes all four valence
bands at every k point plus zero to two sampled conduction states. It contains 4--6
states per k point, strictly below rank 10. The maximum included and minimum excluded
energies are separated from the threshold by `0.482441965196 eV` on the source mesh.

## Prospective convergence policy

This new construction applies the accepted two-atom policy:

```text
conv_tol = 2.0e-9
conv_window = 6
```

It retains `num_cg_steps = 200`, `num_iter = 4000`, `precond = true`,
`dis_mix_ratio = 0.2`, dimensionless `dis_conv_tol = 1.0e-10`, and the native parabolic
line search. It starts fresh and consumes no blocked checkpoint.

Proposed command:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure. Both native convergence messages remain mandatory. Convergence establishes
only eligibility for the separately declared observable tests.

Status: **authorization consumed by one blocked occurrence; no retry authorized**.

Wannierisation converged at iteration 265 under the accepted prospective gate, but
disentanglement exhausted 1000 iterations with final fractional delta `-2.091e-9`
against `1.0e-10`. Blocked evidence is retained at
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-blocked/).

Campaign-preflight SHA-256:
`d29d05f12798314ec5b2bf3ccdc41e3e424cf79043e4b6ffea2ec24bac081828`.

Consumed authorization recommendation:

> Authorize exactly one rank-10 lower-energy frozen-window Wannier90 localization
> invocation described in `campaign-preflight.json`, with zero retries and stop on
> failure.

This does not authorize a retry or scientific acceptance of the resulting operator.
