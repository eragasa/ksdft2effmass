"""Reusable Slater--Koster foundations.

The public surface currently owns a spinless, orthogonal, homopolar diamond
``sp3s*`` model with explicit eV/angstrom units, right-handed geometry, full-center
Bloch phases, first- and second-neighbor maps, and deterministic typed JSON.
It performs no fit and carries no semiconductor adequacy claim.
"""

from .geometry import (
    DiamondNeighborBond,
    DiamondSp3sStarGeometry,
    DiamondSublattice,
)
from .model import DiamondSp3sStarModel, Sp3sStarOrbitalIndex
from .parameters import (
    DiamondSp3sStarFirstNeighbor,
    DiamondSp3sStarOnsite,
    DiamondSp3sStarParameters,
    DiamondSp3sStarSecondNeighbor,
)
from .serialization import DiamondSp3sStarModelJsonSerializer

__all__ = [
    "DiamondNeighborBond",
    "DiamondSp3sStarFirstNeighbor",
    "DiamondSp3sStarGeometry",
    "DiamondSp3sStarModel",
    "DiamondSp3sStarModelJsonSerializer",
    "DiamondSp3sStarOnsite",
    "DiamondSp3sStarParameters",
    "DiamondSp3sStarSecondNeighbor",
    "DiamondSublattice",
    "Sp3sStarOrbitalIndex",
]
