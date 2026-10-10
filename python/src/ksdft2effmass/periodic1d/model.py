"""Canonical scientific models for one-dimensional periodic studies."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic import Periodic1DModel, PeriodicModelRole


@dataclass(frozen=True, slots=True)
class Periodic1DFourierHamiltonianToyModel(Periodic1DModel):
    r"""Define a toy Hamiltonian with a finite real Fourier potential.

    The represented Bloch fibers use ``recoil_energy`` to scale the dimensionless
    kinetic term :math:`(k+n)^2`.  ``reciprocal_vector`` supplies the reciprocal
    coordinate unit and must be dual to the period carried by ``potential``.

    Parameters
    ----------
    identity
        Stable nonempty model identity.  This is a model identity, not a run or
        retained-document identity.
    potential
        Real periodic Fourier potential and direct-lattice period.
    reciprocal_vector
        Positive reciprocal period :math:`2\pi/a`.
    recoil_energy
        Positive kinetic-energy scale and energy unit for represented fibers.
    duality_absolute_tolerance
        Nonnegative absolute tolerance in the magnitude convention of
        ``reciprocal_vector`` used only to validate direct/reciprocal duality.
    """

    identity: str
    potential: PeriodicFourierPotential1D
    reciprocal_vector: ScalarQuantity
    recoil_energy: ScalarQuantity
    duality_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate identity, units, positivity, and direct/reciprocal duality."""
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if not self.identity:
            raise ValueError("identity must be nonempty")
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(self.reciprocal_vector) is not ScalarQuantity:
            raise TypeError("reciprocal_vector must be ScalarQuantity")
        if self.reciprocal_vector.magnitude <= 0.0:
            raise ValueError("reciprocal_vector must be positive")
        if type(self.recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if self.recoil_energy.magnitude <= 0.0:
            raise ValueError("recoil_energy must be positive")
        if type(self.duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.duality_absolute_tolerance)
            or self.duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.potential.constant_coefficient.unit, self.recoil_energy.unit
        ):
            raise ValueError("potential and recoil_energy units must be compatible")
        expected = self.potential.reciprocal_period_in(self.reciprocal_vector)
        if not np.isclose(
            self.reciprocal_vector.magnitude,
            expected,
            rtol=0.0,
            atol=self.duality_absolute_tolerance,
        ):
            raise ValueError("reciprocal_vector must be dual to the potential period")

    @property
    def model_id(self) -> str:
        """Return the stable scientific-model identity."""
        return self.identity

    @property
    def model_role(self) -> PeriodicModelRole:
        """Classify this controlled Fourier Hamiltonian as a toy model."""
        return PeriodicModelRole.TOY



__all__ = ["Periodic1DFourierHamiltonianToyModel"]
