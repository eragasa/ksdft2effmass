# `citation_snapshot.records`

`records.py` owns immutable public DataObjects, the exact Request/Result boundary,
closed enums, and structured compiler failures. Records contain source lineage and
structural citation semantics but no manuscript excerpts or absolute paths inside the
snapshot. `ManuscriptCitationSnapshot` and
`ResearchMonographCitationSnapshotResult` invoke the package integrity replay before
construction succeeds.

- [Schematic](schematic.md)
- [Implementation](implementation.md)

```{toctree}
:maxdepth: 1
:hidden:

schematic
implementation
CitationContentAlgorithm/index
CitationContentIdentity/index
CitationSnapshotError/index
CitationSnapshotErrorCode/index
ManuscriptBibliographyEntrySnapshot/index
ManuscriptCitationCall/index
ManuscriptCitationCommandKind/index
ManuscriptCitationGroup/index
ManuscriptCitationOccurrence/index
ManuscriptCitationOrigin/index
ManuscriptCitationPriority/index
ManuscriptCitationSnapshot/index
ManuscriptCitationSourceGap/index
ManuscriptCitationSourceGapReason/index
ManuscriptCitationTodo/index
ManuscriptIncludeInstance/index
ManuscriptSourceFileSnapshot/index
ManuscriptSourceLocator/index
ResearchMonographCitationSnapshotRequest/index
ResearchMonographCitationSnapshotResult/index
```
