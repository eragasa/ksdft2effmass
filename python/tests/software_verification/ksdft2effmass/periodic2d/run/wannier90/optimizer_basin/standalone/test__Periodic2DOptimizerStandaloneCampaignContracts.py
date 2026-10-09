r"""Routine campaign and result contracts for the standalone optimizer study.

Evidence profile: routine

Synthetic construction proves intrinsic immutability and validation only. It does not
prove verifier execution, retained provenance, optimizer convergence, or model validity.
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import standalone
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.verify import (
    Periodic2DOptimizerStandaloneCampaignVerificationRequest,
    Periodic2DOptimizerStandaloneCampaignVerificationResult,
)

pytestmark = pytest.mark.software_verification
_DIGEST = "add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a"


class TestPeriodic2DOptimizerStandaloneCampaignContracts:
    """Own routine campaign/request/result evidence for row 055."""

    def documents(self) -> standalone.Periodic2DOptimizerStandaloneEncodedDocuments:
        """Return minimal exact bytes suitable for intrinsic construction tests."""
        return standalone.Periodic2DOptimizerStandaloneEncodedDocuments(
            b"{}", b"{}", b"{}"
        )

    def test_campaign__owns_documents_without_shared_verifier(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-ROUTE-001.

        Requirement: A campaign owns exact documents and creates request-scoped
        verification Actions rather than sharing a class collaborator.

        Acceptance: Identity is retained, no class verifier exists, wrong ownership
        fails, and state is frozen.
        """
        documents = self.documents()
        campaign = standalone.Periodic2DOptimizerStandaloneCampaign(documents)

        assert campaign.encoded_documents is documents
        assert (
            "verifier" not in standalone.Periodic2DOptimizerStandaloneCampaign.__dict__
        )
        with pytest.raises(TypeError, match="encoded_documents must be"):
            standalone.Periodic2DOptimizerStandaloneCampaign(
                b"wrong"  # type: ignore[arg-type]
            )
        with pytest.raises(FrozenInstanceError):
            campaign.encoded_documents = documents  # type: ignore[misc]

    def test_request__requires_exact_documents_and_absolute_path(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-REQUEST-001.

        Requirement: Verification location is explicit, absolute, and separate from
        encoded-document ownership.

        Acceptance: Wrong documents, path strings, and relative paths fail closed.
        """
        request = Periodic2DOptimizerStandaloneCampaignVerificationRequest(
            self.documents(), Path("/")
        )
        assert request.repository_root == Path("/")
        with pytest.raises(TypeError, match="encoded_documents must be"):
            Periodic2DOptimizerStandaloneCampaignVerificationRequest(
                b"wrong",  # type: ignore[arg-type]
                Path("/"),
            )
        with pytest.raises(TypeError, match="repository_root must be pathlib.Path"):
            Periodic2DOptimizerStandaloneCampaignVerificationRequest(
                self.documents(),
                "/",  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            Periodic2DOptimizerStandaloneCampaignVerificationRequest(
                self.documents(), Path("relative")
            )
        with pytest.raises(FrozenInstanceError):
            request.repository_root = Path("/tmp")  # type: ignore[misc]

    def test_result__validates_intrinsic_state_and_pass_conjunction(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-RESULT-001.

        Requirement: Pass flags, exact nonnegative counts, digest syntax, and
        immutability are intrinsic; construction does not prove Action execution.

        Acceptance: False flags prevent a pass; negative counts, malformed digests, and
        mutation fail closed.
        """
        result = Periodic2DOptimizerStandaloneCampaignVerificationResult(
            True, True, 256, 120, 196, 60, _DIGEST
        )
        assert result.passes
        assert not Periodic2DOptimizerStandaloneCampaignVerificationResult(
            False, True, 256, 120, 196, 60, _DIGEST
        ).passes
        with pytest.raises(
            ValueError, match="final_nonconverged_count must be nonnegative"
        ):
            Periodic2DOptimizerStandaloneCampaignVerificationResult(
                True, True, 256, 120, 196, -1, _DIGEST
            )
        with pytest.raises(ValueError, match="lowercase SHA-256 digest"):
            Periodic2DOptimizerStandaloneCampaignVerificationResult(
                True, True, 256, 120, 196, 60, "G" * 64
            )
        with pytest.raises(FrozenInstanceError):
            result.endpoint_count = 0  # type: ignore[misc]

    @pytest.mark.parametrize(
        ("case", "message"),
        (
            ("authentication_flag", "source_authentication_passed"),
            ("endpoint_count", "endpoint_count must be an integer"),
        ),
    )
    def test_result__rejects_nonexact_boolean_and_integer_representations(
        self, case: str, message: str
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-RESULT-002.

        Requirement: Result flags and counts reject Boolean/integer interchange even
        though Python's numeric hierarchy relates the two built-in types.

        Acceptance: An integer flag and Boolean count each raise ``TypeError``.
        """
        with pytest.raises(TypeError, match=message):
            if case == "authentication_flag":
                Periodic2DOptimizerStandaloneCampaignVerificationResult(
                    1,  # type: ignore[arg-type]
                    True,
                    256,
                    120,
                    196,
                    60,
                    _DIGEST,
                )
            else:
                Periodic2DOptimizerStandaloneCampaignVerificationResult(
                    True, True, True, 120, 196, 60, _DIGEST
                )
