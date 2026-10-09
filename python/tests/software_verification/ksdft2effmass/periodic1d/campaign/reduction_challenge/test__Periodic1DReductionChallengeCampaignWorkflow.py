r"""Software verification of ``Periodic1DReductionChallengeCampaignWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: read-only Appendix G stress input/result correlation.

Facet and represented meaning

The Workflow binds typed controls, every stress result channel, and source identities.

Intrinsic and cross-object scope

Inventory, route, shape, discretization, experiment, and SHA correlations are included.

VVUQ and scientific exclusions

The Workflow performs no calculation and establishes no scientific validation or UQ.
"""

from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign.reduction_challenge import (
    Periodic1DReductionChallengeCampaignWorkflow,
    Periodic1DReductionChallengeCampaignWorkflowRequest,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DReductionChallengeCampaignWorkflow


class TestPeriodic1DReductionChallengeCampaignWorkflow:
    """Own retained-wire integration evidence for the reduction challenge."""

    def test_method__execute__correlates_complete_typed_campaign(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-011

        Requirement: The public Workflow integrates stress definitions and typed
        outcomes only when every demonstrated inventory and route control agrees.

        Method: Execute the read-only Workflow over retained input and result bytes.

        Oracle: Independent retained SHA-256 identities and exact campaign controls.

        Acceptance: Both identities agree and the correlated result retains 210
        mesh/band/isolation cases with route mesh 64.

        Interpretation: A pass establishes retained campaign integration compatibility.

        Limitations: No stress calculation, scientific validation, or UQ is performed.

        Provenance: Retained Appendix G stress input and result artifacts.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"

        result = SUT().execute(
            Periodic1DReductionChallengeCampaignWorkflowRequest(
                (directory / "stress-input.json").read_bytes(),
                (directory / "stress-result.json").read_bytes(),
            )
        )

        assert (
            result.input_sha256
            == "3be86c6ee7cb08c1c194aa97e856c89458907c23428bed19f6b38cdb437d987a"
        )
        assert (
            result.result_sha256
            == "5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394"
        )
        assert len(result.campaign_result.mesh_band_isolation) == 210
        assert result.campaign_result.route_assumptions.mesh_size == 64

    def test_method__execute__rejects_changed_input_content_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-004.

        Requirement: Correlation authenticates the exact supplied input bytes against
        the digest declared by the retained result before using input-owned controls.

        Method: Replace the input with malformed, schema-invalid bytes while preserving
        the original result bytes.

        Oracle: The result's declared ``provenance.input_sha256``.

        Acceptance: Correlation raises the input SHA-256 authentication error before
        attempting input decoding.

        Interpretation: A pass establishes authentication before any use or validation
        of input-owned controls.

        Limitations: SHA-256 identity does not prove authorship or historical execution.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        changed_input = b"not valid JSON"

        with pytest.raises(ValueError, match="input SHA-256"):
            SUT().execute(
                Periodic1DReductionChallengeCampaignWorkflowRequest(
                    changed_input,
                    (directory / "stress-result.json").read_bytes(),
                )
            )
