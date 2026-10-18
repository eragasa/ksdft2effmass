# Isotropic 3-D implementation architecture

## Planned source

The family begins as experiment-owned composition after its exact protocol is reviewed.

- Planned source: `experiments/model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/`.
- Architecture: `docs/architecture/v2/experiments/model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/`.
- Task: `docs/tasks/dev/experiments/isotropic3d/`.
- No source module or public class exists.

## Ownership

The implementation will compose reusable owners without turning cubic experiment policy
into a generic framework.

- PhysKit owns simple-cubic lattice primitives through its general lattice contracts.
- Numerics owns reusable unit-free finite-periodic Fourier behavior through reviewed
  contracts.
- Optimization may own reviewed unit-free quadratic and support kernels.
- The experiment owns cubic orbit meaning, channels, controls, evidence, and interpretation.

## Future source decomposition

Detailed architecture follows source only after responsibilities are selected.

- Definition ownership must be immutable and explicit.
- Producer and verifier must use separate reconstruction paths.
- Schemas and serializers must remain strict.
- Result objects must enforce evidence correlation.
- Detailed mathematics and method references must be concentrated beneath the implementing module and `ClassName`.

## Evidence status

The active task has no implementation or scientific evidence.

- No source package exists.
- No tests exist.
- No retained run exists.
- No silicon or arbitrary-lattice claim is supported.
