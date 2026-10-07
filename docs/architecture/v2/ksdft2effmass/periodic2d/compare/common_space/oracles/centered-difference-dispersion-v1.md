# Candidate oracle: centered-difference Bloch dispersion v1

## Identity and technical status

| Field | Value |
|---|---|
| Candidate oracle ID | `periodic2d.common-space.centered-difference-dispersion.v1` |
| Kind | Analytic eigenvalue of a declared finite-difference stencil |
| Evidence class sought | Numerical verification |
| Current status | **Candidate**; no qualification record, independent qualification test, disposition, or acceptance-gate result yet |
| Consumers | Free and cosine methods in `TestPeriodic2DCommonSpaceOperatorComparator` |

## Bounded claim

On the square period-$2\pi$ grid with spacing $h=2\pi/N$, the directed-seam centered
negative Laplacian acting on the sampled Bloch mode indexed by $(p,q)$ has eigenvalue

$$
\epsilon^{\mathrm{FD}}_{pq}
=\frac{4}{h^2}\left[
\sin^2\!\frac{(\kappa_x+p)h}{2}
+\sin^2\!\frac{(\kappa_y+q)h}{2}
\right].
$$

The plane-wave kinetic representation uses

$$
\epsilon^{\mathrm{PW}}_{pq}
=(\kappa_x+p)^2+(\kappa_y+q)^2.
$$

When the potential blocks are absent or independently shown to cancel after transport,
the expected common-space difference is diagonal with entries
$\epsilon^{\mathrm{FD}}_{pq}-\epsilon^{\mathrm{PW}}_{pq}$.

## Derivation

For one direction, let $\theta=(\kappa+n)h$. The centered negative second-difference
stencil applied to samples $u_j=e^{ij\theta}$ gives

$$
\frac{2u_j-u_{j+1}-u_{j-1}}{h^2}
=\frac{2-e^{i\theta}-e^{-i\theta}}{h^2}u_j
=\frac{4}{h^2}\sin^2\!\frac{\theta}{2}\,u_j.
$$

The positive and negative boundary seams reproduce the same relation because they carry
$e^{+i\kappa 2\pi}$ and its conjugate. Adding the independent $x$ and $y$ directional
stencils yields the declared two-dimensional eigenvalue. Subtracting the continuum
kinetic diagonal gives the fixed-representation kinetic discrepancy.

The authoritative equations are `EQ-PERIODIC2D-COMMON-003` and
`EQ-PERIODIC2D-COMMON-004` on the comparator
[mathematics page](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
and the “Discrete dispersion and potential sampling” section of the project
specification.

## Representation contract

| Property | Declared value |
|---|---|
| Mathematical operator | Centered finite-difference representation of $-\partial_x^2-\partial_y^2$ |
| Grid state space | $\mathcal G_N\cong\mathbb C^{N^2}$ with Euclidean site normalization |
| Common coefficient space | $\mathcal V_M^{\boldsymbol\kappa}$ after the separately declared sampling-map pullback |
| Mode basis/order | $(p,q)$ with `p_outer_q_inner`; grid sites with `x_outer_y_inner` |
| Gauge/fiber | Reduced momentum $\boldsymbol\kappa$ encoded by directed Bloch seams |
| Geometry | Square period-$2\pi$ half-open grid; $h=2\pi/N$ |
| Normalization | Euclidean finite grid; normalization cancels from the eigenvalue relation |
| Unit and energy reference | Dimensionless reciprocal kinetic-energy scale; parent-model energy zero |
| Scalar representation | binary64 formula; compared with complex128 transported matrices |

The oracle concerns the kinetic finite representation only. It does not define the
potential, sampling map, parent-model adequacy, or a retained physical subspace.

## Candidate validity domains

The v1 consumer domains are two fixed cases:

| Case | $N$ | $M$ | $(\kappa_x,\kappa_y)$ | Potential prerequisite |
|---|---:|---:|---|---|
| Free | 5 | 1 | $(0.13,-0.21)$ | Exactly zero parent couplings |
| Cosine | 7 | 1 | $(-0.17,0.09)$ | Potential cancellation supplied separately by `periodic2d.common-space.resolved-cosine-fourier-transfer.v1` |

Both cases use all retained $(p,q)\in\{-1,0,1\}^2$ in the declared order. The analytic
formula is more general, but the proposed v1 floating-point tolerances are not exported
outside these fixed parameter sets.

## Comparators and proposed tolerances

The free consumer directly compares both the complete transported matrix with the
diagonal finite-difference dispersion and the signed common-space difference with the
diagonal dispersion difference. The cosine consumer does **not** directly compare the
transported matrix or individual potential Fourier coefficients; it compares only the
complete signed difference with the diagonal kinetic discrepancy and checks the
isometry diagnostic. Its potential-cancellation inference therefore also depends on the
separate resolved-cosine-transfer candidate.

The fixed proposed entrywise bounds are:

- free $N=5$ transported matrix and difference: `rtol=0.0`, `atol=4.0e-15`;
- cosine $N=7$ signed difference only: `rtol=0.0`, `atol=6.0e-15`.

The mathematical stencil relation is exact for the declared finite operator. The
nonzero bounds cover binary64 trigonometric evaluation and complex128 map/matrix
products in these small cases. They are not yet independently qualified, are not an
$h$-refinement criterion, and do not bound arbitrary cutoff, momentum, or coupling
values.

## Planned independent qualification

The qualification test will assemble the one-dimensional centered stencil directly in
test code, including its two directed seam entries, apply it to independently sampled
Bloch modes, and compare the resulting action with the analytic eigenvalue. It will
construct the two-dimensional sum from directional actions. It will not import the
production finite-difference constructor, comparator, or their private kernels.

The terminating authority is direct substitution of the sampled exponential into the
declared stencil. Special cases will include the zero-momentum zero mode and the exact
conjugate seam relation. Fixed consumer parameter sets will establish the proposed
complex128/binary64 forward-error bounds.

## Error interpretation

For fixed mode and $h\to0$,
$\epsilon^{\mathrm{FD}}_{pq}-\epsilon^{\mathrm{PW}}_{pq}=O(h^2)$. The candidate
consumer tests do not perform that limit, estimate an observed order, or separate all
sources in a general matrix discrepancy. In the cosine case, attributing the remaining
diagonal difference to kinetics also requires the separately qualified resolved-
transfer oracle.

## Failure and invalidation conditions

The candidate leaves its v1 domain if the stencil width, seam direction, grid origin,
period, basis normalization/order, kinetic prefactor, unit, energy reference, dtype,
backend, momentum, or $(M,N)$ pair changes. Nonfinite formula or comparison results must
fail closed. A different stencil or physical scaling requires a new semantic oracle
version rather than a tolerance adjustment.

## Excluded claims

This oracle does not establish potential Fourier coefficients, transfer alias freedom,
general grid convergence, plane-wave cutoff convergence, physical effective masses,
material-model adequacy, scientific validation, UQ, or human acceptance.

## Provenance and evidence status

The derivation is repository-owned finite-difference algebra under the authoritative
project specification. No literature value or external calculation is used.

| Evidence kind | Status | Reason |
|---|---|---|
| Software verification | Not applicable | The candidate supplies a numerical reference relation |
| Numerical verification | Not evaluated | Qualification record, independent stencil-action tests, disposition, and acceptance gate remain absent |
| Scientific validation | Not evaluated | No physical reference or intended-use validation |
| Uncertainty quantification | Not evaluated | Fixed roundoff tolerances are not uncertainty intervals |
| Human acceptance | Not evaluated | Technical qualification and scientific acceptance remain separate |

## Navigation

- [Oracle inventory](index.md)
- [Resolved cosine transfer candidate](resolved-cosine-fourier-transfer-v1.md)
- [Comparator mathematics](../Periodic2DCommonSpaceOperatorComparator/implementation/mathematics/index.md)
- [Verification strategy](../Periodic2DCommonSpaceOperatorComparator/implementation/testing/index.md)
