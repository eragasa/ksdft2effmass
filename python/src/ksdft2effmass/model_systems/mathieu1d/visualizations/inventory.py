"""Closed Mathieu1D figure inventory."""

from enum import Enum


class Mathieu1dVisualizationPlotEnum(Enum):
    """Declare the closed native Mathieu1D plot inventory.

    Attributes
    ----------
    finite_reduction
        Four-panel representation, band, hopping, and range diagnostic figure.
    publication_summary
        Compact two-panel range-error and omitted-norm figure.
    """

    finite_reduction = "mathieu1d-finite-reduction.png"
    publication_summary = "mathieu1d-publication-summary.png"
