"""Lightweight common identity for periodic two-dimensional campaigns.

The base class records only the spatial dimension shared by every periodic2d
campaign. Campaign-specific models, correlation, verification, numerical policy,
and retained-wire behavior remain with concrete campaign owners.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class Periodic2DCampaign:
    """Represent the common dimensional identity of a periodic2d campaign.

    This deliberately small DataObject supplies a nominal common type for concrete
    periodic2d campaigns without prescribing their models, requests, results,
    tolerances, serializers, or execution behavior.

    Notes
    -----
    Inheriting from this class establishes software organization only. It does not
    establish compatibility between campaign models, represented state spaces,
    numerical methods, retained artifacts, or scientific acceptance criteria.
    """

    @property
    def spatial_dimension(self) -> Literal[2]:
        """Return the exact periodic spatial dimension represented by the campaign."""
        return 2
