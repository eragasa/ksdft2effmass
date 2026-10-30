# Physical interpretation of the gauge-alignment study

## Prescribed gauge alignments

Let $F_r(k)$ be the analytic reference frame for the retained rank-$r$ subspace and
$F'_{r,L}(k)$ the synthetically attacked frame at circuit depth $L$. The study compares
four right-unitary gauge alignments.

### Identity

The attacked frame is left unchanged:

$$
U_{\mathrm{id}}(k)=I_r.
$$

This is the uncorrected control. Its canonical wire identity is `identity`.

### Global-unitary

One matrix $U_{\mathrm{global}}$ is selected on the final construction mesh by minimizing
an aggregate frame-mismatch objective. The same matrix is used at every other
construction point and every direct-evaluation point:

$$
F_{\mathrm{global}}(k)=F'_{r,L}(k)U_{\mathrm{global}}.
$$

Selection occurs only at $M=2049$. A mesh-scoped status at $M=513$ or $M=1025$
describes reuse, not a new fit. Its canonical wire identity is `global-unitary`.

### Pointwise-unitary

An independent polar-Procrustes matrix is selected at each construction-mesh point:

$$
U_{\mathrm{point}}(k)
 = \mathcal{P}\!\left(F_{r,L}^{\prime\dagger}(k)F_r(k)\right),
$$

where $\mathcal{P}$ is the unitary polar factor. Selection is repeated separately on
each construction mesh; selected matrices are not interpolated to the shifted evaluation
mesh. Its canonical wire identity is `pointwise-unitary`.

### Known-inverse-oracle

For the synthetic control, the inverse of the imposed gauge transformation is known:

$$
U_{\mathrm{inverse}}(k)=G_{r,L}^{-1}(k)=G_{r,L}^\dagger(k).
$$

This control tests recovery against the analytic construction. It is not an admissible
fitted solution. Its canonical wire identity is `known-inverse-oracle`.

## Transport is common to all four gauge alignments

Closed-loop parallel transport acts on the analytic reference frame rather than being
appended to pointwise-unitary selection. The same transport construction and evidence
are used when assessing all four gauge alignments. Gauge alignment and transport are
separate numerical operations and separate potential error sources.

## Gauge alignments are not error channels

Identity, global-unitary, pointwise-unitary, and known-inverse-oracle name retained-space
basis choices. After one such choice has produced a represented operator, locality
analysis distinguishes the interpolation, truncation, and total error channels. Those
diagnostic channels satisfy a pointwise decomposition, but maxima over reciprocal space
must not be added or interpreted as separate physical mechanisms.

## Rank deficiency and numerical failure

A rank-deficient aggregate overlap means that global-unitary selection is not defined
under the frozen cutoff. Downstream global-unitary locality values are absent rather than
zero. A deficient pointwise solve suppresses the affected pointwise-unitary result.

A deficient neighbor overlap during frame transport has a different meaning: transport
stops because the next frame cannot be connected under the declared numerical-rank rule.
Backend nonconvergence, nonfinite arithmetic, failed integrity checks, and failure of the
known-inverse-oracle control remain distinct typed outcomes. They are not collapsed into
a generic failure state, and exception messages or tracebacks are not scientific
evidence.

## Rank-specialization boundary

The orthonormal Procrustes, transport, finite-periodic, interpolation, support-tail, and
matrix-field mechanisms are rank-generic where their own contracts admit the operands.
That numerical reuse does not merge the rank-specialized scientific studies.

At rank one, the represented Hamiltonian is scalar and satisfies
$U^\dagger H U=H$ for every $U\in U(1)$. Identity, global-unitary,
pointwise-unitary, and known-inverse-oracle therefore do not define four distinct
operator-locality cases. The D1 analytic orbital and attack coordinates also divide by
$r-1$, so rank one is correctly owned by the separate scalar Fourier-locality study.

At rank two, non-Abelian gauge alignment is meaningful and the generic orthonormal
mechanisms can be reused. The retained rank-two study nevertheless owns a different
analytic model, numerical controls, verification contract, and evidence identity. In
addition, mechanically extending the D1 nearest-neighbor brickwork to rank two leaves
alternating layers without a pair to rotate. Rank two must not be added to D1 v1 merely
by widening an accepted-rank tuple.

The D1 tuple $r\in\{3,4,8,16\}$ is an intentional protocol and evidence boundary. It is
not a statement that the Optimization or PhysKit numerical kernels are incapable of
rank two. See the [rank-specialization crosswalk](rank-specialization-crosswalk.md).

## Boundary of future studies

The right action of a gauge alignment is fiberwise, whereas reciprocal meshes, Fourier
indices, interpolation domains, and support geometry depend on spatial dimension. A
future 2-D or 3-D specialization must choose those geometries explicitly and cannot
inherit the 1-D interval support or odd-mesh Nyquist disposition.

The current reference and attacked frames are orthonormal, so their gauge group is
$U(r)$. A nonorthonormal retained basis requires a positive-definite fiber metric and a
separate metric-aware definition of adjoint, isometry, Procrustes alignment, conditioning,
and recovery. Treating that problem as an optional parameter of the present orthonormal
actions would obscure a scientific change of contract; no such generalization is
implemented.

## Present evidence level

The current producer constructs the declared analytic Hamiltonian, evaluates the four
gauge alignments, transports the common reference frame, analyzes odd-mesh Fourier
locality, and returns correlated typed calculation records. A bounded independent
reference analyzer directly reconstructs the analytic-model and attack core invariants.
A separate bounded direct-sum reference reconstructs all four Fourier controls on all
three construction meshes, compares shifted interpolation and support tails for every
alignment, and verifies the oracle's analytic
$|R|\le2$ support within its declared tolerance. A third bounded reference reconstructs
the global polar selection through an Hermitian eigendecomposition and the pointwise
selections directly from the analytic attack, comparing rank, residual, integrity, and
selected-unitary evidence. A fourth bounded reference directly reconstructs the exact
constant-frame closed route, link ranks, zero closure phases, and identity closure
actions on all construction meshes. None invokes the corresponding producer scientific
actions.

Those bounded comparisons are not the protocol's complete independent reference
calculation and do not establish support-truncated and total-error fields, error-channel
decompositions, refinement, or
result-byte verification. No byte-owning verifier or retained higher-rank
result has been admitted, and the complete 16-case runtime and 4 GiB memory ceilings
remain unestablished. The analytic family does not establish material validity. No
higher-rank result from this package is scientifically validated, formally checked,
sealed, published, or released.
