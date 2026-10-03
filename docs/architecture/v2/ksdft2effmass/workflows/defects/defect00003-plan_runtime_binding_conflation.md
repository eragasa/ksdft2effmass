# DEFECT00003: declarative plan and runtime binding conflation

## Status

Closed after implementation, local software verification, and independent review
with no blocking findings.

## Consolidated scope

This record consolidates the original shallow-plan-immutability finding with the later
observation that the proposed definition-snapshot plan still retains live
`AbstractTask` adapters.

## Problem

The former and initially proposed `WorkflowExecutionPlan` boundaries conflated declarative,
immutable Workflow planning with process-local executable bindings. Snapshotting Task
and Workflow definitions stabilizes identities and routes, but retaining a live adapter
inside `WorkflowTaskBinding` means the plan still contains behavior and dependencies
that a frozen dataclass cannot make deeply immutable.

The proposed operational-immutability convention constrains maintained owners but does
not make the declarative plan independent of runtime objects. As a result, the plan
cannot honestly serve as both a frozen definition artifact and a container of live
execution behavior.

## Evidence

- The former `WorkflowTaskBinding` retained one concrete `AbstractTask` object.
- The former `WorkflowExecutionPlan` retained one concrete `AbstractWorkflow` object.
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

## Implementation evidence

`WorkflowExecutionPlan` now contains only immutable generic definitions and nested
Workflow targets. `WorkflowExecutionBindings` separately owns process-local adapters
and effects. Their constructors enforce complete ordered identity, definition, route,
and nested-target agreement. `WorkflowEngine.execute_in_process` accepts only bindings
and activation; it performs no registry lookup or discovery. Focused plan, binding,
and engine tests pass locally, including plan independence from mutable runtime-owner
state.

## Evidence boundary

This separation establishes software ownership and reproducible declarative
correlation. It does not by itself establish deterministic external effects, numerical
reproducibility, scientific validation, or acceptance.
