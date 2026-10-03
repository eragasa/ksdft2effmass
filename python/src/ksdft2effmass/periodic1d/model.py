"""Complete one-dimensional periodic Fourier scientific toy models."""

from __future__ import annotations

from dataclasses import dataclass, field

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic import Periodic1DModel, PeriodicModelRole


@dataclass(frozen=True, slots=True, init=False)
class Periodic1DFourierHamiltonianToyModel(Periodic1DModel):
    r"""Represent a complete quadratic-kinetic periodic Fourier toy parent.

    The modeled one-dimensional parent has Bloch-fiber matrix elements

    .. math::

       H_{nm}(k) = E_G (k+n)^2\delta_{nm} + V_{n-m},

    where ``potential`` defines the period, Fourier coefficients, and coefficient
    energy unit; ``recoil_energy`` is the positive scalar :math:`E_G`; and ``k`` is
    reduced momentum in the closed primitive interval ``[-0.5, 0.5]``. This record
    identifies the untruncated parent law, not a finite plane-wave representation.

    Parameters
    ----------
    model_id
        Stable nonempty configured-parent identity.
    state_space_id
        Stable nonempty identity of the parent Bloch state-space family.
    reciprocal_domain_id
        Stable nonempty identity of the primitive reduced reciprocal domain.
    potential
        Real finite Fourier potential, including its period and energy convention.
    recoil_energy
        Positive kinetic energy scale compatible with the potential coefficients.

    Raises
    ------
    TypeError
        If an identity or composed scientific value has the wrong exact type.
    ValueError
        If an identity is empty, recoil energy is not positive, or potential and
        recoil-energy units are incompatible.

    Notes
    -----
    Nominal membership and the exact ``TOY`` role classify scientific ownership and
    evidentiary purpose. They do not establish material realism, completeness of a
    parent electronic-structure calculation, scientific validation, or uncertainty
    quantification.
    """

    _model_id: str = field(repr=False)
    state_space_id: str
    reciprocal_domain_id: str
    potential: PeriodicFourierPotential1D
    recoil_energy: ScalarQuantity

    def __init__(
        self,
        model_id: str,
        state_space_id: str,
        reciprocal_domain_id: str,
        potential: PeriodicFourierPotential1D,
        recoil_energy: ScalarQuantity,
    ) -> None:
        """Store and validate the complete parent definition."""
        object.__setattr__(self, "_model_id", model_id)
        object.__setattr__(self, "state_space_id", state_space_id)
        object.__setattr__(self, "reciprocal_domain_id", reciprocal_domain_id)
        object.__setattr__(self, "potential", potential)
        object.__setattr__(self, "recoil_energy", recoil_energy)
        self.__post_init__()

    def __post_init__(self) -> None:
        """Validate identities, exact component types, scale, and units."""
        for name, value in (
            ("model_id", self.model_id),
            ("state_space_id", self.state_space_id),
            ("reciprocal_domain_id", self.reciprocal_domain_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(self.recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if self.recoil_energy.magnitude <= 0.0:
            raise ValueError("recoil_energy must be positive")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.potential.constant_coefficient.unit, self.recoil_energy.unit
        ):
            raise ValueError("potential and recoil-energy units must be compatible")

    @property
    def model_id(self) -> str:
        """Return the stable configured-parent identity."""
        return self._model_id

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the exact toy-model evidentiary role."""
        return PeriodicModelRole.TOY


__all__ = ["Periodic1DFourierHamiltonianToyModel"]
