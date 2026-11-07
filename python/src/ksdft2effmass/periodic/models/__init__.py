"""Dimension-neutral periodic scientific-model API."""

from .base import PeriodicModel, PeriodicModelRole, SpatialDimension
from .block_hopping import PeriodicBlockHoppingModel, PeriodicRank2BlockHoppingModel

__all__ = [
    "PeriodicBlockHoppingModel",
    "PeriodicModel",
    "PeriodicModelRole",
    "PeriodicRank2BlockHoppingModel",
    "SpatialDimension",
]
