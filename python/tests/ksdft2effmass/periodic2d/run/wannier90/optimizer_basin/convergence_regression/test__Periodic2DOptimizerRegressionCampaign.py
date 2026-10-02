"""Independent evidence for the censored optimizer regression."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d import (
    Periodic2DOptimizerRegressionCampaign,
    Periodic2DOptimizerRegressionCampaignModel,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.verify import (  # noqa: E501
    Periodic2DOptimizerRegressionCampaignVerifier as Verifier,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


class TestPeriodic2DOptimizerRegressionCampaign:
    """Own censored likelihood, clustered interval, and claim-boundary evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[8]

    def campaign(
        self, regression: bytes | None = None
    ) -> Periodic2DOptimizerRegressionCampaign:
        """Construct a campaign from exact retained standalone documents."""
        base = (
            self.root() / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        retained = (base / "standalone-convergence-regression.json").read_bytes()
        model = Periodic2DOptimizerRegressionCampaignModel(
            (base / "standalone-result.json").read_bytes(),
            (base / "analyze_standalone_convergence_regression.py").read_bytes(),
            retained if regression is None else regression,
        )
        return Periodic2DOptimizerRegressionCampaign(model)

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__verify__reconstructs_censored_regression(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-019.

        Requirement: Every stopped endpoint remains in the convergence-time model.
        Method: Rebuild design, likelihood, scores, covariance, ratios, and curves.
        Oracle: Declared log-normal right-censoring equations and retained endpoints.
        Acceptance: 256 observations include 196 events and 60 censored records.
        Interpretation: This verifies the retained exploratory regression numerically.
        Limitations: Intervals are neither causal nor physical uncertainty estimates.
        """
        result = self.campaign().verify(repository_root=self.root())
        self.require(result.passes, "censored regression verification failed")
        self.require(result.observation_count == 256, "observation count changed")
        self.require(result.converged_count == 196, "event count changed")
        self.require(result.right_censored_count == 60, "censored count changed")
        self.require(result.parameter_count == 32, "parameter count changed")
        self.require(
            result.retained_result_sha256
            == "572b5ca7fe73ebb1cee6d9334e9ad6cddddea446fad3d02dfaf88202096ced22",
            "retained identity mismatch",
        )

    def test_contract__verifier__is_independent_and_rejects_corruption(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-020.

        Requirement: Verification is independent of the maintained analyzer.
        Method: Inspect imports and mutate the retained censoring count.
        Oracle: Endpoint-derived event and censoring indicators.
        Acceptance: No analyzer import and mutation is rejected.
        Interpretation: This verifies calculation-route independence and sensitivity.
        Limitations: It does not refit an alternative statistical model.
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
                "analyze_standalone" in module or "verify_standalone" in module
                for module in modules
            ),
            "verifier imports maintained route",
        )
        retained = self.campaign().model.regression_payload
        mutated = retained.replace(
            b'"right_censored_count": 60', b'"right_censored_count": 59', 1
        )
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())
