# Periodic-2D optimizer-basin and convergence follow-up

## Status

This directory contains a **calculated synthetic non-DFT numerical-verification
follow-up** to the human-accepted periodic-2D controlled exercise. The exact
local Wannier90 execution was separately authorized at
`RM-PERIODIC-2D-OPTIMIZER-BASIN-EXECUTION-HC07`. It does not reopen or alter the
accepted exercise.

Together with Appendix H, this evidence is completed controlled synthetic
numerical verification. The expanded optimizer-convergence execution is
complete, extracted, independently verified, plotted, and incorporated. It has
not been peer reviewed, submitted, released, or publicly deposited, and it does
not provide material validation.

All 72 declared localization processes completed within their execution limits.
Only 51 satisfied the frozen Wannier90 convergence criterion; 21 reached the
5000-iteration bound without satisfying it. Every endpoint is retained. The
study **does not support** the frozen mesh-and-cutoff convergence criteria or a
reproducibly occupied best basin.

This is not DFT, material validation, uncertainty quantification, proof of a
global optimum, or evidence for general Wannier convergence.

## Contents

- `study-input.json`: exact nine configurations, eight deterministic initial
  gauges, executable identity, convergence rules, and resource bounds;
- `preflight.md`: protected-execution preflight and claim boundary;
- `execute_study.py`: serial bounded execution driver;
- `execution-result.json`: compact execution and native-file manifest;
- `extract_study.py`: extraction, basin classification, and convergence
  assessment;
- `result.json`: compact retained numerical result;
- `verify_study.py`: independent summary, manifest, native-file, operator, and
  convergence verifier;
- `plot_study.py` and `summary.png`: retained execution-study figure;
- `reanalyze_study.py`, `reanalysis-result.json`, `plot_reanalysis.py`, and
  `reanalysis-summary.png`: offline spread-component, trace, symmetry, hopping,
  and common-estimator refinement evidence;
- `verify_reanalysis.py`: independent reconstruction of the offline reanalysis;
- `estimator-inputs/`: exact $256^2$, $512^2$, and $1024^2$ common-estimator
  inputs for four representative endpoints;
- `standalone-study-design.md`, `standalone-study-proposal.json`,
  `generate_standalone_starts.py`, and `standalone-initial-gauges.json`:
  frozen fixed-embedding, deterministic low-discrepancy multi-start,
  optimizer-control, and continuation-study design and inputs;
- `verify_standalone_proposal.py`: static verification of proposal counts,
  configuration axes, exact Halton coordinates, and start unitarity;
- `standalone-execution-preflight.md`: exact authorized execution boundary,
  immutable identities, restart contract, resource limits, and stop rules;
- `execute_standalone_study.py`: serial bounded executor for interface
  preparation, baseline and control localizations, and conditional continuation;
- `standalone-resume-preflight.md`: retained bounded-stop diagnosis and exact
  continuation-resume boundary;
- `resume_standalone_continuations.py`: progress-reporting resume executor for
  only the retained pending continuation set;
- `verify_standalone_execution.py`: independent identity, coverage, resource,
  continuation, and external-file verification;
- `extract_standalone_results.py` and `standalone-result.json`: all initial and
  effective endpoints, $1024^2$ represented diagnostics, density-aware basins,
  and frozen convergence assessment;
- `verify_standalone_results.py`: independent native, hopping, arithmetic, and
  sampled common-grid reconstruction;
- `plot_standalone_results.py` and `standalone-summary.png`: publication-facing
  convergence, spread, holdout, basin-sensitivity, and numerical-control figure;
- `analyze_standalone_convergence_regression.py`,
  `standalone-convergence-regression.json`,
  `verify_standalone_convergence_regression.py`,
  `plot_standalone_convergence_regression.py`, and
  `standalone-convergence-regression.png`: post-hoc right-censored
  convergence-iteration regression, independent arithmetic verification, and
  publication-facing figure;
- `standalone-report.md`: methods, results, limitations, and reproduction;
- `standalone-native-evidence-archive.json` and
  `verify_standalone_archive.py`: local standalone archive identity, inventory,
  link-boundary, and control-record verification;
- `protocol.md`: mathematical and numerical method;
- `report.md`: results, interpretation, and limitations;
- `native-evidence-archive.json` and
  `verify_native_evidence_archive.py`: local archive identity and member checks;
- `SHA256SUMS`: identities of every retained repository artifact.

## Principal result

The nine configurations contain four mesh points, four cutoff points, and three
inactive-embedding values with shared reference configurations. Eight initial
frames are used per configuration: the baseline frame and seven deterministic
smooth reciprocal-periodic $U(3)$ perturbations. These transformations preserve
the retained rank-three subspace but probe different optimizer trajectories.

The best converged native Wannier90 spread along the mesh sequence is

| $N$ | best converged spread ($a^2$) | converged starts |
|---:|---:|---:|
| 11 | 0.597822970 | 7/8 |
| 15 | 0.709283240 | 6/8 |
| 19 | 0.796140901 | 5/8 |
| 23 | 0.863253246 | 2/8 |

The $N=19\to23$ best-spread change is 7.77%, above the frozen 1% tolerance.
The corresponding unordered center-set distance is 0.187 cell and also fails
its 0.01-cell tolerance. The median converged-start diagnostics are less stable.

At $N=c=19$, the best converged spreads for $P=2,3,4,5$ are
0.807170149, 0.796161345, 0.796140901, and 0.796140404 $a^2$. Thus the
$P=4\to5$ best-spread and hopping-tail diagnostics stabilize, but the center-set
and repeated-basin requirements fail. Cutoff stability of selected scalar
metrics is not promoted to an overall convergence claim.

For $P=4,N=19$, the best converged native spreads at $c=15,19,23$ agree near
0.796141 $a^2$, but the number of converged starts is 8, 5, and 5. The inactive
embedding therefore remains an optimizer-trajectory sensitivity even where the
lowest observed spread is nearly unchanged.

Under the original spread-and-center classification, every converged start is a
separate observed basin and the best-basin occupancy is one. A subsequent
offline reanalysis separates the invariant spread $\Omega_I$ from the
gauge-dependent $\widetilde\Omega=\Omega_D+\Omega_{OD}$ and additionally
quotients all eight square-lattice $D_4$ operations. Only the $c=23$ embedding
case merges two non-best endpoints (`identity` and `rough_smooth`); the best
basin still has occupancy one everywhere.

The reanalysis shows that the $N=19\to23$ change is dominated by $\Omega_I$:
it changes by 8.57%, whereas the best converged $\widetilde\Omega$ changes by
0.103%. This refines the interpretation of the failed total-spread gate but does
not restore center-set, repeated-basin, or multi-start convergence. Of the 21
5000-step stops, 11 are still descending, nine are near stationary without
meeting the convergence window, and one is oscillatory or stalled under the
explicitly exploratory terminal-trace classifier.

For four representative endpoints, the independently reconstructed common
spread changes by at most $1.32\times10^{-6}$ relatively from $512^2$ to
$1024^2$, with center-set changes at numerical roundoff. Thus the retained
$512^2$ common estimator is adequate for those sampled cases. Radius-18 hopping
tails replace radius 50 for cross-mesh comparisons because radius 18 is
supported by every declared mesh.

The basin classification remains a conservative observed-endpoint diagnostic,
not proof that every class is a mathematically distinct local minimum.

## Standalone-study result

The expanded study completes 256 initial localizations and 120 exact-checkpoint
continuations. Initial native convergence is 136/256. Continuation rescues 60
of the 120 initial stops, leaving 196/256 final converged endpoints and 60
retained final nonconverged endpoints. The latter comprise 30 continuing-
descent, 25 near-stationary, four oscillatory-or-stalled, and one stalled-or-
nondescent trace under the exploratory classifier.

Final baseline convergence falls from 16/16 at $N=11$ to 9/16 at fixed
$c=31,N=27$ and 6/16 at $N=31$. For the fixed $N=27\to31$ pair, best
$\Omega_I$ changes by 4.66% and best $\widetilde\Omega$ by 1.62%; the holdout
residuals are 3.69% and 2.54%. The $P=5\to6$ cutoff pair passes its scalar,
center, tail, and convergence-fraction criteria, but every density-aware
$D_4$ basin remains a singleton. The required best-basin occupancy of four
therefore fails everywhere. In two matched $N=23$ controls, enabling the
preconditioner is associated with two and one additional native convergences,
without materially changing the best observed objective; no general advantage
is inferred.

The planned pre-execution basin-tolerance control lacks a retained record and is
preserved as a protocol deviation. Post-hoc exact-equivalence controls give
maximum center and density mismatches of $5.56\times10^{-17}$ cell and
$6.69\times10^{-16}$. Threshold sensitivity leaves best-endpoint direct
occupancy at one through density tolerance $10^{-4}$, although non-best direct
matches first appear at $2.5\times10^{-5}$.

A post-hoc right-censored log-normal regression adjusts configuration effects
for the 16 deterministic starts. Relative to fixed $c=31$, $P=4$, $N=23$,
the adjusted convergence-time ratios are 0.335 at fixed $N=11$, 2.11 at fixed
$N=27$, 3.37 at fixed $N=31$, and 8.19 at balanced $N=27$. Disabling the
preconditioner gives ratios 2.49 and 1.50 in the fixed and balanced $N=23$
controls. The regression retains the 60 nonconverged endpoints as right-censored
observations. It is exploratory, not causal, and its model intervals have no
population-sampling or physical-uncertainty interpretation.

The exact frozen expanded-study criteria are not supported. This is a synthetic
negative result, not evidence of material behavior or a general Wannier
convergence theorem.

## Native evidence

The native working set remains outside Git at:

`/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/optimizer-basin-20260918T110000Z`

A local, untransmitted archive is retained at:

`/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/periodic-2d-optimizer-basin-native-evidence-20260918T110000Z.tar.gz`

Its size is 63,801,989 bytes and its SHA-256 is
`c775d55d6b904700b73d5ea2c7654a84c616b2d4ef3344f938501bec7c7725a2`.
The archive is not a published deposit and has not been transmitted.

The standalone native working set is retained separately at:

`/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/standalone-optimizer-20260918T121659Z`

It contains 14 interfaces, 256 initial localizations, 120 continuations, the
pre-resume snapshot, and the final execution record. Its local untransmitted
archive is:

`/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/periodic-2d-standalone-optimizer-native-evidence-20260918T121659Z.tar.gz`

The archive is 397,083,715 bytes with SHA-256
`ac02665dccc1480a9c5ec36997a5971c059c3612ea8def7f715a83922c5a02e8`.
It contains 5,939 members, including 3,880 regular files and 1,248 retained
relative symbolic links. Public deposit remains a separate authorized
publication-production step.

## Verification

From `python/`:

```bash
uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_study.py \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/result.json

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_study.py \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/result.json \
  --native

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_reanalysis.py \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/reanalysis-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_native_evidence_archive.py \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/native-evidence-archive.json

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_standalone_execution.py \
  --proposal ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-study-proposal.json \
  --starts ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-initial-gauges.json \
  --execution-result /Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/standalone-optimizer-20260918T121659Z/execution-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_standalone_results.py \
  --proposal ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-study-proposal.json \
  --execution-result /Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/standalone-optimizer-20260918T121659Z/execution-result.json \
  --result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_standalone_convergence_regression.py \
  --source-result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-result.json \
  --regression-result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-convergence-regression.json

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_standalone_archive.py \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-native-evidence-archive.json
```

The first command verifies retained identities, all original execution
manifests, every native spread and hopping tail, basin membership, and the
convergence disposition. The `--native` mode additionally reconstructs every
converged start from native Wannier90 files through the independent corrected
Wannier90 verifier. Nonconverged starts are independently checked against their
native final iteration, spread, unitary matrices, and hopping files rather than
being reclassified as converged. The reanalysis verifier independently parses
spread components and traces, reconstructs radius-18 tails and $D_4$-aware
basins, and repeats the $256^2$--$1024^2$ common-estimator calculation.

Verify repository artifact identities with:

```bash
cd calculations/research-monograph/periodic-2d-optimizer-basin
shasum -a 256 -c SHA256SUMS
```

## Reproduction boundary

`execute_study.py` records the historical authorized execution procedure. Its
presence is not authorization to rerun protected scientific software. A new
execution requires a new explicit authorization and preflight. Existing
calculated evidence can be reanalyzed, verified, and replotted without rerunning
Wannier90:

```bash
cd python
uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/reanalyze_study.py \
  --result ../calculations/research-monograph/periodic-2d-optimizer-basin/result.json \
  --base-extractor ../calculations/research-monograph/periodic-2d/extract_wannier90.py \
  --output ../calculations/research-monograph/periodic-2d-optimizer-basin/reanalysis-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/plot_study.py \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/result.json \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/summary.png

uv run python \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/plot_reanalysis.py \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/reanalysis-result.json \
  ../calculations/research-monograph/periodic-2d-optimizer-basin/reanalysis-summary.png
```
