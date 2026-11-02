# Periodic-2D rank-two rhombic-path research protocol

This file is the authoritative research protocol for the unit-area periodic-2D
rank-two rhombic path. It owns the scientific question, fixed controls, sampled scan
rules, diagnostics, and interpretation boundary for the neighboring calculation
actions.

## Scientific question

With the parent operator, onsite terms, hopping coefficients, retained rank, energy
reference, and reduced-coordinate gauge fixed, how does homogeneous deformation along
the declared rhombic path change the physical real-space range required to meet a
declared fidelity tolerance?

This is a synthetic gauge and metric stress test. It is not an elastic,
structural-stability, phase-stability, graphene, or material-strain calculation.

## Geometry and state-space convention

The path is the unit-area rhombic deformation

\[
 A_2(\theta)=\frac{1}{\sqrt{\sin\theta}}
 \begin{pmatrix}1&\cos\theta\\0&\sin\theta\end{pmatrix},\qquad
 \theta:\pi/3\to\pi/2.
\]

The endpoints are triangular and square metrics represented in one declared reduced
coordinate convention. The square endpoint retains the strained three-bond orbit; it is
not the square directed-hopping parent of the orthogonal family. Compared operators must
share an identified represented state space, basis, gauge, energy unit, and energy
reference before subtraction.

## Scientific controls

1. **Geometry-only flat-parent control (M0):** a constant rank-two parent and imposed
   smooth gauge. This control has exact band equivalence, zero covariant residual, and
   strain-invariant Fourier coefficients.
2. **Frozen-parent null-response control (M1):** fixed onsite and hopping matrices with
   the seed-projected retained-frame construction and explicit common-state-space map.
3. **Synthetic radial-response control (M2):** the same parent and onsite matrices, with
   only the inter-sublattice bond amplitudes changed by
   \[
   t_j(s)=t_j(0)\exp\!\left[-\beta\left(\frac{d_j(s)}{d_j(0)}-1\right)\right],
   \qquad \beta=1.
   \]
   No strain-dependent refit, normalization, onsite response, or averaging with the M0
   or M1 controls is permitted.

The three controls remain separate scientific channels. The aggregate actions may
sequence them but must not merge their outcomes or evidence claims.

## Frozen bounded controls

The bounded baseline uses nine prospectively selected fractions
\(s\in\{0,1/8,\ldots,1\}\), maximum imposed gauge angle \(a=\pi/4\), and tail-power
tolerances \(10^{-3}\) and \(10^{-5}\). M0 uses a `64 x 64` construction mesh. M1 and
M2 use a `16 x 16` construction mesh and a separately shifted `33 x 33` evaluation
mesh with shift `1/3`. The response controls fix parent scale \(\rho=1\), keep onsite
matrices and \(E_{\mathrm{ref}}\) unchanged, and apply the same imposed
reduced-coordinate gauge at every path fraction.

These are bounded development controls, not convergence ladders. Their maintained
actions are [`run_geometry_control.py`](run_geometry_control.py) and
[`run_response_controls.py`](run_response_controls.py).

## Bounded path scan and transition rules

The replaceable scan uses the frozen base grid

\[
 \widehat S_0=\{s_i=i/200:i=0,\ldots,200\}.
\]

A hat denotes a maximum over the reported finite sample and never a supremum over the
continuous path. The scan locates candidate extrema and transition brackets; it is not a
continuum proof. [`run_path_scan.py`](run_path_scan.py) bisects every adjacent base-grid
interval whose endpoint first-passing block counts or bond-degeneracy counts differ.
Five bisection levels reduce a detected base interval of width at most `1/200` to a
bracket of width at most `1/6400`.

This procedure refines only transitions visible from differing adjacent endpoint values;
it cannot exclude an even number of hidden changes inside an equal-endpoint interval.
Sampled maxima retain their sample locations. Boundary maxima require no extrapolation.
Any future interior-maximum refinement requires a separately frozen rule. The five-level
choice is replaceable development policy, not a retained protocol freeze. A feasibility
crossing cannot be defined or refined until family-specific spectral and operator limits
are independently justified and frozen.

At each sampled fraction, let \(\kappa_i\) be the retained splitting scale and \(\mu_i\)
the maximum finite-mesh correlation after one optimized global real rotation. The
pointwise optimized operator requirement is

\[
 \tau_{o,\min}(s_i)=\sqrt{\kappa_i[1-\max(0,\mu_i)^2]}.
\]

The unchanged reference candidate is \(p_0=(s,\lambda)=(0,1)\), with operator
requirement

\[
 \tau_{o,p_0}(s_i)=\sqrt{2\kappa_i(1-\mu_i)}.
\]

The sampled envelopes are

\[
 \widehat\tau_{o,\min}=\max_{s_i\in\widehat S_0}\tau_{o,\min}(s_i),\qquad
 \widehat\tau_{o,p_0}=\max_{s_i\in\widehat S_0}\tau_{o,p_0}(s_i).
\]

An independently optimized candidate at each sample is a pointwise diagnostic, not one
common path witness. The constant parameter choice \(p_0\) is a prescribed candidate
path, not a scientific witness until frozen limits establish feasibility at every
required fraction. A uniform continuum witness would additionally require certified
bounds between samples.

The locality summaries remain separate:

\[
 \widehat R_\varepsilon=\max_i R_\varepsilon(s_i),\qquad
 \widehat N_\varepsilon=\max_i N_\varepsilon(s_i).
\]

Their maxima need not occur at the same fraction as either operator-requirement maximum.
Shell indices are never transferred between metrics without their physical radii and
complete conjugate-closed block inventories.

## Diagnostics and gates

At every path fraction report the unit-determinant metric, bond-length extrema and orbit
splitting, covariant and restricted alignment meanings, ordinary and centered-Nyquist
Fourier power, and the first complete physical-radius cutoff meeting each tail-power
tolerance. Equal-radius ties must not be split.

The scan additionally reports the fixed-\(p_0\) and pointwise optimized operator
requirements, finite-mesh correlation, splitting scale, direct sorted-band defect, and
sampled envelopes. M1 and M2 report maximum and RMS matrix and sorted-band errors in
three separate channels: withheld interpolation, deliberate truncation relative to the
full interpolant, and total error relative to the direct withheld field. Apply the same
decomposition separately to the pointwise gauge-aligned path difference \(\Delta H_s\).
The three channels are not added.

A failed determinant, Parseval, Hermiticity, Nyquist, state-space, gap, frame, sewing,
resource, schema, or refinement gate remains `unresolved`. Frozen baseline parameters
and base samples must not be changed after observing results. Adaptive points must be
selected by the declared transition rules and reported separately from the 201-point
base grid. Typed canonical source, request, result, and verification documents establish
source-bound software behavior only; independent evidence review and separate
authorization remain required before any retained execution.

## Literature and interpretation boundary

Wannier-gauge and localization background follows Marzari *et al.*
([DOI](https://doi.org/10.1103/RevModPhys.84.1419)) and Mostofi *et al.*
([DOI](https://doi.org/10.1016/j.cpc.2007.11.016)). Compact support is a distinct
algebraic question; see Sathe and Roy
([DOI](https://doi.org/10.1103/PhysRevB.109.155150)). Material-specific strained
hexagonal Hamiltonians and environment-responsive mappings do not make the present
fixed-parent and prescribed-response controls material models.

M0 can show how a fixed gauge's unchanged Fourier weight is reassigned to physical radii
under the declared metric path. It cannot establish forces, stresses, strain energy,
phase stability, realistic graphene, or any material transition. The cost of fidelity is
reported through the first physical hopping radius and retained block count at each
declared tolerance.

The neighboring [technical report](technical-report/technical-report.md) records current
replaceable observations without promoting them to retained evidence.
