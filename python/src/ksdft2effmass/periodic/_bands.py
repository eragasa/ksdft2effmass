"""Private calculator-neutral represented band observations.

These immutable values hold normalized representation and alignment metadata.
They do not perform comparison or establish parent-model equivalence.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum


def _require_string(value: object, name: str) -> None:
    """Require one nonempty exact string."""
    if type(value) is not str:
        raise TypeError(f"{name} must be a string")
    if not value:
        raise ValueError(f"{name} must not be empty")


def _require_optional_string(value: object, name: str) -> None:
    """Require one nonempty exact string or absence."""
    if value is not None:
        _require_string(value, name)


def _require_positive_integer(value: object, name: str) -> None:
    """Require one positive exact integer, excluding booleans."""
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _require_finite_float(value: object, name: str, *, positive: bool = False) -> None:
    """Require one finite exact float with the requested sign."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if (positive and value <= 0.0) or (not positive and value < 0.0):
        qualifier = "positive" if positive else "nonnegative"
        raise ValueError(f"{name} must be {qualifier}")


class DftBackend(StrEnum):
    """Closed backends exercised by the initial internal slice."""

    QUANTUM_ESPRESSO = "quantum_espresso"
    ABINIT = "abinit"


class BandEnergyUnit(StrEnum):
    """Closed energy units admitted by normalized band observations."""

    HARTREE = "hartree"
    ELECTRON_VOLT = "electron_volt"


@dataclass(frozen=True, slots=True)
class BandStructureObservationIdentity:
    """Nominal identity of one normalized represented band observation."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        _require_string(self.value, "band structure observation identity")


@dataclass(frozen=True, slots=True)
class BandStructureObservation:
    """Calculator-neutral represented bands and explicit alignment metadata.

    ``eigenvalues`` is absent when the maintained observation references an
    external complete spectrum rather than embedding it.  Absence is explicit
    and prevents numerical comparison.
    """

    identity: BandStructureObservationIdentity
    source_result_identity: str
    backend: DftBackend
    system_identity: str
    scf_to_fixed_density_bands: bool
    path_topology: tuple[str, ...]
    point_count: int
    band_count: int
    coordinate_convention: str
    comparison_grid_identity: str | None
    lattice_parameter_bohr: float
    wavefunction_cutoff_hartree: float
    pseudopotential_sha256: str
    pseudopotential_alignment_identity: str | None
    energy_unit: BandEnergyUnit
    energy_reference: str
    energy_alignment_identity: str | None
    represented_spectrum_identity: str
    eigenvalues: tuple[tuple[float, ...], ...] | None = None

    def __post_init__(self) -> None:
        """Validate intrinsic normalized-observation state."""
        if type(self.identity) is not BandStructureObservationIdentity:
            raise TypeError("identity must be BandStructureObservationIdentity")
        _require_string(self.source_result_identity, "source_result_identity")
        if not isinstance(self.backend, DftBackend):
            raise TypeError("backend must be DftBackend")
        _require_string(self.system_identity, "system_identity")
        if type(self.scf_to_fixed_density_bands) is not bool:
            raise TypeError("scf_to_fixed_density_bands must be a bool")
        if type(self.path_topology) is not tuple or any(
            type(item) is not str for item in self.path_topology
        ):
            raise TypeError("path_topology must be a tuple of strings")
        if not self.path_topology or any(not item for item in self.path_topology):
            raise ValueError("path_topology must contain nonempty strings")
        _require_positive_integer(self.point_count, "point_count")
        _require_positive_integer(self.band_count, "band_count")
        _require_string(self.coordinate_convention, "coordinate_convention")
        _require_optional_string(
            self.comparison_grid_identity, "comparison_grid_identity"
        )
        _require_finite_float(
            self.lattice_parameter_bohr,
            "lattice_parameter_bohr",
            positive=True,
        )
        _require_finite_float(
            self.wavefunction_cutoff_hartree,
            "wavefunction_cutoff_hartree",
            positive=True,
        )
        _require_string(self.pseudopotential_sha256, "pseudopotential_sha256")
        if len(self.pseudopotential_sha256) != 64 or any(
            character not in "0123456789abcdef"
            for character in self.pseudopotential_sha256
        ):
            raise ValueError(
                "pseudopotential_sha256 must be a lowercase SHA-256 digest"
            )
        _require_optional_string(
            self.pseudopotential_alignment_identity,
            "pseudopotential_alignment_identity",
        )
        if not isinstance(self.energy_unit, BandEnergyUnit):
            raise TypeError("energy_unit must be BandEnergyUnit")
        _require_string(self.energy_reference, "energy_reference")
        _require_optional_string(
            self.energy_alignment_identity, "energy_alignment_identity"
        )
        _require_string(
            self.represented_spectrum_identity, "represented_spectrum_identity"
        )
        if self.eigenvalues is not None:
            self._validate_eigenvalues()

    def _validate_eigenvalues(self) -> None:
        """Validate an immutable complete finite point-by-band representation."""
        values = self.eigenvalues
        assert values is not None
        if type(values) is not tuple or any(type(row) is not tuple for row in values):
            raise TypeError("eigenvalues must be a tuple of tuples or None")
        if len(values) != self.point_count:
            raise ValueError("eigenvalues must contain point_count rows")
        for row in values:
            if len(row) != self.band_count:
                raise ValueError("each eigenvalue row must contain band_count values")
            for value in row:
                if type(value) is not float:
                    raise TypeError("eigenvalues must contain floats")
                if not math.isfinite(value):
                    raise ValueError("eigenvalues must be finite")
