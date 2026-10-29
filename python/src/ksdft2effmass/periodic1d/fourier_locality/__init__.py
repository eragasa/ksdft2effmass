"""Compatible rank-one finite Fourier-locality scientific contracts.

The package exposes the exact immutable configuration, direct calculation action,
correlated finite result records, independent byte-owning verification, authenticated
visualization projection, and closed renderer. It does not create or promote an
execution package.
"""

from .analysis import Periodic1DFourierLocalityAnalyzer
from .configuration import Periodic1DFourierLocalityConfiguration
from .result import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityEvaluationResult,
    Periodic1DFourierLocalityMeshResult,
    Periodic1DFourierLocalityRangeResult,
)
from .verification import (
    FourierLocalityVerification,
    Periodic1DFourierLocalityVerification,
    Periodic1DFourierLocalityVerifier,
)
from .verification_values import (
    Periodic1DFourierLocalityIndependentVerification,
    Periodic1DFourierLocalityIndependentVerificationRequest,
    Periodic1DFourierLocalityIndependentVerifier,
)
from .visualizations import (
    Periodic1DFourierLocalityVisualizationData,
    Periodic1DFourierLocalityVisualizationPlotEnum,
    Periodic1DFourierLocalityVisualizer,
)

__all__ = [
    "Periodic1DFourierLocalityAnalyzer",
    "Periodic1DFourierLocalityCalculationResult",
    "Periodic1DFourierLocalityConfiguration",
    "Periodic1DFourierLocalityEvaluationResult",
    "Periodic1DFourierLocalityMeshResult",
    "FourierLocalityVerification",
    "Periodic1DFourierLocalityIndependentVerification",
    "Periodic1DFourierLocalityIndependentVerificationRequest",
    "Periodic1DFourierLocalityIndependentVerifier",
    "Periodic1DFourierLocalityRangeResult",
    "Periodic1DFourierLocalityVerification",
    "Periodic1DFourierLocalityVerifier",
    "Periodic1DFourierLocalityVisualizationData",
    "Periodic1DFourierLocalityVisualizationPlotEnum",
    "Periodic1DFourierLocalityVisualizer",
]
