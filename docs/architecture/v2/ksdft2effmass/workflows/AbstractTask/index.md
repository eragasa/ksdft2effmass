# `AbstractTask`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Responsibility

`AbstractTask` is the nominal ABC for one Workflow engine node. It owns stable generic
definition construction and route-inheritance enforcement. It does not impose one fake
execution method on every route.

Its public contract is:

- abstract stable `identity: TaskDefinitionIdentity`; and
- final `definition: TaskDefinition`, constructed from `identity` and the route kind
  supplied by exactly one route-root ABC.

`AbstractTask` owns no scheduler, registry, discovery, persistence, authority,
scientific result wrapper, or durable outcome.

## Subclass enforcement

Runtime subclass construction and static final annotations enforce that:

1. a concrete Task resolves to exactly one route root;
2. incompatible route roots cannot be multiply inherited;
3. a concrete Task cannot override the route kind;
4. a concrete Task cannot override generic `definition` construction; and
5. no structural lookalike satisfies the Task boundary.

`AbstractScientificTask` may remain an abstract grouping base without a route.
`AbstractInProcessScientificTask`, `AbstractSimulationTask`, and
`NestedWorkflowTask` are the only route roots.

Plan and binding constructors repeat exact identity, kind, and nominal-membership
checks as cross-object defense in depth. They do not replace ABC enforcement.

## Concrete-owner rule

Maintained concrete Tasks are slotted and operationally immutable. They define only a
stable identity, immutable scientific or integration dependencies, and behavior owned
by their route. They do not create TaskDefinition subclasses, Task-specific result
containers, or serializers merely to name an operation.

## Related architecture

- [Schematic](schematic.md)
- [`TaskDefinition`](../TaskDefinition/index.md)
- [`AbstractScientificTask`](../AbstractScientificTask/index.md)
- [Unclosed-route defect](../defects/defect00002-unclosed_task_execution_routes.md)
