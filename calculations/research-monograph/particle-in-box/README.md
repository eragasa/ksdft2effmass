# Particle-in-a-box residual experiment

## Status

This directory contains a **calculated illustrative numerical experiment** for
Appendix D of the research monograph. It is not a software harness, public API,
semiconductor calculation, scientific validation result, or uncertainty
quantification study.

`appendix-d-draft-report.md` is the experiment-level prose report and
provisional Appendix D draft. `protocol.md` maps the manuscript's mathematical
questions to retained evidence. The maintained LaTeX appendix remains the
manuscript source of record.

The standalone LaTeX source `appendix-d-draft.tex` renders the report with the
retained graphics. Its generated PDF is local and ignored:

```bash
cd calculations/research-monograph/particle-in-box
mkdir -p build
latexmk -lualatex -interaction=nonstopmode -halt-on-error \
  -output-directory=build appendix-d-draft.tex
```

The compiled file is `build/appendix-d-draft.pdf`.

The experiment uses the dimensionless convention $L=m=\hbar=1$. The residual
example uses eight interior Dirichlet-grid coordinates and retains the three
lowest discrete eigenvectors. A grid-refinement extension uses
$N=8,16,32,64,128,256$ interior points and follows the first six fixed continuum
mode indices.

## Question

The experiment checks that three superficially similar matrix differences have
different meanings:

1. consistently compressed Dirichlet Hamiltonian minus consistently compressed
   Dirichlet kinetic operator;
2. compressed Hamiltonian minus the uncompressed kinetic matrix; and
3. Dirichlet matrix minus a declared cyclic closure acting on the same finite
   coordinate space.

The first should vanish. The second should equal the negative discarded kinetic
sector. The third records a boundary-closure difference and is not interpreted
as a representation-independent continuum potential.

The convergence series separately asks whether fixed-index discrete energies
approach the continuum Dirichlet spectrum at the second order expected from the
centered finite-difference stencil. Raw residual norms are not compared across
grids because those matrices act on different finite state spaces.

## Reproduction

From `python/` using the resolved project environment:

```bash
uv run python ../calculations/research-monograph/particle-in-box/run_experiment.py \
  --input ../calculations/research-monograph/particle-in-box/input.json \
  --output ../calculations/research-monograph/particle-in-box/result.json

uv run python ../calculations/research-monograph/particle-in-box/verify_result.py \
  ../calculations/research-monograph/particle-in-box/result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/particle-in-box/plot_results.py \
  ../calculations/research-monograph/particle-in-box/result.json \
  --summary-output \
  ../calculations/research-monograph/particle-in-box/spectrum-and-states.png \
  --residual-output \
  ../calculations/research-monograph/particle-in-box/residual-matrices.png

uv run python \
  ../calculations/research-monograph/particle-in-box/run_convergence.py \
  --input \
  ../calculations/research-monograph/particle-in-box/convergence-input.json \
  --output \
  ../calculations/research-monograph/particle-in-box/convergence-result.json

uv run python \
  ../calculations/research-monograph/particle-in-box/verify_convergence.py \
  ../calculations/research-monograph/particle-in-box/convergence-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/particle-in-box/plot_convergence.py \
  ../calculations/research-monograph/particle-in-box/convergence-result.json \
  --convergence-output \
  ../calculations/research-monograph/particle-in-box/convergence-series.png \
  --mode-sweep-output \
  ../calculations/research-monograph/particle-in-box/convergence-mode-sweep.png

uv run python \
  ../calculations/research-monograph/particle-in-box/run_eigenpair_sweep.py \
  --input \
  ../calculations/research-monograph/particle-in-box/eigenpair-sweep-input.json \
  --output \
  ../calculations/research-monograph/particle-in-box/eigenpair-sweep-result.json

uv run python \
  ../calculations/research-monograph/particle-in-box/verify_eigenpair_sweep.py \
  ../calculations/research-monograph/particle-in-box/eigenpair-sweep-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/particle-in-box/plot_eigenpair_sweep.py \
  ../calculations/research-monograph/particle-in-box/eigenpair-sweep-result.json \
  --spectrum-output \
  ../calculations/research-monograph/particle-in-box/higher-eigenpair-sweep.png \
  --fixed-mode-output \
  ../calculations/research-monograph/particle-in-box/higher-mode-convergence.png

uv run python \
  ../calculations/research-monograph/particle-in-box/run_norm_sweep.py \
  --input \
  ../calculations/research-monograph/particle-in-box/norm-sweep-input.json \
  --output \
  ../calculations/research-monograph/particle-in-box/norm-sweep-result.json

uv run python \
  ../calculations/research-monograph/particle-in-box/verify_norm_sweep.py \
  ../calculations/research-monograph/particle-in-box/norm-sweep-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/particle-in-box/plot_norm_sweep.py \
  ../calculations/research-monograph/particle-in-box/norm-sweep-result.json \
  --operator-output \
  ../calculations/research-monograph/particle-in-box/operator-residual-norms.png \
  --algebraic-output \
  ../calculations/research-monograph/particle-in-box/eigensolver-residual-norms.png

uv run python \
  ../calculations/research-monograph/particle-in-box/run_identifiability.py \
  --input \
  ../calculations/research-monograph/particle-in-box/identifiability-input.json \
  --retained-result \
  ../calculations/research-monograph/particle-in-box/result.json \
  --output \
  ../calculations/research-monograph/particle-in-box/identifiability-result.json

uv run python \
  ../calculations/research-monograph/particle-in-box/verify_identifiability.py \
  ../calculations/research-monograph/particle-in-box/identifiability-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/particle-in-box/plot_identifiability.py \
  ../calculations/research-monograph/particle-in-box/identifiability-result.json \
  --output \
  ../calculations/research-monograph/particle-in-box/identifiability-model-classes.png
```

The retained PNG graphics show the lowest discrete states, the finite-grid
and continuum spectra, and heat maps of the three residual constructions. They
are visualizations of the retained JSON results, not additional scientific
evidence.

For modes $n=1,2,3$, the final $N=256$ relative energy errors are respectively
$1.2452\times10^{-5}$, $4.9809\times10^{-5}$, and
$1.1207\times10^{-4}$. Their final observed refinement orders are 1.99998,
1.99991, and 1.99981. This supports the expected second-order behavior for these
fixed modes under this grid series.

The higher-index sweep diagonalizes the full
$N=8,16,32,64,128,256$ spectra. Fixed modes enter when they exist: $n=8$ from
$N=8$, $n=16$ from $N=16$, and $n=32$ from $N=32$. They converge toward order
two, but eigenvalues whose index
grows in proportion to $N$ retain substantial dispersion error. At fractional
mode index near one half, the relative error remains about 0.18 across the grid
series. Nodal eigenvector overlaps and scaled algebraic residuals remain at
binary64 roundoff; nodal agreement is not a continuum interpolation-error
estimate.

The norm sweep records raw and same-grid-normalized Frobenius, spectral, and
maximum-entry norms. Raw Frobenius norms grow rapidly with dimension and the
$h^{-2}$ kinetic scale. For unmatched compression, normalized Frobenius,
spectral, and maximum-entry ratios approach one because a fixed three-state
retention discards nearly the entire increasingly resolved operator. For the
boundary realization, the normalized Frobenius ratio decreases from 0.209 to
0.036, while the spectral ratio approaches 0.25 and the basis-dependent
maximum-entry ratio remains 0.5. Full-eigensystem algebraic residual ratios stay
below $10^{-15}$ and measure only discrete eigensolver accuracy.

The executable identifiability demonstration addresses Appendix D's central
purpose directly. The physical Dirichlet decomposition and an illustratively
shifted decomposition reconstruct the same retained Hamiltonian, although only
the former has the declared physical interpretation. Fitting the illustrative
shift leaves unexplained Frobenius norms of 1.997, 1.856, 0.566, and zero for
scalar, diagonal, tridiagonal, and unrestricted real-symmetric model classes.
The unrestricted zero is algebraically trivial; the restricted results expose
the prior dependence on the admissible model class.

`protocol.md` maps every Appendix D requirement to retained evidence. The
verifiers check the retained matrices and convergence records against
independently stated finite-difference eigenvalues, projector identities, the
discarded-sector identity, and the declared boundary-closure difference. They
do not rerun or validate a material model.

The maintained files are listed in `SHA256SUMS` using SHA-256.
The result also records input and script identities, Python and NumPy versions,
floating-point representation, and eigensolver name.

## Interpretation boundary

Agreement with closed-form finite-difference eigenvalues and exact projector or
residual identities is numerical verification of this finite illustrative
construction. The refinement series establishes observed second-order behavior
only for the declared fixed modes and grids. The full-spectrum sweep explicitly
shows the lack of uniform eigenvalue accuracy when the mode index scales with
grid dimension. The normalized multi-norm sweep compares residuals only with
the same-grid Hamiltonian; it does not align changing finite spaces or establish
operator convergence. The identifiability result demonstrates why the reduced
Hamiltonian alone does not select a unique decomposition; it does not assign
physical meaning to the illustrative alternative. These results do not validate
a material model or supply evidence about silicon, DFT, Wannier localization,
or impurity physics.
