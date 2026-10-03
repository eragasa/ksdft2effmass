# Scientific Workflow implementation

## Status

**Accepted correction; implementation pending.**

- `AbstractTask`, Workflow composition records, and WorkflowRun control records are
  implemented.
- The current structural `Task` and `Workflow` protocols will be removed without
  compatibility aliases.
- The current `AbstractWorkflow(AbstractTask)` relationship will be replaced by an
  independent `AbstractWorkflow` ABC.
- `NestedWorkflowTask` will be introduced as an ABC for the explicit child-Workflow
  Task adapter.
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

## Implementation sequence

1. Remove the `Task` and `Workflow` structural protocols and their public exports.
2. Separate `AbstractWorkflow` from `AbstractTask`.
3. Add the `NestedWorkflowTask` ABC.
4. Synchronize supported package exports and NumPy-style API documentation.
5. Replace the retired protocol tests with nominal separation and adapter tests.
6. Run focused model tests, the complete Workflow software-verification suite, Ruff,
   formatting, focused strict mypy, strict Sphinx, and diff checks.
7. Commit the correction without migrating unrelated concrete classes.

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
