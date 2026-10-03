# `WorkflowDefinition`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Classification

`WorkflowDefinition` is one concrete frozen, slotted, non-subclassed DataObject:

```python
@final
@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    identity: WorkflowIdentity
    composition: WorkflowComposition
```

It represents reusable declarative Workflow identity and ordered Task-instance
composition. Its identity must equal the composition's Workflow identity.

It contains no live Workflow owner, runtime Task adapter, effect port, WorkflowRun,
activation, result, authority, persistence repository, or scientific acceptance.

## Ownership

`AbstractWorkflow` provides final generic construction from its stable identity and
immutable composition. Concrete Workflows do not define WorkflowDefinition subclasses
or per-Workflow schemas. `WorkflowExecutionPlan` retains this frozen value directly
and never rereads definition state from a live Workflow owner.

Composition continues to own Task-instance membership, dependencies, and start-gate
policy. Definition construction executes no member Task and supplies no scheduler.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractWorkflow`](../AbstractWorkflow/index.md)
- [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md)
- [Plan/runtime conflation defect](../defects/defect00003-plan_runtime_binding_conflation.md)
