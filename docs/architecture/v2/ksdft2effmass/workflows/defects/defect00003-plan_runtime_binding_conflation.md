# DEFECT00003: declarative plan and runtime binding conflation

## Status

Architectural contracts documented; coordinated implementation remains required before
introducing the first concrete periodic Workflow.

## Consolidated scope

This record consolidates the original shallow-plan-immutability finding with the later
observation that the proposed definition-snapshot plan still retains live
`AbstractTask` adapters.

## Problem

The current and proposed `WorkflowExecutionPlan` boundaries conflate declarative,
immutable Workflow planning with process-local executable bindings. Snapshotting Task
and Workflow definitions stabilizes identities and routes, but retaining a live adapter
inside `WorkflowTaskBinding` means the plan still contains behavior and dependencies
that a frozen dataclass cannot make deeply immutable.

The proposed operational-immutability convention constrains maintained owners but does
not make the declarative plan independent of runtime objects. As a result, the plan
cannot honestly serve as both a frozen definition artifact and a container of live
execution behavior.

## Evidence

- The current `WorkflowTaskBinding` retains one concrete `AbstractTask` object.
- The current `WorkflowExecutionPlan` retains one concrete `AbstractWorkflow` object.
- A bounded in-memory reproduction changed Workflow identity observed through an
  already-created frozen plan.
- The proposed architecture removes the live Workflow owner but still retains one
  explicit concrete `AbstractTask` adapter in each binding.
- The proposed operational-immutability section acknowledges that Python cannot prove
  the absence of hidden mutation in an arbitrary adapter or its dependencies.

## Consequence

A plan described as immutable can still expose process-local behavioral change after
compilation. Persisting, comparing, hashing, replaying, or reviewing such a plan would
mix stable declarative meaning with runtime object identity and mutable dependencies.

## Persistent correction

The accepted [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md) and
[`WorkflowExecutionBindings`](../WorkflowExecutionBindings/index.md) contracts separate
the two concerns explicitly:

- `WorkflowExecutionPlan` is a concrete frozen declarative DataObject containing the
  immutable `WorkflowDefinition`, ordered Task instances, immutable Task-definition
  snapshots, routes, dependencies, and gate policy. It contains no executable adapter.
- `WorkflowExecutionBindings` is a separate process-local concrete frozen DataObject
  correlating every planned Task instance with one explicit route-compatible adapter.
- `WorkflowExecutionPlanConstructor` owns declarative plan compilation.
- `WorkflowExecutionBindingsConstructor` owns complete ordered binding closure and
  exact definition/route agreement against one plan.
- `WorkflowEngine` receives the exact `WorkflowExecutionBindings` object, reads its
  contained plan, and performs no separate plan correlation, registry lookup,
  discovery, entry-point loading, or identity-based inference.

Runtime bindings need not be serialized or treated as durable scientific state. Their
adapters must still obey the applicable operational-immutability contract, but hidden
adapter state can no longer mutate the represented declarative plan.

## Required evidence

Before closure, focused software verification must show that the plan contains no live
Workflow or Task owner, bindings are complete and ordered for exactly one plan,
mismatched definitions and routes fail before execution, mutable adapter state cannot
change plan equality or content, and engine invocation remains explicit without a
registry.

## Evidence boundary

This separation establishes software ownership and reproducible declarative
correlation. It does not by itself establish deterministic external effects, numerical
reproducibility, scientific validation, or acceptance.
