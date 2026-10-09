r"""Software verification of ``Periodic1DCompositeCampaign``.

Evidence profile: claim_bearing

Bounded artifact scope: composite campaign DataObject encapsulation and typed verifier
delegation.

Facet and represented meaning

The DataObject contains immutable encoded documents and delegates verification
through an explicit typed request and result.

VVUQ and scientific exclusions

A pass establishes façade composition only. Unavailable frame and gauge channels do
not become independent numerical evidence.
"""

from pathlib import Path

import pytest

from ksdft2effmass.operators import ScalarQuantity, Unitless
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DCompositeCampaign,
    Periodic1DCompositeCampaignCorrelationResult,
    Periodic1DCompositeCampaignVerificationResult,
    Periodic1DCompositeEncodedDocuments,
    Periodic1DCompositeUnavailableVerificationChannel,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeCampaign


class TestPeriodic1DCompositeCampaign:
    """Own composite campaign DataObject encapsulation evidence."""

    @staticmethod
    def _campaign() -> Periodic1DCompositeCampaign:
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        return SUT(
            Periodic1DCompositeEncodedDocuments(
                (directory / "composite-input.json").read_bytes(),
                (directory / "composite-result.json").read_bytes(),
            )
        )

    def test_contract__operations_do_not_retain_shared_action_instances(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-059-004.

        Requirement: The immutable campaign owner retains documents only; every
        operation constructs request-scoped Action owners rather than shared instances.

        Acceptance: No correlator or verifier object exists in class or instance state.

        Limitations: This structural check does not establish numerical independence or
        scientific validity.
        """
        campaign = self._campaign()

        assert campaign.__slots__ == ("encoded_documents",)
        assert not hasattr(type(campaign), "correlator")
        assert not hasattr(type(campaign), "verifier")

    def test_method__correlate__uses_distinct_correlation_action(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-028

        Requirement: Retained-wire binding and validation are a distinct operation
        exposed by the encapsulating DataObject.

        Method: Correlate the immutable composite encoded documents without requesting
        numerical verification.

        Oracle: Exact correlation result type, retained identities, and group order.

        Acceptance: Correlation returns typed records and identities without a
        numerical-verification disposition.

        Interpretation: A pass establishes separate correlation ownership.

        Limitations: Correlation alone establishes no numerical or scientific claim.
        """
        campaign = self._campaign()
        result = campaign.correlate()

        assert type(campaign).__module__.endswith(
            "periodic1d.campaign.composite.campaign"
        )
        assert type(campaign.encoded_documents).__module__.endswith(
            "periodic1d.campaign.composite.encoded_documents"
        )
        assert type(result) is Periodic1DCompositeCampaignCorrelationResult
        assert result.campaign_correlation.input_sha256 == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert result.campaign_correlation.result_sha256 == (
            "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f"
        )
        groups = result.campaign_correlation.campaign_result.groups
        assert tuple(group.group_id for group in groups) == ("low_pair", "higher_pair")

    def test_method__verify__delegates_documents_through_typed_request(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-026

        Requirement: The DataObject encapsulates exact composite bytes while its
        verifier owns correlation and reconstructable-channel policy.

        Method: Construct the public DataObject from the retained version-one encoded
        documents and request verification with an explicit unitless tolerance.

        Oracle: Exact result type, retained identities, ordered groups, aggregate
        disposition, and unavailable-channel inventory.

        Acceptance: Verification passes, identities and group order remain exact, and
        unavailable source channels remain explicit.

        Interpretation: A pass establishes correct DataObject-to-verifier delegation
        without assigning verification behavior to encoded documents.

        Limitations: This test does not independently reconstruct numerical channels
        or establish material validation, UQ, or scientific acceptance.
        """
        result = self._campaign().verify(
            absolute_tolerance=ScalarQuantity(1.0e-11, Unitless())
        )

        assert type(result) is Periodic1DCompositeCampaignVerificationResult
        assert result.passes
        assert result.campaign_correlation.input_sha256 == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert result.campaign_correlation.result_sha256 == (
            "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f"
        )
        correlated_groups = result.campaign_correlation.campaign_result.groups
        assert tuple(group.group_id for group in correlated_groups) == (
            "low_pair",
            "higher_pair",
        )
        assert (
            Periodic1DCompositeUnavailableVerificationChannel.WITHHELD_RANGE_ERRORS
            in result.verification.unavailable_channels
        )
