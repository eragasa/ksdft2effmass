# Prospective higher-rank composite-band alignment and locality protocol

## Status and authority

This document proposes a publication-independent Paper 3 experiment family. It defines a
common analytic model for spatial dimensions one, two, and three, but it does not assign
an immutable experiment version, select numerical coefficients or acceptance thresholds,
authorize execution, or report a result. The dimensional experiment identities, schemas,
resource limits, and retained-evidence policy remain open until protocol review closes.

The family is a successor to, not a replacement for, the retained rank-two controls and
the extracted fixed rank-three two-dimensional calculation. No rank-two tolerance, mesh,
gauge amplitude, truncation range, or evidence disposition transfers into this protocol.

## Scientific question

For an isolated composite subspace of arbitrary finite rank, how do

1. retained rank,
2. noncommuting gauge-decomposition depth,
3. admissible alignment family, and
4. spatial dimension

change the matrix-valued hopping locality and the spectral consequences of deliberate
finite-support truncation, even when the untruncated retained spectra and projectors are
exactly equivalent?

The protocol treats rank, decomposition depth, and spatial dimension as independent
variables. A calculation may vary only one while holding the other declared controls
fixed, or it must label the result as a joint variation. The phrase **arbitrary rank**
means that the formulas and software contract accept any declared finite integer rank
above the protocol minimum. It does not mean an infinite-dimensional computation,
uniform cost in rank, or numerical evidence for every rank.

## Common geometry and state spaces

The first control uses the dimensionless orthogonal unit lattice in
$d\in\{1,2,3\}$ dimensions. Its reduced Brillouin torus is

\[
\mathbb T^d=[-\pi,\pi)^d,
\]

with periodic identification in every coordinate. Real-space translations are
$\mathbf R\in\mathbb Z^d$, measured with the Euclidean unit-lattice metric. A later
nonorthogonal or material specialization is a different protocol.

For retained rank $r\geq3$, the parent state space is $\mathbb C^{2r}$ with canonical
basis $\{|a\rangle\}_{a=1}^{2r}$. The embedding
$E_r:\mathbb C^r\rightarrow\mathbb C^{2r}$ maps retained coordinates to the first $r$
canonical coordinates, and

\[
P_0=E_rE_r^\dagger.
\]

Every result must record $d$, $r$, the ambient dimension $2r$, basis ordering, right-action
frame convention, dimensionless reciprocal coordinates, energy unit, scalar energy
reference, lattice metric, and Fourier-sign convention. Operators are never subtracted
across unequal ranks or unidentified spaces.

## Periodic scalar fields

For a finite harmonic inventory $\mathcal Q_d\subset\mathbb Z^d\setminus\{0\}$, define

\[
\mathcal F_d(\mathbf k;c_0,a,b)
=c_0+\sum_{\mathbf q\in\mathcal Q_d}
\left[
 a_{\mathbf q}\sin(\mathbf q\cdot\mathbf k)
 +b_{\mathbf q}\cos(\mathbf q\cdot\mathbf k)
\right].
\]

The candidate inventories are

\[
\begin{aligned}
\mathcal Q_1={}&\{(1),(2)\},\\
\mathcal Q_2={}&\{(1,0),(0,1),(1,1),(1,-1)\},\\
\mathcal Q_3={}&\{(1,0,0),(0,1,0),(0,0,1),
(1,1,0),(0,1,1),(1,0,1),(1,1,1)\}.
\end{aligned}
\]

These sets specify candidate functional support, not numerical coefficients. A genuinely
multidimensional case must use at least one nonzero mixed-harmonic coefficient, and its
active wavevectors must span $\mathbb R^d$. Otherwise it is labeled separable or
effectively lower dimensional. The protocol assumes no point-group, time-reversal, or
inversion symmetry beyond constraints explicitly imposed by a reviewed coefficient
case.

## Isolated analytic parent

Let

\[
D_r(\mathbf k)=\operatorname{diag}
\bigl(\epsilon_1(\mathbf k),\ldots,\epsilon_r(\mathbf k)\bigr)
\]

and

\[
D_{\mathrm{ext}}(\mathbf k)=\operatorname{diag}
\bigl(\epsilon^{\mathrm{ext}}_1(\mathbf k),\ldots,
\epsilon^{\mathrm{ext}}_r(\mathbf k)\bigr),
\]

where every dispersion is a real field from the declared $\mathcal F_d$ family. A case
is admissible only if it has the prospectively certified uniform exterior-isolation
energy

\[
\Delta_{\mathrm{iso}}=\inf_{\mathbf k\in\mathbb T^d}
\left[
\min_b\epsilon_b^{\mathrm{ext}}(\mathbf k)
-\max_a\epsilon_a(\mathbf k)
\right]>0.
\]

A finite sampled minimum is not this certificate. Until an analytic interval bound or a
reviewed verified enclosure is selected, a sampled isolation energy is reported only as
a sampled diagnostic. The symbol $E_g$ is reserved for a physical valence--conduction
band gap; $E_{\mathrm{ref}}$ is only the common positive energy scale.

For each retained coordinate define the anti-Hermitian retained--exterior generator

\[
K_a=|r+a\rangle\langle a|-|a\rangle\langle r+a|.
\]

With real periodic fields $\eta_a(\mathbf k)$, set

\[
W_r(\mathbf k)=\prod_{a=1}^{r}
\exp\!\left[\eta_a(\mathbf k)K_a\right],
\qquad
F_r(\mathbf k)=W_r(\mathbf k)E_r.
\]

The $K_a$ act on disjoint coordinate pairs, so the factors commute. The parent operator
and retained projector are

\[
H_p^{(d,r)}(\mathbf k)=W_r(\mathbf k)
\begin{pmatrix}
D_r(\mathbf k)&0\\
0&D_{\mathrm{ext}}(\mathbf k)
\end{pmatrix}
W_r^\dagger(\mathbf k),
\qquad
P_r(\mathbf k)=F_r(\mathbf k)F_r^\dagger(\mathbf k).
\]

The smooth represented operator is exactly

\[
H_{F_r}(\mathbf k)=F_r^\dagger H_p^{(d,r)}F_r=D_r(\mathbf k).
\]

Two projector controls remain separate:

- **P0, constant-projector control:** every $\eta_a=0$;
- **P1, moving-projector control:** prospectively selected nonconstant $\eta_a$ fields.

P0 isolates internal gauge, alignment, Fourier conversion, and truncation. P1 additionally
tests frame construction, neighbor transport, reciprocal-boundary sewing, and projector
reconstruction. P0 and P1 results are not pooled into one error measure.

Internal retained-band crossings or degeneracies are permitted because the retained
projector and analytic frame are defined as complete rank-$r$ objects. Individual
backend-selected eigenvectors are not treated as canonical band labels.

## Layered Givens gauge decomposition

For adjacent retained coordinates $j$ and $j+1$, define the embedded complex Givens
rotation

\[
R_{j,j+1}(\theta,\phi)=
\begin{pmatrix}
\cos\theta&-e^{-i\phi}\sin\theta\\
e^{i\phi}\sin\theta&\cos\theta
\end{pmatrix}_{j,j+1}.
\]

At layer $\ell$, use the disjoint neighbor pairs

\[
\mathcal P_\ell=
\left\{(j,j+1):1\leq j<r,\ j\equiv\ell\pmod 2\right\}.
\]

Let every $\theta_{\ell j}(\mathbf k)$, $\phi_{\ell j}(\mathbf k)$, and
$\chi_a(\mathbf k)$ be a declared periodic field. For finite circuit depth $L\geq1$,
define

\[
Q_r(\mathbf k)=\operatorname{diag}
\left(e^{i\chi_1(\mathbf k)},\ldots,e^{i\chi_r(\mathbf k)}\right)
\]

and

\[
G_{r,L}(\mathbf k)=Q_r(\mathbf k)
\prod_{\ell=1}^{L}
\prod_{(j,j+1)\in\mathcal P_\ell}
R_{j,j+1}\!\left(
\theta_{\ell j}(\mathbf k),\phi_{\ell j}(\mathbf k)
\right).
\]

Increasing layer order is part of the canonical definition. Factors within a layer
commute; adjacent layers generally do not. The interaction graph is connected once the
selected layers cover every adjacent pair, so the construction is not a direct sum of
independent rank-two attacks.

The protocol distinguishes two gauge classes:

- **G0, real class:** $\phi_{\ell j}=0$ and $\chi_a=0$, hence
  $G_{r,L}\in SO(r)$;
- **G1, complex class:** complex pair phases and diagonal phases are allowed, hence
  $G_{r,L}\in U(r)$.

A G0 result does not validate G1. The attacked frame and represented operator are

\[
F'_{r,L}(\mathbf k)=F_r(\mathbf k)G_{r,L}(\mathbf k),
\qquad
H'_{r,L}(\mathbf k)=G_{r,L}^\dagger(\mathbf k)
D_r(\mathbf k)G_{r,L}(\mathbf k).
\]

The defining exact identities are

\[
F_{r,L}^{\prime\dagger}F'_{r,L}=I_r,
\qquad
F'_{r,L}F_{r,L}^{\prime\dagger}=P_r,
\qquad
\operatorname{spec}H'_{r,L}=\operatorname{spec}D_r.
\]

These are model identities and must be tested to numerical roundoff after sampling. They
are not empirical scientific conclusions. Increasing $L$ changes a representation of the
same retained operator unless another case explicitly changes the parent.

## Alignment families

Every comparison declares its admissible alignment family before observing results.
The initial diagnostic ladder is:

1. **A0, identity:** no alignment;
2. **A1, one global unitary:** one $U\in U(r)$ for the complete sampled torus;
3. **A2, pointwise complete unitary:** one independently selected full-rank
   $U(\mathbf k)\in U(r)$ at each construction point;
4. **A3, known inverse oracle:** the analytic $G_{r,L}^{-1}(\mathbf k)$, used only to
   verify construction and convention;
5. **A4, restricted circuit:** a separately frozen depth- and harmonic-bounded Givens
   family, if a reviewed optimizer and certificate policy are later selected.

A1, A2, and A4 are different feasible sets. None is described as a numerical
approximation to another. The oracle A3 is not an admissible fitted solution and cannot
be used to claim practical recoverability.

Pointwise and aggregate Procrustes selection must disclose absolute and relative
singular-value cutoffs. Equality at the applied cutoff is deficient. A rank-deficient
cross-covariance fails closed; no null-space completion is inferred. The retained output
must include the complete singular-value inventory or sufficient lossless summaries to
verify every rank disposition independently.

Matrices are aligned before Fourier transformation. Aligning already truncated hopping
blocks is a different, generally noncommuting operation and is outside this protocol.

## Selected first development tranche: periodic 1-D real gauge

The first bounded development tranche is selected as
`HR-CBAL-D1-P0-G0-DEV1`. This is a stable case label, not an immutable experiment-version
identity. It isolates retained rank and Givens-circuit depth before projector motion,
complex phases, or multidimensional plaquettes are introduced.

### Rank-normalized parent

For $a\in\{1,\ldots,r\}$ define the rank-normalized orbital coordinate

\[
x_{r,a}=\frac{2a-r-1}{r-1}\in[-1,1]
\]

and the bounded even harmonic

\[
c(k)=\frac34\cos k+\frac14\cos(2k),
\qquad |c(k)|\leq1.
\]

In units of the declared positive reference energy $E_{\mathrm{ref}}$, the retained and
exterior dispersions are

\[
\frac{\epsilon_a(k)}{E_{\mathrm{ref}}}
=0.40x_{r,a}+0.25\left(1+0.20x_{r,a}\right)c(k),
\]

\[
\frac{\epsilon_a^{\mathrm{ext}}(k)}{E_{\mathrm{ref}}}
=3.00+0.30x_{r,a}+0.10c(k).
\]

For fixed $k$, the retained maximum occurs at $x_{r,a}=1$ and the exterior minimum at
$x_{r,a}=-1$. Their separation is

\[
\frac{\min_a\epsilon_a^{\mathrm{ext}}(k)-\max_a\epsilon_a(k)}
{E_{\mathrm{ref}}}
=2.30-0.20c(k)\geq2.10.
\]

Because $c(0)=1$, equality is attained. Every selected rank therefore has the exact,
mesh-independent isolation certificate
$\Delta_{\mathrm{iso}}=2.10E_{\mathrm{ref}}$.

The first tranche uses P0: $\eta_a(k)=0$, $W_r(k)=I_{2r}$, and
$F_r(k)=E_r$. The parent and retained projector are consequently known without an
eigensolver. Internal retained-band crossings, if present, do not change the complete
rank-$r$ projector.

### Deterministic real attack

For $j\in\{1,\ldots,r-1\}$ define

\[
y_{r,j}=\frac{2j-r}{r-1},
\qquad |y_{r,j}|<1,
\]

and, for each positive layer index $\ell$,

\[
s_\ell(k)=\frac34\sin k+\frac14(-1)^\ell\sin(2k).
\]

The selected adjacent-pair angle is

\[
\theta_{\ell j}(k)=0.35(-1)^{\ell+j}
\left(1+0.15y_{r,j}\right)s_\ell(k).
\]

All pair phases and diagonal phases vanish, so
$G_{r,L}(k)\in SO(r)$. To state the exact continuum angle maximum, define

\[
q=\frac{\sqrt{41}-3}{8},
\qquad
s_*=\sqrt{1-q^2}\left(\frac34+\frac q2\right).
\]

For either sign in $s_\ell$, maximizing over $k$ gives $\max_k|s_\ell(k)|=s_*$;
the maximizing cosine is $q$ for even $\ell$ and $-q$ for odd $\ell$. The positive
amplitude factor is largest at $j=r-1$. Hence

\[
\max_{\substack{k\in[-\pi,\pi)\\ \ell\geq1,\ 1\leq j<r}}
|\theta_{\ell j}(k)|
=0.35\left[1+0.15\frac{r-2}{r-1}\right]s_*<0.4025\ \mathrm{rad}.
\]

This is an analytic continuum certificate, unlike the sampled development diagnostic
below. Layers use the canonical odd/even pair sets and increasing product order defined
above. One layer is an intentionally incomplete-connectivity baseline; two or more
layers cover every adjacent edge and generate the noncommuting connected-chain control.

### Exact representation certificates

The smooth represented field $D_r(k)$ is a trigonometric polynomial with harmonics only
at $0$, $1$, and $2$. Under the continuum Fourier convention of this protocol, its
blocks therefore satisfy

\[
T_{D_r}(R)=0\qquad\text{for every }|R|>2.
\]

This is an analytic support statement, not a sampled locality result. By contrast,
entries of $G_{r,L}(k)$ contain sines and cosines of nonconstant trigonometric
polynomials. Consequently the attacked field
$H'_{r,L}(k)=G_{r,L}^{\dagger}(k)D_r(k)G_{r,L}(k)$ is periodic and analytic but is not
assigned any finite Fourier support by the construction. The first-two-harmonic input
inventory must not be mistaken for a hopping cutoff after the nonlinear gauge attack.

For P0, the exact candidate-to-reference cross-overlap is

\[
M(k)=F_{r,L}^{\prime\dagger}(k)F_r(k)=G_{r,L}^{\dagger}(k).
\]

Every singular value of $M(k)$ is exactly one. The unique complete-unitary pointwise
polar factor is therefore $G_{r,L}^{\dagger}(k)=G_{r,L}^{-1}(k)$. In exact arithmetic,
A2 and A3 both restore $D_r(k)$ before Fourier transformation and hence restore its
$|R|\leq2$ support. They remain separate diagnostic channels: A2 must reconstruct the
polar factor from the sampled frames, whereas A3 receives the generating inverse. A
finite-grid agreement between them tests implementation and convention only; it is not
new scientific evidence. No corresponding recovery statement applies to A1, whose
aggregate cross-covariance must independently pass its rank threshold.

Every represented field is pointwise Hermitian and periodic, so its continuum Fourier
blocks obey $T(-R)=T(R)^\dagger$. A finite transform must test the corresponding discrete
pairing rather than assume it.

### Rank and depth ladder

The selected full one-dimensional development grid is

\[
r\in\{3,4,8,16\},
\qquad
L\in\{1,2,4,8\}.
\]

The shared cross-dimensional core for later 2-D and 3-D specializations is the subset
$r\in\{3,4,8\}$ and $L\in\{1,2,4\}$. Selecting that common subset now does not select
2-D or 3-D harmonic coefficients, meshes, or evidence status.

Every case evaluates A0 identity, A1 one-global-unitary, A2 pointwise-complete-unitary,
and A3 known-inverse-oracle channels. A4 restricted-circuit fitting is excluded from this
tranche because no optimizer or certificate policy has been selected. A3 remains a
construction oracle and cannot be reported as a fitted recovery result.

For cross-rank reporting, matrix Frobenius quantities must be retained both raw and
normalized by $\sqrt rE_{\mathrm{ref}}$; quadratic matrix weights must be retained both
raw and normalized by $rE_{\mathrm{ref}}^2$. This normalization is selected before
observing outcomes and does not replace the raw values. Ordered-spectrum maximum errors
are normalized by $E_{\mathrm{ref}}$, and spectrum RMS errors by
$\sqrt rE_{\mathrm{ref}}$.

### Remaining numerical selections

This tranche closes the 1-D parent coefficients, analytic gap, projector control, real
gauge class, angle law, rank/depth ladder, alignment channels, and cross-rank
normalizations. It does not yet select construction/evaluation meshes, refinement
levels, singular-value cutoffs, numerical-integrity tolerances, hopping supports,
first-passing reporting levels, resource ceilings, schemas, or verifier identities.
Those controls must be frozen before calculation; no development outcome may be used to
choose them.

### Non-authoritative finite-grid sanity check

The development utility `verify_d1_p0_g0_controls.py` samples the selected formulas on

\[
\mathcal K_M=\left\{-\pi+\frac{2\pi n}{M}:n=0,\ldots,M\right\},
\qquad M=20000,
\]

and reports, for each selected rank,

\[
\widehat\Delta_{\mathrm{iso},r}
=\min_{k\in\mathcal K_M}
\left[\min_a\epsilon_a^{\mathrm{ext}}(k)-\max_a\epsilon_a(k)\right]
\]

and

\[
\widehat\theta_r
=\max_{\substack{k\in\mathcal K_M,\ 1\leq\ell\leq8\\1\leq j<r}}
|\theta_{\ell j}(k)|.
\]

This grid is not a selected construction mesh or evaluation mesh. The sampled isolation
energy and sampled angle maximum are only reproducibility checks against the analytic
certificates. The sampled angle is slightly below the exact continuum maximum because
the maximizing momentum need not lie on the grid. Neither sampled value may be promoted
to convergence or retained-evidence status.

## Dimension-specific transport and sewing

All analytic fields are $2\pi$ periodic, so the canonical ambient basis has identity
face sewing. A numerical route must nevertheless reconstruct and verify the declared
sewing rather than infer it from array shape.

### Periodic 1-D

The one-dimensional case has one neighbor-link family, one primitive reciprocal closure,
and hopping blocks indexed by $R\in\mathbb Z$. It is the primary rank/depth isolation
case because it introduces no plaquette channel. Closure eigenphases are stored as an
unordered rank-$r$ multiset.

### Periodic 2-D

The two-dimensional case has $x$- and $y$-link families, sewing across both reciprocal
face pairs, primitive closures in both directions, and $xy$ plaquettes. Hopping blocks
are indexed by $\mathbf R\in\mathbb Z^2$. Wilson-loop phase spectra are compared as
unordered multisets; no band-by-band phase labeling is inferred through crossings.

### Periodic 3-D

The three-dimensional case has $x$, $y$, and $z$ link families, sewing across all three
reciprocal-face pairs, three primitive closures, and $xy$, $xz$, and $yz$ plaquettes.
Hopping blocks are indexed by $\mathbf R\in\mathbb Z^3$. Dense tensor fields must not be
materialized solely for diagnostics when a matrix-free or streamed route can provide the
same declared quantity.

Neighbor transport is applicable only if every required cross-overlap passes its applied
singular-value threshold. Closure and plaquette diagnostics are inapplicable, rather than
zero, when a required link is rank deficient.

## Topological boundary

The analytic frame $F_r(\mathbf k)=W_r(\mathbf k)E_r$ is global and periodic. Therefore
P0 and P1 define topologically trivial complex composite bundles. Wilson loops, closure
phases, and plaquettes are transport and sewing diagnostics in this family; they are not
claims of Chern, $\mathbb Z_2$, crystalline, or three-dimensional topological character.

A nonidentity Wilson loop does not by itself imply a topological obstruction. A future
obstructed model would require patchwise frames and transition functions, and would be a
separate experiment family rather than a hidden coefficient choice here.

The reusable diagnostics developed from this family may later support a fail-closed
pristine/defect compatibility screen, but Paper 3 does not construct defect operators.
Paper 5 owns the common-space subtraction decision, and Paper 6 owns full topological
and symmetry-obstruction protocols. The synthetic P0/P1 cases exercise known-compatible
frames; they do not validate material bundle compatibility.

## Fourier representation and locality

For a declared represented field $H(\mathbf k)$, define the continuum hopping blocks

\[
T(\mathbf R)=\frac{1}{(2\pi)^d}
\int_{\mathbb T^d}e^{-i\mathbf k\cdot\mathbf R}
H(\mathbf k)\,d^d\mathbf k.
\]

A finite calculation uses a declared half-open tensor mesh and its exact discrete Fourier
convention. The discrete transform is a finite matrix representation of sampled data,
not the continuum coefficient sequence. Continuum quadrature error, finite-mesh aliasing,
and deliberate hopping truncation remain distinct.

Every support is an explicit set of translation vectors. It must include inversion pairs
and complete orbits of any point group actually declared by the case. Equal-radius ties
are never split. A shell number is not transferred between dimensions or metrics without
the full vector inventory and physical radius.

For a retained support $\Omega\subset\mathbb Z^d$, define

\[
T_\Omega(\mathbf R)=
\begin{cases}
T(\mathbf R),&\mathbf R\in\Omega,\\
0,&\mathbf R\notin\Omega.
\end{cases}
\]

The protocol reports complete matrix-block norms, omitted quadratic weight, omitted block
norm, reconstruction residual, and the spectral consequence of the reconstructed
truncated operator. Frobenius quantities are reported both unnormalized and, when
cross-rank comparison is intended, with a prospectively selected rank normalization.
The normalization and its interpretation must be frozen before results; dividing by
$\sqrt r$ after observing a trend is not permitted.

## Construction and evaluation roles

Each dimensional protocol must freeze before execution:

- a construction tensor mesh used to build frames, alignments, Fourier blocks, and
  truncations;
- a disjoint shifted evaluation mesh used only after all construction choices are fixed;
- finite rank and depth cases;
- harmonic coefficients and projector/gauge cases;
- support inventories;
- singular-value and numerical tolerances; and
- resource ceilings.

Evaluation data cannot alter ranks, depths, coefficients, meshes, alignments, support,
thresholds, or reported-case selection. The construction role is not called training
unless a statistical model is actually learned.

## Diagnostic ledger

For every case, retain separate diagnostics for:

1. parent Hermiticity and the declared scalar energy reference;
2. sampled retained/exterior gap and any independently certified gap bound;
3. frame orthonormality and projector idempotency;
4. smooth/attacked projector and ordered-spectrum defects;
5. neighbor-overlap singular values and threshold dispositions;
6. reciprocal-face sewing, primitive closures, and applicable plaquettes;
7. identity, global, pointwise, oracle, and any restricted-family alignment residuals;
8. unitary defects and rank-cutoff inventories;
9. Fourier reconstruction, Hermitian pairing, Parseval, and Nyquist bookkeeping;
10. complete-block locality and shell inventories;
11. withheld interpolation error;
12. deliberate truncation error relative to the full interpolant; and
13. total error relative to the direct evaluation field.

The last three channels are not added. Parent discretization, exact analytic embedding or
projection, frame construction, covariant equivalence, restricted alignment, Fourier
conversion, interpolation, and truncation remain distinct. No combined diagnostic score
is defined.

## Scaling study

The mathematical family permits every finite $r\geq3$ and $L\geq1$, but a calculation
uses a finite prospectively selected ladder. Scaling claims require at least:

- rank sweeps at fixed $d$, $L$, active harmonics, coefficient rule, and normalized parent
  energy scale;
- depth sweeps at fixed $d$, $r$, parent, and per-layer coefficient rule; and
- dimensional comparisons using explicitly matched quantities rather than inherited
  mesh sizes or shell indices.

Dense unitary factorization scales as $O(r^3)$ per sampled point. Tensor sampling scales
as $N$ in 1-D, $N_xN_y$ in 2-D, and $N_xN_yN_z$ in 3-D. Actual peak memory and wall time
must be measured rather than inferred solely from these leading-order expressions.
Resource failure is reported as unresolved coverage, not as a scientific failure of the
model.

## Independent verification

A producer-independent verifier must reconstruct, from the canonical source document:

- every harmonic field;
- $W_r$, $F_r$, $H_p$, and $P_r$;
- every Givens layer and $G_{r,L}$ in canonical order;
- exact-equivalence residuals;
- all declared alignment objectives without calling the producer action;
- transport, sewing, closure, and plaquette diagnostics through an independently composed
  route;
- Fourier blocks and truncations; and
- construction/evaluation error channels.

The verifier may share NumPy, SciPy, BLAS, or LAPACK lineage only when that shared lineage
is disclosed. It must not call the producer calculator, deserialize trusted derived
arrays in place of reconstruction, or silently complete rank-deficient maps.

Passing software tests or independent numerical reconstruction establishes bounded
software behavior only. It does not establish continuum convergence, arbitrary-rank
validity, material relevance, localization optimality, topological classification, or
scientific acceptance.

## Required source and result binding

Any future executable version requires strict canonical source, request, result, and
verification schemas. The artifact bundle must bind their SHA-256 identities, exact Git
revision, dependency revisions, Python and numerical-library versions, platform and
floating-point identifiers, and resource record. Generated figures are views of bound
results and are never the authoritative numerical artifact.

No calculation is retained until the protocol version, schemas, verifier, convergence
criteria, failure policy, resource gate, and evidence-package identity are reviewed and
frozen. Execution, retained-evidence creation, publication, and promotion remain separate
protected actions.

## Open selections before implementation or execution

The following choices remain unresolved and must not be selected from observed outcomes:

1. dimensional experiment-family identities and immutable version identities;
2. P1 moving-projector coefficients and every 2-D/3-D or G1 coefficient table;
3. 2-D and 3-D rank/depth ladders beyond the selected common comparison subset;
4. whether any immutable version includes G1 in addition to the selected D1 G0 tranche;
5. analytic or verified-enclosure gap methods for P1 and multidimensional cases;
6. construction and evaluation meshes and refinement sequence;
7. singular-value, Hermiticity, reconstruction, and Parseval tolerances;
8. truncation support, shell inventories, and first-passing reporting levels;
9. any restricted-circuit optimizer or certificate method;
10. resource ceilings and streamed-storage policy;
11. schemas, canonical serialization, and independent-verifier method identities; and
12. scientific acceptance requirements, convergence rules, and retained-evidence policy.

The D1 P0/G0 parent coefficients, exact analytic
$\Delta_{\mathrm{iso}}=2.10E_{\mathrm{ref}}$ isolation energy,
rank/depth ladder, A0--A3 channels, and cross-rank normalizations are selected and may
not be changed in response to their eventual outcomes. Until the remaining selections
close under review, this document remains a prospective protocol and no execution result
can be promoted to higher-rank evidence.
