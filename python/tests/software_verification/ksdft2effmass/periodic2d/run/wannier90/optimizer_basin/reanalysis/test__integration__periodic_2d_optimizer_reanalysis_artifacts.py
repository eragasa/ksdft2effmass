r"""Artifact-owned identity and route evidence for crosswalk row 053.

Evidence profile: claim_bearing

The tests bind compact repository bytes, checksum-catalog entries, reviewed facades, and
retired-route absence. They do not authenticate external native files, rerun Wannier90,
prove optimizer completeness, establish scientific validation, quantify uncertainty, or
record acceptance.
"""

import hashlib
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass import periodic2d
from ksdft2effmass.periodic2d.run import wannier90
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import reanalysis
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.decode import (
    Periodic2DOptimizerReanalysisDocumentDecoder,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.records import (
    OptimizerReanalysisDecodedDocuments,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = reanalysis.Periodic2DOptimizerReanalysisEncodedDocuments
SOURCE_DIGEST = "d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85"
RESULT_DIGEST = "89780db50cb367f429a7947894805a89fbfc757f571a55f82936507ef397f38b"
RETAINED_CONFIGURATION_COUNT = 9
RETAINED_START_COUNT_PER_CONFIGURATION = 8
EXPECTED_ENDPOINT_COUNT = (
    RETAINED_CONFIGURATION_COUNT * RETAINED_START_COUNT_PER_CONFIGURATION
)
EXPECTED_REFINEMENT_CASE_COUNT = 4


class TestPeriodic2DOptimizerReanalysisArtifacts:
    """Own compact artifact and public-route evidence for row 053."""

    def repository_root(self) -> Path:
        """Return the repository root containing retained compact evidence."""
        return Path(__file__).resolve().parents[9]

    def test_retained_artifacts__preserve_bytes_and_catalog_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-ARTIFACT-001.

        Requirement: Exact source/result bytes equal their maintained SHA-256 catalog
        identities without assigning provenance or scientific validity to those hashes.

        Acceptance: DataObject bytes are exact file objects and both catalog entries
        equal independently calculated identities.
        """
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        source = base.joinpath("result.json").read_bytes()
        result = base.joinpath("reanalysis-result.json").read_bytes()
        documents = SUT(source, result)
        catalog = {
            line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0]
            for line in base.joinpath("SHA256SUMS").read_text().splitlines()
            if line.strip()
        }

        assert documents.source_result_payload is source
        assert documents.result_payload is result
        assert hashlib.sha256(source).hexdigest() == SOURCE_DIGEST
        assert hashlib.sha256(result).hexdigest() == RESULT_DIGEST
        assert catalog["result.json"] == SOURCE_DIGEST
        assert catalog["reanalysis-result.json"] == RESULT_DIGEST

    def test_retained_documents__decode_to_closed_immutable_records(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-DECODE-001.

        Requirement: Strict wire decoding returns closed immutable records rather than
        exposing mutable generic JSON mappings to numerical verification Actions.

        Acceptance: The retained pair decodes to the exact aggregate type, nested
        sequences are tuples, and decoded state cannot be reassigned.
        """
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        documents = SUT(
            base.joinpath("result.json").read_bytes(),
            base.joinpath("reanalysis-result.json").read_bytes(),
        )

        decoded = Periodic2DOptimizerReanalysisDocumentDecoder().execute(documents)

        assert type(decoded) is OptimizerReanalysisDecodedDocuments
        assert type(decoded.source_result.configurations) is tuple
        assert type(decoded.reanalysis_result.configurations) is tuple
        with pytest.raises(FrozenInstanceError):
            decoded.source_result = decoded.source_result  # type: ignore[misc]

    def test_retained_campaign__passes_bounded_portable_verification(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-VERIFICATION-001.

        Requirement: The campaign authenticates compact sources and reconstructs the
        retained 72 endpoints and four common-estimator refinement cases without opening
        external native files.

        Acceptance: Both bounded pass flags are true, counts are exact, and the result
        digest identifies the exact retained reanalysis bytes.
        """
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        campaign = reanalysis.Periodic2DOptimizerReanalysisCampaign(
            SUT(
                base.joinpath("result.json").read_bytes(),
                base.joinpath("reanalysis-result.json").read_bytes(),
            )
        )

        verified = campaign.verify(repository_root=self.repository_root())

        assert verified.source_authentication_passed
        assert verified.structural_reconstruction_passed
        assert verified.endpoint_count == EXPECTED_ENDPOINT_COUNT
        assert verified.refinement_case_count == EXPECTED_REFINEMENT_CASE_COUNT
        assert verified.retained_result_sha256 == RESULT_DIGEST
        assert verified.passes

    def test_public_routes__share_identity_and_retired_model_is_absent(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-ROUTE-002.

        Requirement: Three reviewed facades expose one defining class, while the former
        model-named symbol and historical retained-model module remain absent.

        Acceptance: Class identity is shared and no compatibility alias/path exists.
        """
        assert periodic2d.Periodic2DOptimizerReanalysisEncodedDocuments is SUT
        assert wannier90.Periodic2DOptimizerReanalysisEncodedDocuments is SUT
        assert reanalysis.Periodic2DOptimizerReanalysisEncodedDocuments is SUT
        assert not hasattr(reanalysis, "Periodic2DOptimizerReanalysisCampaignModel")
        retired = (
            self.repository_root()
            / "python/src/ksdft2effmass/periodic2d/model/retained/"
            "optimizer_reanalysis.py"
        )
        assert not retired.exists()
