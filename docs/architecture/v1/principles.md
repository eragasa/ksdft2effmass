# Architecture v1 principles

## Authority is explicit

Current human instruction and durable human decisions outrank specifications, repository policy, Task records, procedures, generated reports, and historical evidence. Passing checks and successful processes do not imply authorization or acceptance.

## Source and projection are distinct

Task JSON, chain selection, unresolved checkpoints, specifications, and other declared inputs are authoritative in their respective domains. SQLite, SQL, graphs, indexes, and manifests are derived projections. A projection cannot silently replace a disagreeing source.

## Scientific claims are classified

Software verification, numerical verification, scientific validation, uncertainty quantification, process success, and human acceptance are distinct. V1 records these distinctions but does not enforce them through one independent scientific-run aggregate.

## Scientific representations are separated

Physical models, mathematical objects, finite representations, and software objects are not interchangeable. Periodic geometry, Kohn–Sham observations, plane-wave metadata, calculator syntax, and provenance have separate owners.

## Records are immutable where implemented

Public scientific and harness records use immutable or operationally immutable DataObjects and ResultObjects. Reusable behavior belongs to ActionObjects. Serialization, external execution, comparison policy, and acceptance are not intrinsic DataObject behavior.

## External effects are bounded

Production or protected execution requires explicit human authority. Direct runners bind exact input, executable, pseudopotential, resource, output, and retention identities before invocation. Large calculator artifacts remain outside Git.

## CPN semantics are calculator-independent

CPN guards, enablement, and firing operate on immutable represented values and perform no external I/O. The implemented CPN is a semantic foundation; it is not the authority that drove V1 calculator executions.

## Known architectural constraint

Development Task state coordinates both software work and scientific execution preparation. This coupling is an implemented V1 fact, not an endorsement of a shared development and scientific lifecycle.
