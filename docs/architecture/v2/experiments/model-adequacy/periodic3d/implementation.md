# Periodic 3-D implementation architecture

## Source mapping

The package mirror groups three-dimensional model-adequacy families beneath one source
subpackage.

- Planned source root: `experiments/model-adequacy/periodic3d/`.
- Architecture root: `docs/architecture/v2/experiments/model-adequacy/periodic3d/`.
- Isotropic task: `docs/tasks/dev/experiments/isotropic3d/`.
- Anisotropic source: `experiments/model-adequacy/periodic3d/anisotropic-hopping-support-hierarchy/`.

## Dependency direction

Three-dimensional experiments compose inward lattice and numerical owners.

- PhysKit owns reusable full-rank `3 x 3` lattice records and physics-semantic adapters; primitive arithmetic inside a physics-semantic diagnostic does not alone determine ownership.
- Numerics owns reusable unit-free finite Fourier/Bloch sums, invariant-diagnostic kernels with explicit public contracts, deterministic finite-orbit enumeration, and interval or enclosure primitives and arithmetic validity conditions when extracted through reviewed contracts.
- Optimization owns reusable unit-free fitting, quadratic construction, support functions, intersection-feasibility witnesses, and capability-specific strict-separation certificate mathematics for explicitly supported set representations through exact reviewed contracts.
- KSD installed analysis may own reviewed domain-specific feature construction, but not competing generic kernels; KSD may consume Numerics or Optimization directly when no physics adapter is needed.
- Child experiments own features, units, normalization, domains, thresholds, metric selection, certificate-method bindings, experiment data and retained evidence instantiating owner-defined validity conditions, schemas, evidence wrappers, premise-failure policy, dispositions, and interpretation.
- Installed packages never import experiment code.

## Child implementation status

The children are at different design maturity and expose no shared implemented package
contract.

- Isotropic 3-D hopping support has a task and architecture but no source package.
- Simple-cubic band equivalence versus hopping locality has a maintained protocol,
  reusable typed development source, and bounded verified local three-level matrix-free
  tensor calculations; complete diagnostic parity, final retained schemas, formal convergence,
  and retained-evidence actions remain open.
- Anisotropic 3-D has protocol documents but no source modules or classes.
- No general periodic-3D experiment framework has been selected; the reusable
  model-adequacy owner remains bounded to this dimensional replication sequence.

## Verification

Each child must verify geometry, symmetry, losses, evidence, and role isolation through
an independent route.

- Reconstruct lattice and reciprocal conventions.
- Reconstruct signed or signed-permutation orbits.
- Reconstruct quadratics and membership.
- Reconstruct experiment inputs and retained premise evidence, then check the owner-defined certificate relationships and lower bound independently of the producer.
- Reject evaluation data that feed back into decisive controls.
