"""Immutable outputs of the constrained admissible-set experiment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentCalculationResult,
)

from .definition import (
    AdmissibleSetThresholds,
    ConstrainedAdmissibleSetsExperimentDefinition,
    QuadraticLoss2D,
    _finite_float,
    _parameter,
)


class AdmissibleSetDisposition(Enum):
    """Bounded outcome for one frozen threshold pair."""

    COMPATIBLE_WITNESS = "compatible-witness"
    CERTIFIED_SEPARATED = "certified-separated"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class AdmissibleSetPointEvaluation:
    """Retain both losses and the selected finite component at one point."""

    role: str
    parameter: tuple[float, float]
    selected_alignment_angle: float
    spectral_rms_loss: float
    operator_rms_loss: float

    def __post_init__(self) -> None:
        """Validate one role-identified finite evaluation."""
        if type(self.role) is not str:
            raise TypeError("role must be a built-in str")
        if not self.role:
            raise ValueError("role must be nonempty")
        _parameter("parameter", self.parameter)
        _finite_float("selected_alignment_angle", self.selected_alignment_angle)
        for name, value in (
            ("spectral_rms_loss", self.spectral_rms_loss),
            ("operator_rms_loss", self.operator_rms_loss),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class AdmissibleSetCaseResult:
    """Retain a common witness or one bounded separation certificate."""

    thresholds: AdmissibleSetThresholds
    disposition: AdmissibleSetDisposition
    feasible_operator_component_angles: tuple[float, ...]
    common_witness: AdmissibleSetPointEvaluation | None
    spectral_certificate_point: AdmissibleSetPointEvaluation
    operator_certificate_point: AdmissibleSetPointEvaluation
    separation_lower_bound: float
    separation_upper_bound: float
    separation_resolution: float

    def __post_init__(self) -> None:
        """Validate inventories, bound ordering, and disposition semantics."""
        if type(self.thresholds) is not AdmissibleSetThresholds:
            raise TypeError("thresholds must be AdmissibleSetThresholds")
        if type(self.disposition) is not AdmissibleSetDisposition:
            raise TypeError("disposition must be AdmissibleSetDisposition")
        if type(self.feasible_operator_component_angles) is not tuple:
            raise TypeError("feasible_operator_component_angles must be a tuple")
        for index, angle in enumerate(self.feasible_operator_component_angles):
            _finite_float(f"feasible_operator_component_angles[{index}]", angle)
        if tuple(sorted(set(self.feasible_operator_component_angles))) != (
            self.feasible_operator_component_angles
        ):
            raise ValueError("feasible component angles must be unique and increasing")
        if not self.feasible_operator_component_angles:
            raise ValueError("operator admissible set must have a feasible component")
        if self.common_witness is not None and type(self.common_witness) is not (
            AdmissibleSetPointEvaluation
        ):
            raise TypeError("common_witness must be a point evaluation or None")
        for name, point in (
            ("spectral_certificate_point", self.spectral_certificate_point),
            ("operator_certificate_point", self.operator_certificate_point),
        ):
            if type(point) is not AdmissibleSetPointEvaluation:
                raise TypeError(f"{name} must be AdmissibleSetPointEvaluation")
        for name, value in (
            ("separation_lower_bound", self.separation_lower_bound),
            ("separation_upper_bound", self.separation_upper_bound),
            ("separation_resolution", self.separation_resolution),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if self.separation_lower_bound > self.separation_upper_bound:
            raise ValueError("separation bounds must be ordered")
        if self.disposition is AdmissibleSetDisposition.COMPATIBLE_WITNESS:
            if self.common_witness is None:
                raise ValueError("compatible disposition requires a witness")
            if self.separation_lower_bound != 0.0 or self.separation_upper_bound != 0.0:
                raise ValueError("common witness requires zero separation bounds")
            if (
                self.spectral_certificate_point != self.common_witness
                or self.operator_certificate_point != self.common_witness
            ):
                raise ValueError("common witness must be both certificate points")
        elif self.disposition is AdmissibleSetDisposition.CERTIFIED_SEPARATED:
            if self.common_witness is not None:
                raise ValueError("separated disposition cannot retain a witness")
            if self.separation_lower_bound <= self.separation_resolution:
                raise ValueError("certified separation must exceed the resolution")
        else:
            if self.common_witness is not None:
                raise ValueError("unresolved disposition cannot retain a witness")
            if self.separation_lower_bound > self.separation_resolution:
                raise ValueError("unresolved lower bound cannot exceed resolution")


@dataclass(frozen=True, slots=True)
class ConstrainedAdmissibleSetsExperimentResult:
    """Correlate parent evidence, derived losses, and both threshold cases."""

    definition: ConstrainedAdmissibleSetsExperimentDefinition
    multiband_baseline: Periodic1DMultibandAlignmentCalculationResult
    spectral_loss: QuadraticLoss2D
    operator_losses: tuple[QuadraticLoss2D, ...]
    cases: tuple[AdmissibleSetCaseResult, AdmissibleSetCaseResult]

    def __post_init__(self) -> None:
        """Validate parent identity, loss family, cases, and point evaluations."""
        if type(self.definition) is not ConstrainedAdmissibleSetsExperimentDefinition:
            raise TypeError(
                "definition must be ConstrainedAdmissibleSetsExperimentDefinition"
            )
        if type(self.multiband_baseline) is not (
            Periodic1DMultibandAlignmentCalculationResult
        ):
            raise TypeError(
                "multiband_baseline must be "
                "Periodic1DMultibandAlignmentCalculationResult"
            )
        if self.multiband_baseline.definition is not self.definition.multiband_baseline:
            raise ValueError("baseline must use the exact composed definition")
        if type(self.spectral_loss) is not QuadraticLoss2D:
            raise TypeError("spectral_loss must be QuadraticLoss2D")
        if self.spectral_loss.alignment_angle is not None:
            raise ValueError("spectral_loss must be alignment-invariant")
        if type(self.operator_losses) is not tuple or any(
            type(loss) is not QuadraticLoss2D for loss in self.operator_losses
        ):
            raise TypeError("operator_losses must be a typed tuple")
        if tuple(loss.alignment_angle for loss in self.operator_losses) != (
            self.definition.alignment_angles
        ):
            raise ValueError("operator losses must match the declared angle family")
        if type(self.cases) is not tuple or len(self.cases) != 2:
            raise TypeError("cases must be a length-two tuple")
        if any(type(case) is not AdmissibleSetCaseResult for case in self.cases):
            raise TypeError("cases must contain AdmissibleSetCaseResult values")
        if tuple(case.thresholds for case in self.cases) != (
            self.definition.compatible_thresholds,
            self.definition.separated_thresholds,
        ):
            raise ValueError("cases must match the declared threshold order")
        by_angle = {
            float(loss.alignment_angle): loss
            for loss in self.operator_losses
            if loss.alignment_angle is not None
        }
        tolerance = self.definition.owner_absolute_tolerance
        for case in self.cases:
            if not set(case.feasible_operator_component_angles).issubset(by_angle):
                raise ValueError("feasible angles must belong to the declared family")
            points = {
                case.spectral_certificate_point,
                case.operator_certificate_point,
            }
            if case.common_witness is not None:
                points.add(case.common_witness)
            for point in points:
                if not self.definition.contains(point.parameter):
                    raise ValueError("certificate points must lie in the rectangle")
                if point.selected_alignment_angle not in by_angle:
                    raise ValueError(
                        "selected angle must belong to the declared family"
                    )
                expected_spectral = self.spectral_loss.rms_loss(point.parameter)
                expected_operator = by_angle[point.selected_alignment_angle].rms_loss(
                    point.parameter
                )
                if (
                    abs(point.spectral_rms_loss - expected_spectral) > tolerance
                    or abs(point.operator_rms_loss - expected_operator) > tolerance
                ):
                    raise ValueError("point evaluations must match declared losses")
            if (
                case.spectral_certificate_point.spectral_rms_loss
                > case.thresholds.spectral_rms_threshold + tolerance
            ):
                raise ValueError("spectral certificate point must be feasible")
            if (
                case.operator_certificate_point.operator_rms_loss
                > case.thresholds.operator_rms_threshold + tolerance
            ):
                raise ValueError("operator certificate point must be feasible")
            distance = float(
                np.linalg.norm(
                    np.asarray(case.spectral_certificate_point.parameter)
                    - np.asarray(case.operator_certificate_point.parameter)
                )
            )
            if abs(case.separation_upper_bound - distance) > tolerance:
                raise ValueError(
                    "upper bound must equal the certificate-point distance"
                )


__all__ = [
    "AdmissibleSetCaseResult",
    "AdmissibleSetDisposition",
    "AdmissibleSetPointEvaluation",
    "ConstrainedAdmissibleSetsExperimentResult",
]
