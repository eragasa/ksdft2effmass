# Finite harmonic-oscillator common-space comparison

## Status and scope

This directory contains a **calculated illustrative numerical experiment** for
Appendix E of the research monograph. It compares a finite Dirichlet-grid
oscillator with the exact retained ladder Hamiltonian only after both are
represented in the same ordered number-state coordinates.

The result provides numerical verification for the declared finite
construction. It is not a public software API, semiconductor calculation,
scientific validation result, or uncertainty-quantification study.

## Retained artifacts

- `input.json`: closed dimensionless sweep inputs;
- `protocol.md`: state spaces, map, controls, diagnostics, and acceptance rules;
- `run_experiment.py`: deterministic calculation and result serialization;
- `result.json`: calculated cases, exact map definitions and content identities,
  compact common-coordinate operators, diagnostics, cross-grid comparisons,
  and provenance;
- `verify_result.py`: independent analytic and algebraic verification;
- `plot_result.py`: deterministic visualization of retained values;
- `convergence-summary.png`: box, grid, discrepancy-component, and map studies;
- `operator-difference-heatmap.png`: selected common-coordinate difference;
- `report.md`: bounded interpretation of the calculated results; and
- `SHA256SUMS`: SHA-256 identities for the maintained artifacts.

## Reproduction

From `python/` using the resolved project environment:

```bash
uv run python \
  ../calculations/research-monograph/harmonic-oscillator/run_experiment.py \
  --input \
  ../calculations/research-monograph/harmonic-oscillator/input.json \
  --output \
  ../calculations/research-monograph/harmonic-oscillator/result.json

uv run python \
  ../calculations/research-monograph/harmonic-oscillator/verify_result.py \
  ../calculations/research-monograph/harmonic-oscillator/result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/harmonic-oscillator/plot_result.py \
  ../calculations/research-monograph/harmonic-oscillator/result.json \
  --summary-output \
  ../calculations/research-monograph/harmonic-oscillator/convergence-summary.png \
  --heatmap-output \
  ../calculations/research-monograph/harmonic-oscillator/operator-difference-heatmap.png
```

The calculation covers $b=4,6,8$, $\eta=0.2,0.1,0.05$, and $K=2,4,6$ in the
dimensionless convention $\hbar=m=\omega=\ell=1$. It constructs 27 finite
representations; the largest has 319 interior grid points and retains six
number states. Runtime is expected to be seconds on a laptop, and the outputs
are one JSON record and two PNG figures.

## Calculated summary

At fixed $b=8$, the relative Frobenius discrepancy exhibits approximately
second-order reduction under both grid refinements for every retained $K$. At
$\eta=0.05$, expanding the box from $b=4$ to 6 strongly improves the $K=4$ and
$K=6$ comparisons; the $b=6$ and $b=8$ values are then dominated by the fixed
grid spacing. The $K=2$ total discrepancy is slightly smaller at $b=4$ because
boundary and discretization contributions can cancel. It must not be read as
independent convergence of either contribution.

Exact calculated values and their bounded interpretation are in `report.md`.
The verifier reconstructs the comparison maps using analytic Hermite
polynomials, checks the pullbacks and discrepancy decomposition, and verifies
the recorded source identities.

## Interpretation boundary

Every subtraction is performed only after the finite-box operator is pulled
back through a retained injection $J:S_K\rightarrow\mathcal V_{X,h}$. Equal
matrix dimensions alone are never treated as alignment. The finite-box
boundary-domain effect, finite-difference error, map conditioning, and retained
space remain separately reported. No result is transferred to silicon, DFT,
Wannier localization, effective masses, or impurity physics.
