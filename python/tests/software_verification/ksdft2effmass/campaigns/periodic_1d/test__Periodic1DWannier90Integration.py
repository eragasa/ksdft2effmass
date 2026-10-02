r"""Software verification of ``Periodic1DWannier90Integration``.

Evidence profile: claim_bearing

Bounded artifact scope: encapsulated retained correlation and explicit native/Wilson
verification delegation.

VVUQ and scientific exclusions

A pass establishes façade composition over maintained contracts. It does not rerun
Wannier90, reproduce its convergence trajectory, validate a material, or establish UQ.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCampaignJsonDecoder,
    Periodic1DRetainedResultKind,
    Periodic1DWannier90EncodedDocuments,
    Periodic1DWannier90Integration,
    Periodic1DWannier90IntegrationCorrelationResult,
    Periodic1DWannier90IntegrationVerificationResult,
    Periodic1DWannier90NativeArtifactGroup,
)
from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90Integration


class TestPeriodic1DWannier90Integration:
    """Own encapsulating Wannier90 integration evidence."""

    @staticmethod
    def _calculation_directory() -> Path:
        root = Path(__file__).resolve().parents[6]
        return root / "calculations/research-monograph/periodic-1d"

    def test_method__correlate__delegates_encoded_documents(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-031

        Requirement: The integration DataObject correlates exact retained controls and
        results through its dedicated Actionizer.

        Method: Encapsulate the retained bounded Wannier90 comparison without native
        artifacts and request correlation.

        Oracle: Defining-module ownership, exact result type, and known payload hashes.

        Acceptance: The typed correlation preserves both exact SHA-256 identities.

        Interpretation: A pass establishes encapsulation and correlation delegation.

        Limitations: Correlation makes no numerical or scientific claim.
        """
        directory = self._calculation_directory()
        integration = SUT(
            Periodic1DWannier90EncodedDocuments(
                (directory / "composite-input.json").read_bytes(),
                (directory / "wannier90-result.json").read_bytes(),
                Periodic1DRetainedResultKind.WANNIER90,
            )
        )

        result = integration.correlate()

        assert type(integration).__module__.endswith("periodic_1d.run.wannier90.data")
        assert type(integration.encoded_documents).__module__.endswith(
            "periodic_1d.encoded_documents"
        )
        assert type(result) is Periodic1DWannier90IntegrationCorrelationResult
        assert result.campaign_correlation.composite_input_sha256 == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert result.campaign_correlation.result_sha256 == (
            "d167294da9ebb53173b91fa69f089900f11e03917969bc028b9c0e69db951535"
        )

    def test_method__verify__delegates_explicit_native_artifact_state(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-032

        Requirement: The integration DataObject delegates explicit native bytes and
        numerical controls without filesystem discovery or Wannier90 execution.

        Method: Build the maintained synthetic native-artifact fixture as immutable
        integration state and request bounded Wilson verification.

        Oracle: Existing authenticated native/Wilson Workflow result and disposition.

        Acceptance: The typed integration result reports a passing Wilson comparison.

        Interpretation: A pass establishes native-verification Actionizer delegation.

        Limitations: Synthetic data do not validate Wannier90 or material physics.
        """
        fixture_path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        decoder = Periodic1DCampaignJsonDecoder()
        fixture = decoder.document(fixture_path.read_bytes())
        result_document = decoder.mapping(
            fixture.get("result_document"), "result_document"
        )
        artifact_text = decoder.mapping(
            fixture.get("artifact_text_by_name"), "artifact_text_by_name"
        )
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        artifacts = tuple(
            Wannier90NativeArtifact(name, decoder.string(value, name).encode("utf-8"))
            for name, value in artifact_text.items()
        )
        directory = self._calculation_directory()
        integration = SUT(
            Periodic1DWannier90EncodedDocuments(
                (directory / "composite-input.json").read_bytes(),
                result_payload,
                Periodic1DRetainedResultKind.WANNIER90,
            ),
            (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
        )

        result = integration.verify(
            phase_absolute_tolerance=1.0e-12,
            loop_unitarity_absolute_tolerance=1.0e-12,
            minimum_active_overlap_singular_value=0.5,
        )

        assert type(result) is Periodic1DWannier90IntegrationVerificationResult
        assert result.passes
        assert result.native_verification.wilson_verification.groups[0].passes
