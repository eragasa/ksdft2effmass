"""Project-specific scientific campaign composition.

Canonical campaign packages are organized by scientific capability rather than by
publication artifact. Campaigns bind explicit inputs to analysis, calculator, and
Workflow contracts without owning their generic behavior or deciding scientific
acceptance. ``research_monograph`` remains a bounded owner for monograph-specific
composition and retained root imports; it is not a namespace pattern for new
campaigns. The periodic2d capability lives at :mod:`ksdft2effmass.periodic2d`.
"""

from . import model_adequacy, periodic_1d, periodic_reduction, research_monograph

__all__ = [
    "model_adequacy",
    "periodic_1d",
    "periodic_reduction",
    "research_monograph",
]
