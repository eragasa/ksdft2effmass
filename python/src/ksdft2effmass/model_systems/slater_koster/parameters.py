"""Concrete silicon-program parameter composition over PhysKit integrals."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.solidstate.tb.slater_koster import (
    HomopolarSp3sStarTwoCenterIntegrals,
)
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity, UnitSystem

ELECTRON_VOLT = PhysicalUnit("electron_volt")

_PARAMETER_NAMES = (
    "E_s",
    "E_p",
    "E_s_star",
    "V1_ss_sigma",
    "V1_sp_sigma",
    "V1_pp_sigma",
    "V1_pp_pi",
    "V1_s_star_p_sigma",
    "V2_ss_sigma",
    "V2_sp_sigma",
    "V2_pp_sigma",
    "V2_pp_pi",
    "V2_s_star_p_sigma",
    "V2_s_s_star_sigma",
    "V2_s_star_s_star_sigma",
)


def _require_energy(value: ScalarQuantity, name: str) -> None:
    if type(value) is not ScalarQuantity:
        raise TypeError(f"{name} must be ScalarQuantity")
    if value.unit != ELECTRON_VOLT:
        raise ValueError(f"{name} must be in electron_volt")


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondSp3sStarOnsite:
    """Homopolar onsite energies in eV for ``(s, p_x, p_y, p_z, s*)``."""

    s: ScalarQuantity
    p: ScalarQuantity
    s_star: ScalarQuantity

    def __post_init__(self) -> None:
        for name in ("s", "p", "s_star"):
            _require_energy(getattr(self, name), name)


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondSp3sStarFirstNeighbor:
    """First-neighbor two-center integrals in eV.

    The first-neighbor ``s-s*`` and ``s*-s*`` channels are explicit zeros when
    composed into the seven-channel PhysKit integral record.
    """

    ss_sigma: ScalarQuantity
    sp_sigma: ScalarQuantity
    pp_sigma: ScalarQuantity
    pp_pi: ScalarQuantity
    s_star_p_sigma: ScalarQuantity

    def __post_init__(self) -> None:
        for name in (
            "ss_sigma",
            "sp_sigma",
            "pp_sigma",
            "pp_pi",
            "s_star_p_sigma",
        ):
            _require_energy(getattr(self, name), name)

    @property
    def two_center_integrals(self) -> HomopolarSp3sStarTwoCenterIntegrals:
        """Return the complete PhysKit seven-channel first-neighbor vector."""
        zero = ScalarQuantity(0.0, ELECTRON_VOLT)
        return HomopolarSp3sStarTwoCenterIntegrals(
            ss_sigma=self.ss_sigma,
            sp_sigma=self.sp_sigma,
            pp_sigma=self.pp_sigma,
            pp_pi=self.pp_pi,
            s_star_p_sigma=self.s_star_p_sigma,
            s_s_star_sigma=zero,
            s_star_s_star_sigma=zero,
            unit_system=UnitSystem.METAL,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondSp3sStarSecondNeighbor:
    """Symmetry-shared second-neighbor two-center integrals in eV."""

    ss_sigma: ScalarQuantity
    sp_sigma: ScalarQuantity
    pp_sigma: ScalarQuantity
    pp_pi: ScalarQuantity
    s_star_p_sigma: ScalarQuantity
    s_s_star_sigma: ScalarQuantity
    s_star_s_star_sigma: ScalarQuantity

    def __post_init__(self) -> None:
        for name in (
            "ss_sigma",
            "sp_sigma",
            "pp_sigma",
            "pp_pi",
            "s_star_p_sigma",
            "s_s_star_sigma",
            "s_star_s_star_sigma",
        ):
            _require_energy(getattr(self, name), name)

    @property
    def two_center_integrals(self) -> HomopolarSp3sStarTwoCenterIntegrals:
        """Return the complete PhysKit seven-channel second-neighbor vector."""
        return HomopolarSp3sStarTwoCenterIntegrals(
            ss_sigma=self.ss_sigma,
            sp_sigma=self.sp_sigma,
            pp_sigma=self.pp_sigma,
            pp_pi=self.pp_pi,
            s_star_p_sigma=self.s_star_p_sigma,
            s_s_star_sigma=self.s_s_star_sigma,
            s_star_s_star_sigma=self.s_star_s_star_sigma,
            unit_system=UnitSystem.METAL,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondSp3sStarParameters:
    """The ordered 15-parameter real homopolar ``sp3s*`` inventory.

    KSD owns the concrete onsite, first-neighbor, and second-neighbor grouping used
    by the silicon program. PhysKit owns the reusable seven-channel integral and
    hopping mechanics consumed by the composed model.
    """

    onsite: DiamondSp3sStarOnsite
    first_neighbor: DiamondSp3sStarFirstNeighbor
    second_neighbor: DiamondSp3sStarSecondNeighbor

    def __post_init__(self) -> None:
        if type(self.onsite) is not DiamondSp3sStarOnsite:
            raise TypeError("onsite must be DiamondSp3sStarOnsite")
        if type(self.first_neighbor) is not DiamondSp3sStarFirstNeighbor:
            raise TypeError("first_neighbor must be DiamondSp3sStarFirstNeighbor")
        if type(self.second_neighbor) is not DiamondSp3sStarSecondNeighbor:
            raise TypeError("second_neighbor must be DiamondSp3sStarSecondNeighbor")

    @property
    def parameter_names(self) -> tuple[str, ...]:
        """Return the stable S110 M2 parameter-vector field order."""
        return _PARAMETER_NAMES

    def ordered_quantities(self) -> tuple[ScalarQuantity, ...]:
        """Return parameters in the stable S110 M2 field order."""
        onsite = self.onsite
        first = self.first_neighbor
        second = self.second_neighbor
        return (
            onsite.s,
            onsite.p,
            onsite.s_star,
            first.ss_sigma,
            first.sp_sigma,
            first.pp_sigma,
            first.pp_pi,
            first.s_star_p_sigma,
            second.ss_sigma,
            second.sp_sigma,
            second.pp_sigma,
            second.pp_pi,
            second.s_star_p_sigma,
            second.s_s_star_sigma,
            second.s_star_s_star_sigma,
        )

    def as_vector_ev(self) -> Float64Array:
        """Return an immutable binary64 parameter vector in eV."""
        values = np.asarray(
            tuple(value.magnitude for value in self.ordered_quantities()),
            dtype="<f8",
        )
        return np.frombuffer(values.tobytes(), dtype="<f8")

    @classmethod
    def from_vector_ev(cls, *, values: Float64Array) -> DiamondSp3sStarParameters:
        """Construct the stable parameter map from a length-15 NumPy array in eV."""
        if not isinstance(values, np.ndarray):
            raise TypeError("values must be a numpy.ndarray")
        if values.dtype.kind not in "iuf":
            raise TypeError("values must contain real numbers excluding booleans")
        vector = np.asarray(values, dtype=np.float64)
        if vector.shape != (15,):
            raise ValueError("values must have shape (15,)")
        if not np.all(np.isfinite(vector)):
            raise ValueError("values must be finite")

        quantities = tuple(
            ScalarQuantity(float(value), ELECTRON_VOLT) for value in vector
        )
        return cls(
            onsite=DiamondSp3sStarOnsite(
                s=quantities[0],
                p=quantities[1],
                s_star=quantities[2],
            ),
            first_neighbor=DiamondSp3sStarFirstNeighbor(
                ss_sigma=quantities[3],
                sp_sigma=quantities[4],
                pp_sigma=quantities[5],
                pp_pi=quantities[6],
                s_star_p_sigma=quantities[7],
            ),
            second_neighbor=DiamondSp3sStarSecondNeighbor(
                ss_sigma=quantities[8],
                sp_sigma=quantities[9],
                pp_sigma=quantities[10],
                pp_pi=quantities[11],
                s_star_p_sigma=quantities[12],
                s_s_star_sigma=quantities[13],
                s_star_s_star_sigma=quantities[14],
            ),
        )
