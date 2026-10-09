r"""Routine verification of periodic-2D composite encoded documents.

Evidence profile: routine

Synthetic intrinsic tests establish exact byte ownership, field order, immutability,
and failure behavior. They do not decode campaign content, identify retained band
groups or frames, authenticate provenance, reproduce a numerical result, establish
convergence, quantify uncertainty, or record acceptance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.periodic2d.run.composite import (
    Periodic2DCompositeEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DCompositeEncodedDocuments


class TestPeriodic2DCompositeEncodedDocuments:
    """Own routine intrinsic evidence for crosswalk row 047."""

    def test_contract__owns_exact_ordered_payload_fields(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-047-001.

        Requirement: The renamed DataObject owns only exact encoded composite input and
        result documents under its periodic-2D run implementation.

        Acceptance: Field order, defining module, and exact byte identity agree without
        decoding or copying the supplied synthetic bytes.
        """
        input_payload = b'{"synthetic":"composite-input"}\n'
        result_payload = b'{"synthetic":"composite-result"}\n'

        documents = SUT(input_payload, result_payload)

        assert [field.name for field in fields(SUT)] == [
            "input_payload",
            "result_payload",
        ]
        assert SUT.__module__ == (
            "ksdft2effmass.periodic2d.run.composite.encoded_documents"
        )
        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload

    def test_construction__rejects_wrong_and_empty_payloads(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-047-002.

        Requirement: Encoded documents fail closed for nonexact or empty byte values.

        Acceptance: Strings, byte subclasses, and empty input or result payloads are
        rejected with the documented exception categories.
        """

        class BytesSubclass(bytes):
            """Provide a byte subtype outside the exact representation contract."""

        with pytest.raises(TypeError, match="input_payload must be exact bytes"):
            SUT("{}", b"{}")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="input_payload must be exact bytes"):
            SUT(BytesSubclass(b"{}"), b"{}")
        with pytest.raises(TypeError, match="result_payload must be exact bytes"):
            SUT(b"{}", BytesSubclass(b"{}"))
        with pytest.raises(ValueError, match="input_payload must be nonempty"):
            SUT(b"", b"{}")
        with pytest.raises(ValueError, match="result_payload must be nonempty"):
            SUT(b"{}", b"")

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-047-003.

        Requirement: Maintained encoded-document state is operationally immutable.

        Acceptance: Declared fields cannot be reassigned and undeclared instance state
        cannot be installed.
        """
        documents = SUT(b"input", b"result")

        with pytest.raises(FrozenInstanceError):
            documents.result_payload = b"changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            documents.repository_root = "/tmp"  # type: ignore[attr-defined]
