"""Historical finite-angle results retained only for regression."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentCalculationResult,
)

from .regression_definition import (
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
class AdmissibleSetLocalityResult:
    """Retain energy-valued omitted-block norms at one maximum range.

    Parameters
    ----------
    maximum_range
        Inclusive hopping-representative modulus retained by truncation.
    reference_omitted_block_l2_norm
        Omitted-block norm for the reference represented Hamiltonian.
    attacked_omitted_block_l2_norm
        Omitted-block norm for the attacked represented Hamiltonian.
    candidate_omitted_block_l2_norm
        Omitted-block norm for the selected aligned candidate.

    Notes
    -----
    Each norm is a magnitude in the common parent energy unit. The aggregate result
    supplies that unit through its exact composed parent definition.
    """

    maximum_range: int
    reference_omitted_block_l2_norm: float
    attacked_omitted_block_l2_norm: float
    candidate_omitted_block_l2_norm: float

    def __post_init__(self) -> None:
        """Validate the range and finite nonnegative norm magnitudes."""
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        for name, value in (
            ("reference_omitted_block_l2_norm", self.reference_omitted_block_l2_norm),
            ("attacked_omitted_block_l2_norm", self.attacked_omitted_block_l2_norm),
            ("candidate_omitted_block_l2_norm", self.candidate_omitted_block_l2_norm),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class AdmissibleSetPointEvaluation:
    """Retain objective-role losses and locality at one proof point.

    Parameters
    ----------
    role
        Stable witness or certificate-point role identity.
    parameter
        Energy-shift ratio and splitting scale.
    selected_alignment_angle
        Construction-selected global real-rotation angle in radians.
    objective_construction_spectral_rms_loss
        Spectral loss on samples that define quadratics and decisions.
    objective_construction_operator_rms_loss
        Operator loss on samples that define quadratics and decisions.
    objective_evaluation_spectral_rms_loss
        Post-decision spectral loss on the disjoint evaluation mesh.
    objective_evaluation_operator_rms_loss
        Post-decision operator loss on the disjoint evaluation mesh.
    locality
        Range-resolved finite-mesh omitted-block diagnostics.
    """

    role: str
    parameter: tuple[float, float]
    selected_alignment_angle: float
    objective_construction_spectral_rms_loss: float
    objective_construction_operator_rms_loss: float
    objective_evaluation_spectral_rms_loss: float
    objective_evaluation_operator_rms_loss: float
    locality: tuple[AdmissibleSetLocalityResult, ...]

    def __post_init__(self) -> None:
        """Validate one role-identified finite evaluation."""
        if type(self.role) is not str:
            raise TypeError("role must be a built-in str")
        if not self.role:
            raise ValueError("role must be nonempty")
        _parameter("parameter", self.parameter)
        _finite_float("selected_alignment_angle", self.selected_alignment_angle)
        for name, value in (
            (
                "objective_construction_spectral_rms_loss",
                self.objective_construction_spectral_rms_loss,
            ),
            (
                "objective_construction_operator_rms_loss",
                self.objective_construction_operator_rms_loss,
            ),
            (
                "objective_evaluation_spectral_rms_loss",
                self.objective_evaluation_spectral_rms_loss,
            ),
            (
                "objective_evaluation_operator_rms_loss",
                self.objective_evaluation_operator_rms_loss,
            ),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.locality) is not tuple or any(
            type(item) is not AdmissibleSetLocalityResult for item in self.locality
        ):
            raise TypeError("locality must be a typed tuple")
        ranges = tuple(item.maximum_range for item in self.locality)
        if tuple(sorted(set(ranges))) != ranges:
            raise ValueError("locality ranges must be unique and increasing")


@dataclass(frozen=True, slots=True)
class AdmissibleSetCaseResult:
    """Retain a common witness or one bounded separation certificate.

    Parameters
    ----------
    thresholds
        Named spectral and operator RMS thresholds.
    disposition
        Constructive compatibility, certified separation, or unresolved outcome.
    feasible_operator_component_angles
        Ordered operator components intersecting the parameter rectangle.
    common_witness
        Constructive common point, or ``None`` when none is retained.
    spectral_certificate_point, operator_certificate_point
        Feasible points defining the reported upper bound and axis certificate.
    separation_lower_bound, separation_upper_bound
        Ordered Euclidean parameter-distance bounds.
    separation_resolution
        Resolution that certified separation must strictly exceed.
    """

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
    """Correlate parent evidence, derived losses, and threshold cases.

    Parameters
    ----------
    definition
        Exact immutable controls used by the producer.
    multiband_baseline
        Composed parent result using the exact nested definition.
    spectral_loss
        Alignment-invariant objective-construction quadratic.
    operator_losses
        One objective-construction quadratic per declared alignment angle.
    cases
        Compatible and separated threshold outcomes in declared order.
    """

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
                ranges = tuple(item.maximum_range for item in point.locality)
                if ranges != self.definition.locality_ranges:
                    raise ValueError("locality must match the declared range inventory")
                expected_spectral = self.spectral_loss.rms_loss(point.parameter)
                expected_operator = by_angle[point.selected_alignment_angle].rms_loss(
                    point.parameter
                )
                if (
                    abs(
                        point.objective_construction_spectral_rms_loss
                        - expected_spectral
                    )
                    > tolerance
                    or abs(
                        point.objective_construction_operator_rms_loss
                        - expected_operator
                    )
                    > tolerance
                ):
                    raise ValueError("point evaluations must match declared losses")
            if (
                case.spectral_certificate_point.objective_construction_spectral_rms_loss
                > case.thresholds.spectral_rms_threshold + tolerance
            ):
                raise ValueError("spectral certificate point must be feasible")
            if (
                case.operator_certificate_point.objective_construction_operator_rms_loss
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
    "AdmissibleSetLocalityResult",
    "AdmissibleSetPointEvaluation",
    "ConstrainedAdmissibleSetsExperimentResult",
]
