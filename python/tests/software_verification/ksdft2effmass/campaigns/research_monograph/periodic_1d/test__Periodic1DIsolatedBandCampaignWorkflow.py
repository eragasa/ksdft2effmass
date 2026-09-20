r"""Software verification of ``Periodic1DIsolatedBandCampaignWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: read-only Appendix G isolated input/result correlation.

Facet and represented meaning

The Workflow binds typed controls, typed outcomes, and retained source identities.

Intrinsic and cross-object scope

Discretization, low-mode, weak-gap, mesh, hopping, convention, and SHA correlations
are included.

VVUQ and scientific exclusions

The Workflow performs no calculation and establishes no scientific validation or UQ.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DIsolatedBandCampaignWorkflow,
    Periodic1DIsolatedBandCampaignWorkflowRequest,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedBandCampaignWorkflow


class TestPeriodic1DIsolatedBandCampaignWorkflow:
    """Own retained-wire integration evidence for the isolated campaign."""

    def test_method__execute__correlates_complete_available_campaign(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-012

        Requirement: The public Workflow integrates the isolated definition and typed
        result only when every represented inventory and source identity agrees.

        Method: Execute the read-only Workflow over retained input and result bytes.

        Oracle: Independent retained SHA-256 identities and exact input inventories.

        Acceptance: Both identities, seven hopping studies, and 64 complete hopping
        representatives agree after correlation.

        Interpretation: A pass establishes retained isolated campaign integration.

        Limitations: No calculation, scientific validation, or UQ is performed.

        Provenance: Retained Appendix G isolated input and result artifacts.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"

        result = SUT().execute(
            Periodic1DIsolatedBandCampaignWorkflowRequest(
                (directory / "input.json").read_bytes(),
                (directory / "result.json").read_bytes(),
            )
        )

        assert (
            result.input_sha256
            == "ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb"
        )
        assert (
            result.result_sha256
            == "37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c"
        )
        assert len(result.campaign_result.reduction.hopping_range_study) == 7
        assert len(result.campaign_result.reduction.hopping_model.representatives) == 64
