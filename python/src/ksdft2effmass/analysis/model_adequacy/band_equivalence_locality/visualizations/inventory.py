"""Closed baseline plot inventory for band-equivalence locality."""

from ksdft2effmass.serialization import StringWireEnum


class BandEquivalenceLocalityVisualizationPlotEnum(StringWireEnum):
    """Name the single authenticated baseline plot."""

    LOCALITY_REQUIREMENTS = "band-equivalence-locality-requirements.png"


__all__ = ["BandEquivalenceLocalityVisualizationPlotEnum"]
