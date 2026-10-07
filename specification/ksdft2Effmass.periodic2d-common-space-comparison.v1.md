# Periodic2d plane-wave/finite-difference common-space comparison specification v1

Status: **adopted for software construction; scientific interpretation not yet validated**

Scope: threshold-free comparison of the dimensionless period-$2\pi$ cosine toy
Hamiltonian represented in a finite plane-wave basis and on a centered finite-difference
coordinate grid. This specification defines an explicit directional sampling map,
finite-operator transport, signed subtraction, and matrix diagnostics.

This specification does not define a new represented operator, retained space, retained
operator, effective model, continuum extrapolation, acceptance threshold, material
model, uncertainty model, or scientific-validation result.

## Controlled parent and Bloch fiber

Both representations use the same dimensionless spinless scalar toy parent

$$
H=-\partial_x^2-\partial_y^2
 +\lambda_x\cos x+\lambda_y\cos y
 +\lambda_{xy}\cos x\cos y
$$

on $[0,2\pi)^2$. At reduced momentum
$\boldsymbol\kappa=(\kappa_x,\kappa_y)$, the finite plane-wave space is spanned by
$e^{i[(\kappa_x+p)x+(\kappa_y+q)y]}$ for $-M\leq p,q\leq M$. The coordinate-grid
matrix represents the same Bloch fiber through directed seam phases
$e^{+i\kappa_d2\pi}$ and their conjugates.

The parent is a controlled numerical toy model, not a material Hamiltonian. The
comparison therefore studies two finite representations of one stipulated parent; it
cannot establish that parent model's physical adequacy.

## Compatible represented inputs

The comparison request contains complete
`Periodic2DPlaneWaveHamiltonianResult` and
`Periodic2DFiniteDifferenceHamiltonianResult` records. Their exact adapter types fix:

- the same spinless scalar dimensionless period-$2\pi$ cosine-model family;
- the reciprocal kinetic-energy scale and model-owned zero of energy;
- plane-wave order $(p,q)$ with $p$ outer and $q$ inner;
- coordinate-site order $(i,j)$ with $i$ outer and $j$ inner;
- Euclidean normalization of the finite coordinate-site basis; and
- the directed finite-difference Bloch-seam convention.

The configured parent-model values and reduced Bloch momentum
$\boldsymbol\kappa=(\kappa_x,\kappa_y)$ must agree exactly. Equal matrix ranks,
array shapes, spectra, names, or hashes do not establish compatibility.

For a symmetric plane-wave cutoff $M$ and $N$ grid points per direction, the request
requires

$$
2M+1\leq N.
$$

This condition makes the retained reciprocal indices distinct modulo the coordinate
grid. It is an alias-avoidance precondition, not a convergence condition.

## Directional common-space map

Let

$$
x_i=y_i=\frac{2\pi i}{N},\qquad i=0,\ldots,N-1,
$$

and let $-M\leq p,q\leq M$. The normalized map from ordered plane-wave coefficients
to ordered coordinate-grid samples is

$$
T_{(i,j),(p,q)}=
\frac{1}{N}\exp\!\left(
 i[(\kappa_x+p)x_i+(\kappa_y+q)y_j]
\right).
$$

Thus $T$ has shape $N^2\times(2M+1)^2$. Its rows belong to the finite coordinate-grid
representation and its columns belong to the finite plane-wave representation. The map
direction must not be inferred from its dimensions alone; it is fixed by this equation
and by the declared basis orderings.

When retained basis columns are distinct modulo the grid, exact arithmetic gives
$T^\dagger T=I$. Binary64 evaluation need not be exactly isometric, so the software retains

$$
d_T=\lVert T^\dagger T-I\rVert_F
$$

as a diagnostic and applies no hidden tolerance. When $N>2M+1$, $T$ is a proper
rectangular semiunitary embedding and $TT^\dagger\ne I$. At the allowed equality
boundary $N=2M+1$, both spaces have dimension $N^2$, $T$ is square unitary in exact
arithmetic, and $TT^\dagger=I$ as well.

## Transport and signed comparison

Let $H_{\mathrm{FD}}$ be the finite-difference coordinate-grid matrix and
$H_{\mathrm{PW}}$ the finite plane-wave matrix. The comparison Action transports only
in the grid-to-plane-wave direction:

$$
\widetilde H_{\mathrm{FD}}=T^\dagger H_{\mathrm{FD}}T.
$$

For $N>2M+1$, this is a proper-subspace compression of the grid operator and is not a
similarity transform of the full grid matrix; it does not imply equality of the two
full spectra. For $N=2M+1$, it is a full-space unitary similarity transform. Neither
case establishes a retained physical subspace or scientific adequacy.

Only after this state-space alignment is the signed difference defined:

$$
\Delta H=\widetilde H_{\mathrm{FD}}-H_{\mathrm{PW}}.
$$

Reversing the sign changes the represented comparison and is not an equivalent storage
convention. Direct subtraction of the untransported matrices is undefined even when
matrix sizes happen to agree.

The Result retains $T$, $\widetilde H_{\mathrm{FD}}$, $\Delta H$, $d_T$, and

$$
d_F=\lVert\Delta H\rVert_F,
\qquad
d_{\max}=\max_{a,b}|\Delta H_{ab}|.
$$

All retained quantities are unitless because the specific toy-model energy convention
is dimensionless. The operator-valued quantities still represent dimensionless energy;
`Unitless` does not erase the model energy zero or parent identity carried by the
request.

## Action and Result ownership

`Periodic2DCommonSpaceOperatorComparator` owns request-to-value derivation: it builds
the sampling map, performs the dense transport and signed subtraction, and evaluates
the diagnostics once for the returned values.

`Periodic2DCommonSpaceComparisonResult` owns intrinsic immutable structure and algebra.
It validates:

- exact quantity types, units, directional shapes, and finite storage;
- $\widetilde H_{\mathrm{FD}}=T^\dagger H_{\mathrm{FD}}T$ from retained values;
- $\Delta H=\widetilde H_{\mathrm{FD}}-H_{\mathrm{PW}}$; and
- all three diagnostics from the retained matrices.

The Result does not reconstruct $T$ from the request and does not replay the complete
Action. It does recompute the dense congruence from retained $T$ and
$H_{\mathrm{FD}}$ so a transported matrix cannot be forged together with consistent
downstream differences and norms. This is an explicit intrinsic-integrity cost. A
manually constructed Result satisfying these intrinsic relations does not prove that
the Action ran, establish execution provenance, or constitute retained scientific
evidence.

## Numerical and resource behavior

The map and matrix products use complex128 arithmetic and diagnostics use binary64.
Unrepresentable transport, subtraction, or norm results raise `OverflowError` rather
than becoming accepted nonfinite output. Let $G=N^2$ and $P=(2M+1)^2$. The sampling map contains $GP$ complex values; the
existing grid and plane-wave matrices contain $G^2$ and $P^2$ values. One dense
congruence costs $O(PG^2+P^2G)$ under the implemented multiplication order and needs
additional dense workspace. Result construction repeats that congruence once for
intrinsic correlation. Either evaluation may raise `MemoryError`; the implementation
applies no arbitrary grid or cutoff cap.

No tolerance is attached to $d_T$, $d_F$, or $d_{\max}$. A caller that studies grid or
cutoff sequences owns its convergence protocol, trend criteria, and acceptance
decision. The Frobenius norm is not normalized by rank, so values across different
cutoffs cannot be compared as per-mode errors without a separately declared rule.

## Discrete dispersion and potential sampling

For grid spacing $h=2\pi/N$, the centered finite-difference kinetic energy of one
sampled mode is

$$
\epsilon^{\mathrm{FD}}_{pq}
=\frac{4}{h^2}\left[
\sin^2\!\frac{(\kappa_x+p)h}{2}
+\sin^2\!\frac{(\kappa_y+q)h}{2}
\right],
$$

whereas the finite plane-wave representation uses the continuum kinetic value

$$
\epsilon^{\mathrm{PW}}_{pq}
=(\kappa_x+p)^2+(\kappa_y+q)^2.
$$

Their fixed-mode difference is second order in $h$ as $h\to0$, but this comparator
evaluates one finite pair and performs no extrapolation.

The grid potential is pointwise sampled. For
$\Delta p=p'-p$ and $\Delta q=q'-q$, its compressed matrix element is

$$
(T^\dagger V_{\mathrm{grid}}T)_{(p,q),(p',q')}
=\frac{1}{N^2}\sum_{i,j=0}^{N-1}
 V(x_i,y_j)e^{i(\Delta p x_i+\Delta q y_j)}.
$$

The common Bloch phase cancels, so these entries obey discrete Fourier arithmetic
modulo $N$. For the declared cosine parent, the nonzero continuum Fourier transfers are

$$
\begin{aligned}
(\pm1,0)&:\ \lambda_x/2,\\
(0,\pm1)&:\ \lambda_y/2,\\
(\pm1,\pm1)&:\ \lambda_{xy}/4.
\end{aligned}
$$

For $M=1,N=7$, retained pairwise transfers lie in $\{-2,-1,0,1,2\}^2$ and none of the
listed nonzero cosine transfers wraps onto a different retained transfer modulo seven.
The sampled potential block therefore equals the declared plane-wave Fourier block in
that bounded domain. This is a separate claim from sampling-map orthogonality, even
though both follow from discrete Fourier sums.

The condition $2M+1\leq N$ ensures distinct sampled basis columns; it does not guarantee
that every pairwise reciprocal transfer avoids potential aliasing for every allowed
$M,N$. In particular, the square $M=2,N=5$ map test uses a free potential because a
cosine transfer can wrap onto a different retained pairwise transfer at that boundary.
The full signed matrix is retained so off-diagonal aliasing or discretization structure
is not hidden by scalar norms.

## Error and claim boundaries

For this common parent, $\Delta H$ measures disagreement between two declared finite
representations after one explicit transport. It may contain finite-difference
truncation and plane-wave-basis effects. It is not, by itself, an estimate of:

- parent-model error relative to a material system;
- a uniquely separated attribution among plane-wave cutoff, finite-difference
  dispersion, potential sampling/aliasing, compression, and roundoff;
- retained-space, interpolation, downfolding, or effective-model error;
- continuum or basis-set convergence;
- uncertainty in a physical observable; or
- scientific adequacy or acceptance.

Software tests establish immutable contracts and finite algebra. Machine-readable
candidate records, local schemas, independent artifact-owned qualification tests,
exact consumer bindings, and an empty disposition ledger now cover sampling-map
orthogonality, centered-difference dispersion, and resolved cosine Fourier transfers.
Those consumer tests remain provisional until an exact committed candidate revision is
independently reviewed and its later reviewed-revision dispositions pass the separately
authorized acceptance gate. They therefore do not yet supply accepted numerical-
verification evidence. Neither provisional numerical checks nor software verification
establishes scientific validation or uncertainty quantification.

## Ownership and implementation mapping

- Defining module:
  `python/src/ksdft2effmass/periodic2d/compare/common_space.py`
- Sphinx API:
  `doc/sphinx/api/ksdft2effmass/periodic2d/common_space.rst`
- Software verification:
  `python/tests/software_verification/ksdft2effmass/periodic2d/compare/`
- Candidate qualification records, schemas, independent qualification tests, and
  provisional numerical consumers:
  `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/`
- Bounded resource, binding, independence, and lifecycle validation:
  `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_records.py`

The repository derives this finite comparison convention from its declared basis and
adapter contracts. Historical Fourier-analysis references may explain context, but no
external citation is used to claim that this exact software convention or its
scientific use has been validated.
