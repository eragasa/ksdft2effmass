r"""Software verification of ``Periodic1DWannier90WilsonVerifier``.

Evidence profile: claim_bearing

Bounded artifact scope: independent one-dimensional native Wilson-loop reconstruction.

Facet and represented meaning

Active-neighbor selection, polar factors, ordered loop multiplication, native gauge
transformation, phase spectra, circular defects, and dispositions are included.

Intrinsic and cross-object scope

Authenticated parsed ``nnkp``, ``mmn``, and ``u.mat`` records are compared with a
typed retained Wilson spectrum without production Wilson analysis Actions.

VVUQ and scientific exclusions

The maintained data are synthetic software fixtures and establish neither topology,
material validation, nor uncertainty quantification.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCampaignJsonDecoder,
    Periodic1DRetainedResultKind,
    Periodic1DWannier90NativeArtifactGroup,
    Periodic1DWannier90NativeArtifactWorkflow,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
    Periodic1DWannier90NativeArtifactWorkflowResult,
    Periodic1DWannier90WilsonVerificationRequest,
    Periodic1DWannier90WilsonVerifier,
)
from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90WilsonVerifier


class TestPeriodic1DWannier90WilsonVerifier:
    """Own independent native Wilson-loop reconstruction evidence."""

    def test_method__execute__reconstructs_known_loop_in_two_gauges(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-018

        Requirement: The verifier reconstructs an unordered Wilson spectrum from the
        active native overlap loop and obtains the same spectrum after native gauge
        transformation.

        Method: Verify a maintained one-point rank-two loop with diagonal eigenvalues
        ``-i`` and ``+i`` and an identity native gauge.

        Oracle: The exact loop eigenphases are analytically ``-pi/2`` and ``+pi/2``.

        Acceptance: Both spectra equal the retained pair within ``1e-12`` radians,
        both loops are unitary within ``1e-12``, and the aggregate disposition passes.

        Interpretation: A pass establishes independent loop assembly and gauge-route
        comparison for the represented native contracts.

        Limitations: One synthetic loop does not establish retained-run correctness.

        Provenance: Maintained ``native-artifact-correlation-fixture.json``.
        """
        native_result = self.native_result()

        result = SUT().execute(
            Periodic1DWannier90WilsonVerificationRequest(
                native_result,
                1.0e-12,
                1.0e-12,
                0.5,
            )
        )

        group = result.groups[0]
        assert group.active_overlap_count == 1
        assert group.direct_spectrum.eigenphases == (
            -1.5707963267948966,
            1.5707963267948966,
        )
        assert group.native_gauge_spectrum == group.direct_spectrum
        assert group.minimum_active_overlap_singular_value == 1.0
        assert group.passes
        assert result.passes

    def native_result(self) -> Periodic1DWannier90NativeArtifactWorkflowResult:
        """Build the correlated native Workflow result from maintained resources."""
        path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        decoder = Periodic1DCampaignJsonDecoder()
        fixture = decoder.document(path.read_bytes())
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
        return Periodic1DWannier90NativeArtifactWorkflow().execute(
            Periodic1DWannier90NativeArtifactWorkflowRequest(
                result_payload,
                Periodic1DRetainedResultKind.WANNIER90,
                (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
            )
        )
