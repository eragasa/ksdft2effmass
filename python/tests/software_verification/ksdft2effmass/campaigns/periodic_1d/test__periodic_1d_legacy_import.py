"""Public-import evidence for the periodic-1D namespace migration."""

import importlib
import sys

import pytest

from ksdft2effmass.campaigns import periodic_1d as transitional
from ksdft2effmass.periodic1d import campaign as canonical_campaign


@pytest.mark.integration
class TestPeriodic1DLegacyImport:
    """Own transitional-route removal and remaining façade identity evidence."""

    def test_contract__deprecated_facade__warns_and_preserves_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-033.

        Requirement: The publication route remains deprecated, while moved isolated
        and composite families have no transitional or publication aliases.
        Method: Import the legacy façade under warning capture and compare its exports
        with the transitional package and canonical campaign inventory.
        Oracle: Rows 058--061 route-removal decisions and the remaining reusable
        hopping-workflow facade contract.
        Acceptance: A deprecation warning is emitted; moved names are absent from both
        former facades; and representative unmigrated classes retain identity.
        Interpretation: Family moves narrow old facades without duplicating owners.
        Limitations: This route test does not validate campaign bytes, calculations,
        numerical results, or scientific conclusions.
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

        composite_symbols = {
            name for name in canonical_campaign.__all__ if "Composite" in name
        }
        isolated_symbols = {
            name
            for name in canonical_campaign.__all__
            if "Isolated" in name
            or name.startswith("Periodic1DRangeEffectiveModel")
            or name == "Periodic1DReplaySourceCorrelation"
        }
        reduction_challenge_symbols = {
            name
            for name in canonical_campaign.__all__
            if name.startswith("Periodic1DReductionChallenge")
        }
        if not set(legacy.__all__) <= set(transitional.__all__):
            raise AssertionError(
                "legacy exports must remain within the transitional set"
            )
        if composite_symbols & set(legacy.__all__):
            raise AssertionError("deprecated façade preserved composite aliases")
        if composite_symbols & set(transitional.__all__):
            raise AssertionError("transitional package preserved composite aliases")
        if isolated_symbols & set(legacy.__all__):
            raise AssertionError("deprecated façade preserved isolated aliases")
        if isolated_symbols & set(transitional.__all__):
            raise AssertionError("transitional package preserved isolated aliases")
        if reduction_challenge_symbols & set(legacy.__all__):
            raise AssertionError(
                "deprecated façade preserved reduction-challenge aliases"
            )
        if reduction_challenge_symbols & set(transitional.__all__):
            raise AssertionError(
                "transitional package preserved reduction-challenge aliases"
            )
        if any(name.startswith("Periodic1DStress") for name in legacy.__all__):
            raise AssertionError("deprecated façade preserved former stress names")
        if any(name.startswith("Periodic1DStress") for name in transitional.__all__):
            raise AssertionError("transitional package preserved former stress names")
        wannier90_symbols = {
            name
            for name in canonical_campaign.__all__
            if name.startswith("Periodic1DWannier90")
        }
        if wannier90_symbols & set(legacy.__all__):
            raise AssertionError("deprecated façade preserved Wannier90 aliases")
        if wannier90_symbols & set(transitional.__all__):
            raise AssertionError("transitional package preserved Wannier90 aliases")
        if (
            legacy.Periodic1DHoppingReductionWorkflow
            is not transitional.Periodic1DHoppingReductionWorkflow
        ):
            raise AssertionError("hopping reduction identity changed")
