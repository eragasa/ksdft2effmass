"""Independent adaptive-amplitude reconstruction for embedded rank two."""

from __future__ import annotations

from itertools import pairwise

from .amplitude_refinement import (
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest,
    Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel,
    Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2AmplitudeValidation,
)
from .reference import Periodic1DEmbeddedSubspaceRank2IndependentReferenceAnalyzer
from .request import Periodic1DEmbeddedSubspaceRank2Request
from .results import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2PointAnalysis,
)


class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentReferenceAnalyzer:
    """Rebuild adaptive decisions from direct independent member analyses."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest,
    ) -> None:
        if type(request) is not Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest:
            raise TypeError("request must be an adaptive-amplitude request")
        self._request = request

    def execute(self) -> Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis:
        """Return an independently sampled qualification or adaptive outcome."""
        cache: dict[float, Periodic1DEmbeddedSubspaceRank2PointAnalysis] = {}
        evaluations: list[Periodic1DEmbeddedSubspaceRank2Analysis] = []
        levels: list[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel] = []
        validations: list[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation] = []

        def evaluate(
            amplitudes: tuple[float, ...],
        ) -> Periodic1DEmbeddedSubspaceRank2Analysis | None:
            new = tuple(amplitude for amplitude in amplitudes if amplitude not in cache)
            if len(cache) + len(new) > self._request.maximum_evaluated_amplitudes:
                return None
            direct_amplitudes = (
                amplitudes
                if not cache
                else tuple(sorted({0.0} | set(new)))
            )
            direct_analysis = (
                Periodic1DEmbeddedSubspaceRank2IndependentReferenceAnalyzer(
                    _evaluation_request(
                        self._request.template_request,
                        direct_amplitudes,
                    )
                ).execute()
            )
            evaluation_request = _evaluation_request(
                self._request.template_request,
                amplitudes,
            )
            if not direct_analysis.qualification.qualified:
                analysis = Periodic1DEmbeddedSubspaceRank2Analysis(
                    request=evaluation_request,
                    qualification=direct_analysis.qualification,
                    points=(),
                )
                evaluations.append(analysis)
                return analysis
            cache.update(
                {point.amplitude: point for point in direct_analysis.points}
            )
            analysis = Periodic1DEmbeddedSubspaceRank2Analysis(
                request=evaluation_request,
                qualification=direct_analysis.qualification,
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
                return _evaluation_cap_outcome(
                    self._request,
                    evaluations,
                    levels,
                    validations,
                    cache,
                    midpoint_inventory,
                )
            if not midpoint_analysis.qualification.qualified:
                return (
                    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped(
                        request=self._request,
                        evaluations=tuple(evaluations),
                    )
                )
            midpoint_defects = tuple(
                _reference_interpolation_defects(
                    cache[left], cache[midpoint], cache[right], 0.5
                )
                for left, midpoint, right in zip(
                    nodes[:-1], midpoints, nodes[1:], strict=True
                )
            )
            midpoint_failures = tuple(
                not _reference_defects_within(defects, self._request.thresholds)
                for defects in midpoint_defects
            )
            level = _reference_level(
                level_index,
                nodes,
                midpoint_inventory,
                midpoint_defects,
                tuple(
                    index
                    for index, failed in enumerate(midpoint_failures)
                    if failed
                ),
            )
            levels.append(level)
            candidate_nodes = tuple(
                sorted(
                    set(nodes)
                    | {
                        midpoint
                        for midpoint, failed in zip(
                            midpoints, midpoint_failures, strict=True
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
                validation_inventory = tuple(
                    sorted(set(nodes) | set(quarter_samples))
                )
                validation_analysis = evaluate(validation_inventory)
                if validation_analysis is None:
                    return _evaluation_cap_outcome(
                        self._request,
                        evaluations,
                        levels,
                        validations,
                        cache,
                        validation_inventory,
                    )
                if not validation_analysis.qualification.qualified:
                    return (
                        Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped(
                            request=self._request,
                            evaluations=tuple(evaluations),
                        )
                    )
                validation_defects = tuple(
                    _reference_interpolation_defects(
                        cache[left], cache[sample], cache[right], fraction
                    )
                    for left, right in pairwise(nodes)
                    for sample, fraction in (
                        (left + 0.25 * (right - left), 0.25),
                        (left + 0.75 * (right - left), 0.75),
                    )
                )
                validation_failures = tuple(
                    not _reference_defects_within(defects, self._request.thresholds)
                    for defects in validation_defects
                )
                validation = _reference_validation(
                    level_index,
                    nodes,
                    quarter_samples,
                    validation_defects,
                    tuple(
                        index
                        for index, failed in enumerate(validation_failures)
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
                                validation_failures,
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


def _evaluation_request(
    template: Periodic1DEmbeddedSubspaceRank2Request,
    amplitudes: tuple[float, ...],
) -> Periodic1DEmbeddedSubspaceRank2Request:
    return Periodic1DEmbeddedSubspaceRank2Request(
        reciprocal_mesh_size=template.reciprocal_mesh_size,
        amplitudes=amplitudes,
        parent_hopping_scale=template.parent_hopping_scale,
        minimum_external_gap=template.minimum_external_gap,
        minimum_transport_singular_value=template.minimum_transport_singular_value,
        frame_absolute_tolerance=template.frame_absolute_tolerance,
        transport_rank_relative_tolerance=template.transport_rank_relative_tolerance,
        transport_validation_relative_tolerance=(
            template.transport_validation_relative_tolerance
        ),
        harmonic_absolute_degeneracy_tolerance=(
            template.harmonic_absolute_degeneracy_tolerance
        ),
        harmonic_relative_degeneracy_tolerance=(
            template.harmonic_relative_degeneracy_tolerance
        ),
    )


def _evaluation_cap_outcome(
    request: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest,
    evaluations: list[Periodic1DEmbeddedSubspaceRank2Analysis],
    levels: list[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel],
    validations: list[Periodic1DEmbeddedSubspaceRank2AmplitudeValidation],
    cache: dict[float, Periodic1DEmbeddedSubspaceRank2PointAnalysis],
    blocked_amplitudes: tuple[float, ...],
) -> Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted:
    if not evaluations or not levels:
        raise RuntimeError("validated sample cap failed to hold the first inventory")
    return Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted(
        request=request,
        evaluations=tuple(evaluations),
        levels=tuple(levels),
        validations=tuple(validations),
        blocked_amplitudes=blocked_amplitudes,
    )


def _reference_defects_within(
    defects: tuple[float, float, float, float, float],
    thresholds: Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds,
) -> bool:
    limits = (
        thresholds.maximum_correlation_defect,
        thresholds.maximum_operator_threshold_defect,
        thresholds.maximum_joint_threshold_defect,
        thresholds.maximum_hopping_weight_defect,
        thresholds.maximum_hopping_power_defect,
    )
    return all(
        defect <= limit
        for defect, limit in zip(defects, limits, strict=True)
    )


def _reference_level(
    level_index: int,
    nodes: tuple[float, ...],
    inventory: tuple[float, ...],
    defects: tuple[tuple[float, float, float, float, float], ...],
    failing_indices: tuple[int, ...],
) -> Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel:
    maxima = tuple(max(values[index] for values in defects) for index in range(5))
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


def _reference_validation(
    level_index: int,
    nodes: tuple[float, ...],
    samples: tuple[float, ...],
    defects: tuple[tuple[float, float, float, float, float], ...],
    failing_indices: tuple[int, ...],
) -> Periodic1DEmbeddedSubspaceRank2AmplitudeValidation:
    maxima = tuple(max(values[index] for values in defects) for index in range(5))
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


def _reference_interpolation_defects(
    left: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    sample: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    right: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    fraction: float,
) -> tuple[float, float, float, float, float]:
    def absolute_linear_defect(
        left_value: float,
        sample_value: float,
        right_value: float,
    ) -> float:
        linear_value = left_value + fraction * (right_value - left_value)
        return abs(sample_value - linear_value)

    left_power = {value.displacement: value for value in left.hopping_powers}
    sample_power = {value.displacement: value for value in sample.hopping_powers}
    right_power = {value.displacement: value for value in right.hopping_powers}
    maximum_power_defect = max(
        absolute_linear_defect(
            value.comparison_normalized_squared_frobenius_norm,
            sample_power[
                displacement
            ].comparison_normalized_squared_frobenius_norm,
            right_power[displacement].comparison_normalized_squared_frobenius_norm,
        )
        for displacement, value in left_power.items()
    )
    return (
        absolute_linear_defect(
            left.discrete_maximum_correlation,
            sample.discrete_maximum_correlation,
            right.discrete_maximum_correlation,
        ),
        absolute_linear_defect(
            left.minimum_operator_threshold,
            sample.minimum_operator_threshold,
            right.minimum_operator_threshold,
        ),
        absolute_linear_defect(
            left.exact_spectrum_joint_operator_threshold,
            sample.exact_spectrum_joint_operator_threshold,
            right.exact_spectrum_joint_operator_threshold,
        ),
        absolute_linear_defect(
            left.comparison_nonzero_hopping_weight,
            sample.comparison_nonzero_hopping_weight,
            right.comparison_nonzero_hopping_weight,
        ),
        maximum_power_defect,
    )


__all__ = [
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentReferenceAnalyzer",
]
