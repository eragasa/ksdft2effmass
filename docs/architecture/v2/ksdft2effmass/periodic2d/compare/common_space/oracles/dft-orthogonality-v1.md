# Candidate oracle: period-$2\pi$ DFT orthogonality v1

## Identity and technical status

| Field | Value |
|---|---|
| Candidate oracle ID | `periodic2d.common-space.dft-orthogonality.v1` |
| Kind | Exact analytic identity evaluated in finite precision |
| Evidence class sought | Numerical verification |
| Current status | **Candidate**; no qualification record, independent qualification test, disposition, or acceptance-gate result yet |
| Consumer | `TestPeriodic2DCommonSpaceOperatorComparator::test_execute__equal_basis_and_grid_sides__map_is_unitary` |

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

The candidate does not claim two-sided unitarity when $N>2M+1$.

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

The first qualification is deliberately bounded to:

- $M=2$ and $N=5$;
- fixed reduced momentum $(\kappa_x,\kappa_y)=(0.13,-0.21)$ used by the consumer;
- exact reciprocal labels $p,q\in\{-2,-1,0,1,2\}$;
- the declared ordering and normalization; and
- complex128 evaluation through NumPy on the supported Python environment.

In exact arithmetic the common Bloch phase cancels for arbitrary momentum. That
algebraic generalization is not a complex128 validity claim: sufficiently large finite
binary64 momentum can lose the integer reciprocal offsets when `momentum + index` is
formed. Any other momentum range therefore requires renewed finite-precision
qualification rather than reuse of the fixed `6.0e-15` bound.

## Comparator and proposed tolerance

The consumer forms both Gram products and compares them entrywise with the
$25\times25$ complex identity using

- relative tolerance: `0.0`;
- absolute tolerance: `6.0e-15`; and
- comparator: maximum entrywise absolute discrepancy as implemented by
  `numpy.testing.assert_allclose` with zero relative contribution.

The exact relation has zero mathematical error. The nonzero proposed bound covers only
the fixed complex128 phase evaluation and dense products. It is not yet qualified, is
not a general $N$-scaling bound, and is not an acceptance criterion for the Result's
stored isometry diagnostic.

## Planned independent qualification

The qualification test will construct the finite root-of-unity sums directly from the
published formula and verify the directional Kronecker deltas and two-dimensional
product at $N=5$. It will not import or invoke the production comparator, reuse its
private map builder, or infer orientation from matrix shape. The test will separately
check the exact index residues and the observed complex128 residual against the proposed
bound.

The terminating authority is the finite geometric-series identity, not agreement with
the production map.

## Failure and invalidation conditions

The candidate is outside its v1 domain if:

- reciprocal labels are not distinct modulo $N$;
- normalization, grid origin, period, ordering, or map direction changes;
- the two factors use different Bloch fibers or gauges;
- dtype or backend changes without renewed finite-precision evidence;
- the requested tolerance is used for another $M,N$ pair; or
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
| Numerical verification | Not evaluated | Qualification record, independent test, disposition, and acceptance gate remain absent |
| Scientific validation | Not evaluated | No physical reference or intended-use validation |
| Uncertainty quantification | Not evaluated | The floating-point tolerance is not an uncertainty interval |
| Human acceptance | Not evaluated | Technical qualification and scientific acceptance remain separate |

## Navigation

- [Oracle inventory](index.md)
- [Comparator mathematics](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
- [Verification strategy](../Periodic2DCommonSpaceOperatorComparator/implementation/testing/index.md)
