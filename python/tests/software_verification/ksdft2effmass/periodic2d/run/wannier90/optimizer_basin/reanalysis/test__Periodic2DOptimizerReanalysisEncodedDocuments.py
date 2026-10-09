r"""Routine intrinsic evidence for optimizer-reanalysis encoded documents.

Evidence profile: routine

Synthetic bytes establish representation ownership only. They do not decode scientific
content, authenticate retained artifacts, replay native execution, or establish
scientific acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis import (
    Periodic2DOptimizerReanalysisEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DOptimizerReanalysisEncodedDocuments


class TestPeriodic2DOptimizerReanalysisEncodedDocuments:
    """Own intrinsic byte-container evidence for crosswalk row 053."""

    def test_contract__owns_exact_ordered_payload_fields(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-001.

        Requirement: The DataObject owns source-result bytes followed by reanalysis
        result bytes without copying, decoding, or adding repository location.

        Acceptance: Exact synthetic bytes are retained by identity in field order.
        """
        source = b'{"source":1}'
        result = b'{"result":2}'
        documents = SUT(source, result)

        assert documents.source_result_payload is source
        assert documents.result_payload is result
        assert tuple(documents.__dataclass_fields__) == (
            "source_result_payload",
            "result_payload",
        )
        assert not hasattr(documents, "repository_root")

    @pytest.mark.parametrize("field", ["source", "result"])
    def test_construction__rejects_wrong_and_empty_payloads(self, field: str) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-002.

        Requirement: Payloads are nonempty exact built-in bytes; mutable buffers,
        subclasses, strings, and empty wires fail closed.

        Acceptance: Each invalid representation raises the documented exception.
        """

        class BytesSubclass(bytes):
            """Test-only bytes subclass rejected by the exact wire contract."""

        for invalid in (bytearray(b"{}"), BytesSubclass(b"{}"), "{}"):
            values = {"source": b"{}", "result": b"{}"}
            values[field] = invalid  # type: ignore[assignment]
            with pytest.raises(TypeError, match="must be exact bytes"):
                SUT(values["source"], values["result"])
        values = {"source": b"{}", "result": b"{}"}
        values[field] = b""
        with pytest.raises(ValueError, match="must be nonempty"):
            SUT(values["source"], values["result"])

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-003.

        Requirement: Maintained document state is operationally immutable and has no
        dynamic attribute dictionary.

        Acceptance: Reassignment fails and ``__dict__`` is absent.
        """
        documents = SUT(b"source", b"result")

        with pytest.raises(FrozenInstanceError):
            documents.result_payload = b"changed"  # type: ignore[misc]
        assert not hasattr(documents, "__dict__")
