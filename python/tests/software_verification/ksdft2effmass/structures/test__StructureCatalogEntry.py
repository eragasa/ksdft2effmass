r"""Software verification of ``StructureCatalogEntry``.

Evidence profile: claim_bearing

Bounded artifact scope: source-snapshot checksum binding in one immutable catalog entry.

Facet and represented meaning

The module verifies that retained source content identity authenticates the exact
snapshot bytes before an entry can reach persistence.

Intrinsic and cross-object scope

``StructureCatalogEntry`` is the sole system under test. Synthetic symmetry metadata
only supplies the complete constructor boundary.

VVUQ and scientific exclusions

All values are synthetic software fixtures. This evidence does not establish external
source authenticity, crystallographic correctness, or scientific validation.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.structures.catalog import (
    StructureCatalogEntry,
    StructureCatalogRole,
    StructureSymmetry,
)

pytestmark = pytest.mark.software_verification
SUT = StructureCatalogEntry


class TestStructureCatalogEntry:
    """Own software evidence for intrinsic source-content authentication."""

    @staticmethod
    def symmetry() -> StructureSymmetry:
        """Return complete synthetic symmetry metadata."""
        return StructureSymmetry(
            analyzer_identity="synthetic.analyzer",
            analyzer_version="1",
            symprec_angstrom=0.01,
            angle_tolerance_degree=5.0,
            space_group_symbol="P1",
            space_group_number=1,
            hall_symbol="P 1",
            crystal_system="triclinic",
            point_group_symbol="1",
            wyckoff_symbols=("a",),
            equivalent_atoms=(0,),
        )

    def test_constructor__source_snapshot__rejects_checksum_mismatch(self) -> None:
        """Evidence ID: SV-STRUCTURE-CATALOG-ENTRY-001

        Requirement: A catalog entry must bind its declared SHA-256 content identity to
        the exact retained source snapshot bytes.

        Method: Construct an otherwise complete entry with a deliberately mismatched
        digest and snapshot.

        Oracle: SHA-256 over the exact source bytes is the catalog content-identity
        contract.

        Acceptance: Construction raises ``ValueError`` before persistence.

        Interpretation: Failure would admit unverifiable or misbound provenance.

        Limitations: Digest agreement establishes byte identity, not source truth.
        """
        with pytest.raises(
            ValueError, match="source_content_id must authenticate source_snapshot"
        ):
            SUT(
                identity="materials-project:mp-synthetic",
                role=StructureCatalogRole.EXTERNAL_REFERENCE,
                source_database="Materials Project",
                source_record_id="mp-synthetic",
                source_url="https://materialsproject.org/materials/mp-synthetic",
                source_content_id="sha256:" + "0" * 64,
                source_snapshot=b"synthetic snapshot",
                symmetry=self.symmetry(),
                limitations=("synthetic software fixture",),
            )
