# Non-orthogonal periodic 3-D model-adequacy experiments

This subtree contains three-dimensional experiment families whose primitive direct-
lattice basis is non-orthogonal. It is separate from `periodic3d/` so orthogonal and
non-orthogonal geometry do not become implicit cases of one version contract.

Current family:

- [`band-equivalence-versus-hopping-locality/`](band-equivalence-versus-hopping-locality/)
  — silicon-inspired diamond-basis rank-two representation cost, with separate
  FCC/simple-cubic Bravais controls.

PhysKit owns reusable lattice, reciprocal, metric, and finite-domain primitives. These
experiments own their physical bond orbits, metric-shell acceptance, parameter grids,
thresholds, verification, evidence, resource policy, and interpretation. No general
Bravais-lattice API, immutable experiment version, retained run, or material claim is
established here.
