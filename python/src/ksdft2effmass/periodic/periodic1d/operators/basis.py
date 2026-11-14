"""One-dimensional periodic basis identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from ksdft2effmass.periodic.operators.basis import PeriodicBasisIdentity


@dataclass(frozen=True, slots=True)
class Periodic1DBasisIdentity(PeriodicBasisIdentity):
    """Own an ordered basis identity for a one-dimensional periodic problem."""

    SPATIAL_DIMENSION: ClassVar[int] = 1

    @classmethod
    def _required_spatial_dimension(cls) -> int:
        return cls.SPATIAL_DIMENSION


__all__ = ["Periodic1DBasisIdentity"]
