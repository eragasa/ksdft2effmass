# Prospective composite-band alignment and locality protocol

## Status

This is the publication-independent direct successor to the historical Conference Paper
1 `M2` protocol. It fixes the finite parent, retained state spaces, gauge action,
alignment objectives, Fourier convention, locality diagnostics, and numerical
qualification criteria. The result identity
`ksdft2effmass.periodic1d-rank2-composite-band-alignment-result.v2` distinguishes this
scientific record from the retired historical-byte contract. This protocol records no
new retained run or accepted scientific evidence.

The historical files and checksums under
`calculations/ICMSEP2026/conference/paper_1/multiband-alignment/` remain unchanged.

## Parent and state spaces

The selected parent is the exact finite four-dimensional Hermitian periodic-one-
dimensional block-hopping model retained by the historical protocol. At every declared
reciprocal point, the lowest two ordered eigenstates define the retained rank-two
spectral space. The protocol requires the retained/excluded finite-mesh gap to exceed
the declared energy threshold.

The ambient basis is the ordered four-state coefficient basis shown in the typed
configuration. Retained frames contain the lowest two ordered eigenvectors as columns;
unitaries act on their right. Energies and hopping blocks use the dimensionless reference
energy `E_ref`, the energy zero is the exact parent onsite convention, and reduced
momenta use reciprocal period one on the centered half-open interval. The direct
rank-first study context realizes this reduced convention with the explicit lattice
geometry $a_0=1\,\mathrm{bohr}$; this geometry supplies units and does not alter the
dimensionless scientific model. Operators are compared only after their state spaces
are explicitly aligned.

## Sample roles

- The centered half-open 64-point reciprocal mesh constructs frames, transformations,
  represented operators, Fourier blocks, and finite-range models.
- The disjoint 257-point staggered mesh evaluates already fixed finite-range models.
- Evaluation values cannot alter the parent, frames, attack, transformations, ranges,
  thresholds, or selected result fields.

The maintained schema must call the first role **objective construction** or
**construction**, not training; no statistical model is learned.

## Frame contract

The successor preserves backend-qualified eigenvector-diagonal frames selected from the
lowest two eigenpairs. It retains:

- numerical backend and version;
- ordered eigenvalues;
- input-Hermiticity and residual diagnostics;
- frame orthonormality;
- retained projector and retained/excluded boundary gap; and
- any translated backend failure.

The selected frames are not canonical across eigensolver backends. Within an exactly or
numerically degenerate retained cluster, their coordinates are backend-selected. A
projector-derived deterministic frame would be a different protocol and is not silently
substituted.

## Transport, attack, and alignment

1. Construct the reciprocal frame path with identity sewing.
2. Apply polar parallel transport and distribute the selected closure transformation.
3. Apply the known right-unitary rank-two rotation
   \[
   A(k)=\begin{pmatrix}\cos\theta(k)&-\sin\theta(k)\\
   \sin\theta(k)&\cos\theta(k)\end{pmatrix},
   \qquad
   \theta(k)=0.30+0.65\sin(2\pi k)+0.30\sin(4\pi k).
   \]
4. Select a distinct Procrustes transformation at every construction point.
5. Separately select one unitary from the equal-weight ordered aggregate covariance.

For both Procrustes families, the candidate acts on the right toward the reference.
Optimization combines absolute cutoff `1e-14` and relative cutoff `1e-12` using the
maximum rule. A covariance is full rank only when both singular values exceed the
applied cutoff. A rank-deficient covariance is rejected without returning a
transformation; no null-space completion is part of this protocol. Backend-validation
absolute tolerance is `1e-12` and relative tolerance is zero.

Pointwise and one-global-unitary alignment are different feasible families. Neither is
presented as an approximation to the other.

Let $R_j,C_j\in\mathbb C^{4\times2}$ denote the transported reference and attacked
frames at construction point $j$, and define the cross covariance

\[
X_j=C_j^\dagger R_j.
\]

The pointwise problem is

\[
U_j=\arg\min_{U\in U(2)}\frac{1}{2}\lVert C_jU-R_j\rVert_F^2,
\]

while the global problem constrains all points to one unitary,

\[
U_{\mathrm g}=\arg\min_{U\in U(2)}
\frac{1}{2}\sum_{j=1}^{64}\lVert C_jU-R_j\rVert_F^2,
\qquad
X_{\mathrm g}=\sum_{j=1}^{64}X_j.
\]

For a full-rank covariance $X$, the unique minimizer is its right polar factor

\[
\mathcal P(X)=X(X^\dagger X)^{-1/2}.
\]

A complete complex SVD may be used to evaluate this polar factor, but its individual
left and right singular-vector bases are nonunique when singular values repeat. Those
bases are therefore neither physical quantities nor reproducibility targets. The
scientific evidence consists of the selected polar factor together with the singular
values $\sigma_1\geq\sigma_2$, numerical rank, cutoff $\tau$, strict margin
$\sigma_2-\tau$, condition number $\sigma_1/\sigma_2$, and the normalized objective.

For every admitted selection, also evaluate

\[
\varepsilon_{\mathrm{unit}}=\lVert U^\dagger U-I_2\rVert_F,
\qquad
\varepsilon_{\mathrm{stat}}=
\frac{\lVert U^\dagger X-X^\dagger U\rVert_F}{\sqrt2},
\]

\[
\varepsilon_{\mathrm{obj}}=
\left|J_{\mathrm{direct}}-J_{\mathrm{cov}}\right|,
\qquad
\varepsilon_{\mathrm{psd}}=
\max\!\left\{0,-\lambda_{\min}\!\left(
\frac{U^\dagger X+X^\dagger U}{2}
\right)\right\}.
\]

The pointwise family retains the maximum and root-mean-square normalized objectives over
all 64 points; the global family retains the corresponding one-selection values.
Backend identity is retained only to disclose the numerical realization of these
finite-dimensional quantities.

## Represented operators and locality

Represent the parent Hamiltonian in transported-reference, attacked, pointwise-aligned,
and globally aligned frames. Fourier-transform the transported-reference, attacked, and
pointwise-aligned represented paths using the declared finite positive-exponent
convention. Retain complete block families and reconstruct each source path before
truncation.

Convert each even cyclic transform to an ordinary integer-lattice inventory before
range truncation. Remove only the negative Nyquist representative `-32` and report its
normalized conversion power

\[
P_{c,\mathrm{Nyq}}=\frac{\lVert t_{c,-32}\rVert_F^2}{2E_\mathrm{ref}^2}.
\]

This conversion power is not an off-node spectral error and is not silently pooled with
ordinary support deletion. The complete ordinary inventory is `-31, …, 31`.

On the disjoint evaluation mesh, let `h_c^ord` be the complete ordinary interpolant,
`h_c^(R)` its symmetric range truncation, and `h_c^dir` the directly evaluated channel
field. The reference and pointwise direct fields are the complete ordinary reference
field. The attacked direct field is obtained by applying the declared analytic attack to
that reference field at each evaluation point. Report separately:

- interpolation: `h_c^ord - h_c^dir`;
- deliberate truncation: `h_c^(R) - h_c^ord`; and
- total consequence: `h_c^(R) - h_c^dir`.

Each channel retains the maximum normalized Frobenius residual
`||Δh||_F / (sqrt(2) E_ref)` and the maximum sorted two-band residual. These maxima are
not added as independent scalar errors; only the corresponding pointwise triangle
inequality is available.

Apply symmetric hopping ranges `0, 1, 2, 3, 4, 6, 8`. For each range and channel,
retain the ordinary omitted-block L2 norm, construction total spectral error, and the
disjoint-evaluation truncation and total Hamiltonian and spectral errors. Locality,
conversion, interpolation, and truncation are frame-dependent diagnostics, not
invariant physical observables.

## Independent verification

The independent reference reconstructs the parent Hamiltonians, transported frames,
analytic attack, alignment covariances, represented operators, Fourier blocks,
cyclic-to-ordinary conversion, evaluation fields, and every truncation channel from the
fixed mathematical definitions above.

For pointwise alignment, the analytic relation $C_j=R_jA_j$ gives
$X_j=A_j^\dagger$ up to floating-point roundoff, so the reference uses the cross
covariance directly rather than an SVD. For global alignment, it constructs

\[
\mathcal P(X_{\mathrm g})=
X_{\mathrm g}(X_{\mathrm g}^\dagger X_{\mathrm g})^{-1/2}
\]

from an Hermitian eigendecomposition of $X_{\mathrm g}^\dagger X_{\mathrm g}$. It then
recomputes the singular values, rank decisions, margins, condition numbers, normalized
objectives, and all four integrity defects from the original frames. Array-valued
comparisons use absolute tolerance $10^{-10}$ and scalar summaries use $10^{-11}$.

These tolerances define numerical reproducibility. Exact serialized bytes serve only to
identify one admitted artifact; they are not a claim that separate BLAS/LAPACK
executions must follow identical rounding paths. A fresh calculation is scientifically
admissible only when the full-rank conditions, integrity defects, independent alignment
references, Fourier reconstruction, and separated error-channel checks pass.

## Evidence status and claim boundary

The v2 identity does not reinterpret or replace historical M2 or monograph artifacts;
those remain bound to their own archived bytes and conventions. No retained v2 execution
is authorized by this protocol alone. Retention requires separate review of the finite
numerical results and explicit execution authorization.

Passing the declared checks establishes consistency for this finite four-state,
rank-two, sampled model. It does not establish continuum convergence, material validity,
uncertainty bounds, a preferred physical gauge, or publication acceptance.
