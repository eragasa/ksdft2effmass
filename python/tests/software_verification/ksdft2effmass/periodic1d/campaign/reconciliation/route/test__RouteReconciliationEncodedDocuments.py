r"""Class-owned software verification of route-reconciliation encoded documents.

Evidence profile: routine

Bounded scope
-------------
The intrinsic field, exact-byte, immutability, and repository-location-exclusion
contract of ``RouteReconciliationEncodedDocuments`` using synthetic byte values only.

Ownership and scientific exclusions
-----------------------------------
The SUT owns encoded input and retained-result documents, not repository location,
parent data, represented operators, route identities, alignment, reconciliation,
decoded results, provenance, verification, UQ, or acceptance. These tests access no
retained artifact, deserialize no JSON, and perform no source authentication or
numerical reconstruction. Retained-file and route evidence is owned separately.
"""

from dataclasses import FrozenInstanceError, fields
from typing import get_type_hints

import pytest

from ksdft2effmass.periodic1d.campaign.reconciliation.route import (
    encoded_documents as encoded_documents_module,
)

pytestmark = pytest.mark.software_verification
SUT = encoded_documents_module.RouteReconciliationEncodedDocuments


class TestRouteReconciliationEncodedDocuments:
    """Own intrinsic row-044 encoded-document contract evidence."""

    def test_contract__owns_exact_fields_without_repository_location(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-044-001.

        Requirement: The DataObject owns exactly two ordered encoded-byte fields and no
        repository root or execution state.

        Acceptance: Field names, order, types, defining owner, and supplied byte
        identities match exactly; no repository-location field exists.
        """
        input_document = b"synthetic route-reconciliation input"
        result_document = b"synthetic route-reconciliation result"
        documents = SUT(input_document, result_document)

        assert SUT.__module__ == (
            "ksdft2effmass.periodic1d.campaign.reconciliation.route.encoded_documents"
        )
        assert [field.name for field in fields(SUT)] == [
            "input_document",
            "retained_result_document",
        ]
        assert get_type_hints(SUT) == {
            "input_document": bytes,
            "retained_result_document": bytes,
        }
        assert documents.input_document is input_document
        assert documents.retained_result_document is result_document
        assert not hasattr(documents, "repository_root")

    def test_construction__rejects_wrong_and_empty_payload_representations(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-044-002.

        Requirement: Both fields accept only nonempty exact built-in ``bytes``.

        Acceptance: Wrong representations raise ``TypeError`` and empty exact-byte
        representations raise ``ValueError`` without coercion.
        """

        class BytesSubclass(bytes):
            """Provide a bytes subtype that violates the exact contract."""

        for input_document, result_document, exception, match in (
            (
                bytearray(b"{}"),
                b"{}",
                TypeError,
                "input_document must be exact bytes",
            ),
            (
                BytesSubclass(b"{}"),
                b"{}",
                TypeError,
                "input_document must be exact bytes",
            ),
            (b"", b"{}", ValueError, "input_document must be nonempty"),
            (
                b"{}",
                bytearray(b"{}"),
                TypeError,
                "retained_result_document must be exact bytes",
            ),
            (
                b"{}",
                BytesSubclass(b"{}"),
                TypeError,
                "retained_result_document must be exact bytes",
            ),
            (b"{}", b"", ValueError, "retained_result_document must be nonempty"),
        ):
            with pytest.raises(exception, match=match):
                SUT(input_document, result_document)  # type: ignore[arg-type]

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-044-003.

        Requirement: Encoded documents are operationally immutable and cannot acquire
        undeclared repository-location state.

        Acceptance: Payload replacement and repository-root injection both fail.
        """
        documents = SUT(b"input", b"result")

        with pytest.raises(FrozenInstanceError):
            documents.input_document = b"changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            documents.repository_root = "/tmp"  # type: ignore[attr-defined]
        assert documents.input_document == b"input"
        assert not hasattr(documents, "repository_root")
