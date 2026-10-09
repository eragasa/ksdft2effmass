r"""Routine intrinsic evidence for row-055 exact encoded documents.

Evidence profile: routine

These synthetic tests establish exact immutable byte ownership only. They do not
authenticate retained files or establish optimizer or scientific validity.
"""

from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import standalone

pytestmark = pytest.mark.software_verification


class TestPeriodic2DOptimizerStandaloneEncodedDocuments:
    """Own intrinsic encoded-document evidence for crosswalk row 055."""

    def test_constructor__retains_exact_nonempty_bytes_immutably(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-DATA-001.

        Requirement: The DataObject owns three exact nonempty wires without parsing or
        assigning scientific meaning.

        Acceptance: Exact byte identities are retained and fields cannot be reassigned.
        """
        proposal = b'{"proposal": 1}'
        gauges = b'{"gauges": 1}'
        result = b'{"result": 1}'

        documents = standalone.Periodic2DOptimizerStandaloneEncodedDocuments(
            proposal, gauges, result
        )

        assert documents.proposal_payload is proposal
        assert documents.initial_gauges_payload is gauges
        assert documents.result_payload is result
        with pytest.raises(FrozenInstanceError):
            documents.result_payload = b"changed"  # type: ignore[misc]

    @pytest.mark.parametrize("index", range(3))
    def test_constructor__rejects_empty_or_nonbyte_payloads(self, index: int) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-DATA-002.

        Requirement: No payload may be empty or implicitly coerced into bytes.

        Acceptance: Empty bytes raise ``ValueError`` and bytearray raises ``TypeError``
        at every field position.
        """
        valid: list[bytes | bytearray] = [b"proposal", b"gauges", b"result"]
        empty = list(valid)
        empty[index] = b""
        empty_args = cast(tuple[bytes, bytes, bytes], tuple(empty))
        with pytest.raises(ValueError, match="must be nonempty"):
            standalone.Periodic2DOptimizerStandaloneEncodedDocuments(*empty_args)
        wrong = list(valid)
        wrong[index] = bytearray(b"mutable")
        wrong_args = cast(tuple[bytes, bytes, bytes], tuple(wrong))
        with pytest.raises(TypeError, match="must be exact bytes"):
            standalone.Periodic2DOptimizerStandaloneEncodedDocuments(*wrong_args)
