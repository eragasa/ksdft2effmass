# Scientific Workflow implementation

## Status

**Implemented correction.**

- `AbstractTask` is the sole nominal executable-Task base.
- `AbstractWorkflow` is an independent definition-only ABC.
- `NestedWorkflowTask` is the ABC for explicit controlled child-Workflow adapters.
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

## Implemented sequence

1. Removed the `Task` and `Workflow` structural protocols and their public exports.
2. Separated `AbstractWorkflow` from `AbstractTask`.
3. Added the `NestedWorkflowTask` ABC.
4. Synchronized supported package exports and NumPy-style API documentation.
5. Replaced the retired protocol tests with nominal separation and adapter tests.
6. Migrated the maintained Quantum ESPRESSO executable Task classes to
   `AbstractTask`.
7. Kept unrelated Workflow-named domain ActionObjects outside this bounded correction.

## Periodic-1D replay adoption

After this correction, the isolated-band replay introduces concrete
`AbstractTask` subclasses for each cohesive operation and one root
`AbstractWorkflow` definition containing their run-scoped instances. The root
application boundary supplies execution contexts and invokes Workflow control; the
Workflow definition does not call its member Tasks.

No replay calculation begins until the complete graph, result routing, comparison gate,
and artifact-preparation boundary have focused software verification. Historical
Appendix G inputs, results, reports, figures, and checksum-covered payload bytes remain
unchanged.
