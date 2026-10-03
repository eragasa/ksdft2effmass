# Scientific Workflow implementation

## Status

**Accepted in-process WorkflowEngine slice; implementation pending.**

- `AbstractTask` remains the generic nominal executable engine-node base.
- `AbstractScientificTask(AbstractTask)` identifies ordinary in-process scientific
  operations without adding a second execution signature.
- `AbstractSimulationTask(AbstractScientificTask)` marks scientific operations that
  require the existing authority-checked external-dispatch path.
- `AbstractWorkflow` remains an independent definition-only ABC.
- `NestedWorkflowTask` remains the ABC for explicit controlled child-Workflow
  adapters.
- The retired structural `Task` and `Workflow` protocols have no compatibility aliases.
- The maintained Quantum ESPRESSO Task classes inherit `AbstractSimulationTask`.
- Focused abstract-contract, nominal-separation, public-export, and integration tests
  are synchronized.
- `WorkflowTaskBinding` and `WorkflowExecutionPlan` are implemented immutable engine
  inputs with focused software-verification evidence.
- The first `WorkflowEngine` slice will execute one exact direct in-process scientific
  Task activation and fail closed for simulation, nested, and unknown Task branches.
- Dedicated simulation dispatch, nested execution, the periodic-1D replay Task graph,
  and replay execution remain pending.

## Public contracts

### `AbstractTask`

```python
class AbstractTask(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def identity(self) -> TaskDefinitionIdentity: ...

    @abstractmethod
    def execute(
        self,
        inputs: tuple[TaskInputBinding, ...],
        context: TaskExecutionContext,
    ) -> tuple[ResultObject, ...]: ...
```

### `AbstractScientificTask`

```python
class AbstractScientificTask(AbstractTask):
    __slots__ = ()
```

This semantic ABC adds no new method, registry, result wrapper, or execution policy.
It distinguishes scientific operations from engine-control Task specializations while
retaining the exact `AbstractTask.execute(inputs, context)` contract.

### `AbstractSimulationTask`

```python
class AbstractSimulationTask(AbstractScientificTask):
    __slots__ = ()
```

This semantic ABC adds no second execution method or authority. It marks a scientific
Task for the specialized simulation-dispatch branch. Constructing or selecting the
Task does not authorize an external effect.

### `AbstractWorkflow`

```python
class AbstractWorkflow(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def workflow_identity(self) -> WorkflowIdentity: ...

    @property
    @abstractmethod
    def composition(self) -> WorkflowComposition: ...
```

### `WorkflowTaskBinding`

```python
@dataclass(frozen=True, slots=True)
class WorkflowTaskBinding:
    task_instance: TaskInstance
    task: AbstractTask
```

Construction requires nominal `AbstractTask` inheritance and exact agreement between
`task_instance.definition_identity` and `task.identity`.

### `WorkflowExecutionPlan`

```python
@dataclass(frozen=True, slots=True)
class WorkflowExecutionPlan:
    workflow: AbstractWorkflow
    task_bindings: tuple[WorkflowTaskBinding, ...]
```

Bindings must be in the same order as `workflow.composition.task_instances`, with one
binding for every instance and no extras. Task-instance identities must be unique, and
every binding must repeat the exact corresponding composition instance. The plan does
not create a registry, infer a latest definition, execute a Task, allocate context,
persist state, or establish authority.

### `NestedWorkflowTask`

```python
class NestedWorkflowTask(AbstractTask, ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def workflow(self) -> AbstractWorkflow: ...
```

`NestedWorkflowTask` remains abstract because child-run creation, authority,
correlation, reconciliation, and result export belong to a concrete workflow-control
adapter. The ABC provides no default `execute` implementation.

## Invariants

- `AbstractTask`, `AbstractScientificTask`, `AbstractSimulationTask`, and
  `NestedWorkflowTask` subclasses remain abstract until all required members are
  implemented.
- `AbstractWorkflow` subclasses remain abstract until Workflow identity and composition
  are implemented; the base provides no `identity` or `execute` member.
- Workflow and Task identities remain nominally distinct.
- Every execution-plan binding agrees with its Task instance's declared Task-definition
  identity.
- Execution-plan order and membership exactly equal Workflow composition order and
  membership.
- A nested adapter identifies exactly one target Workflow definition.
- No base class owns a registry, scheduler, persistence object, mutable run state,
  implicit context, or scientific algorithm.

## In-process WorkflowEngine slice

```python
class WorkflowEngine:
    def execute_in_process(
        self,
        plan: WorkflowExecutionPlan,
        activation: TaskActivation,
    ) -> tuple[ResultObject, ...]: ...
```

The ActionObject resolves the activation's exact `TaskInstance` from the validated
plan, requires exact Workflow and Task-instance agreement, constructs the immutable
`TaskExecutionContext` from activation identities, invokes one direct
`AbstractScientificTask`, and validates the returned tuple and unique exact result
identities.

The method rejects `AbstractSimulationTask`, `NestedWorkflowTask`, and any unknown
`AbstractTask` specialization before invocation. It neither selects activation,
constructs authority, catches or translates Task exceptions, creates durable
`TaskInvocationOutcome` state, mutates `WorkflowRun`, persists state, nor discovers a
Task. Separate later engine paths must connect simulation Tasks to existing authority
and dispatch contracts and nested Tasks to distinct child-run creation.

## In-process WorkflowEngine implementation sequence

1. Add the stateless `WorkflowEngine` ActionObject with only `execute_in_process`.
2. Correlate the exact plan Workflow, activation Workflow, and complete Task instance.
3. Reject simulation, nested, and unknown Task specializations before calling
   `execute`.
4. Derive the exact execution context from the activation and validate returned result
   shape and identity uniqueness.
5. Export and document the engine through the supported package route.
6. Verify valid execution, mismatched plan/activation identities and instances,
   fail-closed specialized branches, malformed returns, and propagated Task failures.
7. Add no dispatch, child-run execution, persistence, durable outcome, periodic replay,
   or external effect in this slice.

## Implemented simulation-Task specialization

1. Added `AbstractSimulationTask(AbstractScientificTask)` without execution or
   authority behavior.
2. Exported and documented it through the supported package route.
3. Migrated the maintained Quantum ESPRESSO Task classes to
   `AbstractSimulationTask`.
4. Verified nominal inheritance and separation from direct scientific and nested
   Workflow Tasks.
5. Updated the simulation-Task architecture from the retired structural protocol model
   to the nominal ABC hierarchy.
6. Added no WorkflowEngine invocation, external execution, persistence, scientific
   wrapper, or periodic migration behavior in this slice.

## Periodic-1D replay adoption

After this extension, the isolated-band replay introduces concrete
`AbstractScientificTask` subclasses for each cohesive scientific operation and one root
`AbstractWorkflow` definition containing their run-scoped instances. The root
application boundary supplies execution contexts and invokes Workflow control; the
Workflow definition does not call its member Tasks.

No replay calculation begins until the complete graph, result routing, comparison gate,
and artifact-preparation boundary have focused software verification. Historical
Appendix G inputs, results, reports, figures, and checksum-covered payload bytes remain
unchanged.
