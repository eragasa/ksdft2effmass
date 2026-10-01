"""Portable evidence for the periodic-2D optimizer-basin campaign."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.periodic2d import (
    Periodic2DOptimizerBasinCampaign,
    Periodic2DOptimizerBasinCampaignModel,
)
from ksdft2effmass.campaigns.periodic2d.run import wannier90

Verifier = wannier90.optimizer_basin.verify.Periodic2DOptimizerBasinCampaignVerifier
pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


class TestPeriodic2DOptimizerBasinCampaign:
    """Own retained multi-start outcome and negative-gate evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[8]

    def campaign(self, result: bytes | None = None) -> Periodic2DOptimizerBasinCampaign:
        """Construct a campaign from exact retained study documents."""
        base = (
            self.root() / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        retained = (base / "result.json").read_bytes()
        return Periodic2DOptimizerBasinCampaign(
            Periodic2DOptimizerBasinCampaignModel(
                (base / "study-input.json").read_bytes(),
                retained if result is None else result,
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__verify__retains_every_endpoint_and_negative_disposition(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-013.

        Requirement: Every declared endpoint contributes to the retained disposition.
        Method: Reconstruct identities, basin partitions, counts, and frozen gates.
        Oracle: Closed study declarations and retained endpoint arithmetic.
        Acceptance: Nine configurations retain 51 converged and 21 stopped outcomes.
        Interpretation: This verifies a bounded negative convergence result.
        Limitations: It neither proves distinct minima nor reruns optimization.
        """
        result = self.campaign().verify(repository_root=self.root())
        self.require(result.passes, "optimizer-basin verification failed")
        self.require(result.configuration_count == 9, "configuration count changed")
        self.require(result.converged_count == 51, "converged count changed")
        self.require(result.nonconverged_count == 21, "stopped count changed")
        self.require(
            result.retained_result_sha256
            == "d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85",
            "retained identity mismatch",
        )

    def test_contract__verifier__avoids_external_execution_and_rejects_corruption(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-014.

        Requirement: Portable verification avoids external execution data and
        detects changes.
        Method: Inspect source imports and mutate the aggregate convergence count.
        Oracle: Reconstructed per-endpoint arithmetic.
        Acceptance: No executor/extractor import and mutation is rejected.
        Interpretation: This verifies portable scope and sensitivity.
        Limitations: Native files and optimizer trajectories are not authenticated.
        """
        source = Path(inspect.getfile(Verifier)).read_text()
        tree = ast.parse(source)
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.require(
            not any("execute" in module or "extract" in module for module in modules),
            "verifier imports execution route",
        )
        self.require(
            "execution_result_path).read" not in source,
            "verifier reads external result",
        )
        retained = self.campaign().model.result_payload
        mutated = retained.replace(
            b'"converged_localization_count": 51',
            b'"converged_localization_count": 50',
            1,
        )
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())
