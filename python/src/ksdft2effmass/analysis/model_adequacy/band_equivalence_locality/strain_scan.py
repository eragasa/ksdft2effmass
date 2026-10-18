"""Bounded refinement of sampled synthetic-strain transition brackets."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from .strain import (
    StrainPointDiagnostic,
    SyntheticStrainCalculator,
    SyntheticStrainPath,
    SyntheticStrainResult,
)
from .strain_response import (
    StrainErrorChannels,
    StrainResponseCutoffDiagnostic,
    StrainResponseModel,
    StrainResponsePointDiagnostic,
    StrainWitnessControl,
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
)


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanRequest:
    """Define one finite synthetic-strain scan and its refinement controls."""

    path: SyntheticStrainPath
    strain_fractions: tuple[float, ...]
    geometry_construction_size: int
    witness_construction_size: int
    response_construction_size: int
    response_evaluation_size: int
    response_evaluation_shift: float
    maximum_rotation_amplitude: float
    radial_decay_beta: float
    tail_tolerances: tuple[float, ...]
    maximum_transition_refinement_depth: int

    def __post_init__(self) -> None:
        if type(self.path) is not SyntheticStrainPath:
            raise TypeError("path must be SyntheticStrainPath")
        for name, value in (
            ("geometry_construction_size", self.geometry_construction_size),
            ("witness_construction_size", self.witness_construction_size),
            ("response_construction_size", self.response_construction_size),
        ):
            if type(value) is not int or value < 4 or value % 2:
                raise ValueError(
                    f"{name} must be an even built-in integer at least four"
                )
        if (
            type(self.response_evaluation_size) is not int
            or self.response_evaluation_size < 3
        ):
            raise ValueError(
                "response_evaluation_size must be a built-in integer at least three"
            )
        if (
            type(self.response_evaluation_shift) is not float
            or not 0.0 < self.response_evaluation_shift < 1.0
        ):
            raise ValueError(
                "response_evaluation_shift must be a built-in float in (0, 1)"
            )
        if (
            type(self.strain_fractions) is not tuple
            or not self.strain_fractions
            or self.strain_fractions != tuple(sorted(set(self.strain_fractions)))
            or any(
                type(value) is not float or not 0.0 <= value <= 1.0
                for value in self.strain_fractions
            )
        ):
            raise ValueError(
                "strain_fractions must be a nonempty, sorted, unique tuple of built-in "
                "floats in [0, 1]"
            )
        if (
            type(self.maximum_rotation_amplitude) is not float
            or not 0.0 <= self.maximum_rotation_amplitude <= math.pi / 4.0
        ):
            raise ValueError(
                "maximum_rotation_amplitude must be a built-in float in [0, pi/4]"
            )
        if type(self.radial_decay_beta) is not float or self.radial_decay_beta != 1.0:
            raise ValueError("radial_decay_beta must be the built-in float 1.0")
        if (
            type(self.tail_tolerances) is not tuple
            or not self.tail_tolerances
            or any(
                type(value) is not float or not math.isfinite(value) or value <= 0.0
                for value in self.tail_tolerances
            )
        ):
            raise ValueError(
                "tail_tolerances must be a nonempty tuple of positive built-in floats"
            )
        if (
            type(self.maximum_transition_refinement_depth) is not int
            or not 1 <= self.maximum_transition_refinement_depth <= 20
        ):
            raise ValueError(
                "maximum_transition_refinement_depth must be a built-in integer in "
                "[1, 20]"
            )


@dataclass(frozen=True, slots=True)
class StrainWitnessRequirementEnvelope:
    """Retain sampled extrema for one representation-witness control."""

    control: StrainWitnessControl
    optimized_maximum: float
    optimized_maximum_strain_fraction: float
    fixed_candidate_maximum: float
    fixed_candidate_maximum_strain_fraction: float
    minimum_splitting_scale: float
    minimum_splitting_scale_strain_fraction: float
    maximum_splitting_scale: float
    maximum_splitting_scale_strain_fraction: float
    minimum_correlation: float
    minimum_correlation_strain_fraction: float
    maximum_correlation: float
    maximum_correlation_strain_fraction: float


@dataclass(frozen=True, slots=True)
class StrainLocalityEnvelope:
    """Retain sampled physical-range and block-count maxima at one tolerance."""

    tail_tolerance: float
    maximum_physical_radius: float | None
    maximum_physical_radius_strain_fraction: float | None
    maximum_retained_blocks: int | None
    maximum_retained_blocks_strain_fraction: float | None


@dataclass(frozen=True, slots=True)
class StrainResponseEnvelope:
    """Retain one sampled aligned strain-response maximum."""

    control: StrainWitnessControl
    maximum_aligned_hamiltonian_defect: float
    maximum_strain_fraction: float


@dataclass(frozen=True, slots=True)
class SampledStrainMaximum:
    """Retain one sampled maximum and the first strain where it occurs."""

    value: float
    strain_fraction: float


@dataclass(frozen=True, slots=True)
class SampledStrainMinimum:
    """Retain one sampled minimum and the first strain where it occurs."""

    value: float
    strain_fraction: float


@dataclass(frozen=True, slots=True)
class StrainQualificationEnvelope:
    """Retain sampled subspace and frame qualification extrema."""

    control: StrainWitnessControl
    external_isolation_gap: SampledStrainMinimum
    seed_overlap: SampledStrainMinimum
    frame_overlap_singular_value: SampledStrainMinimum
    pointwise_frame_alignment_residual: SampledStrainMaximum
    restricted_global_frame_alignment_residual: SampledStrainMaximum


@dataclass(frozen=True, slots=True)
class StrainErrorChannelEnvelope:
    """Retain sampled maxima of one four-component error channel."""

    sample_count: int
    maximum_hamiltonian: SampledStrainMaximum
    rms_hamiltonian: SampledStrainMaximum
    maximum_band: SampledStrainMaximum
    rms_band: SampledStrainMaximum


@dataclass(frozen=True, slots=True)
class StrainCutoffApproximationEnvelope:
    """Retain sampled error and omitted-power extrema at one cutoff rule."""

    tail_tolerance: float
    omitted_power: SampledStrainMaximum
    truncation: StrainErrorChannelEnvelope | None
    total: StrainErrorChannelEnvelope | None
    delta_omitted_power: SampledStrainMaximum
    delta_truncation: StrainErrorChannelEnvelope | None
    delta_total: StrainErrorChannelEnvelope | None


@dataclass(frozen=True, slots=True)
class StrainApproximationEnvelope:
    """Retain sampled numerical-approximation extrema for one response control."""

    control: StrainWitnessControl
    aligned_strain_perturbation: StrainErrorChannelEnvelope
    interpolation: StrainErrorChannelEnvelope
    delta_interpolation: StrainErrorChannelEnvelope
    nyquist_power: SampledStrainMaximum
    delta_nyquist_power: SampledStrainMaximum
    cutoffs: tuple[StrainCutoffApproximationEnvelope, ...]


@dataclass(frozen=True, slots=True)
class StrainResponseMechanismEnvelope:
    """Retain sampled extrema that attribute the synthetic response mechanism."""

    control: StrainWitnessControl
    hopping_response_minimum: SampledStrainMinimum
    hopping_response_maximum: SampledStrainMaximum
    scalar_component_maximum: SampledStrainMaximum
    scalar_component_rms_maximum: SampledStrainMaximum
    traceless_component_maximum: SampledStrainMaximum
    traceless_component_rms_maximum: SampledStrainMaximum
    delta_onsite_power_maximum: SampledStrainMaximum
    delta_offsite_power_maximum: SampledStrainMaximum


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanSummary:
    """Combine independently interpreted sampled scan envelopes."""

    base_sample_count: int
    maximum_volume_defect: float
    maximum_volume_defect_strain_fraction: float
    maximum_direct_band_defect: float
    maximum_direct_band_defect_strain_fraction: float
    witness_requirements: tuple[StrainWitnessRequirementEnvelope, ...]
    locality: tuple[StrainLocalityEnvelope, ...]
    responses: tuple[StrainResponseEnvelope, ...]
    qualifications: tuple[StrainQualificationEnvelope, ...]
    approximations: tuple[StrainApproximationEnvelope, ...]
    mechanisms: tuple[StrainResponseMechanismEnvelope, ...]
    status: str = "sampled-development-summary-not-continuum-certificate"


def _sampled_maximum(
    points: tuple[StrainResponsePointDiagnostic, ...],
    value: Callable[[StrainResponsePointDiagnostic], float],
) -> SampledStrainMaximum:
    point = max(points, key=value)
    return SampledStrainMaximum(
        value=value(point),
        strain_fraction=point.strain_fraction,
    )


def _sampled_minimum(
    points: tuple[StrainResponsePointDiagnostic, ...],
    value: Callable[[StrainResponsePointDiagnostic], float],
) -> SampledStrainMinimum:
    point = min(points, key=value)
    return SampledStrainMinimum(
        value=value(point),
        strain_fraction=point.strain_fraction,
    )


def _cutoff_maximum(
    points: tuple[StrainResponsePointDiagnostic, ...],
    cutoff_index: int,
    value: Callable[[StrainResponseCutoffDiagnostic], float],
) -> SampledStrainMaximum:
    point = max(points, key=lambda item: value(item.cutoffs[cutoff_index]))
    return SampledStrainMaximum(
        value=value(point.cutoffs[cutoff_index]),
        strain_fraction=point.strain_fraction,
    )


def _cutoff_error_samples(
    points: tuple[StrainResponsePointDiagnostic, ...],
    cutoff_index: int,
    value: Callable[[StrainResponseCutoffDiagnostic], StrainErrorChannels | None],
) -> tuple[tuple[float, StrainErrorChannels], ...]:
    samples: list[tuple[float, StrainErrorChannels]] = []
    for point in points:
        channels = value(point.cutoffs[cutoff_index])
        if channels is not None:
            samples.append((point.strain_fraction, channels))
    return tuple(samples)


def _error_channel_envelope(
    samples: tuple[tuple[float, StrainErrorChannels], ...],
) -> StrainErrorChannelEnvelope | None:
    if not samples:
        return None

    def maximum(value: Callable[[StrainErrorChannels], float]) -> SampledStrainMaximum:
        fraction, channels = max(samples, key=lambda sample: value(sample[1]))
        return SampledStrainMaximum(
            value=value(channels),
            strain_fraction=fraction,
        )

    return StrainErrorChannelEnvelope(
        sample_count=len(samples),
        maximum_hamiltonian=maximum(lambda channels: channels.maximum_hamiltonian),
        rms_hamiltonian=maximum(lambda channels: channels.rms_hamiltonian),
        maximum_band=maximum(lambda channels: channels.maximum_band),
        rms_band=maximum(lambda channels: channels.rms_band),
    )


class SyntheticStrainScanAssessor:
    """Summarize typed scan results without applying acceptance limits."""

    __slots__ = ()

    def execute(
        self,
        geometry_result: SyntheticStrainResult,
        witness_results: tuple[SyntheticStrainWitnessScanResult, ...],
        frozen_response: SyntheticStrainResponseResult,
        radial_response: SyntheticStrainResponseResult,
    ) -> SyntheticStrainScanSummary:
        """Calculate sampled envelopes for one common strain grid."""
        if type(geometry_result) is not SyntheticStrainResult:
            raise TypeError("geometry_result must be SyntheticStrainResult")
        if type(witness_results) is not tuple or any(
            type(result) is not SyntheticStrainWitnessScanResult
            for result in witness_results
        ):
            raise TypeError(
                "witness_results must be a tuple of SyntheticStrainWitnessScanResult"
            )
        if len(witness_results) != len(StrainWitnessControl) or {
            result.control for result in witness_results
        } != set(StrainWitnessControl):
            raise ValueError("witness_results must contain each control exactly once")
        if type(frozen_response) is not SyntheticStrainResponseResult:
            raise TypeError("frozen_response must be SyntheticStrainResponseResult")
        if type(radial_response) is not SyntheticStrainResponseResult:
            raise TypeError("radial_response must be SyntheticStrainResponseResult")
        if frozen_response.model is not StrainResponseModel.M1_FROZEN:
            raise ValueError("frozen_response must use the frozen-parent model")
        if radial_response.model is not StrainResponseModel.M2_RADIAL:
            raise ValueError("radial_response must use the radial-response model")
        if any(
            result.tail_tolerances != geometry_result.tail_tolerances
            for result in (frozen_response, radial_response)
        ):
            raise ValueError("all scan results must use the same tail tolerances")

        path = geometry_result.path
        fractions = tuple(point.strain_fraction for point in geometry_result.points)
        if not fractions:
            raise ValueError("geometry_result must contain at least one strain point")
        if any(
            result.path is not path
            or tuple(point.strain_fraction for point in result.points) != fractions
            for result in witness_results
        ) or any(
            result.path is not path
            or tuple(point.strain_fraction for point in result.points) != fractions
            for result in (frozen_response, radial_response)
        ):
            raise ValueError("all scan results must use one path and strain grid")

        witness_envelopes: list[StrainWitnessRequirementEnvelope] = []
        for result in sorted(witness_results, key=lambda item: item.control.value):
            optimized = max(
                result.points,
                key=lambda point: point.pointwise_optimized_operator_threshold,
            )
            fixed = max(
                result.points,
                key=lambda point: point.fixed_candidate_operator_threshold,
            )
            minimum_splitting = min(
                result.points,
                key=lambda point: point.splitting_scale,
            )
            maximum_splitting = max(
                result.points,
                key=lambda point: point.splitting_scale,
            )
            minimum_correlation = min(
                result.points,
                key=lambda point: point.finite_mesh_maximum_correlation,
            )
            maximum_correlation = max(
                result.points,
                key=lambda point: point.finite_mesh_maximum_correlation,
            )
            witness_envelopes.append(
                StrainWitnessRequirementEnvelope(
                    control=result.control,
                    optimized_maximum=optimized.pointwise_optimized_operator_threshold,
                    optimized_maximum_strain_fraction=optimized.strain_fraction,
                    fixed_candidate_maximum=fixed.fixed_candidate_operator_threshold,
                    fixed_candidate_maximum_strain_fraction=fixed.strain_fraction,
                    minimum_splitting_scale=minimum_splitting.splitting_scale,
                    minimum_splitting_scale_strain_fraction=(
                        minimum_splitting.strain_fraction
                    ),
                    maximum_splitting_scale=maximum_splitting.splitting_scale,
                    maximum_splitting_scale_strain_fraction=(
                        maximum_splitting.strain_fraction
                    ),
                    minimum_correlation=(
                        minimum_correlation.finite_mesh_maximum_correlation
                    ),
                    minimum_correlation_strain_fraction=(
                        minimum_correlation.strain_fraction
                    ),
                    maximum_correlation=(
                        maximum_correlation.finite_mesh_maximum_correlation
                    ),
                    maximum_correlation_strain_fraction=(
                        maximum_correlation.strain_fraction
                    ),
                )
            )

        locality: list[StrainLocalityEnvelope] = []
        for tolerance_index, tolerance in enumerate(geometry_result.tail_tolerances):
            radius_points = tuple(
                point
                for point in geometry_result.points
                if point.first_passing_radius[tolerance_index] is not None
            )
            block_points = tuple(
                point
                for point in geometry_result.points
                if point.first_passing_blocks[tolerance_index] is not None
            )
            radius_point = (
                None
                if not radius_points
                else max(
                    radius_points,
                    key=lambda point: (
                        point.first_passing_radius[tolerance_index] or 0.0
                    ),
                )
            )
            block_point = (
                None
                if not block_points
                else max(
                    block_points,
                    key=lambda point: point.first_passing_blocks[tolerance_index] or 0,
                )
            )
            locality.append(
                StrainLocalityEnvelope(
                    tail_tolerance=tolerance,
                    maximum_physical_radius=(
                        None
                        if radius_point is None
                        else radius_point.first_passing_radius[tolerance_index]
                    ),
                    maximum_physical_radius_strain_fraction=(
                        None if radius_point is None else radius_point.strain_fraction
                    ),
                    maximum_retained_blocks=(
                        None
                        if block_point is None
                        else block_point.first_passing_blocks[tolerance_index]
                    ),
                    maximum_retained_blocks_strain_fraction=(
                        None if block_point is None else block_point.strain_fraction
                    ),
                )
            )

        responses: list[StrainResponseEnvelope] = []
        qualifications: list[StrainQualificationEnvelope] = []
        approximations: list[StrainApproximationEnvelope] = []
        mechanisms: list[StrainResponseMechanismEnvelope] = []
        response_results = (
            (StrainWitnessControl.FROZEN_PARENT, frozen_response),
            (StrainWitnessControl.RADIAL_RESPONSE, radial_response),
        )
        for control, response_result in response_results:
            points = response_result.points
            maximum = max(
                points,
                key=lambda point: point.aligned_strain_perturbation.maximum_hamiltonian,
            )
            responses.append(
                StrainResponseEnvelope(
                    control=control,
                    maximum_aligned_hamiltonian_defect=(
                        maximum.aligned_strain_perturbation.maximum_hamiltonian
                    ),
                    maximum_strain_fraction=maximum.strain_fraction,
                )
            )
            qualifications.append(
                StrainQualificationEnvelope(
                    control=control,
                    external_isolation_gap=_sampled_minimum(
                        points,
                        lambda point: point.minimum_sampled_external_isolation_gap,
                    ),
                    seed_overlap=_sampled_minimum(
                        points,
                        lambda point: point.minimum_seed_overlap,
                    ),
                    frame_overlap_singular_value=_sampled_minimum(
                        points,
                        lambda point: point.minimum_frame_overlap_singular_value,
                    ),
                    pointwise_frame_alignment_residual=_sampled_maximum(
                        points,
                        lambda point: point.maximum_pointwise_frame_alignment_residual,
                    ),
                    restricted_global_frame_alignment_residual=_sampled_maximum(
                        points,
                        lambda point: point.restricted_global_frame_alignment_residual,
                    ),
                )
            )
            aligned = _error_channel_envelope(
                tuple(
                    (point.strain_fraction, point.aligned_strain_perturbation)
                    for point in points
                )
            )
            interpolation = _error_channel_envelope(
                tuple((point.strain_fraction, point.interpolation) for point in points)
            )
            delta_interpolation = _error_channel_envelope(
                tuple(
                    (point.strain_fraction, point.delta_interpolation)
                    for point in points
                )
            )
            if aligned is None or interpolation is None or delta_interpolation is None:
                raise RuntimeError("complete scan error channels must not be empty")
            cutoff_envelopes: list[StrainCutoffApproximationEnvelope] = []
            for tolerance_index, tolerance in enumerate(
                response_result.tail_tolerances
            ):
                cutoff_envelopes.append(
                    StrainCutoffApproximationEnvelope(
                        tail_tolerance=tolerance,
                        omitted_power=_cutoff_maximum(
                            points,
                            tolerance_index,
                            lambda cutoff: cutoff.omitted_power,
                        ),
                        truncation=_error_channel_envelope(
                            _cutoff_error_samples(
                                points,
                                tolerance_index,
                                lambda cutoff: cutoff.truncation,
                            )
                        ),
                        total=_error_channel_envelope(
                            _cutoff_error_samples(
                                points,
                                tolerance_index,
                                lambda cutoff: cutoff.total,
                            )
                        ),
                        delta_omitted_power=_cutoff_maximum(
                            points,
                            tolerance_index,
                            lambda cutoff: cutoff.delta_omitted_power,
                        ),
                        delta_truncation=_error_channel_envelope(
                            _cutoff_error_samples(
                                points,
                                tolerance_index,
                                lambda cutoff: cutoff.delta_truncation,
                            )
                        ),
                        delta_total=_error_channel_envelope(
                            _cutoff_error_samples(
                                points,
                                tolerance_index,
                                lambda cutoff: cutoff.delta_total,
                            )
                        ),
                    )
                )
            approximations.append(
                StrainApproximationEnvelope(
                    control=control,
                    aligned_strain_perturbation=aligned,
                    interpolation=interpolation,
                    delta_interpolation=delta_interpolation,
                    nyquist_power=_sampled_maximum(
                        points,
                        lambda point: point.nyquist_power,
                    ),
                    delta_nyquist_power=_sampled_maximum(
                        points,
                        lambda point: point.delta_nyquist_power,
                    ),
                    cutoffs=tuple(cutoff_envelopes),
                )
            )
            mechanisms.append(
                StrainResponseMechanismEnvelope(
                    control=control,
                    hopping_response_minimum=_sampled_minimum(
                        points,
                        lambda point: point.minimum_hopping_response,
                    ),
                    hopping_response_maximum=_sampled_maximum(
                        points,
                        lambda point: point.maximum_hopping_response,
                    ),
                    scalar_component_maximum=_sampled_maximum(
                        points,
                        lambda point: point.maximum_scalar_strain_component,
                    ),
                    scalar_component_rms_maximum=_sampled_maximum(
                        points,
                        lambda point: point.rms_scalar_strain_component,
                    ),
                    traceless_component_maximum=_sampled_maximum(
                        points,
                        lambda point: point.maximum_traceless_strain_component,
                    ),
                    traceless_component_rms_maximum=_sampled_maximum(
                        points,
                        lambda point: point.rms_traceless_strain_component,
                    ),
                    delta_onsite_power_maximum=_sampled_maximum(
                        points,
                        lambda point: point.delta_onsite_power,
                    ),
                    delta_offsite_power_maximum=_sampled_maximum(
                        points,
                        lambda point: point.delta_offsite_power,
                    ),
                )
            )

        volume_point = max(
            geometry_result.points,
            key=lambda point: abs(float(np.linalg.det(np.asarray(point.metric))) - 1.0),
        )
        direct_band_point = max(
            (point for result in witness_results for point in result.points),
            key=lambda point: point.maximum_direct_band_defect,
        )
        return SyntheticStrainScanSummary(
            base_sample_count=len(fractions),
            maximum_volume_defect=abs(
                float(np.linalg.det(np.asarray(volume_point.metric))) - 1.0
            ),
            maximum_volume_defect_strain_fraction=volume_point.strain_fraction,
            maximum_direct_band_defect=direct_band_point.maximum_direct_band_defect,
            maximum_direct_band_defect_strain_fraction=(
                direct_band_point.strain_fraction
            ),
            witness_requirements=tuple(witness_envelopes),
            locality=tuple(locality),
            responses=tuple(responses),
            qualifications=tuple(qualifications),
            approximations=tuple(approximations),
            mechanisms=tuple(mechanisms),
        )


@dataclass(frozen=True, slots=True)
class StrainShellTransitionBracket:
    """Bracket one detected change in a first-passing block count."""

    tail_tolerance: float
    left_strain_fraction: float
    right_strain_fraction: float
    left_retained_blocks: int | None
    right_retained_blocks: int | None

    @property
    def width(self) -> float:
        """Return the sampled strain width of the transition bracket."""
        return self.right_strain_fraction - self.left_strain_fraction


@dataclass(frozen=True, slots=True)
class StrainBondDegeneracyTransitionBracket:
    """Bracket one detected change in the number of bond-length orbits."""

    left_strain_fraction: float
    right_strain_fraction: float
    left_distinct_bond_lengths: int
    right_distinct_bond_lengths: int

    @property
    def width(self) -> float:
        """Return the sampled strain width of the transition bracket."""
        return self.right_strain_fraction - self.left_strain_fraction


@dataclass(frozen=True, slots=True)
class SyntheticStrainTransitionRefinementResult:
    """Retain bounded refinements of transitions detected on a base scan."""

    base_sample_count: int
    maximum_refinement_depth: int
    shell_transitions: tuple[StrainShellTransitionBracket, ...]
    bond_degeneracy_transitions: tuple[StrainBondDegeneracyTransitionBracket, ...]
    maximum_final_bracket_width: float
    status: str = "sampled-transition-brackets-not-continuum-certificates"


class SyntheticStrainTransitionRefiner:
    """Refine only transitions already detected between adjacent base samples."""

    __slots__ = ()

    def execute(
        self,
        base_result: SyntheticStrainResult,
        maximum_refinement_depth: int,
    ) -> SyntheticStrainTransitionRefinementResult:
        """Bisect detected shell and bond-degeneracy transition brackets."""
        if type(base_result) is not SyntheticStrainResult:
            raise TypeError("base_result must be SyntheticStrainResult")
        if (
            type(maximum_refinement_depth) is not int
            or not 1 <= maximum_refinement_depth <= 20
        ):
            raise ValueError(
                "maximum_refinement_depth must be a built-in integer in [1, 20]"
            )
        if len(base_result.points) < 2:
            raise ValueError("base_result must contain at least two strain points")
        fractions = tuple(point.strain_fraction for point in base_result.points)
        if fractions != tuple(sorted(set(fractions))):
            raise ValueError(
                "base_result points must have strictly increasing strain fractions"
            )

        cache = {point.strain_fraction: point for point in base_result.points}
        shell_transitions: list[StrainShellTransitionBracket] = []
        for tolerance_index, tolerance in enumerate(base_result.tail_tolerances):
            for left, right in zip(
                base_result.points[:-1], base_result.points[1:], strict=True
            ):
                if (
                    left.first_passing_blocks[tolerance_index]
                    == right.first_passing_blocks[tolerance_index]
                ):
                    continue
                shell_transitions.extend(
                    self._refine_shell_transition(
                        base_result,
                        tolerance_index,
                        tolerance,
                        left,
                        right,
                        maximum_refinement_depth,
                        cache,
                    )
                )

        bond_transitions: list[StrainBondDegeneracyTransitionBracket] = []
        for left, right in zip(
            base_result.points[:-1], base_result.points[1:], strict=True
        ):
            if left.distinct_bond_lengths == right.distinct_bond_lengths:
                continue
            bond_transitions.extend(
                self._refine_bond_transition(
                    base_result,
                    left,
                    right,
                    maximum_refinement_depth,
                    cache,
                )
            )

        ordered_shells = tuple(
            sorted(
                shell_transitions,
                key=lambda bracket: (
                    bracket.tail_tolerance,
                    bracket.left_strain_fraction,
                    bracket.right_strain_fraction,
                ),
            )
        )
        ordered_bonds = tuple(
            sorted(
                bond_transitions,
                key=lambda bracket: (
                    bracket.left_strain_fraction,
                    bracket.right_strain_fraction,
                ),
            )
        )
        widths = tuple(bracket.width for bracket in ordered_shells) + tuple(
            bracket.width for bracket in ordered_bonds
        )
        return SyntheticStrainTransitionRefinementResult(
            base_sample_count=len(base_result.points),
            maximum_refinement_depth=maximum_refinement_depth,
            shell_transitions=ordered_shells,
            bond_degeneracy_transitions=ordered_bonds,
            maximum_final_bracket_width=max(widths, default=0.0),
        )

    def _evaluate(
        self,
        base_result: SyntheticStrainResult,
        fraction: float,
        cache: dict[float, StrainPointDiagnostic],
    ) -> StrainPointDiagnostic:
        cached = cache.get(fraction)
        if cached is not None:
            return cached
        point = (
            SyntheticStrainCalculator()
            .execute(
                base_result.path,
                base_result.construction_size,
                (fraction,),
                base_result.maximum_rotation_amplitude,
                base_result.tail_tolerances,
            )
            .points[0]
        )
        cache[fraction] = point
        return point

    def _refine_shell_transition(
        self,
        base_result: SyntheticStrainResult,
        tolerance_index: int,
        tolerance: float,
        initial_left: StrainPointDiagnostic,
        initial_right: StrainPointDiagnostic,
        maximum_refinement_depth: int,
        cache: dict[float, StrainPointDiagnostic],
    ) -> list[StrainShellTransitionBracket]:
        stack = [(initial_left, initial_right, maximum_refinement_depth)]
        brackets: list[StrainShellTransitionBracket] = []
        while stack:
            left, right, remaining = stack.pop()
            left_count = left.first_passing_blocks[tolerance_index]
            right_count = right.first_passing_blocks[tolerance_index]
            if remaining == 0:
                brackets.append(
                    StrainShellTransitionBracket(
                        tail_tolerance=tolerance,
                        left_strain_fraction=left.strain_fraction,
                        right_strain_fraction=right.strain_fraction,
                        left_retained_blocks=left_count,
                        right_retained_blocks=right_count,
                    )
                )
                continue
            midpoint_fraction = (left.strain_fraction + right.strain_fraction) / 2.0
            midpoint = self._evaluate(base_result, midpoint_fraction, cache)
            midpoint_count = midpoint.first_passing_blocks[tolerance_index]
            if left_count != midpoint_count:
                stack.append((left, midpoint, remaining - 1))
            if midpoint_count != right_count:
                stack.append((midpoint, right, remaining - 1))
        return brackets

    def _refine_bond_transition(
        self,
        base_result: SyntheticStrainResult,
        initial_left: StrainPointDiagnostic,
        initial_right: StrainPointDiagnostic,
        maximum_refinement_depth: int,
        cache: dict[float, StrainPointDiagnostic],
    ) -> list[StrainBondDegeneracyTransitionBracket]:
        stack = [(initial_left, initial_right, maximum_refinement_depth)]
        brackets: list[StrainBondDegeneracyTransitionBracket] = []
        while stack:
            left, right, remaining = stack.pop()
            left_count = left.distinct_bond_lengths
            right_count = right.distinct_bond_lengths
            if remaining == 0:
                brackets.append(
                    StrainBondDegeneracyTransitionBracket(
                        left_strain_fraction=left.strain_fraction,
                        right_strain_fraction=right.strain_fraction,
                        left_distinct_bond_lengths=left_count,
                        right_distinct_bond_lengths=right_count,
                    )
                )
                continue
            midpoint_fraction = (left.strain_fraction + right.strain_fraction) / 2.0
            midpoint = self._evaluate(base_result, midpoint_fraction, cache)
            midpoint_count = midpoint.distinct_bond_lengths
            if left_count != midpoint_count:
                stack.append((left, midpoint, remaining - 1))
            if midpoint_count != right_count:
                stack.append((midpoint, right, remaining - 1))
        return brackets


__all__ = [
    "SampledStrainMaximum",
    "SampledStrainMinimum",
    "StrainApproximationEnvelope",
    "StrainBondDegeneracyTransitionBracket",
    "StrainCutoffApproximationEnvelope",
    "StrainErrorChannelEnvelope",
    "StrainLocalityEnvelope",
    "StrainQualificationEnvelope",
    "StrainResponseEnvelope",
    "StrainResponseMechanismEnvelope",
    "StrainWitnessRequirementEnvelope",
    "StrainShellTransitionBracket",
    "SyntheticStrainScanAssessor",
    "SyntheticStrainScanRequest",
    "SyntheticStrainScanSummary",
    "SyntheticStrainTransitionRefinementResult",
    "SyntheticStrainTransitionRefiner",
]
