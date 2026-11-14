"""Dimension-neutral periodic scientific-model API."""

from .base import PeriodicModel, PeriodicModelRole, SpatialDimension
from .block_hopping import PeriodicBlockHoppingModel

__all__ = [
    "PeriodicBlockHoppingModel",
    "PeriodicModel",
    "PeriodicModelRole",
    "SpatialDimension",
]
