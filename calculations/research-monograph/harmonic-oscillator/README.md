# Finite harmonic-oscillator common-space comparison

## Status and scope

This directory contains a **calculated illustrative numerical experiment** for
Appendix E of the research monograph. It uses three public mathematical software
models of one quantum harmonic oscillator: `HarmonicOscillatorAnalytical`,
`HarmonicOscillatorFiniteDifference`, and
`HarmonicOscillatorLadderOperators`. The finite-difference model composes a reusable
`DirichletInterval`, which owns `UniformCartesianGrid1D` and
`DirichletBoundaryCondition`, with
`SecondOrderCentralDifferenceLaplacian1D`, `SchrodingerKineticEnergy1D`,
`SampledPotential1D`, and `FiniteDifferenceHamiltonian1D` from the public
`ksdft2effmass.operators` package; the ladder model composes that package's
`LadderOperator1D`. Finite-difference and ladder operators use immutable canonical CSR
storage. It compares the finite Dirichlet-grid Hamiltonian with the exact retained
ladder Hamiltonian only after both are represented in the same ordered number-state
coordinates, with dense materialization restricted to that explicit historical
comparison boundary. Public in-memory values
carry typed units backed by Pint. This retained version-one study enters through an
explicit nondimensionalization boundary where `Unitless` is a real unit type; its
historical JSON remains numerical and byte-compatible.

The result provides numerical verification for the declared finite
construction. The retained calculation directory is not itself a public
software API, semiconductor calculation, scientific validation result, or
uncertainty-quantification study.

## Retained artifacts

- `input.json`: closed dimensionless sweep inputs;
- `protocol.md`: state spaces, map, controls, diagnostics, and acceptance rules;
- `run_experiment.py`: minimal typed CLI adapter for the deterministic calculation;
- `python/src/ksdft2effmass/analysis/model_systems/harmonic_oscillator/`:
  three public model DataObjects, the immutable comparison ResultObject, and the
  comparison ActionObject;
- `python/src/ksdft2effmass/campaigns/research_monograph/harmonic_oscillator.py`:
  exact study composition and retained-format ActionObjects;
- `result.json`: calculated cases, exact map definitions and content identities,
  compact common-coordinate operators, diagnostics, cross-grid comparisons,
  and provenance;
- `verify_result.py`: minimal typed CLI adapter for independent verification;
- `python/src/ksdft2effmass/campaigns/research_monograph/harmonic_oscillator/verification.py`:
  independent analytic and algebraic verification ActionObject;
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
the recorded source identities. The retained result remains bound to the exact
pre-refactor runner identity; newly authored records additionally bind the
current public analysis and campaign implementation identities. No retained
numerical result was rerun or relabeled by the package refactor.

## Interpretation boundary

Every subtraction is performed only after the finite-box operator is pulled
back through a retained injection $J:S_K\rightarrow\mathcal V_{X,h}$. Equal
matrix dimensions alone are never treated as alignment. The finite-box
boundary-domain effect, finite-difference error, map conditioning, and retained
space remain separately reported. No result is transferred to silicon, DFT,
Wannier localization, effective masses, or impurity physics.
