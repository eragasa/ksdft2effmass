# Cross-repository export candidates

`exports/` stages reusable source/design candidates and records completed ownership
transfers whose owner is another Project Koios repository. Files here are not part of
the `ksdft2effmass` Python package,
are not supported `ksdft2effmass` imports, and are not calculation or validation
evidence.

An export may be integrated only through a separately reviewed change in its target
repository. The target repository remains authoritative for naming, package layout,
tests, architecture documentation, provenance, versioning, and release decisions.
`ksdft2effmass` may consume the capability only after an immutable target revision is
selected and its dependency update is separately authorized.

Current target bundles:

- [`optimization`](optimization/README.md) — accepted upstream unit-free quadratic and
  bounded-coordinate APIs plus active affine-quadratic and diagonal-metric candidates;
- [`physkit`](physkit/README.md) — active finite hopping orbit, shell, projection, and
  dimensionful Frobenius-geometry candidates built on accepted lattice primitives.

A candidate that carries physical dimensions or units belongs to PhysKit, not
optimization. Scientific callers must nondimensionalize before passing values into an
optimization contract.

Campaign policy, scientific normalization, thresholds, evidence roles, certificates,
dispositions, retained schemas, and workflow routing remain outside these generic
exports unless a target contract explicitly and appropriately owns them.
