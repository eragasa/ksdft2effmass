r"""Numerical verification of ``Periodic1DStressResultVerifier``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G amplitude, shape, mesh, isolation, gauge,
and fitting-route stress channels.

Facet and represented meaning

The verifier independently assembles dense plane-wave and finite-difference matrices,
finite Fourier sums, sewn overlaps, scalar parallel transport, and direct complex
least-squares fits from the exact correlated stress controls.

Intrinsic and cross-object scope

Correlation is supplied by the read-only campaign Workflow; this evidence evaluates
the direct NumPy/SciPy reconstruction without importing production construction,
transport, transform, or fitting algorithms.

VVUQ and scientific exclusions

This is bounded numerical verification of the represented dimensionless stress
campaign, not material validation, polarization or topology evidence, uncertainty
quantification, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DStressCampaignWorkflow,
    Periodic1DStressCampaignWorkflowRequest,
    Periodic1DStressResultVerifier,
    Periodic1DStressVerificationRequest,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.numerical_verification
SUT = Periodic1DStressResultVerifier


class TestPeriodic1DStressResultVerifier:
    """Own independent retained stress-result reconstruction evidence."""

    def test_method__execute__reconstructs_all_retained_stress_channels(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-STRESS-001

        Requirement: The verifier independently reconstructs every stable typed
        amplitude, shape, mesh/band/isolation, gauge-covariance, and fitting-route
        stress value within an explicit stable-scalar tolerance and a binary64
        eigenvector tolerance, while explicitly counting single-band overlaps made
        unavailable by a failed isolation disposition.

        Method: Correlate immutable Appendix G stress bytes, then execute direct dense
        plane-wave and finite-difference assembly, finite Fourier sums, sewn overlaps,
        scalar parallel transport, and complex least squares.

        Oracle: Matrices assembled from the documented finite Fourier equations,
        direct forward and inverse finite sums, projector identities, and independent
        ``numpy.linalg.lstsq`` solutions under the retained mesh conventions.

        Acceptance: Every stable dimensionless channel maximum is at most ``1e-10``;
        isolated overlap defects are at most twice square-root binary64 epsilon; all
        65 nonisolated single-band overlaps are declared unavailable; and the aggregate
        verification disposition passes.

        Interpretation: A pass establishes bounded numerical verification of every
        retained stress channel under the exact represented conventions.

        Limitations: The retained stress campaign is illustrative and establishes no
        material adequacy, scientific validation, UQ, or transferability.

        Provenance: Appendix G ``stress-input.json`` and ``stress-result.json``;
        retained result SHA-256
        ``5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394``.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        correlated = Periodic1DStressCampaignWorkflow().execute(
            Periodic1DStressCampaignWorkflowRequest(
                (directory / "stress-input.json").read_bytes(),
                (directory / "stress-result.json").read_bytes(),
            )
        )

        result = SUT().execute(
            Periodic1DStressVerificationRequest(
                correlated,
                ScalarQuantity(1.0e-10, Unitless()),
            )
        )

        assert result.potential_amplitude_maximum_absolute_defect.magnitude <= 1.0e-10
        assert result.potential_shape_maximum_absolute_defect.magnitude <= 1.0e-10
        assert result.mesh_band_isolation_maximum_absolute_defect.magnitude <= 1.0e-10
        assert (
            result.isolated_overlap_maximum_absolute_defect.magnitude
            <= result.isolated_overlap_absolute_tolerance.magnitude
        )
        assert result.gauge_covariance_maximum_absolute_defect.magnitude <= 1.0e-10
        assert result.route_assumption_maximum_absolute_defect.magnitude <= 1.0e-10
        assert result.unavailable_nonisolated_overlap_count == 65
        assert result.passes
