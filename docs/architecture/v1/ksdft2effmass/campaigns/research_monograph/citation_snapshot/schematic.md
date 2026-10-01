# Citation snapshot schematic

```mermaid
flowchart LR
    request[ResearchMonographCitationSnapshotRequest]
    compiler[ResearchMonographCitationSnapshotCompiler]
    head[Exact Git HEAD blobs]
    parser[Closed TeX and BibLaTeX parsers]
    snapshot[ManuscriptCitationSnapshot]
    integrity[ResearchMonographCitationSnapshotIntegrityValidator]
    result[ResearchMonographCitationSnapshotResult]
    consumer[Reduced neutral adapter]

    request --> compiler
    head --> compiler
    compiler --> parser
    parser --> snapshot
    snapshot --> integrity
    request --> integrity
    integrity --> result
    result --> consumer
```

The absolute repository root is execution input only. The durable request identity
covers the fixed operation and relative contract paths. Exact HEAD admission binds
all consumed source bytes to the recorded revision. The snapshot identity covers
that source lineage; the result identity additionally covers the complete canonical
snapshot projection. Both the snapshot constructor and Result constructor replay the
same integrity policy, while the compiler uses it before returning the Result.

The reduced neutral adapter is downstream-owned. It may project only agreed fields;
it cannot repair or legitimize an invalid owner Result.
