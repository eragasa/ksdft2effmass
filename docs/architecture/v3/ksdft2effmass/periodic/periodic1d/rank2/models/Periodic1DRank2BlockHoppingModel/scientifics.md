# `Periodic1DRank2BlockHoppingModel` scientific interpretation

The model identifies an infinite ordinary one-dimensional periodic Hamiltonian with two
retained primitive-cell states. Rank two refers to the retained coefficient-block size,
not the algebraic rank of an individual coefficient matrix.

The primitive period and its physical unit are part of the scientific geometry. The
provider hopping representation separately owns energy units, energy reference, basis
identity, integer lattice displacements, and coefficient storage. Physical direct-
lattice displacements are geometry-derived values and are not independent coefficient
indices.

Exact conjugate-displacement support is a model-admission condition. Approximate
Hermiticity from a floating-point Fourier transform remains representation-level evidence
until an explicit construction policy promotes it.

## Relationship to the maintained legacy representation

`BlockHoppingModel1D` answers which matrix coefficients a finite numerical transform or
historical study retained. It may have arbitrary square block rank and does not assert
complete conjugate support, exact Hermiticity, physical direct-lattice geometry, a model
role, an ordered basis identity, or an energy reference.

This model answers a narrower and stronger question: whether an exactly identified
one-dimensional rank-two ordinary hopping representation is admissible as one KSD
scientific model. The stronger contract does not make the legacy representation
incorrect or obsolete. It makes representation production, cyclic conversion, and
scientific-model admission separate stages.

Historical studies remain bound to their original representation contract until their
explicit migration demonstrates parity and provenance continuity. A migrated study may
retain its source and cyclic-conversion evidence while using this model for new analysis;
it must not relabel the old object as though it had always carried the new metadata.

The model asserts neither numerical convergence nor scientific validation.
