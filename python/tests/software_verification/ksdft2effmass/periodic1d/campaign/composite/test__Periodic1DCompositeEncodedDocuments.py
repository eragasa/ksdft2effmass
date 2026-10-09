r"""Class-owned software verification of composite encoded documents.

Evidence profile: routine

Bounded scope
-------------
The intrinsic field, representation, and immutability contract of
``Periodic1DCompositeEncodedDocuments`` using synthetic byte values only.

Scientific exclusions
---------------------
These tests perform no repository file access, decode no campaign document, and make no
claim about retained artifacts, provenance, retained groups, frames, operators,
scientific validity, uncertainty quantification, or acceptance. Retained-file and
supported-route evidence is owned by a separate integration module.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.periodic1d.campaign.composite import (
    Periodic1DCompositeEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeEncodedDocuments


class TestPeriodic1DCompositeEncodedDocuments:
    """Own intrinsic row-038 DataObject contract evidence."""

    def test_contract__owns_exact_fields_and_preserves_synthetic_bytes(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-038-001.

        Requirement: The DataObject owns exactly two ordered built-in-byte fields and
        stores supplied byte objects without conversion or copying.

        Method: Inspect dataclass fields and construct the class with two distinct
        synthetic byte objects.

        Oracle: The documented field inventory and Python object identity.

        Acceptance: Names, order, types, defining module, and retained object identities
        match exactly.

        Interpretation: A pass establishes the intrinsic encoded-container contract.

        Limitations: Synthetic nonempty bytes do not establish valid JSON, retained
        artifact identity, decoded semantics, or source provenance.
        """
        input_payload = b"synthetic composite input"
        result_payload = b"synthetic composite result"
        documents = SUT(input_payload, result_payload)

        assert SUT.__module__ == (
            "ksdft2effmass.periodic1d.campaign.composite.encoded_documents"
        )
        assert [(field.name, field.type) for field in fields(SUT)] == [
            ("input_payload", bytes),
            ("result_payload", bytes),
        ]
        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload

    def test_construction__rejects_wrong_and_empty_payload_representations(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-038-002.

        Requirement: Both fields accept only nonempty exact built-in ``bytes``.

        Method: Exercise wrong types, ``bytes`` subclasses, and empty values at each
        constructor position.

        Oracle: The documented representation contract and exception taxonomy.

        Acceptance: Wrong representations raise ``TypeError`` and empty exact-byte
        representations raise ``ValueError`` without coercion.

        Interpretation: A pass establishes fail-closed intrinsic validation.

        Limitations: Nonempty bytes are not thereby valid JSON or a supported schema.
        """

        class BytesSubclass(bytes):
            """Provide a bytes subtype that violates the exact contract."""

        for input_payload, result_payload, exception, match in (
            ("{}", b"{}", TypeError, "input_payload must be built-in bytes"),
            (BytesSubclass(b"{}"), b"{}", TypeError, "input_payload must be"),
            (b"", b"{}", ValueError, "input_payload must be nonempty"),
            (b"{}", "{}", TypeError, "result_payload must be built-in bytes"),
            (b"{}", BytesSubclass(b"{}"), TypeError, "result_payload must be"),
            (b"{}", b"", ValueError, "result_payload must be nonempty"),
        ):
            with pytest.raises(exception, match=match):
                SUT(input_payload, result_payload)  # type: ignore[arg-type]

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-038-003.

        Requirement: Constructed encoded documents are operationally immutable and
        cannot acquire undeclared state.

        Method: Attempt to replace an owned field and add a dynamic attribute.

        Oracle: Frozen and slotted dataclass semantics.

        Acceptance: Both mutations fail without changing the object.

        Interpretation: A pass establishes the immutable container facet.

        Limitations: Immutability does not authenticate the supplied bytes.
        """
        documents = SUT(b"input", b"result")

        with pytest.raises(FrozenInstanceError):
            documents.input_payload = b"changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            documents.extra = b"forbidden"  # type: ignore[attr-defined]
