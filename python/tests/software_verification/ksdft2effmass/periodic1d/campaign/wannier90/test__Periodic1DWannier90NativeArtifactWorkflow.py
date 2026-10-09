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

import copy
import hashlib
import json
from pathlib import Path

import pytest

from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DCampaignJsonDecoder,
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.periodic1d.campaign.wannier90 import (
    Periodic1DWannier90NativeArtifactGroup,
    Periodic1DWannier90NativeArtifactWorkflow,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
)

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
        fixture = self._load_fixture()
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
                Periodic1DEncodedResultKind.WANNIER90,
                (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
            )
        )

        group = result.groups[0]
        assert len(group.correlation.observed_identities) == 11
        assert group.parsed_artifacts.eigenvalues.kpoint_count == 1
        assert group.parsed_artifacts.eigenvalues.band_count == 2
        assert group.parsed_artifacts.localization.wannier_count == 2

    def test_method__execute__authenticates_before_native_parsing(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-003.

        Requirement: Native artifact identity authentication precedes scientific text
        parsing.

        Method: Replace the valid eigenvalue text by malformed bytes while preserving
        the retained expected artifact identity.

        Oracle: The Workflow's documented authentication-before-parsing order.

        Acceptance: Execution raises exact native identity disagreement rather than an
        eigenvalue parsing diagnostic.

        Interpretation: A pass establishes fail-closed ordering at the native byte
        boundary.

        Limitations: SHA-256 authenticates content identity only; it does not establish
        authorship, execution provenance, or scientific validity.
        """
        fixture = self._load_fixture()
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
                (
                    b"malformed eigenvalue text"
                    if name == "fixture.eig"
                    else decoder.string(value, name).encode("utf-8")
                ),
            )
            for name, value in artifact_text.items()
        )
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

        with pytest.raises(
            ValueError, match="native artifact identities do not agree exactly"
        ):
            SUT().execute(
                Periodic1DWannier90NativeArtifactWorkflowRequest(
                    result_payload,
                    Periodic1DEncodedResultKind.WANNIER90,
                    (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
                )
            )

    def test_method__execute__authenticates_all_groups_before_parsing(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-007.

        Requirement: The whole multi-group native inventory crosses its byte-identity
        barrier before scientific parsing begins for any group.

        Method: Give the first group authenticated but malformed eigenvalue text and
        the second group a digest mismatch. Both groups otherwise duplicate the valid
        synthetic rank-two fixture under distinct explicit group identities.

        Oracle: Whole-request authentication must report the second-group identity
        mismatch before a parser can inspect the first group's malformed text.

        Acceptance: Execution raises the native identity disagreement diagnostic rather
        than an eigenvalue parser diagnostic.

        Interpretation: A pass establishes authentication-before-parsing ordering over
        more than one retained group.

        Limitations: Content identity establishes neither authorship nor scientific
        validity, and this synthetic fixture does not exercise external files.
        """
        fixture = self._load_fixture()
        decoder = Periodic1DCampaignJsonDecoder()
        result_document = copy.deepcopy(
            decoder.mapping(fixture.get("result_document"), "result_document")
        )
        artifact_text = decoder.mapping(
            fixture.get("artifact_text_by_name"), "artifact_text_by_name"
        )
        malformed_eigenvalues = b"authenticated but malformed eigenvalue text"
        first_group = copy.deepcopy(result_document["groups"][0])
        first_group["id"] = "first"
        for identity in first_group["artifact_identities"]:
            if identity["name"] == "fixture.eig":
                identity["bytes"] = len(malformed_eigenvalues)
                identity["sha256"] = hashlib.sha256(malformed_eigenvalues).hexdigest()
        second_group = copy.deepcopy(result_document["groups"][0])
        second_group["id"] = "second"
        result_document["groups"] = [first_group, second_group]
        ordinary_artifacts = tuple(
            Wannier90NativeArtifact(
                name,
                decoder.string(value, name).encode("utf-8"),
            )
            for name, value in artifact_text.items()
        )
        first_artifacts = tuple(
            Wannier90NativeArtifact(
                artifact.name,
                (
                    malformed_eigenvalues
                    if artifact.name == "fixture.eig"
                    else artifact.payload
                ),
            )
            for artifact in ordinary_artifacts
        )
        second_artifacts = tuple(
            Wannier90NativeArtifact(
                artifact.name,
                b"late-group identity mismatch"
                if artifact.name == "fixture.amn"
                else artifact.payload,
            )
            for artifact in ordinary_artifacts
        )
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

        with pytest.raises(
            ValueError, match="native artifact identities do not agree exactly"
        ):
            SUT().execute(
                Periodic1DWannier90NativeArtifactWorkflowRequest(
                    result_payload,
                    Periodic1DEncodedResultKind.WANNIER90,
                    (
                        Periodic1DWannier90NativeArtifactGroup(
                            "first", first_artifacts
                        ),
                        Periodic1DWannier90NativeArtifactGroup(
                            "second", second_artifacts
                        ),
                    ),
                )
            )

    def _load_fixture(self) -> dict[str, object]:
        """Decode the maintained immutable synthetic resource."""
        path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        return Periodic1DCampaignJsonDecoder().document(path.read_bytes())
