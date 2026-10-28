"""Canonical scientific models for one-dimensional periodic studies."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import ModelSystemUnitConverter, ScalarQuantity

from ksdft2effmass.periodic import Periodic1DModel, PeriodicModelRole
from ksdft2effmass.solidstate import BlockHoppingModel1D


@dataclass(frozen=True, slots=True)
class Periodic1DBlockHamiltonianToyModel(Periodic1DModel):
    """Define a finite-range matrix-valued periodic toy Hamiltonian.

    The parent Bloch matrix is the exact finite sum represented by
    ``hopping_model``.  The supplied blocks must cover every opposite
    representative and satisfy :math:`T_{-R}=T_R^\\dagger` within the declared
    energy tolerance.  This model describes a parent representation; selecting
    and aligning a retained band group remain separate calculation operations.
    """

    identity: str
    hopping_model: BlockHoppingModel1D
    hermiticity_absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate identity, matrix-valued parent data, and Hermiticity."""
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if not self.identity:
            raise ValueError("identity must be nonempty")
        if type(self.hopping_model) is not BlockHoppingModel1D:
            raise TypeError("hopping_model must be BlockHoppingModel1D")
        if type(self.hermiticity_absolute_tolerance) is not ScalarQuantity:
            raise TypeError("hermiticity_absolute_tolerance must be ScalarQuantity")
        if self.hermiticity_absolute_tolerance.magnitude < 0.0:
            raise ValueError("hermiticity_absolute_tolerance must be nonnegative")
        block_unit = self.hopping_model.hopping_blocks[0].unit
        if not ModelSystemUnitConverter.compatible(
            self.hermiticity_absolute_tolerance.unit, block_unit
        ):
            raise ValueError("Hermiticity tolerance must use energy dimensions")
        tolerance = ModelSystemUnitConverter.convert_scalar(
            self.hermiticity_absolute_tolerance, block_unit
        )
        blocks = dict(
            zip(
                self.hopping_model.representatives,
                self.hopping_model.hopping_blocks,
                strict=True,
            )
        )
        for representative, block in blocks.items():
            opposite = blocks.get(-representative)
            if opposite is None:
                raise ValueError("every parent hopping must have an opposite block")
            defect = float(
                np.linalg.norm(block.magnitude - opposite.magnitude.conj().T)
            )
            if defect > tolerance.magnitude:
                raise ValueError("parent hopping blocks exceed Hermiticity tolerance")

    @property
    def model_id(self) -> str:
        """Return the stable scientific-model identity."""
        return self.identity

    @property
    def model_role(self) -> PeriodicModelRole:
        """Classify this controlled block Hamiltonian as a toy model."""
        return PeriodicModelRole.TOY


__all__ = ["Periodic1DBlockHamiltonianToyModel"]
