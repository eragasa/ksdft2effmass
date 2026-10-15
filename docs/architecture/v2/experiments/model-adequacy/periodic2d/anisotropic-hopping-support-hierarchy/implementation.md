# Anisotropic 2-D implementation architecture

## Planned source

The family will begin as experiment-owned composition after its scientific protocol is
reviewed.

- Planned source: `experiments/model-adequacy/periodic2d/anisotropic-hopping-support-hierarchy/`.
- Architecture: `docs/architecture/v2/experiments/model-adequacy/periodic2d/anisotropic-hopping-support-hierarchy/`.
- Task path: not yet selected.
- No source module or public class exists.

## Ownership

Implementation must consume reusable owners without hiding experiment-specific
anisotropy policy in generic helpers.

- PhysKit owns reusable lattice and metric primitives.
- Numerics owns reusable unit-free finite-periodic Fourier capabilities through reviewed
  contracts.
- Optimization may own reviewed unit-free quadratic kernels.
- The experiment owns symmetry acceptance, directional supports, channels, controls, evidence, and interpretation.

## Future source decomposition

Module and class architecture will be authored only after source responsibilities are
selected.

- Immutable definition ownership must be explicit.
- Producer and verifier must remain separate.
- Schemas and serializers must remain strict.
- Results must enforce evidence/disposition correlation.
- Detailed equations and algorithm references must be concentrated under the implementing `ClassName` pages.

## Evidence status

The selected family currently has no implementation evidence.

- No software tests exist.
- No numerical verification exists.
- No retained run exists.
- No scientific validation or uncertainty quantification is claimed.
