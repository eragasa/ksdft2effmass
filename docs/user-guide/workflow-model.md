# Workflow model

The scientific and computational workflow is a stateful Colored Petri Net (CPN). Static Python imports should remain acyclic where practical, but an import dependency view is not the workflow model.

The CPN supports typed colored tokens, multisets, guards, independent branches, synchronization joins, retries, failures, recovery, repeated convergence iterations, durable markings, provenance, parent-child run lineage, and scope-explicit accepted/rejected/failed/blocked outcomes. Failed attempts remain terminal history while retries use new attempt identities; blocked branches normally remain recoverable unless explicitly finalized.

Computational gates such as G01a, G01b, and G02 are predicates over accepted typed evidence in a durable marking. They are not Boolean graph-node completion flags.

External execution is always two phase:

```text
immutable authorized request
    -> durable requested marking
    -> external adapter outside guard evaluation
    -> correlated immutable result or failure
    -> recording transition
```

Guards are pure and may inspect immutable token fields only. The accepted periodic electronic-structure dataset remains the provenance-aware common parent of the direct-TB and Wannier branches. A deferred paired QE–ABINIT conformance subnet is separate from the prospective QE production path.

See [Colored Petri Nets](colored-petri-nets.md), the authoritative [CPN architecture](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/architecture/colored-petri-net-workflows.md), and the [periodic integration boundary](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/architecture/periodic-electronic-structure-integration.md).
