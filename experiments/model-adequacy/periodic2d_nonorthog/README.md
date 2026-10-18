# Non-orthogonal periodic 2-D model-adequacy experiments

This subtree contains two-dimensional experiment families whose primitive direct-lattice
basis is non-orthogonal. It is separate from `periodic2d/` so orthogonal and
non-orthogonal geometry do not become implicit cases of one version contract.

Current family:

- [`band-equivalence-versus-hopping-locality/`](band-equivalence-versus-hopping-locality/)
  — graphene-inspired honeycomb-basis rank-two representation cost, with separate
  triangular/square Bravais controls.

PhysKit owns reusable lattice, reciprocal, metric, and finite-domain primitives. These
experiments own their physical bond orbits, metric-shell acceptance, parameter grids,
thresholds, verification, evidence, and interpretation. No arbitrary-lattice API,
immutable experiment version, retained run, or material claim is established here.
