# Persistence and projections

## Separate persisted state

Development and scientific state use separate persistence contracts.

Development persistence represents `HarnessTask`,
`DevelopmentTaskSelection`, development decisions, capabilities, evidence, and
repository projections. Scientific persistence represents `Campaign`,
`CampaignRun`, CPN definitions and markings, simulation/result correlations,
artifact lineage, analyses, and dispositions.

No database table or serialized document is shared merely to simplify queries.
Cross-plane references use immutable identities.

## Scientific persistence

A persisted `CampaignRun` records:

- schema and campaign-definition versions;
- run and attempt identities;
- exact `CpnMarking` token colors and payloads;
- request/result correlation;
- simulation and artifact identities;
- retry and failure history where required; and
- parent-child run lineage.

It does not pickle runtime engines, arbitrary Python objects, closures,
credentials, process handles, open files, or calculator clients. CPN guards and
inscriptions use closed versioned representations.

## Development projections

Development authority is compiled into complete deterministic projections for
inspection, documentation, and recovery. Projection formats may include SQLite,
deterministic SQL, generated Task Markdown, indexes, graphs, and manifests. A
projection is never loaded as fallback authority when its source disagrees.

The loader, compiler, validation, projector, synchronization, and comparison
boundaries are defined by the [compiler architecture](compiler-architecture.md).
Persistence owns representation and storage contracts; it does not reinterpret
a normalized development state or create an alternate compilation path.

## Publication storage boundary

Publication accepts only a complete validated artifact set, applies a defined
rollback boundary, and removes temporary state. Maintained SQLite is an
immutable projection. Write-capable connections, WAL, SHM, and journals belong
only to temporary or disposable runtime copies.

Persistence verification covers integrity, foreign keys, schema and version
identities, projection-manifest closure, and applicable canonical-format rules.
Raw SQLite byte inequality alone is not semantic drift unless canonical bytes
are explicitly contracted.

## Scientific views

Read models may project scientific state for inspection, but they do not replace
`CampaignRun` authority or create `ScientificDisposition`. A dashboard,
visualization, or graph is always derived and cannot authorize execution or
accept a scientific result.
