"""Closed flat-parent band-equivalence locality figure inventory."""

from enum import Enum


class Periodic1DBandEquivalenceLocalityVisualizationPlotEnum(Enum):
    """Declare the closed three-figure output inventory."""

    ALIGNMENT = "rank2-flat-band-equivalence-alignment.png"
    LOCALITY = "rank2-flat-band-equivalence-locality.png"
    ERROR_CHANNELS = "rank2-flat-band-equivalence-error-channels.png"


__all__ = ["Periodic1DBandEquivalenceLocalityVisualizationPlotEnum"]
