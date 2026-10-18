# Implementation boundary

No general non-orthogonal 3-D experiment framework is selected. Concrete actions consume
PhysKit lattice primitives and project-owned numerical capabilities directly. They must
not duplicate reusable lattice, dual, metric, or finite-domain behavior.

Typed experiment definitions own exact geometry identifiers, bond inventories, sample
roles, resource caps, thresholds, schemas, verification, and evidence policy. Passing
software tests establishes software behavior only.
