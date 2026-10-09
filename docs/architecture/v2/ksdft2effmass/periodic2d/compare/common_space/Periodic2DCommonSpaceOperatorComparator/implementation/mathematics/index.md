# `Periodic2DCommonSpaceOperatorComparator` mathematics and physics

## Modeled parent and claim boundary

The compared parent is the dimensionless spinless scalar toy Hamiltonian

<a id="eq-periodic2d-common-parent"></a>

$$
H=-\partial_x^2-\partial_y^2
 +\lambda_x\cos x+\lambda_y\cos y
 +\lambda_{xy}\cos x\cos y,
\qquad (x,y)\in[0,2\pi)^2.
\tag{EQ-PERIODIC2D-COMMON-001}
$$

The cell is square, its direct primitive matrix is $A=2\pi I$, and its reciprocal
primitive matrix is $B=I$, so $A^{\mathsf T}B=2\pi I$. The energy variable is in the
model's reciprocal kinetic scale and has the model's fixed zero. There is no physical
length, electron mass, material identity, spin multiplicity, or experimentally fitted
parameter in this comparison.

Equation `EQ-PERIODIC2D-COMMON-001` is a controlled toy parent. Agreement between its
two finite representations cannot validate a material Hamiltonian. Disagreement cannot
be interpreted as parent-model error because both routes use the same parent law.

## Bloch fiber and plane-wave space

At reduced momentum $\boldsymbol\kappa=(\kappa_x,\kappa_y)$, the scalar Bloch basis is

<a id="eq-periodic2d-common-plane-wave"></a>

$$
\phi_{pq}^{\boldsymbol\kappa}(x,y)
 =\frac{1}{2\pi}
  e^{i[(\kappa_x+p)x+(\kappa_y+q)y]},
\qquad -M\leq p,q\leq M.
\tag{EQ-PERIODIC2D-COMMON-002}
$$

The finite plane-wave state space is
$\mathcal V_M^{\boldsymbol\kappa}=\operatorname{span}\{\phi_{pq}^{\boldsymbol\kappa}\}$
of dimension $(2M+1)^2$. Its software order is $p$ outer and $q$ inner. In this basis,
the continuum kinetic diagonal is

<a id="eq-periodic2d-common-continuum-dispersion"></a>

$$
\epsilon^{\mathrm{PW}}_{pq}
 = (\kappa_x+p)^2+(\kappa_y+q)^2.
\tag{EQ-PERIODIC2D-COMMON-003}
$$

The finite plane-wave matrix is already a cutoff representation. It is not the
infinite-dimensional parent operator, even though its kinetic entries use the exact
continuum dispersion for retained modes.

## Twisted coordinate-grid space

The finite-difference route samples the same Bloch fiber on

$$
x_i=y_i=ih,\qquad h=\frac{2\pi}{N},\qquad i=0,\ldots,N-1,
$$

and stores samples in $x$-outer, $y$-inner order. Its finite state space is
$\mathcal G_N\cong\mathbb C^{N^2}$ with Euclidean site normalization. Bloch momentum
enters the last-to-first positive seams as $e^{+i\kappa_d2\pi}$ and the reverse seams
as its conjugate. Thus the grid matrix and plane-wave matrix represent the same Bloch
fiber convention; comparing different $\boldsymbol\kappa$ values would compare
different quasi-periodic boundary conditions.

For one sampled plane wave, the centered negative-Laplacian eigenvalue is

<a id="eq-periodic2d-common-discrete-dispersion"></a>

$$
\epsilon^{\mathrm{FD}}_{pq}
 =\frac{4}{h^2}
  \left[
   \sin^2\!\left(\frac{(\kappa_x+p)h}{2}\right)
  +\sin^2\!\left(\frac{(\kappa_y+q)h}{2}\right)
  \right].
\tag{EQ-PERIODIC2D-COMMON-004}
$$

For fixed retained modes and $h\to0$,
$\epsilon^{\mathrm{FD}}_{pq}-\epsilon^{\mathrm{PW}}_{pq}=O(h^2)$. The comparator does
not perform that limit or estimate its coefficient; it reports one finite-grid matrix
difference.

## Sampling embedding

The software map from plane-wave coefficients to grid samples is

<a id="eq-periodic2d-common-sampling"></a>

$$
T_{(i,j),(p,q)}
 =\frac{1}{N}
  e^{i[(\kappa_x+p)x_i+(\kappa_y+q)y_j]}.
\tag{EQ-PERIODIC2D-COMMON-005}
$$

The $1/N$ factor is the product of two $1/\sqrt N$ discrete normalizations. It aligns
the continuum-normalized mode labels with the Euclidean grid basis used by the finite
matrix; no quadrature-weighted coordinate basis is introduced.

When $2M+1\leq N$, retained reciprocal indices are distinct modulo $N$. Discrete
Fourier orthogonality then gives

<a id="eq-periodic2d-common-semiunitary"></a>

$$
T^\dagger T=I_{(2M+1)^2}
\tag{EQ-PERIODIC2D-COMMON-006}
$$

in exact arithmetic. When $N>2M+1$, the map is proper rectangular and
$TT^\dagger\ne I_{N^2}$, so $T$ is a semiunitary embedding into a proper grid
subspace. At the allowed equality boundary $N=2M+1$, both spaces have dimension
$N^2$, $T$ is square unitary, and $TT^\dagger=I_{N^2}$ as well.

This distinction is physically and mathematically important. For $N>2M+1$, the
operation below compresses the grid operator to a proper sampled plane-wave subspace;
it is not a similarity transform of the full grid matrix and does not imply equality
of the full spectra. For $N=2M+1$, the operation is instead a full-space unitary
similarity transform.

## Common-space compression and difference

The grid operator is pulled back to $\mathcal V_M^{\boldsymbol\kappa}$ as

<a id="eq-periodic2d-common-compression"></a>

$$
\widetilde H_{\mathrm{FD}}
 =T^\dagger H_{\mathrm{FD}}T.
\tag{EQ-PERIODIC2D-COMMON-007}
$$

The signed common-space discrepancy is

<a id="eq-periodic2d-common-difference"></a>

$$
\Delta H
 =\widetilde H_{\mathrm{FD}}-H_{\mathrm{PW}}.
\tag{EQ-PERIODIC2D-COMMON-008}
$$

Both matrices in `EQ-PERIODIC2D-COMMON-008` act on the same ordered finite coefficient
space, use the same scalar Bloch convention, parent couplings, dimensionless energy
unit, and model energy zero. Subtraction before `EQ-PERIODIC2D-COMMON-007` is undefined
because the operands have different domains and bases.

The term “transport” in the public class name refers to this declared pullback: a
proper-subspace compression for $N>2M+1$ and a full-space unitary similarity at
equality. It must not be confused with real-time propagation, carrier transport,
parallel transport of a band frame, Wannier interpolation, or downfolding.

## Potential sampling and aliasing

The coordinate-grid potential is a pointwise sampled multiplication operator. With
$\Delta p=p'-p$ and $\Delta q=q'-q$, its compression is

<a id="eq-periodic2d-common-potential-transfer"></a>

$$
(T^\dagger V_{\mathrm{grid}}T)_{(p,q),(p',q')}
 =\frac{1}{N^2}\sum_{i,j=0}^{N-1}
 V(x_i,y_j)e^{i(\Delta p x_i+\Delta q y_j)}.
\tag{EQ-PERIODIC2D-COMMON-010}
$$

The common Bloch phase cancels. Discrete Fourier orthogonality therefore reproduces
potential Fourier coefficients modulo $N$. For the cosine parent, the only nonzero
transfers are $(\pm1,0)$ with coefficient $\lambda_x/2$, $(0,\pm1)$ with
$\lambda_y/2$, and $(\pm1,\pm1)$ with $\lambda_{xy}/4$.

The prerequisite $2M+1\leq N$ guarantees distinct sampled basis columns and hence
`EQ-PERIODIC2D-COMMON-006`; it does not by itself guarantee that every pairwise
reciprocal transfer inside the retained square avoids wrap-around aliasing of the
sampled potential. For the bounded numerical cosine test, $M=1$ and $N=7$, so retained
pairwise transfers lie in $\{-2,-1,0,1,2\}^2$ and the listed cosine harmonics cannot
wrap onto a different retained block modulo seven. The potential blocks then cancel in
`EQ-PERIODIC2D-COMMON-008`, leaving the diagonal
`EQ-PERIODIC2D-COMMON-004` minus `EQ-PERIODIC2D-COMMON-003`.

This resolved-transfer claim is related to, but distinct from, map orthogonality. The
square $M=2,N=5$ unitarity test therefore uses a free potential: at that boundary,
pairwise transfers can wrap by five even though sampled basis columns remain distinct.
No cosine cancellation claim is generalized beyond its declared $M=1,N=7$ domain.

## Diagnostics

The retained diagnostics are

<a id="eq-periodic2d-common-diagnostics"></a>

$$
d_T=\lVert T^\dagger T-I\rVert_F,
\qquad
d_F=\lVert\Delta H\rVert_F,
\qquad
d_{\max}=\max_{a,b}|\Delta H_{ab}|.
\tag{EQ-PERIODIC2D-COMMON-009}
$$

$d_T$ measures numerical loss of the declared discrete isometry. It is not a physical
observable. $d_F$ and $d_{\max}$ summarize one matrix discrepancy but discard its sign,
mode structure, and diagonal/off-diagonal decomposition; the full $\Delta H$ is
retained for that reason.

The Frobenius norm is not divided by matrix rank. Its scale can therefore change when
$M$ changes even if a per-mode discrepancy does not. Comparing diagnostics across
cutoffs or grids requires a separately declared protocol; this Action supplies none.

## Error decomposition and excluded inference

For this controlled same-parent comparison, possible contributors include:

1. plane-wave cutoff effects relative to the infinite parent space;
2. second-order finite-difference kinetic dispersion error;
3. coordinate sampling and potential-transfer aliasing;
4. compression to the sampled plane-wave subspace; and
5. complex128/binary64 rounding.

The one observed $\Delta H$ does not uniquely separate these contributors. In
particular, it must not be combined with parent-model, retained-space, interpolation,
truncation, downfolding, or observable errors unless another specification defines that
relationship.

No result from this comparator establishes:

- continuum convergence as $N\to\infty$;
- plane-wave convergence as $M\to\infty$;
- physical adequacy of the cosine parent;
- material effective masses or impurity physics;
- uncertainty quantification; or
- scientific or human acceptance.

## Implementation and evidence mapping

| Equation | Implementing owner | Direct evidence | Comparator and domain |
|---|---|---|---|
| `EQ-PERIODIC2D-COMMON-005` | `_plane_wave_to_grid_sampling_map` | Proper-rectangular Result shape/isometry evidence plus square-boundary two-sided unitarity | complex128; `M=1,N=5/7` and `M=2,N=5` |
| `EQ-PERIODIC2D-COMMON-007` | `execute` and Result intrinsic validation | forged-transport mutation test | exact retained-array equality |
| `EQ-PERIODIC2D-COMMON-008` | `execute` and Result intrinsic validation | forged-difference mutation test | exact retained-array equality |
| `EQ-PERIODIC2D-COMMON-004` | finite-difference parent constructor, observed through comparator | Qualified centered-difference-dispersion consumer after proposal acceptance | entrywise absolute `4e-15`/`6e-15` in declared fixed cases |
| `EQ-PERIODIC2D-COMMON-010` | finite-difference potential sampling and common-space transport | Qualified resolved-cosine-transfer consumer after proposal acceptance | entrywise absolute `6e-15`; `M=1,N=7` only |
| `EQ-PERIODIC2D-COMMON-009` | `execute` and Result intrinsic validation | individual diagnostic mutation tests | exact binary64 equality within one retained evaluation route |

## Evidence status

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Intrinsic transport, subtraction, and diagnostic mutation evidence | Result software test module | Exact equality and expected exceptions | Python/NumPy | Synthetic cutoff-one five-point Result | Not applicable |
| Numerical verification | Supported after exact proposal acceptance | DFT orthogonality, centered-difference dispersion, and resolved cosine Fourier transfer are three separately qualified bounded oracles | Comparator numerical test module, disposition ledger, [oracle dossiers](../../../oracles/index.md), and [testing strategy](../testing/index.md) | Entrywise absolute `4e-15`/`6e-15` | complex128/binary64 | Square `N=5,M=2`; free `N=5,M=1`; cosine `N=7,M=1` | Repository oracle-qualification gate v1 |
| Scientific validation | Not evaluated | No material, experimental, or converged reference | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model or propagation | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Review and use acceptance are separate | Decision record when available | Not applicable | Not applicable | Row 036 | Named human authority required |

## Provenance

The exact equations, map orientation, sign, ordering, and diagnostics are the
repository-defined contract in
`specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`. Bloch and
discrete-Fourier references listed in the
[references page](../references/index.md) provide historical context only; they do not
validate this implementation, its test tolerances, or its scientific use.
