# PIAB1D residual and refinement calculation

## Status

This directory contains a **calculated illustrative numerical experiment** for
Appendix D of the research monograph. It is not a software harness, public API,
semiconductor calculation, scientific validation result, or uncertainty
quantification study.

`appendix-d-draft-report.md` is the experiment-level prose report and
provisional Appendix D draft. `protocol.md` maps the manuscript's mathematical
questions to retained evidence. `development_report/development_report.tex` is the
calculation-owned report focused on spectral reduction, with its report-local BibTeX
file at `development_report/references.bib`. The dated search protocol, screening
criteria, evidence matrix, and bounded novelty assessment are retained in
`development_report/prior_art_review.md`. The maintained LaTeX appendix remains the
manuscript source of record.

The standalone LaTeX source `appendix-d-draft.tex` renders the report with committed
graphics. Build it with LuaLaTeX:

```bash
cd calculations/piab1d
latexmk -lualatex -interaction=nonstopmode -halt-on-error appendix-d-draft.tex
```

The selected `appendix-d-draft.pdf` is retained as a review snapshot.

Compile the spectral-reduction report from `development_report/`:

```bash
cd calculations/piab1d/development_report
latexmk -pdf -interaction=nonstopmode -halt-on-error development_report.tex
```

The selected `development_report/development_report.pdf` is also retained as a review
snapshot. These PDFs and the maintained `technical_report/technical_report.pdf` are
not retained calculation evidence unless separately reviewed and admitted to a
checksum contract. LaTeX auxiliary products remain ignored.

## Successor directory structure

The package separates active authored material into:

- `run_01_calculation.py`, containing the visible Python calculation configuration;
- `run_02_verification.py`, independently reconstructing the declared finite problem;
- `run_03_render.py`, rendering only a verified result and recording exact input and
  output byte identities;
- `technical_report/`, containing the maintained report and local assets; and
- `executions/`, containing immutable successor execution directories.

The scripts execute sequentially at module scope. They have no `main()` function,
command-line parser, JSON-authored input, Workflow, or generic study container. JSON is
used only for result, execution, verification, and rendering records. Each stage refuses to
overwrite its owned artifacts.

The retained successor directory `executions/direct-core-n8-m3/` is an explicitly
unsealed development execution. It contains completed calculation, verification, and
rendering stages plus an explicit development-provenance record. It has no
evidence-package seal, source manifest, sealed provenance record, or execution-wide
checksum catalog. Its configuration declares $L=m=\hbar=1$, eight independent
interior degrees of freedom, and three retained states. Its renderer covers the closed
13-figure inventory: the spectrum/state summary, residual matrices, continuum and
discrete wavefunction ladders, retained-dimension selection, convergence series,
higher-eigenpair and higher-mode sweeps, operator and eigensolver residual norms,
finite algebraic diagnostics, and kinetic-potential decomposition under declared
model classes. Every plot consumes the authenticated successor projection. The
calculation stores analytical
sampling, convergence, and retained-selection values once; it does not persist a
second visualization-data copy. Verification derives and authenticates the rendering
projection from those authoritative sections, and rendering consumes that projection
from the verification record. The calculation obtains the
finite Hamiltonian and eigensystem from PhysKit, reduces it through KSD Hamiltonian
objects, and retains both Euclidean and homogeneous-Dirichlet quadrature normalization
checks. Diagnostic values, unit-compatible tolerances, and typed matrix-norm options
are normalized by the reusable typed-value codec. Generic mapping serializers and
deserializers connect final `to_json`/`from_json` boundaries to `to_dict`/`from_dict`.
The script authenticates paths and bytes, then delegates the decoded nested mapping to
`Piab1dVerifier`, which independently reconstructs the centered-difference matrix and
its discrete and continuum spectra with NumPy rather than calling the producer. The
base verifier composes Hamiltonian, eigensystem, spectral-reduction, quadrature,
convergence, selection, diagnostic, and visualization-projection verification values.
Every component inherits the final generic representation boundary; PIAB1D declares
only the ordered inventory and genuinely model-specific reference calculations.

From `python/`, the staged successor commands are:

```bash
uv run python ../calculations/piab1d/run_01_calculation.py
uv run python ../calculations/piab1d/run_02_verification.py
uv run --extra notebooks python ../calculations/piab1d/run_03_render.py
```

PhysKit owns the `Piab1D` model, analytical spectrum, homogeneous-Dirichlet
grid, finite-difference Hamiltonian, and eigensolution. Project Koios Numerics owns
the unit-free closed-interval trapezoidal rule, homogeneous-Dirichlet interior
restriction, and diagonal mass algebra. The core residual experiment composes those
pinned owners with reusable finite-operator analyses from
`ksdft2effmass.analysis.operators`; KSD owns retained-mode selection, residual
semantics, wire shapes, provenance, and independent verification. No local PIAB1D
model or solver compatibility facade is retained. Maintained scripts bind each model
when constructing `Piab1dTiseFdSolver` and consume the returned PhysKit `Eigensystem`
directly. The current source environment pins Project Koios Numerics through
Optimization revision `2a18e485109e307b2f7928bd0418bcf796aeb0d5` and PhysKit
revision `9c74ffa2fa0f40792117ccaa6c0bf0bcb0e70fe5`. PIAB1D matrix diagnostics
consume only `projectkoios.physkit.linalg.matrix.norm`.

The retained JSON results remain historical evidence and continue to record PhysKit
revision `2aaa4ba5ff4c51f5c5068ac895ef4ec5de293439`. Their calculation-local Workflow
producers have been removed from the maintained source surface. The retained result
bytes have not been rewritten, and their recorded historical source identities remain
the provenance locators for reproduction of those exact producers.

The version-two core input enables quadrature explicitly by default. The result keeps
Euclidean-normalized solver vectors separate from quadrature-normalized nodal
amplitudes and serializes the rule identity, spacing, weights, and diagonal mass
matrix. Constant interior weight leaves the spectral projector, reduced Hamiltonian,
and residual matrices invariant. The Hamiltonian is solved as a standard
real-symmetric eigenproblem, not a generalized eigenproblem.

The experiment uses PhysKit's nondimensional unit system, which supplies
$\hbar=1$, with $L=m=1$. The residual example uses eight interior
Dirichlet-grid coordinates and retains the three lowest discrete eigenvectors. The
grid studies evaluate every interior dimension from 8 through 256 and report declared
fixed or full-spectrum mode inventories.

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

## Historical verification and rendering

From `python/` using the resolved project environment:

```bash
uv run python ../calculations/piab1d/run_experiment.py \
  --input ../calculations/piab1d/input.json \
  --output ../calculations/piab1d/result.json

uv run python ../calculations/piab1d/verify_result.py \
  ../calculations/piab1d/result.json

uv run --extra notebooks python \
  ../calculations/piab1d/plot_results.py \
  ../calculations/piab1d/result.json \
  --summary-output \
  ../calculations/piab1d/spectrum-and-states.png \
  --residual-output \
  ../calculations/piab1d/residual-matrices.png

uv run python \
  ../calculations/piab1d/verify_convergence.py \
  ../calculations/piab1d/convergence-result.json

uv run --extra notebooks python \
  ../calculations/piab1d/plot_convergence.py \
  ../calculations/piab1d/convergence-result.json \
  --convergence-output \
  ../calculations/piab1d/convergence-series.png \
  --mode-sweep-output \
  ../calculations/piab1d/convergence-mode-sweep.png

uv run python \
  ../calculations/piab1d/verify_eigenpair_sweep.py \
  ../calculations/piab1d/eigenpair-sweep-result.json

uv run --extra notebooks python \
  ../calculations/piab1d/plot_eigenpair_sweep.py \
  ../calculations/piab1d/eigenpair-sweep-result.json \
  --spectrum-output \
  ../calculations/piab1d/higher-eigenpair-sweep.png \
  --fixed-mode-output \
  ../calculations/piab1d/higher-mode-convergence.png

uv run python \
  ../calculations/piab1d/verify_norm_sweep.py \
  ../calculations/piab1d/norm-sweep-result.json

uv run --extra notebooks python \
  ../calculations/piab1d/plot_norm_sweep.py \
  ../calculations/piab1d/norm-sweep-result.json \
  --operator-output \
  ../calculations/piab1d/operator-residual-norms.png \
  --algebraic-output \
  ../calculations/piab1d/eigensolver-residual-norms.png \
  --identity-output \
  ../calculations/piab1d/finite-identity-diagnostics.png

uv run python \
  ../calculations/piab1d/verify_identifiability.py \
  ../calculations/piab1d/identifiability-result.json

uv run --extra notebooks python \
  ../calculations/piab1d/plot_identifiability.py \
  ../calculations/piab1d/identifiability-result.json \
  --output \
  ../calculations/piab1d/identifiability-model-classes.png
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

The higher-index sweep diagonalizes every full spectrum for interior dimensions
$N=8,9,\ldots,256$. Fixed modes enter when they exist: $n=8$ from $N=8$,
$n=16$ from $N=16$, and $n=32$ from $N=32$. They converge toward order
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

The executable kinetic-potential decomposition demonstration addresses Appendix D's
central purpose directly. The physical Dirichlet decomposition and an illustratively
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

`SHA256SUMS` is retained as a historical catalog. It still names removed Workflow
entry points and therefore does not describe the maintained tip after this migration;
its exact entries remain resolvable at their recorded Git revision. The retained result
also records input and script identities, Python and NumPy versions, floating-point
representation, and eigensolver name.

## Interpretation boundary

Agreement with closed-form finite-difference eigenvalues and exact projector or
residual identities is numerical verification of this finite illustrative
construction. The refinement series establishes observed second-order behavior
only for the declared fixed modes and grids. The full-spectrum sweep explicitly
shows the lack of uniform eigenvalue accuracy when the mode index scales with
grid dimension. The normalized multi-norm sweep compares residuals only with
the same-grid Hamiltonian; it does not align changing finite spaces or establish
operator convergence. The decomposition result demonstrates why the reduced
Hamiltonian alone does not select a unique decomposition; it does not assign
physical meaning to the illustrative alternative. These results do not validate
a material model or supply evidence about silicon, DFT, Wannier localization,
or impurity physics.
