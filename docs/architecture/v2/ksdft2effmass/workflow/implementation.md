# Scientific Workflow implementation

## Status

**Accepted extension; implementation pending.**

- `AbstractTask` remains the generic nominal executable engine-node base.
- `AbstractScientificTask(AbstractTask)` will identify executable scientific
  operations without adding a second execution signature.
- `AbstractWorkflow` remains an independent definition-only ABC.
- `NestedWorkflowTask` remains the ABC for explicit controlled child-Workflow
  adapters.
- The retired structural `Task` and `Workflow` protocols have no compatibility aliases.
- The maintained Quantum ESPRESSO Task classes inherit `AbstractTask`.
- Focused nominal-contract, public-export, and integration tests are synchronized.
- The periodic-1D replay Task graph and replay execution remain pending.

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
- A nested adapter identifies exactly one target Workflow definition.
- No base class owns a registry, scheduler, persistence object, mutable run state,
  implicit context, or scientific algorithm.

## Extension sequence

1. Add `AbstractScientificTask(AbstractTask)` with no additional execution method.
2. Export and document the class through the supported package route.
3. Migrate the maintained Quantum ESPRESSO scientific Task classes from
   `AbstractTask` to `AbstractScientificTask`.
4. Verify abstract enforcement, nominal separation from `NestedWorkflowTask`, exact
   public exports, and integration inheritance.
5. Keep unrelated Workflow-named domain ActionObjects outside this bounded extension.

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
