"""Typed results for constrained rank-two admissible-set analysis."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Self

import numpy as np

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..rank2.band_alignment.composite import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)
from .definition import (
    Periodic1DAdmissibleSetThresholds,
    Periodic1DConstrainedAdmissibleSetConfiguration,
)


def _finite_nonnegative(name: str, value: float) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _parameter(name: str, value: tuple[float, float]) -> None:
    if (
        not isinstance(value, tuple)
        or len(value) != 2
        or any(type(item) is not float for item in value)
    ):
        raise TypeError(f"{name} must be a length-two tuple of built-in floats")
    if any(not isfinite(item) for item in value):
        raise ValueError(f"{name} must contain finite values")


class Periodic1DAdmissibleSetDisposition(Enum):
    """Bounded mathematical outcome for one frozen threshold pair."""

    COMPATIBLE_WITNESS = "compatible-witness"
    CERTIFIED_SEPARATED = "certified-separated"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class Periodic1DQuadraticLoss(BaseTypedRecord):
    """Represent one dimensionless squared RMS loss as a centered quadratic."""

    channel_id: str
    alignment_angle: float | None
    center: tuple[float, float]
    quadratic_matrix: tuple[tuple[float, float], tuple[float, float]]
    minimum_squared_loss: float

    def __post_init__(self) -> None:
        if type(self.channel_id) is not str or not self.channel_id:
            raise ValueError("channel_id must be a nonempty built-in string")
        if self.alignment_angle is not None and (
            type(self.alignment_angle) is not float
            or not isfinite(self.alignment_angle)
        ):
            raise ValueError("alignment_angle must be finite or None")
        _parameter("center", self.center)
        if (
            not isinstance(self.quadratic_matrix, tuple)
            or len(self.quadratic_matrix) != 2
            or any(
                not isinstance(row, tuple) or len(row) != 2
                for row in self.quadratic_matrix
            )
        ):
            raise TypeError("quadratic_matrix must contain two length-two rows")
        entries = tuple(entry for row in self.quadratic_matrix for entry in row)
        if any(type(entry) is not float for entry in entries):
            raise TypeError("quadratic_matrix must contain built-in floats")
        if any(not isfinite(entry) for entry in entries):
            raise ValueError("quadratic_matrix must contain finite values")
        matrix = np.asarray(self.quadratic_matrix, dtype=np.float64)
        if not np.array_equal(matrix, matrix.T):
            raise ValueError("quadratic_matrix must be exactly symmetric")
        if float(np.min(np.linalg.eigvalsh(matrix))) <= 0.0:
            raise ValueError("quadratic_matrix must be positive definite")
        _finite_nonnegative("minimum_squared_loss", self.minimum_squared_loss)

    def squared_loss(self, parameter: tuple[float, float]) -> float:
        _parameter("parameter", parameter)
        delta = np.asarray(parameter) - np.asarray(self.center)
        return float(
            self.minimum_squared_loss
            + delta @ np.asarray(self.quadratic_matrix) @ delta
        )

    def rms_loss(self, parameter: tuple[float, float]) -> float:
        return float(np.sqrt(max(0.0, self.squared_loss(parameter))))

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "channel_id": self.channel_id,
            "alignment_angle": self.alignment_angle,
            "center": self.center,
            "quadratic_matrix": self.quadratic_matrix,
            "minimum_squared_loss": self.minimum_squared_loss,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "channel_id",
            "alignment_angle",
            "center",
            "quadratic_matrix",
            "minimum_squared_loss",
        }:
            raise ValueError("quadratic-loss fields do not match")
        channel = values["channel_id"]
        angle = values["alignment_angle"]
        center = values["center"]
        matrix = values["quadratic_matrix"]
        minimum = values["minimum_squared_loss"]
        if (
            type(channel) is not str
            or (angle is not None and type(angle) is not float)
            or not isinstance(center, tuple)
            or len(center) != 2
            or any(type(item) is not float for item in center)
            or not isinstance(matrix, tuple)
            or len(matrix) != 2
            or type(minimum) is not float
        ):
            raise TypeError("quadratic-loss fields decode to wrong types")
        rows: list[tuple[float, float]] = []
        for row in matrix:
            if (
                not isinstance(row, tuple)
                or len(row) != 2
                or any(type(item) is not float for item in row)
            ):
                raise TypeError("quadratic matrix rows must decode to float pairs")
            rows.append(row)
        return cls(channel, angle, center, (rows[0], rows[1]), minimum)


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetLocalityResult(BaseTypedRecord):
    """Retain separate cyclic-conversion and ordinary-tail locality channels."""

    maximum_range: int
    reference_cyclic_conversion_power: float
    attacked_cyclic_conversion_power: float
    candidate_cyclic_conversion_power: float
    reference_ordinary_omitted_block_l2_norm: float
    attacked_ordinary_omitted_block_l2_norm: float
    candidate_ordinary_omitted_block_l2_norm: float

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int or self.maximum_range < 0:
            raise ValueError("maximum_range must be a nonnegative built-in int")
        _finite_nonnegative(
            "reference_cyclic_conversion_power",
            self.reference_cyclic_conversion_power,
        )
        _finite_nonnegative(
            "attacked_cyclic_conversion_power",
            self.attacked_cyclic_conversion_power,
        )
        _finite_nonnegative(
            "candidate_cyclic_conversion_power",
            self.candidate_cyclic_conversion_power,
        )
        _finite_nonnegative(
            "reference_ordinary_omitted_block_l2_norm",
            self.reference_ordinary_omitted_block_l2_norm,
        )
        _finite_nonnegative(
            "attacked_ordinary_omitted_block_l2_norm",
            self.attacked_ordinary_omitted_block_l2_norm,
        )
        _finite_nonnegative(
            "candidate_ordinary_omitted_block_l2_norm",
            self.candidate_ordinary_omitted_block_l2_norm,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_range": self.maximum_range,
            "reference_cyclic_conversion_power": (
                self.reference_cyclic_conversion_power
            ),
            "attacked_cyclic_conversion_power": self.attacked_cyclic_conversion_power,
            "candidate_cyclic_conversion_power": (
                self.candidate_cyclic_conversion_power
            ),
            "reference_ordinary_omitted_block_l2_norm": (
                self.reference_ordinary_omitted_block_l2_norm
            ),
            "attacked_ordinary_omitted_block_l2_norm": (
                self.attacked_ordinary_omitted_block_l2_norm
            ),
            "candidate_ordinary_omitted_block_l2_norm": (
                self.candidate_ordinary_omitted_block_l2_norm
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "maximum_range",
            "reference_cyclic_conversion_power",
            "attacked_cyclic_conversion_power",
            "candidate_cyclic_conversion_power",
            "reference_ordinary_omitted_block_l2_norm",
            "attacked_ordinary_omitted_block_l2_norm",
            "candidate_ordinary_omitted_block_l2_norm",
        }
        if set(values) != required:
            raise ValueError("locality-result fields do not match")
        maximum_range = values["maximum_range"]
        reference_conversion = values["reference_cyclic_conversion_power"]
        attacked_conversion = values["attacked_cyclic_conversion_power"]
        candidate_conversion = values["candidate_cyclic_conversion_power"]
        reference_tail = values["reference_ordinary_omitted_block_l2_norm"]
        attacked_tail = values["attacked_ordinary_omitted_block_l2_norm"]
        candidate_tail = values["candidate_ordinary_omitted_block_l2_norm"]
        if (
            type(maximum_range) is not int
            or type(reference_conversion) is not float
            or type(attacked_conversion) is not float
            or type(candidate_conversion) is not float
            or type(reference_tail) is not float
            or type(attacked_tail) is not float
            or type(candidate_tail) is not float
        ):
            raise TypeError("locality-result fields decode to wrong types")
        return cls(
            maximum_range,
            reference_conversion,
            attacked_conversion,
            candidate_conversion,
            reference_tail,
            attacked_tail,
            candidate_tail,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetParameterEvaluation(BaseTypedRecord):
    """Retain training-selected and evaluation-only diagnostics for one point."""

    role: str
    parameter: tuple[float, float]
    selected_alignment_angle: float
    training_spectral_rms_loss: float
    training_operator_rms_loss: float
    evaluation_spectral_rms_loss: float
    evaluation_operator_rms_loss: float
    locality: tuple[Periodic1DAdmissibleSetLocalityResult, ...]

    def __post_init__(self) -> None:
        if type(self.role) is not str or not self.role:
            raise ValueError("role must be a nonempty built-in string")
        _parameter("parameter", self.parameter)
        if type(self.selected_alignment_angle) is not float or not isfinite(
            self.selected_alignment_angle
        ):
            raise ValueError("selected_alignment_angle must be finite")
        _finite_nonnegative(
            "training_spectral_rms_loss", self.training_spectral_rms_loss
        )
        _finite_nonnegative(
            "training_operator_rms_loss", self.training_operator_rms_loss
        )
        _finite_nonnegative(
            "evaluation_spectral_rms_loss", self.evaluation_spectral_rms_loss
        )
        _finite_nonnegative(
            "evaluation_operator_rms_loss", self.evaluation_operator_rms_loss
        )
        if not isinstance(self.locality, tuple) or any(
            type(item) is not Periodic1DAdmissibleSetLocalityResult
            for item in self.locality
        ):
            raise TypeError("locality must be a typed tuple")
        if not self.locality:
            raise ValueError("locality must not be empty")
        ranges = tuple(item.maximum_range for item in self.locality)
        if tuple(sorted(set(ranges))) != ranges:
            raise ValueError("locality ranges must be unique and increasing")
        conversion_channels = (
            tuple(item.reference_cyclic_conversion_power for item in self.locality),
            tuple(item.attacked_cyclic_conversion_power for item in self.locality),
            tuple(item.candidate_cyclic_conversion_power for item in self.locality),
        )
        if any(len(set(channel)) != 1 for channel in conversion_channels):
            raise ValueError(
                "cyclic conversion power must not depend on truncation range"
            )
        ordinary_tail_channels = (
            tuple(
                item.reference_ordinary_omitted_block_l2_norm for item in self.locality
            ),
            tuple(
                item.attacked_ordinary_omitted_block_l2_norm for item in self.locality
            ),
            tuple(
                item.candidate_ordinary_omitted_block_l2_norm for item in self.locality
            ),
        )
        if any(
            any(right > left for left, right in zip(channel, channel[1:], strict=False))
            for channel in ordinary_tail_channels
        ):
            raise ValueError("ordinary omitted-tail norms must be nonincreasing")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "role": self.role,
            "parameter": self.parameter,
            "selected_alignment_angle": self.selected_alignment_angle,
            "training_spectral_rms_loss": self.training_spectral_rms_loss,
            "training_operator_rms_loss": self.training_operator_rms_loss,
            "evaluation_spectral_rms_loss": self.evaluation_spectral_rms_loss,
            "evaluation_operator_rms_loss": self.evaluation_operator_rms_loss,
            "locality": self.locality,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "role",
            "parameter",
            "selected_alignment_angle",
            "training_spectral_rms_loss",
            "training_operator_rms_loss",
            "evaluation_spectral_rms_loss",
            "evaluation_operator_rms_loss",
            "locality",
        }
        if set(values) != required:
            raise ValueError("parameter-evaluation fields do not match")
        role = values["role"]
        parameter = values["parameter"]
        locality = values["locality"]
        selected_angle = values["selected_alignment_angle"]
        training_spectral = values["training_spectral_rms_loss"]
        training_operator = values["training_operator_rms_loss"]
        evaluation_spectral = values["evaluation_spectral_rms_loss"]
        evaluation_operator = values["evaluation_operator_rms_loss"]
        if (
            type(role) is not str
            or not isinstance(parameter, tuple)
            or len(parameter) != 2
            or any(type(item) is not float for item in parameter)
            or not isinstance(locality, tuple)
            or type(selected_angle) is not float
            or type(training_spectral) is not float
            or type(training_operator) is not float
            or type(evaluation_spectral) is not float
            or type(evaluation_operator) is not float
        ):
            raise TypeError("parameter-evaluation fields decode to wrong types")
        decoded: list[Periodic1DAdmissibleSetLocalityResult] = []
        for item in locality:
            if not isinstance(item, Mapping):
                raise TypeError("locality entries must decode to mappings")
            decoded.append(Periodic1DAdmissibleSetLocalityResult.from_dict(item))
        return cls(
            role,
            parameter,
            selected_angle,
            training_spectral,
            training_operator,
            evaluation_spectral,
            evaluation_operator,
            tuple(decoded),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetCaseResult(BaseTypedRecord):
    """Retain a constructive witness or bounded separation certificate."""

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
        if (
            type(self.thresholds) is not Periodic1DAdmissibleSetThresholds
            or type(self.disposition) is not Periodic1DAdmissibleSetDisposition
        ):
            raise TypeError("case identity values have the wrong exact types")
        if (
            not isinstance(self.feasible_operator_component_angles, tuple)
            or not self.feasible_operator_component_angles
            or any(
                type(value) is not float or not isfinite(value)
                for value in self.feasible_operator_component_angles
            )
        ):
            raise TypeError("feasible component angles must be a nonempty float tuple")
        if (
            tuple(sorted(set(self.feasible_operator_component_angles)))
            != self.feasible_operator_component_angles
        ):
            raise ValueError("feasible component angles must be unique and increasing")
        if (
            self.common_witness is not None
            and type(self.common_witness)
            is not Periodic1DAdmissibleSetParameterEvaluation
        ):
            raise TypeError("common_witness has the wrong exact type")
        if (
            type(self.spectral_certificate_point)
            is not Periodic1DAdmissibleSetParameterEvaluation
            or type(self.operator_certificate_point)
            is not Periodic1DAdmissibleSetParameterEvaluation
        ):
            raise TypeError("certificate points have the wrong exact types")
        _finite_nonnegative("separation_lower_bound", self.separation_lower_bound)
        _finite_nonnegative("separation_upper_bound", self.separation_upper_bound)
        _finite_nonnegative("separation_resolution", self.separation_resolution)
        if self.separation_lower_bound > self.separation_upper_bound:
            raise ValueError("separation bounds are reversed")
        if self.disposition is Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS:
            if (
                self.common_witness is None
                or self.separation_lower_bound != 0.0
                or self.separation_upper_bound != 0.0
            ):
                raise ValueError(
                    "compatible disposition requires one zero-distance witness"
                )
            if (
                self.spectral_certificate_point != self.common_witness
                or self.operator_certificate_point != self.common_witness
            ):
                raise ValueError("common witness must be both certificate points")
        elif self.disposition is Periodic1DAdmissibleSetDisposition.CERTIFIED_SEPARATED:
            if (
                self.common_witness is not None
                or self.separation_lower_bound <= self.separation_resolution
            ):
                raise ValueError(
                    "separated disposition requires a resolved lower bound"
                )
        elif (
            self.common_witness is not None
            or self.separation_lower_bound > self.separation_resolution
        ):
            raise ValueError("unresolved disposition has inconsistent evidence")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "thresholds": self.thresholds,
            "disposition": self.disposition.value,
            "feasible_operator_component_angles": (
                self.feasible_operator_component_angles
            ),
            "common_witness": self.common_witness,
            "spectral_certificate_point": self.spectral_certificate_point,
            "operator_certificate_point": self.operator_certificate_point,
            "separation_lower_bound": self.separation_lower_bound,
            "separation_upper_bound": self.separation_upper_bound,
            "separation_resolution": self.separation_resolution,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "thresholds",
            "disposition",
            "feasible_operator_component_angles",
            "common_witness",
            "spectral_certificate_point",
            "operator_certificate_point",
            "separation_lower_bound",
            "separation_upper_bound",
            "separation_resolution",
        }
        if set(values) != required:
            raise ValueError("case fields do not match")
        thresholds = values["thresholds"]
        disposition = values["disposition"]
        angles = values["feasible_operator_component_angles"]
        common = values["common_witness"]
        spectral = values["spectral_certificate_point"]
        operator = values["operator_certificate_point"]
        if (
            not isinstance(thresholds, Mapping)
            or type(disposition) is not str
            or not isinstance(angles, tuple)
            or any(type(item) is not float for item in angles)
            or (common is not None and not isinstance(common, Mapping))
            or not isinstance(spectral, Mapping)
            or not isinstance(operator, Mapping)
        ):
            raise TypeError("case fields decode to wrong types")
        separation_lower_bound = values["separation_lower_bound"]
        separation_upper_bound = values["separation_upper_bound"]
        separation_resolution = values["separation_resolution"]
        if (
            type(separation_lower_bound) is not float
            or type(separation_upper_bound) is not float
            or type(separation_resolution) is not float
        ):
            raise TypeError("separation values must decode to floats")
        return cls(
            Periodic1DAdmissibleSetThresholds.from_dict(thresholds),
            Periodic1DAdmissibleSetDisposition(disposition),
            angles,
            None
            if common is None
            else Periodic1DAdmissibleSetParameterEvaluation.from_dict(common),
            Periodic1DAdmissibleSetParameterEvaluation.from_dict(spectral),
            Periodic1DAdmissibleSetParameterEvaluation.from_dict(operator),
            separation_lower_bound,
            separation_upper_bound,
            separation_resolution,
        )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DConstrainedAdmissibleSetCalculationResult(BaseTypedRecord):
    """Retain M3 proof objects and the exact canonical composite baseline."""

    configuration: Periodic1DConstrainedAdmissibleSetConfiguration
    composite_baseline: Periodic1DCompositeBandAlignmentCalculationResult
    spectral_loss: Periodic1DQuadraticLoss
    operator_losses: tuple[Periodic1DQuadraticLoss, ...]
    cases: tuple[Periodic1DAdmissibleSetCaseResult, ...]

    def __post_init__(self) -> None:
        if (
            type(self.configuration)
            is not Periodic1DConstrainedAdmissibleSetConfiguration
            or type(self.composite_baseline)
            is not Periodic1DCompositeBandAlignmentCalculationResult
        ):
            raise TypeError("configuration or composite baseline has the wrong type")
        if (
            hashlib.sha256(self.composite_baseline.to_json()).hexdigest()
            != self.configuration.upstream_result_sha256
        ):
            raise ValueError(
                "embedded upstream result differs from its configured digest"
            )
        if (
            type(self.spectral_loss) is not Periodic1DQuadraticLoss
            or self.spectral_loss.alignment_angle is not None
        ):
            raise ValueError("spectral_loss must be an invariant quadratic")
        if not isinstance(self.operator_losses, tuple) or any(
            type(item) is not Periodic1DQuadraticLoss for item in self.operator_losses
        ):
            raise TypeError("operator_losses must be a typed tuple")
        if (
            tuple(item.alignment_angle for item in self.operator_losses)
            != self.configuration.alignment_angles
        ):
            raise ValueError("operator losses must match the alignment family")
        if not isinstance(self.cases, tuple) or any(
            type(item) is not Periodic1DAdmissibleSetCaseResult for item in self.cases
        ):
            raise TypeError("cases must be a typed tuple")
        if tuple(item.thresholds for item in self.cases) != (
            self.configuration.compatible_thresholds,
            self.configuration.separated_thresholds,
        ):
            raise ValueError("cases must match the configured threshold order")
        compatible_case, separated_case = self.cases
        if (
            compatible_case.spectral_certificate_point.role
            != "compatible-common-witness"
            or compatible_case.operator_certificate_point.role
            != "compatible-common-witness"
            or separated_case.spectral_certificate_point.role
            != "separated-spectral-boundary"
            or separated_case.operator_certificate_point.role
            != "separated-operator-boundary"
        ):
            raise ValueError("case evaluation roles must match the proof inventory")
        if compatible_case.common_witness is None:
            raise ValueError("compatible case must retain its common witness")
        if (
            compatible_case.common_witness.training_spectral_rms_loss
            > compatible_case.thresholds.spectral_rms_threshold
            or compatible_case.common_witness.training_operator_rms_loss
            > compatible_case.thresholds.operator_rms_threshold
        ):
            raise ValueError("compatible witness must satisfy both thresholds")
        losses = {item.alignment_angle: item for item in self.operator_losses}
        tolerance = self.configuration.quadratic_absolute_tolerance
        for case in self.cases:
            evaluations = [
                case.spectral_certificate_point,
                case.operator_certificate_point,
            ]
            if case.common_witness is not None:
                evaluations.append(case.common_witness)
            for evaluation in evaluations:
                if (
                    not self.configuration.contains(evaluation.parameter)
                    or evaluation.selected_alignment_angle not in losses
                ):
                    raise ValueError("evaluation must belong to the configured domain")
                if (
                    tuple(item.maximum_range for item in evaluation.locality)
                    != self.configuration.locality_ranges
                ):
                    raise ValueError(
                        "locality diagnostics must match configured ranges"
                    )
                if (
                    abs(
                        evaluation.training_spectral_rms_loss
                        - self.spectral_loss.rms_loss(evaluation.parameter)
                    )
                    > tolerance
                    or abs(
                        evaluation.training_operator_rms_loss
                        - losses[evaluation.selected_alignment_angle].rms_loss(
                            evaluation.parameter
                        )
                    )
                    > tolerance
                ):
                    raise ValueError(
                        "training diagnostics must match retained quadratics"
                    )
            distance = float(
                np.linalg.norm(
                    np.asarray(case.spectral_certificate_point.parameter)
                    - np.asarray(case.operator_certificate_point.parameter)
                )
            )
            if abs(case.separation_upper_bound - distance) > tolerance:
                raise ValueError("separation upper bound must match certificate points")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "configuration": self.configuration,
            "composite_baseline": self.composite_baseline,
            "spectral_loss": self.spectral_loss,
            "operator_losses": self.operator_losses,
            "cases": self.cases,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "configuration",
            "composite_baseline",
            "spectral_loss",
            "operator_losses",
            "cases",
        }:
            raise ValueError("result fields do not match")
        configuration = values["configuration"]
        baseline = values["composite_baseline"]
        spectral = values["spectral_loss"]
        operators = values["operator_losses"]
        cases = values["cases"]
        if (
            not isinstance(configuration, Mapping)
            or not isinstance(baseline, Mapping)
            or not isinstance(spectral, Mapping)
            or not isinstance(operators, tuple)
            or not isinstance(cases, tuple)
        ):
            raise TypeError("result fields decode to wrong types")
        decoded_operators: list[Periodic1DQuadraticLoss] = []
        for item in operators:
            if not isinstance(item, Mapping):
                raise TypeError("operator losses must decode to mappings")
            decoded_operators.append(Periodic1DQuadraticLoss.from_dict(item))
        decoded_cases: list[Periodic1DAdmissibleSetCaseResult] = []
        for item in cases:
            if not isinstance(item, Mapping):
                raise TypeError("cases must decode to mappings")
            decoded_cases.append(Periodic1DAdmissibleSetCaseResult.from_dict(item))
        return cls(
            Periodic1DConstrainedAdmissibleSetConfiguration.from_dict(configuration),
            Periodic1DCompositeBandAlignmentCalculationResult.from_dict(baseline),
            Periodic1DQuadraticLoss.from_dict(spectral),
            tuple(decoded_operators),
            tuple(decoded_cases),
        )


__all__ = [
    "Periodic1DAdmissibleSetCaseResult",
    "Periodic1DAdmissibleSetDisposition",
    "Periodic1DAdmissibleSetLocalityResult",
    "Periodic1DAdmissibleSetParameterEvaluation",
    "Periodic1DConstrainedAdmissibleSetCalculationResult",
    "Periodic1DQuadraticLoss",
]
