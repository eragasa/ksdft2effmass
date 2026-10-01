# `ResearchMonographCitationSnapshotCompiler`

Public semantic performer for the fixed research-monograph entrypoint and sibling
bibliography. `execute(request)` reads exact source bytes, resolves the confined
include graph, parses the closed grammar, requires every consumed source to equal its
recorded HEAD blob, assembles all immutable records, invokes complete integrity
replay, and returns a replay-valid `ResearchMonographCitationSnapshotResult`.
Failures raise `CitationSnapshotError` and return no partial snapshot.
