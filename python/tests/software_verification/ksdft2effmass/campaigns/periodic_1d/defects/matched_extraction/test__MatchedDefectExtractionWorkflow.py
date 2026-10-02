r"""Software verification of ``MatchedDefectExtractionWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: matched known-map defect construction from immutable retained
input and accepted periodic-1D parents.

A pass establishes agreement with the retained synthetic capability apart from
implementation-specific provenance identities. It does not validate silicon,
transferability, continuum convergence, or uncertainty quantification.
"""

import json
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.periodic_1d import (
    Periodic1DJsonValue,
)
from ksdft2effmass.campaigns.periodic_1d.defects import (
    matched_extraction,
)

pytestmark = pytest.mark.software_verification
SUT = matched_extraction.MatchedDefectExtractionWorkflow


class TestMatchedDefectExtractionWorkflow:
    """Own matched known-map extraction workflow evidence."""

    @staticmethod
    def _repository_root() -> Path:
        return Path(__file__).resolve().parents[8]

    def test_method__execute__matches_retained_scientific_payload(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-003.

        Requirement: The maintained workflow reproduces the retained version-one
        synthetic scientific payload while recording its own implementation identity.

        Method: Decode the retained input, authenticate and load its accepted parent
        artifacts, execute the maintained workflow, and compare all fields except the
        provenance block.

        Oracle: Exact equality of the closed decoded JSON documents after removing
        implementation-specific provenance from both documents.

        Acceptance: Every retained scientific, numerical, limitation, and status
        field agrees exactly.

        Interpretation: A pass establishes behavior preservation for the matched
        known-map capability under the retained input.

        Limitations: Excluding provenance is necessary because the maintained package
        has different source paths and hashes from the historical implementation.
        """
        root = self._repository_root()
        directory = root / "calculations/research-monograph/impurity-defect-1d"
        input_path = directory / "input.json"
        specification = (
            matched_extraction.MatchedDefectExtractionInputDeserializer().execute(
                input_path.read_bytes()
            )
        )
        parent = matched_extraction.MatchedDefectParentDataLoader().execute(
            specification.parent, root
        )

        workflow_result = SUT().execute(
            specification,
            parent,
            root,
            input_path,
            directory / "run_experiment.py",
        )
        generated_path = tmp_path / "result.json"
        generated_path.write_bytes(workflow_result.document)
        matched_extraction.MatchedDefectExtractionResultVerifier().execute(
            generated_path, root
        )
        generated = cast(
            dict[str, Periodic1DJsonValue],
            json.loads(workflow_result.document.decode("utf-8")),
        )
        retained = cast(
            dict[str, Periodic1DJsonValue],
            json.loads((directory / "result.json").read_text(encoding="utf-8")),
        )
        generated.pop("provenance")
        retained.pop("provenance")

        assert generated == retained
