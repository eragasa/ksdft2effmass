# DataObject/ActionObject Architecture

## DataObjects

DataObjects represent scientific state, metadata, configuration, or results. They normally use `@dataclass(frozen=True, slots=True)`.

A DataObject may contain explicitly declared fields, intrinsic constructor validation, canonicalization of its own data, exact value equality, and trivial derived properties.

A DataObject must not own serialization workflows, numerical analysis policies, basis alignment, unit conversion, file I/O, orchestration, or operations that produce conceptually new objects.

## ActionObjects

ActionObjects perform explicit transformations, analyses, validation procedures, or external representations. An ActionObject owns its numerical or algorithmic policy, accepts DataObjects as inputs, returns a DataObject or explicit ResultObject, avoids hidden mutation and global state, and exposes a clear domain verb such as `execute()`, `serialize()`, or `deserialize()`.

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

## Cross-language compatibility

Python/Rust agreement is required only for explicitly language-independent
specifications, shared wire formats, components approved for Rust implementation,
or contracts whose active task requires cross-language conformance. In those
cases, use structs for DataObjects and ResultObjects; structs with `impl` blocks
for ActionObjects; constructors returning `Result` for validated construction;
composition rather than inheritance; explicit ownership and immutable borrowing;
deterministic, versioned serialization; fixed serialized field names; and
explicit error cases.

Python and Rust need not share source code. Python-only internal objects need
conventional Python typing and tests, not speculative Rust design.

## Review checklist

- Are all represented fields explicit and immutable where practical?
- Does each validation rule belong to the object that owns the invariant?
- Are tolerances, alignments, reductions, and analyses outside DataObjects?
- Does serialization live in a named serializer ActionObject?
- Are operation outputs explicit ResultObjects instead of side effects?
- Are free functions restricted to ownerless domain-independent mathematics?
- When cross-language conformance applies, is the design expressible as Rust structs, `impl` blocks, and `Result` errors?
- When persistence applies, are wire-format fields fixed, deterministic, and versioned?
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

## Corrective operator-record policy

DataObjects and ResultObjects are operationally immutable: public arrays and
nested metadata must not be mutable through ordinary public APIs such as
``setflags(write=True)``.  Intrinsic validation belongs to the owning object,
relational compatibility belongs to a named ActionObject, and policy validation
with units belongs to the ActionObject that owns the policy.  Public enum and
error states must be reachable from independently valid public objects; tests
must not manufacture invalid states with ``object.__setattr__`` or monkey
patching. Public Python, runtime acceptance, tests, applicable schemas, and
Sphinx documentation must agree on stored types and structured errors. A Rust
mapping must also agree only when the contract is explicitly language-independent,
uses a shared wire format, is approved for Rust implementation, or the active
task requires cross-language conformance.  Module-level field validators and generic helper modules remain
prohibited; limited owner-local duplication is preferred.  Numerical norms and
residual computations must be scale-safe and must surface structured numerical
errors rather than silent ``inf`` or ``nan`` results.  Reviews must report file
evidence, commands, findings, and a PASS or FAIL conclusion.
