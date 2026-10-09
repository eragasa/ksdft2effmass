r"""Routine campaign and result contracts for optimizer convergence regression.

Evidence profile: routine

Synthetic construction proves intrinsic immutability and validation only. It does not
prove verifier execution, retained provenance, optimizer convergence, or model validity.
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    convergence_regression as regression,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.verify import (  # noqa: E501
    Periodic2DOptimizerRegressionCampaignVerificationRequest,
    Periodic2DOptimizerRegressionCampaignVerificationResult,
)

Periodic2DOptimizerRegressionCampaign = regression.Periodic2DOptimizerRegressionCampaign
Periodic2DOptimizerRegressionEncodedDocuments = (
    regression.Periodic2DOptimizerRegressionEncodedDocuments
)

pytestmark = pytest.mark.software_verification
_DIGEST = "572b5ca7fe73ebb1cee6d9334e9ad6cddddea446fad3d02dfaf88202096ced22"


class TestPeriodic2DOptimizerRegressionCampaignContracts:
    """Own routine campaign/request/result evidence for row 054."""

    def documents(self) -> Periodic2DOptimizerRegressionEncodedDocuments:
        """Return minimal exact bytes suitable for intrinsic construction tests."""
        return Periodic2DOptimizerRegressionEncodedDocuments(b"{}", b"x", b"{}")

    def test_campaign__owns_documents_without_shared_verifier(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-ROUTE-001.

        Requirement: A campaign owns exact documents and creates request-scoped
        verification Actions rather than sharing a mutable class collaborator.

        Acceptance: Identity is retained, no class-level verifier exists, wrong
        ownership fails, and campaign state is frozen.
        """
        documents = self.documents()
        campaign = Periodic2DOptimizerRegressionCampaign(documents)

        assert campaign.encoded_documents is documents
        assert "verifier" not in Periodic2DOptimizerRegressionCampaign.__dict__
        with pytest.raises(TypeError, match="encoded_documents must be"):
            Periodic2DOptimizerRegressionCampaign(
                b"wrong"  # type: ignore[arg-type]
            )
        with pytest.raises(FrozenInstanceError):
            campaign.encoded_documents = documents  # type: ignore[misc]

    def test_request__requires_exact_documents_and_absolute_path(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-REQUEST-001.

        Requirement: Verification location is explicit, absolute, and separate from
        exact encoded-document ownership.

        Acceptance: Valid state is frozen; wrong documents, strings, and relative paths
        fail closed.
        """
        request = Periodic2DOptimizerRegressionCampaignVerificationRequest(
            self.documents(), Path("/")
        )
        assert request.repository_root == Path("/")
        with pytest.raises(TypeError, match="encoded_documents must be"):
            Periodic2DOptimizerRegressionCampaignVerificationRequest(
                b"wrong",  # type: ignore[arg-type]
                Path("/"),
            )
        with pytest.raises(TypeError, match="repository_root must be pathlib.Path"):
            Periodic2DOptimizerRegressionCampaignVerificationRequest(
                self.documents(),
                "/",  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            Periodic2DOptimizerRegressionCampaignVerificationRequest(
                self.documents(), Path("relative")
            )
        with pytest.raises(FrozenInstanceError):
            request.repository_root = Path("/tmp")  # type: ignore[misc]

    def test_result__validates_intrinsic_state_and_pass_conjunction(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-RESULT-001.

        Requirement: Pass flags, exact nonnegative counts, digest syntax, and
        immutability are intrinsic; direct construction does not prove Action execution.

        Acceptance: Valid state is retained, false flags prevent a pass, and invalid
        scalar representations or ranges fail.
        """
        result = Periodic2DOptimizerRegressionCampaignVerificationResult(
            True, True, 256, 196, 60, 32, _DIGEST
        )
        assert result.passes
        assert not Periodic2DOptimizerRegressionCampaignVerificationResult(
            False, True, 256, 196, 60, 32, _DIGEST
        ).passes
        with pytest.raises(TypeError, match="source_authentication_passed"):
            Periodic2DOptimizerRegressionCampaignVerificationResult(
                1,  # type: ignore[arg-type]
                True,
                256,
                196,
                60,
                32,
                _DIGEST,
            )
        with pytest.raises(TypeError, match="observation_count must be an integer"):
            Periodic2DOptimizerRegressionCampaignVerificationResult(
                True, True, True, 196, 60, 32, _DIGEST
            )
        with pytest.raises(ValueError, match="parameter_count must be nonnegative"):
            Periodic2DOptimizerRegressionCampaignVerificationResult(
                True, True, 256, 196, 60, -1, _DIGEST
            )
        with pytest.raises(ValueError, match="lowercase SHA-256 digest"):
            Periodic2DOptimizerRegressionCampaignVerificationResult(
                True, True, 256, 196, 60, 32, "G" * 64
            )
        with pytest.raises(FrozenInstanceError):
            result.observation_count = 0  # type: ignore[misc]
