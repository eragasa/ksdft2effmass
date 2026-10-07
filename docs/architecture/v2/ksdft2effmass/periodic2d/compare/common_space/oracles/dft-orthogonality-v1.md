# Candidate oracle: period-$2\pi$ DFT orthogonality v1

## Identity and technical status

| Field | Value |
|---|---|
| Candidate oracle ID | `periodic2d.common-space.dft-orthogonality.v1` |
| Kind | Exact analytic identity evaluated in finite precision |
| Evidence class sought | Numerical verification |
| Current status | **Candidate**; machine-readable record and independent qualification test implemented, but the disposition ledger is empty and no acceptance-gate result exists |
| Consumers | Square-map, free-dispersion, and cosine-difference methods in `TestPeriodic2DCommonSpaceOperatorComparator` |

## Bounded claim

For the normalized period-$2\pi$ sampling map from the retained plane-wave coefficient
space to the Euclidean coordinate grid, columns whose reciprocal indices are distinct
modulo $N$ are orthonormal in exact arithmetic. Therefore

$$
T^\dagger T=I.
$$

At the declared equality boundary $M=2,N=5$, the map is square, so exact arithmetic
also gives

$$
TT^\dagger=I.
$$

The two rectangular consumers use $M=1,N=5$ and $M=1,N=7$ and claim only the
column-isometry relation $T^\dagger T=I$. The candidate does not claim two-sided
unitarity when $N>2M+1$.

## Derivation

For $x_i=2\pi i/N$ and integers $n,n'$, the one-dimensional normalized column inner
product is

$$
\frac1N\sum_{i=0}^{N-1}e^{i(n'-n)x_i}
=
\begin{cases}
1,&n'\equiv n\pmod N,\\
0,&n'\not\equiv n\pmod N.
\end{cases}
$$

The two-dimensional map is the product of the directional sums. Its Bloch factors
cancel between the conjugated and unconjugated columns, leaving Kronecker deltas in
$p$ and $q$ modulo $N$. The request condition $2M+1\leq N$ makes the retained labels
$-M,\ldots,M$ distinct modulo $N$, which gives column orthogonality.

For $M=2,N=5$, the map has $25$ rows and $25$ columns. A square matrix with
$T^\dagger T=I$ is unitary, yielding the second product. This dimension argument is
used only after state-space direction, basis order, and normalization are fixed; shape
alone is not an oracle.

The authoritative equations are `EQ-PERIODIC2D-COMMON-005` and
`EQ-PERIODIC2D-COMMON-006` on the comparator
[mathematics page](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
and the “Directional common-space map” section of
`specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`.

## Representation contract

| Property | Declared value |
|---|---|
| Source state space | Plane-wave coefficient space $\mathcal V_M^{\boldsymbol\kappa}\cong\mathbb C^{(2M+1)^2}$ |
| Target state space | Euclidean coordinate-grid space $\mathcal G_N\cong\mathbb C^{N^2}$ |
| Map direction | Plane-wave coefficients to grid samples |
| Plane-wave basis/order | $e^{i[(\kappa_x+p)x+(\kappa_y+q)y]}$; `p_outer_q_inner` |
| Grid basis/order | Euclidean site basis; `x_outer_y_inner` |
| Gauge/fiber | One fixed reduced Bloch momentum; identical phase convention in every column; Bloch phase cancels in Gram products |
| Normalization | $1/N$ in two dimensions, the product of two $1/\sqrt N$ factors |
| Geometry | Square half-open cell $[0,2\pi)^2$, $x_i=y_i=2\pi i/N$ |
| Unit and energy reference | Map is unitless; energy reference is not involved |
| Scalar representation | complex128 map and products; binary64 absolute residual comparison |

No retained physical space or material basis is identified by this map.

## Candidate validity domain

The first qualification is deliberately bounded to three consumer domains:

| Consumer domain | $M$ | $N$ | $(\kappa_x,\kappa_y)$ | Claimed product |
|---|---:|---:|---|---|
| Square free | 2 | 5 | $(0.13,-0.21)$ | $T^\dagger T=I$ and $TT^\dagger=I$ |
| Rectangular free | 1 | 5 | $(0.13,-0.21)$ | $T^\dagger T=I$ only |
| Rectangular cosine | 1 | 7 | $(-0.17,0.09)$ | $T^\dagger T=I$ only |

All use the declared ordering and normalization and complex128 evaluation through NumPy
on the supported Python environment. In exact arithmetic the common Bloch phase
cancels for arbitrary momentum. That algebraic generalization is not a complex128
validity claim: sufficiently large finite binary64 momentum can lose the integer
reciprocal offsets when `momentum + index` is formed. Any other momentum range therefore
requires renewed finite-precision qualification rather than reuse of these fixed
bounds.

## Comparator and proposed tolerance

The square consumer forms both Gram products and compares them entrywise with the
$25\times25$ complex identity using `rtol=0.0`, `atol=6.0e-15`, and maximum entrywise
absolute discrepancy. The free rectangular consumer checks the stored
$\lVert T^\dagger T-I\rVert_F<4.0\times10^{-15}$, and the cosine rectangular consumer
checks the same Frobenius diagnostic against $5.0\times10^{-15}$.

The exact relations have zero mathematical error. The nonzero proposed bounds cover
only the fixed complex128 phase evaluation, finite sums, and dense consumer products.
They are not yet qualified, are not general $N$-scaling bounds, and are not production
acceptance criteria.

## Implemented independent qualification evidence

The artifact-owned qualification test evaluates each directional column inner product
as an explicit scalar finite geometric sum for all three fixed domains, multiplies the
two directional sums for each two-dimensional Gram entry, and checks both entrywise and
Frobenius bounds. For the square domain it separately evaluates each row-Gram entry as
scalar sums over reciprocal labels. It does not construct a sampling matrix, use
`numpy.outer`/`numpy.kron` for this claim, import or invoke the production comparator, or
reuse its private map builder. The machine-readable record binds the exact qualification
node and all three consumer nodes, and the software validator enforces that dependency
boundary.

The terminating authority is the finite geometric-series identity, not agreement with
the production map. Passing this candidate evidence does not create a `QUALIFIED`
disposition.

## Failure and invalidation conditions

The candidate is outside its v1 domain if:

- reciprocal labels are not distinct modulo $N$;
- normalization, grid origin, period, ordering, or map direction changes;
- the two factors use different Bloch fibers or gauges;
- dtype or backend changes without renewed finite-precision evidence;
- any bound is used outside its declared $M,N$, momentum, comparator, and dtype domain; or
- nonfinite arithmetic occurs.

Any such change requires a new record digest and qualification decision, and a changed
semantic convention generally requires a new oracle version.

## Excluded claims

This oracle does not establish potential-transfer alias freedom, centered-difference
accuracy, continuum convergence, physical retained-space identity, parent-model
adequacy, scientific validation, UQ, or human acceptance. In particular, square-map
unitarity at $M=2,N=5$ does not make the cosine potential alias-free; the consumer uses
a free potential for that reason.

## Provenance and evidence status

The identity is repository-derived finite Fourier algebra under the authoritative
project specification. The Cooley–Tukey citation is historical context only; no FFT
algorithm is used and that paper does not qualify the software or tolerance.

| Evidence kind | Status | Reason |
|---|---|---|
| Software verification | Not applicable | The candidate supplies a numerical reference relation |
| Numerical verification | Not evaluated | Record and independent test are present, but reviewed-revision disposition and acceptance gate remain absent |
| Scientific validation | Not evaluated | No physical reference or intended-use validation |
| Uncertainty quantification | Not evaluated | The floating-point tolerance is not an uncertainty interval |
| Human acceptance | Not evaluated | Technical qualification and scientific acceptance remain separate |

## Navigation

- [Oracle inventory](index.md)
- [Comparator mathematics](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
- [Verification strategy](../Periodic2DCommonSpaceOperatorComparator/implementation/testing/index.md)
