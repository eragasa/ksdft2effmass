r"""Routine verification of balanced Wannier90 encoded documents.

Evidence profile: routine

Synthetic intrinsic tests establish exact result-byte ownership, field order,
immutability, and failure behavior. They do not imply an input document or native-file
presence, decode observations, reconstruct execution provenance, establish localization
convergence, qualify a numerical oracle, quantify uncertainty, or record acceptance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.periodic2d.run.wannier90.balanced import (
    Periodic2DWannier90BalancedEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DWannier90BalancedEncodedDocuments


class TestPeriodic2DWannier90BalancedEncodedDocuments:
    """Own routine intrinsic evidence for crosswalk row 050."""

    def test_contract__owns_one_exact_result_payload(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-050-001.

        Requirement: The renamed DataObject owns only the exact encoded balanced
        Wannier90 result document under its periodic-2D run implementation.

        Acceptance: Field order, defining module, and exact byte identity agree without
        decoding or copying the supplied synthetic bytes; no input field is introduced.
        """
        result_payload = b'{"synthetic":"balanced-wannier90-result"}\n'

        documents = SUT(result_payload)

        assert [field.name for field in fields(SUT)] == ["result_payload"]
        assert SUT.__module__ == (
            "ksdft2effmass.periodic2d.run.wannier90.balanced.encoded_documents"
        )
        # Identity proves that construction neither normalizes nor copies the wire.
        assert documents.result_payload is result_payload
        assert not hasattr(documents, "input_payload")

    def test_construction__rejects_wrong_and_empty_payloads(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-050-002.

        Requirement: The result document fails closed for nonexact or empty byte values.

        Acceptance: A string, a byte subclass, and empty exact bytes are rejected with
        the documented exception categories.
        """

        class BytesSubclass(bytes):
            """Provide a byte subtype outside the exact representation contract."""

        with pytest.raises(TypeError, match="result_payload must be exact bytes"):
            SUT("{}")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="result_payload must be exact bytes"):
            SUT(BytesSubclass(b"{}"))
        with pytest.raises(ValueError, match="result_payload must be nonempty"):
            SUT(b"")

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-050-003.

        Requirement: Maintained encoded-document state is operationally immutable.

        Acceptance: The declared field cannot be reassigned and undeclared native-file
        state cannot be installed.
        """
        documents = SUT(b"result")

        with pytest.raises(FrozenInstanceError):
            documents.result_payload = b"changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            documents.native_seedname = "run"  # type: ignore[attr-defined]
