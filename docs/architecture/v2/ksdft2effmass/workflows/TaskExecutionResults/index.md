# `TaskExecutionResults`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

This class contract supplies the persistent correction target for
[`DEFECT00001`](../defects/defect00001-incomplete_task_execution_results_contract.md).
It does not claim that the class, route integrations, or durable-outcome migration have
been implemented.

## Classification and ownership

`TaskExecutionResults` is one concrete frozen Workflow-control DataObject. It is:

- not an abstract class;
- not a scientific `AbstractResultObject`;
- not a durable `TaskInvocationOutcome`;
- not an execution-authority record;
- not a provenance or artifact-lineage record; and
- not a base for operation-specific subclasses.

`ksdft2effmass.workflows` owns the class because it defines the common result-shape
boundary shared by all successful Task execution routes. Scientific domains retain
ownership of every contained concrete `AbstractResultObject` and its physical, mathematical,
numerical, unit, and provenance meaning.

## Representation

```python
@final
@dataclass(frozen=True, slots=True)
class TaskExecutionResults:
    results: tuple[AbstractResultObject, ...]
```

The pseudocode identifies the public shape rather than authorizing implementation.
Consumers require the exact `TaskExecutionResults` type. Specialized subclasses and
per-operation result-container classes are unsupported.

## Intrinsic invariants

Construction enforces all and only the common local result-shape invariants:

1. `results` is an exact tuple;
2. the tuple contains at least one item;
3. every item inherits the nominal `AbstractResultObject` ABC;
4. every item exposes an exact `ResultObjectIdentity`;
5. result identities are unique within the tuple; and
6. caller-declared result order is retained unchanged.

Wrong semantic types raise `TypeError`. An empty tuple or duplicate result identity
raises `ValueError`.

The class does not inspect domain-specific result fields, compare scientific values,
resolve artifacts, infer units, or reinterpret result order.

## Ordering

`TaskExecutionResults` is deliberately not named a set. Its tuple order is stable
control data. Where Workflow control later pairs result references with production
records, those records use the same positional order.

Order retention does not claim that the represented scientific objects themselves have
a physical ordering. The concrete Task contract owns any scientific interpretation of
its output positions.

## Route contract

Exactly one `TaskExecutionResults` crosses each successful Task route:

- an in-process scientific Task returns it;
- confirmed simulation result ingress admits it from the authority-correlated dispatch
  result; and
- confirmed nested-Workflow export constructs it from explicit admitted child results.

Rejected and indeterminate routes contain no `TaskExecutionResults`. A scientific Task
that produces no `AbstractResultObject` cannot be represented as a confirmed successful Task
invocation under this contract; effect-free control transitions remain Workflow-control
operations rather than zero-result scientific Tasks.

## Durable-outcome boundary

Possession of `TaskExecutionResults` establishes only:

> One successful route supplied an ordered, nonempty collection of distinctly
> identified `AbstractResultObject` instances.

It does not establish:

- execution authority or a successful authority check;
- dispatch, claim, reservation, or reconciliation success;
- producer or production-record identity;
- activation, operation, attempt, or WorkflowRun correlation;
- artifact existence, content identity, or lineage;
- result ingress or persistence;
- numerical verification, scientific validation, uncertainty quantification, or human
  acceptance; or
- a confirmed durable invocation outcome.

Workflow control may construct a confirmed `TaskInvocationOutcome` only after it has:

1. one `TaskExecutionResults`;
2. one exact production record for every contained result;
3. exact WorkflowRun, Task-instance, activation, operation, and attempt correlation;
4. applicable simulation-dispatch or nested-Workflow evidence; and
5. successful admission through the applicable control boundary.

Result references and production-record identities preserve the result tuple's
positional order.

## Inheritance and schema economy

All Tasks use this one class. Do not introduce classes such as:

- `PeriodicTaskExecutionResults`;
- `QuantumEspressoTaskExecutionResults`;
- `ParentFiberSamplingTaskExecutionResults`; or
- operation-specific result-container schemas or serializers.

Scientific variation belongs in contained domain-specific `AbstractResultObject` implementations.
`TaskExecutionResults` normally remains process-local Workflow control data. Durable
formats serialize the established durable outcome and result references rather than
inventing a second wire representation for this container.

A future requirement to persist this container directly would require an explicit
public-contract decision. Importability, convenience, or a new concrete Task does not
create that requirement.

## Required software evidence

Implementation is incomplete until focused software verification establishes:

- successful construction with one and multiple distinct results;
- exact order retention;
- rejection of non-tuple values;
- rejection of an empty tuple;
- rejection of non-`AbstractResultObject` members and structural lookalikes;
- rejection of wrong result-identity types;
- rejection of duplicate result identities;
- rejection of subclass-based alternate contracts at supported consumers; and
- correct integration with confirmed outcome construction without bypassing production
  and route-specific correlation.

Passing these checks establishes only the documented software contract.

## Related architecture

- [Schematic](schematic.md)
- [Scientific Workflow architecture](../../workflow/index.md)
- [Workflow defects](../defects/index.md)
- [Task and colored-Petri-net adapter](../task-and-colored-petri-net-adapter.md)
- [WorkflowRun object model](../workflow-run.md)
- [Workflow control plane](../control-plane.md)
