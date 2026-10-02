r"""Software verification of ``Periodic1DStressCampaign``.

Evidence profile: claim_bearing

Bounded artifact scope: reduction-challenge encoded-document encapsulation and typed
correlation and verification delegation.

VVUQ and scientific exclusions

A pass establishes façade composition only. Numerical correctness remains owned by
separate numerical evidence and does not establish material validation or UQ.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DReductionChallengeEncodedDocuments,
    Periodic1DStressCampaign,
    Periodic1DStressCampaignCorrelationResult,
    Periodic1DStressCampaignVerificationResult,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Periodic1DStressCampaign


class TestPeriodic1DStressCampaign:
    """Own stress campaign DataObject encapsulation evidence."""

    @staticmethod
    def _campaign() -> Periodic1DStressCampaign:
        root = Path(__file__).resolve().parents[6]
        directory = root / "calculations/research-monograph/periodic-1d"
        return SUT(
            Periodic1DReductionChallengeEncodedDocuments(
                (directory / "stress-input.json").read_bytes(),
                (directory / "stress-result.json").read_bytes(),
            )
        )

    def test_method__correlate__uses_distinct_correlation_action(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-029

        Requirement: Reduction-challenge document binding and validation are a
        distinct operation exposed by the encapsulating DataObject.

        Method: Correlate immutable retained reduction-challenge payloads without
        requesting numerical verification.

        Oracle: Exact correlation result type and retained payload identities.

        Acceptance: Correlation returns typed records and exact SHA-256 identities.

        Interpretation: A pass establishes separate correlation ownership.

        Limitations: Correlation alone establishes no numerical or scientific claim.
        """
        campaign = self._campaign()
        result = campaign.correlate()

        assert type(campaign).__module__.endswith("periodic_1d.run.stress.data")
        assert type(campaign.encoded_documents).__module__.endswith(
            "periodic_1d.encoded_documents"
        )
        assert type(result) is Periodic1DStressCampaignCorrelationResult
        assert result.campaign_correlation.input_sha256 == (
            "3be86c6ee7cb08c1c194aa97e856c89458907c23428bed19f6b38cdb437d987a"
        )
        assert result.campaign_correlation.result_sha256 == (
            "5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394"
        )

    def test_method__verify__delegates_documents_through_typed_request(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-030

        Requirement: The campaign delegates tolerance policy and independent
        reconstruction to its verifier.

        Method: Verify the immutable reduction-challenge documents with an explicit
        unitless tolerance.

        Oracle: Exact result type, aggregate disposition, and preserved identities.

        Acceptance: Verification passes while retaining the correlated result.

        Interpretation: A pass establishes correct typed verifier delegation.

        Limitations: Scientific validation, transferability, and UQ remain excluded.
        """
        result = self._campaign().verify(
            absolute_tolerance=ScalarQuantity(1.0e-10, Unitless())
        )

        assert type(result) is Periodic1DStressCampaignVerificationResult
        assert result.passes
        assert result.campaign_correlation.result_sha256 == (
            "5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394"
        )
