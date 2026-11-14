"""KSD-owned diamond ``sp3s*`` composition over Project Koios PhysKit.

This package retains the concrete diamond geometry, onsite and shell parameter
inventory, KSD represented-basis correlation, wire contract, and silicon-program
meaning. Reusable basis, bond, seven-channel hopping, cell assembly, linear channel
parameterization, reciprocal evaluation, Bloch, and orbital-center gauge mechanics are
consumed from PhysKit.

No fit, material adequacy, evidence promotion, or scientific acceptance is performed.
"""

from .geometry import (
    DiamondNeighborBond,
    DiamondSp3sStarGeometry,
    DiamondSublattice,
)
from .model import (
    DiamondSp3sStarBlochHamiltonianEvaluation,
    DiamondSp3sStarModel,
)
from .parameters import (
    DiamondSp3sStarFirstNeighbor,
    DiamondSp3sStarOnsite,
    DiamondSp3sStarParameters,
    DiamondSp3sStarSecondNeighbor,
)
from .serialization import DiamondSp3sStarModelJsonSerializer

__all__ = [
    "DiamondNeighborBond",
    "DiamondSp3sStarBlochHamiltonianEvaluation",
    "DiamondSp3sStarFirstNeighbor",
    "DiamondSp3sStarGeometry",
    "DiamondSp3sStarModel",
    "DiamondSp3sStarModelJsonSerializer",
    "DiamondSp3sStarOnsite",
    "DiamondSp3sStarParameters",
    "DiamondSp3sStarSecondNeighbor",
    "DiamondSublattice",
]
