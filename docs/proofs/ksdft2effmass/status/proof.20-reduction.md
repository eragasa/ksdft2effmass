# PRF-20: Reduction

[Proof registry](../proof-status.md) · Depends on [PRF-00](proof.00-foundations.md) and applicable parts of [PRF-10](proof.10-operator-alignment.md) · Precedes [PRF-30](proof.30-bounds.md) and parts of [PRF-40](proof.40-compatibility.md)

## Status

`proposed`: reduction statements and proof sketches exist, but locality, excluded-space, asymptotic, and path-consistency assumptions remain to be established.

## Objective

Define and analyze the transformations from aligned atomistic operators to localized, truncated, excluded-space, and continuum representations without conflating coordinate changes with operator approximations.

## Authority and prerequisites

- `PRF-00.03` reduction-map semantics.
- `PRF-10.02` gauge-equivariance conditions.
- `PRF-10.03` aligned impurity operator for dopant reductions.
- Applicable continuum, multivalley, and impurity assumptions under `docs/research/`.

## Decomposition

| ID | Obligation | Status | Prerequisites | Owner |
|---|---|---|---|---|
| `PRF-20.01` | Characterize the gauge dependence of locality and define the restricted gauge class under which spatial truncation is interpreted. | `proposed` | `PRF-00.03`, `PRF-10.02` | [Gauge-constrained locality](../reduction/gauge-constrained-locality.md) |
| `PRF-20.02` | Derive the excluded-space/Feshbach operator and correction bound with explicit energy, resolvent, Hermiticity, and resonance assumptions. | `proposed` | `PRF-00.01` | [Feshbach reduction](../reduction/feshbach-reduction.md) |
| `PRF-20.03` | Establish atomistic-to-continuum consistency under declared scale separation, band expansion, and multivalley assumptions. | `proposed` | `PRF-10.03`; applicable part of `PRF-20.01` | [Atomistic-to-continuum](../reduction/atomistic-to-continuum.md) |
| `PRF-20.04` | Distinguish equivariance from commutativity and bound differences between declared reduction paths. | `proposed` | `PRF-00.03`, `PRF-10.03`, applicable reduction maps | [Reduction-path commutativity](../reduction/reduction-path-commutativity.md) |

## Completion criteria

- Localization and truncation are treated as distinct operations.
- Every reduction identifies the changed state space, approximation, and residual.
- Feshbach statements distinguish real off-spectrum reductions from open-system or resonance continuations.
- Atomistic-to-continuum claims state the scale-separation and silicon-specific multivalley assumptions.
- Path comparisons use common inputs, alignment, energy references, and compatible norms.

## Exclusions

- No universal or gauge-independent crossover radius is asserted.
- No continuum validity follows solely from fitting one observable.
- No excluded-space correction is assumed small without a resolvent-distance and coupling estimate.
