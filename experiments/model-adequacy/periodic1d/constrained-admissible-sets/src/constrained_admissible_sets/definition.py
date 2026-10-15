"""Frozen controls for the publication-independent constrained-set experiment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentCalculationDefinition,
)
from projectkoios.optimization.quadratic.quadratic import (
    PositiveDefiniteQuadraticLoss,
)

EXPERIMENT_FAMILY_ID = (
    "ksdft2effmass.campaign.model-adequacy.periodic1d.constrained-admissible-sets"
)


def _finite_float(name: str, value: float) -> None:
    """Require one finite exact built-in float."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not np.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _parameter(name: str, value: tuple[float, float]) -> None:
    """Require one finite exact two-coordinate parameter."""
    if type(value) is not tuple or len(value) != 2:
        raise TypeError(f"{name} must be a length-two tuple")
    for index, component in enumerate(value):
        _finite_float(f"{name}[{index}]", component)


@dataclass(frozen=True, slots=True)
class QuadraticLoss2D:
    """Label one unit-free positive-definite completed-square loss.

    KSD owns channel and alignment meaning. ``projectkoios-optimization`` owns generic
    validation and evaluation of the completed-square numerical state.
    """

    channel_id: str
    alignment_angle: float | None
    center: tuple[float, float]
    quadratic_matrix: tuple[tuple[float, float], tuple[float, float]]
    minimum_squared_loss: float

    def __post_init__(self) -> None:
        """Validate labels and delegate generic quadratic acceptance."""
        if type(self.channel_id) is not str:
            raise TypeError("channel_id must be a built-in str")
        if not self.channel_id:
            raise ValueError("channel_id must be nonempty")
        if self.alignment_angle is not None:
            _finite_float("alignment_angle", self.alignment_angle)
        _parameter("center", self.center)
        if type(self.quadratic_matrix) is not tuple or len(self.quadratic_matrix) != 2:
            raise TypeError("quadratic_matrix must contain two tuple rows")
        if any(
            type(row) is not tuple or len(row) != 2 for row in self.quadratic_matrix
        ):
            raise TypeError("quadratic_matrix rows must be length-two tuples")
        for row_index, row in enumerate(self.quadratic_matrix):
            for column_index, value in enumerate(row):
                _finite_float(f"quadratic_matrix[{row_index}][{column_index}]", value)
        _finite_float("minimum_squared_loss", self.minimum_squared_loss)
        self._owner_loss()

    def squared_loss(self, parameter: tuple[float, float]) -> float:
        """Return the owner-evaluated squared loss at one KSD parameter."""
        _parameter("parameter", parameter)
        return self._owner_loss().squared_loss(parameter)

    def rms_loss(self, parameter: tuple[float, float]) -> float:
        """Return the owner-evaluated root-mean-square loss."""
        _parameter("parameter", parameter)
        return self._owner_loss().root_loss(parameter)

    def _owner_loss(self) -> PositiveDefiniteQuadraticLoss:
        """Return the unit-free owner representation."""
        return PositiveDefiniteQuadraticLoss(
            self.center,
            self.quadratic_matrix,
            self.minimum_squared_loss,
        )


@dataclass(frozen=True, slots=True)
class AdmissibleSetThresholds:
    """Freeze one named pair of dimensionless RMS thresholds."""

    case_id: str
    spectral_rms_threshold: float
    operator_rms_threshold: float

    def __post_init__(self) -> None:
        """Reject ambiguous identities and nonpositive thresholds."""
        if type(self.case_id) is not str:
            raise TypeError("case_id must be a built-in str")
        if not self.case_id:
            raise ValueError("case_id must be nonempty")
        for name, value in (
            ("spectral_rms_threshold", self.spectral_rms_threshold),
            ("operator_rms_threshold", self.operator_rms_threshold),
        ):
            _finite_float(name, value)
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class ConstrainedAdmissibleSetsExperimentDefinition:
    """Freeze parent composition and bounded admissible-set geometry.

    The experiment composes one exact rank-two multiband baseline and derives its
    normalized spectral and represented-operator training quadratics internally.
    Optimization receives only unit-free completed-square state and bounds.
    """

    multiband_baseline: Periodic1DMultibandAlignmentCalculationDefinition
    energy_shift_ratio_bounds: tuple[float, float]
    splitting_scale_bounds: tuple[float, float]
    alignment_angles: tuple[float, ...]
    loss_energy_scale: ScalarQuantity
    compatible_thresholds: AdmissibleSetThresholds
    separated_thresholds: AdmissibleSetThresholds
    compatible_witness: tuple[float, float]
    separation_resolution: float
    owner_absolute_tolerance: float
    verification_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Require a rank-two parent and complete ordered geometry controls."""
        if type(self.multiband_baseline) is not (
            Periodic1DMultibandAlignmentCalculationDefinition
        ):
            raise TypeError(
                "multiband_baseline must be "
                "Periodic1DMultibandAlignmentCalculationDefinition"
            )
        if self.multiband_baseline.retained_rank != 2:
            raise ValueError("the experiment requires a rank-two baseline")
        for name, bounds in (
            ("energy_shift_ratio_bounds", self.energy_shift_ratio_bounds),
            ("splitting_scale_bounds", self.splitting_scale_bounds),
        ):
            _parameter(name, bounds)
            if bounds[0] >= bounds[1]:
                raise ValueError(f"{name} must be strictly increasing")
        if self.splitting_scale_bounds[0] <= 0.0:
            raise ValueError("splitting_scale_bounds must remain positive")
        if type(self.alignment_angles) is not tuple or len(self.alignment_angles) < 2:
            raise TypeError("alignment_angles must contain at least two values")
        for index, angle in enumerate(self.alignment_angles):
            _finite_float(f"alignment_angles[{index}]", angle)
        if tuple(sorted(set(self.alignment_angles))) != self.alignment_angles:
            raise ValueError("alignment_angles must be unique and increasing")
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
            if type(thresholds) is not AdmissibleSetThresholds:
                raise TypeError(f"{name} must be AdmissibleSetThresholds")
        if self.compatible_thresholds.case_id == self.separated_thresholds.case_id:
            raise ValueError("threshold cases must have distinct identities")
        _parameter("compatible_witness", self.compatible_witness)
        if not self.contains(self.compatible_witness):
            raise ValueError("compatible_witness must lie in the parameter rectangle")
        for name, value in (
            ("separation_resolution", self.separation_resolution),
            ("owner_absolute_tolerance", self.owner_absolute_tolerance),
            ("verification_absolute_tolerance", self.verification_absolute_tolerance),
        ):
            _finite_float(name, value)
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")

    def contains(self, parameter: tuple[float, float]) -> bool:
        """Return whether one exact parameter lies in the closed rectangle."""
        _parameter("parameter", parameter)
        return (
            self.energy_shift_ratio_bounds[0]
            <= parameter[0]
            <= self.energy_shift_ratio_bounds[1]
            and self.splitting_scale_bounds[0]
            <= parameter[1]
            <= self.splitting_scale_bounds[1]
        )


__all__ = [
    "AdmissibleSetThresholds",
    "ConstrainedAdmissibleSetsExperimentDefinition",
    "EXPERIMENT_FAMILY_ID",
    "QuadraticLoss2D",
]
