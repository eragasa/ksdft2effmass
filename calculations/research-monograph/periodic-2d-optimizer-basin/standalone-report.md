# Standalone optimizer-convergence study report

## Status

**Calculated and independently verified synthetic non-DFT numerical evidence.**

This study evaluates Wannier90 localization behavior for the frozen rank-three
periodic-2D parent. It is a controlled negative result: the declared
finite-sequence optimizer and discretization criteria are not supported. The
result does not validate DFT, silicon, another material, production
Wannierization, a global optimizer, or a general convergence theorem.

## Execution

Fourteen unique interfaces received the same 16 deterministic starts. Two
$N=23$, $P=4$ interfaces repeated all starts with the preconditioner disabled.
All 256 initial processes exited successfully. At 5000 iterations, 136 satisfied
the native criterion and 120 did not. Every nonconverged trajectory was
continued once from its exact checkpoint for at most 15000 additional
iterations. All 120 continuation processes exited successfully; 60 satisfied
the native criterion and 60 remained nonconverged.

The complete execution therefore contains 376 localization stages and 256 final
trajectory endpoints. Its cumulative runtime was 8589.24 s (2 h 23 min), and
the retained external tree occupied 1,917,288,708 bytes at execution close.
Process completion and native localization convergence remain distinct.

The 60 final nonconverged traces are descriptively classified as:

| Terminal behavior | Count |
|---|---:|
| continuing descent at the iteration limit | 30 |
| near-stationary without five-step native convergence | 25 |
| oscillatory or stalled | 4 |
| stalled or nondescent | 1 |

These labels summarize the final 200 trace points and do not reclassify native
convergence.

## Common analysis

For a trajectory that converged initially, the initial endpoint is the effective
endpoint. Otherwise, the retained continuation endpoint is used whether or not
it ultimately converged. Initial and continuation records remain separate.

Every effective endpoint was reconstructed on the common $1024^2$
finite-supercell grid. The analysis retains

$$
\Omega=\Omega_I+\widetilde\Omega,
\qquad
\widetilde\Omega=\Omega_D+\Omega_{OD},
$$

common-grid centers and spreads, and hopping tails outside $R^2=8$ and 18.
Observed basins require agreement in $\widetilde\Omega$, centers under orbital
permutation, periodic wrapping and all eight $D_4$ operations, and matched
active-plane density $L^2$ distance.

Independent verification reparsed every effective native endpoint, reconstructed
every radius-8 and radius-18 hopping tail, checked all endpoint and group
counts, and independently reconstructed the common-grid density identity,
center, and spread for the best and center-medoid endpoint of every group
(32 sampled reconstructions).

## Mesh behavior

The final baseline convergence counts are:

| $N$ | fixed $c=31$ | balanced $c=N$ |
|---:|---:|---:|
| 11 | 16/16 | 16/16 |
| 15 | 15/16 | 16/16 |
| 19 | 16/16 | 15/16 |
| 23 | 12/16 | 12/16 |
| 27 | 9/16 | 6/16 |
| 31 | 6/16 | 6/16 |

The frozen minimum fraction is 12/16. It fails for both $N=27\to31$
endpoints. The deterioration with mesh size is an observed property of this
protocol, not proof of a universal mesh dependence.

For the fixed-$c=31$ finest pair $N=27\to31$:

- best-start $\Omega_I$ changes by 4.66%;
- best and median $\widetilde\Omega$ change by 1.62% and 1.59%;
- best and median center-set distances are 0.00252 and 0.0327 cell;
- best and median radius-18 tail changes are 2.52% and 1.41%; and
- neither endpoint has a repeated best basin.

The spread-component, median-center, convergence-fraction, and basin conditions
therefore fail even though the hopping-tail conditions pass.

The $a+b/N^2$ holdout fit on $N=15,19,23,27$ also fails at $N=31$:

| Summary | $\Omega_I$ residual | $\widetilde\Omega$ residual | radius-18 tail residual |
|---|---:|---:|---:|
| best | 3.69% | 2.54% | 0.111% |
| median | 3.69% | 2.54% | 0.480% |

Only the hopping-tail holdouts meet the 1% threshold.

## Cutoff, embedding, and preconditioner controls

At $N=23$, $c=31$, cutoffs $P=3,4,5,6$ each retain 12/16 final converged
starts. The finest pair $P=5\to6$ passes all frozen spread, center, tail, and
converged-fraction metrics. It still fails the required repeated-best-basin
condition.

Fixed and balanced embeddings agree closely through $N=23$ for the best
observed endpoint. At $N=27$, their best-center distance increases to 0.00480
cell and their radius-18 tail difference to 1.08%. This is retained as inactive-
embedding sensitivity rather than combined with mesh error. The $N=31$ point is
shared and therefore has zero representation difference by construction.

At the two $N=23$, $P=4$ controls, the preconditioned protocol finishes with
12/16 converged starts. Disabling the preconditioner gives 10/16 for fixed
$c=31$ and 11/16 for balanced $c=23$. Thus enabling the preconditioner is
associated with two and one additional native convergences in these two matched
controls. The best observed $\widetilde\Omega$ values remain close. This is a
descriptive observation; no general preconditioner advantage is inferred.

## Exploratory censored convergence regression

A post-hoc log-normal accelerated-failure-time regression uses total optimizer
iterations as the response. The 60 endpoints lacking native convergence are
right-censored at their retained final iteration rather than discarded or
assigned a fabricated convergence time. The model includes one effect for each
configuration/optimizer group and fixed effects for the 16 deterministic starts.
The fixed $c=31$, $P=4$, $N=23$ preconditioned group is the reference.

Selected adjusted convergence-time ratios are:

| Group | Time ratio | Exploratory 95% model interval |
|---|---:|---:|
| fixed $N=11$ | 0.335 | 0.138--0.812 |
| fixed $N=27$ | 2.11 | 0.486--9.17 |
| fixed $N=31$ | 3.37 | 0.817--13.9 |
| balanced $N=27$ | 8.19 | 3.46--19.4 |
| fixed $N=23$, preconditioner off | 2.49 | 1.15--5.41 |
| balanced $N=23$, preconditioner off | 1.50 | 0.641--3.49 |

Ratios above one indicate more iterations to native convergence. The regression
reinforces the descriptive concentration of slow or censored trajectories on
finer meshes and gives more information than convergence counts alone. The wide
intervals for several groups retain the limits of the finite design. Because the
starts are deterministic rather than sampled from a population, these
start-clustered sandwich intervals are model diagnostics only: they are not
physical uncertainty quantification, population inference, causal effects, or a
replacement for the native criterion.

## Observed basins

Under the frozen tolerances, every converged endpoint remains a singleton
observed density-aware $D_4$ basin. Thus the best-basin occupancy is one in all
16 configuration/optimizer groups, below the required occupancy of four and
without membership in both start blocks.

The nearest rejected pair has density $L^2$ mismatch
$2.23\times10^{-5}$, above the frozen $10^{-5}$ threshold, despite center
distance $3.61\times10^{-6}$ cell. It does not prove 196 physically distinct
local minima: it establishes only that the endpoints are not equivalent under
the declared numerical classifier.

The study design required reconstruction-roundoff and exact self-symmetry
controls before execution. No retained record demonstrates that this check was
performed at the specified time, so this remains a protocol deviation that
cannot be corrected retroactively. Post-hoc identity, orbital-permutation,
all-eight-$D_4$, and integer-translation controls over the 16 group-best
endpoints give maximum center and density mismatches of
$5.56\times10^{-17}$ cell and $6.69\times10^{-16}$, respectively. Independent
round-trip reconstruction verifies that these controls remain below
$10^{-8}$.

A post-hoc threshold sensitivity analysis gives no direct matching endpoint
pair through density tolerance $2\times10^{-5}$, one non-best pair at
$2.5\times10^{-5}$, and five pairs across four groups at $10^{-4}$. The
best-endpoint direct occupancy remains one at every tested threshold through
$10^{-4}$. These checks bound numerical roundoff and show that the best-basin
failure is insensitive over the tested range; they do not restore compliance
with the missed pre-execution step.

## Disposition

The standalone study does **not** support the frozen combined convergence
criteria. Its principal retained findings are:

1. continuation rescues half of the 120 initially nonconverged trajectories;
2. final native convergence degrades strongly on the finer meshes;
3. the finest fixed-mesh pair and inverse-square holdout fail spread criteria;
4. the finest cutoff pair is numerically stable except for basin reproducibility;
5. two matched controls associate preconditioning with one or two additional
   native convergences, without establishing a general advantage; and
6. no repeated best basin is observed under the density-aware quotient.

These are synthetic numerical results, not material validation or uncertainty
quantification. Further iterations, another optimizer, changed tolerances, or a
DFT interface would constitute new controlled work.

## Reproduction

No Wannier90 rerun is needed for offline reproduction. From `python/`:

```text
uv run python ../calculations/research-monograph/periodic-2d-optimizer-basin/extract_standalone_results.py \
  --proposal ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-study-proposal.json \
  --execution-result /Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/standalone-optimizer-20260918T121659Z/execution-result.json \
  --output ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-result.json

uv run python ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_standalone_results.py \
  --proposal ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-study-proposal.json \
  --execution-result /Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/standalone-optimizer-20260918T121659Z/execution-result.json \
  --result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-result.json

uv run python ../calculations/research-monograph/periodic-2d-optimizer-basin/plot_standalone_results.py \
  --result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-result.json \
  --output ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-summary.png

uv run python ../calculations/research-monograph/periodic-2d-optimizer-basin/analyze_standalone_convergence_regression.py \
  --result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-result.json \
  --output ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-convergence-regression.json

uv run python ../calculations/research-monograph/periodic-2d-optimizer-basin/verify_standalone_convergence_regression.py \
  --source-result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-result.json \
  --regression-result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-convergence-regression.json

uv run python ../calculations/research-monograph/periodic-2d-optimizer-basin/plot_standalone_convergence_regression.py \
  --result ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-convergence-regression.json \
  --output ../calculations/research-monograph/periodic-2d-optimizer-basin/standalone-convergence-regression.png
```
