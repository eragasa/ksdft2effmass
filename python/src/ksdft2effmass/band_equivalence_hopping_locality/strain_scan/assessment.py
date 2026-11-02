"""Assessment of bounded synthetic-strain scan results."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from ..strain import SyntheticStrainResult
from ..strain_response import (
    StrainErrorChannels,
    StrainResponseCutoffDiagnostic,
    StrainResponseModelEnum,
    StrainResponsePointDiagnostic,
    StrainWitnessControlEnum,
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
)
from .records import (
    SampledStrainMaximum,
    SampledStrainMinimum,
    StrainApproximationEnvelope,
    StrainCutoffApproximationEnvelope,
    StrainErrorChannelEnvelope,
    StrainLocalityEnvelope,
    StrainQualificationEnvelope,
    StrainResponseEnvelope,
    StrainResponseMechanismEnvelope,
    StrainWitnessRequirementEnvelope,
    SyntheticStrainScanSummary,
)


class SyntheticStrainScanAssessor:
    """Own one typed strain-scan assessment without acceptance limits."""

    __slots__ = (
        "_frozen_response",
        "_geometry_result",
        "_radial_response",
        "_witness_results",
    )

    def __init__(
        self,
        *,
        geometry_result: SyntheticStrainResult,
        witness_results: tuple[SyntheticStrainWitnessScanResult, ...],
        frozen_response: SyntheticStrainResponseResult,
        radial_response: SyntheticStrainResponseResult,
    ) -> None:
        if type(geometry_result) is not SyntheticStrainResult:
            raise TypeError("geometry_result must be SyntheticStrainResult")
        if type(witness_results) is not tuple or any(
            type(result) is not SyntheticStrainWitnessScanResult
            for result in witness_results
        ):
            raise TypeError(
                "witness_results must be a tuple of SyntheticStrainWitnessScanResult"
            )
        if len(witness_results) != len(StrainWitnessControlEnum) or {
            result.control for result in witness_results
        } != set(StrainWitnessControlEnum):
            raise ValueError("witness_results must contain each control exactly once")
        if type(frozen_response) is not SyntheticStrainResponseResult:
            raise TypeError("frozen_response must be SyntheticStrainResponseResult")
        if type(radial_response) is not SyntheticStrainResponseResult:
            raise TypeError("radial_response must be SyntheticStrainResponseResult")
        if frozen_response.model is not StrainResponseModelEnum.M1_FROZEN:
            raise ValueError("frozen_response must use the frozen-parent model")
        if radial_response.model is not StrainResponseModelEnum.M2_RADIAL:
            raise ValueError("radial_response must use the radial-response model")
        if any(
            result.tail_tolerances != geometry_result.tail_tolerances
            for result in (frozen_response, radial_response)
        ):
            raise ValueError("all scan results must use the same tail tolerances")
        self._geometry_result = geometry_result
        self._witness_results = witness_results
        self._frozen_response = frozen_response
        self._radial_response = radial_response

    def _sampled_maximum(
        self,
        points: tuple[StrainResponsePointDiagnostic, ...],
        value: Callable[[StrainResponsePointDiagnostic], float],
    ) -> SampledStrainMaximum:
        point = max(points, key=value)
        return SampledStrainMaximum(
            value=value(point),
            strain_fraction=point.strain_fraction,
        )

    def _sampled_minimum(
        self,
        points: tuple[StrainResponsePointDiagnostic, ...],
        value: Callable[[StrainResponsePointDiagnostic], float],
    ) -> SampledStrainMinimum:
        point = min(points, key=value)
        return SampledStrainMinimum(
            value=value(point),
            strain_fraction=point.strain_fraction,
        )

    def _cutoff_maximum(
        self,
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
        self,
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
        self,
        samples: tuple[tuple[float, StrainErrorChannels], ...],
    ) -> StrainErrorChannelEnvelope | None:
        if not samples:
            return None

        def maximum(
            value: Callable[[StrainErrorChannels], float],
        ) -> SampledStrainMaximum:
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

    def execute(self) -> SyntheticStrainScanSummary:
        """Calculate sampled envelopes for the constructor-bound strain grid."""
        geometry_result = self._geometry_result
        witness_results = self._witness_results
        frozen_response = self._frozen_response
        radial_response = self._radial_response
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
        for result in sorted(
            witness_results,
            key=lambda item: item.control.to_wire(),
        ):
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
            (StrainWitnessControlEnum.FROZEN_PARENT, frozen_response),
            (StrainWitnessControlEnum.RADIAL_RESPONSE, radial_response),
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
                    external_isolation_gap=self._sampled_minimum(
                        points,
                        lambda point: point.minimum_sampled_external_isolation_gap,
                    ),
                    seed_overlap=self._sampled_minimum(
                        points,
                        lambda point: point.minimum_seed_overlap,
                    ),
                    frame_overlap_singular_value=self._sampled_minimum(
                        points,
                        lambda point: point.minimum_frame_overlap_singular_value,
                    ),
                    pointwise_frame_alignment_residual=self._sampled_maximum(
                        points,
                        lambda point: point.maximum_pointwise_frame_alignment_residual,
                    ),
                    restricted_global_frame_alignment_residual=self._sampled_maximum(
                        points,
                        lambda point: point.restricted_global_frame_alignment_residual,
                    ),
                )
            )
            aligned = self._error_channel_envelope(
                tuple(
                    (point.strain_fraction, point.aligned_strain_perturbation)
                    for point in points
                )
            )
            interpolation = self._error_channel_envelope(
                tuple((point.strain_fraction, point.interpolation) for point in points)
            )
            delta_interpolation = self._error_channel_envelope(
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
                        omitted_power=self._cutoff_maximum(
                            points,
                            tolerance_index,
                            lambda cutoff: cutoff.omitted_power,
                        ),
                        truncation=self._error_channel_envelope(
                            self._cutoff_error_samples(
                                points,
                                tolerance_index,
                                lambda cutoff: cutoff.truncation,
                            )
                        ),
                        total=self._error_channel_envelope(
                            self._cutoff_error_samples(
                                points,
                                tolerance_index,
                                lambda cutoff: cutoff.total,
                            )
                        ),
                        delta_omitted_power=self._cutoff_maximum(
                            points,
                            tolerance_index,
                            lambda cutoff: cutoff.delta_omitted_power,
                        ),
                        delta_truncation=self._error_channel_envelope(
                            self._cutoff_error_samples(
                                points,
                                tolerance_index,
                                lambda cutoff: cutoff.delta_truncation,
                            )
                        ),
                        delta_total=self._error_channel_envelope(
                            self._cutoff_error_samples(
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
                    nyquist_power=self._sampled_maximum(
                        points,
                        lambda point: point.nyquist_power,
                    ),
                    delta_nyquist_power=self._sampled_maximum(
                        points,
                        lambda point: point.delta_nyquist_power,
                    ),
                    cutoffs=tuple(cutoff_envelopes),
                )
            )
            mechanisms.append(
                StrainResponseMechanismEnvelope(
                    control=control,
                    hopping_response_minimum=self._sampled_minimum(
                        points,
                        lambda point: point.minimum_hopping_response,
                    ),
                    hopping_response_maximum=self._sampled_maximum(
                        points,
                        lambda point: point.maximum_hopping_response,
                    ),
                    scalar_component_maximum=self._sampled_maximum(
                        points,
                        lambda point: point.maximum_scalar_strain_component,
                    ),
                    scalar_component_rms_maximum=self._sampled_maximum(
                        points,
                        lambda point: point.rms_scalar_strain_component,
                    ),
                    traceless_component_maximum=self._sampled_maximum(
                        points,
                        lambda point: point.maximum_traceless_strain_component,
                    ),
                    traceless_component_rms_maximum=self._sampled_maximum(
                        points,
                        lambda point: point.rms_traceless_strain_component,
                    ),
                    delta_onsite_power_maximum=self._sampled_maximum(
                        points,
                        lambda point: point.delta_onsite_power,
                    ),
                    delta_offsite_power_maximum=self._sampled_maximum(
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
