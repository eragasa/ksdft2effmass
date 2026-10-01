"""Portable evidence for the periodic-2D standalone optimizer study."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic2d import (
    Periodic2DOptimizerStandaloneCampaign,
    Periodic2DOptimizerStandaloneCampaignModel,
)
from ksdft2effmass.campaigns.research_monograph.periodic2d.run.wannier90.optimizer_basin.standalone.verify import (  # noqa: E501
    Periodic2DOptimizerStandaloneCampaignVerifier as Verifier,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


class TestPeriodic2DOptimizerStandaloneCampaign:
    """Own initial, continuation, basin, and negative-disposition evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[10]

    def campaign(
        self, result: bytes | None = None
    ) -> Periodic2DOptimizerStandaloneCampaign:
        """Construct a campaign from exact retained standalone documents."""
        base = (
            self.root() / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        retained = (base / "standalone-result.json").read_bytes()
        model = Periodic2DOptimizerStandaloneCampaignModel(
            (base / "standalone-study-proposal.json").read_bytes(),
            (base / "standalone-initial-gauges.json").read_bytes(),
            retained if result is None else result,
        )
        return Periodic2DOptimizerStandaloneCampaign(model)

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__verify__retains_all_initial_and_continuation_outcomes(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-017.

        Requirement: Every declared start and exact-checkpoint continuation is retained.
        Method: Reconstruct transitions, classifications, basin gates, and summaries.
        Oracle: Closed proposal and gauge design plus endpoint arithmetic.
        Acceptance: 256 starts, 120 continuations, 196 converged, and 60 stopped pass.
        Interpretation: This verifies the retained standalone negative result.
        Limitations: It neither replays native files nor proves optimizer completeness.
        """
        result = self.campaign().verify(repository_root=self.root())
        self.require(result.passes, "standalone verification failed")
        self.require(result.endpoint_count == 256, "endpoint count changed")
        self.require(result.continuation_count == 120, "continuation count changed")
        self.require(result.effective_converged_count == 196, "converged count changed")
        self.require(result.final_nonconverged_count == 60, "stopped count changed")
        self.require(
            result.retained_result_sha256
            == "add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a",
            "retained identity mismatch",
        )

    def test_contract__verifier__avoids_native_paths_and_rejects_corruption(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-018.

        Requirement: Portable verification avoids native paths and detects corruption.
        Method: Inspect imports and mutate the effective convergence count.
        Oracle: Independently accumulated endpoint statuses.
        Acceptance: No calculation-route import and mutation is rejected.
        Interpretation: This verifies portable scope and aggregate sensitivity.
        Limitations: Native Wannier90 outputs and archives remain unauthenticated.
        """
        source = Path(inspect.getfile(Verifier)).read_text()
        tree = ast.parse(source)
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.require(
            not any(
                "extract_standalone" in module or "verify_standalone" in module
                for module in modules
            ),
            "verifier imports calculation route",
        )
        self.require(
            'Path(self._string(endpoint["effective_run_root"]))' not in source,
            "verifier reads native run path",
        )
        retained = self.campaign().model.result_payload
        mutated = retained.replace(
            b'"effective_native_converged_count": 196',
            b'"effective_native_converged_count": 195',
            1,
        )
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())
