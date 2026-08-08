# DataObject and ActionObject Architecture

## Architectural distinctions

Keep the modeled subject, mathematical object or operation, finite or numerical
representation, and software implementation distinct. A convenient software
shape must not silently choose scientific meaning or turn structural conformance
into numerical or scientific correctness.

## DataObjects

A DataObject represents state, metadata, configuration, or another durable value.
It should normally be an immutable concrete public record. Operational
immutability also requires that nested arrays, mappings, and other values cannot
be mutated through ordinary public APIs.

A DataObject owns explicit fields, intrinsic invariants among its own fields,
contract-authorized copying or canonicalization, exact value semantics where
specified, and trivial properties derived only from its state. Canonicalization
must not erase a meaningful distinction merely to simplify implementation.

A DataObject does not own external execution, persistence, file I/O,
serialization, numerical or tolerance policy, scientific acceptance, algorithm
selection, orchestration, or compatibility between independently valid objects.
Use concrete records and composition by default; add a nominal base class,
protocol, or abstraction only for demonstrated polymorphism.

## ResultObjects

A ResultObject is semantically a DataObject representing an operation outcome.
It may contain derived state, structured findings, diagnostics, status, or
multiple related values and does not need nominal DataObject inheritance. It
records an outcome but does not perform the operation, apply policy to new
inputs, mutate source objects, or establish scientific acceptance.

Return an explicit immutable ResultObject when an operation produces more than
one obvious value or needs structured errors, findings, warnings, or provenance.

## ActionObjects

An ActionObject owns a reusable transformation, analysis, comparison, validation
procedure, numerical policy, algorithm, serialization operation, persistence
operation, or explicitly authorized external boundary. It should:

- receive explicit inputs and dependencies;
- expose `execute(...)` unless an accepted contract requires another interface;
- keep tolerances, unit policy, acceptance criteria, and algorithm choice with
  the operation that uses them;
- avoid hidden mutable state and ambient global selection;
- leave input objects unchanged; and
- return a DataObject, ResultObject, or one obvious value.

Do not create a generic ActionObject base class solely to label classes.

## Serialization and persistence

Serialization and deserialization belong to a named serializer ActionObject.
DataObjects should not accumulate `to_json`, `from_json`, `to_dict`,
`from_dict`, database, or file methods unless an accepted public contract places
that behavior on the record.

A serializer owns wire-field names, version handling, canonical representation,
and wire-format errors. Schema success or a round trip establishes represented
wire behavior only, not physical alignment, numerical verification, scientific
validity, provenance truth, or human acceptance.

## Cross-object behavior and free functions

| Behavior | Primary owner |
|---|---|
| Intrinsic validity of one object's fields | That DataObject |
| Compatibility of independently valid objects | Named ActionObject |
| Transformation, comparison, or analysis | Named ActionObject |
| Tolerance, units policy, or algorithm selection | ActionObject performing the operation |
| Operation outcome or structured findings | ResultObject |
| Wire-format conversion | Serializer ActionObject |

Avoid module-level validation helpers when an invariant has a clear owner. A
private method or module-local function may mechanically implement public rules,
but must not hide scientific convention, policy, or a cross-object contract.

A small cohesive free function is justified only when the behavior has no domain
owner, mutable policy, or external boundary and a class would add no meaningful
contract. Do not create generic dumping-ground modules.

## Workflow objects

A Workflow is a concrete ActionObject for a genuine reusable composition with
explicit inputs, outputs, dependencies, ordering, failure meaning, and execution
semantics. Do not introduce one merely to own an integration test, group a
one-time sequence, or represent orchestration already owned by a task. Add no
generic Workflow base class without demonstrated shared behavior.

## Portability

Consider Rust or another language mapping only for an accepted cross-language
contract, shared serialized representation, authorized implementation task, or
concrete portability requirement. Where required, preserve explicit fields,
immutable semantics, deterministic versioned serialization, explicit errors,
and composition-friendly operation boundaries. Python-only internals do not
require speculative foreign-language designs.

## Review checklist

- Are fields explicit and operationally immutable?
- Does each intrinsic invariant belong to its DataObject?
- Is contract-authorized canonicalization distinguished from policy?
- Are compatibility, tolerances, units, algorithms, and acceptance on the owning
  ActionObject?
- Are nontrivial outcomes explicit immutable ResultObjects?
- Does serialization live in a serializer ActionObject?
- Is a free function genuinely ownerless and cohesive?
- Is a Workflow reusable behavior rather than test or task ceremony?
- Are dependencies explicit and hidden mutable or global state absent?
- Is abstraction supported by demonstrated polymorphism?
- Is portability required by an actual contract or task?
- Are subject, mathematics, representation, implementation, and evidence claims
  kept distinct?
