"""Project-specific scientific campaign composition.

Canonical campaign packages are organized by scientific capability rather than by
publication artifact. Campaigns bind explicit inputs to analysis, calculator, and
Workflow contracts without owning their generic behavior or deciding scientific
acceptance.
"""

from . import periodic2d, periodic_1d, piab1d, qho1d, research_monograph

__all__ = ["periodic_1d", "periodic2d", "piab1d", "qho1d", "research_monograph"]
