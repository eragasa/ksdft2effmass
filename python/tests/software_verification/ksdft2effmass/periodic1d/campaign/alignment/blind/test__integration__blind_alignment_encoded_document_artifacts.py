r"""Artifact-owned integration evidence for row-041 blind-alignment documents.

Evidence profile: claim_bearing

Bounded artifact, route, and ownership scope
-------------------------------------------
The maintained blind-alignment ``input.json`` and ``result.json`` files, their
``SHA256SUMS`` entries, the curated leaf-package route, removal of the former
``BlindAlignmentCampaignModel`` route, and relocation of repository roots into explicit
calculation, retained-correlation, and verification requests.

Runtime and scientific boundary
-------------------------------
The tests perform bounded local reads of compact maintained JSON files and inspect typed
Python structure. They do not deserialize campaign content, authenticate transitive
sources, reveal hidden alignment truth, reconstruct numerical channels, or run campaign
or calculator behavior.

Scientific exclusions
---------------------
A pass establishes retained content identity and software ownership only. It does not
establish calculation provenance, information-boundary correctness, numerical or
scientific validity, uncertainty quantification, transferability, or acceptance.
"""

import hashlib
from dataclasses import fields
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign.alignment import (
    blind as blind_alignment_package,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind import (
    BlindAlignmentEncodedDocuments as PublicEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind import (
    encoded_documents as encoded_documents_module,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.campaign import (
    BlindAlignmentCampaignCalculationRequest,
    BlindAlignmentCampaignRetainedCorrelationRequest,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.result_records import (
    BlindAlignmentProvenance,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.verification import (
    BlindAlignmentCampaignVerificationRequest,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = encoded_documents_module.BlindAlignmentEncodedDocuments


class TestBlindAlignmentEncodedDocumentArtifacts:
    """Own row-041 retained-file, route, and location-split evidence."""

    repository_root = Path(__file__).resolve().parents[8]
    artifact_directory = repository_root / (
        "calculations/research-monograph/impurity-defect-1d-blind-alignment"
    )
    input_digest = "3476c0b1ed45913e5386be3688528d549f7eea15840b67559763d875406d7d48"
    result_digest = "a3b7d20c870fe5d87fd6a591fbafe9a997e7a261a5bc08163c3273b4789416fe"

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes]:
        """Read the two maintained row-041 payloads as exact bytes."""
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
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-041-ARTIFACT-001.

        Requirement: The renamed encoded owner preserves the exact maintained input and
        retained-result byte objects and their reviewed SHA-256 content identities.

        Method: Read both compact artifacts, construct the DataObject, and compare
        object identity and computed digests with the maintained checksum catalog.

        Oracle: The two reviewed SHA-256 values and their ``SHA256SUMS`` entries.

        Acceptance: Both fields retain supplied objects and both computed and catalog
        digests equal the reviewed values.

        Interpretation: A pass establishes exact retained-byte and content-identity
        preservation across the row-041 split.

        Limitations: Digest equality establishes content identity only, not provenance,
        decoded semantics, hidden-truth handling, numerical correctness, UQ, or
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

    def test_routes_and_request_fields__preserve_repository_location_split(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-041-ROUTE-001.

        Requirement: The curated leaf facade exposes the defining byte-only class,
        repository roots belong to explicit operation requests, and the former aggregate
        model and source module remain absent.

        Method: Compare facade identity, inspect exact dataclass fields for documents
        and all repository-reading request families, inspect ``__all__``, and check
        retired names and the former source path.

        Oracle: The documented row-041 ownership split and supported package surface.

        Acceptance: Documents have no repository root; all three request families own
        one, reject relative roots, and accept an absent absolute root without access;
        the facade exports only campaign and documents; retired routes are absent.

        Interpretation: A pass establishes explicit software ownership without
        performing filesystem access or source authentication.

        Limitations: Field placement does not prove that downstream Actions authenticate
        sources correctly or preserve the blind information boundary.
        """
        assert PublicEncodedDocuments is SUT
        assert blind_alignment_package.BlindAlignmentEncodedDocuments is SUT
        assert blind_alignment_package.__all__ == [
            "BlindAlignmentCampaign",
            "BlindAlignmentEncodedDocuments",
        ]
        assert [field.name for field in fields(SUT)] == [
            "input_document",
            "retained_result_document",
        ]
        for request_type in (
            BlindAlignmentCampaignCalculationRequest,
            BlindAlignmentCampaignRetainedCorrelationRequest,
            BlindAlignmentCampaignVerificationRequest,
        ):
            assert "repository_root" in {field.name for field in fields(request_type)}

        documents = SUT(b"synthetic input", b"synthetic result")
        provenance = BlindAlignmentProvenance(
            input_path="input.json",
            input_sha256="0" * 64,
            script_path="run.py",
            script_sha256="1" * 64,
            python_version="synthetic",
            numpy_version="synthetic",
        )
        absent_absolute_root = tmp_path / "absent-repository-root"
        assert not absent_absolute_root.exists()
        requests = (
            BlindAlignmentCampaignCalculationRequest(
                documents, absent_absolute_root, provenance
            ),
            BlindAlignmentCampaignRetainedCorrelationRequest(
                documents, absent_absolute_root
            ),
            BlindAlignmentCampaignVerificationRequest(documents, absent_absolute_root),
        )
        assert all(
            request.repository_root is absent_absolute_root for request in requests
        )
        for request_constructor in (
            lambda: BlindAlignmentCampaignCalculationRequest(
                documents, Path("relative-root"), provenance
            ),
            lambda: BlindAlignmentCampaignRetainedCorrelationRequest(
                documents, Path("relative-root")
            ),
            lambda: BlindAlignmentCampaignVerificationRequest(
                documents, Path("relative-root")
            ),
        ):
            with pytest.raises(ValueError, match="repository_root must be absolute"):
                request_constructor()

        retired_name = "BlindAlignmentCampaignModel"
        assert not hasattr(blind_alignment_package, retired_name)
        # A removed export is insufficient if an aggregate forwarding module survives.
        retired_module = (
            self.repository_root
            / "python/src/ksdft2effmass/campaigns/periodic_1d/defects"
            / "blind_alignment/model.py"
        )
        assert not retired_module.exists()
