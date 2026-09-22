# Workflow model

The scientific and computational workflow is a stateful Colored Petri Net (CPN). Static Python imports should remain acyclic where practical, but an import dependency view is not the workflow model.

The CPN supports typed colored tokens, multisets, guards, independent branches, synchronization joins, retries, failures, recovery, repeated convergence iterations, durable markings, provenance, parent-child run lineage, and scope-explicit accepted/rejected/failed/blocked outcomes. Failed attempts remain terminal history while retries use new attempt identities; blocked branches normally remain recoverable unless explicitly finalized.

Computational gates such as G01a, G01b, and G02 are predicates over accepted typed evidence in a durable marking. They are not Boolean graph-node completion flags.

After a concrete integration has produced an immutable extracted Kohn--Sham
ResultObject, `NormalizedObservationAssembler` may assemble it through the
calculator-independent `NormalizedObservationSource` protocol. The returned
`NormalizedObservationSet` retains each exact source object in declared order and
requires its identity to differ from every source identity, unique source-result
identities and manifest-revision/entry pairs, content/provenance agreement, explicit
parser and policy identities, and canonical
limitations. Assembly performs no parsing, unit conversion, calculator execution, or
scientific acceptance;
invalid membership returns a closed failure with no partial set.

External execution is always two phase:

```text
immutable authorized request
    -> durable requested marking
    -> external adapter outside guard evaluation
    -> correlated immutable result or failure
    -> recording transition
```

Guards are pure and may inspect immutable token fields only. The accepted periodic electronic-structure dataset remains the provenance-aware common parent of the direct-TB and Wannier branches. A deferred paired QE–ABINIT conformance subnet is separate from the prospective QE production path.

See [Colored Petri Nets](colored-petri-nets.md), the [implemented Architecture v1 snapshot](../architecture/v1/index.md), and the [Architecture v2 target](../architecture/v2/index.md).
