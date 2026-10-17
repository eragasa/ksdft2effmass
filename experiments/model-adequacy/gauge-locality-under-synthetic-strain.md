# Gauge-locality cost under synthetic finite strain

## Scientific question

With the parent operator, onsite terms, hopping coefficients, retained rank, energy
reference, and reduced-coordinate gauge fixed, how does homogeneous strain change the
physical real-space range required to meet a declared fidelity tolerance?

This is a synthetic gauge stress test. It is not an elastic, structural-stability, or
material-strain calculation.

## Model stages

1. **M0 flat-parent gauge control:** a constant rank-two parent and imposed smooth gauge.
   This stage has exact band equivalence, zero covariant residual, and strain-invariant
   Fourier coefficients.
2. **M1 frozen four-state bipartite parent:** fixed onsite and hopping matrices with the
   existing seed-projected retained-frame construction and the explicit common-cell map.
3. **M2 radial-response robustness control:** the same parent and onsite matrices, with
   only the inter-sublattice bond amplitudes changed by the prospectively fixed law
   \[
   t_j(s)=t_j(0)\exp\!\left[-\beta\left(\frac{d_j(s)}{d_j(0)}-1\right)\right],
   \qquad \beta=1.
   \]
   No strain-dependent refit, normalization, onsite response, or averaging with M0/M1
   is permitted.

M0 is the primary geometry control. M1 and M2 are separately labeled bounded synthetic
development controls; none is retained or material evidence.

## Paths

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
map exactly to the six Bain-coordinate bond pairs used by M0. Software verification
checks the metric, offset, bond, determinant, and finite-cell bijection identities.
This resolves the coordinate/state-space map only. The bounded M1/M2 actions remain
synthetic controls and do not turn that coordinate identity into a material-model
identification.

## Frozen controls

The construction uses nine prospectively selected strain fractions
\(s\in\{0,1/8,\ldots,1\}\), maximum gauge angle \(a=\pi/4\), and tail-power tolerances
\(10^{-3}\) and \(10^{-5}\). The M0 development transform uses \(64^2\) points in 2-D
and \(24^3\) points in 3-D. The initial M1/M2 smoke actions use construction/evaluation
sizes \(16^2/33^2\) in 2-D and \(8^3/17^3\) in 3-D, with evaluation shift \(1/3\).
These are smoke controls, not convergence ladders. M1/M2 fix parent scale \(\rho=1\),
keep onsite matrices and \(E_{\mathrm{ref}}\) unchanged, and apply the same imposed
reduced-coordinate gauge at every strain.

## Diagnostics

At every strain point report the unit-determinant metric, bond-length extrema and orbit
splitting, covariant and restricted alignment meanings, ordinary and centered-Nyquist
Fourier power, and the first complete physical-radius cutoff meeting each tail-power
tolerance. Equal-radius ties must not be split. For M1/M2, report maximum and RMS matrix
and sorted-band errors in three separate channels: withheld interpolation, deliberate
truncation relative to the full interpolant, and total error relative to the direct
withheld field. Apply the same decomposition separately to the pointwise gauge-aligned
strain difference \(\Delta H_s\). The three channels are not added.

## Gates

A failed determinant, Parseval, Hermiticity, Nyquist, state-space, gap, frame, sewing,
resource, schema, or refinement gate remains `unresolved`. Parameters and strain samples
must not be changed after observing results. Strict packaged M0/M1/M2 result schemas now
qualify the replaceable development wire shape. Typed canonical inputs, exact
request/result binding, verification schemas, environment provenance, independent
artifact-reading verification, and separate authorization remain required before any
retained execution.

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

M0 can show how a fixed gauge's unchanged Fourier weight is reassigned to physical
radii under extreme deformation. It cannot establish forces, stresses, strain energy,
phase stability, realistic graphene, realistic silicon, or a material FCC--BCC
transition. The cost of fidelity is summarized by the first physical hopping radius and
retained block count at each declared tolerance.
