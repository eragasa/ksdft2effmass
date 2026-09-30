# PRF-10: Operator Alignment

[Proof registry](../proof-status.md) · Depends on [PRF-00](proof.00-foundations.md) and applicable checked lemmas from [PRF-05](proof.05-mechanized-lemmas.md) when a machine-checked claim is made · Precedes [PRF-20](proof.20-reduction.md), [PRF-30](proof.30-bounds.md), and [PRF-40](proof.40-compatibility.md)

## Status

`proposed`: candidate identification and covariance statements exist, but their assumptions and global compatibility require complete proof and review.

## Objective

Construct a physically interpretable identification between pristine, doped, Wannier, and tight-binding retained spaces so that aligned operator subtraction is mathematically meaningful and gauge covariant.

## Authority and prerequisites

- `PRF-00.01` state spaces.
- `PRF-00.02` Bloch-fiber correspondence where fiberwise constructions are used.
- `PRF-00.03` representation-map and group-action definitions.
- Applicable `PRF-05` results for any claim represented as machine checked; prose development may proceed before mechanization.
- Frozen orbital labels, symmetry conventions, basis ordering, and energy references from the applicable research and specification owners.

## Decomposition

| ID | Obligation | Status | Prerequisites | Owner |
|---|---|---|---|---|
| `PRF-10.01` | Establish existence, unitarity, conditioning, and allowed global regularity of the TB-anchored identification. | `proposed` | `PRF-00.01`, `PRF-00.02` | [TB-anchored identification](../operator-alignment/tb-anchored-identification.md) |
| `PRF-10.02` | Establish gauge actions and equivariance of projection, identification pullback or pushforward, and represented comparison. | `proposed` | `PRF-00.03`, `PRF-10.01` | [Gauge equivariance](../operator-alignment/gauge-equivariance.md) |
| `PRF-10.03` | Define aligned pristine–doped subtraction on one identified space and prove covariance of the resulting impurity operator. | `proposed` | `PRF-10.01`, `PRF-10.02` | [Aligned impurity operator](../operator-alignment/aligned-impurity-operator.md) |

## Completion criteria

- The orientation of every identification map is fixed and consistent.
- The anchor rank and conditioning assumptions are explicit and sufficient.
- Fiberwise constructions include the required smoothness, periodicity, and symmetry conditions.
- The pristine and doped Hamiltonians are placed on a common state space and energy reference before subtraction.
- Covariance statements specify the acting group and use unitarily invariant conclusions only where justified.

## Exclusions

- TB anchoring does not prove that the anchor model is physically complete.
- Gauge covariance does not prove gauge-independent locality or reduction-path commutativity.
- Successful numerical alignment does not itself prove global existence or scientific adequacy.
