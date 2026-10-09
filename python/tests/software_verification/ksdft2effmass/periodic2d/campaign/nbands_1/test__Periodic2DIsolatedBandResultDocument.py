r"""Routine evidence for isolated-band encoded result-document ownership.

Evidence profile: routine

Synthetic bytes establish intrinsic representation, content-identity, immutability, and
failure behavior only. They do not decode a result, authenticate an artifact, prove a
calculation occurred, establish convergence, validate science, quantify uncertainty, or
record acceptance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.periodic2d.campaign.nbands_1.result_documents import (
    Periodic2DIsolatedBandResultDocument,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DIsolatedBandResultDocument


class TestPeriodic2DIsolatedBandResultDocument:
    """Own routine intrinsic evidence for crosswalk row 056."""

    def test_contract__retains_exact_bytes_and_derives_content_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-056-001.

        Requirement: The encoded result-document owner retains one exact byte field and
        derives SHA-256 from those bytes without decoding or canonical re-encoding.

        Acceptance: The field and defining module are exact, byte-object identity is
        preserved, and the digest equals an independently fixed synthetic identity.
        """
        payload = b"result"

        document = SUT(payload)

        assert [field.name for field in fields(SUT)] == ["payload"]
        assert SUT.__module__ == (
            "ksdft2effmass.periodic2d.campaign.nbands_1.result_documents"
        )
        assert document.payload is payload
        assert document.sha256 == (
            "f6a214f7a5fcda0c2cee9660b7fc29f5649e3c68aad48e20e950137c98913a68"
        )

    def test_construction__rejects_nonexact_and_empty_payloads(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-056-002.

        Requirement: Public encoded-byte ownership rejects implicit representation
        coercion and empty documents.

        Acceptance: A string, byte subclass, and empty exact bytes raise the documented
        exception categories.
        """

        class BytesSubclass(bytes):
            """Provide a byte subtype outside the exact representation contract."""

        with pytest.raises(TypeError, match="payload must be exact built-in bytes"):
            SUT("result")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="payload must be exact built-in bytes"):
            SUT(BytesSubclass(b"result"))
        with pytest.raises(ValueError, match="payload must be nonempty"):
            SUT(b"")

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-056-003.

        Requirement: Maintained encoded result-document state is operationally
        immutable and closed to undeclared instance attributes.

        Acceptance: Field reassignment and undeclared state installation both fail.
        """
        document = SUT(b"result")

        with pytest.raises(FrozenInstanceError):
            document.payload = b"changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            document.schema_version = 1  # type: ignore[attr-defined]
