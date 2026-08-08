---
name: design-data-action-objects
description: Assigns reusable software behavior and invariants among DataObjects, ResultObjects, ActionObjects, serializers, Workflows, and narrowly justified free functions.
---

# Design DataObject and ActionObject Boundaries

## Purpose

Use this skill when adding a nontrivial object model, changing public object
boundaries, or deciding which object should own reusable behavior. It supplies
architecture guidance only; it does not choose scientific meaning or authorize
implementation.

## Load first

Read `references/data-action-architecture.md` for the detailed rules and
checklist.

## Ownership rules

- A **DataObject** represents immutable or operationally immutable state. It owns
  intrinsic invariants of its fields and only contract-authorized
  canonicalization.
- A **ResultObject** is a DataObject that represents an operation outcome,
  structured findings, or derived state. It records a result but does not
  perform the operation.
- An **ActionObject** owns a reusable operation, policy, analysis,
  transformation, comparison, validation, serialization, or external boundary.
  It normally exposes `execute(...)` and avoids hidden mutable state.
- A **serializer ActionObject** owns serialization, deserialization, and
  wire-format mechanics. Wire-format validity remains distinct from scientific
  validity.
- A **Workflow** is warranted only for a genuine reusable multi-step composition
  with explicit inputs, outputs, dependencies, and execution meaning.
- A small cohesive **free function** is acceptable only when no domain object
  owns the behavior and a class would add no meaningful contract.

Prefer concrete public records and composition. Do not introduce nominal
DataObject or ActionObject base classes without a demonstrated polymorphic
requirement.

## Decision table

| Question | Owner |
|---|---|
| Is one field intrinsically valid? | DataObject |
| Are two independently valid objects compatible? | ActionObject |
| Does an operation apply tolerance, units policy, or algorithm selection? | ActionObject |
| Is this an operation outcome or structured finding? | ResultObject |
| Is this a wire-format conversion? | Serializer ActionObject |
| Is this a reusable multi-step computation? | Workflow, only when genuinely warranted |
| Is the behavior cohesive but ownerless and class-free? | Narrow free function |

## Essential prohibitions

- Do not put external execution, persistence, numerical policy, scientific
  acceptance, or unrelated cross-object validation on a DataObject.
- Do not add `to_json`, `from_json`, `to_dict`, or equivalent persistence methods
  to DataObjects unless an accepted public contract explicitly assigns them.
- Do not hide tolerances, unit policy, scientific acceptance, or algorithm
  choice in module-level validators or generic helper modules.
- Do not create a Workflow merely to own an integration test or a one-time
  sequence.
- Do not require speculative Rust or other language mappings. Consider them only
  for an accepted cross-language contract, shared serialized representation,
  authorized implementation task, or concrete portability requirement.
- Distinguish the modeled subject, mathematical object, numerical
  representation, and software implementation. Structural software conformance
  does not establish numerical verification, scientific validation, uncertainty
  quantification, physical correctness, or human acceptance.

## Stop boundary

Return the proposed ownership decomposition, its contract-relevant reasons, and
any unresolved public or scientific decision. Stop without implementation when
accepted authority does not determine a required boundary.
