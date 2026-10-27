# Prospective composite-band alignment and locality protocol

## Status

This is the publication-independent prospective successor to the historical Conference
Paper 1 `M2` protocol. It freezes the parity-preserving scientific and numerical meaning
needed for migration, but it is not yet an immutable experiment version and records no
new run or evidence.

The historical files and checksums under
`calculations/ICMSEP2026/conference/paper_1/multiband-alignment/` remain unchanged.

## Parent and state spaces

The selected parent is the exact finite four-dimensional Hermitian periodic-one-
dimensional block-hopping model retained by the historical protocol. At every declared
reciprocal point, the lowest two ordered eigenstates define the retained rank-two
spectral space. The protocol requires the retained/excluded finite-mesh gap to exceed
the declared energy threshold.

Every represented operator records its ambient basis, retained frame, right-action
convention, energy unit, reciprocal coordinate, and energy reference. Operators are
compared only after their state spaces are explicitly aligned.

## Sample roles

- The centered half-open 64-point reciprocal mesh constructs frames, transformations,
  represented operators, Fourier blocks, and finite-range models.
- The disjoint 257-point staggered mesh evaluates already fixed finite-range models.
- Evaluation values cannot alter the parent, frames, attack, transformations, ranges,
  thresholds, or selected result fields.

The maintained schema must call the first role **objective construction** or
**construction**, not training; no statistical model is learned.

## Frame contract

The successor preserves backend-qualified eigenvector-diagonal frames selected from the
lowest two eigenpairs. It retains:

- numerical backend and version;
- ordered eigenvalues;
- input-Hermiticity and residual diagnostics;
- frame orthonormality;
- retained projector and retained/excluded boundary gap; and
- any translated backend failure.

The selected frames are not canonical across eigensolver backends. Within an exactly or
numerically degenerate retained cluster, their coordinates are backend-selected. A
projector-derived deterministic frame would be a different protocol and is not silently
substituted.

## Transport, attack, and alignment

1. Construct the reciprocal frame path with identity sewing.
2. Apply polar parallel transport and distribute the selected closure transformation.
3. Apply the known right-unitary rank-two rotation
   \[
   A(k)=\begin{pmatrix}\cos\theta(k)&-\sin\theta(k)\\
   \sin\theta(k)&\cos\theta(k)\end{pmatrix},
   \qquad
   \theta(k)=0.30+0.65\sin(2\pi k)+0.30\sin(4\pi k).
   \]
4. Select a distinct Procrustes transformation at every construction point.
5. Separately select one unitary from the equal-weight ordered aggregate covariance.

For both Procrustes families, the candidate acts on the right toward the reference. The
owner or temporary local implementation must determine numerical rank from a disclosed
cutoff and reject a rank-deficient covariance without returning a transformation. No
null-space completion is part of this protocol.

Pointwise and one-global-unitary alignment are different feasible families. Neither is
presented as an approximation to the other.

## Represented operators and locality

Represent the parent Hamiltonian in transported-reference, attacked, pointwise-aligned,
and globally aligned frames. Fourier-transform the transported-reference, attacked, and
pointwise-aligned represented paths using the declared finite positive-exponent
convention. Retain complete block families and reconstruct each source path before
truncation.

Apply symmetric hopping ranges `0, 1, 2, 3, 4, 6, 8`. For each range and channel,
retain omitted complete-block norms and maximum construction/evaluation spectral errors.
Locality and truncation are frame-dependent diagnostics, not invariant physical
observables.

## Independent verification

The producer-independent verifier must reconstruct the parent samples, frame/projector
diagnostics, attack, alignment objectives, represented operators, Fourier blocks,
truncations, and evaluation errors without calling the producer Action or an owner
alignment solver. It must independently establish that every accepted pointwise and
aggregate covariance is numerically full rank under the retained cutoff.

Shared BLAS/LAPACK and array-library lineage must be disclosed. Numerical agreement
establishes bounded software behavior only; it does not establish continuum convergence,
material validity, uncertainty bounds, or scientific acceptance.

## Migration and evidence gates

Before assigning `.v1` or retaining a maintained run:

1. close strict input, result, and verification schemas;
2. freeze canonical serialization and method identities;
3. bind exact owner and experiment dependencies;
4. replace temporary numerical selection mechanisms where reviewed owner contracts fit,
   without forwarding facades;
5. migrate the historical 64/257 regression consumer to the maintained result contract;
6. define evidence retention and failure policy; and
7. obtain separate execution authorization.

Open owner replacements are tracked as
[`TECH_DEBT`](../../../../docs/tasks/tech_debt/composite-band-alignment-and-locality/index.md).
