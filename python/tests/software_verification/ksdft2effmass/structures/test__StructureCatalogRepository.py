r"""Software verification of ``StructureCatalogRepository``.

Evidence profile: claim_bearing

Bounded artifact scope: immutable structure entries, stable serialization, append-only
SQLite revision composition, exact replay, and latest-entry reconstruction.

Facet and represented meaning

The module verifies that one structures-owned repository persists complete canonical
snapshot and symmetry records through the existing opaque atomic revision store.

Intrinsic and cross-object scope

``StructureCatalogRepository`` is the sole system under test. It composes public
catalog records, serializer behavior, and ``SQLiteAtomicRevisionStore`` without
reproducing shared-store internals.

VVUQ and scientific exclusions

All structure bytes and symmetry values are synthetic software fixtures. The tests do
not establish crystallographic correctness, scientific validation, production geometry,
external database availability, or protected calculation authority.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.persistence import SQLiteAtomicRevisionStore
from ksdft2effmass.structures.catalog import (
    StructureCatalogEntry,
    StructureCatalogEntrySerializer,
    StructureCatalogLoadStatus,
    StructureCatalogRepository,
    StructureCatalogRole,
    StructureCatalogWriteStatus,
    StructureSymmetry,
)

pytestmark = pytest.mark.software_verification
SUT = StructureCatalogRepository


class TestStructureCatalogRepository:
    """Own software evidence for append-only canonical structure persistence."""

    @staticmethod
    def entry(snapshot: bytes = b'{"unit_system":"metal"}\n') -> StructureCatalogEntry:
        """Return one complete synthetic external-reference catalog entry."""
        return StructureCatalogEntry(
            identity="materials-project:mp-149",
            role=StructureCatalogRole.EXTERNAL_REFERENCE,
            source_database="Materials Project",
            source_record_id="mp-149",
            source_url="https://materialsproject.org/materials/mp-149",
            source_content_id="sha256:" + hashlib.sha256(snapshot).hexdigest(),
            source_snapshot=snapshot,
            symmetry=StructureSymmetry(
                analyzer_identity="pymatgen.symmetry.analyzer.SpacegroupAnalyzer",
                analyzer_version="synthetic-version",
                symprec_angstrom=0.01,
                angle_tolerance_degree=5.0,
                space_group_symbol="Fd-3m",
                space_group_number=227,
                hall_symbol="F 4d 2 3 -1d",
                crystal_system="cubic",
                point_group_symbol="m-3m",
                wyckoff_symbols=("a", "a"),
                equivalent_atoms=(0, 0),
            ),
            limitations=("synthetic software fixture",),
        )

    @staticmethod
    def repository(path: Path) -> StructureCatalogRepository:
        """Return a catalog repository over one isolated local SQLite store."""
        return StructureCatalogRepository(
            SQLiteAtomicRevisionStore(
                path.resolve(), busy_timeout_ms=1000, max_payload_bytes=1_048_576
            )
        )

    def test_method__write__commits_and_loads_complete_entry(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-STRUCTURE-CATALOG-REPOSITORY-001

        Requirement: One catalog write atomically retains the complete immutable entry
        and one latest load reconstructs it exactly.

        Method: Commit one synthetic entry to an isolated SQLite store, load its stream,
        and compare the reconstructed value and revision identity.

        Oracle: The public entry serializer and atomic revision-store contract define
        exact byte and latest-revision behavior.

        Acceptance: Write is committed, load is loaded, identities agree, and the exact
        reconstructed entry equals the submitted value.

        Interpretation: Failure identifies lost fields, wrong stream binding, or broken
        domain-to-generic persistence composition.

        Limitations: One local transaction does not establish hardware durability or
        scientific correctness.
        """
        repository = self.repository(tmp_path / "structures.sqlite3")
        expected = self.entry()

        written = repository.write(expected)
        loaded = repository.load(expected.identity)

        assert written.status is StructureCatalogWriteStatus.COMMITTED
        assert loaded.status is StructureCatalogLoadStatus.LOADED
        assert loaded.revision_identity == written.revision_identity
        assert loaded.entry == expected

    def test_method__write__returns_unchanged_for_exact_snapshot_replay(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-STRUCTURE-CATALOG-REPOSITORY-002

        Requirement: Reimporting the exact current catalog entry must not create a new
        historical revision.

        Method: Submit the same immutable entry twice and load the resulting latest
        stream revision.

        Oracle: Equal canonical payload content identifies an idempotent current-state
        replay rather than a new revision.

        Acceptance: The first write commits, the second is unchanged, and both report
        the same revision identity.

        Interpretation: Failure identifies duplicate history or unstable serialization.

        Limitations: Concurrent competing writers are represented by the shared store's
        conflict path and are outside this sequential case.
        """
        repository = self.repository(tmp_path / "structures.sqlite3")
        entry = self.entry()

        first = repository.write(entry)
        second = repository.write(entry)

        assert first.status is StructureCatalogWriteStatus.COMMITTED
        assert second.status is StructureCatalogWriteStatus.UNCHANGED
        assert second.revision_identity == first.revision_identity

    def test_method__write__appends_changed_and_reverted_snapshots(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-STRUCTURE-CATALOG-REPOSITORY-003

        Requirement: Each changed snapshot appends after the observed head, including a
        deliberate return to bytes retained in an earlier historical revision.

        Method: Write snapshots A, B, and A sequentially to one identity and load the
        latest entry.

        Oracle: Revision identity binds both payload content and predecessor identity;
        latest reconstruction must equal the final submitted entry.

        Acceptance: All three writes commit with distinct revision identities and latest
        load reconstructs the final A entry.

        Interpretation: Failure identifies content-only revision collisions or broken
        append-only head advancement.

        Limitations: This sequential case does not exercise simultaneous writers.
        """
        repository = self.repository(tmp_path / "structures.sqlite3")
        entry_a = self.entry(b'{"unit_system":"metal","version":"A"}\n')
        entry_b = self.entry(b'{"unit_system":"metal","version":"B"}\n')

        written_a = repository.write(entry_a)
        written_b = repository.write(entry_b)
        written_a_again = repository.write(entry_a)
        loaded = repository.load(entry_a.identity)

        assert written_a.status is StructureCatalogWriteStatus.COMMITTED
        assert written_b.status is StructureCatalogWriteStatus.COMMITTED
        assert written_a_again.status is StructureCatalogWriteStatus.COMMITTED
        assert (
            len(
                {
                    written_a.revision_identity,
                    written_b.revision_identity,
                    written_a_again.revision_identity,
                }
            )
            == 3
        )
        assert loaded.entry == entry_a

    def test_method__serialize__round_trips_snapshot_and_symmetry(self) -> None:
        """Evidence ID: SV-STRUCTURE-CATALOG-REPOSITORY-004

        Requirement: The catalog wire preserves exact source bytes and every
        tolerance-qualified symmetry field.

        Method: Serialize and deserialize one complete entry through the public codec.

        Oracle: Structural equality of frozen records is the exact round-trip oracle.

        Acceptance: The reconstructed entry equals the original and its source checksum
        continues to authenticate the exact snapshot bytes.

        Interpretation: Failure identifies persistence loss or wire ambiguity.

        Limitations: Round-trip equality does not independently verify symmetry.
        """
        serializer = StructureCatalogEntrySerializer()
        expected = self.entry()

        observed = serializer.deserialize(serializer.serialize(expected))

        assert observed == expected
