r"""Routine intrinsic evidence for optimizer-reanalysis campaign contracts.

Evidence profile: routine

These synthetic tests establish immutable composition and verification-result
invariants. They do not execute retained numerical verification or authenticate
campaign artifacts.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis import (
    Periodic2DOptimizerReanalysisCampaign,
    Periodic2DOptimizerReanalysisEncodedDocuments,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.verify import (
    Periodic2DOptimizerReanalysisCampaignVerificationResult,
)

pytestmark = pytest.mark.software_verification
DIGEST = "89780db50cb367f429a7947894805a89fbfc757f571a55f82936507ef397f38b"
VALID_ENDPOINT_COUNT = 72
VALID_REFINEMENT_CASE_COUNT = 4


class TestPeriodic2DOptimizerReanalysisCampaignContracts:
    """Own campaign-composition and Result invariants for crosswalk row 053."""

    def test_campaign__owns_documents_without_shared_verifier(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-ROUTE-001.

        Requirement: The immutable campaign owns exact documents and constructs a fresh
        verifier Action per request rather than exposing a shared mutable collaborator.

        Acceptance: Exact documents are retained, no class-level verifier exists,
        incompatible ownership fails, and state is frozen.
        """
        documents = Periodic2DOptimizerReanalysisEncodedDocuments(b"{}", b"{}")
        campaign = Periodic2DOptimizerReanalysisCampaign(documents)

        assert campaign.encoded_documents is documents
        assert "verifier" not in Periodic2DOptimizerReanalysisCampaign.__dict__
        with pytest.raises(TypeError, match="encoded_documents must be"):
            Periodic2DOptimizerReanalysisCampaign(
                b"not-documents"  # type: ignore[arg-type]
            )
        with pytest.raises(FrozenInstanceError):
            campaign.encoded_documents = documents  # type: ignore[misc]

    def test_result__validates_state_and_pass_conjunction(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-RESULT-001.

        Requirement: Result flags, nonnegative counts, digest syntax, immutability, and
        aggregate pass logic are intrinsic; direct construction proves no Action run.

        Acceptance: Valid state is retained, either false flag prevents a pass, invalid
        scalar representations/ranges fail, and fields cannot be reassigned.
        """
        result = Periodic2DOptimizerReanalysisCampaignVerificationResult(
            True,
            True,
            VALID_ENDPOINT_COUNT,
            VALID_REFINEMENT_CASE_COUNT,
            DIGEST,
        )

        assert result.passes
        assert not Periodic2DOptimizerReanalysisCampaignVerificationResult(
            False,
            True,
            VALID_ENDPOINT_COUNT,
            VALID_REFINEMENT_CASE_COUNT,
            DIGEST,
        ).passes
        assert not Periodic2DOptimizerReanalysisCampaignVerificationResult(
            True,
            False,
            VALID_ENDPOINT_COUNT,
            VALID_REFINEMENT_CASE_COUNT,
            DIGEST,
        ).passes
        with pytest.raises(TypeError, match="source_authentication_passed"):
            Periodic2DOptimizerReanalysisCampaignVerificationResult(
                1,  # type: ignore[arg-type]
                True,
                VALID_ENDPOINT_COUNT,
                VALID_REFINEMENT_CASE_COUNT,
                DIGEST,
            )
        with pytest.raises(TypeError, match="endpoint_count must be an integer"):
            Periodic2DOptimizerReanalysisCampaignVerificationResult(
                True,
                True,
                True,
                VALID_REFINEMENT_CASE_COUNT,
                DIGEST,
            )
        with pytest.raises(
            ValueError, match="refinement_case_count must be nonnegative"
        ):
            Periodic2DOptimizerReanalysisCampaignVerificationResult(
                True, True, VALID_ENDPOINT_COUNT, -1, DIGEST
            )
        with pytest.raises(ValueError, match="lowercase SHA-256 digest"):
            Periodic2DOptimizerReanalysisCampaignVerificationResult(
                True,
                True,
                VALID_ENDPOINT_COUNT,
                VALID_REFINEMENT_CASE_COUNT,
                "G" * 64,
            )
        with pytest.raises(FrozenInstanceError):
            result.endpoint_count = 0  # type: ignore[misc]
