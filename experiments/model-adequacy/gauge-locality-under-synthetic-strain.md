# Gauge-locality cost under synthetic finite strain

## Scientific question

With the parent operator, onsite terms, hopping coefficients, retained rank, energy
reference, and reduced-coordinate gauge fixed, how does homogeneous strain change the
physical real-space range required to meet a declared fidelity tolerance?

This is a synthetic gauge stress test. It is not an elastic, structural-stability, or
material-strain calculation.

## Scientific controls

1. **Geometry-only flat-parent control:** a constant rank-two parent and imposed smooth
   gauge. This control has exact band equivalence, zero covariant residual, and
   strain-invariant Fourier coefficients.
2. **Frozen-parent null-response control:** fixed onsite and hopping matrices with the
   existing seed-projected retained-frame construction and the explicit common-cell map.
3. **Synthetic radial-response control:** the same parent and onsite matrices, with only
   the inter-sublattice bond amplitudes changed by the prospectively fixed law
   \[
   t_j(s)=t_j(0)\exp\!\left[-\beta\left(\frac{d_j(s)}{d_j(0)}-1\right)\right],
   \qquad \beta=1.
   \]
   No strain-dependent refit, normalization, onsite response, or averaging with the
   geometry-only or frozen-parent controls is permitted.

The geometry-only calculation is the primary metric control. The frozen-parent and
radial-response calculations are separately labeled bounded synthetic development
controls; none is retained or material evidence.

## Paths

PhysKit owns reusable crystallographic path, fractional-basis, and coordinate-bridge
mechanics. The formulas below freeze the current KSD donor definitions used by this
replaceable campaign while the corresponding PhysKit contracts remain under separate
review. They must not be expanded into competing KSD geometry APIs or migrated without
a reviewed compatible PhysKit checkpoint and consumer plan.

The 2-D path is the unit-area rhombic deformation

\[
 A_2(\theta)=\frac{1}{\sqrt{\sin\theta}}
 \begin{pmatrix}1&\cos\theta\\0&\sin\theta\end{pmatrix},\qquad
 \theta:\pi/3\to\pi/2.
\]

The 3-D path is the unit-primitive-volume Bain deformation in a common body-centered
tetragonal primitive basis, with \(c/a:\sqrt2\to1\). The endpoints are FCC and BCC
representations.

### 3-D common-cell map

At the FCC endpoint, let \(\mathbf n_F\) denote the existing FCC primitive coordinate
and \(\mathbf n_B\) the Bain/BCT coordinate. The prospectively fixed map is

\[
 \mathbf n_F=U\mathbf n_B,\qquad
 U=\begin{pmatrix}1&1&0\\0&0&1\\0&-1&0\end{pmatrix},
 \qquad \det U=1.
\]

It induces \(\mathbf q_B=U^\mathsf{T}\mathbf q_F\) on the reciprocal torus and a cell
permutation \(\mathbf n_B\mapsto U\mathbf n_B\pmod N\) on every finite periodic mesh.
The existing diamond offset \((1/4,1/4,1/4)_F\) becomes
\((1/2,-1/4,1/4)_B\); orbital and sublattice labels are otherwise unchanged. The
unit-volume endpoint metrics obey \(G_B=U^\mathsf{T}G_FU\), and the six FCC bond pairs
map exactly to the six Bain-coordinate bond pairs used by the geometry-only control.
Software verification checks the metric, offset, bond, determinant, and finite-cell
bijection identities. This resolves the coordinate/state-space map only. The bounded
frozen-parent and radial-response actions remain synthetic controls and do not turn that
coordinate identity into a material-model identification.

## Frozen baseline controls

The initial construction uses nine prospectively selected strain fractions
\(s\in\{0,1/8,\ldots,1\}\), maximum gauge angle \(a=\pi/4\), and tail-power tolerances
\(10^{-3}\) and \(10^{-5}\). The geometry-only development transform uses \(64^2\)
points in 2-D and \(24^3\) points in 3-D. The initial frozen-parent and radial-response
smoke actions use construction/evaluation sizes \(16^2/33^2\) in 2-D and
\(8^3/17^3\) in 3-D, with evaluation shift \(1/3\). These are smoke controls, not
convergence ladders. Both response actions fix parent scale \(\rho=1\), keep onsite
matrices and \(E_{\mathrm{ref}}\) unchanged, and apply the same imposed
reduced-coordinate gauge at every strain.

## Bounded strain scan and candidate hierarchy

The replaceable development scan uses the frozen base grid
\[
 \widehat S_0=\{s_i=i/200:i=0,\ldots,200\}.
\]
A hat denotes a maximum over the reported finite sample and never a supremum over the
continuous path. The scan is intended to locate candidate extrema and transition
brackets; it is not a continuum proof. The current replaceable development action
bisects every adjacent base-grid interval whose endpoint first-passing block counts or
bond-degeneracy counts differ. Five bisection levels reduce a detected base interval of
width at most \(1/200\) to brackets of width at most \(1/6400\). This procedure refines
only transitions visible from differing adjacent endpoint values; it cannot exclude an
even number of hidden changes inside an equal-endpoint interval. Sampled maxima are
reported with their sample locations. Boundary maxima require no extrapolation, while
any later interior-maximum refinement must use a separately frozen rule. The five-level
choice was introduced during replaceable development and is not a retained protocol
freeze. A feasibility crossing cannot be defined or refined until the family-specific
spectral and operator limits are independently justified and frozen.

At each sampled strain, let \(\kappa_i\) be the retained splitting scale and
\(\mu_i\) the maximum finite-mesh correlation after one optimized global real rotation.
The pointwise optimized operator requirement is
\[
 \tau_{o,\min}(s_i)
 =\sqrt{\kappa_i[1-\max(0,\mu_i)^2]}.
\]
The unchanged reference candidate is \(p_0=(s,\lambda)=(0,1)\), which has zero sorted-band
loss for the exactly band-equivalent pair at each strain. Its operator requirement is
\[
 \tau_{o,p_0}(s_i)=\sqrt{2\kappa_i(1-\mu_i)}.
\]
The two sampled envelopes are therefore
\[
 \widehat\tau_{o,\min}=\max_{s_i\in\widehat S_0}\tau_{o,\min}(s_i),
 \qquad
 \widehat\tau_{o,p_0}=\max_{s_i\in\widehat S_0}\tau_{o,p_0}(s_i).
\]
An independently optimized candidate at each \(s_i\) is a pointwise diagnostic, not one
common path witness. The constant parameter choice \(p_0\) is a prescribed candidate
path, not a scientific witness until frozen limits establish its feasibility at every
required strain. A uniform continuum witness would additionally require certified
bounds between samples.

The locality summaries remain separate:
\[
 \widehat R_\varepsilon=\max_i R_\varepsilon(s_i),\qquad
 \widehat N_\varepsilon=\max_i N_\varepsilon(s_i).
\]
Their maxima need not occur at the same strain as either operator-requirement maximum,
and shell indices are never transferred between metrics without their physical radii
and complete block inventories.

## Diagnostics

At every strain point report the unit-determinant metric, bond-length extrema and orbit
splitting, covariant and restricted alignment meanings, ordinary and centered-Nyquist
Fourier power, and the first complete physical-radius cutoff meeting each tail-power
tolerance. Equal-radius ties must not be split. The 201-point scan additionally reports
the fixed-\(p_0\) and pointwise optimized operator requirements, finite-mesh correlation,
splitting scale, direct sorted-band defect, and sampled envelopes defined above. For the
frozen-parent and radial-response controls, report maximum and RMS matrix and sorted-band
errors in three separate channels: withheld interpolation, deliberate truncation
relative to the full interpolant, and total error relative to the direct withheld field.
Apply the same decomposition separately to the pointwise gauge-aligned strain difference
\(\Delta H_s\). The three channels are not added.

## Gates

A failed determinant, Parseval, Hermiticity, Nyquist, state-space, gap, frame, sewing,
resource, schema, or refinement gate remains `unresolved`. Frozen baseline parameters
and strain samples must not be changed after observing results. Any adaptive scan points
must be selected by the prospective transition rules above and reported separately from
the 201-point base grid. Strict packaged result schemas for all three controls now
qualify the replaceable baseline wire shape; the scan records and renderer remain
unretained development surfaces. Typed canonical source, request, result, and verification
documents now bind exact SHA-256 identities and environment identifiers, and the
artifact-reading verifier reconstructs the development grid, extrema, envelopes, and
transition brackets. These capabilities establish source-bound software behavior only;
frozen resource gates, independent evidence review, and separate authorization remain
required before any retained execution.

## Related literature and boundary

The Wannier-gauge and localization background follows the review by Marzari *et al.*
([DOI](https://doi.org/10.1103/RevModPhys.84.1419)) and the Wannier90 construction of
Mostofi *et al.* ([DOI](https://doi.org/10.1016/j.cpc.2007.11.016)). Compact support is
a distinct algebraic question; see Sathe and Roy
([DOI](https://doi.org/10.1103/PhysRevB.109.155150)). Material-specific strained
hexagonal Hamiltonians have been constructed by Fang *et al.*
([DOI](https://doi.org/10.1103/PhysRevB.98.075106)), and environment-responsive
Hamiltonian mappings by Zhang *et al.*
([DOI](https://doi.org/10.1038/s41524-022-00843-2)). The 3-D path uses the geometric
Bain deformation named for Bain's original martensite construction
([source](https://onemine.org/documents/the-nature-of-martensite)). None of these
references makes the present frozen-potential control a material model.

## Interpretation

The geometry-only control can show how a fixed gauge's unchanged Fourier weight is
reassigned to physical radii under extreme deformation. It cannot establish forces, stresses, strain energy,
phase stability, realistic graphene, realistic silicon, or a material FCC--BCC
transition. The cost of fidelity is summarized by the first physical hopping radius and
retained block count at each declared tolerance.
