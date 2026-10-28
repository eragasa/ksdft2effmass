# Selected rank-one finite numerical controls

## Scope

This record freezes the bounded Phase 2 simulation controls for the exact parent selected
in [`scientific-control-decision.md`](scientific-control-decision.md). It defines a
Mathieu-compatible scalar support/error--locality baseline with the later draft-program
three-channel and finite error--complexity diagnostics. It does not define a Formal
certificate, continuum limit, uncertainty estimate, or material-accuracy criterion.

## Momentum point sets

For each construction size `N` in

```text
(32, 64, 128, 256)
```

the construction mesh is

\[
Q_N=\left\{-\frac12+\frac{j}{N}:j=0,\ldots,N-1\right\}.
\]

The production construction size is `N = 256`. The common evaluation inventory has
`M = 1025` points

\[
E=\left\{-\frac12+\frac{i+1/257}{1025}:i=0,\ldots,1024\right\}.
\]

This is the Mathieu stagger scaled from construction size 64 and evaluation size 257.
It is exactly disjoint from every declared `Q_N`: equality would imply
`257*1025*j = N*(257*i + 1)`. Because every `N` is a power of two and the odd factors on
the left are coprime to `N`, `N` must divide `j`; no admitted `j` then satisfies the
equality. The common evaluation inventory gives a like-for-like finite comparison across
construction meshes. It is not a continuum guarantee. Evaluation-mesh refinement is not
part of the initial production contract.

## Fourier and support inventories

For even `N`, the complete centered cyclic representatives are

\[
\{-N/2,-N/2+1,\ldots,N/2-1\}.
\]

The ordinary symmetric support at maximum range `R` is

\[
S_R=\{-R,-R+1,\ldots,R\},\qquad R=0,\ldots,15.
\]

All sixteen integer ranges are present and ordered increasingly. The support complexity
is `c(R) = 2*R + 1`. At `N = 32`, `c(15) = 31 < 32`; the cyclic Nyquist representative
`-N/2` never receives ordinary hopping meaning. Transform-mediated truncation and the
equal-weight direct fit use the same ordered `S_R`.

The direct fit uses an explicitly Hermitian scalar parameterization: the onsite
coefficient is real and `t[-r] = conjugate(t[r])`. Its declared design rank and condition
number are retained and independently checked.

## Mathieu-compatible attained channels

For every `N` and `R`, retain:

- transform-mediated training and evaluation candidates and maximum errors;
- omitted complete-transform coefficient `L2` norm;
- Parseval observed, expected, and residual channels;
- equal-weight direct-fit coefficients, design diagnostics, training `L2` and maximum
  residuals, and total evaluation maximum error;
- transform/direct coefficient `L2`, sampled `L2`, and sampled maximum defects;
- scalar bandwidth, zone-center curvature, and imaginary residual; and
- the complete cyclic-to-ordinary-support/Nyquist diagnostic.

These are results for the selected Option B parent. Donor values are not copied or
relabelled.

## Three evaluation-error channels

For the exact scalar field `H`, complete cyclic interpolant `I_N`, and
transform-mediated truncation `T_(N,R)`, retain both maximum and root-mean-square values
on `E` for

\[
H-I_N,\qquad I_N-T_{N,R},\qquad H-T_{N,R}.
\]

The maximum values are

\[
e_{\mathrm{int}}(N)=\max_{q\in E}|H(q)-I_N(q)|,
\]

\[
e_{\mathrm{trunc}}(N,R)=\max_{q\in E}|I_N(q)-T_{N,R}(q)|,
\]

and

\[
e_{\mathrm{tot}}(N,R)=\max_{q\in E}|H(q)-T_{N,R}(q)|.
\]

The corresponding root-mean-square value is the square root of the arithmetic mean of
squared absolute residuals over all 1025 evaluation points. Residuals telescope
pointwise, but maxima and root-mean-square summaries are never added as identities.
Independent verification reconstructs all values and checks the applicable norm triangle
inequalities. `e_int` is independent of `R`; deliberate truncation and total error are
support-indexed. First-passage decisions use total error only.

The direct-fit route retains its own total evaluation maximum and root-mean-square errors
and its defects from the transform-mediated route. A direct-fit residual is never named
interpolation or transform truncation.

## Sampled-gap qualification

On the authenticated finite union `Q_256 union E`, retain the least first-to-second
ordered eigenvalue gap and its minimizing momentum and mesh role. The qualification is

\[
\min_{q\in Q_{256}\cup E}\bigl(\lambda_1(K(q))-\lambda_0(K(q))\bigr)
\ge 0.25\,E_{\mathrm{ref}}.
\]

Equality passes. Failure is fail-closed. This prospectively selected quarter-reference
margin is a synthetic robustness gate for the controlled family, not a value inferred
from the Option B outcome. Its permitted claim is limited to the declared sampled union;
it is not global band isolation.

## Numerical consistency and refinement gates

For energy-valued producer/verifier comparisons, require

\[
|x_p-x_v|\le 10^{-12}E_{\mathrm{ref}}
 +10^{-12}\max(|x_p|,|x_v|).
\]

Use the analogous mixed rule with absolute term `1e-12` after explicit normalization for
dimensionless channels and `1e-12*E_ref^2` for squared-energy channels. Inventories,
identifiers, shapes, units, orderings, rational mesh definitions, and dispositions match
exactly. Reject booleans as numbers, numeric strings, nonfinite values, unknown or
missing fields, endpoint violations, and digest mismatches.

Consistency tolerances never relax the sampled-gap or application thresholds. If
independent computations lie on opposite sides of a decisive threshold, the decision
fails closed even when their values satisfy the consistency comparison.

Final construction-mesh stability compares `N = 128` with `N = 256` on the same `E` and
supports. Normalize energy values by `E_ref` and squared-energy values by `E_ref^2`, then
require maximum componentwise absolute change no greater than `1e-10` across:

- the interpolation maximum and root-mean-square values;
- every support-indexed transform truncation and total maximum/root-mean-square value;
- direct-fit total maximum/root-mean-square values;
- omitted norms and transform/direct coefficient and sampled defects; and
- the production first-passage disposition.

The first-passage identifier, including explicit `none`, must be unchanged. Earlier mesh
pairs are retained as refinement diagnostics but are not required to satisfy the final
stability gate. Adjacent-mesh changes are not continuum errors or uncertainty estimates.

## Application threshold and passage

The prospectively frozen application threshold is

\[
T=10^{-8}E_{\mathrm{ref}}.
\]

It is inherited as a controlled donor/draft-program target and is not a material-accuracy
criterion or a theorem. For production `N = 256`, a range passes jointly when both the
transform-mediated and equal-weight direct-fit total maximum evaluation errors are no
greater than `T`.

`first_joint_pass` is the least passing `R` after checking every earlier member of
`0,...,15`; no monotonicity is assumed. If no range passes, its value is explicit `none`.
`sustained_after_first_pass` records whether every later declared support also passes. A
false sustained flag reports a nonmonotonic anomaly and prevents interpretation of the
first passing range as a stable cutoff; it does not replace `first_joint_pass` with a new
suffix-envelope objective.

## Finite error--complexity analysis

For each construction `N` separately, the attained candidate at `R` has the primary
objective pair

\[
\bigl(c(R),e_{\mathrm{tot}}(N,R)\bigr),\qquad c(R)=2R+1,
\]

with both objectives minimized. One attained candidate dominates another exactly when it
is weakly no worse in both objectives and strictly better in at least one. Equal objective
vectors do not dominate each other. The verifier independently reconstructs the finite
nondominated mask from authenticated values. Tolerances do not manufacture dominance;
near-equal total errors within the producer/verifier consistency scale are flagged
separately without changing the mask.

Direct-fit error, omitted norm, interpolation floor, route defects, and the `1e-8`
threshold accompany each point but are not silently substituted as Pareto objectives.
Points from different construction meshes are never pooled. The threshold overlay and
actual `first_joint_pass` remain a separate decision layer.

## Closed authenticated figure inventory

The initial native inventory is:

1. `rank1-fourier-locality.png`, containing parent/gap qualification, coefficient decay
   with omitted norm, three-channel error behavior across support and construction mesh,
   and the per-mesh error--complexity view with production threshold and actual first
   passage; and
2. `rank1-fourier-route-agreement.png`, containing direct/mediated coefficient and
   sampled defects plus their separately named total evaluation errors.

Every plotted value, threshold, mask, flag, support, and marker comes from the
verifier-owned authenticated projection. Neither figure is a Formal certificate or a
continuum claim.
