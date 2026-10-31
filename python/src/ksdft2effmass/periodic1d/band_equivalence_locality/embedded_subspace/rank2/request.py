"""Request for the installed embedded-subspace rank-two control."""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

_AMBIENT_RANK = 4
_RETAINED_RANK = 2
_PARENT_MODEL_ID = "specified-finite-range-ambient-rank4-retained-rank2-parent.v1"
_AMBIENT_BASIS_ID = "fixed-ambient-rank4-parent-basis.v1"
_RETAINED_FRAME_ID = "lowest-rank2-spectral-frame.v1"
_ENDPOINT_SEWING_ID = "identity-periodic-endpoint-sewing.v1"
_ENERGY_REFERENCE_ID = "positive-reference-energy-E_ref.v1"
_RECIPROCAL_COORDINATE_CONVENTION = "centered-half-open-reduced-coordinate.v1"
_GAUGE_ATTACK_ID = "retained-real-sinusoidal-rotation.v1"
_VERIFICATION_ABSOLUTE_TOLERANCE = 1.0e-10


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2Request:
    """Bind mesh, gauge attack amplitudes, qualification gates, and tolerances."""

    reciprocal_mesh_size: int
    amplitudes: tuple[float, ...]
    parent_hopping_scale: float
    minimum_external_gap: float
    minimum_transport_singular_value: float
    frame_absolute_tolerance: float
    transport_rank_relative_tolerance: float
    transport_validation_relative_tolerance: float
    harmonic_absolute_degeneracy_tolerance: float
    harmonic_relative_degeneracy_tolerance: float

    def __post_init__(self) -> None:
        if type(self.reciprocal_mesh_size) is not int:
            raise TypeError("reciprocal_mesh_size must be a built-in int")
        if self.reciprocal_mesh_size < 8 or self.reciprocal_mesh_size % 2:
            raise ValueError("reciprocal_mesh_size must be even and at least eight")
        if type(self.amplitudes) is not tuple or len(self.amplitudes) < 2:
            raise TypeError("amplitudes must contain at least two built-in floats")
        for amplitude in self.amplitudes:
            if type(amplitude) is not float:
                raise TypeError("amplitudes must contain built-in floats")
            if not math.isfinite(amplitude) or not 0.0 <= amplitude <= math.pi / 4.0:
                raise ValueError("amplitudes must be finite and lie in [0, pi/4]")
        if self.amplitudes[0] != 0.0:
            raise ValueError("amplitudes must begin at zero")
        if tuple(sorted(set(self.amplitudes))) != self.amplitudes:
            raise ValueError("amplitudes must be unique and strictly increasing")
        for name in (
            "parent_hopping_scale",
            "minimum_external_gap",
            "minimum_transport_singular_value",
            "frame_absolute_tolerance",
            "transport_rank_relative_tolerance",
            "transport_validation_relative_tolerance",
            "harmonic_absolute_degeneracy_tolerance",
            "harmonic_relative_degeneracy_tolerance",
        ):
            value = getattr(self, name)
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if not 0.0 <= self.parent_hopping_scale <= 1.0:
            raise ValueError("parent_hopping_scale must lie in [0, 1]")
        if self.minimum_external_gap == 0.0:
            raise ValueError("minimum_external_gap must be positive")
        if not 0.0 < self.minimum_transport_singular_value <= 1.0:
            raise ValueError("minimum_transport_singular_value must lie in (0, 1]")
        if self.frame_absolute_tolerance == 0.0:
            raise ValueError("frame_absolute_tolerance must be positive")
        if (
            self.harmonic_absolute_degeneracy_tolerance == 0.0
            and self.harmonic_relative_degeneracy_tolerance == 0.0
        ):
            raise ValueError("at least one harmonic tolerance must be positive")

    @property
    def verification_absolute_tolerance(self) -> float:
        """Return the fixed installed independent-comparison policy."""
        return _VERIFICATION_ABSOLUTE_TOLERANCE

    @property
    def ambient_rank(self) -> int:
        """Return the fixed ambient matrix rank."""
        return _AMBIENT_RANK

    @property
    def retained_rank(self) -> int:
        """Return the fixed retained-subspace rank."""
        return _RETAINED_RANK

    @property
    def parent_model_identifier(self) -> str:
        """Return the fixed parent-model identity."""
        return _PARENT_MODEL_ID

    @property
    def ambient_basis_identifier(self) -> str:
        """Return the fixed ambient-basis identity."""
        return _AMBIENT_BASIS_ID

    @property
    def retained_frame_identifier(self) -> str:
        """Return the fixed retained-frame identity."""
        return _RETAINED_FRAME_ID

    @property
    def endpoint_sewing_identifier(self) -> str:
        """Return the fixed endpoint-sewing identity."""
        return _ENDPOINT_SEWING_ID

    @property
    def energy_reference_identifier(self) -> str:
        """Return the fixed energy-reference identity."""
        return _ENERGY_REFERENCE_ID

    @property
    def reciprocal_coordinate_convention(self) -> str:
        """Return the fixed reduced-coordinate convention."""
        return _RECIPROCAL_COORDINATE_CONVENTION

    @property
    def gauge_attack_identifier(self) -> str:
        """Return the fixed retained-space gauge-attack identity."""
        return _GAUGE_ATTACK_ID

    def construction_reduced_momenta(self) -> tuple[float, ...]:
        """Return the exact centered half-open construction mesh."""
        size = self.reciprocal_mesh_size
        return tuple(-0.5 + float(index) / float(size) for index in range(size))

    def transport_tolerance(self) -> ComplexUnitaryProcrustesTolerance:
        """Return the explicitly declared Optimization-owner tolerance."""
        return ComplexUnitaryProcrustesTolerance(
            rank_absolute=self.frame_absolute_tolerance,
            rank_relative=self.transport_rank_relative_tolerance,
            validation_absolute=self.frame_absolute_tolerance,
            validation_relative=self.transport_validation_relative_tolerance,
        )

    def principal_phase_branch(
        self,
    ) -> ClosedLoopPolarFrameTransportPrincipalPhaseBranch:
        """Return the fixed principal branch used by the installed control."""
        return ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open


__all__ = ["Periodic1DEmbeddedSubspaceRank2Request"]
