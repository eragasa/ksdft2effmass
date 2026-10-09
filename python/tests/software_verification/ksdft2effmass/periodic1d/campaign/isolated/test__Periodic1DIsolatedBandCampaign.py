r"""Software verification of ``Periodic1DIsolatedBandCampaign``.

Evidence profile: claim_bearing

Bounded artifact scope: isolated campaign DataObject encapsulation and typed verifier
delegation.

Facet and represented meaning

The DataObject contains immutable encoded documents and delegates verification
through an explicit typed request and result.

VVUQ and scientific exclusions

A pass establishes façade composition only. Numerical correctness remains separately
owned, and unavailable localization channels remain unavailable.
"""

from pathlib import Path

import pytest

from ksdft2effmass.operators import ScalarQuantity, Unitless
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DIsolatedBandCampaign,
    Periodic1DIsolatedBandCampaignCorrelationResult,
    Periodic1DIsolatedBandCampaignVerificationResult,
    Periodic1DIsolatedBandEncodedDocuments,
    Periodic1DIsolatedUnavailableVerificationChannel,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedBandCampaign


class TestPeriodic1DIsolatedBandCampaign:
    """Own isolated campaign DataObject encapsulation evidence."""

    @staticmethod
    def _campaign() -> Periodic1DIsolatedBandCampaign:
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        return SUT(
            Periodic1DIsolatedBandEncodedDocuments(
                (directory / "input.json").read_bytes(),
                (directory / "result.json").read_bytes(),
            )
        )

    def test_method__correlate__uses_distinct_correlation_action(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-027

        Requirement: Retained-wire binding and validation are a distinct operation
        exposed by the encapsulating DataObject.

        Method: Correlate the immutable isolated encoded documents without requesting
        numerical verification.

        Oracle: Exact correlation result type and retained input/result identities.

        Acceptance: Correlation returns the typed definition and result identities
        without a numerical-verification disposition.

        Interpretation: A pass establishes separate correlation ownership.

        Limitations: Correlation alone establishes no numerical or scientific claim.
        """
        campaign = self._campaign()
        result = campaign.correlate()

        assert type(campaign).__module__ == (
            "ksdft2effmass.periodic1d.campaign.isolated.campaign"
        )
        assert type(campaign.encoded_documents).__module__ == (
            "ksdft2effmass.periodic1d.campaign.isolated.encoded_documents"
        )
        assert type(result) is Periodic1DIsolatedBandCampaignCorrelationResult
        assert result.campaign_correlation.input_sha256 == (
            "ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb"
        )
        assert result.campaign_correlation.result_sha256 == (
            "37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c"
        )

    def test_method__verify__delegates_documents_through_typed_request(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-025

        Requirement: The DataObject encapsulates exact retained bytes while its
        verifier owns correlation and numerical-verification policy.

        Method: Construct the public DataObject from the retained version-one encoded
        documents and request verification with explicit unitless tolerances.

        Oracle: Exact result type, retained identities, aggregate disposition, and
        unavailable-channel inventory.

        Acceptance: Verification passes, identities remain exact, and unavailable
        localization evidence remains explicit.

        Interpretation: A pass establishes correct DataObject-to-verifier delegation
        without assigning verification behavior to encoded documents.

        Limitations: This test does not independently reconstruct numerical channels
        or establish material validation, UQ, or scientific acceptance.
        """
        result = self._campaign().verify(
            absolute_tolerance=ScalarQuantity(1.0e-10, Unitless()),
            curvature_absolute_tolerance=ScalarQuantity(1.0e-7, Unitless()),
        )

        assert type(result) is Periodic1DIsolatedBandCampaignVerificationResult
        assert result.passes
        assert result.campaign_correlation.input_sha256 == (
            "ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb"
        )
        assert result.campaign_correlation.result_sha256 == (
            "37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c"
        )
        assert result.verification.unavailable_channels == (
            Periodic1DIsolatedUnavailableVerificationChannel.GAUGE_TRANSPORT_AND_OVERLAPS,
            Periodic1DIsolatedUnavailableVerificationChannel.WANNIER_LOCALIZATION_PROFILE,
        )
