"""Closed baseline plot inventory for band-equivalence locality."""

from ksdft2effmass.serialization import StrWireEnum


class BandEquivalenceHoppingLocalityVisualizationPlotEnum(StrWireEnum):
    """Name the single authenticated baseline plot."""

    LOCALITY_REQUIREMENTS = "band-equivalence-locality-requirements.png"


__all__ = ["BandEquivalenceHoppingLocalityVisualizationPlotEnum"]
