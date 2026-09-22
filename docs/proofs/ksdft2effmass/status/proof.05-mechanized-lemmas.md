# PRF-05: Mechanized Operator Lemmas

[Proof registry](../proof-status.md) · Depends on [PRF-00](proof.00-foundations.md) · Precedes applicable parts of [PRF-10](proof.10-operator-alignment.md), [PRF-20](proof.20-reduction.md), and [PRF-40](proof.40-compatibility.md) · Governed by the [Architecture v1](../../../architecture/v1/index.md)

## Status

`proposed`: the multi-prover architecture is defined and nine prover-neutral contracts from `PRF-05.01` through `PRF-05.08`, including `PRF-05.05a` and `PRF-05.05b`, are frozen. The bounded Lean trial authorized by `PRF-05-HC01` checked `PRF-05.01` with Lean 4 and mathlib `v4.33.0`. The remaining Lean targets and every Isabelle and Rocq target are unencoded; no contract is cross-checked.

## Objective

Independently mechanize the elementary finite-dimensional algebra supporting gauge-equivariant operator comparison in Lean 4, Isabelle/HOL, and Rocq, then compare the three encodings against one theorem contract.

## Authority and prerequisites

- `PRF-00.01` state spaces.
- `PRF-00.02` Bloch-fiber definitions where wavevector-indexed families are used.
- `PRF-00.03` representation maps and gauge actions.
- [Architecture v1](../../../architecture/v1/index.md).
- [PRF-05 theorem catalog](../../../../formal/theorem-catalog/PRF-05.md).
- Exact theorem contracts must be reconciled with applicable specifications and research conventions before encoding.

## Decomposition

| ID | Obligation | Status | Prerequisites | Prose owner |
|---|---|---|---|---|
| `PRF-05.01` | Frame rotation leaves the retained-space projector invariant. | `in development` | `PRF-00.01` | [Gauge equivariance](../operator-alignment/gauge-equivariance.md) |
| `PRF-05.02` | Represented operators transform covariantly under unitary coordinate changes. | `proposed` | `PRF-00.01`, `PRF-00.03` | [Representation maps](../foundations/representation-maps.md) |
| `PRF-05.03` | Identification pullback is covariant under compatible source and target gauges. | `proposed` | `PRF-00.03` | [Aligned impurity operator](../operator-alignment/aligned-impurity-operator.md) |
| `PRF-05.04` | Pristine-space and doped-space aligned differences are covariant and, for unitary identification, equivalent. | `proposed` | `PRF-05.02`, `PRF-05.03`; both common spaces | [Aligned impurity operator](../operator-alignment/aligned-impurity-operator.md) |
| `PRF-05.05a` | The Frobenius norm is invariant under unitary conjugation. | `proposed` | `PRF-05.02`; Frobenius definition | [Gauge equivariance](../operator-alignment/gauge-equivariance.md) |
| `PRF-05.05b` | The induced Euclidean operator norm is invariant under unitary conjugation. | `proposed` | `PRF-05.02`; induced-norm definition | [Gauge equivariance](../operator-alignment/gauge-equivariance.md) |
| `PRF-05.06` | The norm of the difference between conformant equivariant paths is gauge invariant. | `proposed` | `PRF-05.04`, `PRF-05.05a`, `PRF-05.05b` | [Reduction-path commutativity](../reduction/reduction-path-commutativity.md) |
| `PRF-05.07` | A two-point counterexample shows that gauge and real-space truncation need not commute. | `proposed` | `PRF-00.02`, `PRF-00.03` | [Gauge-constrained locality](../reduction/gauge-constrained-locality.md) |
| `PRF-05.08` | Shell Frobenius diagnostics are invariant under declared lattice-local constant unitary rotations. | `proposed` | `PRF-05.02`; shell decomposition | [Gauge-constrained locality](../reduction/gauge-constrained-locality.md) |

Each obligation is tracked independently as `unencoded`, `encoded`, or `checked` in each backend. `cross-checked` requires all three checked encodings plus semantic conformance review.

## Bounded Lean trial evidence

- Authority: resolved checkpoint [`PRF-05-HC01`](../../../../.pi/checkpoints/PRF-05-HC01-lean-trial-toolchain.json).
- Contract: frozen `PRF-05.01` in the [theorem catalog](../../../../formal/theorem-catalog/PRF-05.md#prf-0501-projector-invariance-under-unitary-frame-rotation).
- Source: [`formal/lean/Ksdft2Effmass/Gauge.lean`](../../../../formal/lean/Ksdft2Effmass/Gauge.lean).
- Toolchain: Lean 4 `v4.33.0`; mathlib input revision `v4.33.0`, resolved in `lake-manifest.json`.
- Check: `cd formal/lean && ~/.elan/bin/lake build` completed without warnings or errors. The explicit path is required because the installer could not modify the local shell profile.
- Admission check: no `sorry` or `admit` occurs in the project-owned Lean source. Lean reports only the standard foundational dependencies `propext`, `Classical.choice`, and `Quot.sound` for the exported theorem.

This establishes only that the pinned Lean checker accepts the `PRF-05.01` encoding. It does not establish cross-backend conformance, numerical verification, or scientific validation.

## Completion criteria

- One reviewed theorem contract exists for every `PRF-05.*` identity.
- Lean, Isabelle, and Rocq each check an independently written encoding of every required theorem.
- Cross-backend review confirms compatible fields, spaces, adjoints, norms, quantifiers, index sets, and assumptions.
- Exact toolchain and library versions are retained.
- No admitted theorem, axiom added for convenience, or unchecked placeholder is represented as checked.
- Completion is recorded manually and does not imply scientific validation.

## Exclusions

- No Kohn–Sham, Wannier-localization, continuum-limit, Feshbach, or silicon-specific theorem is included initially.
- No prover backend is authoritative over scientific assumptions.
- No automatic translation among backends is permitted for the independent conformance proofs.
- No Pi extension, Python runtime dependency, or automatic status mutation is introduced.
