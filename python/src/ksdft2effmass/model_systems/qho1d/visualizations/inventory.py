"""Closed QHO1D figure inventory."""

from enum import Enum


class Qho1dVisualizationPlotEnum(Enum):
    """Enumerate the closed direct QHO1D figure inventory."""

    eigenstates = "qho1d-eigenstates.png"
    eigenstate_distortion = "qho1d-eigenstate-distortion.png"
    diagnostics = "qho1d-diagnostics.png"
