# PRF-90: Agentic-Workflow Proof Track

[Proof registry](../proof-status.md) · Separate from the physical proof packages

## Status

`proposed`: candidate workflow invariants exist, but they do not constitute proved software or scientific properties.

## Objective

Develop mathematical statements about authorization, marking preservation, replay, provenance completeness, and failure propagation for the agentic workflow without mixing those results with semiconductor physics.

## Authority and prerequisites

- Accepted workflow semantics and versioned workflow contracts.
- Explicit state-transition, authorization, evidence, and replay definitions.
- Recorded distinction between deterministic software behavior and human scientific decisions.

## Decomposition

| ID | Obligation | Status | Prerequisites | Owner |
|---|---|---|---|---|
| `PRF-90.01` | Authorization safety: no transition occurs without the authority required by its declared boundary. | `proposed` | Formal authorization and transition relation | [Agentic-workflow proof program](../programs/agentic-workflow-proof-program.md) |
| `PRF-90.02` | Marking preservation: accepted state invariants survive permitted transitions. | `proposed` | Formal marking invariants | Same program |
| `PRF-90.03` | Replay determinism under fixed inputs, versions, and deterministic transition semantics. | `proposed` | Replay identity and nondeterminism model | Same program |
| `PRF-90.04` | Provenance completeness for declared artifact and decision dependencies. | `proposed` | Provenance graph and completeness criterion | Same program |
| `PRF-90.05` | Correct failure propagation without converting software failure into scientific disposition. | `proposed` | Failure classes and propagation rules | Same program |

## Completion criteria

- Every theorem identifies the exact workflow model and version it governs.
- Human decisions are inputs or boundary conditions, not inferred transition results.
- Replay claims state all permitted nondeterminism.
- Provenance completeness is defined relative to a declared schema and dependency relation.
- No workflow theorem is represented as evidence of physical correctness.

## Exclusions

- This package does not prove semiconductor, operator-reduction, or numerical claims.
- Passing tests does not prove the workflow model mathematically complete.
- Workflow determinism does not establish scientific validity.
