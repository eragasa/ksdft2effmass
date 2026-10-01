# Compilation implementation

`RepositoryRevisionInspector` reads worktree and common Git metadata to obtain an
exact 40-character HEAD. `RepositoryHeadSourceVerifier` compares every consumed TeX
and bibliography byte sequence with the blob at that explicit object ID; a dirty,
untracked, absent, or inaccessible relevant source fails with
`source_differs_from_revision`.

The graph compiler confines resolved paths to the monograph root, rejects missing
sources and cycles, records exact content identities, and preserves source event
order. The semantic compiler reconciles literal keys with bibliography entries,
derives closure sets, invokes complete integrity replay, and returns only
`ResearchMonographCitationSnapshotResult`.
