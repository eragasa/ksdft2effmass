"""Retained evidence for the periodic-2D composite campaign."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic2d import (
    Periodic2DCompositeCampaign,
    Periodic2DCompositeCampaignModel,
)
from ksdft2effmass.campaigns.research_monograph.periodic2d.run.composite.verify import (
    Periodic2DCompositeCampaignVerifier,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.numerical_verification,
    pytest.mark.expensive,
]


class TestPeriodic2DCompositeCampaign:
    """Own composite correlation, reconstruction, and independence evidence."""

    @staticmethod
    def root() -> Path:
        """Return the retained repository root."""
        return Path(__file__).resolve().parents[8]

    def campaign(self, result: bytes | None = None) -> Periodic2DCompositeCampaign:
        """Build a campaign from exact retained documents."""
        base = self.root() / "calculations/research-monograph/periodic-2d"
        retained = (base / "composite-result.json").read_bytes()
        return Periodic2DCompositeCampaign(
            Periodic2DCompositeCampaignModel(
                (base / "composite-input.json").read_bytes(),
                retained if result is None else result,
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__correlate_and_verify__reproduces_composite_gauges(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-003.

        Requirement: Maintained and independent routes reproduce the rank-three result.
        Method: Correlate bytes and independently reconstruct both gauge routes.
        Oracle: Independent polar projection, hopping, topology, and density routes.
        Acceptance: Exact identity and all reconstruction checks pass.
        Interpretation: This is bounded synthetic numerical verification.
        Limitations: It is not material validation or a localization theorem.
        """
        campaign = self.campaign()
        correlation = campaign.correlate()
        verification = campaign.verify(repository_root=self.root())
        self.require(correlation.passes, "composite correlation failed")
        self.require(
            correlation.retained_sha256
            == "2bd97c1138e501e0b26f19dd43b3bb1718dc6e4655804f6bc96e853c7fd87792",
            "result identity mismatch",
        )
        self.require(verification.passes, "composite verification failed")

    def test_contract__verifier__is_independent_and_rejects_corruption(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-004.

        Requirement: Verification is implementation-independent and
        corruption-sensitive.
        Method: Inspect imports and mutate the retained minimum gap.
        Oracle: Independent finite plane-wave reconstruction.
        Acceptance: No maintained constructor import and mutation is rejected.
        Interpretation: A pass verifies route separation and sensitivity.
        Limitations: Static imports do not establish independent physical evidence.
        """
        tree = ast.parse(
            Path(inspect.getfile(Periodic2DCompositeCampaignVerifier)).read_text()
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
        marker = b'"minimum_composite_to_exterior_gap": '
        start = retained.find(marker)
        begin = start + len(marker)
        end = retained.find(b"\n", begin)
        mutated = retained[:begin] + b"0.5," + retained[end:]
        with pytest.raises((ValueError, AssertionError)):
            self.campaign(mutated).verify(repository_root=self.root())
