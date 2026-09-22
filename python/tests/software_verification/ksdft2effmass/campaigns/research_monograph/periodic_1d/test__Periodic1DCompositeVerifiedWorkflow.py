r"""Software verification of ``Periodic1DCompositeVerifiedWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: integrated retained Appendix G composite correlation and
independent numerical-verification composition.

Facet and represented meaning

The Workflow preserves the complete correlation ResultObject and the independent
composite-verification ResultObject in one supported orchestration result.

Intrinsic and cross-object scope

Input/result identities and controls are correlated before numerical verification;
ordered group inventories remain equal across both nested results.

VVUQ and scientific exclusions

This composition evidence does not reproduce the calculation, convert unavailable
channels into passes, establish material validity, or perform uncertainty
quantification.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeCampaignWorkflowRequest,
    Periodic1DCompositeUnavailableVerificationChannel,
    Periodic1DCompositeVerifiedWorkflow,
    Periodic1DCompositeVerifiedWorkflowRequest,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeVerifiedWorkflow


class TestPeriodic1DCompositeVerifiedWorkflow:
    """Own integrated composite correlation and verification evidence."""

    def test_method__execute__preserves_correlation_and_verification(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-021

        Requirement: The supported integrated Workflow correlates retained bytes
        before verification and returns both complete ResultObjects with one bounded
        aggregate disposition.

        Method: Execute the Workflow over the immutable Appendix G composite input and
        result bytes with an explicit ``1e-11 E_G`` tolerance.

        Oracle: Exact retained wire identities, ordered group inventories, and the
        independent verifier's explicit unavailable-channel contract.

        Acceptance: Both nested results are retained, input/result SHA-256 values and
        group order agree, verification passes, and unavailable channels remain listed.

        Interpretation: A pass establishes correct one-call orchestration without
        conflating retained correlation and numerical verification.

        Limitations: Numerical correctness belongs to separate numerical evidence; no
        missing source channel, scientific validation, or UQ is accepted here.

        Provenance: Appendix G ``composite-input.json`` and ``composite-result.json``.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        request = Periodic1DCompositeVerifiedWorkflowRequest(
            Periodic1DCompositeCampaignWorkflowRequest(
                (directory / "composite-input.json").read_bytes(),
                (directory / "composite-result.json").read_bytes(),
            ),
            ScalarQuantity(1.0e-11, Unitless()),
        )

        result = SUT().execute(request)

        assert result.passes
        assert result.campaign_result.input_sha256 == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert result.campaign_result.result_sha256 == (
            "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f"
        )
        low_campaign, high_campaign = result.campaign_result.campaign_result.groups
        low_verified, high_verified = result.composite_verification.groups
        assert (low_campaign.group_id, high_campaign.group_id) == (
            "low_pair",
            "higher_pair",
        )
        assert (low_verified.group_id, high_verified.group_id) == (
            "low_pair",
            "higher_pair",
        )
        assert (
            Periodic1DCompositeUnavailableVerificationChannel.WITHHELD_RANGE_ERRORS
            in result.composite_verification.unavailable_channels
        )
