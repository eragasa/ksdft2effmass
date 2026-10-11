# Frozen M2 multiband-alignment protocol

## Status and scope

This protocol prospectively freezes the local synthetic M2 calculation for
Conference Paper 1. It is a bounded numerical experiment, not a material
calculation, uncertainty quantification, or scientific acceptance decision. It
runs no external calculator.

The parent is a four-dimensional Hermitian one-dimensional block-hopping model.
The lowest two eigenstates define a retained composite space separated from the
other two states by a frozen minimum-gap requirement. The calculation evaluates
the parent on a 64-point centered half-open reciprocal mesh and on a disjoint
257-point staggered withheld mesh.

## Frozen operations

1. Diagonalize the four-state parent on the training mesh and retain rank two.
2. Construct a reciprocal frame path, close it with identity sewing, and apply
   polar parallel transport.
3. Apply the known nonidentity periodic rotation
   \[
   A(k)=\begin{pmatrix}\cos\theta(k)&-\sin\theta(k)\\
   \sin\theta(k)&\cos\theta(k)\end{pmatrix},\qquad
   \theta(k)=0.30+0.65\sin(2\pi k)+0.30\sin(4\pi k).
   \]
4. Retain invariant projector diagnostics, exact pointwise Procrustes recovery,
   and a distinct constrained family consisting of one global unitary for the
   full path. Pointwise recovery is not identified with the constrained family.
5. Project the parent Hamiltonian into the transported, attacked, pointwise
   aligned, and globally aligned frames.
6. Fourier transform the transported, attacked, and pointwise-aligned paths to
   complete block hoppings.
7. Truncate symmetric hopping ranges 0, 1, 2, 3, 4, 6, and 8. Record omitted
   block norms and maximum spectral errors on training and withheld meshes.
8. Independently reconstruct the finite protocol and compare all retained
   scalar diagnostics and block coefficients at absolute tolerance `1e-11`.

## Frozen controls

All numerical controls and all parent blocks are encoded in `input.json`.
Training values determine frames, alignments, transforms, and truncations.
Withheld values evaluate only the already fixed finite-range models and cannot
change the parent, attack, frames, ranges, thresholds, or reported figure-data
selection.

The protocol requires an external gap of at least `0.5` in the declared unit,
a neighboring/closure overlap singular value strictly greater than `0.8`,
transform and Hermiticity tolerances of `1e-12`, and independent verification
tolerance of `1e-11`.

The reusable definition accepts the full declared rank-two rotation family,
including identity-valued controls. “Known nonidentity attack” refers to this
retained instance and its explicitly frozen coefficients, not to every generic
M2 definition.

## Evidence boundary

A passing calculation may establish only the encoded finite-mesh facts:
projector invariance under the known gauge attack, pointwise recovery for this
constructed attack, the limitation of the one-global-unitary family, and the
gauge dependence of block-hopping locality and finite-range errors. It does not
establish a general alignment optimizer, continuum convergence, transferability,
material validity, topological classification, or uncertainty bounds.

`source.sha256` binds the M2 scripts and the direct package modules used for
frames, alignment, transforms, diagnostics, quantities, and serialization.
`software.json` separately records library versions. These byte digests detect
inconsistency with the retained manifest; they do not prove chronology, and a
dirty-worktree marker is not replaced by a claim of a clean release snapshot.
