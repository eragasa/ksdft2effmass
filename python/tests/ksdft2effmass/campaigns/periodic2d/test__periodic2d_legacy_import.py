"""Public-import evidence for the periodic-2D namespace migration."""

import importlib
import sys

import pytest

from ksdft2effmass.campaigns import periodic2d as canonical


@pytest.mark.integration
class TestPeriodic2DLegacyImport:
    """Own canonical-route and deprecated-façade compatibility evidence."""

    def test_contract__deprecated_facade__warns_and_preserves_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-009.

        Requirement: The publication-owned route is deprecated without duplicating
        public class definitions.
        Method: Import the legacy façade under warning capture and compare exports.
        Oracle: The canonical ``campaigns.periodic2d`` package.
        Acceptance: A deprecation warning is emitted and representative classes are
        identical objects with the same explicit export set.
        Interpretation: Existing root-level imports remain compatible during migration.
        Limitations: Unsupported deep implementation-module imports are not preserved.
        """
        module_name = "ksdft2effmass.campaigns.research_monograph.periodic2d"
        sys.modules.pop(module_name, None)
        with pytest.warns(
            DeprecationWarning,
            match=r"campaigns\.research_monograph\.periodic2d is deprecated",
        ):
            importlib.import_module(module_name)

        from ksdft2effmass.campaigns.research_monograph import (
            periodic2d as legacy,
        )

        if legacy.__all__ != canonical.__all__:
            raise AssertionError("legacy and canonical export sets disagree")
        if (
            legacy.Periodic2DCompositeCampaign
            is not canonical.Periodic2DCompositeCampaign
        ):
            raise AssertionError("composite campaign identity changed")
        if legacy.Periodic2DDefect is not canonical.Periodic2DDefect:
            raise AssertionError("defect identity changed")
        if (
            legacy.Periodic2DOptimizerRegressionCampaign
            is not canonical.Periodic2DOptimizerRegressionCampaign
        ):
            raise AssertionError("optimizer regression identity changed")
