r"""Routine ownership evidence for the optimizer-basin campaign facade.

Evidence profile: routine

These synthetic tests establish exact document ownership, operational immutability, and
absence of a replaceable shared verifier collaborator. They do not authenticate retained
files, execute the verifier, establish convergence, or record scientific acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    Periodic2DOptimizerBasinCampaign,
    Periodic2DOptimizerBasinEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DOptimizerBasinCampaign


class TestPeriodic2DOptimizerBasinCampaign:
    """Own intrinsic campaign-composition evidence for crosswalk row 052."""

    def test_construction__owns_exact_documents_without_shared_verifier(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-ROUTE-002.

        Requirement: The immutable campaign owns only its exact encoded documents and
        creates request-scoped verifier Actions rather than exposing a shared mutable
        collaborator.

        Acceptance: Exact documents are retained, no class-level ``verifier`` exists,
        incompatible documents fail, and the retained field cannot be reassigned.
        """
        documents = Periodic2DOptimizerBasinEncodedDocuments(b"{}", b"{}")
        campaign = SUT(documents)

        assert campaign.encoded_documents is documents
        assert "verifier" not in SUT.__dict__
        with pytest.raises(TypeError, match="encoded_documents must be"):
            SUT(object())  # type: ignore[arg-type]
        with pytest.raises(FrozenInstanceError):
            campaign.encoded_documents = documents  # type: ignore[misc]
