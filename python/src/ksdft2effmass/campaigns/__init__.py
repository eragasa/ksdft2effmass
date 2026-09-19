"""Project-specific scientific campaign composition.

The public :mod:`ksdft2effmass.campaigns.research_monograph` subpackage owns exact
research-monograph study definitions and retained-format adapters. Campaigns bind
explicit inputs to analysis, calculator, and Workflow contracts without owning their
generic behavior or deciding scientific acceptance.
"""

from . import research_monograph

__all__ = ["research_monograph"]
