"""Real energy parameters for the homopolar diamond ``sp3s*`` model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity

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


@dataclass(frozen=True, slots=True)
class DiamondSp3sStarOnsite:
    """Homopolar onsite energies in eV for ``(s, px, py, pz, s*)``."""

    s: ScalarQuantity
    p: ScalarQuantity
    s_star: ScalarQuantity

    def __post_init__(self) -> None:
        for name in ("s", "p", "s_star"):
            _require_energy(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class DiamondSp3sStarFirstNeighbor:
    """First-neighbor two-center integrals in eV.

    The ``s-s*`` and ``s*-s*`` first-neighbor channels are absent by contract and
    therefore cannot be assigned accidentally.
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


@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
class DiamondSp3sStarParameters:
    """The ordered 15-parameter real homopolar ``sp3s*`` inventory.

    All values are finite binary64 scalars with the exact PhysKit unit
    ``electron_volt``. The stable vector order matches the S110 M2 declaration.
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
        """Return the stable parameter-vector field order."""
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
    def from_vector_ev(cls, values: Float64Array) -> DiamondSp3sStarParameters:
        """Construct the stable parameter map from a length-15 array in eV.

        Boolean arrays, numeric strings, nonfinite values, and non-arrays are
        rejected rather than coerced. Integer and floating inputs are converted to
        binary64; values that overflow that representation are rejected as nonfinite.
        """
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
            onsite=DiamondSp3sStarOnsite(*quantities[0:3]),
            first_neighbor=DiamondSp3sStarFirstNeighbor(*quantities[3:8]),
            second_neighbor=DiamondSp3sStarSecondNeighbor(*quantities[8:15]),
        )
