"""Periodic-2D rank-N aggregate band-equivalence/locality analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.finite_periodic.numpy.tensor_product_evaluation import (
    NumpyTensorProductFourierMatrixEvaluationDefinition,
    NumpyTensorProductFourierMatrixSeriesEvaluator,
)
from projectkoios.numerics.finite_periodic.numpy.transforms import (
    NumpyCenteredUniformMeshMatrixFourierTransformDefinition,
    NumpyCenteredUniformMeshMatrixFourierTransformer,
)
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array, Int64Array
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.band_equivalence_hopping_locality.fourier import (
    error_channels,
    iter_complete_shell_fields,
    maximum_matrix_defect,
)
from ksdft2effmass.band_equivalence_hopping_locality.geometry import (
    metric_shell_classification,
)
from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityErrorChannels,
)
from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (
    MetricShellHoppingPowerResult,
)
from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentGroupIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic2d.rankN.band_alignment.frame_transport.analysis import (
    Periodic2DRankNTransportAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.band_alignment.frame_transport.request import (
    Periodic2DRankNTransportAnalysisRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence.base import (
    Periodic2DRankNBandEquivalence,
    Periodic2DRankNBandEquivalenceAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.analysis import (
    Periodic2DRankNGlobalGaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.definition import (
    Periodic2DRankNGaugeAlignment,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.procrustes.analysis import (
    Periodic2DRankNProcrustesAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.procrustes.request import (
    Periodic2DRankNProcrustesAnalysisRequest,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.procrustes.result import (
    Periodic2DRankNProcrustesAnalysis,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.request import (
    Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.result import (
    Periodic2DRankNGlobalGaugeAlignmentAnalysis,
    Periodic2DRankNGlobalGaugeAlignmentRankDeficient,
    Periodic2DRankNGlobalGaugeAlignmentSelected,
)
from ksdft2effmass.periodic2d.rankN.hopping_locality.analysis import (
    Periodic2DRankNHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.hopping_locality.request import (
    Periodic2DRankNHoppingLocalityAnalysisRequest,
    Periodic2DRankNHoppingLocalityChannelEnum,
)
from ksdft2effmass.periodic2d.rankN.support_truncation.analysis import (
    Periodic2DRankNSupportTruncationAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.support_truncation.request import (
    Periodic2DRankNSupportTruncationAnalysisRequest,
    Periodic2DRankNSupportTruncationChannelEnum,
)
from ksdft2effmass.real_space_support_truncation import (
    MetricShellClassification,
    MinimumToleranceSatisfyingSupport,
    SupportToleranceSelectionOutcome,
    SupportToleranceUnresolved,
)

from .case_expansion import Periodic2DRankNBandEquivalenceHoppingLocalityCaseExpander
from .model import Periodic2DRankNAnalyticCase
from .request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from .result import (
    Periodic2DRankNAlignmentInapplicabilityEnum,
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels,
    Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary,
    Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityShellAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityToleranceDecision,
    Periodic2DRankNFittedAlignmentEvidence,
    Periodic2DRankNPrescribedAlignmentEvidence,
    Periodic2DRankNSupportSelected,
    Periodic2DRankNSupportSelection,
    Periodic2DRankNSupportUnresolved,
)


@dataclass(frozen=True, slots=True)
class _ReferenceFourierData:
    source_mesh: CenteredUniformMesh
    construction_axes: tuple[Float64Array, Float64Array]
    evaluation_axes: tuple[Float64Array, Float64Array]
    ordinary_series: NumpyFiniteFourierMatrixSeries
    full_construction: Complex128Array
    full_evaluation: Complex128Array
    shell_classification: MetricShellClassification
    metric_indices: Int64Array
    metric_shell_values: tuple[int, ...]
    locality: MetricShellHoppingPowerResult
    shell_evaluation_fields: tuple[Complex128Array, ...]


@final
class Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
    Periodic2DRankNBandEquivalence
):
    """Compose installed capability owners for one exact analytic case."""

    __slots__ = ("_geometry", "_model", "_request")

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the exact case's represented band-subspace rank."""
        return (self._model.retained_rank,)

    def __init__(
        self,
        *,
        request: Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
        model: Periodic2DRankNAnalyticCase,
        geometry: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    ) -> None:
        if type(request) is not Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        if type(model) is not Periodic2DRankNAnalyticCase:
            raise TypeError("model must be the exact periodic-2D analytic case")
        if (
            type(geometry)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition
        ):
            raise TypeError("geometry must be the exact periodic-2D case definition")
        selected_geometry = next(
            (
                case
                for case in request.cases
                if case.identifier == model.case_identifier
            ),
            None,
        )
        if selected_geometry is not geometry:
            raise ValueError("geometry must be the request-owned model geometry")
        if (
            model.positive_bonds != geometry.positive_bonds
            or model.gauge_normalization is not geometry.gauge_normalization
            or model.retained_rank not in request.retained_ranks
            or model.circuit_depth not in request.circuit_depths
            or model.parent_scale not in request.parent_scales
            or model.attack_coefficient not in request.attack_coefficients
        ):
            raise ValueError("model must be one exact expansion of the request")
        self._request = request
        self._model = model
        self._geometry = geometry

    @property
    def request(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
        """Return the immutable aggregate request bound to this action."""
        return self._request

    @staticmethod
    def _coordinate_axis(size: int, offset: float) -> Float64Array:
        return np.asarray(
            -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size),
            dtype=np.float64,
        )

    @classmethod
    def _coordinates(cls, size: int, offset: float) -> Float64Array:
        axis = cls._coordinate_axis(size, offset)
        return np.asarray(
            np.stack(np.meshgrid(axis, axis, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    @staticmethod
    def _transform(
        mesh: CenteredUniformMesh,
        values: Complex128Array,
    ) -> NumpyFiniteFourierMatrixSeries:
        return (
            NumpyCenteredUniformMeshMatrixFourierTransformer(
                definition=NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                    mesh,
                    values,
                )
            )
            .result()
            .series
        )

    @staticmethod
    def _evaluate(
        mesh: CenteredUniformMesh,
        series: NumpyFiniteFourierMatrixSeries,
        axes: tuple[Float64Array, Float64Array],
    ) -> Complex128Array:
        return (
            NumpyTensorProductFourierMatrixSeriesEvaluator(
                definition=NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                    mesh,
                    series,
                    axes,
                )
            )
            .result()
            .matrix_values
        )

    @staticmethod
    def _ordinary_series(
        construction_size: int,
        series: NumpyFiniteFourierMatrixSeries,
    ) -> NumpyFiniteFourierMatrixSeries:
        ordinary = ~np.any(
            series.integer_modes == -construction_size // 2,
            axis=1,
        )
        return NumpyFiniteFourierMatrixSeries.from_arrays(
            2,
            series.integer_modes[ordinary],
            series.matrix_coefficients[ordinary],
        )

    def _alignment_identity(
        self,
        retained_rank: int,
    ) -> GaugeAlignmentAnalysisIdentity:
        return GaugeAlignmentAnalysisIdentity(
            gauge_group_identity=GaugeAlignmentGroupIdentity.unitary(
                represented_dimension=retained_rank
            ),
            alignment_sample_count=self._request.construction_size**2,
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=GaugeAlignmentInnerProductConvention.EUCLIDEAN,
        )

    @staticmethod
    def _apply_right_action(
        operators: Complex128Array,
        right_action: Complex128Array,
    ) -> Complex128Array:
        return np.asarray(
            np.swapaxes(right_action.conjugate(), -1, -2) @ operators @ right_action,
            dtype=np.complex128,
        )

    @staticmethod
    def _error_record(
        value: BandEquivalenceHoppingLocalityErrorChannels,
    ) -> Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels:
        return Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels(
            maximum_matrix_frobenius=value.maximum_hamiltonian,
            root_mean_square_matrix_frobenius=value.rms_hamiltonian,
            maximum_ordered_spectrum=value.maximum_band,
            root_mean_square_ordered_spectrum=value.rms_band,
        )

    @staticmethod
    def _locality_summary(
        value: MetricShellHoppingPowerResult,
    ) -> Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary:
        onsite = tuple(
            power.displacement for power in value.powers if power.displacement.is_zero
        )
        onsite_power = value.normalized_power_for(onsite)
        total = value.normalized_total_power
        return Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary(
            total_power=total,
            onsite_power=onsite_power,
            nononsite_power=max(0.0, total - onsite_power),
        )

    def _hopping_locality(
        self,
        *,
        model: Periodic2DRankNAnalyticCase,
        channel: Periodic2DRankNHoppingLocalityChannelEnum,
        series: NumpyFiniteFourierMatrixSeries,
        metric_indices: Int64Array,
    ) -> MetricShellHoppingPowerResult:
        return Periodic2DRankNHoppingLocalityAnalyzer(
            request=Periodic2DRankNHoppingLocalityAnalysisRequest(
                retained_rank=model.retained_rank,
                channel=channel,
                energy_reference="dimensionless-zero-v1",
                basis_identifier=(
                    f"{model.MODEL_FAMILY_IDENTITY}:retained-coordinate-basis"
                ),
                series=series,
                shell_indices=tuple(int(value) for value in metric_indices),
            ),
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()

    def _reference_fourier(
        self,
        *,
        model: Periodic2DRankNAnalyticCase,
        geometry: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        construction_values: Complex128Array,
    ) -> _ReferenceFourierData:
        size = self._request.construction_size
        source_mesh = CenteredUniformMesh(2, size, (0.5, 0.5))
        construction_axis = self._coordinate_axis(size, 0.5)
        evaluation_axis = self._coordinate_axis(
            self._request.evaluation_size,
            0.5 + self._request.evaluation_shift,
        )
        construction_axes = (construction_axis, construction_axis)
        evaluation_axes = (evaluation_axis, evaluation_axis)
        series = self._ordinary_series(
            size,
            self._transform(source_mesh, construction_values),
        )
        full_construction = self._evaluate(source_mesh, series, construction_axes)
        full_evaluation = self._evaluate(source_mesh, series, evaluation_axes)
        classification = metric_shell_classification(geometry, series.integer_modes)
        metric_indices = np.asarray(
            classification.metric_shell_values,
            dtype=np.int64,
        )
        metric_shell_values = tuple(
            value
            for value in sorted(set(classification.metric_shell_values))
            if value <= self._request.shell_cap
        )
        if not metric_shell_values or metric_shell_values[0] != 0:
            raise RuntimeError("selected shell cap must retain the onsite shell")
        locality = self._hopping_locality(
            model=model,
            channel=Periodic2DRankNHoppingLocalityChannelEnum.REFERENCE,
            series=series,
            metric_indices=metric_indices,
        )
        return _ReferenceFourierData(
            source_mesh=source_mesh,
            construction_axes=construction_axes,
            evaluation_axes=evaluation_axes,
            ordinary_series=series,
            full_construction=full_construction,
            full_evaluation=full_evaluation,
            shell_classification=classification,
            metric_indices=metric_indices,
            metric_shell_values=metric_shell_values,
            locality=locality,
            shell_evaluation_fields=tuple(
                iter_complete_shell_fields(
                    source_mesh,
                    series,
                    evaluation_axes,
                    metric_indices,
                    metric_shell_values,
                )
            ),
        )

    @staticmethod
    def _fitted_evidence(
        *analyses: Periodic2DRankNGlobalGaugeAlignmentAnalysis
        | Periodic2DRankNProcrustesAnalysis,
    ) -> Periodic2DRankNFittedAlignmentEvidence:
        owner_results = tuple(analysis.owner_result for analysis in analyses)
        return Periodic2DRankNFittedAlignmentEvidence(
            sample_count=sum(result.batch_size for result in owner_results),
            minimum_numerical_rank=min(
                int(np.min(result.numerical_ranks)) for result in owner_results
            ),
            minimum_cross_singular_value=min(
                float(np.min(result.cross_singular_values)) for result in owner_results
            ),
            maximum_optimal_residual_frobenius_norm=max(
                float(np.max(result.optimal_residual_frobenius_norms))
                for result in owner_results
            ),
            maximum_applied_rank_cutoff=max(
                float(np.max(result.applied_rank_cutoffs)) for result in owner_results
            ),
        )

    def _support_selection(
        self,
        outcome: SupportToleranceSelectionOutcome,
        metric_shell_values: tuple[int, ...],
    ) -> Periodic2DRankNSupportSelection:
        if type(outcome) is MinimumToleranceSatisfyingSupport:
            index = outcome.comparison_index
            return Periodic2DRankNSupportSelected(
                ordinal_shell_index=index,
                metric_shell_value=metric_shell_values[index],
                satisfying_error=outcome.satisfying_error,
                preceding_error=outcome.preceding_error,
            )
        if type(outcome) is SupportToleranceUnresolved:
            return Periodic2DRankNSupportUnresolved(
                comparison_count=outcome.comparison_count,
                minimum_observed_error=outcome.minimum_observed_error,
                largest_support_error=outcome.largest_support_error,
            )
        raise TypeError("support outcome must be an exact selected or unresolved value")

    def _decisions(
        self,
        *,
        model: Periodic2DRankNAnalyticCase,
        reference_errors: tuple[BandEquivalenceHoppingLocalityErrorChannels, ...],
        comparison_errors: tuple[BandEquivalenceHoppingLocalityErrorChannels, ...],
        reference: _ReferenceFourierData,
    ) -> tuple[Periodic2DRankNBandEquivalenceHoppingLocalityToleranceDecision, ...]:
        decisions: list[
            Periodic2DRankNBandEquivalenceHoppingLocalityToleranceDecision
        ] = []
        for tolerance in self._request.band_tolerances:
            reference_selection = Periodic2DRankNSupportTruncationAnalyzer(
                request=Periodic2DRankNSupportTruncationAnalysisRequest(
                    retained_rank=model.retained_rank,
                    channel=Periodic2DRankNSupportTruncationChannelEnum.REFERENCE,
                    support_inventory=reference.shell_classification.support_inventory,
                    total_errors=reference_errors,
                    tolerance=tolerance,
                )
            ).execute()
            comparison_selection = Periodic2DRankNSupportTruncationAnalyzer(
                request=Periodic2DRankNSupportTruncationAnalysisRequest(
                    retained_rank=model.retained_rank,
                    channel=Periodic2DRankNSupportTruncationChannelEnum.COMPARISON,
                    support_inventory=reference.shell_classification.support_inventory,
                    total_errors=comparison_errors,
                    tolerance=tolerance,
                )
            ).execute()
            decisions.append(
                Periodic2DRankNBandEquivalenceHoppingLocalityToleranceDecision(
                    tolerance=tolerance,
                    reference_matrix=self._support_selection(
                        reference_selection.matrix_frobenius_maximum_error,
                        reference.metric_shell_values,
                    ),
                    reference_ordered_spectrum=self._support_selection(
                        reference_selection.ordered_eigenvalue_maximum_absolute_error,
                        reference.metric_shell_values,
                    ),
                    comparison_matrix=self._support_selection(
                        comparison_selection.matrix_frobenius_maximum_error,
                        reference.metric_shell_values,
                    ),
                    comparison_ordered_spectrum=self._support_selection(
                        comparison_selection.ordered_eigenvalue_maximum_absolute_error,
                        reference.metric_shell_values,
                    ),
                )
            )
        return tuple(decisions)

    def _qualified_alignment(
        self,
        *,
        model: Periodic2DRankNAnalyticCase,
        geometry: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        alignment: Periodic2DRankNGaugeAlignment,
        evidence: Periodic2DRankNFittedAlignmentEvidence
        | Periodic2DRankNPrescribedAlignmentEvidence,
        aligned_frame: Complex128Array,
        comparison_construction: Complex128Array,
        comparison_evaluation: Complex128Array,
        reference_construction: Complex128Array,
        reference_evaluation: Complex128Array,
        reference_frame: Complex128Array,
        reference: _ReferenceFourierData,
    ) -> (
        Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
        | Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
    ):
        transport = Periodic2DRankNTransportAnalyzer(
            request=Periodic2DRankNTransportAnalysisRequest(
                retained_rank=model.retained_rank,
                frame=aligned_frame,
                rank_absolute=self._request.transport_rank_absolute,
                rank_relative=self._request.transport_rank_relative,
            )
        ).execute()
        if transport.rank_deficient_link_count > 0:
            return Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(  # noqa: E501
                identity=self._alignment_identity(model.retained_rank),
                alignment=alignment,
                reason=(
                    Periodic2DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
                ),
                deficient_sample_count=transport.rank_deficient_link_count,
                minimum_numerical_rank=None,
            )
        if transport.maximum_absolute_closure_phases is None:
            raise RuntimeError("applicable transport must retain closure phases")
        if transport.maximum_plaquette_phase is None:
            raise RuntimeError("periodic-2D transport must retain a plaquette phase")
        comparison_series = self._ordinary_series(
            self._request.construction_size,
            self._transform(reference.source_mesh, comparison_construction),
        )
        if not np.array_equal(
            reference.ordinary_series.integer_modes,
            comparison_series.integer_modes,
        ):
            raise RuntimeError("reference and comparison Fourier inventories differ")
        comparison_full_construction = self._evaluate(
            reference.source_mesh,
            comparison_series,
            reference.construction_axes,
        )
        comparison_full_evaluation = self._evaluate(
            reference.source_mesh,
            comparison_series,
            reference.evaluation_axes,
        )
        comparison_locality = self._hopping_locality(
            model=model,
            channel=Periodic2DRankNHoppingLocalityChannelEnum.COMPARISON,
            series=comparison_series,
            metric_indices=reference.metric_indices,
        )
        comparison_shell_evaluation = tuple(
            iter_complete_shell_fields(
                reference.source_mesh,
                comparison_series,
                reference.evaluation_axes,
                reference.metric_indices,
                reference.metric_shell_values,
            )
        )
        shell_results: list[
            Periodic2DRankNBandEquivalenceHoppingLocalityShellAnalysis
        ] = []
        reference_total_errors: list[BandEquivalenceHoppingLocalityErrorChannels] = []
        comparison_total_errors: list[BandEquivalenceHoppingLocalityErrorChannels] = []
        for ordinal, (metric_value, reference_eval, comparison_eval) in enumerate(
            zip(
                reference.metric_shell_values,
                reference.shell_evaluation_fields,
                comparison_shell_evaluation,
                strict=True,
            )
        ):
            retained = reference.metric_indices <= metric_value
            reference_truncation = error_channels(
                reference_eval,
                reference.full_evaluation,
            )
            comparison_truncation = error_channels(
                comparison_eval,
                comparison_full_evaluation,
            )
            reference_total = error_channels(reference_eval, reference_evaluation)
            comparison_total = error_channels(comparison_eval, comparison_evaluation)
            reference_total_errors.append(reference_total)
            comparison_total_errors.append(comparison_total)
            shell_results.append(
                Periodic2DRankNBandEquivalenceHoppingLocalityShellAnalysis(
                    ordinal_shell_index=ordinal,
                    metric_shell_value=metric_value,
                    retained_block_count=int(np.count_nonzero(retained)),
                    reference_shell_power=reference.locality.normalized_power_at_shell(
                        metric_value
                    ),
                    comparison_shell_power=comparison_locality.normalized_power_at_shell(
                        metric_value
                    ),
                    reference_omitted_power=reference.locality.normalized_power_beyond_shell(
                        metric_value
                    ),
                    comparison_omitted_power=comparison_locality.normalized_power_beyond_shell(
                        metric_value
                    ),
                    reference_total_errors=self._error_record(reference_total),
                    comparison_total_errors=self._error_record(comparison_total),
                    reference_truncation_errors=self._error_record(
                        reference_truncation
                    ),
                    comparison_truncation_errors=self._error_record(
                        comparison_truncation
                    ),
                )
            )
        direct_spectrum_difference = float(
            np.max(
                np.abs(
                    np.linalg.eigvalsh(reference_evaluation)
                    - np.linalg.eigvalsh(comparison_evaluation)
                )
            )
        )
        return Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis(
            identity=self._alignment_identity(model.retained_rank),
            alignment=alignment,
            alignment_evidence=evidence,
            maximum_aligned_frame_defect=maximum_matrix_defect(
                aligned_frame,
                reference_frame,
            ),
            minimum_transport_singular_value=transport.minimum_singular_value,
            maximum_transport_procrustes_residual=(
                transport.maximum_procrustes_residual
            ),
            maximum_transport_unitarity_defect=transport.maximum_unitarity_defect,
            maximum_transport_rank_cutoff=transport.maximum_rank_cutoff,
            maximum_absolute_closure_phases=(transport.maximum_absolute_closure_phases),
            maximum_plaquette_phase=transport.maximum_plaquette_phase,
            maximum_direct_matrix_difference=maximum_matrix_defect(
                comparison_evaluation,
                reference_evaluation,
            ),
            maximum_direct_ordered_spectrum_difference=direct_spectrum_difference,
            reference_reconstruction_errors=self._error_record(
                error_channels(reference.full_construction, reference_construction)
            ),
            comparison_reconstruction_errors=self._error_record(
                error_channels(
                    comparison_full_construction,
                    comparison_construction,
                )
            ),
            reference_interpolation_errors=self._error_record(
                error_channels(reference.full_evaluation, reference_evaluation)
            ),
            comparison_interpolation_errors=self._error_record(
                error_channels(comparison_full_evaluation, comparison_evaluation)
            ),
            reference_locality=self._locality_summary(reference.locality),
            comparison_locality=self._locality_summary(comparison_locality),
            shells=tuple(shell_results),
            tolerance_decisions=self._decisions(
                model=model,
                reference_errors=tuple(reference_total_errors),
                comparison_errors=tuple(comparison_total_errors),
                reference=reference,
            ),
        )

    def _case(
        self,
        model: Periodic2DRankNAnalyticCase,
        geometry: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        construction: Float64Array,
        evaluation: Float64Array,
    ) -> Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis:
        reference_construction = model.exact_reduced_hamiltonians(construction)
        reference_evaluation = model.exact_reduced_hamiltonians(evaluation)
        reference_frame = model.reference_frames(construction)
        attacked_frame = model.attacked_frames(construction)
        attacked_construction = model.attacked_reduced_hamiltonians(construction)
        attacked_evaluation = model.attacked_reduced_hamiltonians(evaluation)
        reference = self._reference_fourier(
            model=model,
            geometry=geometry,
            construction_values=reference_construction,
        )
        alignments: list[
            Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
            | Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
        ] = []
        for alignment in self._request.gauge_alignments:
            if alignment is Periodic2DRankNGaugeAlignment.IDENTITY:
                alignments.append(
                    self._qualified_alignment(
                        model=model,
                        geometry=geometry,
                        alignment=alignment,
                        evidence=Periodic2DRankNPrescribedAlignmentEvidence("identity"),
                        aligned_frame=attacked_frame,
                        comparison_construction=attacked_construction,
                        comparison_evaluation=attacked_evaluation,
                        reference_construction=reference_construction,
                        reference_evaluation=reference_evaluation,
                        reference_frame=reference_frame,
                        reference=reference,
                    )
                )
                continue
            if alignment is Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE:
                construction_action = model.known_inverse_right_actions(construction)
                evaluation_action = model.known_inverse_right_actions(evaluation)
                alignments.append(
                    self._qualified_alignment(
                        model=model,
                        geometry=geometry,
                        alignment=alignment,
                        evidence=Periodic2DRankNPrescribedAlignmentEvidence(
                            "known-inverse-oracle"
                        ),
                        aligned_frame=attacked_frame @ construction_action,
                        comparison_construction=self._apply_right_action(
                            attacked_construction,
                            construction_action,
                        ),
                        comparison_evaluation=self._apply_right_action(
                            attacked_evaluation,
                            evaluation_action,
                        ),
                        reference_construction=reference_construction,
                        reference_evaluation=reference_evaluation,
                        reference_frame=reference_frame,
                        reference=reference,
                    )
                )
                continue
            if alignment is Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY:
                global_analysis = Periodic2DRankNGlobalGaugeAlignmentAnalyzer(
                    request=Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest(
                        retained_rank=model.retained_rank,
                        source=attacked_frame,
                        target=reference_frame,
                        tolerance=self._request.procrustes_tolerance,
                    )
                ).execute()
                outcome = global_analysis.selection_outcome
                if type(outcome) is Periodic2DRankNGlobalGaugeAlignmentRankDeficient:
                    alignments.append(
                        Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                            identity=self._alignment_identity(model.retained_rank),
                            alignment=alignment,
                            reason=(
                                Periodic2DRankNAlignmentInapplicabilityEnum.AGGREGATE_RANK_DEFICIENT
                            ),
                            deficient_sample_count=1,
                            minimum_numerical_rank=outcome.numerical_rank,
                        )
                    )
                    continue
                if type(outcome) is not Periodic2DRankNGlobalGaugeAlignmentSelected:
                    raise RuntimeError("global alignment returned an unknown outcome")
                action = outcome.right_unitary
                alignments.append(
                    self._qualified_alignment(
                        model=model,
                        geometry=geometry,
                        alignment=alignment,
                        evidence=self._fitted_evidence(global_analysis),
                        aligned_frame=attacked_frame @ action,
                        comparison_construction=self._apply_right_action(
                            attacked_construction,
                            action,
                        ),
                        comparison_evaluation=self._apply_right_action(
                            attacked_evaluation,
                            action,
                        ),
                        reference_construction=reference_construction,
                        reference_evaluation=reference_evaluation,
                        reference_frame=reference_frame,
                        reference=reference,
                    )
                )
                continue
            construction_analysis = Periodic2DRankNProcrustesAnalyzer(
                request=Periodic2DRankNProcrustesAnalysisRequest(
                    retained_rank=model.retained_rank,
                    source=attacked_frame,
                    target=reference_frame,
                    tolerance=self._request.procrustes_tolerance,
                )
            ).execute()
            if construction_analysis.owner_result.rank_deficient_count > 0:
                alignments.append(
                    Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                        identity=self._alignment_identity(model.retained_rank),
                        alignment=alignment,
                        reason=(
                            Periodic2DRankNAlignmentInapplicabilityEnum.POINTWISE_CONSTRUCTION_RANK_DEFICIENT
                        ),
                        deficient_sample_count=(
                            construction_analysis.owner_result.rank_deficient_count
                        ),
                        minimum_numerical_rank=int(
                            np.min(construction_analysis.owner_result.numerical_ranks)
                        ),
                    )
                )
                continue
            attacked_eval_frame = model.attacked_frames(evaluation)
            reference_eval_frame = model.reference_frames(evaluation)
            evaluation_analysis = Periodic2DRankNProcrustesAnalyzer(
                request=Periodic2DRankNProcrustesAnalysisRequest(
                    retained_rank=model.retained_rank,
                    source=attacked_eval_frame,
                    target=reference_eval_frame,
                    tolerance=self._request.procrustes_tolerance,
                )
            ).execute()
            if evaluation_analysis.owner_result.rank_deficient_count > 0:
                alignments.append(
                    Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                        identity=self._alignment_identity(model.retained_rank),
                        alignment=alignment,
                        reason=(
                            Periodic2DRankNAlignmentInapplicabilityEnum.POINTWISE_EVALUATION_RANK_DEFICIENT
                        ),
                        deficient_sample_count=(
                            evaluation_analysis.owner_result.rank_deficient_count
                        ),
                        minimum_numerical_rank=int(
                            np.min(evaluation_analysis.owner_result.numerical_ranks)
                        ),
                    )
                )
                continue
            construction_action = (
                construction_analysis.owner_result.right_unitary_completions
            )
            evaluation_action = (
                evaluation_analysis.owner_result.right_unitary_completions
            )
            alignments.append(
                self._qualified_alignment(
                    model=model,
                    geometry=geometry,
                    alignment=alignment,
                    evidence=self._fitted_evidence(
                        construction_analysis,
                        evaluation_analysis,
                    ),
                    aligned_frame=attacked_frame @ construction_action,
                    comparison_construction=self._apply_right_action(
                        attacked_construction,
                        construction_action,
                    ),
                    comparison_evaluation=self._apply_right_action(
                        attacked_evaluation,
                        evaluation_action,
                    ),
                    reference_construction=reference_construction,
                    reference_evaluation=reference_evaluation,
                    reference_frame=reference_frame,
                    reference=reference,
                )
            )
        retained = model.retained_energies(construction)
        exterior = model.exterior_energies(construction)
        minimum_gap = float(
            np.min(exterior[..., 0] - retained[..., model.retained_rank - 1])
        )
        return Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis(
            model_identity=model.model_identity,
            case_identifier=model.case_identifier,
            retained_rank=model.retained_rank,
            circuit_depth=model.circuit_depth,
            parent_scale=model.parent_scale,
            attack_coefficient=model.attack_coefficient,
            minimum_sampled_external_gap=minimum_gap,
            alignments=tuple(alignments),
        )

    def execute(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis:
        """Execute one analytic case without creating retained evidence."""
        construction = self._coordinates(self._request.construction_size, 0.5)
        evaluation = self._coordinates(
            self._request.evaluation_size,
            0.5 + self._request.evaluation_shift,
        )
        return self._case(
            self._model,
            self._geometry,
            construction,
            evaluation,
        )


@final
class Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer(
    Periodic2DRankNBandEquivalenceAnalyzer[
        Periodic2DRankNBandEquivalenceHoppingLocalityRequest
    ]
):
    """Thinly expand and sequence one exact aggregate software request."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
    ) -> None:
        if type(request) is not Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        self._request = request

    @property
    def request(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
        """Return the immutable aggregate request bound to this action."""
        return self._request

    def execute(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis:
        """Execute all analytic cases without creating retained evidence."""
        geometry_by_identifier = {case.identifier: case for case in self._request.cases}
        models = Periodic2DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=self._request
        ).execute()
        cases = tuple(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
                request=self._request,
                model=model,
                geometry=geometry_by_identifier[model.case_identifier],
            ).execute()
            for model in models
        )
        return Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis(
            request=self._request,
            status=(
                Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum.SOFTWARE_QUALIFICATION_NOT_SCIENTIFIC_EVIDENCE
            ),
            cases=cases,
        )


__all__ = [
    "Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer",
]
