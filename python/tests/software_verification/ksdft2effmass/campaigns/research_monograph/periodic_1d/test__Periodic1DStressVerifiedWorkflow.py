r"""Software verification of ``Periodic1DStressVerifiedWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: integrated Appendix G stress correlation and independent
numerical-verification composition.

Facet and represented meaning

The Workflow preserves the complete retained-correlation ResultObject and independent
stress-verification ResultObject behind one supported orchestration surface.

Intrinsic and cross-object scope

Input/result identities and complete stress inventories are correlated before the
explicit verification tolerance is applied.

VVUQ and scientific exclusions

Composition success does not reproduce the historical calculation, establish material
validation, perform uncertainty quantification, or provide human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DStressCampaignWorkflowRequest,
    Periodic1DStressVerifiedWorkflow,
    Periodic1DStressVerifiedWorkflowRequest,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Periodic1DStressVerifiedWorkflow


class TestPeriodic1DStressVerifiedWorkflow:
    """Own integrated stress correlation and verification evidence."""

    def test_method__execute__preserves_correlation_and_verification(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-024

        Requirement: The supported stress Workflow correlates retained bytes before
        independent verification and preserves both complete outcomes.

        Method: Execute the public Workflow over immutable Appendix G stress bytes
        with an explicit ``1e-10`` unitless tolerance.

        Oracle: Exact retained input/result SHA-256 identities and the independent
        verifier's separate channel defects and aggregate disposition.

        Acceptance: Both identities agree, stable channel defects meet ``1e-10``,
        isolated overlaps meet their binary64 eigenvector tolerance, nonisolated
        overlaps remain explicitly unavailable, and the integrated disposition passes.

        Interpretation: A pass establishes correct supported orchestration without
        conflating retained correlation and numerical verification.

        Limitations: Numerical correctness belongs to separate numerical evidence;
        material validation, UQ, protected execution, and acceptance are excluded.

        Provenance: Appendix G ``stress-input.json`` and ``stress-result.json``.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        request = Periodic1DStressVerifiedWorkflowRequest(
            Periodic1DStressCampaignWorkflowRequest(
                (directory / "stress-input.json").read_bytes(),
                (directory / "stress-result.json").read_bytes(),
            ),
            ScalarQuantity(1.0e-10, Unitless()),
        )

        result = SUT().execute(request)

        assert result.passes
        assert result.campaign_result.input_sha256 == (
            "3be86c6ee7cb08c1c194aa97e856c89458907c23428bed19f6b38cdb437d987a"
        )
        assert result.campaign_result.result_sha256 == (
            "5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394"
        )
        verification = result.stress_verification
        assert (
            verification.potential_amplitude_maximum_absolute_defect.magnitude
            <= 1.0e-10
        )
        assert verification.potential_shape_maximum_absolute_defect.magnitude <= 1.0e-10
        assert (
            verification.mesh_band_isolation_maximum_absolute_defect.magnitude
            <= 1.0e-10
        )
        assert (
            verification.isolated_overlap_maximum_absolute_defect.magnitude
            <= verification.isolated_overlap_absolute_tolerance.magnitude
        )
        assert (
            verification.gauge_covariance_maximum_absolute_defect.magnitude <= 1.0e-10
        )
        assert (
            verification.route_assumption_maximum_absolute_defect.magnitude <= 1.0e-10
        )
        assert verification.unavailable_nonisolated_overlap_count == 65
