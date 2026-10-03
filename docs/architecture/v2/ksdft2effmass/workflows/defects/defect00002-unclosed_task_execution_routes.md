# DEFECT00002: unclosed Task execution routes

## Status

Closed after implementation, local software verification, and independent review
with no blocking findings.

## Consolidated scope

This record consolidates:

- Python's ability to construct one Task satisfying multiple route ABCs;
- the proposed duplication between nominal route inheritance and independently supplied
  `TaskDefinition.execution_kind`;
- the absence of ABC-level enforcement for generic definition construction and route
  exclusivity; and
- the proposed `AbstractSimulationTask.execute(inputs, TaskExecutionContext)` method,
  even though `TaskExecutionContext` grants no authority and the established protected
  target effect boundary is `AbstractSimulationDispatchEffect`.

## Problem

Before correction, the architecture did not close route identity, behavioral
inheritance, and protected execution authority through one enforced contract. It called
`TaskDefinition.execution_kind` authoritative while allowing concrete classes to
express conflicting nominal memberships, and delegates rejection to plan compilation.
It also places a direct execution method on the simulation Task even though that method
cannot receive or verify the authority-bearing dispatch request.

## Evidence

- A bounded in-memory reproduction instantiated one concrete class satisfying both
  `AbstractSimulationTask` and `NestedWorkflowTask`.
- The former `WorkflowTaskBinding` validated nominal `AbstractTask` membership and
  definition identity but not incompatible specialization overlap.
- The proposed architecture makes execution kind authoritative while separately
  declaring route ABC membership and did not specify final generic definition
  construction or subclass-time route enforcement.
- `python/src/ksdft2effmass/workflows/model.py` defines `TaskExecutionContext` as
  correlation state rather than execution authority.
- `../simulation-task-model.md` assigns the authority-bearing external effect to the
  current `SimulationDispatchEffect` port; the target replaces it with the nominal
  `AbstractSimulationDispatchEffect` ABC.
- The proposed schematic nevertheless gives `AbstractSimulationTask` a direct
  `execute(inputs, context)` method returning results.

## Consequence

Without one closed route contract, engine behavior can depend on `isinstance` check
order or late compiler errors. More seriously, a simulation operation can expose a
callable effect-shaped method whose signature cannot demonstrate the authority required
for protected external execution.

## Persistent correction

The accepted class contracts are [`AbstractTask`](../AbstractTask/index.md),
[`TaskExecutionKind`](../TaskExecutionKind/index.md), the three route roots, and
[`AbstractSimulationDispatchEffect`](../AbstractSimulationDispatchEffect/index.md).
They make the route ABC hierarchy construct the generic definition rather than asking every
concrete Task to declare a parallel route value:

1. `AbstractTask` supplies a final generic `TaskDefinition` property.
2. Each route root supplies its fixed `TaskExecutionKind`.
3. `AbstractTask.__init_subclass__` rejects multiple route roots, route-kind overrides,
   and overrides of generic definition construction.
4. Concrete Tasks provide only stable definition identity, immutable dependencies, and
   route-owned behavior.
5. Plan compilation checks declarative route closure, and runtime-binding compilation
   checks exact kind and nominal membership as cross-object defense in depth.

`AbstractSimulationTask` must not expose the ordinary in-process execution signature.
It owns immutable simulation operation definition and binding data. The existing
`AbstractSimulationDispatchEffect`, consuming an authority-bearing request, becomes the
sole external-effect method. Confirmed dispatch and ingress may yield
`TaskExecutionResults`; nominal simulation membership itself never grants authority.

`NestedWorkflowTask` similarly owns immutable child-definition correlation and no
scientific execution method. Child-run creation and reconciliation remain with the
nested Workflow control path.

## Implementation evidence

`workflows/tasks.py` now enforces route closure at subclass construction and supplies
final generic Task-definition construction. `workflows/planning.py` and
`workflows/bindings.py` enforce declarative and runtime closure separately. QE Tasks
are immutable definition/input owners without direct calculator or effect invocation;
`LocalQuantumEspressoExecutor` remains behind the authority-bearing dispatch-effect
request. Focused route, planning, binding, engine, QE, and dispatch tests pass locally.

## Evidence boundary

Closing route inheritance and authority boundaries establishes software structure only.
It does not authorize an external calculation or establish numerical or scientific
acceptance.
