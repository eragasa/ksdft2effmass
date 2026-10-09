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

from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DCampaignJsonDecoder,
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.periodic1d.campaign.wannier90 import (
    Periodic1DWannier90EncodedDocuments,
    Periodic1DWannier90Integration,
    Periodic1DWannier90IntegrationCorrelationResult,
    Periodic1DWannier90IntegrationVerificationResult,
    Periodic1DWannier90NativeArtifactGroup,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90Integration


class TestPeriodic1DWannier90Integration:
    """Own encapsulating Wannier90 integration evidence."""

    @staticmethod
    def _calculation_directory() -> Path:
        root = Path(__file__).resolve().parents[7]
        return root / "calculations/research-monograph/periodic-1d"

    def test_method__correlate__delegates_encoded_documents(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-031

        Requirement: The integration DataObject correlates exact retained controls and
        results through its dedicated Action.

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
                Periodic1DEncodedResultKind.WANNIER90,
            )
        )

        result = integration.correlate()

        assert type(integration).__module__.endswith(
            "periodic1d.campaign.wannier90.integration"
        )
        assert type(integration.encoded_documents).__module__.endswith(
            "periodic1d.campaign.wannier90.encoded_documents"
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

        Interpretation: A pass establishes native-verification Action delegation.

        Limitations: Synthetic data do not validate Wannier90 or material physics.
        """
        fixture_path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        decoder = Periodic1DCampaignJsonDecoder()
        fixture = decoder.document(fixture_path.read_bytes())
        composite_input_document = decoder.mapping(
            fixture.get("composite_input_document"), "composite_input_document"
        )
        result_document = decoder.mapping(
            fixture.get("result_document"), "result_document"
        )
        artifact_text = decoder.mapping(
            fixture.get("artifact_text_by_name"), "artifact_text_by_name"
        )
        composite_input_payload = (
            json.dumps(composite_input_document, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        artifacts = tuple(
            Wannier90NativeArtifact(name, decoder.string(value, name).encode("utf-8"))
            for name, value in artifact_text.items()
        )
        integration = SUT(
            Periodic1DWannier90EncodedDocuments(
                composite_input_payload,
                result_payload,
                Periodic1DEncodedResultKind.WANNIER90,
            ),
            (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
        )

        result = integration.verify(
            phase_absolute_tolerance=1.0e-12,
            loop_unitarity_absolute_tolerance=1.0e-12,
            minimum_active_overlap_singular_value=0.5,
        )

        assert type(result) is Periodic1DWannier90IntegrationVerificationResult
        assert result.campaign_correlation.composite_input_sha256 == (
            "61a55618dc080dc5a6faa049aeb81bd16b86dc388afe21a6a12809c17ff2f00f"
        )
        assert result.passes
        assert result.native_verification.wilson_verification.groups[0].passes

    def test_result__rejects_campaign_and_native_result_wire_disagreement(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-010.

        Requirement: The integration verification Result intrinsically binds campaign
        correlation and native verification to the same exact result wire and kind.

        Method: Combine the retained production correlation with a verified synthetic
        native Result that consumes different result bytes.

        Oracle: Both nested Results retain their exact source bytes and explicit kind.

        Acceptance: Construction raises ``ValueError`` for result-wire disagreement.

        Interpretation: A pass establishes that callers cannot assemble a misleading
        integrated Result from independently valid but unrelated evidence objects.

        Limitations: Exact-byte equality does not establish execution provenance or
        scientific validity.
        """
        synthetic = self._verified_synthetic_integration()
        directory = self._calculation_directory()
        production_correlation = SUT(
            Periodic1DWannier90EncodedDocuments(
                (directory / "composite-input.json").read_bytes(),
                (directory / "wannier90-result.json").read_bytes(),
                Periodic1DEncodedResultKind.WANNIER90,
            )
        ).correlate()

        with pytest.raises(
            ValueError,
            match="campaign and native verification result wires do not agree",
        ):
            Periodic1DWannier90IntegrationVerificationResult(
                production_correlation.campaign_correlation,
                synthetic.native_verification,
            )

    def test_method__verify__authenticates_composite_input_before_native_work(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-008.

        Requirement: Integrated verification authenticates composite-input bytes from
        the result declaration before constructing or parsing native-artifact state.

        Method: Pair the valid synthetic result with malformed opaque input bytes and
        an empty native inventory.

        Oracle: Result-first campaign correlation owns the declared input SHA-256.

        Acceptance: Verification raises the input identity disagreement rather than a
        JSON parsing or missing-native-inventory diagnostic.

        Interpretation: A pass establishes the integration facade's input/result
        authentication barrier before native verification.

        Limitations: SHA-256 establishes exact content identity only, not authorship,
        historical execution, scientific validity, or acceptance.
        """
        fixture_path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        decoder = Periodic1DCampaignJsonDecoder()
        fixture = decoder.document(fixture_path.read_bytes())
        result_document = decoder.mapping(
            fixture.get("result_document"), "result_document"
        )
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        integration = SUT(
            Periodic1DWannier90EncodedDocuments(
                b"malformed opaque composite input",
                result_payload,
                Periodic1DEncodedResultKind.WANNIER90,
            )
        )

        with pytest.raises(
            ValueError, match="Wannier90 composite input SHA-256 does not agree"
        ):
            integration.verify(
                phase_absolute_tolerance=1.0e-12,
                loop_unitarity_absolute_tolerance=1.0e-12,
                minimum_active_overlap_singular_value=0.5,
            )

    def _verified_synthetic_integration(
        self,
    ) -> Periodic1DWannier90IntegrationVerificationResult:
        """Build the maintained fully correlated synthetic integration Result."""
        fixture_path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        decoder = Periodic1DCampaignJsonDecoder()
        fixture = decoder.document(fixture_path.read_bytes())
        composite_input_document = decoder.mapping(
            fixture.get("composite_input_document"), "composite_input_document"
        )
        result_document = decoder.mapping(
            fixture.get("result_document"), "result_document"
        )
        artifact_text = decoder.mapping(
            fixture.get("artifact_text_by_name"), "artifact_text_by_name"
        )
        composite_input_payload = (
            json.dumps(composite_input_document, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        artifacts = tuple(
            Wannier90NativeArtifact(name, decoder.string(value, name).encode("utf-8"))
            for name, value in artifact_text.items()
        )
        integration = SUT(
            Periodic1DWannier90EncodedDocuments(
                composite_input_payload,
                result_payload,
                Periodic1DEncodedResultKind.WANNIER90,
            ),
            (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
        )
        return integration.verify(
            phase_absolute_tolerance=1.0e-12,
            loop_unitarity_absolute_tolerance=1.0e-12,
            minimum_active_overlap_singular_value=0.5,
        )
