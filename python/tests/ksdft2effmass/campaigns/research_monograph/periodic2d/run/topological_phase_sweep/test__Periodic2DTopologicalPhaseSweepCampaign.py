"""Retained evidence for the periodic-2D topological phase sweep."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic2d import (
    Periodic2DTopologicalPhaseSweepCampaign,
    Periodic2DTopologicalPhaseSweepCampaignModel,
)
from ksdft2effmass.campaigns.research_monograph.periodic2d.run import (
    topological_phase_sweep,
)

Verifier = (
    topological_phase_sweep.verify.Periodic2DTopologicalPhaseSweepCampaignVerifier
)
pytestmark = [
    pytest.mark.integration,
    pytest.mark.numerical_verification,
    pytest.mark.expensive,
]


class TestPeriodic2DTopologicalPhaseSweepCampaign:
    """Own retained three-model phase-sweep evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[8]

    def campaign(
        self, result: bytes | None = None
    ) -> Periodic2DTopologicalPhaseSweepCampaign:
        """Construct a campaign from retained exact bytes."""
        base = self.root() / "calculations/research-monograph/periodic-2d"
        retained = (base / "topological-phase-sweep-result.json").read_bytes()
        return Periodic2DTopologicalPhaseSweepCampaign(
            Periodic2DTopologicalPhaseSweepCampaignModel(
                (base / "topological-phase-sweep-input.json").read_bytes(),
                retained if result is None else result,
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__correlate_and_verify__reproduces_every_sample(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-007.

        Requirement: Maintained and independent routes reproduce every sweep sample.
        Method: Correlate exact bytes and reconstruct projector Bargmann invariants.
        Oracle: Independent model-specific eigensystem and analytic-sector checks.
        Acceptance: Exact identity and all independent sample checks pass.
        Interpretation: This verifies bounded synthetic parameter sweeps.
        Limitations: It is not a material phase diagram or transition theorem.
        """
        campaign = self.campaign()
        correlation = campaign.correlate()
        verification = campaign.verify(repository_root=self.root())
        self.require(correlation.passes, "phase-sweep correlation failed")
        self.require(
            correlation.retained_sha256
            == "298532cba30f56518c6578feb187704ad8f031eabdeae468b7ad067d0b286b11",
            "retained identity mismatch",
        )
        self.require(verification.passes, "phase-sweep verification failed")

    def test_contract__verifier__is_independent_and_corruption_sensitive(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-008.

        Requirement: Verification is maintained-route independent and sensitive.
        Method: Inspect imports and mutate one retained Chern value.
        Oracle: Independent projector Bargmann reconstruction.
        Acceptance: No calculation import and mutation is rejected.
        Interpretation: This verifies route separation and sensitivity.
        Limitations: Import inspection does not prove scientific independence.
        """
        tree = ast.parse(Path(inspect.getfile(Verifier)).read_text())
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.require(
            not any(
                "calculate" in module or "toy_models" in module for module in modules
            ),
            "verifier imports maintained route",
        )
        retained = self.campaign().model.result_payload
        marker = b'"retained_chern": -1.0'
        mutated = retained.replace(marker, b'"retained_chern": -0.5', 1)
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())
