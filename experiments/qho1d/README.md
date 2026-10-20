# QHO1D development experiment

This mutable experiment composes the canonical one-dimensional quantum harmonic
oscillator implementation in
`ksdft2effmass.model_systems.qho1d`. The `QHO1D` name is deliberately
dimension-specific; no dimension-neutral `QHO` implementation or 2D/3D extension is
claimed.

## Files and output

- `input.json` declares the development sweep.
- `dev_analysis.py` calculates and independently verifies a candidate before writing
  the replaceable result.
- `dev_verification.py` independently verifies the existing development result.
- `dev_plots.py` verifies that result and writes replaceable report figures.
- `development-report.tex` records the protocol, formal crosswalk, results,
  diagnostics, limitations, and next error-bound steps.
- The fixed result and generated figures/PDF are written under
  `experiments/qho1d/analysis/development/`.

From `python/`:

```console
uv run python ../experiments/qho1d/dev_analysis.py
uv run python ../experiments/qho1d/dev_verification.py
uv run python ../experiments/qho1d/dev_plots.py
```

After generating the figures, compile the report from `experiments/qho1d/`:

```console
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=analysis/development development-report.tex
```

The output directory is ignored because these are replaceable development bytes, not a
retained evidence package. The historical files under
`calculations/research-monograph/harmonic-oscillator/` remain unchanged and retain
their original hashes and provenance.

## Present comparison and next decomposition

The current comparator reports

\[
J^{\mathsf T} H_{X,h} J - H_K,
\]

where `J` is the sampled-state Gram-orthonormalized injection, `H_{X,h}` is the finite
Dirichlet-grid matrix, and `H_K` is the directly constructed diagonal number-state
reference. The direct diagonal reference is intentional: reconstructing it from
already-truncated ladder products has a highest-state boundary defect.

The reported discrepancy currently combines several mechanisms and is not an error
bound. The next development tranche should retain separate channels for:

1. the algebraic isometry defect of `J`;
2. the finite-matrix residual `H_{X,h} J - J H_K`;
3. the two boundary-adjacent rows, where homogeneous Dirichlet closure replaces the
   nonzero real-line Hermite tail;
4. the interior centered-difference residual;
5. the Gram-orthonormalization correction relative to raw sampled states; and
6. binary64 reconstruction and verification tolerance.

For an exactly isometric `J`, the common-coordinate discrepancy obeys the elementary
residual relation

\[
J^{\mathsf T} H_{X,h} J - H_K
= J^{\mathsf T}(H_{X,h}J-JH_K).
\]

This supplies a computable a-posteriori norm bound once the residual norm is recorded.
It does not by itself prove continuum finite-box error, second-order convergence with an
explicit constant, or a physical uncertainty interval. Those require separate
assumptions and evidence.
