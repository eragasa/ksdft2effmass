r"""Artifact-owned integration evidence for row-044 route documents.

Evidence profile: claim_bearing

Bounded artifact, route, and ownership scope
-------------------------------------------
The maintained independent-route ``input.json`` and ``result.json`` files, their
``SHA256SUMS`` entries, the curated leaf-package route, removal of the former
``RouteReconciliationCampaignModel`` route, and separation of repository location from
encoded bytes at calculation, retained-correlation, and verification boundaries.

Runtime and scientific boundary
-------------------------------
The tests perform bounded local reads of compact maintained files and inspect typed
Python structure. They do not decode campaign payloads, authenticate parent results,
construct either numerical route, reconcile operators, invoke a calculator, or run
retained correlation or verification.

Scientific exclusions
---------------------
A pass establishes retained content identity and software ownership only. It does not
establish execution provenance, route compatibility outside the retained case,
scientific validation, transferability, uncertainty quantification, or acceptance.
"""

import hashlib
import inspect
from dataclasses import fields
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign.reconciliation import (
    route as route_reconciliation_package,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route import (
    RouteReconciliationEncodedDocuments as PublicEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route import (
    campaign as campaign_module,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route import (
    encoded_documents as encoded_documents_module,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route import (
    verification as verification_module,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route.workflow import (
    RouteReconciliationProvenance,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = encoded_documents_module.RouteReconciliationEncodedDocuments
CAMPAIGN = campaign_module.RouteReconciliationCampaign
CALCULATION_REQUEST = campaign_module.RouteReconciliationCalculationRequest
CORRELATION_REQUEST = campaign_module.RouteReconciliationRetainedCorrelationRequest
VERIFICATION_REQUEST = verification_module.RouteReconciliationVerificationRequest


class TestRouteReconciliationEncodedDocumentArtifacts:
    """Own row-044 retained-file, route, and location-split evidence."""

    repository_root = Path(__file__).resolve().parents[8]
    artifact_directory = repository_root / (
        "calculations/research-monograph/impurity-defect-1d-independent-route"
    )
    input_digest = "aa7bd0750556bca3199678877f9ca2cd340f6c6b02885d6019c56173e912953f"
    result_digest = "861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc"

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes]:
        """Read the two maintained row-044 payloads as exact bytes."""
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
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-044-ARTIFACT-001.

        Requirement: The renamed owner preserves exact maintained input/result objects
        and both reviewed SHA-256 content identities.

        Acceptance: Supplied object identities, computed digests, and checksum-catalog
        entries all agree exactly.
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
        assert catalog["input.json"] == self.input_digest
        assert catalog["result.json"] == self.result_digest

    def test_operations__reject_input_bytes_outside_declared_provenance(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-044-INPUT-001.

        Requirement: Calculation and verification must bind exact encapsulated input
        bytes to provenance before decoding route contracts.

        Method: Change only the encoded energy unit while retaining the original result
        and original input provenance identity.

        Oracle: The reviewed retained-input SHA-256 identity.

        Acceptance: Both paths reject the mismatch before route construction or
        independent numerical reconstruction.

        Interpretation: A pass prevents unauthenticated input metadata from relabeling
        authenticated finite sources.

        Limitations: This samples one mutation and establishes neither transitive
        provenance nor scientific validity.
        """
        input_document, result_document = self._retained_payloads()
        altered = input_document.replace(
            b'"energy_unit": "E_G"', b'"energy_unit": "forged-unit"', 1
        )
        if altered == input_document:
            raise ValueError("test mutation target was absent")
        campaign = CAMPAIGN(SUT(altered, result_document))

        with pytest.raises(ValueError, match="encapsulated input sha256"):
            campaign.verify_retained(self.repository_root)
        with pytest.raises(ValueError, match="encapsulated input sha256 mismatch"):
            campaign.calculate(
                repository_root=self.repository_root,
                input_path=(
                    "calculations/research-monograph/"
                    "impurity-defect-1d-independent-route/input.json"
                ),
                input_sha256=self.input_digest,
                script_path="unused-runner.py",
                script_sha256="b" * 64,
                python_version="test-python",
                numpy_version="test-numpy",
            )

    def test_routes_and_operation_requests__preserve_location_split(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-044-ROUTE-001.

        Requirement: Encoded documents exclude location while calculation,
        retained-correlation, and verification requests own explicit absolute roots.

        Acceptance: Request fields are exact, nonexistent absolute roots cause no
        construction-time access, relative roots fail before payload decoding, the
        curated facade is narrow, and the retired aggregate route is absent.
        """
        assert PublicEncodedDocuments is SUT
        assert route_reconciliation_package.RouteReconciliationEncodedDocuments is SUT
        assert route_reconciliation_package.__all__ == [
            "RouteReconciliationCampaign",
            "RouteReconciliationCampaignResultDocument",
            "RouteReconciliationEncodedDocuments",
        ]
        assert [field.name for field in fields(SUT)] == [
            "input_document",
            "retained_result_document",
        ]
        assert [field.name for field in fields(CALCULATION_REQUEST)] == [
            "encoded_documents",
            "repository_root",
            "provenance",
        ]
        assert [field.name for field in fields(CORRELATION_REQUEST)] == [
            "encoded_documents",
            "repository_root",
        ]
        assert [field.name for field in fields(VERIFICATION_REQUEST)] == [
            "encoded_documents",
            "repository_root",
        ]
        assert "repository_root" in inspect.signature(CAMPAIGN.calculate).parameters
        assert list(inspect.signature(CAMPAIGN.correlate_retained).parameters) == [
            "self",
            "repository_root",
        ]

        documents = SUT(b"synthetic input", b"synthetic result")
        campaign = CAMPAIGN(documents)
        absent_absolute_root = tmp_path / "absent-repository-root"
        assert not absent_absolute_root.exists()
        provenance = RouteReconciliationProvenance(
            input_path="input.json",
            input_sha256="a" * 64,
            script_path="runner.py",
            script_sha256="b" * 64,
            python_version="test-python",
            numpy_version="test-numpy",
        )
        assert (
            CALCULATION_REQUEST(
                documents, absent_absolute_root, provenance
            ).repository_root
            is absent_absolute_root
        )
        assert (
            CORRELATION_REQUEST(documents, absent_absolute_root).repository_root
            is absent_absolute_root
        )
        assert (
            VERIFICATION_REQUEST(documents, absent_absolute_root).repository_root
            is absent_absolute_root
        )

        for request_type, arguments in (
            (CALCULATION_REQUEST, (documents, Path("relative-root"), provenance)),
            (CORRELATION_REQUEST, (documents, Path("relative-root"))),
            (VERIFICATION_REQUEST, (documents, Path("relative-root"))),
        ):
            with pytest.raises(ValueError, match="repository_root must be absolute"):
                request_type(*arguments)
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.correlate_retained(Path("relative-root"))
        with pytest.raises(TypeError, match="repository_root must be pathlib.Path"):
            campaign.correlate_retained("relative-root")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.calculate(
                repository_root=Path("relative-root"),
                input_path="input.json",
                input_sha256="a" * 64,
                script_path="runner.py",
                script_sha256="b" * 64,
                python_version="test-python",
                numpy_version="test-numpy",
            )
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.verify_retained(Path("relative-root"))

        retired_name = "RouteReconciliationCampaignModel"
        assert not hasattr(route_reconciliation_package, retired_name)
        retired_package = self.repository_root / (
            "python/src/ksdft2effmass/campaigns/periodic_1d/defects/"
            "route_reconciliation"
        )
        assert not retired_package.exists()
