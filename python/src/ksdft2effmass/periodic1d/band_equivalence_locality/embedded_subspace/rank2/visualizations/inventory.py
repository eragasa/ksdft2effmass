"""Closed authenticated figure inventories for embedded rank-two analyses."""

from enum import Enum


class Periodic1DEmbeddedSubspaceRank2CalculationVisualizationPlot(Enum):
    """Identify every required aggregate refinement and truncation figure."""

    MOMENTUM_REFINEMENT = "embedded-rank2-momentum-refinement.png"
    ADAPTIVE_AMPLITUDE_REFINEMENT = "embedded-rank2-adaptive-amplitude-refinement.png"
    TRUNCATION_CONSEQUENCES = "embedded-rank2-truncation-consequences.png"


class Periodic1DEmbeddedSubspaceRank2VisualizationPlot(Enum):
    """Identify every required single-parent embedded figure."""

    BAND_AND_ALIGNMENT = "embedded-rank2-band-and-alignment.png"
    LOCALITY = "embedded-rank2-locality.png"
    NUMERICAL_RESIDUALS = "embedded-rank2-numerical-residuals.png"


class Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationPlot(Enum):
    """Identify every required parent-family figure."""

    ALIGNMENT_LANDSCAPE = "embedded-rank2-family-alignment-landscape.png"
    LOCALITY_LANDSCAPE = "embedded-rank2-family-locality-landscape.png"
    QUALIFICATION = "embedded-rank2-family-qualification.png"


__all__ = [
    "Periodic1DEmbeddedSubspaceRank2CalculationVisualizationPlot",
    "Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationPlot",
    "Periodic1DEmbeddedSubspaceRank2VisualizationPlot",
]
