# Candidate oracle: resolved cosine Fourier transfer v1

## Identity and technical status

| Field | Value |
|---|---|
| Candidate oracle ID | `periodic2d.common-space.resolved-cosine-fourier-transfer.v1` |
| Kind | Exact finite Fourier-transfer relation in a bounded no-wrap domain |
| Evidence class sought | Numerical verification |
| Current status | **Candidate**; no qualification record, independent qualification test, disposition, or acceptance-gate result yet |
| Consumer | `TestPeriodic2DCommonSpaceOperatorComparator::test_execute__cosine_operator__isolates_discrete_kinetic_error` |

## Why this is separate from DFT orthogonality

Sampling-map orthogonality asks whether two sampled plane-wave **columns** have the
correct inner product. This oracle asks whether a sampled multiplication operator has
the correct **off-diagonal transfer blocks** after compression. Both use finite Fourier
sums, but they have different inputs, alias conditions, and failure consequences.

The condition $2M+1\leq N$ is enough for distinct map columns. It is not enough to make
every potential transfer alias-free. Therefore the cosine cancellation claim cannot be
inferred from a passing map-unitarity test.

## Bounded claim

For

$$
V(x,y)=\lambda_x\cos x+\lambda_y\cos y
       +\lambda_{xy}\cos x\cos y,
$$

and the declared $M=1,N=7$ grid/cutoff pair, the compressed sampled potential satisfies

$$
(T^\dagger V_{\mathrm{grid}}T)_{(p,q),(p',q')}
=\frac{1}{N^2}\sum_{i,j=0}^{N-1}
V(x_i,y_j)e^{i[(p'-p)x_i+(q'-q)y_j]}.
$$

The common Bloch phase cancels. In the retained basis, the only nonzero transfer
coefficients are

$$
\begin{aligned}
(p'-p,q'-q)=(\pm1,0)&:\quad \lambda_x/2,\\
(0,\pm1)&:\quad \lambda_y/2,\\
(\pm1,\pm1)&:\quad \lambda_{xy}/4.
\end{aligned}
$$

All other retained transfer blocks are zero in exact arithmetic. Consequently the
sampled finite-difference potential contribution equals the plane-wave potential block,
so the cosine consumer's common-space difference isolates the separately declared
kinetic dispersion difference.

## Derivation

The parent harmonics are

$$
\cos x=\frac12(e^{ix}+e^{-ix}),\qquad
\cos y=\frac12(e^{iy}+e^{-iy}),
$$

and

$$
\cos x\cos y
=\frac14\sum_{\sigma_x,\sigma_y\in\{-1,+1\}}
e^{i(\sigma_xx+\sigma_yy)}.
$$

Substituting these expressions into the finite sum reduces each matrix element to a
product of root-of-unity sums. With $M=1$, retained directional differences belong to
$\{-2,-1,0,1,2\}$. Modulo seven, none of these differences is congruent to an intended
$\pm1$ harmonic except the corresponding $+1$ or $-1$ difference itself. Thus no
nonzero cosine harmonic wraps onto another retained transfer block.

The authoritative relation is `EQ-PERIODIC2D-COMMON-010` on the comparator
[mathematics page](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
and the potential-sampling equation in the project specification.

## Representation contract

| Property | Declared value |
|---|---|
| Parent | Dimensionless spinless scalar period-$2\pi$ cosine toy model |
| Potential operator | Pointwise multiplication on the coordinate grid; Fourier coupling in the plane-wave basis |
| Grid state space | $\mathcal G_7\cong\mathbb C^{49}$, Euclidean `x_outer_y_inner` site basis |
| Plane-wave state space | $\mathcal V_1^{\boldsymbol\kappa}\cong\mathbb C^9$, `p_outer_q_inner` basis |
| Map direction | Grid potential compressed to plane-wave coefficient space by $T^\dagger(\cdot)T$ |
| Gauge/fiber | Fixed reduced momentum $(-0.17,0.09)$ in the consumer; common Bloch phase cancels from potential transfers |
| Normalization | Two-dimensional sampling factor $1/N$ in each map column, giving $1/N^2$ in matrix elements |
| Geometry | Half-open square cell $[0,2\pi)^2$, seven points per direction |
| Couplings | $(\lambda_x,\lambda_y,\lambda_{xy})=(0.4,0.7,0.2)$ |
| Unit and energy reference | Dimensionless model energy and parent-owned zero |
| Scalar representation | complex128 transport and plane-wave blocks |

No frame alignment, retained-space projection, interpolation, or material provenance is
involved.

## Candidate validity domain

The v1 claim is restricted to:

- $M=1$, $N=7$;
- the exact cosine harmonics and coupling values above;
- the declared period, grid origin, basis orders, map normalization, and transfer-sign
  convention;
- one common Bloch fiber, noting that its phase cancels algebraically; and
- complex128/NumPy evaluation in the supported Python environment.

The no-wrap fact is domain-specific. It does not extend to the allowed square
$M=2,N=5$ map case, where a retained difference can differ by five and hence wrap onto
a cosine harmonic modulo five.

## Comparator and proposed tolerance

The existing cosine consumer does **not** directly compare the transported Hamiltonian
or individual potential Fourier coefficients. It compares only the complete signed
difference against the diagonal kinetic discrepancy supplied by the centered-difference
candidate, using `rtol=0.0` and `atol=6.0e-15`, and separately checks the isometry
diagnostic. Vanishing off-diagonal entries in that signed difference provide indirect
cancellation evidence, but they do not constitute a direct coefficient-by-coefficient
potential-block test.

The planned independent qualification test, not the current consumer, will compare
every sampled potential transfer with its explicit Fourier coefficient. For the
potential relation itself, the exact mathematical discrepancy is zero. The
proposed bound covers finite complex exponential evaluation and dense products for this
fixed $49$-site/$9$-mode case. It remains unqualified and is not a general potential,
cutoff, grid, or coupling tolerance.

## Planned independent qualification

The qualification test will:

1. enumerate the retained transfer differences independently of the production basis
   constructor;
2. derive expected coefficients directly from the three exponential expansions;
3. evaluate the finite root-of-unity sums at $N=7$;
4. verify every retained matrix element, including analytically zero blocks; and
5. demonstrate that the same no-wrap inference is unavailable at $M=2,N=5$.

It will not import the production comparator, cosine plane-wave constructor,
finite-difference constructor, or private map builder. The terminating authority is the
explicit harmonic expansion plus finite geometric-series identity.

## Dependence on the other candidate oracles

This candidate uses the same root-of-unity identity as
[`periodic2d.common-space.dft-orthogonality.v1`](dft-orthogonality-v1.md), but it has a
separate record because its input is a multiplication operator and its domain includes
pairwise transfer aliasing. The cosine consumer also relies on
[`periodic2d.common-space.centered-difference-dispersion.v1`](centered-difference-dispersion-v1.md)
to identify the remaining diagonal difference. All required candidates must become
effectively qualified before that consumer supplies accepted numerical evidence.

## Failure and invalidation conditions

The candidate is invalidated by a changed harmonic content, cutoff, grid count, grid
origin, period, transfer sign, basis ordering, map normalization, coupling value, dtype,
backend, or alias domain. Nonfinite couplings or arithmetic must fail closed. A new
potential family requires a new semantic oracle rather than reuse based on a similar
matrix pattern.

## Excluded claims

This oracle does not establish map unitarity, kinetic dispersion, arbitrary-potential
quadrature, no aliasing for every $2M+1\leq N$, continuum convergence, physical model
adequacy, scientific validation, UQ, or human acceptance.

## Provenance and evidence status

The Fourier coefficients and bounded no-wrap argument are repository-derived from the
authoritative parent equation and common-space specification. Historical Fourier
citations provide context only and do not qualify the coefficients or tolerance.

| Evidence kind | Status | Reason |
|---|---|---|
| Software verification | Not applicable | The candidate supplies a numerical reference relation |
| Numerical verification | Not evaluated | Qualification record, independent transfer tests, disposition, and acceptance gate remain absent |
| Scientific validation | Not evaluated | The parent is a controlled toy model, not a material reference |
| Uncertainty quantification | Not evaluated | Fixed roundoff tolerance is not uncertainty propagation |
| Human acceptance | Not evaluated | Technical qualification and scientific acceptance remain separate |

## Navigation

- [Oracle inventory](index.md)
- [DFT orthogonality candidate](dft-orthogonality-v1.md)
- [Centered-difference candidate](centered-difference-dispersion-v1.md)
- [Comparator mathematics](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
- [Verification strategy](../Periodic2DCommonSpaceOperatorComparator/implementation/testing/index.md)
