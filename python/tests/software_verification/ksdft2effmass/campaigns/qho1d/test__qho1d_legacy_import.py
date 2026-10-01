"""Public-import evidence for the QHO1D namespace migration."""

import importlib
import sys

import pytest

from ksdft2effmass.campaigns import qho1d as canonical


@pytest.mark.integration
class TestQho1DLegacyImport:
    """Own canonical-route and deprecated-façade compatibility evidence."""

    def test_contract__deprecated_facade__warns_and_preserves_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-QHO-ONE-D-001.

        Requirement: The publication-owned route is deprecated without duplicating
        public class definitions.
        Method: Import the legacy façade under warning capture and compare exports.
        Oracle: The canonical ``campaigns.qho1d`` package.
        Acceptance: A deprecation warning is emitted and representative classes are
        identical objects with the same ordered explicit export list.
        Interpretation: Existing root-level imports remain compatible during migration.
        Limitations: Unsupported deep implementation-module imports are not preserved.
        """
        module_name = "ksdft2effmass.campaigns.research_monograph.harmonic_oscillator"
        sys.modules.pop(module_name, None)
        with pytest.warns(
            DeprecationWarning,
            match=r"campaigns\.research_monograph\.harmonic_oscillator is deprecated",
        ):
            importlib.import_module(module_name)

        from ksdft2effmass.campaigns import research_monograph as legacy_root
        from ksdft2effmass.campaigns.research_monograph import (
            harmonic_oscillator as legacy,
        )

        if legacy.__all__ != canonical.__all__:
            raise AssertionError("legacy and canonical export lists disagree")
        if (
            legacy.HarmonicOscillatorStudyDefinition
            is not canonical.HarmonicOscillatorStudyDefinition
        ):
            raise AssertionError("study-definition identity changed")
        if (
            legacy.HarmonicOscillatorStudyEvaluator
            is not canonical.HarmonicOscillatorStudyEvaluator
        ):
            raise AssertionError("study-evaluator identity changed")
        if (
            legacy.HarmonicOscillatorResultVerifier
            is not canonical.HarmonicOscillatorResultVerifier
        ):
            raise AssertionError("result-verifier identity changed")
        if (
            legacy_root.HarmonicOscillatorStudyResultSerializer
            is not canonical.HarmonicOscillatorStudyResultSerializer
        ):
            raise AssertionError("research-monograph root identity changed")
