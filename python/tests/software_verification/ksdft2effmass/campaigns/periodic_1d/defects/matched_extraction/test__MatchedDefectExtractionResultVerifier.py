r"""Software verification of ``MatchedDefectExtractionResultVerifier``.

Evidence profile: claim_bearing

Bounded artifact scope: retained version-one matched known-map defect result.

A pass establishes independent reconstruction of the synthetic retained controls and
strict rejection of an unsupported result schema. It does not establish material
validation, silicon behavior, transferability, or uncertainty quantification.
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
SUT = matched_extraction.MatchedDefectExtractionResultVerifier


class TestMatchedDefectExtractionResultVerifier:
    """Own retained matched-extraction independent-verification evidence."""

    @staticmethod
    def _repository_root() -> Path:
        return Path(__file__).resolve().parents[8]

    def test_method__execute__reconstructs_retained_result(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-001.

        Requirement: The maintained verifier independently reconstructs every
        retained matched known-map control without importing the calculation
        workflow.

        Method: Verify the immutable retained version-one result and its bound input,
        parent, runner, and implementation identities.

        Oracle: Complete execution without a structured contract or numerical
        mismatch.

        Acceptance: The verifier returns normally.

        Interpretation: A pass establishes the bounded synthetic software and
        numerical-verification contract represented by the retained document.

        Limitations: The test does not rerun a material calculation or establish
        scientific validation or uncertainty quantification.
        """
        root = self._repository_root()
        result_path = (
            root / "calculations/research-monograph/impurity-defect-1d/result.json"
        )

        SUT().execute(result_path, root)

    def test_method__execute__rejects_unsupported_schema(self, tmp_path: Path) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-002.

        Requirement: Runtime verification rejects unsupported schemas under normal
        and optimized Python execution.

        Method: Change only the decoded schema version in a runtime-scratch copy.

        Oracle: Exact ``ValueError`` category and message.

        Acceptance: Verification stops before interpreting scientific fields.

        Interpretation: A pass establishes active version gating without relying on
        language-level assertions.

        Limitations: This case does not exhaust malformed JSON inputs.
        """
        root = self._repository_root()
        retained_path = (
            root / "calculations/research-monograph/impurity-defect-1d/result.json"
        )
        document = cast(
            dict[str, Periodic1DJsonValue],
            json.loads(retained_path.read_text(encoding="utf-8")),
        )
        document["schema_version"] = 2
        corrupted_path = tmp_path / "result.json"
        corrupted_path.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="unsupported result schema version"):
            SUT().execute(corrupted_path, root)
