"""Public-import evidence for the periodic-1D namespace migration."""

import importlib
import sys

import pytest

from ksdft2effmass.campaigns import periodic_1d as canonical


@pytest.mark.integration
class TestPeriodic1DLegacyImport:
    """Own canonical-route and deprecated-façade compatibility evidence."""

    def test_contract__deprecated_facade__warns_and_preserves_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-033.

        Requirement: The publication-owned route is deprecated without duplicating
        public class definitions.
        Method: Import the legacy façade under warning capture and compare exports.
        Oracle: The canonical ``campaigns.periodic_1d`` package.
        Acceptance: A deprecation warning is emitted and representative classes are
        identical objects with the same ordered explicit export list.
        Interpretation: Existing root-level imports remain compatible during migration.
        Limitations: Unsupported deep implementation-module imports are not preserved.
        """
        module_name = "ksdft2effmass.campaigns.research_monograph.periodic_1d"
        sys.modules.pop(module_name, None)
        with pytest.warns(
            DeprecationWarning,
            match=r"campaigns\.research_monograph\.periodic_1d is deprecated",
        ):
            importlib.import_module(module_name)

        from ksdft2effmass.campaigns.research_monograph import (
            periodic_1d as legacy,
        )

        if legacy.__all__ != canonical.__all__:
            raise AssertionError("legacy and canonical export lists disagree")
        if (
            legacy.Periodic1DCompositeCampaign
            is not canonical.Periodic1DCompositeCampaign
        ):
            raise AssertionError("composite campaign identity changed")
        if (
            legacy.Periodic1DWannier90Integration
            is not canonical.Periodic1DWannier90Integration
        ):
            raise AssertionError("Wannier90 integration identity changed")
        if (
            legacy.Periodic1DHoppingReductionWorkflow
            is not canonical.Periodic1DHoppingReductionWorkflow
        ):
            raise AssertionError("hopping reduction identity changed")
