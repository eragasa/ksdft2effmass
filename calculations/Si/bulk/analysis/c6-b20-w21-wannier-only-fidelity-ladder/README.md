# C6-B20-W21 Wannier-only fidelity ladder

Status:
`wannier-only-fidelity-ladder-producer-checked-development-not-independently-verified`.

This authorized no-calculator study freezes three fitted native Wigner--Seitz shell
witnesses from the post-hoc refitting exploration and evaluates them without changing
support or parameters. The full authenticated rank-10 `C6-B20-W21` Wannier Hamiltonian
is the sole reference. No Slater--Koster model, DFT values, Quantum ESPRESSO execution,
or Wannier90 execution enters this ladder.

## Frozen witnesses

- `H-shell-05`: 79 representatives, moderate-fidelity anchor;
- `H-shell-10`: 201 representatives, intermediate anchor; and
- `H-shell-16`: 371 representatives, tight anchor.

The exact retained shell-scale vectors are bound in [`request-v2.json`](request-v2.json)
and are authenticated against the retained fitted-witness surface.

## Fidelity levels

1. **Exact integrated operator fidelity.** Parseval's identity over the unique effective
   integer representatives gives the normalized-Brillouin-zone RMS Frobenius error per
   state directly from coefficient differences.
2. **Dense interpolation fidelity.** Frozen models are evaluated on Gamma-origin
   \(12^3\), \(20^3\), and \(32^3\) tensor meshes.
3. **Source-relative feature fidelity.** Six axis valleys are located from a \(32^3\)
   sector search and local optimization. Indirect gaps, valley displacements, Hessians,
   and principal masses are compared with the full Wannier source using identical
   algorithms and a \(0.002\,\AA^{-1}\) curvature step.

## Result

The fitted 408-point errors understate broader interpolation error for every frozen
witness. The discrepancy decreases as support approaches the full model:

| witness | fitted-408 spectral RMS (eV) | \(32^3\) spectral RMS (eV) | ratio | fitted-408 operator RMS (eV) | exact Parseval operator RMS (eV) | ratio |
|---|---:|---:|---:|---:|---:|---:|
| H-shell-05 | 0.07242 | 0.18196 | 2.51 | 0.12814 | 0.26004 | 2.03 |
| H-shell-10 | 0.01320 | 0.02785 | 2.11 | 0.03229 | 0.05956 | 1.84 |
| H-shell-16 | 0.000404 | 0.000657 | 1.62 | 0.001394 | 0.001747 | 1.25 |

The dense spectral RMS values are stable across the tested meshes: changes from
\(12^3\) to \(32^3\) are approximately 0.58%, 1.38%, and 1.23% in magnitude for
H-shell-05, H-shell-10, and H-shell-16. Sampled operator RMS values agree with the exact
Parseval values to at most `5.56e-17 eV` on every tested mesh.

Source-relative feature changes are:

| witness | gap change (meV) | maximum valley displacement (\(\AA^{-1}\)) | maximum Hessian relative change | maximum principal-mass relative change |
|---|---:|---:|---:|---:|
| H-shell-05 | -65.77 | 0.09481 | 29.9% | 67.7% |
| H-shell-10 | -34.09 | 0.01612 | 10.6% | 53.2% |
| H-shell-16 | -0.503 | 0.002758 | 0.259% | 2.54% |

Thus moderate and intermediate support can look substantially better on the fitted
408-point inventory than on an independent dense Wannier interpolation test. Curvature
is especially demanding: H-shell-10 has a dense all-band spectral RMS below `0.028 eV`
but changes at least one source-relative principal mass by approximately 53%. The
near-full H-shell-16 witness remains close to the source across all tested channels.

These observations establish source-relative interpolation behavior only. The full
source itself fails declared DFT-parent gap and effective-mass fidelity targets, so
preserving it does not establish silicon accuracy.

## Retained artifacts

- [`request-v2.json`](request-v2.json): final frozen controls and global-axis valley
  route;
- [`run_analysis_v2.py`](run_analysis_v2.py): final authenticated producer;
- [`result-v2.json`](result-v2.json): exact operator, dense-mesh, valley, gap, Hessian,
  and mass results;
- [`render_results.py`](render_results.py): final renderer;
- [`figures/`](figures/): fidelity-ladder and source-relative feature figures with a
  checksum manifest; and
- [`executions/`](executions/): retained no-overwrite execution records.

The initial [`request.json`](request.json), [`run_analysis.py`](run_analysis.py), and
[`result.json`](result.json) are retained as a preliminary source-centered valley-search
attempt. Its H-shell-05 y-valley search reached the declared local bound. The final v2
route uses eight lowest \(32^3\) starts in each Cartesian-axis sector; all retained v2
valley optimizations succeeded without an active local bound, and the recomputed full
source valley energies agree with the prior characterization within
`1.51e-14 eV`.
