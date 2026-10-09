r"""Routine evidence for route-reconciliation encoded result ownership.

Evidence profile: routine

Synthetic bytes establish intrinsic representation, content identity, immutability,
and failure behavior only. They do not decode a result, authenticate an artifact, align
state spaces, establish route compatibility, validate science, quantify uncertainty, or
record acceptance.
"""

from dataclasses import FrozenInstanceError, fields
from typing import cast

import pytest

from ksdft2effmass.periodic1d.campaign.reconciliation.route.result_documents import (  # noqa: E501
    RouteReconciliationCampaignResultDocument,
)

pytestmark = pytest.mark.software_verification
SUT = RouteReconciliationCampaignResultDocument


class TestRouteReconciliationCampaignResultDocument:
    """Own routine intrinsic route-reconciliation evidence for row 057."""

    def test_contract__retains_exact_bytes_and_derives_content_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-ROW-057-ROUTE-001.

        Requirement: The result-document owner retains one exact byte field and derives
        SHA-256 without decoding or canonical re-encoding.

        Acceptance: Field/module identity, byte-object identity, and a fixed synthetic
        digest agree with the documented contract.
        """
        payload = b"result"

        document = SUT(payload)

        assert [field.name for field in fields(SUT)] == ["payload"]
        assert SUT.__module__ == (
            "ksdft2effmass.periodic1d.campaign.reconciliation.route.result_documents"
        )
        assert document.payload is payload
        assert document.sha256 == (
            "f6a214f7a5fcda0c2cee9660b7fc29f5649e3c68aad48e20e950137c98913a68"
        )

    def test_construction__rejects_nonexact_and_empty_payloads(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-ROW-057-ROUTE-002.

        Requirement: Result bytes reject implicit coercion, subclasses, and emptiness.

        Acceptance: A string, byte subclass, and empty exact bytes raise the documented
        exception categories.
        """

        class BytesSubclass(bytes):
            """Provide a byte subtype outside the exact representation contract."""

        with pytest.raises(TypeError, match="payload must be exact built-in bytes"):
            SUT(cast(bytes, "result"))
        with pytest.raises(TypeError, match="payload must be exact built-in bytes"):
            SUT(BytesSubclass(b"result"))
        with pytest.raises(ValueError, match="payload must be nonempty"):
            SUT(b"")

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-ROW-057-ROUTE-003.

        Requirement: Maintained result-document state is operationally immutable.

        Acceptance: Field reassignment and undeclared state installation both fail.
        """
        document = SUT(b"result")

        with pytest.raises(FrozenInstanceError):
            document.payload = b"changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            document.route_identity = "forged"  # type: ignore[attr-defined]
