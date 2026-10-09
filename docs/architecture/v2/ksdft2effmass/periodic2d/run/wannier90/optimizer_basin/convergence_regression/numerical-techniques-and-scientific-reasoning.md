# Numerical techniques and scientific reasoning

## Scope

The retained analysis is an exploratory post-hoc regression of calculated synthetic,
non-DFT optimizer trajectories. It asks how retained iteration-to-native-convergence
times vary across the finite configuration/optimizer groups after adjustment for the 16
fixed deterministic starts. It does not estimate a universal optimizer law.

Every one of the 256 retained endpoints enters the design. A trajectory with the native
Wannier90 convergence statement supplies an observed event time; a trajectory without
that statement is right-censored at its retained final effective iteration. Process
completion remains distinct from native convergence.

## Declared log-normal accelerated-failure-time model

For endpoint \(i\), let \(t_i>0\) be its effective total iteration count,
\(y_i=\log t_i\), \(x_i\) its fixed design row, and \(\delta_i\) its native-convergence
indicator. The retained parameterization is

\[
 y_i = x_i^T\beta + \sigma z_i,\qquad z_i\sim N(0,1),\qquad
 \sigma=\exp(\lambda)>0.
\]

The design contains an intercept, 15 nonreference group indicators, and 15 nonreference
start indicators. The final parameter is \(\lambda=\log\sigma\), giving 32 fitted
parameters in total. Reference group and start identities are explicit retained fields;
they are not inferred from ordering, names, counts, or coefficient magnitudes.

For converged trajectories, the negative log-likelihood contribution is

\[
 \ell_i = \lambda + \frac{z_i^2}{2} + \frac{1}{2}\log(2\pi).
\]

For right-censored trajectories it is

\[
 \ell_i = -\log\Phi(-z_i),
\]

where \(\Phi\) is the standard-normal cumulative distribution. The implementation uses
`scipy.special.log_ndtr` for the censored log-survival term and reconstructs analytic
per-observation score rows independently from the retained analyzer.

## Hessian and clustered sandwich covariance

The verifier reconstructs the Hessian by centered finite differences of the analytic
gradient. For parameter \(\theta_j\), the step is

\[
 h_j=10^{-5}\max(1,|\theta_j|).
\]

The symmetrized Hessian is pseudoinverted with relative cutoff \(10^{-12}\). Scores are
summed within the 16 deterministic-start clusters. With \(G\) clusters, \(n\)
observations, and \(p\) parameters, the finite-cluster correction is

\[
 \frac{G}{G-1}\frac{n-1}{n-p}.
\]

This construction reproduces the retained exploratory covariance. It does **not** make
the deterministic starts an independent population sample. The resulting intervals are
neither causal intervals nor physical uncertainty quantification.

Dense storage scales as \(O(np+p^2)\). Repeated finite-difference gradient evaluation
scales as \(O(np^2)\). The public route documents possible `MemoryError` and
`OverflowError`; it imposes no arbitrary size cap.

## Category summaries

A nonreference group coefficient \(\gamma_g\) gives retained time ratio
\(\exp(\gamma_g)\). Values above one mean more iterations to the declared native
convergence event within this descriptive model. The reference ratio is exactly one.
The retained 95-percent interval is reconstructed as

\[
 \left[\exp(\gamma_g-1.96s_g),\ \exp(\gamma_g+1.96s_g)\right],
\]

where \(s_g\) is the clustered standard error.

The adjusted median uses the intercept, group coefficient, and arithmetic mean of the
15 explicit nonreference start coefficients plus the reference start's zero coefficient.
At retained checkpoint \(T\), the predicted convergence probability is

\[
 \Phi\!\left(\frac{\log T-\mu_g}{\sigma}\right).
\]

The verifier checks exactly checkpoints 500, 1000, 2500, 5000, 10000, and 20000. These
curves summarize the fitted finite design; they are not forecasts for unobserved physical
systems or production DFT calculations.

## Error and claim separation

This diagnostic concerns observed optimizer trajectory and censoring behavior only. It
does not combine or replace parent-model, basis/discretization, reciprocal sampling,
auxiliary embedding, retained-space, gauge initialization, localization, interpolation,
truncation, or comparison errors. It does not overturn row 052's negative finite-design
convergence disposition or row 053's distinct offline basin reanalysis.

Passing verification establishes that exact retained bytes and the independent
implementation agree within documented numerical tolerances. It does not validate the
log-normal family, justify extrapolation, prove asymptotic or global optimizer behavior,
establish physical adequacy, quantify scientific uncertainty, or authorize acceptance.
