# Scientific boundary

Non-orthogonal 2-D experiments must declare a full-rank primitive matrix `A`, reciprocal
matrix `2*pi*A^(-T)`, Gram matrix `G=A^T A`, reduced-coordinate convention, physical
bond orbit, integer point group, and metric-shell rule. Coordinate radius is not a
physical distance unless implied by `G`.

PhysKit owns reusable lattice and metric primitives. Each KSD experiment owns its parent,
retained space, gauge family, support acceptance, thresholds, error channels, verifier,
evidence, and interpretation. Results remain conditional on the selected lattice and do
not imply arbitrary-lattice or material validity.
