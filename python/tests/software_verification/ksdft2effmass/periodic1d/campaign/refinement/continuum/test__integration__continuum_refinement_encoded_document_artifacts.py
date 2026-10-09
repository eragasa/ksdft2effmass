r"""Artifact-owned integration evidence for row-042 continuum-refinement documents.

Evidence profile: claim_bearing

Bounded artifact, route, and ownership scope
-------------------------------------------
The maintained continuum-refinement ``input.json`` and ``result.json`` files, their
``SHA256SUMS`` entries, the curated leaf-package route, removal of the former
``ContinuumRefinementCampaignModel`` route, and separation of repository location from
encoded bytes at retained-correlation and verification operation boundaries.

Runtime and scientific boundary
-------------------------------
The tests perform bounded local reads of compact maintained JSON files and inspect typed
Python structure. They do not deserialize campaign content, authenticate transitive
sources, reconstruct operators or spectra, execute refinement axes, or invoke a
calculator or retained-result verifier.

Scientific exclusions
---------------------
A pass establishes retained content identity and software ownership only. It does not
establish provenance, asymptotic convergence, continuum-limit validity, material
adequacy, transferability, uncertainty quantification, or acceptance.
"""

import hashlib
import inspect
from dataclasses import fields
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign.refinement import (
    continuum as continuum_refinement_package,
)
from ksdft2effmass.periodic1d.campaign.refinement.continuum import (
    ContinuumRefinementEncodedDocuments as PublicEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.refinement.continuum import (
    campaign as campaign_module,
)
from ksdft2effmass.periodic1d.campaign.refinement.continuum import (
    encoded_documents as encoded_documents_module,
)
from ksdft2effmass.periodic1d.campaign.refinement.continuum import (
    verification as verification_module,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = encoded_documents_module.ContinuumRefinementEncodedDocuments
CAMPAIGN = campaign_module.ContinuumRefinementCampaign
VERIFICATION_REQUEST = verification_module.ContinuumRefinementVerificationRequest


class TestContinuumRefinementEncodedDocumentArtifacts:
    """Own row-042 retained-file, route, and location-split evidence."""

    repository_root = Path(__file__).resolve().parents[8]
    artifact_directory = repository_root / (
        "calculations/research-monograph/impurity-defect-1d-continuum-refinement"
    )
    input_digest = "55d647a8c259d3a1f1e5c756b496a9d1a16fee0a691c7b53d2f877da5f287fdd"
    result_digest = "1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc"

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes]:
        """Read the two maintained row-042 payloads as exact bytes."""
        return (
            (cls.artifact_directory / "input.json").read_bytes(),
            (cls.artifact_directory / "result.json").read_bytes(),
        )

    @classmethod
    def _catalog_digests(cls) -> dict[str, str]:
        """Read the maintained checksum catalog without decoding campaign payloads."""
        return {
            path: digest
            for digest, path in (
                line.split(maxsplit=1)
                for line in (cls.artifact_directory / "SHA256SUMS")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            )
        }

    def test_retained_artifacts__preserve_exact_bytes_and_catalog_identities(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-042-ARTIFACT-001.

        Requirement: The renamed encoded owner preserves exact maintained input and
        retained-result objects plus reviewed SHA-256 content identities.

        Method: Read both compact artifacts, construct the DataObject, and compare
        object identity and computed digests with the maintained checksum catalog.

        Oracle: The two reviewed SHA-256 values and their ``SHA256SUMS`` entries.

        Acceptance: Both fields retain supplied objects and both computed and catalog
        digests equal the reviewed values.

        Interpretation: A pass establishes exact retained-byte and content-identity
        preservation across the row-042 split.

        Limitations: Digest equality establishes content identity only, not provenance,
        decoded semantics, continuum convergence, scientific validity, UQ, or
        acceptance.
        """
        input_document, result_document = self._retained_payloads()
        documents = SUT(input_document, result_document)
        catalog = self._catalog_digests()

        assert documents.input_document is input_document
        assert documents.retained_result_document is result_document
        assert hashlib.sha256(documents.input_document).hexdigest() == self.input_digest
        assert (
            hashlib.sha256(documents.retained_result_document).hexdigest()
            == self.result_digest
        )
        # Bind reviewed constants to maintained content identities, not provenance.
        assert catalog["input.json"] == self.input_digest
        assert catalog["result.json"] == self.result_digest

    def test_routes_and_operation_roots__preserve_repository_location_split(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-042-ROUTE-001.

        Requirement: The curated facade exposes the defining byte-only class,
        correlation receives an explicit absolute root, verification owns its root in a
        typed request, and the former aggregate model and source module remain absent.

        Method: Compare facade identity, inspect fields and signatures, exercise root
        validation without source access, inspect ``__all__``, and check retired paths.

        Oracle: The documented row-042 ownership and operation-boundary split.

        Acceptance: Documents have no root; verification requests accept a nonexistent
        absolute root without access and reject relative roots; correlation rejects
        unsupported or relative roots before decoding; retired routes are absent.

        Interpretation: A pass establishes explicit location ownership without
        authenticating sources or executing refinement calculations.

        Limitations: Structural boundaries do not prove source authentication,
        numerical reconstruction, asymptotic convergence, or physical adequacy.
        """
        assert PublicEncodedDocuments is SUT
        assert continuum_refinement_package.ContinuumRefinementEncodedDocuments is SUT
        assert continuum_refinement_package.__all__ == [
            "ContinuumRefinementCampaign",
            "ContinuumRefinementCampaignResultDocument",
            "ContinuumRefinementEncodedDocuments",
        ]
        assert [field.name for field in fields(SUT)] == [
            "input_document",
            "retained_result_document",
        ]
        assert [field.name for field in fields(VERIFICATION_REQUEST)] == [
            "encoded_documents",
            "repository_root",
        ]
        assert list(inspect.signature(CAMPAIGN.correlate_retained).parameters) == [
            "self",
            "repository_root",
        ]

        documents = SUT(b"synthetic input", b"synthetic result")
        campaign = CAMPAIGN(documents)
        absent_absolute_root = tmp_path / "absent-repository-root"
        assert not absent_absolute_root.exists()
        request = VERIFICATION_REQUEST(documents, absent_absolute_root)
        assert request.repository_root is absent_absolute_root

        with pytest.raises(ValueError, match="repository_root must be absolute"):
            VERIFICATION_REQUEST(documents, Path("relative-root"))
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.correlate_retained(Path("relative-root"))
        with pytest.raises(TypeError, match="repository_root must be pathlib.Path"):
            campaign.correlate_retained("relative-root")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.verify_retained(Path("relative-root"))

        retired_name = "ContinuumRefinementCampaignModel"
        assert not hasattr(continuum_refinement_package, retired_name)
        retired_package = self.repository_root / (
            "python/src/ksdft2effmass/campaigns/periodic_1d/defects/"
            "continuum_refinement"
        )
        assert not retired_package.exists()
