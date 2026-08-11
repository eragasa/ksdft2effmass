# `ksdft2effmass` proof workspace

This folder separates proof foundations, operator-alignment arguments, reductions, bounds, compatibility results, and research programs. Publication narratives are owned by `docs/publications/papers/`.

The material is provisional. Authoritative physical and mathematical contracts remain in the applicable versioned files under `specification/`. These proof drafts do not override those contracts and do not establish numerical verification, scientific validation, uncertainty quantification, or human acceptance.

## Dependency order

```text
foundations
→ operator alignment
→ gauge-equivariant reduction
→ gauge-constrained locality
→ atomistic-to-continuum reduction
→ error and excluded-space bounds
→ spectral/operator compatibility
→ model-class expressiveness
```

## Architecture and mechanization

- [Multi-prover mechanized-proof architecture](../../architecture/mechanized-proof-system.md)
- [PRF-05 prover-neutral theorem catalog](../../../formal/theorem-catalog/PRF-05.md)
- [PRF-05 mechanized operator lemmas](status/proof.05-mechanized-lemmas.md)

## Foundations

- [State-space assumptions](foundations/state-space-assumptions.md)
- [Bloch-fiber correspondence](foundations/bloch-fiber-correspondence.md)
- [Representation and reduction maps](foundations/representation-maps.md)

## Operator alignment

- [TB-anchored identification](operator-alignment/tb-anchored-identification.md)
- [Aligned impurity operator](operator-alignment/aligned-impurity-operator.md)
- [Gauge equivariance](operator-alignment/gauge-equivariance.md)

## Reduction

- [Gauge-constrained locality](reduction/gauge-constrained-locality.md)
- [Feshbach and excluded-space reduction](reduction/feshbach-reduction.md)
- [Atomistic-to-continuum reduction](reduction/atomistic-to-continuum.md)
- [Reduction-path commutativity](reduction/reduction-path-commutativity.md)

## Bounds

- [Spatial residual and crossover radius](bounds/spatial-residual-and-crossover.md)
- [Operator-to-observable error bounds](bounds/operator-to-observable-errors.md)
- [Continuum fitting and identifiability](bounds/continuum-fitting-identifiability.md)

## Compatibility

- [Spectral–operator compatibility](compatibility/spectral-operator-compatibility.md)
- [Model-class expressiveness](compatibility/model-class-expressiveness.md)

## Publication narratives

- [P01 gauge-equivariant operator framework](../../publications/papers/ksdft2effmass.P01/manuscript.md)
- [P04 impurity extraction and continuum reduction](../../publications/papers/ksdft2effmass.P04/manuscript.md)

## Programs and status

- [Physics proof program](programs/physics-proof-program.md)
- [Agentic-workflow proof program](programs/agentic-workflow-proof-program.md)
- [Claims register](claims-register.md)
- [Proof-package registry, precedence, decomposition, and status](proof-status.md)

## References

- [Bibliography disposition](references/bibliography.md)
- [Reference verification status](references/verification-status.md)
