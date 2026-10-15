# Periodic 2-D implementation architecture

## Source mapping

The package mirror groups experiment families beneath the periodic-2D model-adequacy
source path.

- Planned source root: `experiments/model-adequacy/periodic2d/`.
- Architecture root: `docs/architecture/v2/experiments/model-adequacy/periodic2d/`.
- Isotropic task: `docs/tasks/dev/experiments/isotropic2d/`.
- Anisotropic task: not yet opened.

## Dependency direction

Two-dimensional experiment children compose inward geometry and numerical owners.

- PhysKit owns reusable intrinsic and embedded-plane lattice records and physics-semantic adapters; primitive arithmetic inside a physics-semantic diagnostic does not alone determine ownership.
- Numerics owns reusable unit-free finite Fourier/Bloch sums, invariant-diagnostic kernels with explicit public contracts, deterministic finite-orbit enumeration, and interval or enclosure primitives and arithmetic validity conditions when extracted through reviewed contracts.
- Optimization owns reusable unit-free fitting, quadratic construction, support functions, intersection-feasibility witnesses, and capability-specific strict-separation certificate mathematics for explicitly supported set representations through exact reviewed contracts.
- KSD installed analysis may own reviewed domain-specific feature construction, but not competing generic kernels; KSD may consume Numerics or Optimization directly when no physics adapter is needed.
- Child experiments own features, units, normalization, domains, thresholds, metric selection, certificate-method bindings, experiment data and retained evidence instantiating owner-defined validity conditions, evidence wrappers, premise-failure policy, dispositions, and interpretation.
- Installed packages never import the child experiment packages.

## Child implementation status

Implementation status is reported by each child rather than aggregated into a false
package capability.

- Isotropic 2-D has architecture and task planning but no maintained experiment source.
- Anisotropic 2-D has architecture identity only.
- No shared module or class has been selected.
- Future module and class architecture will be created only with matching source contracts.

## Verification

Each child must own a verifier independent of its producer.

- Geometry and orbit reconstruction are checked directly.
- Loss and threshold membership are reconstructed.
- Experiment inputs and retained premise evidence are reconstructed, and the owner-defined certificate relationships are checked independently of the producer.
- Evaluation-only roles are checked for noninterference.
- Child-specific tests and exact node mappings belong below the child package.
