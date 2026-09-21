r"""Numerical verification of ``Periodic1DIsolatedResultVerifier``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G isolated parent and reduction channels.

Facet and represented meaning

The verifier independently assembles dense parent matrices, finite Fourier sums,
finite-range reconstructions, withheld comparisons, and reference diagnostics.

Intrinsic and cross-object scope

Correlation is supplied by the read-only campaign Workflow; this evidence evaluates
the independent verifier without importing production construction algorithms.

VVUQ and scientific exclusions

This is bounded numerical verification, not material validation, polarization evidence,
uncertainty quantification, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DIsolatedBandCampaignWorkflow,
    Periodic1DIsolatedBandCampaignWorkflowRequest,
    Periodic1DIsolatedResultVerifier,
    Periodic1DIsolatedUnavailableVerificationChannel,
    Periodic1DIsolatedVerificationRequest,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.numerical_verification
SUT = Periodic1DIsolatedResultVerifier


class TestPeriodic1DIsolatedResultVerifier:
    """Own independent isolated-band reconstruction evidence."""

    def test_method__execute__reconstructs_available_retained_channels(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-ISOLATED-001

        Requirement: The verifier independently reconstructs every isolated-band
        channel supported by retained source values and names unavailable channels.

        Method: Correlate the immutable input/result bytes and execute direct NumPy,
        SciPy-Mathieu, finite-difference, Fourier, and least-squares reconstruction.

        Oracle: Dense matrices assembled from the documented cosine-model equations,
        exact finite sums, direct least squares, and SciPy Mathieu characteristic
        values.

        Acceptance: Ordinary defects do not exceed ``1e-10 E_G``; the separately
        scaled center-curvature defect does not exceed ``1e-7 E_G``; exact unavailable
        channels remain listed.

        Interpretation: A pass establishes bounded numerical verification of the
        reconstructable retained isolated-band channels.

        Limitations: Source transported frames and localization density samples were
        not retained and are not treated as verified.

        Provenance: Appendix G ``input.json`` and ``result.json``.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        correlated = Periodic1DIsolatedBandCampaignWorkflow().execute(
            Periodic1DIsolatedBandCampaignWorkflowRequest(
                (directory / "input.json").read_bytes(),
                (directory / "result.json").read_bytes(),
            )
        )

        result = SUT().execute(
            Periodic1DIsolatedVerificationRequest(
                correlated,
                ScalarQuantity(1.0e-10, Unitless()),
                ScalarQuantity(1.0e-7, Unitless()),
            )
        )

        assert result.passes
        assert result.parent_maximum_reported_absolute_defect.magnitude <= 1.0e-10
        assert result.lowest_band_maximum_absolute_defect.magnitude <= 1.0e-10
        assert result.hopping_transform_maximum_absolute_defect.magnitude <= 1.0e-10
        assert result.range_study_maximum_reported_absolute_defect.magnitude <= 1.0e-10
        assert result.zone_center_curvature_reported_absolute_defect.magnitude <= 1.0e-7
        assert result.unavailable_channels == (
            Periodic1DIsolatedUnavailableVerificationChannel.GAUGE_TRANSPORT_AND_OVERLAPS,
            Periodic1DIsolatedUnavailableVerificationChannel.WANNIER_LOCALIZATION_PROFILE,
        )
