# `PeriodicBlockHoppingModel` scientific interpretation

A concrete model identifies an infinite ordinary periodic Hamiltonian through a finite
inventory of matrix-valued coefficients, an explicit direct-lattice geometry, and an
exact ordered basis for coefficient-block rows and columns. The integer support index
\(\mathbf n\), physical translation \(\mathbf R_{\mathbf n}=A\mathbf n\), and basis
coordinates \(\alpha,\beta\) are correlated but distinct values in
\(T(\mathbf n)[\alpha,\beta]\).

The model is not a sampled periodic-fiber Hamiltonian field, finite supercell matrix,
gauge choice, basis embedding, or truncated comparison result. Rank is the number of
retained basis coordinates. Spatial dimension is the number of components in each
lattice displacement. Neither determines the other.

Fixed-rank ownership is expressed by inheritance refinement. In particular, a rank-two
dimensional model is a finite-rank dimensional model with the retained-rank proposition
fixed to two. Block-hopping ownership is a separate capability combined at the concrete
model. This avoids a duplicate dimension-neutral rank-two block-hopping class while
preserving exact dimensional scientific types.

Exact Hermiticity is an admissibility condition for the scientific model. A transform
whose coefficients satisfy Hermiticity only within floating-point tolerance is useful
numerical evidence but is not silently reclassified as this exact model.

`PeriodicModelRole` distinguishes contextual model roles. No role asserts fitting
completion, numerical convergence, validation, certification, or publication
acceptance.

The ordered retained basis is necessary but not sufficient for orbital- or
MLWF-resolved locality. Such an analysis requires separately correlated intracell
embedding and, for MLWF interpretation, localization and gauge provenance. Passing
model tests establishes software enforcement of these declarations only.
