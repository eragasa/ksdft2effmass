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
locality, and returns correlated typed calculation records. Software tests exercise
producer behavior only.

There is no independent reference calculation or byte-owning verifier. No retained
higher-rank result has been admitted, and the complete 16-case runtime and 4 GiB memory
ceilings remain unestablished. The analytic family does not establish material validity.
No higher-rank result from this package is scientifically validated, formally checked,
sealed, published, or released.
