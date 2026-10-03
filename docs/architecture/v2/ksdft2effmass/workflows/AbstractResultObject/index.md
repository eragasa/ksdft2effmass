# `AbstractResultObject`

## Status

**Implemented nominal-ABC contract; local software-verification evidence passes.**

## Responsibility

`AbstractResultObject(ABC)` is the nominal Workflow-facing base for an immutable
produced or admitted result. It declares one abstract
`identity -> ResultObjectIdentity` property. Concrete domains continue to own result
fields, units, provenance, and intrinsic invariants.

Nominal inheritance proves only Workflow result membership and identity shape. It does
not prove that work ran, that bytes were persisted, that provenance is authentic, or
that a result is numerically or scientifically valid.

## Closed admission

Only maintained classes that actually cross the Workflow result boundary inherit this
ABC. A class is not admitted merely because its name ends in `Result` or because it
exposes an `identity` attribute. Structural fallback, virtual subclass registration,
and compatibility aliases are prohibited.

The exact initial implementation set is recorded in the repository-wide migration
crosswalk. `AbstractNormalizedObservationSource` extends this ABC for the narrower
observation boundary.

## Related architecture

- [Schematic](schematic.md)
- [`TaskExecutionResults`](../TaskExecutionResults/index.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
