# C6-B20-W21 post-hoc tau1–tau2 exploration

**Status:** authorized post-hoc, producer-checked development exploration completed on
2026-11-02. It is not independently reconstructed and is not a prospective acceptance
test.

## Question

This calculation bypasses Slater–Koster parameterization and evaluates the two-tolerance
hypothesis directly in the fixed authenticated rank-10 Wannier basis. The candidate
family is the 18 native complete Wigner–Seitz shell truncations frozen by S90.
`H-shell-00` through `H-shell-16` are the proper reduced candidates. The exact
full-support `H-shell-17` source is retained as a zero-loss control but excluded from
reduced-family feasibility because including it would make every nonnegative threshold
pair trivially feasible.

For each proper reduced shell, the primary requirements are

- `tau_1`: uniform-408-point RMS ordered-spectrum error divided by `1 eV`; and
- `tau_2`: uniform-408-point RMS Hamiltonian Frobenius error per retained state divided
  by `1 eV`.

A threshold pair is feasible when at least one proper reduced shell has both requirements
no greater than the supplied thresholds. The witness is the feasible candidate with the
smallest exact included-representative count. Maximum-error maps are retained separately.
No fitted alignment is used: all matrices already act in the same Wannier basis.

## Result

The literal nested shell family does **not** exhibit a global conflict at its tightest
proper reduction. `H-shell-16` minimizes both primary losses among every proper reduced
candidate, although smaller shells retain local nonmonotonic tradeoffs that create
distinct minimum-support witness cells:

- `tau_1 = 0.00044635917135606217`;
- `tau_2 = 0.0015173254290054908`; and
- `371` of the `383` effective Wigner–Seitz representatives retained.

Therefore the post-hoc primary feasibility region is nonempty exactly above both of
those finite-family requirements. Below either requirement, no proper reduced shell is
feasible. The full-support control remains exactly `(0, 0)` but is not a reduction.

The minimum-support witness still changes with the threshold pair. Illustrative points
read directly from the complete map are:

| `(tau_1, tau_2)` | Minimum witness | Representatives |
|---|---:|---:|
| `(1.0, 1.0)` | `H-shell-02` | 19 |
| `(0.5, 0.5)` | `H-shell-03` | 43 |
| `(0.1, 0.15)` | `H-shell-07` | 135 |
| `(0.05, 0.1)` | `H-shell-09` | 177 |
| `(0.02, 0.04)` | `H-shell-11` | 225 |
| `(0.01, 0.02)` | `H-shell-13` | 313 |
| `(0.002, 0.006)` | `H-shell-14` | 353 |
| `(0.001, 0.002)` | `H-shell-16` | 371 |
| `(0.0004, 0.001)` | none | — |

These points are descriptive examples from the post-hoc map, not selected acceptance
thresholds.

## Retained files

- [`request.json`](request.json): authorization, source identities, loss definitions,
  and post-hoc status;
- [`run_analysis.py`](run_analysis.py): authenticated native-shell evaluation;
- [`result.json`](result.json): all 18 candidate requirements and exact finite-family
  feasibility rules;
- [`render_single_witness.py`](render_single_witness.py): exact-cell renderer for the
  headline single witness surface;
- [`render_plots_v3.py`](render_plots_v3.py): supplementary two-panel diagnostic-map
  renderer; and
- [`figures-v3/`](figures-v3/): the single witness surface, supplementary RMS and
  maximum-loss maps, and separate checksum manifests.

The earlier `figures/` and `figures-v2/` directories retain superseded layout attempts;
they are not technical-report inputs.

## Nonclaims

This exploration does not establish prospective threshold acceptance, DFT-parent or
experimental accuracy, a Slater–Koster model, refitted finite-range expressivity,
independent numerical verification, or a general incompatibility theorem. It tests only
literal complete-shell compression of one fixed represented Wannier Hamiltonian on the
revealed 408-point development inventory. The frozen 402-point geometry and all parent
values on it remain unconsumed.
