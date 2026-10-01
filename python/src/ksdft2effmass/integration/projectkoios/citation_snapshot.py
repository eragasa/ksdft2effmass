"""One-way adaptation of owner citation Results to Project Koios target records.

This optional integration boundary consumes one exact replay-valid ksdft citation
snapshot Result and constructs only the neutral target records owned by
``projectkoios.references.citations``.  It creates no bibliography observation
binding, identity decision, availability evidence, document projection, rights state,
processing authority, or downstream status.
"""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.references.citations import (
    CitationContentIdentity as KoiosCitationContentIdentity,
)
from projectkoios.references.citations import (
    CitationSourceLocator as KoiosCitationSourceLocator,
)
from projectkoios.references.citations import (
    CitationTargetBibliographyEntry,
    CitationTargetGroup,
    CitationTargetOccurrence,
    CitationTargetSnapshot,
    CitationTargetSourceGap,
)

from ksdft2effmass.campaigns.research_monograph.citation_snapshot import (
    CitationContentIdentity,
    ManuscriptBibliographyEntrySnapshot,
    ManuscriptCitationOccurrence,
    ManuscriptCitationSourceGap,
    ManuscriptSourceLocator,
    ResearchMonographCitationSnapshotIntegrityValidator,
    ResearchMonographCitationSnapshotResult,
)


@dataclass(frozen=True, slots=True)
class ResearchMonographCitationTargetSnapshotAdapter:
    """Adapt one owner Result to the reviewed neutral Project Koios projection.

    The adapter preserves target-owned identities, literal keys, locators, content
    identities, ordering, closure tuples, and nullable bibliography-observation
    bindings.  Owner-only source-file, include, call, todo, request, result, parser,
    generator, and repository-revision records do not cross this reduced boundary.
    """

    def execute(
        self, result: ResearchMonographCitationSnapshotResult
    ) -> CitationTargetSnapshot:
        """Return the neutral target snapshot for one exact replay-valid Result.

        Parameters
        ----------
        result
            Complete immutable ksdft citation snapshot Result.

        Returns
        -------
        projectkoios.references.citations.CitationTargetSnapshot
            Canonical neutral target projection.  Its ``target_projection_id`` is
            derived by the Project Koios owner.

        Raises
        ------
        TypeError
            ``result`` is not the exact supported Result type.
        ValueError
            Owner integrity replay fails or Project Koios rejects the neutral
            projection.
        """
        if type(result) is not ResearchMonographCitationSnapshotResult:
            raise TypeError("result must be ResearchMonographCitationSnapshotResult")
        expected = ResearchMonographCitationSnapshotIntegrityValidator().execute(
            result.snapshot, result.request_id
        )
        if result.result_id != expected:
            raise ValueError("result_id does not replay from the complete snapshot")
        snapshot = result.snapshot
        return CitationTargetSnapshot(
            snapshot_id=snapshot.snapshot_id,
            bibliography_source_path=snapshot.bibliography_path,
            bibliography_content_identity=self._content_identity(
                snapshot.bibliography_content_identity
            ),
            occurrences=tuple(
                self._occurrence(value) for value in snapshot.occurrences
            ),
            groups=tuple(
                CitationTargetGroup(
                    group_id=value.group_id,
                    group_index=value.group_index,
                    key=value.key,
                    occurrence_indexes=value.occurrence_indexes,
                    direct_occurrence_count=value.direct_occurrence_count,
                    generated_occurrence_count=value.generated_occurrence_count,
                    bibliography_entry_index=value.bibliography_entry_index,
                )
                for value in snapshot.groups
            ),
            bibliography_entries=tuple(
                self._entry(value) for value in snapshot.bibliography_entries
            ),
            source_gaps=tuple(self._gap(value) for value in snapshot.source_gaps),
            missing_keys=snapshot.missing_keys,
            duplicate_keys=snapshot.duplicate_keys,
            uncited_keys=snapshot.uncited_keys,
        )

    @staticmethod
    def _content_identity(
        value: CitationContentIdentity,
    ) -> KoiosCitationContentIdentity:
        """Adapt one exact target-owned content identity."""
        return KoiosCitationContentIdentity(
            algorithm=value.algorithm.value,
            digest=value.digest,
            byte_count=value.byte_count,
        )

    def _locator(self, value: ManuscriptSourceLocator) -> KoiosCitationSourceLocator:
        """Adapt one excerpt-free target locator."""
        return KoiosCitationSourceLocator(
            source_path=value.source_path,
            source_content_identity=self._content_identity(
                value.source_content_identity
            ),
            include_index=value.include_index,
            byte_start=value.byte_start,
            byte_end=value.byte_end,
            line=value.line,
            column=value.column,
        )

    def _occurrence(
        self, value: ManuscriptCitationOccurrence
    ) -> CitationTargetOccurrence:
        """Adapt one literal-key occurrence without adding status."""
        return CitationTargetOccurrence(
            occurrence_id=value.occurrence_id,
            occurrence_index=value.occurrence_index,
            call_index=value.call_index,
            key_index=value.key_index,
            key=value.key,
            origin=value.origin.value,
            locator=self._locator(value.locator),
            bibliography_entry_index=value.bibliography_entry_index,
            todo_marker_index=value.todo_marker_index,
        )

    def _entry(
        self, value: ManuscriptBibliographyEntrySnapshot
    ) -> CitationTargetBibliographyEntry:
        """Adapt one entry while preserving the null observation binding."""
        return CitationTargetBibliographyEntry(
            entry_id=value.bibliography_entry_id,
            entry_index=value.entry_index,
            key=value.key,
            entry_type=value.entry_type,
            locator=self._locator(value.locator),
            entry_content_identity=self._content_identity(value.entry_content_identity),
            source_bibliography_observation_id=(
                value.source_bibliography_observation_id
            ),
        )

    def _gap(self, value: ManuscriptCitationSourceGap) -> CitationTargetSourceGap:
        """Adapt one non-key source gap without inventing a citation key."""
        return CitationTargetSourceGap(
            source_gap_id=value.source_gap_id,
            source_gap_index=value.source_gap_index,
            locator=self._locator(value.locator),
            reason=value.reason.value,
            placeholder_identifier=value.placeholder_identifier,
        )
