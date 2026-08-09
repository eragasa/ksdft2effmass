# Task graph and selection-state architecture decision

Decision identity: `harness.simplification.task-control.task-graph-selection-state`

Input revision: `26d67b809de0dff8f217a09324f3369d7477cac8`

Controlling Task at decision time: `harness.simplification.control.task-catalog-reconciliation`

Decision status: resolved by current human authority

## Decision question

When Tasks represent recursive decomposition and prerequisites, should the control plane retain a chain that also catalogs Tasks, or allocate mutable activation state separately?

## Options presented

- **A — Full chain plus Tasks:** retain chain membership, order, and activation alongside Task-local hierarchy and prerequisites.
- **B — Task-only recursive control:** remove chains and store active-descendant state in root Tasks.
- **C — Task graph plus minimal selection state:** Tasks exclusively own identity, hierarchy, prerequisites, lifecycle status, and decomposition; a separate minimal record owns only `active_task`, explicit activation receipts, and automatic-successor policy.
- **D — Reconsider or defer.**

## Human response

> C

## Normalized decision

**Selected: C — Task graph plus minimal selection state.**

A full chain is not retained as a second Task catalog. Task records are the complete Task graph. A separate minimal selection-state record owns mutable activation facts and references Tasks without duplicating their hierarchy, prerequisites, scope, lifecycle status, or sequence.

## Consequences

- The active `harness.simplification.control.task-catalog-reconciliation` Task is superseded because its objective would create or preserve a competing catalog.
- The current chain remains the operational authority only until a separately authorized migration implements the selected architecture.
- No implementation Task is activated by this decision.
- A future bounded migration must define the minimal selection-state schema and path, migrate the remaining Markdown-backed Task records to JSON where authorized, update `TaskStateInspector` and projections, preserve historical chain evidence, and provide compatibility or rollback behavior.
- Automatic successor activation remains disabled.

## Boundaries

This decision does not authorize source implementation, chain deletion, Task-record migration, SQLite, persistence APIs, dependency changes, historical rewriting, publication, scientific work, external execution, release action, or automatic successor activation. Those require a separately defined and explicitly activated Task.
