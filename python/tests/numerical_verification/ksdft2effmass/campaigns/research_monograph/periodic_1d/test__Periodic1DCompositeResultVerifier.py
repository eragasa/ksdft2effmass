r"""Numerical verification of ``Periodic1DCompositeResultVerifier``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G composite finite Fourier, hopping,
training-error, route-comparison, Hermiticity, and array-identity reconstruction.

Facet and represented meaning

The verifier independently reconstructs channels determined by retained rank-two
matrices and exact composite input controls and explicitly identifies unavailable
channels.

Intrinsic and cross-object scope

The typed input/result correlation is supplied by the read-only campaign Workflow;
this evidence evaluates the verifier's direct NumPy reconstruction route without
importing production transform, fitting, or frame algorithms.

VVUQ and scientific exclusions

This is numerical verification of represented retained arrays.  It does not establish
material validity, polarization, topology, scientific validation, uncertainty
quantification, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeCampaignWorkflow,
    Periodic1DCompositeCampaignWorkflowRequest,
    Periodic1DCompositeResultVerifier,
    Periodic1DCompositeUnavailableVerificationChannel,
    Periodic1DCompositeVerificationRequest,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.numerical_verification
SUT = Periodic1DCompositeResultVerifier


class TestPeriodic1DCompositeResultVerifier:
    """Own independent retained composite-result reconstruction evidence."""

    def test_method__execute__reconstructs_available_retained_channels(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-001

        Requirement: The independent verifier reconstructs stored Fourier pairs,
        exact-pair Hermiticity, range diagnostics, direct routes, and array identities
        within an explicit absolute tolerance while naming unavailable channels.

        Method: Correlate the immutable Appendix G input/result bytes, then execute the
        direct-NumPy verifier at ``1e-11 E_G`` without importing production numerical
        construction algorithms.

        Oracle: Exact retained SHA-256 identities, direct finite Fourier sums, direct
        inverse sums, dense Hermitian eigenspectra, and unconstrained complex least
        squares under the documented half-open mesh and centered representatives.

        Acceptance: Both groups pass; independently measured reconstruction and route
        values equal the retained values to ``1e-11 E_G``; unavailable channels match
        the exact declared inventory.

        Interpretation: A pass establishes bounded numerical verification of every
        reconstructable composite result channel under the retained conventions.

        Limitations: Missing source frames, projectors, attacked gauges, withheld
        matrices, and rough reciprocal matrices prevent independent verification of
        the explicitly listed unavailable channels.

        Provenance: Appendix G ``composite-input.json`` and ``composite-result.json``;
        retained result SHA-256
        ``9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f``.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        correlated = Periodic1DCompositeCampaignWorkflow().execute(
            Periodic1DCompositeCampaignWorkflowRequest(
                (directory / "composite-input.json").read_bytes(),
                (directory / "composite-result.json").read_bytes(),
            )
        )

        result = SUT().execute(
            Periodic1DCompositeVerificationRequest(
                correlated,
                ScalarQuantity(1.0e-11, Unitless()),
            )
        )

        assert result.passes
        low_pair, higher_pair = result.groups
        assert low_pair.passes
        assert higher_pair.passes
        assert low_pair.smooth_transform_maximum_absolute_defect.magnitude <= 1.0e-11
        assert higher_pair.smooth_transform_maximum_absolute_defect.magnitude <= 1.0e-11
        assert low_pair.smooth_inverse_maximum_frobenius_error.magnitude <= 1.0e-11
        assert higher_pair.smooth_inverse_maximum_frobenius_error.magnitude <= 1.0e-11
        assert (
            low_pair.maximum_omitted_norm_reported_absolute_defect.magnitude <= 1.0e-11
        )
        higher_training_report_defect = (
            higher_pair.maximum_training_error_reported_absolute_defect.magnitude
        )
        assert higher_training_report_defect <= 1.0e-11
        assert low_pair.direct_coefficient_frobenius_defect.magnitude <= 1.0e-11
        higher_direct_operator_defect = (
            higher_pair.direct_training_operator_maximum_frobenius_defect.magnitude
        )
        assert higher_direct_operator_defect <= 1.0e-11
        assert result.unavailable_channels == (
            Periodic1DCompositeUnavailableVerificationChannel.SAMPLED_GAPS,
            Periodic1DCompositeUnavailableVerificationChannel.NEIGHBOR_OVERLAP_AND_WILSON,
            Periodic1DCompositeUnavailableVerificationChannel.CONTROLLED_GAUGE,
            Periodic1DCompositeUnavailableVerificationChannel.POINTWISE_ALIGNMENT,
            Periodic1DCompositeUnavailableVerificationChannel.ROUGH_RECIPROCAL_RECONSTRUCTION,
            Periodic1DCompositeUnavailableVerificationChannel.WITHHELD_RANGE_ERRORS,
            Periodic1DCompositeUnavailableVerificationChannel.SMOOTH_FRAME_IDENTITY,
            Periodic1DCompositeUnavailableVerificationChannel.SMOOTH_PROJECTOR_IDENTITY,
        )
