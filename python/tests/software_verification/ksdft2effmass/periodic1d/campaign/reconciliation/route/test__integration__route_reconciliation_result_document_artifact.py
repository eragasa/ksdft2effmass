r"""Artifact-owned row-057 evidence for the route-reconciliation result document.

Evidence profile: claim_bearing

The test binds compact maintained bytes to their checksum-catalog content identity and
reviews the leaf-package facade. It does not decode the result, authenticate transitive
sources or execution, align state spaces, establish route compatibility, validate
science, quantify uncertainty, or record acceptance.
"""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns import periodic_1d
from ksdft2effmass.campaigns.periodic_1d import defects
from ksdft2effmass.periodic1d.campaign.reconciliation import (
    route as route_reconciliation,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route.encoded_documents import (  # noqa: E501
    RouteReconciliationEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route.result_documents import (  # noqa: E501
    RouteReconciliationCampaignResultDocument,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = RouteReconciliationCampaignResultDocument
_RESULT_SHA256 = "861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc"


class TestRouteReconciliationResultDocumentArtifact:
    """Own retained route-reconciliation evidence for crosswalk row 057."""

    def test_retained_result__preserves_bytes_catalog_identity_and_route(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-ROW-057-ROUTE-ARTIFACT-001.

        Requirement: The result-document owner must preserve the exact retained result,
        bind its reviewed checksum identity, compose with the paired encoded owner, and
        remain available through its leaf campaign facade.

        Method: Read compact maintained input/result bytes and ``SHA256SUMS``, construct
        both byte owners, hash the result independently, and inspect facade identity.

        Oracle: The reviewed digest literal and maintained checksum-catalog entry.

        Acceptance: Both owners retain the same result byte object; computed, property,
        reviewed, and catalog identities agree; the leaf facade exposes the defining
        class while broader facades do not.

        Interpretation: A pass establishes byte/content and public-route preservation.

        Limitations: Content and route identity do not establish state-space alignment,
        compatibility, provenance, scientific validation, UQ, or acceptance.
        """
        repository_root = Path(__file__).resolve().parents[8]
        retained = repository_root / (
            "calculations/research-monograph/impurity-defect-1d-independent-route"
        )
        input_payload = retained.joinpath("input.json").read_bytes()
        result_payload = retained.joinpath("result.json").read_bytes()
        catalog: dict[str, str] = {}
        for line in (
            retained.joinpath("SHA256SUMS").read_text(encoding="utf-8").splitlines()
        ):
            if not line:
                continue
            digest, logical_name = line.split(maxsplit=1)
            if logical_name in catalog:
                raise ValueError(f"duplicate checksum-catalog name: {logical_name}")
            catalog[logical_name] = digest
        encoded = RouteReconciliationEncodedDocuments(input_payload, result_payload)

        document = SUT(encoded.retained_result_document)
        digest = hashlib.sha256(document.payload).hexdigest()

        assert document.payload is result_payload
        assert document.payload is encoded.retained_result_document
        assert document.sha256 == digest == _RESULT_SHA256
        assert catalog["result.json"] == _RESULT_SHA256
        assert route_reconciliation.RouteReconciliationCampaignResultDocument is SUT
        assert not hasattr(defects, SUT.__name__)
        assert not hasattr(periodic_1d, SUT.__name__)
