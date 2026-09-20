r"""Software verification of ``Periodic1DWannier90VerifiedNativeWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: integrated native correlation and Wilson verification.

Facet and represented meaning

Retained-result adaptation, complete byte authentication, supported native parsing,
active-loop reconstruction, gauge comparison, and aggregate disposition are included.

Intrinsic and cross-object scope

The Workflow composes the public native-artifact Workflow with the independent Wilson
verifier while preserving both operational ResultObjects.

VVUQ and scientific exclusions

The maintained fixture is synthetic; passing establishes software and bounded
numerical-verification behavior, not topology, material validation, or UQ.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCampaignJsonDecoder,
    Periodic1DRetainedResultKind,
    Periodic1DWannier90NativeArtifactGroup,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
    Periodic1DWannier90VerifiedNativeWorkflow,
    Periodic1DWannier90VerifiedNativeWorkflowRequest,
)
from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90VerifiedNativeWorkflow


class TestPeriodic1DWannier90VerifiedNativeWorkflow:
    """Own integrated retained/native/Wilson Workflow evidence."""

    def test_method__execute__returns_correlated_passing_verification(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-019

        Requirement: One supported Workflow integrates authenticated native records and
        the independent Wilson verifier without hiding either ResultObject.

        Method: Execute the integrated Workflow over the maintained rank-two fixture.

        Oracle: Exact artifact hashes and analytical ``-pi/2,+pi/2`` loop phases.

        Acceptance: Eleven artifacts correlate, the Wilson group passes, and the
        integrated disposition is true.

        Interpretation: A pass establishes supported end-to-end retained integration.

        Limitations: Synthetic data do not validate a Wannier90 executable or material.

        Provenance: Maintained ``native-artifact-correlation-fixture.json``.
        """
        native_request = self.native_request()

        result = SUT().execute(
            Periodic1DWannier90VerifiedNativeWorkflowRequest(
                native_request,
                1.0e-12,
                1.0e-12,
                0.5,
            )
        )

        assert (
            len(result.native_artifact_result.groups[0].correlation.observed_identities)
            == 11
        )
        assert result.wilson_verification.groups[0].passes
        assert result.passes

    def native_request(self) -> Periodic1DWannier90NativeArtifactWorkflowRequest:
        """Build one native-artifact request from the maintained fixture resource."""
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
        return Periodic1DWannier90NativeArtifactWorkflowRequest(
            result_payload,
            Periodic1DRetainedResultKind.WANNIER90,
            (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
        )
