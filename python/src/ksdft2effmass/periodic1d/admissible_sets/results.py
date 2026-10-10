"""Typed results for constrained multiband admissible sets."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentCalculationResult,
)

from .definition import (
    Periodic1DAdmissibleSetThresholds,
    Periodic1DConstrainedAdmissibleSetCalculationDefinition,
)


def _finite_nonnegative(name: str, value: float) -> None:
    """Require a finite nonnegative exact float and reject Booleans."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not np.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _parameter(name: str, value: tuple[float, float]) -> None:
    """Validate a finite shift/splitting parameter pair of built-in floats."""
    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError(f"{name} must be a length-two tuple")
    if any(type(item) is not float for item in value):
        raise TypeError(f"{name} must contain built-in floats")
    if any(not np.isfinite(item) for item in value):
        raise ValueError(f"{name} must contain finite values")


def _quadratic_matrix(
    name: str,
    value: tuple[tuple[float, float], tuple[float, float]],
) -> None:
    """Validate exact finite entries and shape of a two-dimensional quadratic."""
    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError(f"{name} must be a length-two tuple of rows")
    if any(not isinstance(row, tuple) or len(row) != 2 for row in value):
        raise TypeError(f"{name} rows must be length-two tuples")
    entries = tuple(entry for row in value for entry in row)
    if any(type(entry) is not float for entry in entries):
        raise TypeError(f"{name} must contain built-in floats")
    if any(not np.isfinite(entry) for entry in entries):
        raise ValueError(f"{name} must contain finite values")


class Periodic1DAdmissibleSetDisposition(Enum):
    """Bounded mathematical outcome for one frozen threshold pair.

    ``COMPATIBLE_WITNESS`` requires a constructive common point;
    ``CERTIFIED_SEPARATED`` requires a verified lower bound above resolution; and
    ``UNRESOLVED`` is mandatory when neither proof obligation is met.
    """

    COMPATIBLE_WITNESS = "compatible-witness"
    CERTIFIED_SEPARATED = "certified-separated"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class Periodic1DQuadraticLoss:
    r"""Represent one dimensionless squared RMS loss in centered quadratic form.

    The retained function is
    ``L(p)^2 = (p-center)^T quadratic_matrix (p-center) + minimum_squared_loss``
    over ``p=(energy_shift_ratio, splitting_scale)``.  Operator channels carry one
    frozen global ``alignment_angle``; the spectral channel carries ``None``.
    """

    channel_id: str
    alignment_angle: float | None
    center: tuple[float, float]
    quadratic_matrix: tuple[tuple[float, float], tuple[float, float]]
    minimum_squared_loss: float

    def __post_init__(self) -> None:
        """Require a finite positive-definite symmetric quadratic."""
        if type(self.channel_id) is not str or not self.channel_id:
            raise ValueError("channel_id must be a nonempty built-in string")
        if self.alignment_angle is not None:
            if type(self.alignment_angle) is not float or not np.isfinite(
                self.alignment_angle
            ):
                raise ValueError("alignment_angle must be finite or None")
        _parameter("center", self.center)
        _quadratic_matrix("quadratic_matrix", self.quadratic_matrix)
        matrix = np.asarray(self.quadratic_matrix, dtype=np.float64)
        if not np.array_equal(matrix, matrix.T):
            raise ValueError("quadratic_matrix must be exactly symmetric")
        if float(np.min(np.linalg.eigvalsh(matrix))) <= 0.0:
            raise ValueError("quadratic_matrix must be positive definite")
        _finite_nonnegative("minimum_squared_loss", self.minimum_squared_loss)

    def squared_loss(self, parameter: tuple[float, float]) -> float:
        """Evaluate the dimensionless retained squared loss at one parameter.

        Raises ``TypeError`` or ``ValueError`` for malformed, Boolean, or nonfinite
        parameter components.
        """
        _parameter("parameter", parameter)
        delta = np.asarray(parameter) - np.asarray(self.center)
        matrix = np.asarray(self.quadratic_matrix)
        return float(self.minimum_squared_loss + delta @ matrix @ delta)

    def rms_loss(self, parameter: tuple[float, float]) -> float:
        """Return the nonnegative dimensionless root-mean-square loss."""
        return float(np.sqrt(max(0.0, self.squared_loss(parameter))))


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetLocalityResult:
    """Retain omitted-block norms for three channels at one hopping range.

    The plain float norms are magnitudes in the common M2 parent energy unit. Reference,
    attacked, and selected-candidate values remain separate and are correlated by the
    aggregate result.
    """

    maximum_range: int
    reference_omitted_block_l2_norm: float
    attacked_omitted_block_l2_norm: float
    candidate_omitted_block_l2_norm: float

    def __post_init__(self) -> None:
        """Validate the range and energy-valued omitted norms."""
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        for name, value in (
            (
                "reference_omitted_block_l2_norm",
                self.reference_omitted_block_l2_norm,
            ),
            ("attacked_omitted_block_l2_norm", self.attacked_omitted_block_l2_norm),
            (
                "candidate_omitted_block_l2_norm",
                self.candidate_omitted_block_l2_norm,
            ),
        ):
            _finite_nonnegative(name, value)


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetParameterEvaluation:
    """Retain training-selected and evaluation-only diagnostics for one point.

    ``role`` identifies the prospective common witness or one of the two separation
    boundary points. ``parameter`` is ordered as energy-shift ratio and splitting
    scale; ``selected_alignment_angle`` belongs to the frozen finite angle family.
    Evaluation losses and locality cannot alter the selected point, angle, or
    disposition.
    """

    role: str
    parameter: tuple[float, float]
    selected_alignment_angle: float
    training_spectral_rms_loss: float
    training_operator_rms_loss: float
    withheld_spectral_rms_loss: float
    withheld_operator_rms_loss: float
    locality: tuple[Periodic1DAdmissibleSetLocalityResult, ...]

    def __post_init__(self) -> None:
        """Validate finite diagnostics and a unique ordered locality inventory."""
        if type(self.role) is not str or not self.role:
            raise ValueError("role must be a nonempty built-in string")
        _parameter("parameter", self.parameter)
        if type(self.selected_alignment_angle) is not float or not np.isfinite(
            self.selected_alignment_angle
        ):
            raise ValueError("selected_alignment_angle must be finite")
        for name, value in (
            ("training_spectral_rms_loss", self.training_spectral_rms_loss),
            ("training_operator_rms_loss", self.training_operator_rms_loss),
            ("withheld_spectral_rms_loss", self.withheld_spectral_rms_loss),
            ("withheld_operator_rms_loss", self.withheld_operator_rms_loss),
        ):
            _finite_nonnegative(name, value)
        if not isinstance(self.locality, tuple) or any(
            type(item) is not Periodic1DAdmissibleSetLocalityResult
            for item in self.locality
        ):
            raise TypeError("locality must be a typed tuple")
        ranges = tuple(item.maximum_range for item in self.locality)
        if tuple(sorted(set(ranges))) != ranges:
            raise ValueError("locality ranges must be unique and strictly increasing")


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetCaseResult:
    """Retain a constructive witness or bounded separation certificate.

    The compatible disposition requires ``common_witness`` and zero separation bounds.
    The separated disposition forbids a witness and requires the lower bound to exceed
    ``separation_resolution``. Otherwise the result must remain unresolved.
    """

    thresholds: Periodic1DAdmissibleSetThresholds
    disposition: Periodic1DAdmissibleSetDisposition
    feasible_operator_component_angles: tuple[float, ...]
    common_witness: Periodic1DAdmissibleSetParameterEvaluation | None
    spectral_certificate_point: Periodic1DAdmissibleSetParameterEvaluation
    operator_certificate_point: Periodic1DAdmissibleSetParameterEvaluation
    separation_lower_bound: float
    separation_upper_bound: float
    separation_resolution: float

    def __post_init__(self) -> None:
        """Validate certificate ordering and disposition semantics."""
        if type(self.thresholds) is not Periodic1DAdmissibleSetThresholds:
            raise TypeError("thresholds must be Periodic1DAdmissibleSetThresholds")
        if type(self.disposition) is not Periodic1DAdmissibleSetDisposition:
            raise TypeError("disposition must be Periodic1DAdmissibleSetDisposition")
        if not isinstance(self.feasible_operator_component_angles, tuple) or any(
            type(value) is not float or not np.isfinite(value)
            for value in self.feasible_operator_component_angles
        ):
            raise TypeError("feasible component angles must be a tuple of floats")
        if tuple(sorted(set(self.feasible_operator_component_angles))) != (
            self.feasible_operator_component_angles
        ):
            raise ValueError("feasible component angles must be unique and increasing")
        if not self.feasible_operator_component_angles:
            raise ValueError(
                "the operator admissible set must have a feasible component"
            )
        if self.common_witness is not None and type(self.common_witness) is not (
            Periodic1DAdmissibleSetParameterEvaluation
        ):
            raise TypeError("common_witness must be a parameter evaluation or None")
        for name, evaluation in (
            ("spectral_certificate_point", self.spectral_certificate_point),
            ("operator_certificate_point", self.operator_certificate_point),
        ):
            if type(evaluation) is not Periodic1DAdmissibleSetParameterEvaluation:
                raise TypeError(f"{name} must be a parameter evaluation")
        for name, scalar in (
            ("separation_lower_bound", self.separation_lower_bound),
            ("separation_upper_bound", self.separation_upper_bound),
            ("separation_resolution", self.separation_resolution),
        ):
            _finite_nonnegative(name, scalar)
        if self.separation_lower_bound > self.separation_upper_bound:
            raise ValueError("separation bounds are reversed")
        if self.disposition is Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS:
            if self.common_witness is None:
                raise ValueError("compatible disposition requires a witness")
            if self.separation_lower_bound != 0.0 or self.separation_upper_bound != 0.0:
                raise ValueError("a common witness requires zero separation bounds")
            if (
                self.spectral_certificate_point != self.common_witness
                or self.operator_certificate_point != self.common_witness
            ):
                raise ValueError("a common witness must be both certificate points")
        elif self.disposition is (
            Periodic1DAdmissibleSetDisposition.CERTIFIED_SEPARATED
        ):
            if self.common_witness is not None:
                raise ValueError("separated disposition cannot retain a common witness")
            if self.separation_lower_bound <= self.separation_resolution:
                raise ValueError("certified separation must exceed the resolution")
        else:
            if self.common_witness is not None:
                raise ValueError(
                    "unresolved disposition cannot retain a common witness"
                )
            if self.separation_lower_bound > self.separation_resolution:
                raise ValueError(
                    "an unresolved lower bound cannot exceed the resolution"
                )


@dataclass(frozen=True, slots=True)
class Periodic1DConstrainedAdmissibleSetCalculationResult:
    """Retain and correlate all M3 quadratics, cases, and diagnostics.

    The aggregate binds the exact composed M2 result, one invariant spectral quadratic,
    one operator quadratic per frozen angle, and the compatible/separated cases in
    declared order. It checks domain membership, selected angles, locality ranges,
    quadratic/evaluation agreement, threshold feasibility, and separation upper bounds.

    Notes
    -----
    The result applies only to the frozen continuous parameter rectangle and finite
    global-angle family; it carries no material or uncertainty interpretation.
    """

    definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition
    multiband_baseline: Periodic1DMultibandAlignmentCalculationResult
    spectral_loss: Periodic1DQuadraticLoss
    operator_losses: tuple[Periodic1DQuadraticLoss, ...]
    cases: tuple[Periodic1DAdmissibleSetCaseResult, ...]

    def __post_init__(self) -> None:
        """Validate exact baseline composition and declared case inventories."""
        if type(self.definition) is not (
            Periodic1DConstrainedAdmissibleSetCalculationDefinition
        ):
            raise TypeError(
                "definition must be "
                "Periodic1DConstrainedAdmissibleSetCalculationDefinition"
            )
        if type(self.multiband_baseline) is not (
            Periodic1DMultibandAlignmentCalculationResult
        ):
            raise TypeError(
                "multiband_baseline must be "
                "Periodic1DMultibandAlignmentCalculationResult"
            )
        if self.multiband_baseline.definition is not self.definition.multiband_baseline:
            raise ValueError(
                "M3 baseline result must use the exact composed definition"
            )
        if type(self.spectral_loss) is not Periodic1DQuadraticLoss:
            raise TypeError("spectral_loss must be Periodic1DQuadraticLoss")
        if self.spectral_loss.alignment_angle is not None:
            raise ValueError("spectral loss must be alignment-invariant")
        if not isinstance(self.operator_losses, tuple) or any(
            type(item) is not Periodic1DQuadraticLoss for item in self.operator_losses
        ):
            raise TypeError("operator_losses must be a typed tuple")
        if tuple(item.alignment_angle for item in self.operator_losses) != (
            self.definition.alignment_angles
        ):
            raise ValueError("operator losses must match the declared alignment family")
        if not isinstance(self.cases, tuple) or any(
            type(item) is not Periodic1DAdmissibleSetCaseResult for item in self.cases
        ):
            raise TypeError("cases must be a typed tuple")
        if tuple(item.thresholds for item in self.cases) != (
            self.definition.compatible_thresholds,
            self.definition.separated_thresholds,
        ):
            raise ValueError("cases must match the declared threshold order")
        loss_by_angle = {item.alignment_angle: item for item in self.operator_losses}
        tolerance = self.definition.quadratic_absolute_tolerance
        for case in self.cases:
            if not set(case.feasible_operator_component_angles).issubset(
                self.definition.alignment_angles
            ):
                raise ValueError(
                    "feasible components must belong to the alignment family"
                )
            evaluations = [
                case.spectral_certificate_point,
                case.operator_certificate_point,
            ]
            if case.common_witness is not None:
                evaluations.append(case.common_witness)
            for evaluation in evaluations:
                if not self.definition.contains(evaluation.parameter):
                    raise ValueError("certificate points must lie in the frozen domain")
                if evaluation.selected_alignment_angle not in loss_by_angle:
                    raise ValueError(
                        "selected alignment must belong to the frozen family"
                    )
                ranges = tuple(item.maximum_range for item in evaluation.locality)
                if ranges != self.definition.locality_ranges:
                    raise ValueError(
                        "locality diagnostics must match the frozen ranges"
                    )
                spectral_value = self.spectral_loss.rms_loss(evaluation.parameter)
                operator_value = loss_by_angle[
                    evaluation.selected_alignment_angle
                ].rms_loss(evaluation.parameter)
                if (
                    abs(evaluation.training_spectral_rms_loss - spectral_value)
                    > tolerance
                    or abs(evaluation.training_operator_rms_loss - operator_value)
                    > tolerance
                ):
                    raise ValueError(
                        "training diagnostics must match retained quadratics"
                    )
            if (
                case.spectral_certificate_point.training_spectral_rms_loss
                > case.thresholds.spectral_rms_threshold + tolerance
            ):
                raise ValueError(
                    "spectral certificate point must be threshold-feasible"
                )
            if (
                case.operator_certificate_point.training_operator_rms_loss
                > case.thresholds.operator_rms_threshold + tolerance
            ):
                raise ValueError(
                    "operator certificate point must be threshold-feasible"
                )
            feasible_distance = float(
                np.linalg.norm(
                    np.asarray(case.spectral_certificate_point.parameter)
                    - np.asarray(case.operator_certificate_point.parameter)
                )
            )
            if abs(case.separation_upper_bound - feasible_distance) > tolerance:
                raise ValueError(
                    "separation upper bound must come from certificate points"
                )
            if case.common_witness is not None and (
                case.common_witness.training_spectral_rms_loss
                > case.thresholds.spectral_rms_threshold + tolerance
                or case.common_witness.training_operator_rms_loss
                > case.thresholds.operator_rms_threshold + tolerance
            ):
                raise ValueError("common witness must satisfy both thresholds")


__all__ = [
    "Periodic1DAdmissibleSetCaseResult",
    "Periodic1DAdmissibleSetDisposition",
    "Periodic1DAdmissibleSetLocalityResult",
    "Periodic1DAdmissibleSetParameterEvaluation",
    "Periodic1DConstrainedAdmissibleSetCalculationResult",
    "Periodic1DQuadraticLoss",
]
