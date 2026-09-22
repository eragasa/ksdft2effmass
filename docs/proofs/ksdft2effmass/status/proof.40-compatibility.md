# PRF-40: Compatibility and Model-Class Expressiveness

[Proof registry](../proof-status.md) · Depends on applicable parts of [PRF-00](proof.00-foundations.md), [PRF-10](proof.10-operator-alignment.md), and [PRF-20](proof.20-reduction.md)

## Status

`proposed`: the admissible-set and model-class-distance formulations exist, but certified incompatibility and admissible-gauge conclusions have not been established.

## Objective

Determine whether one declared reduced-model class can satisfy spectral and aligned-operator requirements, and distinguish optimization failure, representation sensitivity, and intrinsic model-class inadequacy.

## Authority and prerequisites

- `PRF-00` state-space and reduction-map definitions.
- `PRF-10.01` and `PRF-10.02` admissible alignment and gauge action.
- Any path-consistency result from `PRF-20.04` needed to compare different constructions.
- Frozen model classes, parameter domains, tolerances, norms, and held-out observables from the applicable scientific owners.

## Decomposition

| ID | Obligation | Status | Prerequisites | Owner |
|---|---|---|---|---|
| `PRF-40.01` | Define spectral- and operator-admissible sets and prove minimum-separation statements under explicit compactness and continuity assumptions. | `proposed` | `PRF-10.01`, `PRF-10.02` | [Spectral–operator compatibility](../compatibility/spectral-operator-compatibility.md) |
| `PRF-40.02` | Define model-class distance on admissible gauge orbits and establish what a nonzero certified residual implies. | `proposed` | `PRF-40.01`; applicable path consistency | [Model-class expressiveness](../compatibility/model-class-expressiveness.md) |
| `PRF-40.03` | Establish a certified incompatibility method that distinguishes a global lower bound from optimizer failure. | `proposed` | `PRF-40.01`, frozen finite computational problem | Proposed proof owner; no dedicated proof unit yet |
| `PRF-40.04` | Define nested model classes and conditions under which residual changes can diagnose a relaxed assumption without claiming unique physical causation. | `proposed` | `PRF-40.02`, declared model hierarchy | [P01 manuscript projection](../../../publications/papers/ksdft2effmass.P01/manuscript.md#residual-guided-model-class-refinement) |

## Completion criteria

- The admissible gauge group is independently declared and computationally reproducible.
- Compactness, continuity, closure, and metric assumptions are explicit.
- Optimizer failure is never used as proof of empty intersection or positive separation.
- Anchor sensitivity is separated from within-anchor fitting residual.
- Nested model-class improvements are tested against held-out constraints and do not imply unique physical explanation without additional evidence.

## Exclusions

- Spectral agreement alone does not establish operator equivalence.
- A flexible alignment is not allowed to absorb unrestricted model error.
- A smaller residual does not by itself validate the added physical terms.
