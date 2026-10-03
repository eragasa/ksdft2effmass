"""Project-specific scientific campaign composition.

Canonical campaign packages are organized by scientific capability rather than by
publication artifact. Campaigns bind explicit inputs to analysis, calculator, and
Workflow contracts without owning their generic behavior or deciding scientific
acceptance. The periodic2d capability now lives at
:mod:`ksdft2effmass.periodic2d`; the former campaigns subpackage was removed during
the alpha namespace migration.
"""

from . import periodic_1d, piab1d, qho1d, research_monograph
from .serialization import CampaignJsonDecoder

__all__ = [
    "CampaignJsonDecoder",
    "periodic_1d",
    "piab1d",
    "qho1d",
    "research_monograph",
]
