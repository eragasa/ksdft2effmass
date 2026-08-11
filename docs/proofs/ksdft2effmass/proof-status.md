# Proof Status Registry

This registry organizes proof development as a hierarchy of static Markdown work packages. It borrows the useful structure of task records—objective, prerequisites, decomposition, completion criteria, and exclusions—but it is not software-controlled task state.

No JSON, SQLite record, harness command, automatic activation, or generated projection governs these files. Status changes are made explicitly in the relevant Markdown record after the stated proof evidence exists.

## Interpretive precedence

When statements disagree, interpret this proof workspace in the following order:

1. applicable versioned contracts under `specification/`;
2. accepted scientific assumptions and conventions under `docs/research/`;
3. definitions and assumptions in the owning proof unit;
4. proved prerequisites cited by the result;
5. the result's own statement and derivation;
6. corollaries, numerical illustrations, manuscript summaries, and publication projections.

A lower-precedence document may explain or specialize a higher-precedence statement but may not silently redefine it. A manuscript theorem label does not outrank an unresolved assumption or an incomplete prerequisite proof.

## Status vocabulary

| Status | Meaning |
|---|---|
| `proposed` | Claim, definitions, or proof strategy exist, but a complete proof has not been established. |
| `in development` | A proof is being actively constructed and its prerequisites are sufficiently identified. |
| `blocked` | A named missing definition, assumption, prerequisite, or human scientific decision prevents progress. |
| `complete, unreviewed` | A complete derivation is recorded, but independent mathematical review has not been completed. |
| `reviewed` | The derivation and its declared prerequisites passed independent mathematical review. |
| `numerically checked` | Separate numerical evidence agrees under declared conditions; this supplements rather than replaces proof. |
| `retired` | The claim was superseded, merged, or rejected, with the disposition recorded. |

Scientific validation and human publication acceptance are separate from these statuses.

## Proof-package precedence

The package graph is a partial order, not a single sequence:

```text
PRF-00 Foundations
├──→ PRF-05 Mechanized operator lemmas
│    ├──→ PRF-10 Operator alignment
│    ├──→ PRF-20 Reduction
│    └──→ PRF-40 Compatibility
├──→ PRF-10 Operator alignment
│    ├──→ PRF-30 Bounds
│    └──→ PRF-40 Compatibility
└──→ PRF-20 Reduction
     ├──→ PRF-30 Bounds
     └──→ PRF-40 Compatibility

PRF-90 Agentic workflow (separate proof and publication track)
```

`PRF-90` may reuse general definitions of determinism, evidence, or state transition, but it does not depend on the physical foundations and does not establish any physical or numerical theorem.

## Package registry

| Package | Status | Objective | Immediate prerequisites | Record |
|---|---|---|---|---|
| `PRF-00` | `proposed` | Fix state spaces, Bloch correspondence, and reduction-map semantics. | Versioned specifications and research conventions | [Foundations](status/proof.00-foundations.md) |
| `PRF-05` | `proposed` | Independently mechanize elementary operator lemmas in Lean, Isabelle, and Rocq. | Applicable parts of `PRF-00`; approved architecture, inactive implementation | [Mechanized operator lemmas](status/proof.05-mechanized-lemmas.md) |
| `PRF-10` | `proposed` | Construct TB-anchored identification and gauge-covariant impurity extraction. | `PRF-00` | [Operator alignment](status/proof.10-operator-alignment.md) |
| `PRF-20` | `proposed` | Control locality, excluded spaces, continuum reduction, and reduction paths. | Applicable parts of `PRF-00` and `PRF-10` | [Reduction](status/proof.20-reduction.md) |
| `PRF-30` | `proposed` | Convert operator residuals into crossover, observable, and fitting statements. | Applicable parts of `PRF-10` and `PRF-20` | [Bounds](status/proof.30-bounds.md) |
| `PRF-40` | `proposed` | Establish spectral/operator compatibility and model-class expressiveness. | Applicable parts of `PRF-00`, `PRF-10`, and `PRF-20` | [Compatibility](status/proof.40-compatibility.md) |
| `PRF-90` | `proposed` | Develop the separate agentic-workflow proof track. | Declared workflow semantics, not physics results | [Agentic workflow](status/proof.90-agentic-workflow.md) |

## Status rules

1. A parent package does not become `complete, unreviewed` until every required child obligation is complete or explicitly removed from that package's objective.
2. A child may advance before unrelated siblings when all of its own prerequisites are satisfied.
3. Numerical agreement cannot advance a mathematical proof from `proposed` to `complete, unreviewed`.
4. A manuscript projection may authorize proof development, but it cannot mark the projected proof complete.
5. Any change to a theorem's state spaces, gauge group, norm, domain, codomain, or physical interpretation must first be reconciled with the higher-precedence owner.
6. A blocked item must name the exact missing prerequisite rather than use a generic incomplete status.

No package in this registry currently denotes a scientifically validated or human-accepted result.
