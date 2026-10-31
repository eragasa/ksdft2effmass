# Wannier90 localization convergence controls

## Purpose

This note centralizes the Wannier90 3.1.0 controls relevant to the current rank-10
silicon localization campaign. It separates disentanglement, Wannierisation,
optimizer-policy, scientific-target, and reporting controls so that changing one is not
mistaken for changing another.

The authoritative executable behavior is the retained Wannier90 3.1.0 source. The user
guide is supporting documentation. In particular, its `dis_conv_tol` prose attaches an
angstrom-squared unit even though the source evaluates a dimensionless ratio.

## Two separate convergence problems

### Disentanglement

Wannier90 accepts the subspace when every value in the most recent
`dis_conv_window` iterations satisfies

```text
abs(Omega_I(i - 1) / Omega_I(i) - 1) < dis_conv_tol
```

The current window is 3 and the threshold is dimensionless `1.0e-10`.

| Control | Native default | Meaning | Current campaign status |
| --- | ---: | --- | --- |
| `dis_num_iter` | 200 | Maximum disentanglement iterations | 1000 in revised candidates |
| `dis_conv_tol` | `1.0e-10` | Dimensionless fractional change in `Omega_I` | Retained unchanged |
| `dis_conv_window` | 3 | Required consecutive passing fractional changes | Retained unchanged |
| `dis_mix_ratio` | `0.5` | Subspace-update mixing ratio | Damped to `0.2` |
| outer/frozen windows | construction-specific | Define eligible and mandatory parent states | Scientific target, not merely an optimizer knob |

The conduction-frozen candidates converged this stage at iteration 531 with final
fractional delta `9.017e-11`. Further changes to disentanglement controls do not address
the present Wannierisation failure.

### Wannierisation

Wannier90 accepts localization when every total-spread change in the most recent
`conv_window` iterations satisfies

```text
abs(Omega_total(i) - Omega_total(i - 1)) <= conv_tol
```

The historical occurrences used window 3 and `conv_tol = 1.0e-10 angstrom^2`. The
gradient norm, final spread, Hamiltonian Hermiticity, and native return code are not
substitutes for the applicable declared criterion.

| Control | Native default | Meaning | Current campaign status |
| --- | ---: | --- | --- |
| `num_iter` | 100 | Maximum spread-minimization iterations | Tested at 100, 500, 1000, and 4000 |
| `conv_tol` | `1.0e-10 angstrom^2` | Absolute successive total-spread-change threshold | Historical occurrences used the default value; prospective policy uses `2.0e-9 angstrom^2` for the exact two-atom cell |
| `conv_window` | -1 | Values greater than 1 enable consecutive-change convergence | Historical occurrences used 3; prospective policy uses 6 |
| `precond` | false | Damp high-frequency gradient contributions from large lattice vectors | Enabled in conditioned and later candidates |
| `num_cg_steps` | 5 | Number of Fletcher--Reeves CG updates before resetting toward steepest descent | Tested at 1 and 200 in addition to the default |
| `guiding_centres` | false | Control projection phases and logarithm branch choices; can avoid some local minima | Tested true; did not converge |
| `num_guide_cycles` | 1 | Frequency of guiding-centre use | Native default in guided test |
| `num_no_guide_iter` | 0 | Delay before guiding centres begin | Native default in guided test |
| `trial_step` | `2.0` | Dimensionless trial length for the parabolic line search | Default verified; explicit `1.0` also tested |
| `fixed_step` | none | Dimensionless fixed update replacing parabolic line search | Explicit `1.0` tested |
| `conv_noise_amp` | -1 (disabled) | After initial convergence, perturb the search direction and reconverge | Not applicable before first convergence |
| `conv_noise_num` | 3 | Maximum convergence-noise repetitions | Inactive while noise is disabled |

`trial_step` and `fixed_step` are mutually exclusive. They are algorithmic step lengths,
not energies, distances, or atomic displacements.

## Accepted prospective policy

The scientific owner accepted the recommendation in
[`localization-convergence-policy-decision.md`](localization-convergence-policy-decision.md).
For a new construction using the exact two-atom primitive cell, optimizer eligibility
uses `conv_tol = 2.0e-9 angstrom^2` and `conv_window = 6`. This is the
AiiDA-precise-associated per-atom coordinate scaled to two atoms. It is necessary but
not sufficient for scientific acceptance and does not alter any historical occurrence.
The decision does not adopt a 40000-iteration budget or other AiiDA protocol settings.

## Controls that do not repair this failure

- `conv_noise_amp` acts only after convergence has first been reached.
- `num_print_cycles`, `num_dump_cycles`, and `iprint` change output/restart frequency or
  verbosity, not the mathematical stopping condition.
- `optimisation` selects memory/speed implementations and is not a scientific
  convergence coordinate.
- More `num_iter` alone is unsupported by the observed excursions and the 500/1000
  interpolation sensitivity.
- Loosening `conv_tol` does not make an irregular, observably sensitive trajectory
  stationary.
- Changing `dis_mix_ratio` does not target the already-converged Wannierisation gauge.

## Scientific-target controls

The following change the represented state space or initialization and therefore create
a new scientific candidate rather than a mere optimizer variant:

- `num_wann`, `num_bands`, and excluded bands;
- outer and frozen energy windows;
- projection definitions and `select_projections`;
- reciprocal mesh and neighbor topology; and
- symmetry-adapted or Bloch-phase modes.

`use_bloch_phases` is unavailable for the present disentangled construction.
`site_symmetry` cannot be combined with the current frozen inner window.

## Tested optimizer branches

| Candidate | Disentanglement | Wannierisation | Final total spread (`angstrom^2`) | Disposition |
| --- | --- | --- | ---: | --- |
| Initial defaults, 100/200 iterations | Failed | Failed | diagnostic | Blocked |
| Conditioned/damped | Failed after 1000 | Converged at 86 | 21.731283428 | Blocked |
| Conduction-frozen, 500 iterations | Converged at 531 | Failed | 39.776686650 | Blocked |
| Conduction-frozen, 1000 iterations | Converged at 531 | Failed | 37.128984231 | Blocked |
| `guiding_centres = true` | Converged at 531 | Failed | 52.632067930 | Blocked |
| `trial_step = 1.0` | Converged at 531 | Failed | 43.536848529 | Blocked |
| `fixed_step = 1.0` | Converged at 531 | Failed | 50.615119724 | Blocked |
| `num_cg_steps = 1` | Converged at 531 | Failed | 57.056694066 | Blocked |
| `num_cg_steps = 200` | Converged at 531 | Failed | 36.563494226 | Blocked |
| `num_cg_steps = 200`, `num_iter = 4000` | Converged at 531 | Failed | 36.557416368 | Blocked |
| Lower-energy frozen window, prospective precise gate | Failed after 1000 | Converged at 265 | 19.532779948 | Blocked |
| Lower-energy frozen window, `dis_num_iter = 2000` | Converged at 1290 | Converged at 189 | 19.532839107 | Provider-eligible; scientific tests pending |

The lower spread of one failed occurrence does not make it accepted. The retained
500/1000 sensitivity analysis found source-mesh agreement but large between-mesh
spectral, edge, and curvature differences.

## Remaining decision space

The source-exposed CG reset diagnostic `num_cg_steps = 1` also failed and produced the
largest final spread among the tested conduction-frozen optimizer variants. A subsequent
literature review identified one protocol-grounded coordinate: the current AiiDA
high-throughput Wannier90 moderate and precise protocols use `num_cg_steps = 200`.
The one-variable occurrence lowered the final spread but still failed the strict gate;
its best three-iteration spread-change window also remained about 38 times above the
literature-associated moderate two-atom threshold.

Because the same AiiDA moderate protocol combines `num_cg_steps = 200` with
`num_iter = 4000`, one final exact iteration-budget occurrence changed only the latter.
It exhausted all 4000 iterations without the strict native convergence message. Five
three-iteration windows met the comparison moderate two-atom threshold, but none met the
comparison precise or campaign thresholds, and large excursions continued through
iteration 3934.

Iteration-only and optimizer-combination studies now stop under the prospective rule.
The explicit
[`localization-convergence-policy-review.md`](localization-convergence-policy-review.md)
finds that the historical exact threshold lacks a calculation-specific observable
justification, but that the moderate comparison would stop at a transient plateau and
cannot establish robustness. It recommends a prospective two-atom precise operational
coordinate, `conv_tol = 2.0e-9 angstrom^2` with `conv_window = 6`, separated from
observable-based scientific acceptance. The current construction does not meet that
precise gate and remains blocked.

The selected successor is the
[`lower-energy-frozen-window-decision.md`](lower-energy-frozen-window-decision.md)
construction. It retains rank 10 and the `sp3s*` projections but freezes all four valence
states at every source k point plus zero to two sampled low-energy conduction states,
leaving four to six dimensions for localization and higher-energy representation. It
uses the accepted prospective precise operational policy. Its first occurrence solved
Wannierisation at iteration 265 but exhausted the 1000-step disentanglement budget with
final fractional delta `-2.091e-9` against `1.0e-10`. The final 200 absolute deltas
decreased monotonically; fits to their late log trend would reach the threshold near
iteration 1274--1285, but that is extrapolation rather than completed convergence. The
first operator remained blocked. Its fresh successor changed only `dis_num_iter` from
1000 to 2000 and converged disentanglement at iteration 1290 and Wannierisation at
iteration 189. The outputs are provider-eligible, but scientific acceptance still
requires the declared interpolation, target-observable, and locality tests. A looser
retrospective comparison must not be relabeled as satisfaction of either historical or
prospective gates.
