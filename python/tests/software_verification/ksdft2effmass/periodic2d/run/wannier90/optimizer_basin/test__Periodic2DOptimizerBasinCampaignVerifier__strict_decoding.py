r"""Strict-wire verification for the portable optimizer-basin verifier.

Evidence profile: routine

These synthetic malformed-wire tests establish that verification fails before campaign
fields from ambiguous or nonstandard JSON can affect a disposition. They do not verify
retained numerical observations, native execution, optimizer convergence, scientific
validity, uncertainty quantification, or acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    Periodic2DOptimizerBasinEncodedDocuments,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.verify import (
    Periodic2DOptimizerBasinCampaignVerificationRequest,
    Periodic2DOptimizerBasinCampaignVerifier,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DOptimizerBasinCampaignVerifier


class TestPeriodic2DOptimizerBasinCampaignVerifierStrictDecoding:
    """Own strict-wire evidence for the row-052 portable verifier."""

    @staticmethod
    def request(
        input_payload: bytes,
        result_payload: bytes = b'{"schema_version":1}',
    ) -> Periodic2DOptimizerBasinCampaignVerificationRequest:
        """Return a request whose malformed input fails before repository access."""
        return Periodic2DOptimizerBasinCampaignVerificationRequest(
            Periodic2DOptimizerBasinEncodedDocuments(input_payload, result_payload),
            Path(__file__).resolve().parents[8],
        )

    @pytest.mark.parametrize(
        ("payload", "exception", "message"),
        [
            (
                b'{"schema_version":1,"schema_version":1}',
                ValueError,
                "duplicate JSON key",
            ),
            (
                b'{"schema_version":NaN}',
                ValueError,
                "non-finite JSON constant",
            ),
            (b'{"schema_version":"\xff"}', ValueError, "valid strict UTF-8 JSON"),
            (b"[]", TypeError, "root must be a JSON object"),
        ],
    )
    def test_execute__rejects_ambiguous_or_nonstandard_input_wires(
        self,
        payload: bytes,
        exception: type[Exception],
        message: str,
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-STRICT-001.

        Requirement: Claim-bearing verification must consume strict, duplicate-free,
        finite UTF-8 JSON objects through the shared decoder.

        Acceptance: Duplicate keys, nonstandard nonfinite constants, invalid UTF-8, and
        a non-object root fail with the shared decoder's documented exception category
        before repository correlation or disposition reconstruction begins.
        """
        with pytest.raises(exception, match=message):
            SUT().execute(self.request(payload))
