# Controlled one-dimensional isolated-band protocol

## Evidence boundary

This protocol governs the prospective isolated-band calculation for ICMSEP 2026
Conference Paper 1. It is a controlled illustrative numerical-verification calculation
for a synthetic scalar periodic Hamiltonian. It is not a material calculation, silicon
validation, uncertainty quantification, or evidence of transferability. It does not
execute Quantum ESPRESSO, Wannier90, VASP, ABINIT, a scheduler, or remote compute.

`input.json` freezes the model, sampling roles, representation sequences, hopping
ranges, tolerances, scope, and figure identity before confirmatory evaluation.

## Parent model and conventions

The dimensionless parent is

$$
H(k)=-\frac{d^2}{dx^2}+0.5\cos x,
\qquad a=2\pi,\quad G=1,\quad E_G=1.
$$

Reduced momentum $k/G$ lies in $[-1/2,1/2]$. Plane-wave indices are ordered integer
translations from $-P$ through $P$. The energy zero is the model's declared zero; no
post-calculation energy shift is fitted. All retained quantities in this package are
dimensionless multiples of the declared scales.

The plane-wave cutoff-$15$ spectrum is the finite represented reference for the parent
refinement study. It is not asserted to be the exact continuum spectrum. The production
lowest-band samples use cutoff 11. Plane-wave and finite-difference errors remain
separate discretization channels.

## Parent refinement

At reduced momenta

$$
-\tfrac12,-\tfrac14,0,\tfrac14,\tfrac12,
$$

the lowest three ordered eigenvalues are compared against the cutoff-15 plane-wave
reference. The declared plane-wave cutoffs are 3, 5, 7, 9, and 11. The declared
centered finite-difference point counts are 31, 63, 127, and 255.

The calculation reports maximum absolute eigenvalue error for each representation. No
monotonicity or acceptance threshold is imposed, so the package may describe observed
refinement but may not declare continuum convergence solely from these values.

## Training and withheld roles

The training set is the complete centered half-open 64-point reciprocal mesh used by
the discrete Fourier transform and equal-weight direct fits.

For training extent $N=64$ and withheld extent $M=257$, withheld point $i$ is

$$
k_i/G=-\frac12+\frac{i+1/(N+1)}{M},\qquad i=0,\ldots,M-1.
$$

This frozen staggered uniform mesh is disjoint from the training mesh. Withheld values
are evaluation-only. They cannot change Fourier coefficients, direct fits, hopping
ranges, tolerances, figures' data selection, or any later disposition.

## Complete and finite-range hopping routes

The complete scalar hoppings are

$$
t_R=\frac1N\sum_{j=0}^{N-1}
  e^{-2\pi iRk_j/G}E(k_j),
$$

using the centered Born--von Karman representatives supplied by the maintained
64-point mesh. Inverse interpolation must reproduce every training sample within the
frozen reconstruction tolerance.

For each range $R_{\max}\in\{0,1,2,3,4,6,8\}$, the mediated route retains complete
coefficients satisfying $|R|\leq R_{\max}$. The direct route performs an equal-weight
complex least-squares fit on the same training mesh using exactly the same
representatives. Primary and alternative routes are compared but never averaged.

Each range retains:

- omitted hopping-block norm;
- training maximum absolute band error;
- withheld maximum absolute band error;
- Parseval residual;
- direct-fit rank and condition number;
- coefficient and sampled direct-versus-mediated defects;
- bandwidth and zone-center curvature; and
- maximum imaginary residual.

## Numerical-consistency conditions

The frozen absolute tolerances are $10^{-12}$ in the applicable dimensionless energy
or squared-energy scale, except for the coordinate check at $10^{-14}$. These are
binary64 numerical-consistency tolerances, not scientific uncertainty or confidence
levels.

The producer must stop before retaining a result if its maintained independent
in-memory verifier fails. The retained verifier must then reconstruct the result from
`input.json` and `result.json` without importing `run.py`. It must independently
rebuild parent matrices, spectra, Fourier coefficients, truncations, direct fits,
route defects, Hermiticity, Parseval quantities, and band-shape diagnostics.

A passing retained verifier establishes only consistency with this frozen finite
protocol. It does not select a preferred hopping range or establish scientific
acceptance for another application.

## Explicit exclusions

This package does not recalculate the historical Mathieu, common-low-mode,
weak-potential, or stress channels. Those remain separate historical evidence and must
not be silently attributed to this result. It also excludes multiband alignment,
nonidentity gauge families, localization, topology, two-dimensional shells, material
parameters, and protected electronic-structure execution.

## Retention and manuscript use

`result.json` uses
`ksdft2effmass.periodic1d.isolated-band-calculation-result.v1`; it does not reuse the
historical Appendix G wire identity. Figures must be generated from retained result
data. `SHA256SUMS` will bind the frozen input, protocol, software record, result,
verification, report, scripts, figure data, and figure.

Numerical statements may enter Conference Paper 1 only after independent verification
passes and the manuscript identifies this bounded evidence class and its exclusions.
