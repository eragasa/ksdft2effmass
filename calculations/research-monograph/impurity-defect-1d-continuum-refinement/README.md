# Continuum refinement for the synthetic 1D defect

This directory retains a deterministic comparison of the accepted scalar lattice parent with its parabolic band-edge approximation under independently varied continuum mesh, continuum domain, lattice supercell, lattice scale, and Gaussian width.

## Evidence status

**Synthetic test data / software and numerical verification.** The package does not establish an asymptotic theorem, silicon or dopant behavior, material validity, transferability, scientific validation, or uncertainty quantification.

## Main result

- Continuum-mesh, continuum-domain, and lattice-supercell support axes pass.
- At fixed physical profile, the lattice-scale sequence passes every frozen criterion from $a=0.5a_{\mathrm{ref}}$ through $0.125a_{\mathrm{ref}}$.
- Neither fixed-integrated nor fixed-peak broadening defines a crossover at the original spacing. A $3.78\times10^{-3}E_G$ compressed parent-dispersion residual remains above the frozen $10^{-3}E_G$ rule.
- The retained conclusion is therefore a bounded lattice-scale pass but **no profile-defined continuum crossover over the tested width domain**.

This resolves the limitation of the earlier one-grid smoothness scan: profile broadening and represented lattice refinement are not treated as the same operation.

## Contents

- `input.json` — immutable sources, separated axes, profile families, and frozen tolerances.
- `run_experiment.py` — direct Fourier-coordinate continuum and scaled-lattice calculation.
- `result.json` — retained axis records, criteria, boundaries, digests, and limitations.
- `verify_result.py` — independent site-space lattice reconstruction and entrywise continuum reconstruction; it does not import the runner.
- `plot_result.py` and `summary.png` — deterministic diagnostics.
- `protocol.md` — represented operators, scaling definitions, metrics, literature relationship, and reproduction contract.
- `report.md` — compact methods-and-results mini-paper.
- `SHA256SUMS` — package content identities.

## Reproduce

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/summary.png
```

Then run `sha256sum -c SHA256SUMS` from this directory.
