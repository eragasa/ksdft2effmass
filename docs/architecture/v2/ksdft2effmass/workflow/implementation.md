# Scientific Workflow implementation

## Status

**Implemented execution-plan slice.**

- `AbstractTask` remains the generic nominal executable engine-node base.
- `AbstractScientificTask(AbstractTask)` identifies executable scientific operations
  without adding a second execution signature.
- `AbstractWorkflow` remains an independent definition-only ABC.
- `NestedWorkflowTask` remains the ABC for explicit controlled child-Workflow
  adapters.
- The retired structural `Task` and `Workflow` protocols have no compatibility aliases.
- The maintained Quantum ESPRESSO Task classes inherit `AbstractScientificTask`.
- Focused abstract-contract, nominal-separation, public-export, and integration tests
  are synchronized.
- `WorkflowTaskBinding` and `WorkflowExecutionPlan` are implemented immutable engine
  inputs with focused software-verification evidence.
- `WorkflowEngine`, the periodic-1D replay Task graph, and replay execution remain
  pending.

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

- `AbstractTask` and `NestedWorkflowTask` subclasses remain abstract until all required
  members are implemented.
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

## Implemented execution-plan slice

1. Added `WorkflowTaskBinding` with exact Task-instance/definition correlation.
2. Added `WorkflowExecutionPlan` with complete ordered composition closure.
3. Exported and documented both records through the supported package route.
4. Verified wrong semantic types, missing/extra/reordered bindings, definition
   mismatch, nominal Task enforcement, and valid scientific/nested Task specialization
   membership.
5. Added no engine execution, persistence, registry, scientific wrapper, or periodic
   migration behavior in this slice.

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
