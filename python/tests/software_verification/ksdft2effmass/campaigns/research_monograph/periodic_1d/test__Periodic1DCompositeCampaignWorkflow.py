r"""Software verification of ``Periodic1DCompositeCampaignWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G composite input/result correlation.

Facet and represented meaning

Band groups, mesh and range controls, typed outcomes, and source identities are
included.

Intrinsic and cross-object scope

The input definition, all typed group channels, result document, and retained
provenance are correlated.

VVUQ and scientific exclusions

The read-only Workflow performs no calculation or scientific validation.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeCampaignWorkflow,
    Periodic1DCompositeCampaignWorkflowRequest,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeCampaignWorkflow


class TestPeriodic1DCompositeCampaignWorkflow:
    """Own retained composite campaign integration evidence."""

    def test_method__execute__correlates_groups_and_source_identities(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-014

        Requirement: Composite typed results bind to their exact input controls and
        retained groups.

        Method: Execute the read-only Workflow over retained input and result bytes.

        Oracle: Independent SHA-256 identities and exact input group, mesh, hopping
        range, direct-route, and isolation-threshold controls.

        Acceptance: Both hashes and every correlated control agree for both groups.

        Interpretation: A pass establishes retained composite campaign integration.

        Limitations: No composite calculation, validation, or UQ is performed.

        Provenance: Retained Appendix G composite artifacts.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"

        result = SUT().execute(
            Periodic1DCompositeCampaignWorkflowRequest(
                (directory / "composite-input.json").read_bytes(),
                (directory / "composite-result.json").read_bytes(),
            )
        )

        assert result.input_sha256 == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert result.result_sha256 == (
            "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f"
        )
        assert len(result.campaign_result.groups) == 2
        low_pair, higher_pair = result.campaign_result.groups
        assert (
            len(low_pair.hopping_representation.smooth_reciprocal_hamiltonians.matrices)
            == 128
        )
        assert (
            len(
                higher_pair.hopping_representation.smooth_reciprocal_hamiltonians.matrices
            )
            == 128
        )
        expected_representatives = tuple(range(-64, 64))
        assert (
            low_pair.hopping_representation.smooth_hopping_model.representatives
            == expected_representatives
        )
        assert (
            higher_pair.hopping_representation.smooth_hopping_model.representatives
            == expected_representatives
        )
        assert len(low_pair.range_study) == 8
        assert low_pair.range_study[0].hopping_range_cells == 0
        assert low_pair.range_study[-1].hopping_range_cells == 12
        assert len(higher_pair.range_study) == 8
        assert higher_pair.range_study[0].hopping_range_cells == 0
        assert higher_pair.range_study[-1].hopping_range_cells == 12
        assert low_pair.direct_route.hopping_range_cells == 4
        assert higher_pair.direct_route.hopping_range_cells == 4
        assert low_pair.isolation.external_status.value == "pass"
        assert higher_pair.isolation.external_status.value == "pass"
