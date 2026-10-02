"""Portable evidence for the periodic-2D optimizer reanalysis."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d import (
    Periodic2DOptimizerReanalysisCampaign,
    Periodic2DOptimizerReanalysisCampaignModel,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.verify import (  # noqa: E501
    Periodic2DOptimizerReanalysisCampaignVerifier as Verifier,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


class TestPeriodic2DOptimizerReanalysisCampaign:
    """Own spread decomposition, D4 basin, trace, and refinement evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[8]

    def campaign(
        self, result: bytes | None = None
    ) -> Periodic2DOptimizerReanalysisCampaign:
        """Construct a campaign from exact retained result documents."""
        base = (
            self.root() / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        retained = (base / "reanalysis-result.json").read_bytes()
        return Periodic2DOptimizerReanalysisCampaign(
            Periodic2DOptimizerReanalysisCampaignModel(
                (base / "result.json").read_bytes(),
                retained if result is None else result,
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__verify__reconstructs_retained_offline_diagnostics(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-015.

        Requirement: Offline diagnostics retain every endpoint and grid case.
        Method: Reconstruct spread sums, trace classes, D4 basins, and grid deltas.
        Oracle: Closed source records, stated rules, and repository estimator inputs.
        Acceptance: 72 endpoints and four refinement cases pass every check.
        Interpretation: This verifies retained post-hoc numerical diagnosis.
        Limitations: Native traces and wavefunctions are not independently replayed.
        """
        result = self.campaign().verify(repository_root=self.root())
        self.require(result.passes, "optimizer reanalysis verification failed")
        self.require(result.endpoint_count == 72, "endpoint count changed")
        self.require(result.refinement_case_count == 4, "refinement count changed")
        self.require(
            result.retained_result_sha256
            == "89780db50cb367f429a7947894805a89fbfc757f571a55f82936507ef397f38b",
            "retained identity mismatch",
        )

    def test_contract__verifier__avoids_native_paths_and_rejects_corruption(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-016.

        Requirement: Portable reanalysis avoids native files and detects corruption.
        Method: Inspect imports and mutate one retained aggregate classification count.
        Oracle: Independently accumulated endpoint classifications.
        Acceptance: No calculation-route import and mutation is rejected.
        Interpretation: This verifies portable scope and aggregate sensitivity.
        Limitations: It does not authenticate unavailable native artifacts.
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
                "reanalyze_study" in module or "verify_reanalysis" in module
                for module in modules
            ),
            "verifier imports calculation route",
        )
        self.require(
            'Path(self._string(start["source_analysis_result_path"]))' not in source,
            "verifier reads native analysis",
        )
        retained = self.campaign().model.result_payload
        mutated = retained.replace(
            b'"native_converged": 51', b'"native_converged": 50', 1
        )
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())
