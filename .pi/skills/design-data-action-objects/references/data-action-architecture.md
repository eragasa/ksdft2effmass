# DataObject/ActionObject Architecture

## DataObjects

DataObjects represent scientific state, metadata, configuration, or results. They normally use `@dataclass(frozen=True, slots=True)`.

A DataObject may contain explicitly declared fields, intrinsic constructor validation, canonicalization of its own data, exact value equality, and trivial derived properties.

A DataObject must not own serialization workflows, numerical analysis policies, basis alignment, unit conversion, file I/O, orchestration, or operations that produce conceptually new objects.

## ActionObjects

ActionObjects perform explicit transformations, analyses, validation procedures, or external representations. An ActionObject owns its numerical or algorithmic policy, accepts DataObjects as inputs, returns a DataObject or explicit ResultObject, avoids hidden mutation and global state, and exposes a clear domain verb such as `execute()`, `encode()`, or `decode()`.

A Workflow is a specialized concrete ActionObject that encapsulates a reusable, scientifically or computationally meaningful sequence of actions. Workflow inputs and outputs must be explicit DataObjects or ResultObjects; dependencies must be explicit; Workflows must not rely on hidden global state. Do not introduce a generic Workflow base class unless multiple existing workflows require a real shared interface. Do not treat every integration test as a Workflow. Do not create production Workflow objects solely to provide an owner for tests.

The standard form is:

```text
DataObject --ActionObject--> DataObject or ResultObject
```

Do not create abstract `DataObject` or `ActionObject` base classes. Prefer concrete types and composition. Introduce protocols only after multiple real implementations share a required interface.

## Ownership rules

- data invariant -> owning DataObject;
- numerical operation -> corresponding ActionObject;
- serialization rule -> serializer ActionObject;
- operation output -> explicit ResultObject;
- genuinely domain-independent mathematics -> free function only when it has no natural owner.

Do not create `utils.py`, `helpers.py`, `common.py`, or `misc.py` dumping grounds. Every nontrivial operation needs an explicit and documented domain owner.

## Rust compatibility

New architecture must remain translatable to Rust using structs for DataObjects and ResultObjects; structs with `impl` blocks for ActionObjects; constructors returning `Result` for validated construction; composition rather than inheritance; explicit ownership and immutable borrowing; deterministic, versioned serialization; fixed serialized field names; explicit error cases; no dynamic attributes or monkey patching; and no implicit workflow state.

Python and Rust need not share source code. They must share an intelligible data model, operation boundaries, and wire-format specification.

## Review checklist

- Are all represented fields explicit and immutable where practical?
- Does each validation rule belong to the object that owns the invariant?
- Are tolerances, alignments, reductions, and analyses outside DataObjects?
- Does serialization live in a named serializer ActionObject?
- Are operation outputs explicit ResultObjects instead of side effects?
- Are free functions restricted to ownerless domain-independent mathematics?
- Is the design expressible as Rust structs, `impl` blocks, and `Result` errors?
- Are wire-format fields fixed, deterministic, and versioned?
- If a Workflow is proposed, is it a genuine reusable domain/computational ActionObject with explicit DataObject/ResultObject inputs, outputs, and dependencies?
- Are technical integrations routed to integration tests instead of artificial production Workflow objects?
- Are there no dynamic attributes, monkey patches, global workflow state, or dumping-ground modules?

## Public validation surfaces and private implementation

Every scientific invariant, convention, transformation, approximation, and
wire-format decision must be public, documented, and validated through an
independently executable surface such as constructors, ActionObject methods,
public schema files, and golden fixtures. Tests should exercise public behavior,
not private method names.

Private methods may only mechanically implement already public rules owned by
their class. They must be fully observable through public inputs and outputs, may
not be called by other classes, and must not contain hidden scientific semantics.
Module-private functions may be used within a module for shared mechanical
invariants when they have a clear module owner, introduce no hidden scientific
semantics, and are documented when nontrivial. Do not create generic helper
modules such as `utils.py`, `helpers.py`, `common.py`, or `misc.py`.
