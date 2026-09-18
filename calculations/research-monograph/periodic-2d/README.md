# Two-dimensional periodic reduction exercise

## Status

The controlled exercise was human accepted and closed at
`RM-PERIODIC-2D-FINAL-ACCEPTANCE-HC05`. This directory contains a calculated
illustrative separable-to-coupled
extension of the accepted one-dimensional periodic exercise. It verifies exact
Kronecker structure, independently refined plane-wave and real-space parents,
degenerate projectors, reciprocal-loop and Chern diagnostics, two-dimensional
hopping shells, direct-versus-mediated reduction, effective-mass tensors, and a
frozen nonseparable-coupling sequence. A human-requested extension also verifies
a rank-three direct composite projected gauge against a controlled rough gauge,
including non-Abelian Wilson loops, finite-supercell spreads, and matrix-valued
hopping locality. Three separately represented Chern-band benchmarks--
Qi--Wu--Zhang, Hofstadter, and Haldane--supply genuine topological-obstruction
controls. The first authorized Wannier90 attempt stopped during preprocessing
and remains retained. A separately authorized balanced inactive-embedding
attempt then completed and converged, enabling an independently implemented
rank-three localization and hopping comparison. A later bounded non-DFT study
retains six one-axis mesh, cutoff, and inactive-embedding cases; their
nonmonotone outcomes explicitly prevent a convergence or embedding-independence
claim. Separate topological phase sweeps test the selected controls against
analytic boundaries and a numerical Hofstadter continuation.

The result is synthetic numerical verification. It is not a calculation for a
two-dimensional material or silicon, scientific validation, uncertainty
quantification, or production Wannier localization. The bounded Wannier90 run
is a synthetic comparison only.

## Retained files

- `input.json`: frozen scalar dimensionless controls and tolerances;
- `composite-input.json`: frozen rank-three projected-gauge controls;
- `protocol.md`: represented spaces, methods, acceptance criteria, and claim
  boundary;
- `run_experiment.py` and `run_composite.py`: scalar and composite primary
  implementations;
- `verify_result.py` and `verify_composite.py`: independent reconstructions that
  do not import the runners;
- `result.json` and `composite-result.json`: retained calculated results and
  provenance;
- `plot_result.py`, `plot_composite.py`, `summary.png`, and
  `composite-summary.png`: journal-facing diagnostic figures;
- `prepare_wannier90.py` and `wannier90-preflight.md`: deterministic interface
  preparation and original protected-execution boundary;
- `wannier90-execution.json`, `verify_wannier90_execution.py`, and
  `wannier90-failure-diagnosis.md`: retained preprocessing failure, independent
  identity/stage verification, and diagnosis;
- `wannier90-retry-preflight.md`: frozen balanced-embedding correction and
  protected-execution boundary;
- `composite-projected-gauge-correction.md`: deterministic correction of the
  provisional direct projected-gauge implementation;
- `extract_wannier90.py`, `wannier90-balanced-result.json`, and
  `verify_wannier90_balanced.py`: corrected execution extraction and independent
  numerical reconstruction;
- `plot_wannier90_balanced.py`, `wannier90-balanced-summary.png`, and
  `wannier90-balanced-report.md`: corrected comparison figure and mini-paper;
- `topological-model-decision.md`: the human-resolved model choice;
- `topological-input.json`, `run_topological.py`, `topological-result.json`, and
  `verify_topological.py`: three separate Chern-band contracts, calculations,
  and independent projector-route verification;
- `plot_topological.py`, `topological-summary.png`, and
  `topological-report.md`: topological figure and self-contained mini-paper;
- `topological-phase-sweep-input.json`, `run_topological_phase_sweep.py`,
  `verify_topological_phase_sweep.py`, `topological-phase-sweep-result.json`,
  `plot_topological_phase_sweep.py`, `topological-phase-sweep-summary.png`, and
  `topological-phase-sweep-report.md`: separate parameter sweeps and independent
  projector-Bargmann verification;
- `wannier90-study-input.json`, `wannier90-study-preflight.md`,
  `execute_wannier90_study.py`, `extract_wannier90_study.py`,
  `verify_wannier90_study.py`, `wannier90-study-result.json`, the portable
  `wannier90-study-results/` records, `plot_wannier90_study.py`,
  `wannier90-study-summary.png`, and `wannier90-study-report.md`: bounded
  non-DFT convergence and inactive-embedding evidence;
- `native-evidence-archive.json` and `verify_native_evidence_archive.py`: local
  archive identity and member-root verification; the archive is not published
  or transmitted;
- `report.md`: self-contained scalar and composite mini-paper; and
- `SHA256SUMS`: content identities for retained files.

## Reproduction

From `python/`:

```bash
uv run python \
  ../calculations/research-monograph/periodic-2d/run_experiment.py \
  --input ../calculations/research-monograph/periodic-2d/input.json \
  --output ../calculations/research-monograph/periodic-2d/result.json

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_result.py \
  ../calculations/research-monograph/periodic-2d/result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-2d/plot_result.py \
  ../calculations/research-monograph/periodic-2d/result.json \
  --output ../calculations/research-monograph/periodic-2d/summary.png

uv run python \
  ../calculations/research-monograph/periodic-2d/run_composite.py \
  --input ../calculations/research-monograph/periodic-2d/composite-input.json \
  --output ../calculations/research-monograph/periodic-2d/composite-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_composite.py \
  ../calculations/research-monograph/periodic-2d/composite-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-2d/plot_composite.py \
  ../calculations/research-monograph/periodic-2d/composite-result.json \
  --output ../calculations/research-monograph/periodic-2d/composite-summary.png

uv run python \
  ../calculations/research-monograph/periodic-2d/run_topological.py \
  --input ../calculations/research-monograph/periodic-2d/topological-input.json \
  --output ../calculations/research-monograph/periodic-2d/topological-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_topological.py \
  ../calculations/research-monograph/periodic-2d/topological-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-2d/plot_topological.py \
  ../calculations/research-monograph/periodic-2d/topological-result.json \
  --output ../calculations/research-monograph/periodic-2d/topological-summary.png

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_wannier90_execution.py \
  ../calculations/research-monograph/periodic-2d/wannier90-execution.json

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_wannier90_balanced.py \
  ../calculations/research-monograph/periodic-2d/wannier90-balanced-result.json \
  --portable

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-2d/plot_wannier90_balanced.py \
  ../calculations/research-monograph/periodic-2d/wannier90-balanced-result.json \
  --output ../calculations/research-monograph/periodic-2d/wannier90-balanced-summary.png

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_wannier90_study.py \
  ../calculations/research-monograph/periodic-2d/wannier90-study-result.json \
  --portable

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_topological_phase_sweep.py \
  ../calculations/research-monograph/periodic-2d/topological-phase-sweep-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_native_evidence_archive.py \
  ../calculations/research-monograph/periodic-2d/native-evidence-archive.json

(cd ../calculations/research-monograph/periodic-2d && shasum -a 256 -c SHA256SUMS)
```

The portable Wannier90 mode reconstructs the numerical comparisons from the
compact extracted fixture embedded in `wannier90-balanced-result.json`; it does
not claim to re-parse native formats or execution logs. When the retained
external run is available at its recorded path, omitting `--portable` adds
native-file identity, format, and log verification.

The runner and verifier each complete in a few seconds on the development
machine. The largest retained dense represented operator is the
$25^2\times25^2$ finite-difference matrix; dense matrices are recomputed and
are not serialized.

## Main calculated findings

- The exact separable represented Kronecker-sum defect is zero; the complete
  product-spectrum defect is $3.55\times10^{-14}E_G$.
- A controlled $45^\circ$ rotation reduces individual degenerate-state overlap
  to $1/\sqrt2$ while changing the rank-two projector by only
  $2.68\times10^{-16}$.
- Plane-wave low-band cutoff error falls from $5.25\times10^{-2}E_G$ at $P=1$
  to $6.27\times10^{-11}E_G$ at $P=4$. Independent finite differences show
  monotone second-order-like refinement but retain a
  $6.27\times10^{-3}E_G$ low-band error at $25^2$ points.
- Every coupling case remains isolated, with the minimum band gap decreasing
  from $0.4971E_G$ to $0.3251E_G$.
- Neighbor overlaps remain above `0.978`; all lattice Chern diagnostics are
  zero, Wilson phases are $\pi$ without transverse winding, and deterministic
  phase attacks change the loop diagnostics by at most
  $1.14\times10^{-15}$.
- The mixed-direction hopping norm grows from a numerical floor of
  $3.00\times10^{-15}E_G$ in the separable case to
  $1.94\times10^{-3}E_G$ at $\lambda_{xy}=0.30$.
- Direct and mediated shell coefficients agree within
  $3.37\times10^{-16}E_G$. Full-shell reconstruction is at binary64 scale on
  the transform mesh, while the finest withheld error remains
  $1.70\times10^{-6}E_G$ at the strongest coupling because reciprocal-mesh
  interpolation is a separate limit.
- The isotropic principal mass decreases from $1.534m$ to $1.313m$ over the
  coupling sequence. The anisotropic control yields principal masses
  $1.184m$ and $2.112m$ and a fourfold-symmetry defect of
  $7.46\times10^{-2}E_G$ while preserving time reversal and reflections.
- The rank-three composite remains isolated by at least
  $3.48\times10^{-2}E_G$; the minimum projection and neighbor singular values
  are 0.886 and 0.785.
- Smooth and rough internal gauges agree in spectra within
  $1.22\times10^{-15}E_G$, in Wilson eigenphase sets within
  $2.22\times10^{-15}$, and in zero total Chern number, but the rough gauge
  increases total finite-supercell spread from $24.90a^2$ to $67.70a^2$ and
  the radius-18 omitted hopping-block norm from $1.38\times10^{-2}E_G$ to
  $5.25\times10^{-1}E_G$.
- The topological QWZ, Hofstadter, and Haldane retained bands have Chern integer
  $-1$ and Wilson winding $+1$ on every mesh from $21^2$ through $81^2$;
  their declared trivial controls have zero Chern and zero winding.
- At $81^2$, the topological retained gaps are 2.000, 1.274, and 1.559 in their
  respective model energy units. Phase attacks alter Chern sums by at most
  $2.3\times10^{-16}$ and Wilson phases by at most $1.5\times10^{-15}$.
- The first authorized Wannier90 preprocessing attempt exited with code 1 after
  0.31 s because its unit inactive cell forced the neighbor search past the
  compiled 12-neighbor limit; it remains explicit failure evidence.
- The separately authorized balanced-embedding attempt preprocesses in 0.28 s
  and converges in 94 iterations and 0.47 s to native active-plane spread
  $0.7094a^2$. On the same finite-supercell estimator used for the direct
  gauge and the same external mesh, the optimized spread is $6.1359a^2$ versus
  $24.5163a^2$; the separate centered-mesh direct route gives $24.8951a^2$.
  Native and common-estimator values remain separate. The optimized frame spans
  the direct projected subspace within $2.65\times10^{-10}$ and reduces the
  radius-50 hopping tail from $5.90\times10^{-3}E_G$ to
  $2.72\times10^{-4}E_G$.
- Six additional Wannier90 cases all converge within their limits, but their
  spreads and tails are nonmonotone: common spreads range from $4.6847a^2$ to
  $10.3654a^2$, and the $N=19$, $P=2$, and $P=4$ tails are much larger than the
  reference. The $c=12$ embedding closely reproduces the reference totals,
  whereas $c=18$ reaches a different basin. No cutoff-, mesh-, or
  embedding-independent localization claim is supported.
- The phase sweeps recover QWZ changes at $m=-2,0,2$, bracket Haldane changes
  around $M=\pm0.7794$, and locate the sampled Hofstadter lower-band change
  between $\Delta=1.8$ and $2.0$. The declared $\Delta=4$ control remains in the
  sampled zero-Chern sector through $\Delta=12$.
