# Numerical definition

## Common represented frame

At each source-mesh point, let \(C(\mathbf{k})\) contain the retained parent
plane-wave eigenvectors and let \(W(\mathbf{k})\) be the accepted
parent-to-Wannier isometry, including disentanglement when applicable. The
production pseudopotential is norm-conserving, so the parent overlap metric is
the identity. Define

\[
H^W(\mathbf{k}) = W(\mathbf{k})^\dagger
E(\mathbf{k})W(\mathbf{k}),
\]

\[
T^W(\mathbf{k}) = W(\mathbf{k})^\dagger C(\mathbf{k})^\dagger
T^{\mathrm{PW}}(\mathbf{k})C(\mathbf{k})W(\mathbf{k}),
\qquad
R^W(\mathbf{k})=H^W(\mathbf{k})-T^W(\mathbf{k}).
\]

All three operators use the same accepted state space and frame at every
\(\mathbf{k}\). Basis, reciprocal coordinates, Fourier phase, energy unit,
energy reference, lattice representatives, and any Wigner--Seitz degeneracy
weights must be explicit.

Before interpretation, independent checks must establish:

- isometry/unitarity defects;
- Hermiticity of reciprocal- and real-space matrices;
- \(H^W-T^W-R^W\) closure;
- forward/inverse Fourier reconstruction;
- covariance under controlled unitary frame transformations;
- consistency with native Wannier90 \(H^W(\mathbf R)\); and
- exact correlation of every consumed artifact with its manifest entry.

## Pair-symmetric physical-radius truncation

For \(X\in\{H,T,R\}\), define

\[
X^W_r(\mathbf{k})=
\sum_{\lVert\mathbf R\rVert\le r}
X^W_{\mathbf R}e^{i\mathbf{k}\cdot\mathbf R},
\]

using canonical lattice representatives and a pair-symmetric mask. Mesh studies
compare fixed physical radii common to every mesh, not equal block counts. The
primary direct error is

\[
\epsilon_X(r)=
\max_{\mathbf{k}\in K_{\mathrm{eval}}}
\left\|X^W(\mathbf{k})-X^W_r(\mathbf{k})\right\|_2.
\]

Retain two complementary tail quantities:

\[
B_X(r)=\sum_{\lVert\mathbf R\rVert>r}
\lVert X^W_{\mathbf R}\rVert_2,
\qquad
F_X(r)=\left(
\sum_{\lVert\mathbf R\rVert>r}
\lVert X^W_{\mathbf R}\rVert_F^2
\right)^{1/2}.
\]

\(B_X\) is a uniform operator-error upper bound. \(F_X\) is an RMS/Parseval
measure and must not be described as a uniform bound. Report absolute errors in
electron volt or millielectron volt. Any relative normalization must be frozen
before evaluation and reported alongside the absolute quantity.

For each preregistered operator tolerance \(\tau\), define the support radius
from the monotone error envelope:

\[
r_X(\tau)=\inf\left\{r:
\sup_{r'\ge r}\epsilon_X(r')\le\tau\right\}.
\]

This avoids choosing one favorable point from a nonmonotone direct-error curve.
For Hermitian represented matrices, Weyl's inequality gives

\[
\max_j\left|\lambda_j(X^W)-\lambda_j(X^W_r)\right|
\le \left\|X^W-X^W_r\right\|_2.
\]

Ordered-eigenvalue errors are secondary diagnostics. Eigenvalues of \(T^W\) and
\(R^W\) are not independent material observables.

## Evaluation channels

Three channels remain distinct:

1. **Source-mesh reconstruction** checks exact finite-transform identities at
   Wannier source points.
2. **Finite-representation compression** compares complete and truncated finite
   Fourier representations on a deterministic dense or staggered reciprocal
   grid. Dense evaluation of the finite representation is not independent
   first-principles validation.
3. **Withheld parent validation** compares the complete Si-VC Hamiltonian with
   direct QE energies and required gap, valley, mass, and withheld-band records.
   A withheld test of \(T^W\) or \(R^W\) is claimed only when the accepted
   retained frame is independently extended to those points.

Training, construction, and withheld roles are sealed before confirmatory
analysis. Evaluation cannot revise fitting, frame, window, threshold, or
candidate-selection decisions.

## Error bookkeeping

Retain separate records for:

- parent-model choices and their bounded sensitivity checks;
- basis, cutoff, reciprocal-mesh, Fourier, and floating-point numerical errors;
- retained-subspace and gauge-construction variation;
- real-space truncation or model-reduction error; and
- withheld parent-versus-reduced validation error.

These channels must not be pooled into one uncertainty number unless a later
specification defines and justifies that relationship. Mesh-to-mesh variation is
not by itself uncertainty quantification, and passing software tolerances is not
scientific validation.

## Prospective staged design

These stages describe meanings of CPN places and transitions; they are not a
second DAG or imperative runner.

### Stage 0 — execution-free qualification

Complete strict records/codecs, parsers, synthetic tests, independent
reconstruction, norm/tail calculations, pair-symmetric masks, verifiers, and
tamper tests. Qualify the ONCV \(S=I\) route without importing the legacy
ultrasoft convention as authority.

### Stage 1 — Si-V control

After separate authorization, construct the occupied-valence control to qualify
the QE--Wannier90 bridge and expose isolated-subspace, gauge, or Fourier defects.
It cannot establish the Si-VC headline claim.

### Stage 2 — Si-VC candidate selection

Evaluate the prospectively frozen rank/projection/window candidates under Tasks
`03.01.01`--`03.01.03`. Test rather than presume the rank-ten candidate.
Compressibility outcomes remain unavailable to selection.

### Stage 3 — Wannier-mesh convergence

Refine a prospectively frozen uniform sequence, potentially
\(4^3,6^3,8^3,10^3\). The \(4^3\) point is a lower diagnostic and is not
presumed adequate. The primary comparison uses only common, non-aliased physical
radii.

### Stage 4 — parent-representation guards

At the provisionally selected Wannier mesh, test lower/accepted/higher cutoff
guards with `ecutrho = 4 * ecutwfc`. Test ratios 6 or 8 only if charge-density
sensitivity controls an accepted observable. Retain bounded cutoff--SCF-mesh and
cutoff--Wannier-mesh interaction checks.

### Stage 5 — gauge robustness

Repeat the accepted construction from prospectively identified,
symmetry-compatible initializations. Compare subspaces, interpolation,
centers/spreads, and component-compression diagnostics without changing windows,
thresholds, or optimizer policy.

### Stage 6 — confirmatory locality evaluation

Freeze radii, tolerances, grids, normalization, comparison rules, and
dispositions before opening component-tail results. Evaluate \(\epsilon_X\),
\(B_X\), \(F_X\), and \(r_X(\tau)\) for every accepted numerical and gauge guard.
The complete finite block family remains the reference representation;
truncation is an evaluated approximation.

## Numerical blockers

No production result can be interpreted until the campaign has:

- an accepted cutoff/SCF-mesh setting and bounded interaction check;
- an accepted zero-pressure structure;
- a qualified production SCF parent and restart lineage;
- semantically qualified NSCF outputs with exact requested k-point and band
  inventories;
- accepted subspace, projection, window, mesh, and gauge policies;
- complete represented-frame reconstruction and independent verification; and
- direct-QE path, valley, and effective-mass validation records defining the
  withheld domain.

The provisional `C48/K8` setting is planning input only and must not be promoted
silently.
