# Physical interpretation of the alignment study

## Alignment families

Let $F_r(k)$ be the reference frame for the retained rank-$r$ subspace and let
$F'_{r,L}(k)$ be the synthetically attacked frame at circuit depth $L$. The study compares
four feasible right-unitary alignments.

### Identity gauge

The attacked frame is left unchanged:

$$
U_{\mathrm{id}}(k)=I_r.
$$

This is the uncorrected control. Its frozen protocol identifier is `A0`.

### One global unitary

One matrix $U_{\mathrm{global}}$ is selected on the final construction mesh by minimizing
an aggregate frame-mismatch objective. The same matrix is then used at every other
construction point and every direct-evaluation point:

$$
F_{\mathrm{global}}(k)=F'_{r,L}(k)U_{\mathrm{global}}.
$$

The selection is not repeated on refinement or evaluation meshes. A mesh-scoped status
at $M=513$ or $M=1025$ therefore describes application of the unitary selected at
$M=2049$; it does not describe a new fit. Its frozen protocol identifier is `A1`.

### Pointwise unitary alignment

An independent polar-Procrustes matrix is selected at each reciprocal-space point:

$$
U_{\mathrm{point}}(k)
 = \mathcal{P}\!\left(F_{r,L}^{\prime\dagger}(k)F_r(k)\right),
$$

where $\mathcal{P}$ denotes the unitary polar factor. Its frozen protocol identifier is
`A2`.

### Known inverse transformation

For the synthetic control, the exact inverse of the imposed gauge transformation
$G_{r,L}(k)$ is known:

$$
U_{\mathrm{inverse}}(k)
 = G_{r,L}^{-1}(k)
 = G_{r,L}^\dagger(k).
$$

This channel tests recovery against a known answer. Its frozen protocol identifier is
`A3`.

## Transport is common to all four families

Closed-loop parallel transport is applied to the analytic reference frame, not appended
to the pointwise-alignment channel. The same transported reference is used when assessing
all four alignment families. Alignment and transport are therefore separate numerical
operations and separate error sources.

## Rank deficiency and numerical failure

A rank-deficient aggregate overlap means that the global-unitary alignment is not defined
under the frozen cutoff. This is a scientifically admissible outcome: downstream global
alignment and locality quantities are inapplicable rather than zero.

A deficient neighbor overlap during frame transport has a different meaning. Transport
stops because the next frame cannot be connected uniquely under the declared numerical
rank rule. Backend nonconvergence, nonfinite arithmetic, failed decomposition checks, and
failure of the known-inverse control are also recorded separately. These outcomes must
not be collapsed into one generic failure state.

## Present evidence level

The current implementation establishes data structures and transport checks only. It has
not produced a retained higher-rank calculation, established the stated runtime and
memory ceilings, or demonstrated material-level validity. No higher-rank result from this
package is presently scientifically validated, formally checked, sealed, published, or
released.
