# M4 protocol: two-dimensional represented-parent common-space comparison

## 1. Status and evidence boundary

This is a **draft, prospective protocol**. It is not frozen and has not been
executed. No result, convergence claim, or acceptance disposition is reported
here.

M4 is a local synthetic software- and numerical-verification study. It asks
whether two finite representations of the same two-dimensional scalar periodic
operator agree after both are transported into one explicitly identified finite
state space. It does **not** validate a material, silicon, density-functional
theory, Wannier localization, uncertainty calibration, or transferability.
Passing M4 would establish only bounded behavior for the operators, geometries,
meshes, formulas, and tolerances frozen by this protocol.

The square-cell cases partly repeat a previously retained synthetic calculation.
They are regression and reconciliation evidence, not an independent discovery.
The nonorthogonal cases are prospective, but remain synthetic numerical
verification.

## 2. Scientific question

For a fixed physical model and Bloch fiber, plane waves and finite differences
produce matrices of different dimensions and in different bases. Raw subtraction
is undefined. M4 asks:

> After sampling a declared plane-wave space on an alias-free periodic grid,
> does the transported finite-difference Hamiltonian differ from the plane-wave
> Hamiltonian by exactly the independently derived centered-difference kinetic
> symbol, for both orthogonal and nonorthogonal primitive cells?

A secondary question is how the represented operator and low-band spectral
discrepancies change under the predeclared cutoff and grid sequences. Those
trends are reported observations. Expected monotonicity is not used as an
oracle or pass criterion.

## 3. Frozen model intended for a later protocol freeze

### 3.1 Coordinates, lattice, and Bloch convention

Let the columns of the dimensionless direct primitive-basis matrix be
\(A=(\mathbf a_1,\mathbf a_2)\), and let

\[
 \mathbf r=A\mathbf s,\qquad \mathbf s\in[0,1)^2,
 \qquad g=A^{\mathsf T}A,
 \qquad B=2\pi A^{-\mathsf T}.
\]

The reduced Bloch momentum \(\boldsymbol\kappa\) is measured in turns along the
direct primitive axes. The quotient-seam convention is

\[
 \psi(\mathbf s+\mathbf q)
 =\exp\!\left(2\pi i\,\boldsymbol\kappa\cdot\mathbf q\right)
  \psi(\mathbf s),
 \qquad \mathbf q\in\mathbb Z^2.
\]

Two geometries are declared in `configuration.toml`:

1. `square-2pi`, with \(A=2\pi I\), is the orthogonal control and the
   geometry of the retained historical calculation;
2. `triangular-60deg-2pi`, with
   \(\mathbf a_1=(2\pi,0)^{\mathsf T}\) and
   \(\mathbf a_2=(\pi,\sqrt3\pi)^{\mathsf T}\), is the nonorthogonal control.

The second geometry has a nonzero off-diagonal inverse metric and therefore
requires mixed finite differences. It is well conditioned and is not a proxy
for a material lattice.

### 3.2 Parent operator

For each geometry the dimensionless spinless scalar parent is

\[
 H(\boldsymbol\kappa)=-\nabla_{\mathbf r}^2+V(\mathbf s),
\]

with

\[
 V(\mathbf s)=
 \lambda_1\cos(2\pi s_1)+
 \lambda_2\cos(2\pi s_2)+
 \lambda_{12}\cos(2\pi s_1)\cos(2\pi s_2).
\]

The kinetic coefficient and energy unit are one. The energy zero is the zero
cell average of this potential. Four parents are declared:

| Parent | Geometry | \((\lambda_1,\lambda_2,\lambda_{12})\) | Role |
|---|---|---:|---|
| square Fourier-separable | square | \((0.5,0.5,0)\) | historical reconciliation and exact Kronecker control |
| square Fourier-coupled | square | \((0.5,0.5,0.15)\) | historical reconciliation and coupled-potential control |
| skew free | triangular | \((0,0,0)\) | analytic mixed-derivative control |
| skew Fourier-coupled | triangular | \((0.5,0.5,0.15)\) | prospective nonorthogonal coupled parent |

“Fourier-separable” describes the potential. The complete skew-cell Hamiltonian
is not separable because its kinetic operator contains the inverse-metric cross
term. Only the square \(\lambda_{12}=0\) case is an exact Kronecker sum.

## 4. Finite representations and common state space

### 4.1 Plane-wave representation

For cutoff \(P\), reciprocal indices are
\(\mathbf m=(m_1,m_2)\in[-P,P]^2\), ordered with the first index outer and the
second index inner, both increasing. The matrix is

\[
 (H_{\mathrm{PW}})_{\mathbf m\mathbf n}
 =\delta_{\mathbf m\mathbf n}
 (2\pi(\mathbf m+\boldsymbol\kappa))^{\mathsf T}
 g^{-1}(2\pi(\mathbf m+\boldsymbol\kappa))
 +V_{\mathbf m-\mathbf n}.
\]

The Fourier coefficients are assembled analytically: axial transfers carry
\(\lambda_1/2\) or \(\lambda_2/2\), and the four diagonal transfers carry
\(\lambda_{12}/4\). Cutoffs are \(P=1,2,3,4,5,6\); \(P=6\) is the declared
low-band reference. Reference stability is checked by comparing the lowest four
bands at \(P=5\) and \(P=6\), rather than assuming that \(P=6\) is continuum
truth.

### 4.2 Finite-difference representation

The endpoint-excluded fractional grid is

\[
 \mathbf s_{n_1n_2}=(n_1/N,n_2/N),
 \qquad n_1,n_2=0,\ldots,N-1,
\]

with first-axis-outer, second-axis-inner C ordering. The declared extents are
\(N=9,13,17,25,33\).

PhysKit owns construction of the geometric Laplacian

\[
 \Delta_h=\sum_i g^{ii}D_{ii}+2g^{12}D_{12}
\]

with quotient-seam phases, where all derivatives are centered second-order
stencils. `ksdft2effmass` owns composition of
\(H_{\mathrm{FD}}=-\Delta_h+V\), model identity, comparison policy, and retained
diagnostics. The calculation must not copy PhysKit's reusable lattice or
Laplacian implementation.

### 4.3 Common-space map

The fixed common plane-wave cutoff is \(M=2\), so the common dimension is 25.
For each grid and momentum, the sampling map is

\[
 T_{(n_1,n_2),\mathbf m}
 =\frac{1}{N}
 \exp\!\left[
   2\pi i(\mathbf m+\boldsymbol\kappa)\cdot
   (n_1/N,n_2/N)
 \right],
 \qquad \mathbf m\in[-M,M]^2.
\]

Every declared grid satisfies \(N\geq2M+1\), so these sampled modes are distinct
modulo the discrete Fourier lattice. The required isometry check is
\(\|T^\dagger T-I\|_{\mathrm F}\).

The finite-difference matrix is transported as

\[
 \widetilde H_{\mathrm{FD}}=T^\dagger H_{\mathrm{FD}}T,
 \qquad
 \Delta H=\widetilde H_{\mathrm{FD}}-H_{\mathrm{PW}}^{(M)}.
\]

No matrices are subtracted before model, geometry, momentum, energy, spin,
unit, basis ordering, and state-space identity have been checked. The full
finite-difference and plane-wave matrices have different dimensions and are
never directly subtracted.

## 5. Independent analytic oracle

For \(h_i=1/N\) and
\(\theta_i=2\pi(m_i+\kappa_i)/N\), the centered finite-difference kinetic
symbol is

\[
 \varepsilon_h(\mathbf m+\boldsymbol\kappa)
 =\sum_i\frac{4g^{ii}}{h_i^2}\sin^2(\theta_i/2)
 +\frac{2g^{12}}{h_1h_2}\sin(\theta_1)\sin(\theta_2).
\]

The continuum plane-wave kinetic value is

\[
 \varepsilon(\mathbf m+\boldsymbol\kappa)
 =(2\pi(\mathbf m+\boldsymbol\kappa))^{\mathsf T}
  g^{-1}(2\pi(\mathbf m+\boldsymbol\kappa)).
\]

Because every potential Fourier transfer in the declared family is resolved on
every grid and common basis, the independently expected common-space difference
is diagonal:

\[
 (\Delta H)_{\mathbf m\mathbf n}
 =\delta_{\mathbf m\mathbf n}
 [\varepsilon_h(\mathbf m+\boldsymbol\kappa)
  -\varepsilon(\mathbf m+\boldsymbol\kappa)].
\]

This formula is the primary numerical oracle. In particular, changing from the
separable to the coupled potential should change spectra but not this operator
difference. The standalone verifier must reconstruct the mixed symbol and the
potential transfers directly; it must not infer correctness from a decreasing
error curve.

## 6. Sampling roles

The primary and diagnostic momenta are fully declared in `configuration.toml`
and represented in generated `input.json`. All components lie in the reduced
half-open cell \([-1/2,1/2)\).

- **Primary momenta** determine reported maxima and the formal disposition.
- **Diagnostic momenta** are disjoint and test whether the same reconstruction
  identities persist away from the primary coordinates. They cannot alter the
  parent, maps, cutoffs, grids, criteria, or disposition.
- There is no parameter fitting, calibration set, or training stage in M4.

The diagnostic set is therefore not claimed as statistical validation or a
material-level held-out data set.

## 7. Required diagnostics

For every parent, momentum, and applicable representation level, retain:

1. geometry identifier, primitive basis, direct metric, inverse metric, and
   reciprocal basis;
2. represented dimensions and explicit index ordering;
3. Hermiticity defects for both parent matrices;
4. \(\|T^\dagger T-I\|_{\mathrm F}\);
5. raw and per-common-dimension Frobenius norms of \(\Delta H\);
6. maximum elementwise defect between \(\Delta H\) and the analytic diagonal
   symbol;
7. maximum off-diagonal potential-transfer defect after transport;
8. complete ordered common-space spectral maximum and RMS discrepancies;
9. lowest-four full finite-difference versus \(P=6\) plane-wave spectral
   discrepancies, explicitly labeled as a two-discretization comparison;
10. \(P=5\) versus \(P=6\) low-band reference-stability defect;
11. refinement ratios and empirical slopes as descriptive observations; and
12. primary and diagnostic results as separate groups.

The square Fourier-separable case additionally retains the represented
Kronecker-sum matrix and complete-spectrum defects. No corresponding separable
claim is permitted for the skew geometry.

## 8. Historical reconciliation channel

The configured SHA-256 identities bind the retained historical square-cell
`input.json` and `result.json`. SHA-256 binds bytes; it does not establish
chronology or scientific validity.

The M4 implementation must reconstruct the exact historical comparison design
from the bound input and compare shared aggregate observables under the old
square-cell convention. This channel is labeled
`historical-square-case-reconciliation-only`. It may establish continuity with
retained bytes, but it is not independent evidence. New momenta, \(N=33\),
\(P=6\), and both skew-cell cases remain outside that historical result.

A mismatch must be reported, not repaired by changing the new input or the
historical artifact.

## 9. Verification criteria and dispositions

The criteria in `configuration.toml` are benchmark software controls, not
physical tolerances:

| Criterion | Bound |
|---|---:|
| represented Hermiticity defect | \(10^{-11}\) |
| common-map isometry Frobenius defect | \(10^{-11}\) |
| analytic-symbol elementwise reconstruction defect | \(10^{-10}\) |
| resolved potential-block elementwise defect | \(10^{-11}\) |
| independent result reconstruction defect | \(10^{-10}\) |
| \(P=5\) versus \(P=6\) lowest-four-band reference defect | \(10^{-8}\) |

These tolerances are deliberately above expected binary64 accumulation error
for the bounded matrix sizes. The reference-stability tolerance is a numerical
control, not a continuum error estimate.

The result disposition is one of:

- `verified-stable-reference`: every structural and independent-reconstruction
  criterion passes and the plane-wave reference stability criterion passes;
- `verified-reference-not-stable`: the operator identities pass but the
  declared low-band reference is not stable, so no low-band convergence claim
  may be made;
- `not-verified`: any Hermiticity, map, analytic-symbol, potential-transfer, or
  independent-reconstruction criterion fails.

Before execution, missing implementation prerequisites produce a preflight
`blocked` status rather than a scientific disposition. Refinement sequences are
reported as `decreasing`, `not-decreasing`, or `indeterminate`, but those labels
do not determine the verification disposition.

## 10. Independent verification contract

Two verification routes are required.

1. The library verifier strictly decodes `input.json` and `result.json`, checks
   identifiers and enums, replays maintained Actions, and compares every
   retained scalar and short array.
2. A standalone verifier imports neither the M4 calculator nor the M4
   comparator, serializer, PhysKit Laplacian constructor, or historical runner.
   It reconstructs the primitive metric, reciprocal basis, plane-wave matrix,
   quotient-seam finite-difference stencil, sampling map, analytic symbol, and
   diagnostics directly with NumPy/SciPy.

The standalone route still shares NumPy/SciPy, eigensolvers, binary64 arithmetic,
and the protocol's mathematical conventions. It is independent of the producer
implementation, not independent experimental evidence.

Strict decoding must reject unknown fields, missing fields, Boolean numeric
impostors, numeric strings, nonfinite values, inconsistent dimensions,
nonpositive-orientation lattices, aliased grids, unknown units, incompatible
momenta, and mismatched model identities.

## 11. Required implementation gate before freeze

The protocol must not be frozen or executed until all of the following exist:

1. an immutable M4 definition with nominal `Periodic2DModel` parent identity;
2. a plane-wave constructor supporting both declared primitive bases;
3. finite-difference Hamiltonian composition using PhysKit's maintained
   nonorthogonal Bloch-periodic Laplacian;
4. a common-space comparator that accepts those represented results and checks
   every compatibility precondition;
5. typed result objects, strict input/result codecs, and deterministic canonical
   serialization;
6. the library and standalone verifiers;
7. focused software tests, analytic-oracle tests, tamper tests, Ruff, and strict
   focused mypy passing; and
8. a source manifest and `protocol-freeze.json` binding the final input,
   protocol, implementation, verifier, dependency lock, and PhysKit revision.

The current `Periodic2DRepresentedParentCalculationScaffold` is intentionally
non-executable, and the current square-cell cosine wrapper/common-space
comparator does not by itself satisfy the nonorthogonal M4 contract. This is a
known preflight blocker, not permission to weaken the protocol to the existing
implementation.

## 12. Execution envelope and protected-action boundary

A future M4 run is restricted to local in-process synthetic Python computation.
It must invoke no Quantum ESPRESSO, Wannier90, scheduler, container service,
remote host, cluster, cloud service, or network resource. It must not read or
transmit private or unpublished calculation data.

The intended largest finite-difference matrix is \(1089\times1089\), the
largest plane-wave matrix is \(169\times169\), and the common space is
\(25\times25\). Sparse construction and low-band eigensolvers are expected.
Before execution, the runner must declare an explicit local wall-time and memory
limit; the proposed ceiling is 30 minutes and 2 GiB with no automatic retry.
This estimate is a planning bound, not a measured runtime.

Building and checking this protocol does not authorize any protected calculator
execution or commit.

## 13. Retained package required after an authorized local run

A completed package must contain at least:

- editable `configuration.toml` and deterministic `build_input.py`;
- canonical generated `input.json`;
- frozen `protocol.md` and `protocol-freeze.json`;
- `run.py`, strict result codec, and `result.json`;
- `verify_result.py`, `verification.json`, and
  `standalone-verification.json`;
- figure-data CSV and a bounded refinement/common-space figure;
- `report.md` with separate operator, common-spectrum, low-band, historical,
  and limitation sections;
- `software.json`, `source.sha256`, and package `SHA256SUMS`.

Large dense matrices are not retained. The result retains defining metadata,
short spectra, diagnostic arrays, and matrix digests sufficient for replay;
the verifiers reconstruct matrices from the frozen input.

## 14. Amendment and claim policy

After freeze, any change to geometry, model coefficients, momenta, cutoff or
grid sequences, map normalization, ordering, criteria, verifier identity, or
disposition logic requires a numbered amendment. Amendments must state whether
they are prospective, invalidate a result, or create a post-hoc analysis.
Post-hoc sensitivity studies must be stored separately and cannot modify the
sealed M4 disposition.

Permitted wording after a passing run is limited to the frozen synthetic domain,
for example: “the represented plane-wave and finite-difference operators agree
after explicit common-space transport up to the independently reconstructed
finite-difference kinetic-symbol defect.” It is not permitted to infer material
accuracy, physical validation, universal convergence, or uncertainty bounds.
