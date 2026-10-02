"""Retained evidence for the periodic-2D topological benchmark."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d import (
    Periodic2DTopologicalCampaign,
    Periodic2DTopologicalCampaignModel,
)
from ksdft2effmass.periodic2d.run.topological import (
    verify as verification_module,
)

Periodic2DTopologicalCampaignVerifier = (
    verification_module.Periodic2DTopologicalCampaignVerifier
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.numerical_verification,
    pytest.mark.expensive,
]


class TestPeriodic2DTopologicalCampaign:
    """Own retained three-model topological benchmark evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[6]

    def campaign(self, result: bytes | None = None) -> Periodic2DTopologicalCampaign:
        """Construct the campaign from retained exact bytes."""
        base = self.root() / "calculations/research-monograph/periodic-2d"
        retained = (base / "topological-result.json").read_bytes()
        return Periodic2DTopologicalCampaign(
            Periodic2DTopologicalCampaignModel(
                (base / "topological-input.json").read_bytes(),
                retained if result is None else result,
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__correlate_and_verify__reproduces_three_models(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-005.

        Requirement: Maintained and independent routes reproduce all model cases.
        Method: Correlate exact bytes and independently rebuild projector invariants.
        Oracle: Separate QWZ, Hofstadter, and Haldane eigensystem routes.
        Acceptance: Exact identity and independent reconstruction pass.
        Interpretation: This verifies three controlled synthetic benchmarks.
        Limitations: It is not material validation or a general topology theorem.
        """
        campaign = self.campaign()
        correlation = campaign.correlate()
        verification = campaign.verify(repository_root=self.root())
        self.require(correlation.passes, "topological correlation failed")
        self.require(
            correlation.retained_sha256
            == "bd94c40a3b12f4f7ecb41009e86c936e456d09738176256f4e0d27ab9fdd959a",
            "retained identity mismatch",
        )
        self.require(verification.passes, "independent verification failed")

    def test_contract__verifier__is_independent_and_corruption_sensitive(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-006.

        Requirement: Verification remains separate and rejects changed Chern evidence.
        Method: Inspect imports and mutate one retained Chern value.
        Oracle: Independent projector Bargmann invariants and Wilson winding.
        Acceptance: No calculation import and the mutation is rejected.
        Interpretation: This verifies route separation and sensitivity.
        Limitations: Import inspection does not establish scientific independence.
        """
        tree = ast.parse(
            Path(inspect.getfile(Periodic2DTopologicalCampaignVerifier)).read_text()
        )
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
        mutated = retained.replace(
            b'"retained_chern": -1.0', b'"retained_chern": -0.5', 1
        )
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())
