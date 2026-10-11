"""Prospective controls for the one-dimensional constrained admissible-set study."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic1d.model import Periodic1DBlockHamiltonianToyModel
from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentCalculationDefinition,
)


def _finite_float(name: str, value: float) -> None:
    """Require a finite exact built-in float and reject Boolean impostors."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not np.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive_float(name: str, value: float) -> None:
    """Require a finite strictly positive exact built-in float."""
    _finite_float(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetThresholds:
    """Freeze one named pair of dimensionless RMS benchmark thresholds.

    Parameters
    ----------
    case_id
        Stable nonempty case identity.
    spectral_rms_threshold, operator_rms_threshold
        Finite strictly positive built-in floats defining spectral and represented-
        operator sublevel sets.  They are design controls, not uncertainty bounds.
    """

    case_id: str
    spectral_rms_threshold: float
    operator_rms_threshold: float

    def __post_init__(self) -> None:
        """Reject ambiguous identities and nonpositive thresholds."""
        if type(self.case_id) is not str:
            raise TypeError("case_id must be a built-in str")
        if not self.case_id:
            raise ValueError("case_id must be nonempty")
        _positive_float("spectral_rms_threshold", self.spectral_rms_threshold)
        _positive_float("operator_rms_threshold", self.operator_rms_threshold)


@dataclass(frozen=True, slots=True)
class Periodic1DConstrainedAdmissibleSetCalculationDefinition:
    """Freeze the M3 rectangular domain, angle family, losses, and thresholds.

    Parameters
    ----------
    calculation_id
        Stable nonempty M3 calculation identity.
    multiband_baseline
        Exact rank-two M2 definition composed by M3.
    energy_shift_ratio_bounds, splitting_scale_bounds
        Strictly increasing intervals defining a continuous closed rectangle.  The
        splitting scale remains strictly positive.
    alignment_angles
        Finite strictly increasing radian inventory of one-global real rotations.
    loss_energy_scale
        Positive parent-energy quantity used to normalize both RMS losses.
    compatible_thresholds, separated_thresholds
        Distinct prospective case controls.
    compatible_witness
        Prospective point ``(energy_shift_ratio, splitting_scale)`` in the rectangle.
    locality_ranges
        Ordered finite ranges used only for locality diagnostics.
    separation_resolution
        Positive Euclidean parameter-space resolution for the bounded certificate.
    quadratic_absolute_tolerance, verification_absolute_tolerance
        Positive finite controls for proof-object and independent reconstruction checks.

    Notes
    -----
    At each reciprocal point, the candidate is the trace part of the M2 reference plus
    ``energy_shift_ratio * loss_energy_scale`` times identity and ``splitting_scale``
    times the traceless part.  Training formulas define quadratics, witnesses, and
    certificates; the M2 staggered mesh is evaluation-only.
    """

    calculation_id: str
    multiband_baseline: Periodic1DMultibandAlignmentCalculationDefinition
    energy_shift_ratio_bounds: tuple[float, float]
    splitting_scale_bounds: tuple[float, float]
    alignment_angles: tuple[float, ...]
    loss_energy_scale: ScalarQuantity
    compatible_thresholds: Periodic1DAdmissibleSetThresholds
    separated_thresholds: Periodic1DAdmissibleSetThresholds
    compatible_witness: tuple[float, float]
    locality_ranges: tuple[int, ...]
    separation_resolution: float
    quadratic_absolute_tolerance: float
    verification_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Require a compact domain, finite alignment family, and frozen roles."""
        if type(self.calculation_id) is not str:
            raise TypeError("calculation_id must be a built-in str")
        if not self.calculation_id:
            raise ValueError("calculation_id must be nonempty")
        if type(self.multiband_baseline) is not (
            Periodic1DMultibandAlignmentCalculationDefinition
        ):
            raise TypeError(
                "multiband_baseline must be "
                "Periodic1DMultibandAlignmentCalculationDefinition"
            )
        if self.multiband_baseline.retained_rank != 2:
            raise ValueError("M3 v1 requires a rank-two M2 baseline")
        for name, bounds in (
            ("energy_shift_ratio_bounds", self.energy_shift_ratio_bounds),
            ("splitting_scale_bounds", self.splitting_scale_bounds),
        ):
            if not isinstance(bounds, tuple) or len(bounds) != 2:
                raise TypeError(f"{name} must be a length-two tuple")
            _finite_float(f"{name}[0]", bounds[0])
            _finite_float(f"{name}[1]", bounds[1])
            if bounds[0] >= bounds[1]:
                raise ValueError(f"{name} must be strictly increasing")
        if self.splitting_scale_bounds[0] <= 0.0:
            raise ValueError("splitting_scale_bounds must remain strictly positive")
        if (
            not isinstance(self.alignment_angles, tuple)
            or len(self.alignment_angles) < 2
        ):
            raise TypeError("alignment_angles must contain at least two values")
        for index, angle in enumerate(self.alignment_angles):
            _finite_float(f"alignment_angles[{index}]", angle)
        if tuple(sorted(set(self.alignment_angles))) != self.alignment_angles:
            raise ValueError("alignment_angles must be unique and strictly increasing")
        if not any(angle != 0.0 for angle in self.alignment_angles):
            raise ValueError("alignment family must contain a nonidentity rotation")
        if type(self.loss_energy_scale) is not ScalarQuantity:
            raise TypeError("loss_energy_scale must be ScalarQuantity")
        if self.loss_energy_scale.magnitude <= 0.0:
            raise ValueError("loss_energy_scale must be positive")
        parent_unit = self.multiband_baseline.parent_model.hopping_model.hopping_blocks[
            0
        ].unit
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.loss_energy_scale.unit, parent_unit
        ):
            raise ValueError("loss_energy_scale must use parent energy dimensions")
        for name, thresholds in (
            ("compatible_thresholds", self.compatible_thresholds),
            ("separated_thresholds", self.separated_thresholds),
        ):
            if type(thresholds) is not Periodic1DAdmissibleSetThresholds:
                raise TypeError(f"{name} must be Periodic1DAdmissibleSetThresholds")
        if self.compatible_thresholds.case_id == self.separated_thresholds.case_id:
            raise ValueError("threshold cases must have distinct identities")
        if (
            not isinstance(self.compatible_witness, tuple)
            or len(self.compatible_witness) != 2
        ):
            raise TypeError("compatible_witness must be a length-two tuple")
        for index, value in enumerate(self.compatible_witness):
            _finite_float(f"compatible_witness[{index}]", value)
        if not self.contains(self.compatible_witness):
            raise ValueError("compatible_witness must lie in the parameter domain")
        if not isinstance(self.locality_ranges, tuple) or not self.locality_ranges:
            raise TypeError("locality_ranges must be a nonempty tuple")
        if any(type(value) is not int for value in self.locality_ranges):
            raise TypeError("locality_ranges must contain built-in integers")
        if tuple(sorted(set(self.locality_ranges))) != self.locality_ranges:
            raise ValueError("locality_ranges must be unique and strictly increasing")
        if self.locality_ranges[0] < 0:
            raise ValueError("locality_ranges must be nonnegative")
        if self.locality_ranges[-1] >= (
            self.multiband_baseline.reciprocal_mesh_size // 2
        ):
            raise ValueError("locality ranges must be smaller than half the mesh")
        _positive_float("separation_resolution", self.separation_resolution)
        _positive_float(
            "quadratic_absolute_tolerance", self.quadratic_absolute_tolerance
        )
        _positive_float(
            "verification_absolute_tolerance", self.verification_absolute_tolerance
        )

    def contains(self, parameter: tuple[float, float]) -> bool:
        """Return whether a strict numeric pair lies in the closed rectangle.

        ``parameter`` is ordered as ``(energy_shift_ratio, splitting_scale)``.  Boolean,
        non-float, nonfinite, and malformed inputs raise rather than compare loosely.
        """
        if not isinstance(parameter, tuple) or len(parameter) != 2:
            raise TypeError("parameter must be a length-two tuple")
        for index, value in enumerate(parameter):
            _finite_float(f"parameter[{index}]", value)
        shift, splitting = parameter
        return (
            self.energy_shift_ratio_bounds[0]
            <= shift
            <= self.energy_shift_ratio_bounds[1]
            and self.splitting_scale_bounds[0]
            <= splitting
            <= self.splitting_scale_bounds[1]
        )

    @property
    def parent_model(self) -> Periodic1DBlockHamiltonianToyModel:
        """Return the exact parent model supplied by the M2 baseline."""
        return self.multiband_baseline.parent_model


__all__ = [
    "Periodic1DAdmissibleSetThresholds",
    "Periodic1DConstrainedAdmissibleSetCalculationDefinition",
]
