# Scientific Workflow architecture

## Responsibility

The scientific Workflow architecture separates executable operations, immutable
composition definitions, represented runs, and control-plane behavior.

- A `Task` is one executable operation over already-bound ResultObjects and explicit
  execution context.
- A `Workflow` is one definition-only composition of run-scoped Task instances.
- A `NestedWorkflowTask` is the explicit Task adapter for controlled invocation of one
  child Workflow.
- A `WorkflowRun` is represented immutable run state and history; it is not the
  Workflow definition or an execution engine.

This separation prevents Workflow definitions from acquiring fake `execute` methods,
member Tasks from inventing their own activation or authority, and nested runs from
reusing a parent Task context.

## Nominal contracts

The Task and Workflow architecture uses only nominal ABCs. It does not expose `Task`
or `Workflow` structural protocols or compatibility aliases.

- `AbstractTask` defines the generic executable engine-node boundary.
- `AbstractScientificTask(AbstractTask)` identifies ordinary in-process scientific
  operations.
- `AbstractSimulationTask(AbstractScientificTask)` identifies scientific operations
  requiring the specialized authority-checked external-dispatch path.
- `AbstractWorkflow` defines the graph and composition boundary.
- `NestedWorkflowTask(AbstractTask)` identifies the engine-control node targeting one
  child `AbstractWorkflow`.

A concrete `AbstractWorkflow` is not an `AbstractTask`.
`AbstractScientificTask` and `NestedWorkflowTask` are distinct `AbstractTask`
specializations: the former owns scientific operations, while the latter owns
controlled child-Workflow invocation. `AbstractSimulationTask` further marks the
scientific operations that must enter the existing external-dispatch control plane
rather than ordinary in-process execution.

## Decomposition rule

A Workflow owns identity, Task-instance membership, dependencies, and start-gate
policy. `WorkflowTaskBinding` binds each declared `TaskInstance` to one concrete
`AbstractTask`. `WorkflowExecutionPlan` binds one `AbstractWorkflow` to the complete
ordered set of those bindings and rejects missing, extra, duplicate, or definition-
incompatible Tasks before execution.

Reusable in-process scientific transformations, numerical algorithms, scientific
comparisons, and scientific artifact preparation belong to direct
`AbstractScientificTask` subclasses. Calculator and other external scientific effects
belong to `AbstractSimulationTask` subclasses and remain behind the established
authority, reservation, claim, dispatch-entry, reconciliation, and result-ingress
boundary. Engine-control behavior such as nested invocation belongs to its applicable
`AbstractTask` specialization.

A Workflow and execution plan do not execute or schedule member Tasks, create Task
contexts, persist a run, invoke a calculator, or infer scientific acceptance. The plan
is explicit immutable engine input rather than a registry or discovery mechanism.
Workflow control owns cross-operation responsibilities under explicit authority and
correlation.

Task decomposition remains cohesive: intrinsic DataObject invariants stay on their
records, and one numerical operation is not fragmented into scalar-check Tasks merely
to increase Task count.

## Initial engine boundary

The first `WorkflowEngine` slice consumes a validated `WorkflowExecutionPlan`. Its
`execute_in_process` path resolves one exact activation binding, derives
`TaskExecutionContext`, and invokes only a direct `AbstractScientificTask`. It fails
closed before invocation for `AbstractSimulationTask`, `NestedWorkflowTask`, or an
unknown `AbstractTask` specialization. It does not catch Task exceptions or construct a
durable invocation outcome.

The engine does not search modules, use entry points, consult a mutable registry, infer
a Task from its identity, or accept a structural lookalike. Later simulation and nested
paths remain separate because they require, respectively, authority-checked dispatch
and distinct child-run creation.

## Evidence boundary

Structural conformance and software-verification tests establish only the documented
software contracts. They do not establish that a calculation ran, that a numerical
method is converged, or that a scientific result is validated or accepted.

## Detailed pages

- [Schematic](schematic.md)
- [Implementation](implementation.md)
- [`ksdft2effmass.workflows` package architecture](../workflows/index.md)
- [Task and colored-Petri-net adapter](../workflows/task-and-colored-petri-net-adapter.md)
- [WorkflowRun object model](../workflows/workflow-run.md)
- [Control plane](../workflows/control-plane.md)
