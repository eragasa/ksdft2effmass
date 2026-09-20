r"""Software verification of ``Periodic1DWannier90NativeArtifactWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: execution-free retained-result/native-artifact correlation.

Facet and represented meaning

Complete identities, seven parsed scientific text files, centers, and dimensions are
included; opaque checkpoint and log bytes are authenticated without interpretation.

Intrinsic and cross-object scope

Typed retained results, authenticated payloads, parser results, and Wilson rank are
correlated for one authored group.

VVUQ and scientific exclusions

Synthetic fixtures establish software composition only, not Wannier90 correctness,
localization convergence, material validation, or UQ.
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
)
from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90NativeArtifactWorkflow


class TestPeriodic1DWannier90NativeArtifactWorkflow:
    """Own execution-free native correlation Workflow evidence."""

    def test_method__execute__authenticates_parses_and_correlates_group(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-017

        Requirement: The Workflow authenticates all artifacts and parses supported
        scientific files only after binding them to one retained result group.

        Method: Execute over one maintained synthetic result and artifact inventory.

        Oracle: Explicit fixture hashes, dimensions, centers, and native text records.

        Acceptance: Eleven identities correlate; seven scientific records parse with
        one k point, two bands, two Wannier functions, and retained centers.

        Interpretation: A pass establishes execution-free native correlation behavior.

        Limitations: The fixture is synthetic and no executable or filesystem discovery
        is invoked by the Workflow.

        Provenance: Maintained ``native-artifact-correlation-fixture.json``.
        """
        fixture = self.load_fixture()
        decoder = Periodic1DCampaignJsonDecoder()
        result_document = decoder.mapping(
            fixture.get("result_document"), "result_document"
        )
        artifact_text = decoder.mapping(
            fixture.get("artifact_text_by_name"), "artifact_text_by_name"
        )
        artifacts = tuple(
            Wannier90NativeArtifact(
                name,
                decoder.string(value, name).encode("utf-8"),
            )
            for name, value in artifact_text.items()
        )
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

        result = SUT().execute(
            Periodic1DWannier90NativeArtifactWorkflowRequest(
                result_payload,
                Periodic1DRetainedResultKind.WANNIER90,
                (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
            )
        )

        group = result.groups[0]
        assert len(group.correlation.observed_identities) == 11
        assert group.parsed_artifacts.eigenvalues.kpoint_count == 1
        assert group.parsed_artifacts.eigenvalues.band_count == 2
        assert group.parsed_artifacts.localization.wannier_count == 2

    def load_fixture(self) -> dict[str, object]:
        """Decode the maintained immutable synthetic resource."""
        path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        return Periodic1DCampaignJsonDecoder().document(path.read_bytes())
