"""Public-import evidence for the PIAB1D namespace migration."""

import importlib
import sys

import pytest

from ksdft2effmass.campaigns import piab1d as canonical


@pytest.mark.integration
class TestPiab1DLegacyImport:
    """Own canonical-route and deprecated-façade compatibility evidence."""

    def test_contract__deprecated_facade__warns_and_preserves_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PIAB-ONE-D-001.

        Requirement: The publication-owned route is deprecated without duplicating
        public class definitions.
        Method: Import the legacy façade under warning capture and compare exports.
        Oracle: The canonical ``campaigns.piab1d`` package.
        Acceptance: A deprecation warning is emitted and representative classes are
        identical objects with the same ordered explicit export list.
        Interpretation: Existing root-level imports remain compatible during migration.
        Limitations: Unsupported deep implementation-module imports are not preserved.
        """
        module_name = "ksdft2effmass.campaigns.research_monograph.particle_in_box"
        sys.modules.pop(module_name, None)
        with pytest.warns(
            DeprecationWarning,
            match=r"campaigns\.research_monograph\.particle_in_box is deprecated",
        ):
            importlib.import_module(module_name)

        from ksdft2effmass.campaigns import research_monograph as legacy_root
        from ksdft2effmass.campaigns.research_monograph import (
            particle_in_box as legacy,
        )

        if legacy.__all__ != canonical.__all__:
            raise AssertionError("legacy and canonical export lists disagree")
        if (
            legacy.ParticleInBoxStudyDefinition
            is not canonical.ParticleInBoxStudyDefinition
        ):
            raise AssertionError("study-definition identity changed")
        if (
            legacy.ParticleInBoxResidualStudyEvaluator
            is not canonical.ParticleInBoxResidualStudyEvaluator
        ):
            raise AssertionError("residual-study evaluator identity changed")
        if (
            legacy.ParticleInBoxIdentifiabilityWorkflow
            is not canonical.ParticleInBoxIdentifiabilityWorkflow
        ):
            raise AssertionError("identifiability workflow identity changed")
        if (
            legacy_root.ParticleInBoxResultVerifier
            is not canonical.ParticleInBoxResultVerifier
        ):
            raise AssertionError("research-monograph root identity changed")
