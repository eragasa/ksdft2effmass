# Periodic-3D rank-two Bain-path research protocol

This file is the authoritative research protocol for the unit-primitive-volume
periodic-3D rank-two Bain path. It owns the scientific question, common-cell map, fixed
M0/M1/M2 controls, sampled scan rules, diagnostics, and interpretation boundary.

## Scientific question

With the parent operator, onsite terms, hopping coefficients, retained rank, energy
reference, and reduced-coordinate gauge fixed, how does homogeneous deformation along
the declared Bain path change the physical real-space range required to meet a declared
fidelity tolerance?

This is a synthetic gauge and metric stress test. It is not an elastic,
structural-stability, martensitic-transition, silicon, or material-strain calculation.

## Path and common-cell convention

The path is the unit-primitive-volume Bain deformation in a common body-centered
Tetragonal primitive basis, with `c/a` varying from `sqrt(2)` to `1`. The endpoints are
FCC and BCC metric representations; the path does not identify a material phase
transition.

At the FCC endpoint, let $\mathbf n_F$ denote the FCC primitive coordinate and
$\mathbf n_B$ the Bain coordinate. The fixed map is

\[
 \mathbf n_F=U\mathbf n_B,\qquad
 U=\begin{pmatrix}1&1&0\\0&0&1\\0&-1&0\end{pmatrix},
 \qquad \det U=1.
\]

It induces $\mathbf q_B=U^\mathsf{T}\mathbf q_F$ on the reciprocal torus and the finite
cell permutation $\mathbf n_B\mapsto U\mathbf n_B\pmod N$. The FCC diamond offset
$(1/4,1/4,1/4)_F$ becomes $(1/2,-1/4,1/4)_B$; orbital and sublattice labels are otherwise
unchanged. The endpoint metrics obey $G_B=U^\mathsf{T}G_FU$, and the six FCC bond pairs
map to the six Bain-coordinate bond pairs used by M0. These identities establish the
coordinate and state-space map only; they do not identify a material model.

## Scientific controls

1. **Geometry-only flat-parent control (M0):** a constant rank-two parent and imposed
   smooth gauge. This control has exact band equivalence, zero covariant residual, and
   strain-invariant Fourier coefficients.
2. **Frozen-parent null-response control (M1):** fixed onsite and hopping matrices with
   the seed-projected retained-frame construction and the declared common-cell map.
3. **Synthetic radial-response control (M2):** the same parent and onsite matrices, with
   only inter-sublattice bond amplitudes changed by
   \[
   t_j(s)=t_j(0)\exp\!\left[-\beta\left(\frac{d_j(s)}{d_j(0)}-1\right)\right],
   \qquad \beta=1.
   \]
   No path-dependent refit, normalization, onsite response, or averaging with M0 or M1
   is permitted.

The controls remain distinct scientific channels. The aggregate actions may sequence
them but must not merge their outcomes or evidence claims.

## Frozen bounded controls

The bounded baseline uses nine fractions $s\in\{0,1/8,\ldots,1\}$, maximum imposed gauge
angle $a=\pi/4$, and tail-power tolerances $10^{-3}$ and $10^{-5}$. M0 uses a `24 x 24 x
24` construction mesh. M1 and M2 use an `8 x 8 x 8` construction mesh and a separately
shifted `17 x 17 x 17` evaluation mesh with shift `1/3`. The response controls fix parent
scale $\rho=1$, keep onsite matrices and $E_{\mathrm{ref}}$ unchanged, and apply the same
imposed reduced-coordinate gauge at every path fraction.

These are bounded development controls, not convergence ladders. Their maintained
actions are [`run_geometry_control.py`](run_geometry_control.py) and
[`run_response_controls.py`](run_response_controls.py).

## Bounded path scan and transition rules

The replaceable scan uses the frozen base grid

\[
 \widehat S_0=\{s_i=i/200:i=0,\ldots,200\}.
\]

A hat denotes a maximum over the reported finite sample and never a supremum over the
continuous path. [`run_path_scan.py`](run_path_scan.py) locates candidate extrema and
transition brackets; it is not a continuum proof. It bisects adjacent base-grid
intervals whose endpoint first-passing block counts or bond-degeneracy counts differ.
Five bisection levels reduce a detected base interval of width at most `1/200` to a
bracket of width at most `1/6400`.

This rule refines only transitions visible from differing adjacent endpoint values and
cannot exclude an even number of hidden changes inside an equal-endpoint interval.
Sampled maxima retain their sample locations. Boundary maxima require no extrapolation.
Any future interior-maximum refinement requires a separately frozen rule. A feasibility
crossing cannot be defined until family-specific spectral and operator limits are
independently justified and frozen.

At each sampled fraction, let $\kappa_i$ be the retained splitting scale and $\mu_i$ the
maximum finite-mesh correlation after one optimized global real rotation. The pointwise
optimized operator requirement is

\[
 \tau_{o,\min}(s_i)=\sqrt{\kappa_i[1-\max(0,\mu_i)^2]}.
\]

For the unchanged reference candidate $p_0=(s,\lambda)=(0,1)$,

\[
 \tau_{o,p_0}(s_i)=\sqrt{2\kappa_i(1-\mu_i)}.
\]

The sampled envelopes are the maxima of these quantities over $\widehat S_0$. A
pointwise optimized candidate is not one common path witness. The constant $p_0$ is a
prescribed candidate path, not a scientific witness until frozen limits establish its
feasibility at every required fraction. A uniform continuum witness additionally
requires certified bounds between samples.

The locality summaries

\[
 \widehat R_\varepsilon=\max_i R_\varepsilon(s_i),\qquad
 \widehat N_\varepsilon=\max_i N_\varepsilon(s_i)
\]

remain separate. Their maxima need not occur at the same fraction as either operator
requirement. Shell indices are never transferred between metrics without physical radii
and complete conjugate-closed block inventories.

## Diagnostics and gates

At every path fraction report the unit-determinant metric, bond-length extrema and orbit
splitting, covariant and restricted alignment meanings, ordinary and centered-Nyquist
Fourier power, and the first complete physical-radius cutoff meeting each tail-power
tolerance. Equal-radius ties must not be split.

The scan additionally reports fixed-$p_0$ and pointwise optimized operator requirements,
finite-mesh correlation, splitting scale, direct sorted-band defect, and sampled
envelopes. M1 and M2 report maximum and RMS matrix and sorted-band errors in separate
withheld-interpolation, deliberate-truncation, and total-error channels. Apply the same
decomposition separately to the pointwise gauge-aligned path difference $\Delta H_s$.
The channels are not added.

A failed determinant, common-cell, Parseval, Hermiticity, Nyquist, state-space, gap,
frame, sewing, resource, schema, or refinement gate remains `unresolved`. Frozen
baseline parameters and base samples must not be changed after observing results.
Adaptive points must follow the declared transition rules and remain separate from the
201-point base grid. Typed canonical records establish source-bound software behavior
only; independent evidence review and separate authorization remain required before any
retained execution.

## Interpretation boundary

M0 can show how a fixed gauge's unchanged Fourier weight is reassigned to physical radii
along the declared unit-volume metric path. It cannot establish forces, stresses, strain
energy, phase stability, a martensitic transition, realistic silicon, or any material
response. The cost of fidelity is reported through the first physical hopping radius and
retained block count at each declared tolerance.

The calculation-owned shared donor protocol is
[`calculations/periodic/multiband/gauge-locality-under-synthetic-strain.md`](../../periodic/multiband/gauge-locality-under-synthetic-strain.md).
The neighboring [technical report](technical-report/technical-report.md) records current
replaceable observations without promoting them to retained evidence.
