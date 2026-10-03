# Workflow current-to-target class crosswalk

## Status

**Accepted architecture plan; source implementation has not started.**

This map defines one coordinated implementation run after the architecture gate is
complete. No compatibility aliases are retained for retired contracts.

## Current-to-target class and contract map

| Current contract | Target contract | Coordinated change |
|---|---|---|
| Raw `tuple[ResultObject, ...]` Task returns | `TaskExecutionResults` | Enforce ordered, nonempty, unique result identities once. |
| `AbstractTask.identity` plus universal `execute` | `AbstractTask.identity` plus final generic `definition` | Remove universal execution; enforce exactly one route root. |
| Direct `AbstractScientificTask` execution | `AbstractInProcessScientificTask.execute` | Move ordinary in-process Tasks to the explicit route ABC. |
| `AbstractSimulationTask.execute` inherited from `AbstractTask` | Definition-only `AbstractSimulationTask` | Remove the non-authority-bearing direct effect path. |
| `NestedWorkflowTask.execute` inherited from `AbstractTask` | Definition-only `NestedWorkflowTask` with immutable child definition | Keep child-run creation in nested Workflow control. |
| Structural `ResultObject` protocol | Nominal `AbstractResultObject` ABC | Migrate the closed maintained Workflow result set; structural lookalikes are rejected. |
| Structural observation identity, policy, and source protocols | `AbstractObservationCorrelationIdentity`, `AbstractObservationNormalizationPolicySource`, and `AbstractNormalizedObservationSource` | Migrate QE-owned identities, policy, and extracted result plus test doubles to explicit inheritance. |
| Structural `SimulationDispatchEntryCommitter` protocol | Nominal `AbstractSimulationDispatchEntryCommitter` ABC | Migrate `WorkflowRunDispatchEntryCommitter`; retain no protocol alias. |
| Structural `SimulationDispatchEffect` protocol | Nominal `AbstractSimulationDispatchEffect` ABC | Migrate concrete executors; retain no protocol alias. |
| Structural `WorkflowResultValueCodec` protocol | Nominal `AbstractWorkflowResultValueCodec` ABC | Migrate the four maintained serializers without changing bytes or supported branches. |
| Structural `WorkflowRunRepository` protocol | Nominal `AbstractWorkflowRunRepository` ABC | Migrate `WorkflowRunAtomicRepository`; retain no protocol alias. |
| `AbstractWorkflow.workflow_identity` and `.composition` read by plans | Final generic `AbstractWorkflow.definition` | Snapshot `WorkflowDefinition`; never retain the owner in a plan. |
| `WorkflowTaskBinding(TaskInstance, AbstractTask)` as plan content | Process-local `WorkflowTaskBinding` with route-closed runtime fields | Move all live adapters to runtime bindings. |
| `WorkflowExecutionPlan(AbstractWorkflow, bindings)` | Declarative `WorkflowExecutionPlan(WorkflowDefinition, TaskDefinitions, nested targets)` | Remove live owners and adapters from plan state. |
| Constructor checks in DataObject post-init only | `WorkflowExecutionPlanConstructor` and `WorkflowExecutionBindingsConstructor` | Centralize cross-object compilation while retaining intrinsic DataObject checks. |
| `WorkflowEngine.execute_in_process(plan, activation)` returning raw tuple | `execute_in_process(bindings, activation) -> TaskExecutionResults` | Use the exact plan carried by validated runtime bindings. |

## Quantum ESPRESSO migration

The four maintained QE Tasks become immutable `AbstractSimulationTask` definition and
operation-input owners with no direct calculator invocation method. Their generic
`TaskDefinition` is supplied by the ABC hierarchy.

`LocalQuantumEspressoExecutor` becomes an
`AbstractSimulationDispatchEffect`. External process invocation remains there, behind
the authority-bearing request and successful claim. Existing QE Workflow families are
outside this migration because they are separately implemented. No QE-specific
Workflow ABC is introduced. `QuantumEspressoSimulation` receives only the mechanical
nominal-ABC reference changes required by the repository-wide decision.

Existing concrete QE ResultObjects inherit `AbstractResultObject`; extracted
observations also inherit `AbstractNormalizedObservationSource`. Execution inputs,
native artifact identities, authority records, dispatch outcomes, payload bytes, and
scientific limitations otherwise remain unchanged unless an exact target contract
requires a mechanical type annotation update.

## Public API changes

Add:

- `TaskExecutionKind`, `TaskDefinition`, and `TaskExecutionResults`;
- `AbstractResultObject`;
- `AbstractInProcessScientificTask`;
- `AbstractObservationCorrelationIdentity`,
  `AbstractObservationNormalizationPolicySource`, and
  `AbstractNormalizedObservationSource`;
- `AbstractSimulationDispatchEntryCommitter` and
  `AbstractSimulationDispatchEffect`;
- `AbstractWorkflowResultValueCodec` and `AbstractWorkflowRunRepository`;
- `WorkflowDefinition` and `NestedWorkflowTarget`;
- `WorkflowExecutionBindings`;
- `WorkflowExecutionPlanConstructor`; and
- `WorkflowExecutionBindingsConstructor`.

Change the documented signatures and semantics of `AbstractTask`,
`AbstractScientificTask`, `AbstractSimulationTask`, `NestedWorkflowTask`,
`AbstractWorkflow`, `WorkflowTaskBinding`, `WorkflowExecutionPlan`, and
`WorkflowEngine`.

Remove every retired Workflow Protocol export and retired signature without
compatibility aliases. The repository-wide calculator, operator-representation, and
shared-persistence ABC changes are specified by the
[complete Protocol-to-ABC crosswalk](../../protocol-to-abc-migration.md).

## Implementation order within the single run

1. Add shared enums and frozen DataObjects.
2. Replace the Task and Workflow ABC hierarchy and subclass enforcement.
3. Add declarative plan and process-local binding constructors.
4. Migrate `WorkflowEngine` and result handling.
5. Migrate simulation control typing and Quantum ESPRESSO owners.
6. Update exports, Sphinx API documentation, concepts, and package architecture.
7. Migrate focused tests, then run broader Workflow and QE checks.
8. Run strict typing, Ruff, formatting, strict Sphinx, public-API, and diff checks.
9. Record any unrelated pre-existing failures without weakening contracts.

No periodic-1D Workflow or replay behavior is added during this migration.

## Required evidence

The run must verify ABC route enforcement, no multiple route roots, final generic
definition construction, exact result invariants, declarative-plan purity, complete
runtime binding closure, simulation authority preservation, nested fail-closed
behavior, QE nominal effect conformance, and absence of retired public aliases.

Passing checks establish software conformance only, not numerical verification,
scientific validation, uncertainty quantification, execution authority, or acceptance.
