r"""Software verification of ``Periodic1DIsolatedVerifiedWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: integrated Appendix G isolated correlation and verification.

Facet and represented meaning

The Workflow preserves separate correlation and independent numerical-verification
ResultObjects behind one supported orchestration surface.

Intrinsic and cross-object scope

Retained bytes are correlated before verification, with explicit ordinary and
curvature tolerances.

VVUQ and scientific exclusions

Composition success does not establish material validation, polarization, UQ, or
human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DIsolatedBandCampaignWorkflowRequest,
    Periodic1DIsolatedUnavailableVerificationChannel,
    Periodic1DIsolatedVerifiedWorkflow,
    Periodic1DIsolatedVerifiedWorkflowRequest,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedVerifiedWorkflow


class TestPeriodic1DIsolatedVerifiedWorkflow:
    """Own integrated isolated correlation and verification evidence."""

    def test_method__execute__preserves_correlation_and_verification(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-022

        Requirement: The integrated isolated Workflow correlates retained bytes before
        numerical verification and preserves both complete outcomes.

        Method: Execute the public Workflow over immutable Appendix G bytes with
        explicit ordinary and curvature tolerances.

        Oracle: Exact input/result SHA-256 identities and the independent verifier's
        explicit disposition and unavailable-channel inventory.

        Acceptance: Both identities agree, verification passes, and unavailable frame
        and localization channels remain explicit.

        Interpretation: A pass establishes correct supported orchestration.

        Limitations: Numerical correctness belongs to separate numerical evidence;
        unavailable and scientific channels are not accepted.

        Provenance: Appendix G ``input.json`` and ``result.json``.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        result = SUT().execute(
            Periodic1DIsolatedVerifiedWorkflowRequest(
                Periodic1DIsolatedBandCampaignWorkflowRequest(
                    (directory / "input.json").read_bytes(),
                    (directory / "result.json").read_bytes(),
                ),
                ScalarQuantity(1.0e-10, Unitless()),
                ScalarQuantity(1.0e-7, Unitless()),
            )
        )

        assert result.passes
        assert result.campaign_result.input_sha256 == (
            "ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb"
        )
        assert result.campaign_result.result_sha256 == (
            "37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c"
        )
        assert (
            Periodic1DIsolatedUnavailableVerificationChannel.WANNIER_LOCALIZATION_PROFILE
            in result.isolated_verification.unavailable_channels
        )
