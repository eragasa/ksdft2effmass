"""Software verification of the direct Mathieu1D public surface."""

from __future__ import annotations

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
    """Verify direct ownership of the maintained public surface."""

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
