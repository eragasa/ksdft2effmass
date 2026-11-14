# `study`

## Purpose and status

This implemented namespace owns reusable KSD study identity and thin orchestration
contracts. A study correlates one exact scientific model with a named investigation. It
is not a DFT, molecular-dynamics, or electronic-structure calculator.

The namespace does not own named FCC, BCT, diamond, simple-cubic, material,
multi-model-comparison, or retained-execution policy. Those compositions remain under
`calculations/` or `experiments/`.

## Child map

- [`periodic`](periodic/index.md): dimension-neutral periodic study and orchestration
  bases.
- [`periodic1d`](periodic1d/index.md): one-dimensional base and rank-two specialization.
- [`periodic2d`](periodic2d/index.md): two-dimensional base and rank-two specialization.
- [`periodic3d`](periodic3d/index.md): three-dimensional base and rank-two specialization.

## Ownership boundary

A base study contains one exact model. Comparison among models or studies must be an
explicit higher-level study composition owned by a named calculation. Study construction
performs no external execution, persistence, verification, scientific acceptance, or
evidence promotion.
