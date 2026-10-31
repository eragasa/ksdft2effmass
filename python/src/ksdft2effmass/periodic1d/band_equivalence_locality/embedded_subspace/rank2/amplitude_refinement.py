"""Adaptive amplitude refinement for the embedded-subspace rank-two control."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from itertools import pairwise
from typing import final

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.numerical_consistency import NumericalConsistency

from .analysis import (
    Periodic1DEmbeddedSubspaceRank2Analyzer,
    _Periodic1DEmbeddedSubspaceRank2PreparedAnalysis,
)
from .request import Periodic1DEmbeddedSubspaceRank2Request
from .results import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2PointAnalysis,
)
from .transport import _Periodic1DEmbeddedSubspaceRank2UnqualifiedPreparation


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds:
    """Declare separate direct interpolation-defect thresholds."""

    maximum_correlation_defect: float
    maximum_operator_threshold_defect: float
    maximum_joint_threshold_defect: float
    maximum_hopping_weight_defect: float
    maximum_hopping_power_defect: float

    def __post_init__(self) -> None:
        for name in (
            "maximum_correlation_defect",
            "maximum_operator_threshold_defect",
            "maximum_joint_threshold_defect",
            "maximum_hopping_weight_defect",
            "maximum_hopping_power_defect",
        ):
            value = getattr(self, name)
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest:
    """Bind deterministic midpoint refinement to one fixed momentum calculation."""

    template_request: Periodic1DEmbeddedSubspaceRank2Request
    thresholds: Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds
    maximum_refinement_levels: int
    maximum_evaluated_amplitudes: int

    def __post_init__(self) -> None:
        if type(self.template_request) is not Periodic1DEmbeddedSubspaceRank2Request:
            raise TypeError(
                "template_request must be Periodic1DEmbeddedSubspaceRank2Request"
            )
        if self.template_request.amplitudes[-1] != math.pi / 4.0:
            raise ValueError("template amplitudes must span exactly through pi/4")
        if type(self.thresholds) is not (
            Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds
        ):
            raise TypeError("thresholds must be amplitude-refinement thresholds")
        if type(self.maximum_refinement_levels) is not int:
            raise TypeError("maximum_refinement_levels must be a built-in int")
        if self.maximum_refinement_levels < 1:
            raise ValueError("maximum_refinement_levels must be positive")
        if type(self.maximum_evaluated_amplitudes) is not int:
            raise TypeError("maximum_evaluated_amplitudes must be a built-in int")
        first_inventory_size = 2 * len(self.template_request.amplitudes) - 1
        if self.maximum_evaluated_amplitudes < first_inventory_size:
            raise ValueError(
                "maximum_evaluated_amplitudes cannot hold the first midpoint inventory"
            )

    def evaluation_request(
        self, amplitudes: tuple[float, ...]
    ) -> Periodic1DEmbeddedSubspaceRank2Request:
        """Return a request changing only the direct amplitude inventory."""
        return replace(self.template_request, amplitudes=amplitudes)


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel:
    """Retain direct midpoint interpolation defects for one adaptive level."""

    level_index: int
    interpolation_nodes: tuple[float, ...]
    evaluated_amplitudes: tuple[float, ...]
    maximum_correlation_defect: float
    maximum_operator_threshold_defect: float
    maximum_joint_threshold_defect: float
    maximum_hopping_weight_defect: float
    maximum_hopping_power_defect: float
    failing_interval_indices: tuple[int, ...]
    within_tolerances: bool

    def __post_init__(self) -> None:
        _validate_level_identity(
            self.level_index,
            self.interpolation_nodes,
            self.evaluated_amplitudes,
            validation=False,
        )
        _validate_defects(self)
        _validate_failure_indices(
            self.failing_interval_indices,
            len(self.interpolation_nodes) - 1,
            "failing_interval_indices",
        )
        if type(self.within_tolerances) is not bool:
            raise TypeError("within_tolerances must be a built-in bool")
        if self.within_tolerances is not (not self.failing_interval_indices):
            raise ValueError("within_tolerances must match failing_interval_indices")

    @property
    def failing_interval_count(self) -> int:
        """Return the number of intervals selected for refinement."""
        return len(self.failing_interval_indices)


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AmplitudeValidation:
    """Retain disjoint quarter-point validation for one frozen node inventory."""

    level_index: int
    interpolation_nodes: tuple[float, ...]
    evaluated_amplitudes: tuple[float, ...]
    maximum_correlation_defect: float
    maximum_operator_threshold_defect: float
    maximum_joint_threshold_defect: float
    maximum_hopping_weight_defect: float
    maximum_hopping_power_defect: float
    failing_point_indices: tuple[int, ...]
    within_tolerances: bool

    def __post_init__(self) -> None:
        _validate_level_identity(
            self.level_index,
            self.interpolation_nodes,
            self.evaluated_amplitudes,
            validation=True,
        )
        _validate_defects(self)
        _validate_failure_indices(
            self.failing_point_indices,
            len(self.evaluated_amplitudes),
            "failing_point_indices",
        )
        if type(self.within_tolerances) is not bool:
            raise TypeError("within_tolerances must be a built-in bool")
        if self.within_tolerances is not (not self.failing_point_indices):
            raise ValueError("within_tolerances must match failing_point_indices")

    @property
    def failing_point_count(self) -> int:
        """Return the number of validation samples selected for refinement."""
        return len(self.failing_point_indices)


class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis(NumericalConsistency):
    """Identify one closed adaptive-amplitude outcome variant."""

    __slots__ = ()

    request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest
    evaluations: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]

    @property
    @final
    def converged(self) -> bool:
        """Return whether midpoint and disjoint validation checks passed."""
        return type(self) is Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged

    @property
    @final
    def all_evaluated_points(
        self,
    ) -> tuple[Periodic1DEmbeddedSubspaceRank2PointAnalysis, ...]:
        """Project the unique direct points from the retained evaluations."""
        points = {
            point.amplitude: point
            for analysis in self.evaluations
            for point in analysis.points
        }
        return tuple(points[amplitude] for amplitude in sorted(points))


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped(
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis
):
    """Retain the evaluated request whose parent qualification stopped refinement."""

    request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest
    evaluations: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]

    def __post_init__(self) -> None:
        _validate_evaluations(self.request, self.evaluations)
        if self.evaluations[-1].qualification.qualified:
            raise ValueError(
                "qualification-stopped outcome requires an unqualified result"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged(
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis
):
    """Retain a midpoint-stable inventory with passing disjoint quarter points."""

    request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest
    evaluations: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    levels: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel, ...]
    validations: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation, ...]

    def __post_init__(self) -> None:
        _validate_qualified_outcome(self)
        if not self.levels[-1].within_tolerances:
            raise ValueError("converged outcome requires a passing midpoint level")
        if not self.validations:
            raise ValueError("converged outcome requires disjoint validation")
        final_validation = self.validations[-1]
        if (
            final_validation.level_index != self.levels[-1].level_index
            or not final_validation.within_tolerances
        ):
            raise ValueError("converged outcome requires passing final validation")


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted(
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis
):
    """Retain an unresolved study that reached its declared refinement-level cap."""

    request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest
    evaluations: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    levels: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel, ...]
    validations: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation, ...]

    def __post_init__(self) -> None:
        _validate_qualified_outcome(self)
        if len(self.levels) != self.request.maximum_refinement_levels:
            raise ValueError("levels-exhausted outcome must reach the declared cap")
        if _final_amplitude_checks_pass(self.levels, self.validations):
            raise ValueError("passing final checks require the converged variant")


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted(
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis
):
    """Retain an unresolved study stopped before exceeding its sample cap."""

    request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest
    evaluations: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    levels: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel, ...]
    validations: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation, ...]
    blocked_amplitudes: tuple[float, ...]

    def __post_init__(self) -> None:
        _validate_qualified_outcome(self)
        _validate_amplitudes(self.blocked_amplitudes, "blocked_amplitudes")
        current = {point.amplitude for point in self.all_evaluated_points}
        new = set(self.blocked_amplitudes) - current
        if len(current) + len(new) <= self.request.maximum_evaluated_amplitudes:
            raise ValueError("blocked amplitudes must exceed the declared sample cap")


_QualifiedAdaptiveAmplitudeAnalysis = (
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged
    | Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted
    | Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted
)


def _validate_amplitudes(values: tuple[float, ...], name: str) -> None:
    if type(values) is not tuple or len(values) < 2:
        raise TypeError(f"{name} must contain at least two built-in floats")
    for value in values:
        if type(value) is not float:
            raise TypeError(f"{name} must contain built-in floats")
        if not math.isfinite(value) or not 0.0 <= value <= math.pi / 4.0:
            raise ValueError(f"{name} must lie in [0, pi/4]")
    if tuple(sorted(set(values))) != values:
        raise ValueError(f"{name} must be unique and increasing")


def _validate_level_identity(
    level_index: int,
    nodes: tuple[float, ...],
    evaluated: tuple[float, ...],
    *,
    validation: bool,
) -> None:
    if type(level_index) is not int or level_index < 0:
        raise ValueError("level_index must be a nonnegative built-in int")
    _validate_amplitudes(nodes, "interpolation_nodes")
    _validate_amplitudes(evaluated, "evaluated_amplitudes")
    if validation:
        expected = tuple(
            sample
            for left, right in pairwise(nodes)
            for sample in (
                left + 0.25 * (right - left),
                left + 0.75 * (right - left),
            )
        )
        if evaluated != expected:
            raise ValueError("validation must contain two quarter points per interval")
        if set(evaluated) & set(nodes):
            raise ValueError("validation amplitudes must be disjoint from nodes")
        return
    midpoints = tuple(0.5 * (left + right) for left, right in pairwise(nodes))
    expected = tuple(sorted(set(nodes) | set(midpoints)))
    if evaluated != expected:
        raise ValueError("level evaluation must contain every interval midpoint")


def _validate_failure_indices(
    indices: tuple[int, ...],
    inventory_size: int,
    name: str,
) -> None:
    if type(indices) is not tuple or any(type(index) is not int for index in indices):
        raise TypeError(f"{name} must be a tuple of built-in ints")
    if tuple(sorted(set(indices))) != indices:
        raise ValueError(f"{name} must be unique and increasing")
    if any(index < 0 or index >= inventory_size for index in indices):
        raise ValueError(f"{name} exceeds its inventory")


def _validate_defects(
    value: (
        Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel
        | Periodic1DEmbeddedSubspaceRank2AmplitudeValidation
    ),
) -> None:
    for name in (
        "maximum_correlation_defect",
        "maximum_operator_threshold_defect",
        "maximum_joint_threshold_defect",
        "maximum_hopping_weight_defect",
        "maximum_hopping_power_defect",
    ):
        defect = getattr(value, name)
        if type(defect) is not float:
            raise TypeError(f"{name} must be a built-in float")
        if not math.isfinite(defect) or defect < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")


def _validate_evaluations(
    request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest,
    evaluations: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...],
) -> None:
    if type(request) is not Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest:
        raise TypeError("request must be an adaptive-amplitude request")
    if (
        type(evaluations) is not tuple
        or not evaluations
        or any(
            type(item) is not Periodic1DEmbeddedSubspaceRank2Analysis
            for item in evaluations
        )
    ):
        raise TypeError("evaluations must be a nonempty typed tuple")
    template = request.template_request
    for analysis in evaluations:
        if replace(analysis.request, amplitudes=template.amplitudes) != template:
            raise ValueError("evaluation changes a non-amplitude control")


def _validate_qualified_outcome(value: _QualifiedAdaptiveAmplitudeAnalysis) -> None:
    _validate_evaluations(value.request, value.evaluations)
    if not all(item.qualification.qualified for item in value.evaluations):
        raise ValueError("qualified adaptive outcome requires qualified evaluations")
    if (
        type(value.levels) is not tuple
        or not value.levels
        or any(
            type(item) is not Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel
            for item in value.levels
        )
    ):
        raise TypeError("levels must be a nonempty typed tuple")
    if len(value.levels) > value.request.maximum_refinement_levels:
        raise ValueError("levels exceed maximum_refinement_levels")
    if tuple(item.level_index for item in value.levels) != tuple(
        range(len(value.levels))
    ):
        raise ValueError("levels must have contiguous zero-based identities")
    if type(value.validations) is not tuple or any(
        type(item) is not Periodic1DEmbeddedSubspaceRank2AmplitudeValidation
        for item in value.validations
    ):
        raise TypeError("validations must be a typed tuple")
    if tuple(item.level_index for item in value.validations) != tuple(
        sorted({item.level_index for item in value.validations})
    ):
        raise ValueError("validations must have unique increasing level identities")
    for level in value.levels:
        expected = _within_thresholds(level, value.request.thresholds)
        if level.within_tolerances is not expected:
            raise ValueError("level disposition does not match amplitude thresholds")
    validation_by_level = {item.level_index: item for item in value.validations}
    for validation in value.validations:
        if validation.level_index >= len(value.levels):
            raise ValueError("validation level identity is out of range")
        if (
            validation.interpolation_nodes
            != value.levels[validation.level_index].interpolation_nodes
        ):
            raise ValueError("validation nodes must match their refinement level")
        expected = _within_thresholds(validation, value.request.thresholds)
        if validation.within_tolerances is not expected:
            raise ValueError(
                "validation disposition does not match amplitude thresholds"
            )
    if value.levels[0].interpolation_nodes != value.request.template_request.amplitudes:
        raise ValueError("first level must use the template amplitude nodes")
    expected_evaluation_inventories: list[tuple[float, ...]] = []
    for index, level in enumerate(value.levels):
        expected_evaluation_inventories.append(level.evaluated_amplitudes)
        matching_validation = validation_by_level.get(level.level_index)
        if matching_validation is not None:
            expected_evaluation_inventories.append(
                tuple(
                    sorted(
                        set(matching_validation.interpolation_nodes)
                        | set(matching_validation.evaluated_amplitudes)
                    )
                )
            )
        if index + 1 < len(value.levels):
            expected_nodes = _refined_nodes(level, matching_validation)
            if value.levels[index + 1].interpolation_nodes != expected_nodes:
                raise ValueError("adaptive interpolation nodes are not nested exactly")
    if tuple(item.request.amplitudes for item in value.evaluations) != tuple(
        expected_evaluation_inventories
    ):
        raise ValueError("evaluations do not match the adaptive level inventories")
    points_by_amplitude: dict[float, Periodic1DEmbeddedSubspaceRank2PointAnalysis] = {}
    for analysis in value.evaluations:
        for point in analysis.points:
            previous = points_by_amplitude.get(point.amplitude)
            if previous is not None and point != previous:
                raise ValueError("repeated direct amplitude evaluations must agree")
            points_by_amplitude[point.amplitude] = point
    if len(points_by_amplitude) > value.request.maximum_evaluated_amplitudes:
        raise ValueError("direct evaluations exceed the declared sample cap")


def _refined_nodes(
    level: Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel,
    validation: Periodic1DEmbeddedSubspaceRank2AmplitudeValidation | None,
) -> tuple[float, ...]:
    nodes = level.interpolation_nodes
    if validation is None:
        midpoints = tuple(0.5 * (left + right) for left, right in pairwise(nodes))
        selected = {midpoints[index] for index in level.failing_interval_indices}
    else:
        selected = {
            validation.evaluated_amplitudes[index]
            for index in validation.failing_point_indices
        }
    return tuple(sorted(set(nodes) | selected))


def _within_thresholds(
    value: (
        Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel
        | Periodic1DEmbeddedSubspaceRank2AmplitudeValidation
    ),
    thresholds: Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds,
) -> bool:
    return all(
        getattr(value, name) <= getattr(thresholds, name)
        for name in (
            "maximum_correlation_defect",
            "maximum_operator_threshold_defect",
            "maximum_joint_threshold_defect",
            "maximum_hopping_weight_defect",
            "maximum_hopping_power_defect",
        )
    )


def _final_amplitude_checks_pass(
    levels: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel, ...],
    validations: tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation, ...],
) -> bool:
    return bool(
        levels[-1].within_tolerances
        and validations
        and validations[-1].level_index == levels[-1].level_index
        and validations[-1].within_tolerances
    )


class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalyzer:
    """Refine failing intervals and validate stable nodes at quarter points."""

    __slots__ = ("_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest:
            raise TypeError("request must be an adaptive-amplitude request")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._transporter = transporter

    def execute(self) -> Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis:
        """Return one explicit qualification, convergence, or cap-stop variant."""
        cache: dict[float, Periodic1DEmbeddedSubspaceRank2PointAnalysis] = {}
        evaluations: list[Periodic1DEmbeddedSubspaceRank2Analysis] = []
        levels: list[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel] = []
        validations: list[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation] = []
        preparation = Periodic1DEmbeddedSubspaceRank2Analyzer(
            request=self._request.template_request,
            transporter=self._transporter,
        )._prepare()

        def evaluate(
            amplitudes: tuple[float, ...],
        ) -> Periodic1DEmbeddedSubspaceRank2Analysis | None:
            new = tuple(amplitude for amplitude in amplitudes if amplitude not in cache)
            if len(cache) + len(new) > self._request.maximum_evaluated_amplitudes:
                return None
            evaluation_request = self._request.evaluation_request(amplitudes)
            if type(preparation) is (
                _Periodic1DEmbeddedSubspaceRank2UnqualifiedPreparation
            ):
                analysis = Periodic1DEmbeddedSubspaceRank2Analysis(
                    request=evaluation_request,
                    qualification=preparation.qualification,
                    points=(),
                )
                evaluations.append(analysis)
                return analysis
            if type(preparation) is not (
                _Periodic1DEmbeddedSubspaceRank2PreparedAnalysis
            ):
                raise TypeError("analysis preparation returned an unknown variant")
            for amplitude in new:
                cache[amplitude] = preparation.point(amplitude)
            analysis = Periodic1DEmbeddedSubspaceRank2Analysis(
                request=evaluation_request,
                qualification=preparation.qualification,
                points=tuple(cache[amplitude] for amplitude in amplitudes),
            )
            evaluations.append(analysis)
            return analysis

        nodes = self._request.template_request.amplitudes
        for level_index in range(self._request.maximum_refinement_levels):
            midpoints = tuple(0.5 * (left + right) for left, right in pairwise(nodes))
            midpoint_inventory = tuple(sorted(set(nodes) | set(midpoints)))
            midpoint_analysis = evaluate(midpoint_inventory)
            if midpoint_analysis is None:
                return self._evaluations_exhausted(
                    evaluations,
                    levels,
                    validations,
                    cache,
                    midpoint_inventory,
                )
            if not midpoint_analysis.qualification.qualified:
                return Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped(  # noqa: E501
                    request=self._request,
                    evaluations=tuple(evaluations),
                )
            midpoint_defects = tuple(
                _interpolation_defects(cache[left], cache[midpoint], cache[right], 0.5)
                for left, midpoint, right in zip(
                    nodes[:-1], midpoints, nodes[1:], strict=True
                )
            )
            midpoint_failing = tuple(
                not _defects_within(defects, self._request.thresholds)
                for defects in midpoint_defects
            )
            level = _level(
                level_index,
                nodes,
                midpoint_inventory,
                midpoint_defects,
                tuple(index for index, failed in enumerate(midpoint_failing) if failed),
            )
            levels.append(level)
            candidate_nodes = tuple(
                sorted(
                    set(nodes)
                    | {
                        midpoint
                        for midpoint, failed in zip(
                            midpoints, midpoint_failing, strict=True
                        )
                        if failed
                    }
                )
            )
            if level.within_tolerances:
                quarter_samples = tuple(
                    sample
                    for left, right in pairwise(nodes)
                    for sample in (
                        left + 0.25 * (right - left),
                        left + 0.75 * (right - left),
                    )
                )
                validation_inventory = tuple(sorted(set(nodes) | set(quarter_samples)))
                validation_analysis = evaluate(validation_inventory)
                if validation_analysis is None:
                    return self._evaluations_exhausted(
                        evaluations,
                        levels,
                        validations,
                        cache,
                        validation_inventory,
                    )
                if not validation_analysis.qualification.qualified:
                    return Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped(  # noqa: E501
                        request=self._request,
                        evaluations=tuple(evaluations),
                    )
                validation_defects = tuple(
                    _interpolation_defects(
                        cache[left], cache[sample], cache[right], fraction
                    )
                    for left, right in pairwise(nodes)
                    for sample, fraction in (
                        (left + 0.25 * (right - left), 0.25),
                        (left + 0.75 * (right - left), 0.75),
                    )
                )
                validation_failing = tuple(
                    not _defects_within(defects, self._request.thresholds)
                    for defects in validation_defects
                )
                validation = _validation(
                    level_index,
                    nodes,
                    quarter_samples,
                    validation_defects,
                    tuple(
                        index
                        for index, failed in enumerate(validation_failing)
                        if failed
                    ),
                )
                validations.append(validation)
                if validation.within_tolerances:
                    return Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged(
                        request=self._request,
                        evaluations=tuple(evaluations),
                        levels=tuple(levels),
                        validations=tuple(validations),
                    )
                candidate_nodes = tuple(
                    sorted(
                        set(nodes)
                        | {
                            sample
                            for sample, failed in zip(
                                quarter_samples,
                                validation_failing,
                                strict=True,
                            )
                            if failed
                        }
                    )
                )
            if level_index + 1 < self._request.maximum_refinement_levels:
                nodes = candidate_nodes
        return Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted(
            request=self._request,
            evaluations=tuple(evaluations),
            levels=tuple(levels),
            validations=tuple(validations),
        )

    def _evaluations_exhausted(
        self,
        evaluations: list[Periodic1DEmbeddedSubspaceRank2Analysis],
        levels: list[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel],
        validations: list[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation],
        cache: dict[float, Periodic1DEmbeddedSubspaceRank2PointAnalysis],
        blocked_amplitudes: tuple[float, ...],
    ) -> Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted:
        if not evaluations or not levels:
            raise RuntimeError(
                "validated sample cap failed to hold the first inventory"
            )
        return Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted(
            request=self._request,
            evaluations=tuple(evaluations),
            levels=tuple(levels),
            validations=tuple(validations),
            blocked_amplitudes=blocked_amplitudes,
        )


def _defects_within(
    defects: tuple[float, float, float, float, float],
    thresholds: Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds,
) -> bool:
    return all(
        defect <= threshold
        for defect, threshold in zip(
            defects,
            (
                thresholds.maximum_correlation_defect,
                thresholds.maximum_operator_threshold_defect,
                thresholds.maximum_joint_threshold_defect,
                thresholds.maximum_hopping_weight_defect,
                thresholds.maximum_hopping_power_defect,
            ),
            strict=True,
        )
    )


def _level(
    level_index: int,
    nodes: tuple[float, ...],
    inventory: tuple[float, ...],
    defects: tuple[tuple[float, float, float, float, float], ...],
    failing_indices: tuple[int, ...],
) -> Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel:
    maxima = tuple(max(item[index] for item in defects) for index in range(5))
    return Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel(
        level_index=level_index,
        interpolation_nodes=nodes,
        evaluated_amplitudes=inventory,
        maximum_correlation_defect=maxima[0],
        maximum_operator_threshold_defect=maxima[1],
        maximum_joint_threshold_defect=maxima[2],
        maximum_hopping_weight_defect=maxima[3],
        maximum_hopping_power_defect=maxima[4],
        failing_interval_indices=failing_indices,
        within_tolerances=not failing_indices,
    )


def _validation(
    level_index: int,
    nodes: tuple[float, ...],
    samples: tuple[float, ...],
    defects: tuple[tuple[float, float, float, float, float], ...],
    failing_indices: tuple[int, ...],
) -> Periodic1DEmbeddedSubspaceRank2AmplitudeValidation:
    maxima = tuple(max(item[index] for item in defects) for index in range(5))
    return Periodic1DEmbeddedSubspaceRank2AmplitudeValidation(
        level_index=level_index,
        interpolation_nodes=nodes,
        evaluated_amplitudes=samples,
        maximum_correlation_defect=maxima[0],
        maximum_operator_threshold_defect=maxima[1],
        maximum_joint_threshold_defect=maxima[2],
        maximum_hopping_weight_defect=maxima[3],
        maximum_hopping_power_defect=maxima[4],
        failing_point_indices=failing_indices,
        within_tolerances=not failing_indices,
    )


def _interpolation_defects(
    left: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    sample: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    right: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    fraction: float,
) -> tuple[float, float, float, float, float]:
    def defect(left_value: float, sample_value: float, right_value: float) -> float:
        interpolated = (1.0 - fraction) * left_value + fraction * right_value
        return abs(sample_value - interpolated)

    left_powers = {item.displacement: item for item in left.hopping_powers}
    sample_powers = {item.displacement: item for item in sample.hopping_powers}
    right_powers = {item.displacement: item for item in right.hopping_powers}
    hopping_power_defect = max(
        defect(
            left_item.comparison_normalized_squared_frobenius_norm,
            sample_powers[displacement].comparison_normalized_squared_frobenius_norm,
            right_powers[displacement].comparison_normalized_squared_frobenius_norm,
        )
        for displacement, left_item in left_powers.items()
    )
    return (
        defect(
            left.discrete_maximum_correlation,
            sample.discrete_maximum_correlation,
            right.discrete_maximum_correlation,
        ),
        defect(
            left.minimum_operator_threshold,
            sample.minimum_operator_threshold,
            right.minimum_operator_threshold,
        ),
        defect(
            left.exact_spectrum_joint_operator_threshold,
            sample.exact_spectrum_joint_operator_threshold,
            right.exact_spectrum_joint_operator_threshold,
        ),
        defect(
            left.comparison_nonzero_hopping_weight,
            sample.comparison_nonzero_hopping_weight,
            right.comparison_nonzero_hopping_weight,
        ),
        hopping_power_defect,
    )


__all__ = [
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis",
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalyzer",
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged",
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted",
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted",
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped",
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest",
    "Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel",
    "Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds",
    "Periodic1DEmbeddedSubspaceRank2AmplitudeValidation",
]
