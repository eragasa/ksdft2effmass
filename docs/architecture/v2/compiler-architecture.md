# Compiler architecture

## Purpose

The development harness uses one deterministic compiler architecture to turn a
closed snapshot of authoritative repository inputs into validated normalized
state and complete derived projections. Compilation is distinct from repository
loading, domain validation, projection, publication, and comparison.

The semantic path is:

```text
authoritative inputs
→ immutable source snapshot
→ normalized development state
→ domain validation
→ complete candidate artifact set
```

Synchronization and checking consume that same candidate artifact set:

```text
synchronize: candidate artifact set → validate publication boundary → publish
check:       candidate artifact set → compare with maintained artifacts
```

No synchronization-only or check-only path may independently reinterpret source
authority.

## Repository loader

The repository loader owns explicit repository I/O. It receives an explicit
repository root and an operation-specific input contract, resolves only declared
sources, and returns an immutable `HarnessSourceSnapshot`.

The snapshot contains source identities, parsed source values, and the provenance
needed to trace normalized values and findings back to authoritative inputs. It
contains no open files, mutable parser nodes, database connections, temporary
paths, or ambient current-directory assumptions.

Generated projections are not source inputs unless a separate authoritative
contract explicitly declares them as such.

## Compiler

`HarnessCompiler` is a deterministic transformation:

```text
HarnessSourceSnapshot → HarnessState
```

It owns normalization of identifiers, relationships, ordering, and equivalent
source representations. It preserves source provenance but does not perform
repository I/O, invoke command-line tools, authorize actions, publish files, or
read maintained projections as fallback authority.

Equivalent snapshots produce equivalent normalized state. Normalization never
silently repairs conflicting authority; conflicts remain explicit validation
findings.

## Validation boundary

Domain validators own their respective rules for development Tasks, active
selection, dependency graphs, unresolved decisions, capabilities, resources,
evidence, and generated-artifact closure. Validation composition owns only
deterministic ordering and cross-domain closure.

A `ValidationResult` states the exact inputs and claim boundary. Structural
success does not establish software-test success, numerical verification,
scientific validation, uncertainty quantification, protected authorization, or
human acceptance.

## Projector

`HarnessProjector` deterministically maps one validated `HarnessState` to one
complete `HarnessArtifactSet`. An artifact set declares its full path and format
closure before publication and may contain SQLite, deterministic SQL, generated
Task documentation, indexes, graphs, and manifests.

A projector:

- performs no source discovery;
- writes no maintained destination;
- grants no action authority;
- exposes all generated artifact identities; and
- never presents a partial candidate as current state.

A format-specific projector is an output strategy, not an independent authority
model.

## Synchronizer and comparator

`HarnessSynchronizer` is the sole owner of maintained publication. It accepts
only a complete validated artifact set, applies a bounded rollback contract,
removes stale projector-owned artifacts, and closes mutable resources before
publication.

`HarnessStateComparator` is read-only. It compares the candidate artifact set
with maintained artifacts using exact bytes where a canonical-byte contract
exists and normalized semantics where the format contract permits physical-byte
variation. It has no dependency on publication behavior and no write capability.

The synchronizer does not compile policy. The comparator does not repair drift.

## Determinism and failure

Compiler and projector determinism is defined over explicit input identities,
schema versions, normalization rules, and format versions. Failures retain their
owning phase: loading, compilation, domain validation, projection, candidate
validation, publication, or comparison.

A failed phase publishes nothing. Diagnostics identify the phase, governing
input identities, and source provenance without exposing credentials or private
data.

## Authority limits

The compiler architecture belongs to the development harness. It does not load
or advance scientific `CampaignRun` state, interpret calculator observations,
create `ScientificAnalysis`, or record `ScientificDisposition`. Scientific
workflow compilation, if introduced, requires its own contract under the
scientific execution harness and cannot reuse development authority implicitly.
