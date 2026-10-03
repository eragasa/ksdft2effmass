# Abstract Task and Workflow bases

## Status

**Implemented architecture.** The public `AbstractTask` and `AbstractWorkflow`
nominal bases supplement the existing `Task` and `Workflow` structural protocols.
Source, focused software-verification tests, package exports, and public API
documentation are synchronized.

## Decision

`ksdft2effmass.workflows` will provide two nominal abstract ActionObject bases:

- `AbstractTask` for one reusable scientific operation; and
- `AbstractWorkflow` for one reusable composition of Task instances.

The abstract bases supplement rather than replace the structural `Task` and `Workflow`
protocols. Protocols remain suitable for compatible external implementations and typed
ports. Maintained first-party Task and Workflow implementations use the nominal bases
once migrated. This supplies shared nominal ownership without weakening the existing
structural boundary.

## `AbstractTask` contract

`AbstractTask` is an abstract, stateless ActionObject with no instance dictionary. It
requires:

```python
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

A concrete Task consumes only already-bound named ResultObjects and the exact supplied
operation context. It returns concrete immutable ResultObjects. It does not discover
prerequisites, inspect a complete marking, select its own activation, schedule itself,
construct a durable `TaskInvocationOutcome`, persist state, issue authority, or infer
scientific acceptance.

The base supplies no default scientific operation, input-name vocabulary, result
factory, mutable registry, ambient dependency lookup, error suppression, or execution
policy. Concrete domains own those contracts.

## `AbstractWorkflow` contract

`AbstractWorkflow` inherits `AbstractTask` and adds the abstract properties:

```python
@property
@abstractmethod
def workflow_identity(self) -> WorkflowIdentity: ...

@property
@abstractmethod
def composition(self) -> WorkflowComposition: ...
```

A concrete Workflow is therefore invocable as a Task and may be nested. Its
`WorkflowComposition` identifies its run-scoped Task instances. The Workflow owns
composition, dependency routing, and start-gate policy; it does not implement the
scientific operations assigned to its member Tasks.

`AbstractWorkflow` does not provide a sequential runner, scheduler, mutable execution
context, hidden Task registry, persistence adapter, colored-Petri-net evaluator, retry
loop, or external-effect boundary. Workflow control remains responsible for activation,
invocation outcomes, run transitions, and persistence. A nested invocation still owns
a distinct child `WorkflowRun`.

## Decomposition rule

A Workflow must be decomposed into Tasks whenever it performs more than composition and
routing. In particular, each reusable scientific transformation, numerical algorithm,
comparison, artifact preparation operation, or authorized external effect belongs to a
concrete Task or to an already established specialized execution boundary.

A Workflow may:

- declare immutable Task-instance membership;
- declare start gates and result dependencies;
- route already-produced ResultObjects; and
- expose the Task contract required for nested invocation.

A Workflow may not directly:

- diagonalize or transform represented operators;
- select or transport frames;
- truncate or fit effective models;
- compare replay results;
- encode or write scientific artifacts;
- invoke a calculator or filesystem effect; or
- convert a failed Task into a successful scientific result.

Task decomposition does not require one Task per scalar check. Intrinsic DataObject
invariants remain on their owning records, and cohesive numerical operations remain
cohesive Tasks.

## Protocol and nominal-base relationship

A subclass of `AbstractTask` must satisfy the public `Task` protocol, and a subclass of
`AbstractWorkflow` must satisfy the public `Workflow` protocol. Tests verify both
nominal inheritance and runtime structural conformance. The bases do not register
unrelated structural implementations or require external implementations to inherit.

The `identity` of a Workflow remains its Task-definition identity. The distinct
`workflow_identity` identifies the reusable Workflow definition. Neither identity is
derived implicitly from the other.

## Migration boundary

Introduction of the bases is additive. The completed foundation slice:

1. adds the two abstract classes under `ksdft2effmass.workflows`;
2. exports and documents them through the supported package route; and
3. verifies abstract-member enforcement, nominal inheritance, protocol conformance,
   and absence of base-provided execution behavior.

The periodic-1D replay Task graph will use these bases. Unrelated existing first-party
classes migrate only through separately bounded work.

The migration must not rename or remove the existing protocols, reinterpret ordinary
campaign ActionObjects as Workflows, or introduce a second scheduler or persistence
system.

## Periodic-1D replay application

The bounded isolated-band replay uses `AbstractWorkflow` only as the composition owner.
Its member `AbstractTask` implementations separately own input adaptation, parent-model
construction, parent-fiber sampling, band-frame transport, retained-space/operator
binding, retained-operator projection, complete hopping transformation, range-specific
truncation, range-specific fitting, historical-result comparison, and artifact
preparation.

The artifact adapter may write only outputs returned by a confirmed preparation Task.
A failed replay comparison produces no prepared artifact output. Existing Appendix G
inputs, results, reports, figures, and checksum-covered payload bytes remain unchanged.
