"""Software verification of the direct Mathieu1D public surface."""

from __future__ import annotations

import importlib

import pytest

import ksdft2effmass.model_systems as model_systems
import ksdft2effmass.model_systems.mathieu1d as mathieu1d
from ksdft2effmass.model_systems.mathieu1d.analysis import (
    Mathieu1dAnalysisRequest,
    Mathieu1dAnalyzer,
)
from ksdft2effmass.model_systems.mathieu1d.configuration import Mathieu1dConfiguration
from ksdft2effmass.model_systems.mathieu1d.result import Mathieu1dCalculationResult
from ksdft2effmass.model_systems.mathieu1d.verification import Mathieu1dVerifier
from ksdft2effmass.model_systems.mathieu1d.verification_values import (
    Mathieu1dVerification,
)
from ksdft2effmass.model_systems.mathieu1d.visualizations import (
    Mathieu1dVisualizationData,
    Mathieu1dVisualizer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestMathieu1dPublicSurface:
    """Verify direct ownership and complete predecessor removal."""

    def test_public_api__direct_classes__are_owner_classes(self) -> None:
        """Both supported package roots expose the direct owner classes."""
        expected = {
            "Mathieu1dAnalysisRequest": Mathieu1dAnalysisRequest,
            "Mathieu1dAnalyzer": Mathieu1dAnalyzer,
            "Mathieu1dCalculationResult": Mathieu1dCalculationResult,
            "Mathieu1dConfiguration": Mathieu1dConfiguration,
            "Mathieu1dVerification": Mathieu1dVerification,
            "Mathieu1dVerifier": Mathieu1dVerifier,
            "Mathieu1dVisualizationData": Mathieu1dVisualizationData,
            "Mathieu1dVisualizer": Mathieu1dVisualizer,
        }
        for name, owner in expected.items():
            assert getattr(mathieu1d, name) is owner
            assert getattr(model_systems, name) is owner
        assert not hasattr(Mathieu1dAnalyzer, "calculate")

    def test_public_api__legacy_study_exports__are_absent(self) -> None:
        """No supported package root retains a predecessor study symbol."""
        former = {
            "Mathieu1dStudyDefinition",
            "Mathieu1dStudyEvaluator",
            "Mathieu1dStudyInputDeserializer",
            "Mathieu1dStudyInputSerializer",
            "Mathieu1dStudyResult",
            "Mathieu1dStudyResultSerializer",
            "Mathieu1dStudyVerificationResult",
            "Mathieu1dStudyVerificationSerializer",
            "Mathieu1dStudyVerifier",
        }
        assert former.isdisjoint(mathieu1d.__all__)
        assert former.isdisjoint(model_systems.__all__)
        assert all(not hasattr(mathieu1d, name) for name in former)
        assert all(not hasattr(model_systems, name) for name in former)

    def test_import__legacy_study_package__is_absent(self) -> None:
        """The predecessor package is recoverable from Git but not importable."""
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("ksdft2effmass.model_systems.mathieu1d.study")
