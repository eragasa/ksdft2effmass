# PRF-00: Foundations

[Proof registry](../proof-status.md) · Precedes [PRF-10](proof.10-operator-alignment.md), [PRF-20](proof.20-reduction.md), [PRF-30](proof.30-bounds.md), and [PRF-40](proof.40-compatibility.md)

## Status

`proposed`: definitions and candidate constructions exist, but specification agreement and complete foundational proofs have not been established.

## Objective

Fix the state spaces, coordinate representations, Bloch-fiber correspondence, and reduction-map semantics required before operators from different calculations or model classes can be compared.

## Authority and prerequisites

- Applicable versioned physical and numerical specifications under `specification/`.
- Accepted state-space, projection, Wannier, and reduction conventions under `docs/research/`.
- Explicit basis, gauge, energy-reference, unit, and geometry conventions.

## Decomposition

| ID | Obligation | Status | Prerequisites | Owner |
|---|---|---|---|---|
| `PRF-00.01` | Define ambient, retained, Wannier-coordinate, and continuum spaces with required domains and codomains. | `proposed` | Authoritative specifications | [State-space assumptions](../foundations/state-space-assumptions.md) |
| `PRF-00.02` | Establish fixed-rank Bloch-fiber correspondence and identify conditions for smooth, periodic global frames. | `proposed` | `PRF-00.01` | [Bloch-fiber correspondence](../foundations/bloch-fiber-correspondence.md) |
| `PRF-00.03` | Define projection, representation, alignment, subtraction, truncation, and continuum-reduction maps between identified operator spaces. | `proposed` | `PRF-00.01`; applicable parts of `PRF-00.02` | [Representation maps](../foundations/representation-maps.md) |

## Completion criteria

- Every operator and map used downstream has an identified domain and codomain.
- Pristine, doped, TB, Wannier, and continuum representations are distinguished from their abstract operators.
- Fixed-rank, smoothness, periodicity, symmetry, and topology assumptions are explicit.
- Definitions agree with the applicable versioned specifications and research conventions.
- All foundational existence or compatibility claims have complete derivations or are explicitly retained as assumptions.

## Exclusions

- No claim of physical alignment follows from equal matrix dimensions alone.
- No numerical calculation or scientific validation is established here.
- This record does not choose new physical conventions or silently repair specification ambiguity.
