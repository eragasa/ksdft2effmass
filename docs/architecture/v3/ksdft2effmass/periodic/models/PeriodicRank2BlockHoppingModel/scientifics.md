# `PeriodicRank2BlockHoppingModel` scientific interpretation

The model identifies an infinite ordinary periodic Hamiltonian through a finite inventory
of matrix-valued coefficients indexed by integer lattice displacements and an explicit
direct-lattice geometry. The integer index \(\mathbf n\) and physical direct-lattice
displacement \(\mathbf R_{\mathbf n}=A\mathbf n\) are correlated but distinct values.
The model is not a sampled periodic-fiber Hamiltonian field, a finite supercell matrix, a
gauge choice, or a truncated comparison result.

Exact Hermiticity is an admissibility condition for the scientific model. A transform
whose coefficients satisfy Hermiticity only within floating-point tolerance is useful
numerical evidence but is not silently reclassified as this exact model.

The role enum distinguishes a controlled model, material reference, and reduced model.
None of those roles asserts fitting completion, numerical convergence, scientific
validation, or publication acceptance.

The model's ordered retained basis is necessary but not sufficient for orbital- or
MLWF-resolved locality. A locality analyzer must receive a separately correlated basis
embedding, and an MLWF-resolved analyzer must additionally receive localization and
gauge provenance. The model does not choose between cell-block, orbital-resolved, and
MLWF-resolved interpretation.

Passing model tests establishes software enforcement of these declarations only.
