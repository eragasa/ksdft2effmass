r"""Software verification of ``DevelopmentDecisionMigrator``.

Evidence profile: routine

Bounded artifact scope: manifest-driven one-way legacy checkpoint migration and
post-verification source deletion in an isolated filesystem.

Facet and represented meaning

The ActionObject preserves exact legacy provenance in canonical v1 decision bytes and
deletes only explicitly selected source files after complete verification.

Intrinsic and cross-object scope

Tests cover proposal, canonical writing, verification, provenance identity, and
source-deletion ordering. Repository configuration cutover remains separate.

VVUQ and scientific exclusions

Synthetic filesystem operations establish software behavior only. They grant no
operation authority, scientific validity, release status, or human acceptance.
"""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath

import pytest

from ksdft2effmass.harness.decision_migration import (
    DevelopmentDecisionMigrationManifestSerializer,
    DevelopmentDecisionMigrator,
)
from ksdft2effmass.harness.decisions import DevelopmentDecisionSerializer

pytestmark = pytest.mark.software_verification
SUT = DevelopmentDecisionMigrator


class TestDevelopmentDecisionMigrator:
    """Own maintained evidence for explicit checkpoint migration."""

    @staticmethod
    def legacy_payload() -> bytes:
        """Return one maintained valid legacy checkpoint fixture."""
        return (
            Path(__file__).parent / "resources" / "legacy-checkpoint.json"
        ).read_bytes()

    def test_method__migration_phases__verify_before_selected_source_deletion(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-DEVELOPMENT-DECISION-MIGRATION-001

        Requirement: Migration must retain exact source provenance, produce canonical
        successor bytes, and delete no source until every successor verifies.

        Method: Propose, serialize, write, verify, and delete one isolated fixture.

        Oracle: The original source SHA-256, canonical serializer round trip, and
        explicit migration-manifest paths.

        Acceptance: The target is canonical and retains the original digest; write and
        verification retain both source files; deletion removes only selected source
        and obsolete-schema files while preserving the canonical successor.

        Interpretation: The phased ActionObject supports cutover without an implicit
        rewrite or pre-verification deletion.

        Limitations: Atomic repository configuration cutover is tested by its owning
        Harness projection and validation surfaces.
        """
        root = tmp_path.resolve()
        source_root = root / ".pi" / "checkpoints"
        source_root.mkdir(parents=True)
        source = source_root / "legacy-checkpoint.json"
        schema = source_root / "checkpoint.schema.json"
        payload = self.legacy_payload()
        source.write_bytes(payload)
        schema.write_text("{}\n", encoding="utf-8")
        migrator = SUT()

        manifest, proposed = migrator.propose(
            root, PurePosixPath(".pi/checkpoints"), PurePosixPath("decisions")
        )
        manifest_payload = DevelopmentDecisionMigrationManifestSerializer().serialize(
            manifest
        )
        restored_manifest = (
            DevelopmentDecisionMigrationManifestSerializer().deserialize(
                manifest_payload
            )
        )
        written = migrator.write(root, restored_manifest)
        verified = migrator.verify(root, restored_manifest)
        target = root / "decisions" / "legacy-checkpoint.json"
        decision = DevelopmentDecisionSerializer().deserialize(target.read_bytes())

        assert proposed.phase == "proposed"
        assert written.phase == "written"
        assert verified.phase == "verified"
        assert source.is_file()
        assert schema.is_file()
        assert (
            decision.source_provenance.source_artifact_identity
            == hashlib.sha256(payload).hexdigest()
        )

        deleted = migrator.delete_sources(root, restored_manifest)

        assert deleted.phase == "sources_deleted"
        assert not source.exists()
        assert not schema.exists()
        assert target.is_file()

        cutover = migrator.verify_cutover(root, restored_manifest)

        assert cutover.phase == "cutover_verified"
        assert cutover.target_count == 1
