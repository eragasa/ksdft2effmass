# Protocol: deterministic optimizer-basin and convergence study

## Evidence class and ownership

This protocol defines synthetic non-DFT numerical verification for the
rank-three periodic-2D Wannier90 interface. Wannier90 owns the localization
objective and native convergence decision. The repository driver owns the
synthetic parent/interface generation, deterministic initialization family,
resource bounds, retained manifests, and analysis policy.

The accepted periodic-2D exercise remains unchanged. This follow-up addresses
only the previously retained optimizer-basin and finite-parameter convergence
ambiguity.

## Frozen parent and configurations

The parent Hamiltonian, retained rank-three subspace, trial functions, energy
convention, and interface construction are inherited from
`../periodic-2d/composite-input.json` and `../periodic-2d/prepare_wannier90.py`.
The configuration axes are:

- mesh: $N=11,15,19,23$ at $P=4$ and balanced auxiliary length $c=N$;
- cutoff: $P=2,3,4,5$ at $N=c=19$;
- inactive embedding: $c=15,19,23$ at $P=4,N=19$.

Shared points occur only once, giving nine interfaces and 72 localizations.
The auxiliary third direction is not physical. Only active-plane centers,
spreads, hoppings, and represented operators are interpreted.

## Deterministic initialization family

Let $A(\mathbf k)$ be the baseline $3\times3$ trial-overlap matrix. Start $s$
uses

$$
A_s(\mathbf k)=A(\mathbf k)U_s(\mathbf k),
$$

where

$$
U_s(\mathbf k)=\prod_j
\exp\left[i\alpha_{sj}
\sin\left(2\pi\mathbf m_{sj}\cdot\mathbf k+\phi_{sj}\right)G_{sj}\right].
$$

The ordered amplitudes $\alpha_{sj}$, integer reciprocal harmonics
$\mathbf m_{sj}$, phases $\phi_{sj}$, and traceless Hermitian generators
$G_{sj}$ are frozen in `study-input.json`. They comprise identity, single
soft rotations, diagonal winding, mixed two-generator, and stronger
higher-harmonic starts.

Each $U_s(\mathbf k)$ is smooth, reciprocal-periodic, and unitary. Consequently
$A_sA_s^\dagger=AA^\dagger$: the retained physical subspace and singular values
are unchanged. The driver checks unitarity and Gram-matrix preservation at
every mesh point to $10^{-12}$ Frobenius tolerance before localization.

This family probes optimizer trajectories. It is not a probability measure over
all initial conditions and cannot prove discovery of a global minimum.

## Execution policy

For each configuration, the parent eigensystem, `.eig`, `.nnkp`, and `.mmn`
interface are prepared once. Each deterministic `.amn` initialization is then
localized exactly once. Runs are serial. No failed or unfavorable start is
retried, replaced, removed, or used to modify a later start.

The exact protected-execution limits are:

- 72 localizations;
- 300 seconds per stage and 7200 seconds total;
- 512 MiB resident memory per stage;
- 8 MiB external output per localization and 400 MiB total;
- stop on the first exceeded resource bound.

A process exit code of zero is not equated with localization convergence.
Convergence requires the explicit native Wannier90 convergence statement.
Endpoints at the 5000-iteration bound without that statement remain
nonconverged evidence.

## Localization estimators

Native Wannier90 Berry-link spread is the primary objective used to classify
optimizer convergence and compare finite-parameter sequences. It retains the
same owning definition across the study.

A separate common $512^2$ finite-supercell estimator reconstructs each external
gauge and the direct projected gauge in a shared represented setting. The grid
is large enough to avoid aliasing for the largest declared $(P,N)=(5,23)$
combination. This common estimator supports within-configuration representation
comparisons; it is not substituted for the native objective in the mesh and
cutoff convergence gate. Native and common spreads remain distinct.

The radius-50 hopping tail is

$$
\tau_{50}=\left(
\sum_{R_x^2+R_y^2>50}\lVert H_{\mathrm W}(\mathbf R)\rVert_{\mathrm F}^2
\right)^{1/2}.
$$

Centers are compared as unordered active-plane sets after periodic wrapping.
Orbital permutations are minimized explicitly.

## Observed basin classification

Only native-converged endpoints are classified as observed basins. Two
converged endpoints belong to one observed basin only when both conditions hold:

1. native total-spread difference is at most $10^{-8}a^2$; and
2. maximum matched periodic center distance is at most $10^{-5}$ cell.

Nonconverged endpoints are retained separately and never promoted into a basin.
The quotient handles orbital permutation and lattice-period wrapping. It does
not quotient every point-group or continuous gauge equivalence, so the observed
basin count is deliberately conservative and is not a theorem about distinct
stationary points.

The `best observed converged` endpoint minimizes native spread among converged
starts. It is not called a global minimum. The across-start median uses only
converged starts. Its center representative is the center-set medoid, while
spread and hopping-tail values are scalar medians.

## Frozen convergence gate

For both the mesh pair $N=19\to23$ and cutoff pair $P=4\to5$, the best observed
converged endpoint and the median converged-start summary must simultaneously
satisfy:

- relative native-spread change $\le 1\%$;
- periodic center-set distance $\le0.01$ cell;
- relative radius-50 tail change $\le10\%$.

In addition, the best observed basin must have occupancy at least two at both
endpoints. Both mesh and cutoff pairs must pass for a convergence-supporting
classification. Inactive-embedding sensitivity is reported separately and does
not substitute for either sequence.

Failure of any gate is retained as a negative numerical result. Passing would
still establish only the frozen finite-parameter criterion, not a mathematical
limit, global optimizer convergence, material validation, or uncertainty
quantification.

## Authorized offline reanalysis

The later human-authorized recommendation performs no new Wannier90 execution.
It preserves `result.json` and reanalyzes the retained native files in
`reanalysis-result.json`.

The native final spread is decomposed as

$$
\Omega=\Omega_I+\widetilde\Omega,
\qquad
\widetilde\Omega=\Omega_D+\Omega_{OD}.
$$

$\Omega_I$ diagnoses retained-subspace and reciprocal-discretization change;
$\widetilde\Omega$ diagnoses the gauge-dependent localization objective. The
symmetry-aware observed-basin classifier replaces total spread with
$\widetilde\Omega$ and minimizes center-set distance over orbital permutation,
periodic wrapping, and all eight $D_4$ square-lattice operations. The original
and reanalyzed classifications remain separately retained.

For each run, the last at most 200 native iteration records provide spread
slope, detrended spread RMS, median absolute spread change, and median RMS
gradient. Post-hoc nonconverged labels distinguish continuing descent, near
stationarity without window convergence, oscillatory or stalled behavior, and
other stalled or nondescent behavior. These labels are explicitly exploratory
diagnostics, not predeclared acceptance rules and not substitutes for the
native convergence statement.

Cross-mesh hopping comparison uses the radius-18 tail, which is representable on
every declared mesh. Radius 50 remains retained in the original study but is not
used as a common all-mesh diagnostic because the $N=11$ translation domain
cannot support a nonzero tail beyond that radius.

Four representative converged and nonconverged endpoints are reconstructed on
$256^2$, $512^2$, and $1024^2$ common-estimator grids. This tests estimator
discretization separately from Wannier90 mesh, plane-wave cutoff, embedding, and
optimizer error. No post-hoc diagnostic is promoted into a new convergence gate.

## Standalone fixed-embedding and continuation study

The publication follow-up retains the same synthetic parent but adds the exact
interfaces and starts declared in `standalone-study-proposal.json`:

- fixed $c=31$ and balanced $c=N$ mesh sequences at
  $N=11,15,19,23,27,31$;
- a $P=3,4,5,6$ cutoff sequence at $N=23,c=31$;
- identity plus 15 deterministic Halton-designed smooth periodic $U(3)$ starts;
- preconditioner-disabled controls at the fixed and balanced $N=23,P=4$
  interfaces; and
- one exact-checkpoint continuation of every initially nonconverged trajectory.

The initial protocol permits 5000 iterations. Continuations permit 15000
additional iterations with the same $10^{-12}$ tolerance and five-step window.
The original and continued endpoints remain distinct records. The effective
analysis endpoint is the initial endpoint when it converged and otherwise the
continuation endpoint, whether or not the continuation converged.

The standalone common estimator uses $1024^2$. Basin classification uses
$\widetilde\Omega$, orbital permutation, periodic lattice translation, all
eight $D_4$ operations, and matched active-plane density. The density mismatch
is the continuous-grid $L^2$ norm reconstructed by Parseval after the matched
$D_4$ operation and integer-cell Fourier translation. Frozen tolerances are
$10^{-6}a^2$ in $\widetilde\Omega$, $10^{-3}$ cell in centers, and $10^{-5}$
in density mismatch. The best basin must have occupancy at least four and
appear in both eight-start blocks. The design required exact self-equivalence
and reconstruction-roundoff checks before execution, but no retained record
shows that this check occurred at the specified time. This is preserved as a
protocol deviation. Post-hoc exact-equivalence and threshold-sensitivity
controls are diagnostics only and do not retroactively satisfy that requirement.

The finest fixed-mesh pair is $N=27\to31$ and the finest cutoff pair is
$P=5\to6$. Best and median summaries must meet the separate $\Omega_I$,
$\widetilde\Omega$, center, radius-18 tail, converged-fraction, and repeated-
basin criteria in `standalone-study-proposal.json`. A separate holdout fits
$a+b/N^2$ on $N=15,19,23,27$ and predicts $N=31$. Fixed and balanced
representations are compared only at common $N$ and their difference remains an
embedding result.

The first execution stopped after all 256 initial localizations and five
continuations because the immutable 8 MiB output bound was exceeded. The
retained stop was not retried. A separately authorized resume snapshots the
pre-resume execution record, reruns no completed stage, and executes only the
115 pending continuations under revised 32 MiB per-continuation and 3 GiB total
tree limits. Flushed terminal progress identifies every resumed stage.

A post-hoc log-normal accelerated-failure-time regression models total optimizer
iterations while retaining final nonconverged trajectories as right-censored
observations. It includes configuration/optimizer-group effects and fixed effects
for all 16 deterministic starts. Start-clustered sandwich intervals are retained
as exploratory model diagnostics only; the deterministic design supplies no
population-sampling, causal, physical-uncertainty, or convergence-theorem
interpretation.

## Independent verification

`verify_study.py` independently checks:

- study, driver, extractor, execution-record, and native-file identities;
- every exit code, timeout, resource bound, and original file manifest;
- final native spread, convergence statement, iteration, unitary matrices, and
  radius-50 hopping tail for all 72 starts;
- full represented-operator and common-estimator reconstruction for every
  converged start through the independent corrected Wannier90 verifier;
- converged/nonconverged partition, basin membership, best endpoint, and frozen
  convergence disposition.

`verify_reanalysis.py` independently parses final $\Omega_I$, $\Omega_D$, and
$\Omega_{OD}$ values and full terminal traces; reconstructs radius-18 hopping
tails and $D_4$-aware basin membership; and independently rebuilds the parent
frames and common finite-supercell localization at all three FFT sizes.

`verify_standalone_execution.py` independently checks all 14 interfaces, 256
initial localizations, 120 exact continuation assignments, both authorization
limits, retained file identities, and the pre-resume snapshot.
`verify_standalone_results.py` independently reparses all effective native
spread components and convergence statements, reconstructs all radius-8 and
radius-18 hopping tails, verifies endpoint and basin arithmetic, and rebuilds
the $1024^2$ common-grid density identity, centers, and spreads for the best and
center-medoid endpoint of all 16 configuration/optimizer groups. It also checks
post-hoc exact-equivalence controls and basin-threshold sensitivity.
`verify_standalone_convergence_regression.py` independently reconstructs the
right-censored likelihood, gradient, category time ratios, adjusted medians,
and selected convergence probabilities from the retained compact endpoint
records.

The archive verifier checks the exact local compressed archive, total member
count and bytes, execution-result identity, and representative required native
members.

## Claim boundary

The calculation tests one synthetic retained subspace, deterministic families
of eight and sixteen starts, and finite mesh/cutoff/embedding sequences. It does
not sample a
probability distribution, establish a global optimum, validate silicon or any
material, validate production Wannierization, quantify uncertainty, or prove a
general localization-convergence theorem.
