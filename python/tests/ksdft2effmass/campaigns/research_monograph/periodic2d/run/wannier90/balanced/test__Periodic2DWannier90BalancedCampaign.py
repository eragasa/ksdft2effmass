"""Portable evidence for the balanced periodic-2D Wannier90 comparison."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic2d import (
    Periodic2DWannier90BalancedCampaign,
    Periodic2DWannier90BalancedCampaignModel,
)
from ksdft2effmass.campaigns.research_monograph.periodic2d.run import wannier90

Verifier = wannier90.balanced.verify.Periodic2DWannier90BalancedCampaignVerifier
pytestmark = [
    pytest.mark.integration,
    pytest.mark.numerical_verification,
    pytest.mark.expensive,
]


class TestPeriodic2DWannier90BalancedCampaign:
    """Own repository-portable balanced comparison evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[9]

    def campaign(
        self, result: bytes | None = None
    ) -> Periodic2DWannier90BalancedCampaign:
        """Construct a campaign from retained exact result bytes."""
        path = self.root() / (
            "calculations/research-monograph/periodic-2d/wannier90-balanced-result.json"
        )
        retained = path.read_bytes()
        return Periodic2DWannier90BalancedCampaign(
            Periodic2DWannier90BalancedCampaignModel(
                retained if result is None else result
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__verify__reconstructs_portable_balanced_comparison(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-009.

        Requirement: Repository evidence reconstructs the balanced comparison.
        Method: Authenticate sources and rebuild parent, gauges, hopping, and spreads.
        Oracle: Independent loop-based Hamiltonian and Hermitian polar routes.
        Acceptance: Portable reconstruction passes with the retained result identity.
        Interpretation: This verifies one bounded synthetic external-tool result.
        Limitations: It does not rerun Wannier90 or establish convergence.
        """
        result = self.campaign().verify(repository_root=self.root())
        self.require(result.passes, "portable Wannier90 verification failed")
        self.require(
            result.retained_result_sha256
            == "422e53b012fb824164e3f03e67eeef6f5a013ce6f17da942ddc3f2d477b06e93",
            "retained identity mismatch",
        )

    def test_contract__verifier__does_not_import_extractor_and_rejects_corruption(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-010.

        Requirement: Verification is extractor-independent and corruption-sensitive.
        Method: Inspect imports and mutate one retained represented quantity.
        Oracle: Independent portable reconstruction.
        Acceptance: No extractor import and mutation is rejected.
        Interpretation: This verifies route separation and sensitivity.
        Limitations: Portable evidence does not authenticate absent native files.
        """
        tree = ast.parse(Path(inspect.getfile(Verifier)).read_text())
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.require(
            not any("extract" in module for module in modules),
            "verifier imports extractor",
        )
        retained = self.campaign().model.result_payload
        marker = b'"direct_w90_projector_maximum_frobenius_defect": '
        start = retained.find(marker)
        begin = start + len(marker)
        end = retained.find(b"\n", begin)
        mutated = retained[:begin] + b"0.5," + retained[end:]
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())
