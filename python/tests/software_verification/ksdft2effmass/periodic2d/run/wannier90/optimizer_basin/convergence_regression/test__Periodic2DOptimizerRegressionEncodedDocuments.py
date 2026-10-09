r"""Routine intrinsic evidence for row-054 exact encoded documents.

Evidence profile: routine

These synthetic tests establish exact immutable byte ownership only. They do not
authenticate retained files or establish statistical or scientific validity.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    convergence_regression as regression,
)

Periodic2DOptimizerRegressionEncodedDocuments = (
    regression.Periodic2DOptimizerRegressionEncodedDocuments
)

pytestmark = pytest.mark.software_verification


class TestPeriodic2DOptimizerRegressionEncodedDocuments:
    """Own intrinsic encoded-document evidence for crosswalk row 054."""

    def test_constructor__retains_exact_nonempty_bytes_immutably(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-DATA-001.

        Requirement: The DataObject owns three exact nonempty byte strings without
        parsing or assigning scientific meaning.

        Acceptance: Exact byte identities are retained and fields cannot be reassigned.
        """
        source = b'{"source": 1}'
        analyzer = b"print('retained')\n"
        regression = b'{"regression": 1}'

        documents = Periodic2DOptimizerRegressionEncodedDocuments(
            source, analyzer, regression
        )

        assert documents.standalone_result_payload is source
        assert documents.analyzer_payload is analyzer
        assert documents.regression_payload is regression
        with pytest.raises(FrozenInstanceError):
            documents.regression_payload = b"changed"  # type: ignore[misc]

    @pytest.mark.parametrize("index", range(3))
    def test_constructor__rejects_empty_or_nonbyte_payloads(self, index: int) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-DATA-002.

        Requirement: No payload may be empty or implicitly coerced into bytes.

        Acceptance: Empty bytes raise ``ValueError`` and bytearray raises ``TypeError``
        at each field position.
        """
        valid: list[bytes | bytearray] = [b"source", b"analyzer", b"regression"]
        empty = list(valid)
        empty[index] = b""
        with pytest.raises(ValueError, match="must be nonempty"):
            Periodic2DOptimizerRegressionEncodedDocuments(*empty)  # type: ignore[arg-type]
        wrong = list(valid)
        wrong[index] = bytearray(b"mutable")
        with pytest.raises(TypeError, match="must be exact bytes"):
            Periodic2DOptimizerRegressionEncodedDocuments(*wrong)  # type: ignore[arg-type]
