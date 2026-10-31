# Lower-energy frozen-window disentanglement extension decision

## Evidence-based exception

The first lower-energy frozen-window occurrence solved Wannierisation at iteration 265
under the accepted prospective policy but exhausted `dis_num_iter = 1000`. Its final
dimensionless fractional disentanglement delta was `-2.091e-9` against `1.0e-10`.
Absolute deltas decreased monotonically throughout iterations 801--1000. Log-linear
fits over the final 50, 100, and 200 iterations cross the threshold near iterations
1285, 1283, and 1274, respectively.

Those crossings are extrapolations, not completed results. They nevertheless distinguish
this occurrence from the irregular all-conduction-frozen localization trajectories and
support one bounded iteration-budget test. The scientific owner authorized the
recommendation to prepare that successor.

## One-variable successor

Starting from the exact lower-energy frozen-window candidate, change only:

```text
dis_num_iter = 2000
```

Retain:

- rank 10, 12 parent bands, and the `sp3s*` projection inventory;
- outer window `[-5.85, 19.02] eV` and frozen window `[-5.85, 8.00] eV`;
- dimensionless `dis_conv_tol = 1.0e-10`, `dis_conv_window = 3`, and
  `dis_mix_ratio = 0.2`;
- `num_cg_steps = 200`, `num_iter = 4000`, and `precond = true`;
- `conv_tol = 2.0e-9 angstrom^2`, `conv_window = 6`;
- native parabolic line search and default `trial_step = 2.0`; and
- all physical, mesh, topology, interface, and provenance identities.

Start fresh and do not consume the blocked checkpoint. The 2000-step bound is sufficient
to test the observed trend while remaining below the AiiDA moderate workflow's
4000-step disentanglement budget. This comparison is precedent, not an automatic
scientific acceptance rule.

## Stop and acceptance rules

Both native convergence messages remain mandatory. If disentanglement exhausts 2000
iterations, this rank-10 window/projection candidate ends; no further iteration or
optimizer extension is supported. Native convergence makes the operator eligible only
for the declared construction- and withheld-mesh tests of spectra, valley identity and
location, edge energies, derivatives, curvature/effective masses, and locality/tail
sensitivity.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action tied to the resulting preflight.
